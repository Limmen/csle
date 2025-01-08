import random
import numpy as np
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.pi.pi_agent import PIAgent
from csle_common.dao.training.random_policy import RandomPolicy
import csle_agents.constants.constants as agents_constants
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil


if __name__ == '__main__':
    simulation_name = "csle-stopping-mdp-attacker-002"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    simulation_env_config.simulation_env_input_config.defender_strategy = RandomPolicy(
        actions=simulation_env_config.joint_action_space_config.action_spaces[0].actions,
        player_type=PlayerType.DEFENDER, stage_policy_tensor=None)
    T = np.array(simulation_env_config.transition_operator_config.transition_tensor)
    num_states = len(simulation_env_config.state_space_config.states)
    R = np.array(simulation_env_config.reward_function_config.reward_tensor)
    num_actions = len(simulation_env_config.joint_action_space_config.action_spaces[1].actions)
    T = StoppingGameUtil.reduce_T_defender(T, simulation_env_config.simulation_env_input_config.defender_strategy)
    R = -StoppingGameUtil.reduce_R_defender(R, simulation_env_config.simulation_env_input_config.defender_strategy)
    initial_pi = np.zeros((num_states, num_actions))
    for s in range(num_states):
        a = random.choice(list(range(num_actions)))
        initial_pi[s][a] = 1

    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}pi_test",
        title="Policy iteration computation",
        random_seeds=[399], agent_type=AgentType.POLICY_ITERATION,
        log_every=1,
        hparams={
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=100,
                                                            name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="number of iterations to evaluate"),
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
            agents_constants.PI.TRANSITION_TENSOR: HParam(
                value=list(T.tolist()), name=agents_constants.PI.TRANSITION_TENSOR,
                descr="the transition tensor"),
            agents_constants.PI.REWARD_TENSOR: HParam(
                value=list(R.tolist()), name=agents_constants.PI.REWARD_TENSOR,
                descr="the reward tensor"),
            agents_constants.PI.NUM_STATES: HParam(
                value=num_states, name=agents_constants.PI.NUM_STATES,
                descr="the number of states"),
            agents_constants.PI.NUM_ACTIONS: HParam(
                value=num_actions, name=agents_constants.PI.NUM_ACTIONS,
                descr="the number of actions"),
            agents_constants.PI.N: HParam(
                value=100, name=agents_constants.PI.N,
                descr="the number of iterations"),
            agents_constants.PI.INITIAL_POLICY: HParam(
                value=list(initial_pi.tolist()), name=agents_constants.PI.INITIAL_POLICY,
                descr="the initial policy")
        },
        player_type=PlayerType.ATTACKER, player_idx=1
    )

    agent = PIAgent(simulation_env_config=simulation_env_config,
                    experiment_config=experiment_config, save_to_metastore=True)
    experiment_execution = agent.train()
    MetastoreFacade.save_experiment_execution(experiment_execution)
    for policy in experiment_execution.result.policies.values():
        MetastoreFacade.save_tabular_policy(tabular_policy=policy)
