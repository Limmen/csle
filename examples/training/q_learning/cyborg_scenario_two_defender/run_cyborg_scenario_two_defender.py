import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.q_learning.q_learning_agent import QLearningAgent
import csle_agents.constants.constants as agents_constants
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender

if __name__ == '__main__':
    emulation_name = "csle-level9-070"
    emulation_env_config = MetastoreFacade.get_emulation_by_name(emulation_name)
    if emulation_env_config is None:
        raise ValueError(f"Could not find an emulation environment with the name: {emulation_name}")
    simulation_name = "csle-cyborg-001"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")

    simulation_env_config.simulation_env_input_config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=False, scanned_state=False,
        decoy_state=False, decoy_optimization=True, cache_visited_states=False)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=simulation_env_config.simulation_env_input_config)
    A = list(range(len(csle_cyborg_env.decoy_hosts)))
    S = csle_cyborg_env.decoy_state_space
    initial_state_dist = []
    initial_state = csle_cyborg_env.decoy_state_space_lookup[(0, 0, 0, 0, 0, 0, 0, 0)]
    for s in S:
        if s == initial_state:
            initial_state_dist.append(1)
        else:
            initial_state_dist.append(0)
    simulation_env_config.initial_state_distribution_config.initial_state_distribution = initial_state_dist

    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}q_learning_test",
        title="Q-learning",
        random_seeds=[399], agent_type=AgentType.Q_LEARNING,
        log_every=5000,
        hparams={
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=100,
                                                            name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="number of iterations to evaluate theta"),
            agents_constants.COMMON.EVAL_EVERY: HParam(value=1000,
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
            agents_constants.Q_LEARNING.S: HParam(
                value=S, name=agents_constants.Q_LEARNING.S,
                descr="the state space"),
            agents_constants.Q_LEARNING.A: HParam(
                value=A, name=agents_constants.Q_LEARNING.A,
                descr="the action space"),
            agents_constants.Q_LEARNING.EPSILON: HParam(
                value=0.5, name=agents_constants.Q_LEARNING.EPSILON,
                descr="the exploration parameter"),
            agents_constants.Q_LEARNING.N: HParam(
                value=180000, name=agents_constants.Q_LEARNING.N,
                descr="the number of iterations"),
            agents_constants.Q_LEARNING.EPSILON_DECAY_RATE: HParam(
                value=0.99999, name=agents_constants.Q_LEARNING.EPSILON_DECAY_RATE,
                descr="epsilon decay rate")
        },
        player_type=PlayerType.DEFENDER, player_idx=1
    )

    agent = QLearningAgent(simulation_env_config=simulation_env_config,
                           experiment_config=experiment_config, save_to_metastore=False)
    experiment_execution = agent.train()
    MetastoreFacade.save_experiment_execution(experiment_execution)
    for policy in experiment_execution.result.policies.values():
        MetastoreFacade.save_tabular_policy(tabular_policy=policy)
