import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.shapley_iteration.shapley_iteration_agent import ShapleyIterationAgent
import csle_agents.constants.constants as agents_constants

if __name__ == '__main__':
    simulation_name = "csle-stopping-game-002"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    state_space = simulation_env_config.state_space_config.states_ids()
    action_space_player_1 = simulation_env_config.joint_action_space_config.action_spaces[0].actions_ids()
    action_space_player_2 = simulation_env_config.joint_action_space_config.action_spaces[1].actions_ids()
    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}shapley_iteration_test",
        title="Shapley iteration  training attacker and defender through self-play to approximate a Nash equilibrium",
        random_seeds=[399, 98912], agent_type=AgentType.SHAPLEY_ITERATION,
        log_every=1, br_log_every=5000,
        hparams={
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=1,
                                                            name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="number of iterations to evaluate theta"),
            agents_constants.COMMON.SAVE_EVERY: HParam(
                value=10000, name=agents_constants.COMMON.SAVE_EVERY, descr="how frequently to save the model"),
            agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                value=0.95, name=agents_constants.COMMON.CONFIDENCE_INTERVAL,
                descr="confidence interval"),
            agents_constants.COMMON.MAX_ENV_STEPS: HParam(
                value=500, name=agents_constants.COMMON.MAX_ENV_STEPS,
                descr="maximum number of steps in the environment (for envs with infinite horizon generally)"),
            agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                value=40, name=agents_constants.COMMON.RUNNING_AVERAGE,
                descr="the number of samples to include when computing the running avg"),
            agents_constants.COMMON.GAMMA: HParam(
                value=0.99, name=agents_constants.COMMON.GAMMA,
                descr="the discount factor gamma"),
            agents_constants.SHAPLEY_ITERATION.N: HParam(
                value=100, name=agents_constants.SHAPLEY_ITERATION.N,
                descr="the number of iterations of Shapley iteration"),
            agents_constants.SHAPLEY_ITERATION.DELTA: HParam(
                value=0.001, name=agents_constants.SHAPLEY_ITERATION.DELTA,
                descr="the delta threshold parameter for Shapley iteration"),
            agents_constants.SHAPLEY_ITERATION.TRANSITION_TENSOR: HParam(
                value=simulation_env_config.transition_operator_config.transition_tensor[0],
                name=agents_constants.COMMON.GAMMA,
                descr="the transition tensor for Shapley iteration"),
            agents_constants.SHAPLEY_ITERATION.REWARD_TENSOR: HParam(
                value=simulation_env_config.reward_function_config.reward_tensor[0],
                name=agents_constants.SHAPLEY_ITERATION.REWARD_TENSOR,
                descr="the reward tensor for Shapley iteration"),
            agents_constants.SHAPLEY_ITERATION.STATE_SPACE: HParam(
                value=state_space,
                name=agents_constants.SHAPLEY_ITERATION.STATE_SPACE,
                descr="the state space for Shapley iteration"),
            agents_constants.SHAPLEY_ITERATION.ACTION_SPACE_PLAYER_1: HParam(
                value=action_space_player_1,
                name=agents_constants.SHAPLEY_ITERATION.ACTION_SPACE_PLAYER_1,
                descr="the action space for player 1 in Shapley iteration"),
            agents_constants.SHAPLEY_ITERATION.ACTION_SPACE_PLAYER_2: HParam(
                value=action_space_player_2,
                name=agents_constants.SHAPLEY_ITERATION.ACTION_SPACE_PLAYER_2,
                descr="the action space for player 2 in Shapley iteration")
        },
        player_type=PlayerType.SELF_PLAY, player_idx=1
    )
    agent = ShapleyIterationAgent(simulation_env_config=simulation_env_config,
                                  experiment_config=experiment_config, save_to_metastore=True)
    experiment_execution = agent.train()
    MetastoreFacade.save_experiment_execution(experiment_execution)
    for policy in experiment_execution.result.policies.values():
        MetastoreFacade.save_tabular_policy(tabular_policy=policy)
