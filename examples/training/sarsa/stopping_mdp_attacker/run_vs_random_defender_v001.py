import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.sarsa.sarsa_agent import SARSAAgent
from csle_common.dao.training.random_policy import RandomPolicy
import csle_agents.constants.constants as agents_constants

if __name__ == '__main__':
    simulation_name = "csle-stopping-mdp-attacker-002"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    simulation_env_config.simulation_env_input_config.defender_strategy = RandomPolicy(
        actions=simulation_env_config.joint_action_space_config.action_spaces[0].actions,
        player_type=PlayerType.DEFENDER, stage_policy_tensor=None)
    A = simulation_env_config.joint_action_space_config.action_spaces[1].actions_ids()
    S = simulation_env_config.state_space_config.states_ids()

    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}sarsa_test",
        title="SARSA",
        random_seeds=[399], agent_type=AgentType.SARSA,
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
            agents_constants.SARSA.S: HParam(
                value=S, name=agents_constants.SARSA.S,
                descr="the state spaec"),
            agents_constants.SARSA.A: HParam(
                value=A, name=agents_constants.SARSA.A,
                descr="the action space"),
            agents_constants.SARSA.EPSILON: HParam(
                value=0.05, name=agents_constants.SARSA.EPSILON,
                descr="the exploration parameter"),
            agents_constants.SARSA.N: HParam(
                value=200, name=agents_constants.SARSA.N,
                descr="the number of iterations")
        },
        player_type=PlayerType.ATTACKER, player_idx=1
    )

    agent = SARSAAgent(simulation_env_config=simulation_env_config,
                       experiment_config=experiment_config, save_to_metastore=True)
    experiment_execution = agent.train()
    MetastoreFacade.save_experiment_execution(experiment_execution)
    for policy in experiment_execution.result.policies.values():
        MetastoreFacade.save_tabular_policy(tabular_policy=policy)
