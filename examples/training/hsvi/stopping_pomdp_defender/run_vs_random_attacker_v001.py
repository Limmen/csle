import numpy as np
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.hsvi.hsvi_agent import HSVIAgent
from csle_common.dao.training.random_policy import RandomPolicy
import csle_agents.constants.constants as agents_constants
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil


if __name__ == '__main__':
    simulation_name = "csle-stopping-pomdp-defender-002"
    simulation_env_config = MetastoreFacade.get_simulation_by_name("csle-stopping-pomdp-defender-002")
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
    num_states = len(simulation_env_config.state_space_config.states)
    simulation_env_config.reward_function_config.reward_tensor = list(StoppingGameUtil.reward_tensor(
        R_INT=-10, R_COST=-10, R_SLA=0, R_ST=100, L=1))
    R = np.array(simulation_env_config.reward_function_config.reward_tensor)
    num_observations = 50
    Z = StoppingGameUtil.observation_tensor(len(range(0, num_observations)))
    num_actions = len(simulation_env_config.joint_action_space_config.action_spaces[0].actions)
    T = StoppingGameUtil.reduce_T_attacker(T, simulation_env_config.simulation_env_input_config.attacker_strategy)
    R = StoppingGameUtil.reduce_R_attacker(R, simulation_env_config.simulation_env_input_config.attacker_strategy)
    Z = StoppingGameUtil.reduce_Z_attacker(Z, simulation_env_config.simulation_env_input_config.attacker_strategy)
    state_space = simulation_env_config.state_space_config.states_ids()
    action_space = simulation_env_config.joint_action_space_config.action_spaces[0].actions_ids()
    observation_space = list(range(0, num_observations + 1))
    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}hsvi_test",
        title="HSVI computation",
        random_seeds=[399], agent_type=AgentType.HSVI,
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
            agents_constants.HSVI.TRANSITION_TENSOR: HParam(
                value=list(T.tolist()), name=agents_constants.VI.TRANSITION_TENSOR,
                descr="the transition tensor"),
            agents_constants.HSVI.REWARD_TENSOR: HParam(
                value=list(R.tolist()), name=agents_constants.VI.REWARD_TENSOR,
                descr="the reward tensor"),
            agents_constants.HSVI.EPSILON: HParam(
                value=0.00001, name=agents_constants.HSVI.EPSILON,
                descr="the epsilon parameter of HSVI"),
            agents_constants.HSVI.INITIAL_BELIEF: HParam(
                value=[1, 0, 0], name=agents_constants.HSVI.INITIAL_BELIEF,
                descr="the initial belief"),
            agents_constants.HSVI.USE_LP: HParam(
                value=False, name=agents_constants.HSVI.USE_LP,
                descr="boolean flag whether to use LP for pruning or not"),
            agents_constants.HSVI.PRUNE_FREQUENCY: HParam(
                value=100, name=agents_constants.HSVI.PRUNE_FREQUENCY,
                descr="how frequently to prune alpha vectors"),
            agents_constants.HSVI.SIMULATION_FREQUENCY: HParam(
                value=1, name=agents_constants.HSVI.SIMULATION_FREQUENCY,
                descr="how frequently to run evaluation simulations"),
            agents_constants.HSVI.SIMULATE_HORIZON: HParam(
                value=100, name=agents_constants.HSVI.SIMULATE_HORIZON,
                descr="maximum time horizon for simulations"),
            agents_constants.HSVI.NUMBER_OF_SIMULATIONS: HParam(
                value=50, name=agents_constants.HSVI.NUMBER_OF_SIMULATIONS,
                descr="batch size for simulations"),
            agents_constants.HSVI.ACTION_SPACE: HParam(
                value=action_space, name=agents_constants.HSVI.ACTION_SPACE,
                descr="action space of the POMDP"),
            agents_constants.HSVI.STATE_SPACE: HParam(
                value=state_space, name=agents_constants.HSVI.STATE_SPACE,
                descr="state space of the POMDP"),
            agents_constants.HSVI.OBSERVATION_SPACE: HParam(
                value=observation_space, name=agents_constants.HSVI.OBSERVATION_SPACE,
                descr="observation space of the POMDP"),
            agents_constants.HSVI.OBSERVATION_TENSOR: HParam(
                value=list(Z.tolist()), name=agents_constants.HSVI.OBSERVATION_TENSOR,
                descr="observation tensor of the POMDP")
        },
        player_type=PlayerType.DEFENDER, player_idx=0
    )

    agent = HSVIAgent(simulation_env_config=simulation_env_config,
                      experiment_config=experiment_config, save_to_metastore=True)
    experiment_execution = agent.train()
    MetastoreFacade.save_experiment_execution(experiment_execution)
    for policy in experiment_execution.result.policies.values():
        MetastoreFacade.save_alpha_vec_policy(alpha_vec_policy=policy)
