import numpy as np
import copy
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.pomcp.pomcp_agent import POMCPAgent
from csle_agents.agents.pomcp.pomcp_acquisition_function_type import POMCPAcquisitionFunctionType
import csle_agents.constants.constants as agents_constants
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from csle_agents.common.objective_type import ObjectiveType
from csle_common.dao.training.random_policy import RandomPolicy
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from gym_csle_stopping_game.dao.stopping_game_defender_pomdp_config import StoppingGameDefenderPomdpConfig

if __name__ == '__main__':
    emulation_name = "csle-level9-070"
    emulation_env_config = MetastoreFacade.get_emulation_by_name(emulation_name)
    if emulation_env_config is None:
        raise ValueError(f"Could not find an emulation environment with the name: {emulation_name}")
    simulation_name = "csle-stopping-pomdp-defender-002"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")

    stopping_game_config = StoppingGameConfig(
        T=StoppingGameUtil.transition_tensor(L=1),
        O=StoppingGameUtil.observation_space(n=10),
        Z=StoppingGameUtil.observation_tensor(n=10),
        R=StoppingGameUtil.reward_tensor(R_INT=-5, R_COST=-10, R_SLA=0, R_ST=20, L=1),
        A1=StoppingGameUtil.defender_actions(),
        A2=StoppingGameUtil.attacker_actions(),
        L=1, R_INT=-10, R_COST=-10, R_SLA=0, R_ST=20, b1=StoppingGameUtil.b1(),
        S=StoppingGameUtil.state_space(), env_name="csle-stopping-game-v1",
        save_dir="/home/kim/stopping_game_1", checkpoint_traces_freq=1000, gamma=1,
        compute_beliefs=False, save_trace=False
    )
    attacker_stage_strategy = np.zeros((3, 2))
    attacker_stage_strategy[0][0] = 0.9
    attacker_stage_strategy[0][1] = 0.1
    attacker_stage_strategy[1][0] = 1
    attacker_stage_strategy[1][1] = 0
    attacker_stage_strategy[2] = attacker_stage_strategy[1]
    attacker_strategy = RandomPolicy(actions=StoppingGameUtil.attacker_actions(),
                                     player_type=PlayerType.ATTACKER,
                                     stage_policy_tensor=list(attacker_stage_strategy))
    defender_pomdp_config = StoppingGameDefenderPomdpConfig(
        env_name="csle-stopping-game-pomdp-defender-v1", stopping_game_name="csle-stopping-game-v1",
        stopping_game_config=stopping_game_config, attacker_strategy=attacker_strategy
    )
    simulation_env_config.simulation_env_input_config = defender_pomdp_config
    S = simulation_env_config.simulation_env_input_config.stopping_game_config.S
    A = simulation_env_config.simulation_env_input_config.stopping_game_config.A1
    O = simulation_env_config.simulation_env_input_config.stopping_game_config.O
    b1 = simulation_env_config.simulation_env_input_config.stopping_game_config.b1
    initial_particles = [np.argmax(b1)]
    rollout_policy = None
    value_function = None
    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}pomcp_test", title="POMCP test",
        random_seeds=[399, 98912, 999, 555],
        agent_type=AgentType.POMCP,
        log_every=1,
        hparams={
            agents_constants.POMCP.N: HParam(value=50, name=agents_constants.POMCP.N,
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
            agents_constants.POMCP.GAMMA: HParam(value=0.99, name=agents_constants.POMCP.GAMMA,
                                                 descr="the discount factor"),
            agents_constants.POMCP.INITIAL_PARTICLES: HParam(value=initial_particles,
                                                             name=agents_constants.POMCP.INITIAL_PARTICLES,
                                                             descr="the initial belief"),
            agents_constants.POMCP.REINVIGORATION: HParam(value=True, name=agents_constants.POMCP.REINVIGORATION,
                                                          descr="whether reinvigoration should be used"),
            agents_constants.POMCP.REINVIGORATED_PARTICLES_RATIO: HParam(
                value=0.1, name=agents_constants.POMCP.REINVIGORATED_PARTICLES_RATIO,
                descr="the ratio of reinvigorated particles in the particle filter"),
            agents_constants.POMCP.PLANNING_TIME: HParam(value=30, name=agents_constants.POMCP.PLANNING_TIME,
                                                         descr="the planning time"),
            agents_constants.POMCP.MAX_PARTICLES: HParam(value=100, name=agents_constants.POMCP.MAX_PARTICLES,
                                                         descr="the maximum number of belief particles"),
            agents_constants.POMCP.MAX_PLANNING_DEPTH: HParam(value=100, name=agents_constants.POMCP.MAX_PLANNING_DEPTH,
                                                              descr="the maximum depth for planning"),
            agents_constants.POMCP.MAX_ROLLOUT_DEPTH: HParam(value=100, name=agents_constants.POMCP.MAX_ROLLOUT_DEPTH,
                                                             descr="the maximum depth for rollout"),
            agents_constants.POMCP.C: HParam(value=15, name=agents_constants.POMCP.C,
                                             descr="the weighting factor for UCB exploration"),
            agents_constants.POMCP.PARALLEL_ROLLOUT: HParam(
                value=False, name=agents_constants.POMCP.PARALLEL_ROLLOUT, descr="boolean flag indicating whether "
                                                                                 "parallel rollout should be used"),
            agents_constants.POMCP.PRUNE_ACTION_SPACE: HParam(
                value=False, name=agents_constants.POMCP.PRUNE_ACTION_SPACE,
                descr="boolean flag indicating whether the action space should be pruned or not"),
            agents_constants.POMCP.PRUNE_SIZE: HParam(
                value=3, name=agents_constants.POMCP.PRUNE_ACTION_SPACE, descr="size of the pruned action space"),
            agents_constants.POMCP.NUM_PARALLEL_PROCESSES: HParam(
                value=50, name=agents_constants.POMCP.NUM_PARALLEL_PROCESSES, descr="number of parallel processes"),
            agents_constants.POMCP.NUM_EVALS_PER_PROCESS: HParam(
                value=10, name=agents_constants.POMCP.NUM_EVALS_PER_PROCESS,
                descr="number of evaluations per process"),
            agents_constants.POMCP.MAX_NEGATIVE_SAMPLES: HParam(
                value=200, name=agents_constants.POMCP.MAX_NEGATIVE_SAMPLES,
                descr="maximum number of negative samples when filling belief particles"),
            agents_constants.POMCP.DEFAULT_NODE_VALUE: HParam(
                value=-2000, name=agents_constants.POMCP.DEFAULT_NODE_VALUE, descr="the default node value in "
                                                                                   "the search tree"),
            agents_constants.POMCP.ACQUISITION_FUNCTION_TYPE: HParam(
                value=POMCPAcquisitionFunctionType.UCB, name=agents_constants.POMCP.ACQUISITION_FUNCTION_TYPE,
                descr="the type of acquisition function"),
            agents_constants.POMCP.C2: HParam(value=15000, name=agents_constants.POMCP.C2,
                                              descr="the weighting factor for AlphaGo exploration"),
            agents_constants.POMCP.LOG_STEP_FREQUENCY: HParam(
                value=1, name=agents_constants.POMCP.LOG_STEP_FREQUENCY, descr="frequency of logging time-steps"),
            agents_constants.POMCP.VERBOSE: HParam(value=False, name=agents_constants.POMCP.VERBOSE,
                                                   descr="verbose logging flag"),
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=100, name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="number of evaluation episodes"),
            agents_constants.POMCP.PRIOR_WEIGHT: HParam(value=5, name=agents_constants.POMCP.PRIOR_WEIGHT,
                                                        descr="the weight on the prior"),
            agents_constants.POMCP.PRIOR_CONFIDENCE: HParam(value=1, name=agents_constants.POMCP.PRIOR_CONFIDENCE,
                                                            descr="the prior confidence"),
            agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                value=0.95, name=agents_constants.COMMON.CONFIDENCE_INTERVAL,
                descr="confidence interval"),
            agents_constants.POMCP.USE_ROLLOUT_POLICY: HParam(
                value=False, name=agents_constants.POMCP.USE_ROLLOUT_POLICY,
                descr="boolean flag indicating whether rollout policy should be used"),
            agents_constants.POMCP.EVAL_ENV_NAME: HParam(
                value=simulation_env_config.gym_env_name,
                name=agents_constants.POMCP.EVAL_ENV_NAME,
                descr="the name of the evaluation environment"),
            agents_constants.POMCP.EVAL_ENV_CONFIG: HParam(
                value=copy.deepcopy(simulation_env_config.simulation_env_input_config),
                name=agents_constants.POMCP.EVAL_ENV_CONFIG, descr="the configuration of the evaluation environment"),
            agents_constants.COMMON.MAX_ENV_STEPS: HParam(
                value=500, name=agents_constants.COMMON.MAX_ENV_STEPS,
                descr="maximum number of steps in the environment (for envs with infinite horizon generally)"),
            agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                value=100, name=agents_constants.COMMON.RUNNING_AVERAGE,
                descr="the number of samples to include when computing the running avg"),
            agents_constants.COMMON.GAMMA: HParam(
                value=0.99, name=agents_constants.COMMON.GAMMA,
                descr="the discount factor")
        },
        player_type=PlayerType.DEFENDER, player_idx=0
    )
    agent = POMCPAgent(emulation_env_config=emulation_env_config, simulation_env_config=simulation_env_config,
                       experiment_config=experiment_config, save_to_metastore=False)
    experiment_execution = agent.train()
    MetastoreFacade.save_experiment_execution(experiment_execution)
