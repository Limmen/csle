import numpy as np
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.vi.vi_agent import VIAgent
from csle_common.dao.training.random_policy import RandomPolicy
import csle_agents.constants.constants as agents_constants


def reduce_T(T, strategy):
    """
    Reduces the transition tensor based on a given strategy

    :param T: the tensor to reduce
    :param strategy: the strategy to use for the reduction
    :return: the reduced tensor
    """
    reduced_T = np.zeros((T.shape[1], T.shape[2], T.shape[3]))
    for i in range(T.shape[1]):
        for j in range(T.shape[2]):
            for k in range(T.shape[3]):
                reduced_T[i][j][k] = T[0][i][j][k] * strategy.probability(j, 0) + T[1][i][j][k] * strategy.probability(
                    j, 1)
    return reduced_T


def reduce_R(R, strategy):
    """
    Reduces the reward tensor based on a given strategy

    :param R: the reward tensor to reduce
    :param strategy: the strategy to use for the reduction
    :return: the reduced reward tensor
    """
    reduced_R = np.zeros((R.shape[1], R.shape[2]))
    for i in range(R.shape[1]):
        for j in range(R.shape[2]):
            reduced_R[i][j] = R[0][i][j] * strategy.probability(i, 0) + R[1][i][j] * strategy.probability(i, 1)
    return reduced_R


if __name__ == '__main__':
    simulation_name = "csle-stopping-mdp-attacker-002"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    simulation_env_config.simulation_env_input_config.defender_strategy = RandomPolicy(
        actions=simulation_env_config.joint_action_space_config.action_spaces[0].actions,
        player_type=PlayerType.DEFENDER, stage_policy_tensor=None)

    T = np.array(simulation_env_config.transition_operator_config.transition_tensor)
    if len(T.shape) == 5:
        T = T[0]
    num_states = len(simulation_env_config.state_space_config.states)
    R = np.array(simulation_env_config.reward_function_config.reward_tensor)
    if len(R.shape) == 4:
        R = R[0]
    num_actions = len(simulation_env_config.joint_action_space_config.action_spaces[1].actions)

    T = reduce_T(T, simulation_env_config.simulation_env_input_config.defender_strategy)
    R = -reduce_R(R, simulation_env_config.simulation_env_input_config.defender_strategy)

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
                value=0.99, name=agents_constants.COMMON.GAMMA,
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
                value=num_states, name=agents_constants.VI.NUM_STATES,
                descr="the number of states"),
            agents_constants.VI.NUM_ACTIONS: HParam(
                value=num_actions, name=agents_constants.VI.NUM_ACTIONS,
                descr="the number of actions")
        },
        player_type=PlayerType.ATTACKER, player_idx=1
    )

    agent = VIAgent(simulation_env_config=simulation_env_config,
                    experiment_config=experiment_config, save_to_metastore=True)
    experiment_execution = agent.train()
    MetastoreFacade.save_experiment_execution(experiment_execution)
    for policy in experiment_execution.result.policies.values():
        MetastoreFacade.save_tabular_policy(tabular_policy=policy)
