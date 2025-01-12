from typing import List
import numpy as np
from multiprocessing import Process, Manager
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType
import gym_csle_intrusion_response_game.constants.constants as env_constants
from gym_csle_intrusion_response_game.util.intrusion_response_game_util import IntrusionResponseGameUtil
from gym_csle_intrusion_response_game.dao.workflow_intrusion_response_game_config \
    import WorkflowIntrusionResponseGameConfig
from csle_common.dao.training.tabular_policy import TabularPolicy
from gym_csle_intrusion_response_game.envs.intrusion_response_game_workflow_pomdp_defender \
    import IntrusionResponseGameWorkflowPOMDPDefenderEnv
import csle_agents.constants.constants as agents_constants
from csle_common.dao.training.hparam import HParam
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.policy_type import PolicyType
from csle_agents.agents.differential_evolution.differential_evolution_agent import DifferentialEvolutionAgent
from csle_agents.agents.vi.vi_agent import VIAgent


def is_node_reachable(node: int, gw_reachable: List, adjacency_matrix: List, num_nodes: int, local_envs: List) -> bool:
    """
    Checks if a node is reachable from the gw

    :param node: the node to check
    :return: True if reachable otherwise False
    """
    A = adjacency_matrix.copy()
    for i, local_env in enumerate(local_envs):
        if local_env.state.defender_state() in [env_constants.DEFENDER_STATES.SHUTDOWN,
                                                env_constants.DEFENDER_STATES.REDIRECT]:
            A[i] = [0] * num_nodes
    gw_reachable_nodes = gw_reachable
    A = np.array(A)
    for i in range(1, num_nodes + 1):
        A_n = np.linalg.matrix_power(A, i)
        for gw_reachable in gw_reachable_nodes:
            if A_n[gw_reachable][node] != 0:
                return True
    return False


def get_descendants(node, adjacency_matrix: List, num_nodes: int) -> List[int]:
    """
    Utility function to get the descendants of a node

    :param node: the node to get descendants of
    :param adjacency_matrix: the adjacency matrix
    :param num_nodes: the total number of nodes
    :return: a list with the descendants (node ids)
    """
    reachable = []
    A = adjacency_matrix.copy()
    A = np.array(A)
    for i in range(1, num_nodes + 1):
        A_n = np.linalg.matrix_power(A, i)
        for i in range(num_nodes):
            if i != node and A_n[node][i] != 0:
                if i not in reachable:
                    reachable.append(i)
    return reachable


def reduce_T(T, strategy):
    """
    Utility function for reducing the T tensor based on a given strategy

    :param T: the tensor to reduce
    :param strategy: the strategy for the reduction
    :return: the reduced tensor
    """
    attacker_state = 2
    reduced_T = np.zeros((T.shape[0], T.shape[2], T.shape[3]))
    for i in range(T.shape[0]):
        for j in range(T.shape[2]):
            for k in range(T.shape[3]):
                prob = 0
                for a2 in range(T.shape[1]):
                    prob += strategy.probability(attacker_state, a2) * T[i][a2][j][k]
                reduced_T[i][j][k] = prob
    return reduced_T


def reduce_R(R, strategy):
    """
    Utility function for reducing a reward tensor based on a given strategy

    :param R: the reward tensor to reduce
    :param strategy: the strategy to use for the reduction
    :return: the reduced tensor
    """
    attacker_state = 2
    reduced_R = np.zeros((R.shape[0], R.shape[2]))
    for i in range(R.shape[0]):
        for j in range(R.shape[2]):
            r = 0
            for a2 in range(R.shape[1]):
                r += strategy.probability(attacker_state, a2) * R[i][a2][j]
            reduced_R[i][j] = r
    return reduced_R


if __name__ == '__main__':

    # Workflow Env Config
    emulation_name = "csle-level9-070"
    emulation_env_config = MetastoreFacade.get_emulation_by_name(emulation_name)
    if emulation_env_config is None:
        raise ValueError(f"Could not find an emulation environment with the name: {emulation_name}")
    simulation_name = "csle-intrusion-response-game-workflow-pomdp-defender-001"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    num_nodes = 15
    number_of_zones = 6
    X_max = 100
    eta = 0.5
    reachable = True
    beta = 3
    gamma = 0.99
    zones = IntrusionResponseGameUtil.zones(num_zones=number_of_zones)
    Z_D_P = np.array([0, 0.8, 0.5, 0.1, 0.05, 0.025])
    S = IntrusionResponseGameUtil.local_state_space(number_of_zones=number_of_zones)
    states_to_idx = {}
    for i, s in enumerate(S):
        states_to_idx[(s[env_constants.STATES.D_STATE_INDEX], s[env_constants.STATES.A_STATE_INDEX])] = i
    S_A = IntrusionResponseGameUtil.local_attacker_state_space()
    S_D = IntrusionResponseGameUtil.local_defender_state_space(number_of_zones=number_of_zones)
    A1 = IntrusionResponseGameUtil.local_defender_actions(number_of_zones=number_of_zones)
    C_D = np.array([0, 35, 30, 25, 20, 20, 20, 15])
    A2 = IntrusionResponseGameUtil.local_attacker_actions()
    A_P = np.array([1, 1, 0.75, 0.85])
    O = IntrusionResponseGameUtil.local_observation_space(X_max=X_max)
    T = np.array([IntrusionResponseGameUtil.local_transition_tensor(S=S, A1=A1, A2=A2, Z_D=Z_D_P, A_P=A_P)])
    Z = IntrusionResponseGameUtil.local_observation_tensor_betabinom(S=S, A1=A1, A2=A2, O=O)
    Z_U = np.array([0, 0, 2.5, 5, 10, 15])
    env_name = "csle-intrusion-response-game-pomdp-defender-v1"
    attacker_stage_strategy = np.zeros((len(IntrusionResponseGameUtil.local_attacker_state_space()), len(A2)))
    for i, s_a in enumerate(IntrusionResponseGameUtil.local_attacker_state_space()):
        if s_a == env_constants.ATTACK_STATES.HEALTHY:
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.WAIT] = 0.9
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.RECON] = 0.1
        elif s_a == env_constants.ATTACK_STATES.RECON:
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.WAIT] = 0
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.BRUTE_FORCE] = 0.5
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.EXPLOIT] = 0.5
        else:
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.WAIT] = 1
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.BRUTE_FORCE] = 0.
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.EXPLOIT] = 0
    attacker_strategy = TabularPolicy(
        player_type=PlayerType.ATTACKER, actions=A2,
        simulation_name="csle-intrusion-response-game-pomdp-defender-001",
        value_function=None, q_table=None,
        lookup_table=list(attacker_stage_strategy.tolist()),
        agent_type=AgentType.RANDOM, avg_R=-1)
    gw_reachable = np.array([0])
    adjacency_matrix = [
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    adjacency_matrix = np.array(adjacency_matrix)
    A_n = np.linalg.matrix_power(adjacency_matrix, 2)
    nodes = np.array(list(range(num_nodes)))
    initial_zones = []
    possible_inital_zones = zones[2:]
    attacker_strategies = []
    initial_zones = [
        4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5
    ]
    for node in nodes:
        attacker_strategies.append(attacker_strategy)
    initial_zones = np.array(initial_zones)
    simulation_env_config.simulation_env_input_config.game_config = WorkflowIntrusionResponseGameConfig(
        env_name="csle-intrusion-response-game-workflow-pomdp-defender-v1",
        nodes=nodes, initial_zones=initial_zones, X_max=X_max, beta=beta, gamma=gamma,
        zones=zones, Z_D_P=Z_D_P, C_D=C_D, A_P=A_P, Z_U=Z_U, adjacency_matrix=adjacency_matrix, eta=eta,
        gw_reachable=gw_reachable
    )
    simulation_env_config.simulation_env_input_config.attacker_strategies = attacker_strategies
    env = IntrusionResponseGameWorkflowPOMDPDefenderEnv(config=simulation_env_config.simulation_env_input_config)

    # DE config
    local_simulation_env_config = MetastoreFacade.get_simulation_by_name(
        "csle-intrusion-response-game-local-pomdp-defender-001")
    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}differential_evolution_test",
        title="Differential evolution test",
        random_seeds=[399],
        agent_type=AgentType.DIFFERENTIAL_EVOLUTION,
        log_every=1,
        hparams={
            agents_constants.DIFFERENTIAL_EVOLUTION.N: HParam(value=50, name=constants.T_SPSA.N,
                                                              descr="the number of training iterations"),
            agents_constants.DIFFERENTIAL_EVOLUTION.L: HParam(value=2, name="L", descr="the number of stop actions"),
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=10, name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="number of iterations to evaluate theta"),
            agents_constants.DIFFERENTIAL_EVOLUTION.THETA1: HParam(value=[0.6, 1.1],
                                                                   name=constants.T_SPSA.THETA1,
                                                                   descr="initial thresholds"),
            agents_constants.DIFFERENTIAL_EVOLUTION.POPULATION_SIZE: HParam(
                value=10, name=agents_constants.DIFFERENTIAL_EVOLUTION.POPULATION_SIZE,
                descr="population size"),
            agents_constants.DIFFERENTIAL_EVOLUTION.MUTATE: HParam(
                value=0.2, name=agents_constants.DIFFERENTIAL_EVOLUTION.MUTATE,
                descr="mutate step"),
            agents_constants.DIFFERENTIAL_EVOLUTION.RECOMBINATION: HParam(
                value=0.7, name=agents_constants.DIFFERENTIAL_EVOLUTION.RECOMBINATION,
                descr="number of recombinations"),
            agents_constants.DIFFERENTIAL_EVOLUTION.BOUNDS: HParam(
                value=[(-5, 5) for l in range(2)], name=agents_constants.DIFFERENTIAL_EVOLUTION.BOUNDS,
                descr="parameter bounds"),
            agents_constants.COMMON.SAVE_EVERY: HParam(value=1000, name=agents_constants.COMMON.SAVE_EVERY,
                                                       descr="how frequently to save the model"),
            agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                value=0.95, name=agents_constants.COMMON.CONFIDENCE_INTERVAL,
                descr="confidence interval"),
            agents_constants.COMMON.MAX_ENV_STEPS: HParam(
                value=100, name=agents_constants.COMMON.MAX_ENV_STEPS,
                descr="maximum number of steps in the environment (for envs with infinite horizon generally)"),
            agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                value=100, name=agents_constants.COMMON.RUNNING_AVERAGE,
                descr="the number of samples to include when computing the running avg"),
            agents_constants.COMMON.GAMMA: HParam(
                value=0.99, name=agents_constants.COMMON.GAMMA,
                descr="the discount factor"),
            agents_constants.DIFFERENTIAL_EVOLUTION.POLICY_TYPE: HParam(
                value=PolicyType.LINEAR_THRESHOLD, name=agents_constants.DIFFERENTIAL_EVOLUTION.POLICY_TYPE,
                descr="policy type for the execution")
        },
        player_type=PlayerType.DEFENDER, player_idx=0
    )

    # VI config
    T = IntrusionResponseGameUtil.local_stopping_mdp_transition_tensor(
        S=env.local_envs[0].config.local_intrusion_response_game_config.S,
        A1=env.local_envs[0].config.local_intrusion_response_game_config.A1,
        A2=env.local_envs[0].config.local_intrusion_response_game_config.A2,
        S_D=env.local_envs[0].config.local_intrusion_response_game_config.S_D,
        T=env.local_envs[0].config.local_intrusion_response_game_config.T[0]
    )
    T = reduce_T(T=T, strategy=attacker_strategy)
    R = IntrusionResponseGameUtil.local_stopping_mdp_reward_tensor(
        S=env.local_envs[0].config.local_intrusion_response_game_config.S,
        A1=env.local_envs[0].config.local_intrusion_response_game_config.A1,
        A2=env.local_envs[0].config.local_intrusion_response_game_config.A2,
        R=env.local_envs[0].config.local_intrusion_response_game_config.R[0],
        S_D=env.local_envs[0].config.local_intrusion_response_game_config.S_D
    )
    R = reduce_R(R=R, strategy=attacker_strategy)

    vi_experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}vi_test",
        title="Value iteration computation",
        random_seeds=[399], agent_type=AgentType.VALUE_ITERATION,
        log_every=1,
        hparams={
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=100,
                                                            name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="number of iterations to evaluate theta"),
            agents_constants.COMMON.EVAL_EVERY: HParam(value=1,
                                                       name=agents_constants.COMMON.EVAL_EVERY,
                                                       descr="how frequently to run evaluation"),
            agents_constants.COMMON.SAVE_EVERY: HParam(value=1000, name=agents_constants.COMMON.SAVE_EVERY,
                                                       descr="how frequently to save the model"),
            agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                value=0.95, name=agents_constants.COMMON.CONFIDENCE_INTERVAL,
                descr="confidence interval"),
            agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                value=100, name=agents_constants.COMMON.RUNNING_AVERAGE,
                descr="the number of samples to include when computing the running avg"),
            agents_constants.COMMON.GAMMA: HParam(
                value=gamma, name=agents_constants.COMMON.GAMMA,
                descr="the discount factor"),
            agents_constants.VI.THETA: HParam(
                value=0.001, name=agents_constants.VI.THETA,
                descr="the stopping theshold for value iteration"),
            agents_constants.VI.TRANSITION_TENSOR: HParam(
                value=list(T.tolist()), name=agents_constants.VI.TRANSITION_TENSOR,
                descr="the transition tensor"),
            agents_constants.VI.REWARD_TENSOR: HParam(
                value=list(R.tolist()), name=agents_constants.VI.REWARD_TENSOR,
                descr="the reward tensor"),
            agents_constants.VI.NUM_STATES: HParam(
                value=T.shape[2], name=agents_constants.VI.NUM_STATES,
                descr="the number of states"),
            agents_constants.VI.NUM_ACTIONS: HParam(
                value=T.shape[0], name=agents_constants.VI.NUM_ACTIONS,
                descr="the number of actions")
        },
        player_type=PlayerType.DEFENDER, player_idx=1
    )
    stopping_env = "csle-intrusion-response-game-local-stopping-pomdp-defender-v1"

    # Training
    def optimize_stopping_policy(node, agent, zone, action, return_dict):
        """
        Optimizes the stopping policy for a given node

        :param node: the node to use for the optimization
        :param agent: the agent to use for the optimization
        :param zone: the zone of the node
        :param action: the stopping action
        :param return_dict: the dict to accumulate results
        :return: None
        """
        experiment_execution = agent.train()
        stopping_policy = list(experiment_execution.result.policies.values())[0]
        for zone in zones:
            for zone2 in zones:
                return_dict[f"{node}_{zone}_{zone2}_stopping_policy"] = stopping_policy

    def optimize_defense_policy(node, agent, return_dict):
        """
        Optimizes the defense policy for a given node

        :param node: the node to optimize for
        :param agent: the agent to optimize
        :param return_dict: the return dict to accumulate the results
        :return: None
        """
        experiment_execution = agent.train()
        defense_policy = list(experiment_execution.result.policies.values())[0]
        return_dict[f"{node}_defense_policy"] = defense_policy

    processes = []
    manager = Manager()
    return_dict = manager.dict()
    for i, local_env in enumerate(env.local_envs):
        cfg = local_simulation_env_config.copy()
        cfg.simulation_env_input_config = local_env.config
        cfg.gym_env_name = stopping_env
        # Stopping
        agent = DifferentialEvolutionAgent(
            emulation_env_config=emulation_env_config, simulation_env_config=cfg,
            experiment_config=experiment_config, save_to_metastore=False)
        p = Process(target=optimize_stopping_policy, args=(i, agent, 3, 3, return_dict))
        p.start()
        processes.append(p)
        # for zone in zones:
        #     for zone2 in zones:
        #         cfg.simulation_env_input_config.stopping_zone = zone
        #         cfg.simulation_env_input_config.stopping_action = zone2
        #         # Stopping
        #         agent = DifferentialEvolutionAgent(
        #             emulation_env_config=emulation_env_config, simulation_env_config=cfg,
        #             experiment_config=experiment_config, save_to_metastore=False)
        #         p = Process(target=optimize_stopping_policy, args=(i,agent, zone, zone2, return_dict))
        #         p.start()
        #         processes.append(p)

        # Defense
        T = IntrusionResponseGameUtil.local_stopping_mdp_transition_tensor(
            S=local_env.config.local_intrusion_response_game_config.S,
            A1=local_env.config.local_intrusion_response_game_config.A1,
            A2=local_env.config.local_intrusion_response_game_config.A2,
            S_D=local_env.config.local_intrusion_response_game_config.S_D,
            T=local_env.config.local_intrusion_response_game_config.T[0]
        )
        T = reduce_T(T=T, strategy=attacker_strategy)
        descendants = get_descendants(node=i, adjacency_matrix=adjacency_matrix, num_nodes=num_nodes)
        # topology_cost = beta*len(descendants)
        topology_cost = 0
        R = np.array(
            [IntrusionResponseGameUtil.local_reward_tensor(eta=eta, C_D=C_D, A1=A1, A2=A2, reachable=reachable,
                                                           beta=beta,
                                                           S=S, Z_U=Z_U, initial_zone=initial_zones[i],
                                                           topology_cost=topology_cost)])
        R = IntrusionResponseGameUtil.local_stopping_mdp_reward_tensor(
            S=local_env.config.local_intrusion_response_game_config.S,
            A1=local_env.config.local_intrusion_response_game_config.A1,
            A2=local_env.config.local_intrusion_response_game_config.A2,
            R=R[0],
            S_D=local_env.config.local_intrusion_response_game_config.S_D
        )
        R = reduce_R(R=R, strategy=attacker_strategy)
        vi_experiment_config.hparams[agents_constants.VI.REWARD_TENSOR].value == list(R.tolist())
        vi_experiment_config.hparams[agents_constants.VI.TRANSITION_TENSOR].value == list(T.tolist())
        vi_agent = VIAgent(simulation_env_config=local_simulation_env_config,
                           experiment_config=vi_experiment_config, save_to_metastore=False)
        p = Process(target=optimize_defense_policy, args=(i, vi_agent, return_dict))
        p.start()
        processes.append(p)

    for process in processes:
        process.join()

    stopping_policies = []
    defense_policies = []
    for i in range(len(env.local_envs)):
        defense_policy = return_dict[f"{i}_defense_policy"]
        defense_policies.append(defense_policy)
        policies_1 = []
        for zone in zones:
            policies = []
            for zone2 in zones:
                stopping_policy = return_dict[f"{i}_{zone}_{zone2}_stopping_policy"]
                policies.append(stopping_policy)
            policies_1.append(policies)
        stopping_policies.append(policies_1)
    print(stopping_policies)
    print(np.array(stopping_policies).shape)

    # Evaluation
    num_evals = 50
    returns = []
    for j in range(num_evals):
        observations = []
        for i, local_env in enumerate(env.local_envs):
            o, _ = local_env.reset()
            observations.append(o)
        done = False
        R = 0
        t = 0
        max_steps = 200
        while not done:
            r = 0
            a = []
            states = []
            beliefs = []
            reachability = []
            for i, local_env in enumerate(env.local_envs):
                reachable = is_node_reachable(node=i, gw_reachable=gw_reachable, adjacency_matrix=adjacency_matrix,
                                              local_envs=env.local_envs, num_nodes=num_nodes)
                reachability.append(reachable)
                obs = observations[i]
                zone = int(obs[0])
                b = obs[1:]
                a1 = 0
                if reachable:
                    defensive_action = defense_policies[i].action(zone) + 1
                    a1 = stopping_policies[int(i)][int(zone) - 1][int(defensive_action) - 1].action(b)
                    if a1 == 1:
                        a1 = defensive_action
                local_o, local_r, local_done, _, _ = local_env.step(a1=a1)
                if not reachable:
                    local_r = local_env.config.local_intrusion_response_game_config.C_D[a1]
                    local_o = np.array([local_o[0], 1, 0, 0])
                if local_done:
                    done = True
                r += local_r
                observations[i] = local_o
                a.append(a1)
                states.append(local_env.state.state_vector())
                beliefs.append(local_o[1:])
                # print(f"node {i}, reachable: {reachable}, zone: {zone}, b:{b}, a1:{a1}, done: {done}")
            R += r
            t += 1
            print(f"Step, t:{t} r:{r}, a:{a}, s:{states}, b:{beliefs}, reachability:{reachability}")
            if t >= max_steps:
                done = True
        print(f"RETURN:{R}")
        returns.append(R)
    avg_return = np.mean(returns)
    print(f"Avg return: {avg_return}, upper bound: {env.upper_bound_return}, random baseline: {env.random_return}")

    # MetastoreFacade.save_experiment_execution(experiment_execution)
    # for policy in experiment_execution.result.policies.values():
    #     MetastoreFacade.save_ppo_policy(ppo_policy=policy)
