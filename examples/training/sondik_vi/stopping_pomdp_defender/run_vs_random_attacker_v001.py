import numpy as np
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.sondik_vi.sondik_vi_agent import SondikVIAgent
from csle_common.dao.training.random_policy import RandomPolicy
import csle_agents.constants.constants as agents_constants
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil


def reduce_T(T, strategy, intrusion_start_prob: float = 0.1, intrusion_stop_prob: float = 0.05) -> np.ndarray:
    """
    Reduces the transition tensor based on a given strategy

    :param T: the transition tensor to reduce
    :param strategy: the strategy to use for the reduction
    :param intrusion_start_prob: the intrusion start probability
    :param intrusion_stop_prob: the intrusion stop probability
    :return: the reduced tensor
    """
    reduced_T = np.zeros((T.shape[0], T.shape[2], T.shape[3]))
    for i in range(T.shape[0]):
        for j in range(T.shape[2]):
            for k in range(T.shape[3]):
                if j == 0:
                    reduced_T[i][j][k] = T[i][0][j][k] * (1 - intrusion_start_prob) + T[i][1][j][
                        k] * intrusion_start_prob
                else:
                    reduced_T[i][j][k] = T[i][0][j][k] * (1 - intrusion_stop_prob) + T[i][1][j][k] * intrusion_stop_prob
    return reduced_T


def reduce_R(R, strategy, intrusion_start_prob: float = 0.1, intrusion_stop_prob: float = 0.05):
    """
    Reduces the reward tensor based on a given strategy

    :param R: the reward tensor to reduce
    :param strategy: the strategy to use for the reduction
    :param intrusion_start_prob: the intrusion start probability
    :param intrusion_stop_prob: the intrusion stop probability
    :return: the reduced tensor.
    """
    reduced_R = np.zeros((R.shape[0], R.shape[2]))
    for i in range(R.shape[0]):
        for j in range(R.shape[2]):
            if j == 0:
                reduced_R[i][j] = R[i][0][j] * (1 - intrusion_start_prob) + R[i][1][j] * intrusion_start_prob
            else:
                reduced_R[i][j] = R[i][0][j] * (1 - intrusion_stop_prob) + R[i][1][j] * intrusion_stop_prob
    return reduced_R


def reduce_Z(Z, strategy):
    """
    Reduces the observation tensor based on a given strategy

    :param Z: the tensor to reduce
    :param strategy: the strategy to use for the reduction
    :return: the reduced tensor
    """
    reduced_Z = np.zeros((Z.shape[0], Z.shape[2], Z.shape[3]))
    for i in range(Z.shape[0]):
        for j in range(Z.shape[2]):
            for k in range(Z.shape[3]):
                reduced_Z[i][j][k] = Z[i][0][j][k] * strategy.probability(i, 0) + Z[i][1][j][k] * strategy.probability(
                    i, 1)
    return reduced_Z


if __name__ == '__main__':
    simulation_name = "csle-stopping-pomdp-defender-002"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    simulation_env_config.simulation_env_input_config.attacker_strategy = RandomPolicy(
        actions=simulation_env_config.joint_action_space_config.action_spaces[1].actions,
        player_type=PlayerType.ATTACKER, stage_policy_tensor=[
            [0.5, 0.5],
            [0.5, 0.5],
            [0.5, 0.5]
        ])

    T = np.array(simulation_env_config.transition_operator_config.transition_tensor)
    if len(T.shape) == 5:
        T = T[0]
    num_states = len(simulation_env_config.state_space_config.states)

    simulation_env_config.reward_function_config.reward_tensor = list(StoppingGameUtil.reward_tensor(
        R_INT=-10, R_COST=-10, R_SLA=0, R_ST=100, L=1))

    R = np.array(simulation_env_config.reward_function_config.reward_tensor)
    if len(R.shape) == 4:
        R = R[0]
    # Z = np.array(simulation_env_config.observation_function_config.observation_tensor)
    num_observations = 3
    Z = StoppingGameUtil.observation_tensor(len(range(0, num_observations)))
    if len(R.shape) == 5:
        Z = Z[0]
    num_actions = len(simulation_env_config.joint_action_space_config.action_spaces[0].actions)

    T = reduce_T(T, simulation_env_config.simulation_env_input_config.attacker_strategy)
    R = reduce_R(R, simulation_env_config.simulation_env_input_config.attacker_strategy)
    Z = reduce_Z(Z, simulation_env_config.simulation_env_input_config.attacker_strategy)

    state_space = simulation_env_config.state_space_config.states_ids()
    action_space = simulation_env_config.joint_action_space_config.action_spaces[0].actions_ids()
    # observation_space = simulation_env_config.joint_observation_space_config.observation_spaces[0].observation_ids()
    observation_space = list(range(0, num_observations + 1))

    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}sondik_vi_test",
        title="Sondik-Vi computation",
        random_seeds=[399], agent_type=AgentType.SONDIK_VALUE_ITERATION,
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
                value=0.7, name=agents_constants.COMMON.GAMMA,
                descr="the discount factor"),
            agents_constants.SONDIK_VI.TRANSITION_TENSOR: HParam(
                value=list(T.tolist()), name=agents_constants.VI.TRANSITION_TENSOR,
                descr="the transition tensor"),
            agents_constants.SONDIK_VI.REWARD_TENSOR: HParam(
                value=list(R.tolist()), name=agents_constants.VI.REWARD_TENSOR,
                descr="the reward tensor"),
            agents_constants.SONDIK_VI.INITIAL_BELIEF: HParam(
                value=[1, 0, 0], name=agents_constants.SONDIK_VI.INITIAL_BELIEF,
                descr="the initial belief"),
            agents_constants.SONDIK_VI.ACTION_SPACE: HParam(
                value=action_space, name=agents_constants.SONDIK_VI.ACTION_SPACE,
                descr="action space of the POMDP"),
            agents_constants.SONDIK_VI.STATE_SPACE: HParam(
                value=state_space, name=agents_constants.SONDIK_VI.STATE_SPACE,
                descr="state space of the POMDP"),
            agents_constants.SONDIK_VI.OBSERVATION_SPACE: HParam(
                value=observation_space, name=agents_constants.SONDIK_VI.OBSERVATION_SPACE,
                descr="observation space of the POMDP"),
            agents_constants.SONDIK_VI.OBSERVATION_TENSOR: HParam(
                value=list(Z.tolist()), name=agents_constants.SONDIK_VI.OBSERVATION_TENSOR,
                descr="observation tensor of the POMDP"),
            agents_constants.SONDIK_VI.USE_PRUNING: HParam(
                value=True, name=agents_constants.SONDIK_VI.USE_PRUNING,
                descr="boolean flag whether to use pruning or not"),
            agents_constants.SONDIK_VI.PLANNING_HORIZON: HParam(
                value=10, name=agents_constants.SONDIK_VI.PLANNING_HORIZON,
                descr="the planning horizon for backward induction")
        },
        player_type=PlayerType.DEFENDER, player_idx=0
    )

    agent = SondikVIAgent(simulation_env_config=simulation_env_config,
                          experiment_config=experiment_config, save_to_metastore=True)
    experiment_execution = agent.train()
    MetastoreFacade.save_experiment_execution(experiment_execution)
    for policy in experiment_execution.result.policies.values():
        MetastoreFacade.save_alpha_vec_policy(alpha_vec_policy=policy)
