import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.pomcp.pomcp_agent import POMCPAgent
from csle_agents.agents.pomcp.pomcp_acquisition_function_type import POMCPAcquisitionFunctionType
import csle_agents.constants.constants as agents_constants
from csle_agents.common.objective_type import ObjectiveType
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from gym_csle_cyborg.dao.csle_cyborg_wrapper_config import CSLECyborgWrapperConfig
from gym_csle_cyborg.envs.cyborg_scenario_two_wrapper import CyborgScenarioTwoWrapper

if __name__ == '__main__':
    emulation_name = "csle-level9-040"
    emulation_env_config = None
    # emulation_env_config = MetastoreFacade.get_emulation_by_name(emulation_name)
    # if emulation_env_config is None:
    #     raise ValueError(f"Could not find an emulation environment with the name: {emulation_name}")
    simulation_name = "csle-cyborg-001"
    # simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    # if simulation_env_config is None:
    #     raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    simulation_env_config = SimulationEnvConfig(name="", version="", gym_env_name="", simulation_env_input_config="",
                                                players_config="", joint_action_space_config="",
                                                joint_observation_space_config="", time_step_type=None,
                                                reward_function_config=None, transition_operator_config=None,
                                                observation_function_config=None,
                                                initial_state_distribution_config=None, env_parameters_config=None,
                                                plot_transition_probabilities=False, plot_observation_function=False,
                                                plot_reward_function=False, descr="", state_space_config=None)
    simulation_env_config.simulation_env_input_config = CSLECyborgWrapperConfig(
        gym_env_name="csle-cyborg-scenario-two-wrapper-v1", maximum_steps=100, save_trace=False)
    simulation_env_config.gym_env_name = "csle-cyborg-scenario-two-wrapper-v1"
    csle_cyborg_env = CyborgScenarioTwoWrapper(config=simulation_env_config.simulation_env_input_config)
    A = csle_cyborg_env.get_action_space()
    initial_particles = csle_cyborg_env.initial_particles
    # rollout_policy = MetastoreFacade.get_ppo_policy(id=58)
    # rollout_policy.save_path = ("/Users/kim/workspace/csle/examples/training/pomcp/cyborg_scenario_two_wrapper/"
    #                             "ppo_test_1706439955.8221297/ppo_model2900_1706522984.6982665.zip")
    # rollout_policy.save_path = ("/Users/kim/workspace/csle/examples/training/pomcp/cyborg_scenario_two_wrapper/"
    #                             "ppo_test_1706439955.8221297/ppo_model50_1706441287.1284034.zip")
    # ppo_model50_1706441287.1284034.zip
    # rollout_policy.load()
    rollout_policy = None
    value_function = lambda x: 0
    # value_function = rollout_policy.value
    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}pomcp_test", title="POMCP test",
        random_seeds=[9981, 98912, 999, 555],
        agent_type=AgentType.POMCP,
        log_every=1,
        hparams={
            agents_constants.POMCP.N: HParam(value=5000, name=agents_constants.POMCP.N,
                                             descr="the number of episodes"),
            agents_constants.POMCP.OBJECTIVE_TYPE: HParam(
                value=ObjectiveType.MAX, name=agents_constants.POMCP.OBJECTIVE_TYPE,
                descr="the type of objective (max or min)"),
            agents_constants.POMCP.ROLLOUT_POLICY: HParam(
                value=rollout_policy, name=agents_constants.POMCP.ROLLOUT_POLICY,
                descr="the policy to use for rollouts"),
            agents_constants.POMCP.VALUE_FUNCTION: HParam(
                value=value_function, name=agents_constants.POMCP.VALUE_FUNCTION,
                descr="the value function to use for truncated rollouts"),
            agents_constants.POMCP.A: HParam(value=A, name=agents_constants.POMCP.A, descr="the action space"),
            agents_constants.POMCP.GAMMA: HParam(value=1, name=agents_constants.POMCP.GAMMA,
                                                 descr="the discount factor"),
            agents_constants.POMCP.REINVIGORATION: HParam(value=False, name=agents_constants.POMCP.REINVIGORATION,
                                                          descr="whether reinvigoration should be used"),
            agents_constants.POMCP.REINVIGORATED_PARTICLES_RATIO: HParam(
                value=0.01, name=agents_constants.POMCP.REINVIGORATED_PARTICLES_RATIO,
                descr="the ratio of reinvigorated particles in the particle filter"),
            agents_constants.POMCP.INITIAL_PARTICLES: HParam(value=initial_particles,
                                                             name=agents_constants.POMCP.INITIAL_PARTICLES,
                                                             descr="the initial belief"),
            agents_constants.POMCP.PLANNING_TIME: HParam(value=10, name=agents_constants.POMCP.PLANNING_TIME,
                                                         descr="the planning time"),
            agents_constants.POMCP.MAX_PARTICLES: HParam(value=5000, name=agents_constants.POMCP.MAX_PARTICLES,
                                                         descr="the maximum number of belief particles"),
            agents_constants.POMCP.MAX_PLANNING_DEPTH: HParam(
                value=4, name=agents_constants.POMCP.MAX_PLANNING_DEPTH, descr="the maximum depth for planning"),
            agents_constants.POMCP.MAX_ROLLOUT_DEPTH: HParam(value=5, name=agents_constants.POMCP.MAX_ROLLOUT_DEPTH,
                                                             descr="the maximum depth for rollout"),
            agents_constants.POMCP.C: HParam(value=1, name=agents_constants.POMCP.C,
                                             descr="the weighting factor for UCB exploration"),
            agents_constants.POMCP.C2: HParam(value=15000, name=agents_constants.POMCP.C2,
                                              descr="the weighting factor for AlphaGo exploration"),
            agents_constants.POMCP.USE_ROLLOUT_POLICY: HParam(
                value=False, name=agents_constants.POMCP.USE_ROLLOUT_POLICY,
                descr="boolean flag indicating whether rollout policy should be used"),
            agents_constants.POMCP.PRIOR_WEIGHT: HParam(value=5, name=agents_constants.POMCP.PRIOR_WEIGHT,
                                                        descr="the weight on the prior"),
            agents_constants.POMCP.PRIOR_CONFIDENCE: HParam(value=0, name=agents_constants.POMCP.PRIOR_CONFIDENCE,
                                                            descr="the prior confidence"),
            agents_constants.POMCP.ACQUISITION_FUNCTION_TYPE: HParam(
                value=POMCPAcquisitionFunctionType.UCB, name=agents_constants.POMCP.ACQUISITION_FUNCTION_TYPE,
                descr="the type of acquisition function"),
            agents_constants.POMCP.LOG_STEP_FREQUENCY: HParam(
                value=1, name=agents_constants.POMCP.LOG_STEP_FREQUENCY, descr="frequency of logging time-steps"),
            agents_constants.POMCP.MAX_NEGATIVE_SAMPLES: HParam(
                value=20, name=agents_constants.POMCP.MAX_NEGATIVE_SAMPLES,
                descr="maximum number of negative samples when filling belief particles"),
            agents_constants.POMCP.DEFAULT_NODE_VALUE: HParam(
                value=0, name=agents_constants.POMCP.DEFAULT_NODE_VALUE, descr="the default node value in "
                                                                               "the search tree"),
            agents_constants.POMCP.VERBOSE: HParam(value=False, name=agents_constants.POMCP.VERBOSE,
                                                   descr="verbose logging flag"),
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=100, name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="number of evaluation episodes"),
            agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                value=0.95, name=agents_constants.COMMON.CONFIDENCE_INTERVAL,
                descr="confidence interval"),
            agents_constants.COMMON.MAX_ENV_STEPS: HParam(
                value=100, name=agents_constants.COMMON.MAX_ENV_STEPS,
                descr="maximum number of steps in the environment (for envs with infinite horizon generally)"),
            agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                value=100, name=agents_constants.COMMON.RUNNING_AVERAGE,
                descr="the number of samples to include when computing the running avg")
        },
        player_type=PlayerType.DEFENDER, player_idx=0
    )
    agent = POMCPAgent(emulation_env_config=emulation_env_config, simulation_env_config=simulation_env_config,
                       experiment_config=experiment_config, save_to_metastore=False)
    experiment_execution = agent.train()
    MetastoreFacade.save_experiment_execution(experiment_execution)
