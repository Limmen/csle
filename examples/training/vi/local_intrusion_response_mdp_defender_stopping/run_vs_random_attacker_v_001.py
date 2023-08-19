import numpy as np
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType
import gym_csle_intrusion_response_game.constants.constants as env_constants
from gym_csle_intrusion_response_game.util.intrusion_response_game_util import IntrusionResponseGameUtil
from gym_csle_intrusion_response_game.dao.local_intrusion_response_game_config import LocalIntrusionResponseGameConfig
from csle_common.dao.training.tabular_policy import TabularPolicy
from csle_agents.agents.vi.vi_agent import VIAgent
from csle_common.dao.training.hparam import HParam
import csle_agents.constants.constants as agents_constants
import gymnasium as gym


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
    simulation_name = "csle-intrusion-response-game-local-pomdp-defender-001"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
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
    simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config = \
        LocalIntrusionResponseGameConfig(
            env_name=env_name, T=T, O=O, Z=Z, R=R, S=S, S_A=S_A, S_D=S_D, s_1_idx=initial_state_idx, zones=zones,
            A1=A1, A2=A2, d_b1=d_b1, a_b1=a_b1, gamma=gamma, beta=beta, C_D=C_D, A_P=A_P, Z_D_P=Z_D_P, Z_U=Z_U,
            eta=eta
        )
    simulation_env_config.simulation_env_input_config.attacker_strategy = attacker_strategy
    env = gym.make(simulation_env_config.gym_env_name, config=simulation_env_config.simulation_env_input_config)
    T = IntrusionResponseGameUtil.local_stopping_mdp_transition_tensor(
        S=simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.S,
        A1=simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.A1,
        A2=simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.A2,
        S_D=simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.S_D,
        T=simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.T[0]
    )
    T = reduce_T(T=T, strategy=attacker_strategy)
    R = IntrusionResponseGameUtil.local_stopping_mdp_reward_tensor(
        S=simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.S,
        A1=simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.A1,
        A2=simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.A2,
        R=simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.R[0],
        S_D=simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.S_D
    )
    R = reduce_R(R=R, strategy=attacker_strategy)

    experiment_config = ExperimentConfig(
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
    print("T")
    print(list(T.tolist()))

    print("R")
    print(list(R.tolist()))
    agent = VIAgent(simulation_env_config=simulation_env_config,
                    experiment_config=experiment_config, save_to_metastore=True)
    experiment_execution = agent.train()
    print(list(experiment_execution.result.policies.values())[0].lookup_table)
    # MetastoreFacade.save_experiment_execution(experiment_execution)
    # for policy in experiment_execution.result.policies.values():
    #     MetastoreFacade.save_tabular_policy(tabular_policy=policy)
