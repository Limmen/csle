import numpy as np
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.dfsp_local.dfsp_local_agent import DFSPLocalAgent
import csle_agents.constants.constants as agents_constants
import gym_csle_intrusion_response_game.constants.constants as env_constants
from gym_csle_intrusion_response_game.util.intrusion_response_game_util import IntrusionResponseGameUtil
from gym_csle_intrusion_response_game.dao.local_intrusion_response_game_config import LocalIntrusionResponseGameConfig
from csle_common.dao.training.tabular_policy import TabularPolicy
from csle_common.dao.training.policy_type import PolicyType


def reduce_T(T, strategy):
    """
    Reduces the transition tensor based on a given strategy

    :param T: the tensor to reduce
    :param strategy: the strategy to use for the reduction
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
    Reduces the reward tensor based on a given strategy

    :param R: the reward tensor to reduce
    :param strategy: the strategy to use for the reduction
    :return: the reduced reward tensor
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
    emulation_name = "csle-level9-070"
    emulation_env_config = MetastoreFacade.get_emulation_by_name(emulation_name)
    if emulation_env_config is None:
        raise ValueError(f"Could not find an emulation environment with the name: {emulation_name}")
    defender_simulation_name = "csle-intrusion-response-game-local-pomdp-defender-001"
    defender_simulation_env_config = MetastoreFacade.get_simulation_by_name(defender_simulation_name)
    if defender_simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {defender_simulation_name}")
    attacker_simulation_name = "csle-intrusion-response-game-local-pomdp-attacker-001"
    attacker_simulation_env_config = MetastoreFacade.get_simulation_by_name(attacker_simulation_name)
    if attacker_simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {attacker_simulation_name}")
    ppo_experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}dfsp_local_test",
        title="Local DFSP intrusion response",
        random_seeds=[399, 98912, 999], agent_type=AgentType.DFSP_LOCAL,
        log_every=1,
        hparams={
            constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER: HParam(
                value=64, name=constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER,
                descr="neurons per hidden layer of the policy network"),
            constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS: HParam(
                value=4, name=constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS,
                descr="number of layers of the policy network"),
            agents_constants.PPO.STEPS_BETWEEN_UPDATES: HParam(
                value=4096, name=agents_constants.PPO.STEPS_BETWEEN_UPDATES,
                descr="number of steps in the environment for doing rollouts between policy updates"),
            agents_constants.COMMON.BATCH_SIZE: HParam(value=64, name=agents_constants.COMMON.BATCH_SIZE,
                                                       descr="batch size for updates"),
            agents_constants.COMMON.LEARNING_RATE: HParam(value=0.0001,
                                                          name=agents_constants.COMMON.LEARNING_RATE,
                                                          descr="learning rate for updating the policy"),
            constants.NEURAL_NETWORKS.DEVICE: HParam(value="cpu",
                                                     name=constants.NEURAL_NETWORKS.DEVICE,
                                                     descr="the device to train on (cpu or cuda:x)"),
            agents_constants.COMMON.NUM_PARALLEL_ENVS: HParam(
                value=1, name=agents_constants.COMMON.NUM_PARALLEL_ENVS,
                descr="the nunmber of parallel environments for training"),
            agents_constants.COMMON.GAMMA: HParam(
                value=0.99, name=agents_constants.COMMON.GAMMA, descr="the discount factor"),
            agents_constants.PPO.GAE_LAMBDA: HParam(
                value=0.95, name=agents_constants.PPO.GAE_LAMBDA, descr="the GAE weighting term"),
            agents_constants.PPO.CLIP_RANGE: HParam(
                value=0.2, name=agents_constants.PPO.CLIP_RANGE, descr="the clip range for PPO"),
            agents_constants.PPO.CLIP_RANGE_VF: HParam(
                value=None, name=agents_constants.PPO.CLIP_RANGE_VF,
                descr="the clip range for PPO-update of the value network"),
            agents_constants.PPO.ENT_COEF: HParam(
                value=0.0, name=agents_constants.PPO.ENT_COEF,
                descr="the entropy coefficient for exploration"),
            agents_constants.PPO.VF_COEF: HParam(value=0.5, name=agents_constants.PPO.VF_COEF,
                                                 descr="the coefficient of the value network for the loss"),
            agents_constants.PPO.MAX_GRAD_NORM: HParam(
                value=0.5, name=agents_constants.PPO.MAX_GRAD_NORM, descr="the maximum allows gradient norm"),
            agents_constants.PPO.TARGET_KL: HParam(value=None,
                                                   name=agents_constants.PPO.TARGET_KL,
                                                   descr="the target kl"),
            agents_constants.COMMON.NUM_TRAINING_TIMESTEPS: HParam(
                value=int(200000), name=agents_constants.COMMON.NUM_TRAINING_TIMESTEPS,
                descr="number of timesteps to train"),
            agents_constants.COMMON.EVAL_EVERY: HParam(value=10, name=agents_constants.COMMON.EVAL_EVERY,
                                                       descr="training iterations between evaluations"),
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=50, name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="the batch size for evaluation"),
            agents_constants.COMMON.SAVE_EVERY: HParam(value=1000000, name=agents_constants.COMMON.SAVE_EVERY,
                                                       descr="how frequently to save the model"),
            agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                value=0.95, name=agents_constants.COMMON.CONFIDENCE_INTERVAL,
                descr="confidence interval"),
            agents_constants.COMMON.MAX_ENV_STEPS: HParam(
                value=200, name=agents_constants.COMMON.MAX_ENV_STEPS,
                descr="maximum number of steps in the environment (for envs with infinite horizon generally)"),
            agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                value=100, name=agents_constants.COMMON.RUNNING_AVERAGE,
                descr="the number of samples to include when computing the running avg"),
            agents_constants.LOCAL_DFSP.N_2: HParam(
                value=100, name=agents_constants.LOCAL_DFSP.N_2, descr="the number of iterations of self-play"),
            agents_constants.LOCAL_DFSP.BEST_RESPONSE_EVALUATION_ITERATIONS: HParam(
                value=50, name=agents_constants.T_FP.BEST_RESPONSE_EVALUATION_ITERATIONS,
                descr="number of iterations to evaluate best response strategies when calculating exploitability"),
            agents_constants.LOCAL_DFSP.EQUILIBRIUM_STRATEGIES_EVALUATION_ITERATIONS: HParam(
                value=50, name=agents_constants.T_FP.EQUILIBRIUM_STRATEGIES_EVALUATION_ITERATIONS,
                descr="number of iterations to evaluate equilibrium strategies in each iteration")
        },
        player_type=PlayerType.ATTACKER, player_idx=0
    )

    de_experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}differential_evolution_test",
        title="Differential evolution test",
        random_seeds=[399],
        agent_type=AgentType.DIFFERENTIAL_EVOLUTION,
        log_every=1,
        hparams={
            agents_constants.DIFFERENTIAL_EVOLUTION.N: HParam(value=20, name=constants.T_SPSA.N,
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
    stopping_env = "csle-intrusion-response-game-local-stopping-pomdp-defender-v1"
    defender_simulation_env_config.gym_env_name = stopping_env
    ppo_experiment_config.name = "dfsp_local_self_play"
    number_of_zones = 6
    X_max = 100
    eta = 0.5
    reachable = True
    beta = 3
    gamma = 0.99
    initial_zone = 3
    initial_state = [initial_zone, 0]
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
    R = np.array(
        [IntrusionResponseGameUtil.local_reward_tensor(eta=eta, C_D=C_D, A1=A1, A2=A2, reachable=reachable, beta=beta,
                                                       S=S, Z_U=Z_U, initial_zone=initial_zone)])
    d_b1 = IntrusionResponseGameUtil.local_initial_defender_belief(S_A=S_A)
    a_b1 = IntrusionResponseGameUtil.local_initial_attacker_belief(S_D=S_D, initial_zone=initial_zone)
    initial_state_idx = states_to_idx[(initial_state[env_constants.STATES.D_STATE_INDEX],
                                       initial_state[env_constants.STATES.A_STATE_INDEX])]
    env_name = "csle-intrusion-response-game-pomdp-defender-v1"
    attacker_stage_strategy = np.zeros((len(IntrusionResponseGameUtil.local_attacker_state_space()), len(A2)))
    for i, s_a in enumerate(IntrusionResponseGameUtil.local_attacker_state_space()):
        if s_a == env_constants.ATTACK_STATES.HEALTHY:
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.WAIT] = 0.8
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.RECON] = 0.2
        elif s_a == env_constants.ATTACK_STATES.RECON:
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.WAIT] = 0.7
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.BRUTE_FORCE] = 0.15
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.EXPLOIT] = 0.15
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
    defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config = \
        LocalIntrusionResponseGameConfig(
            env_name=env_name, T=T, O=O, Z=Z, R=R, S=S, S_A=S_A, S_D=S_D, s_1_idx=initial_state_idx, zones=zones,
            A1=A1, A2=A2, d_b1=d_b1, a_b1=a_b1, gamma=gamma, beta=beta, C_D=C_D, A_P=A_P, Z_D_P=Z_D_P, Z_U=Z_U,
            eta=eta
        )
    env_name = "csle-intrusion-response-game-pomdp-attacker-v1"
    defender_stage_strategy = np.zeros((len(IntrusionResponseGameUtil.local_defender_state_space(
        number_of_zones=number_of_zones)), len(A1)))
    for i, s_d in enumerate(IntrusionResponseGameUtil.local_defender_state_space(number_of_zones=number_of_zones)):
        defender_stage_strategy[i][env_constants.DEFENDER_ACTIONS.WAIT] = 0.95
        for z in zones:
            defender_stage_strategy[i][z] = 0.05 / len(zones)
    defender_strategy = TabularPolicy(
        player_type=PlayerType.DEFENDER,
        actions=A1,
        simulation_name="csle-intrusion-response-game-pomdp-attacker-001",
        value_function=None, q_table=None,
        lookup_table=list(defender_stage_strategy.tolist()),
        agent_type=AgentType.RANDOM, avg_R=-1)
    attacker_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config = \
        LocalIntrusionResponseGameConfig(
            env_name=env_name, T=T, O=O, Z=Z, R=R, S=S, S_A=S_A, S_D=S_D, s_1_idx=initial_state_idx, zones=zones,
            A1=A1, A2=A2, d_b1=d_b1, a_b1=a_b1, gamma=gamma, beta=beta, C_D=C_D, A_P=A_P, Z_D_P=Z_D_P, Z_U=Z_U,
            eta=eta
        )
    attacker_simulation_env_config.simulation_env_input_config.defender_strategy = defender_strategy
    attacker_simulation_env_config.simulation_env_input_config.attacker_strategy = attacker_strategy
    defender_simulation_env_config.simulation_env_input_config.defender_strategy = defender_strategy
    defender_simulation_env_config.simulation_env_input_config.attacker_strategy = attacker_strategy

    # VI config
    T = IntrusionResponseGameUtil.local_stopping_mdp_transition_tensor(
        S=defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.S,
        A1=defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.A1,
        A2=defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.A2,
        S_D=defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.S_D,
        T=defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.T[0]
    )
    T = reduce_T(T=T, strategy=attacker_strategy)
    R = IntrusionResponseGameUtil.local_stopping_mdp_reward_tensor(
        S=defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.S,
        A1=defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.A1,
        A2=defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.A2,
        R=defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.R[0],
        S_D=defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.S_D
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
                value=0.0001, name=agents_constants.VI.THETA,
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

    agent = DFSPLocalAgent(emulation_env_config=emulation_env_config,
                           attacker_simulation_env_config=attacker_simulation_env_config,
                           defender_simulation_env_config=defender_simulation_env_config,
                           ppo_experiment_config=ppo_experiment_config,
                           de_experiment_config=de_experiment_config,
                           vi_experiment_config=vi_experiment_config)
    experiment_execution = agent.train()

    # MetastoreFacade.save_experiment_execution(experiment_execution)
    # for policy in experiment_execution.result.policies.values():
    #     MetastoreFacade.save_ppo_policy(ppo_policy=policy)
