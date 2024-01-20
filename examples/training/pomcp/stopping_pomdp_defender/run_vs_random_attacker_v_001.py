import numpy as np
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.pomcp.pomcp_agent import POMCPAgent
import csle_agents.constants.constants as agents_constants
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from csle_agents.common.objective_type import ObjectiveType
from csle_common.dao.training.random_policy import RandomPolicy
from csle_common.dao.training.multi_threshold_stopping_policy import MultiThresholdStoppingPolicy
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from gym_csle_stopping_game.dao.stopping_game_defender_pomdp_config import StoppingGameDefenderPomdpConfig

if __name__ == '__main__':
    emulation_name = "csle-level9-040"
    emulation_env_config = MetastoreFacade.get_emulation_by_name(emulation_name)
    if emulation_env_config is None:
        raise ValueError(f"Could not find an emulation environment with the name: {emulation_name}")
    simulation_name = "csle-stopping-pomdp-defender-002"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")

    stopping_game_config = StoppingGameConfig(
        T=StoppingGameUtil.transition_tensor(L=1, p=0),
        O=StoppingGameUtil.observation_space(n=10),
        Z=StoppingGameUtil.observation_tensor(n=10),
        R=StoppingGameUtil.reward_tensor(R_INT=-5, R_COST=-10, R_SLA=0, R_ST=20, L=1),
        A1=StoppingGameUtil.defender_actions(),
        A2=StoppingGameUtil.attacker_actions(),
        L=1, R_INT=-10, R_COST=-10, R_SLA=0, R_ST=20, b1=StoppingGameUtil.b1(),
        S=StoppingGameUtil.state_space(), env_name="csle-stopping-game-v1",
        save_dir="/home/kim/stopping_game_1", checkpoint_traces_freq=1000, gamma=1
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
    initial_belief = {}
    for i in range(len(b1)):
        initial_belief[i] = b1[i]
    rollout_policy = MultiThresholdStoppingPolicy(
        theta=[0.75], simulation_name=simulation_name, L=stopping_game_config.L,
        states=simulation_env_config.state_space_config.states, player_type=PlayerType.DEFENDER,
        actions=simulation_env_config.joint_action_space_config.action_spaces[0].actions, experiment_config=None,
        avg_R=-1, agent_type=AgentType.POMCP, opponent_strategy=None)
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
                value=lambda x: 0, name=agents_constants.POMCP.VALUE_FUNCTION,
                descr="the value function to use for truncated rollouts"),
            agents_constants.POMCP.A: HParam(value=A, name=agents_constants.POMCP.A, descr="the action space"),
            agents_constants.POMCP.GAMMA: HParam(value=0.99, name=agents_constants.POMCP.GAMMA,
                                                 descr="the discount factor"),
            agents_constants.POMCP.INITIAL_BELIEF: HParam(value=initial_belief,
                                                          name=agents_constants.POMCP.INITIAL_BELIEF,
                                                          descr="the initial belief"),
            agents_constants.POMCP.REINVIGORATION: HParam(value=True, name=agents_constants.POMCP.REINVIGORATION,
                                                          descr="whether reinvigoration should be used"),
            agents_constants.POMCP.PLANNING_TIME: HParam(value=120, name=agents_constants.POMCP.PLANNING_TIME,
                                                         descr="the planning time"),
            agents_constants.POMCP.MAX_PARTICLES: HParam(value=100, name=agents_constants.POMCP.MAX_PARTICLES,
                                                         descr="the maximum number of belief particles"),
            agents_constants.POMCP.MAX_DEPTH: HParam(value=500, name=agents_constants.POMCP.MAX_DEPTH,
                                                     descr="the maximum depth for planning"),
            agents_constants.POMCP.C: HParam(value=0.35, name=agents_constants.POMCP.C,
                                             descr="the weighting factor for UCB exploration"),
            agents_constants.POMCP.MAX_NEGATIVE_SAMPLES: HParam(
                value=200, name=agents_constants.POMCP.MAX_NEGATIVE_SAMPLES,
                descr="maximum number of negative samples when filling belief particles"),
            agents_constants.POMCP.DEFAULT_NODE_VALUE: HParam(
                value=-2000, name=agents_constants.POMCP.DEFAULT_NODE_VALUE, descr="the default node value in "
                                                                                   "the search tree"),
            agents_constants.POMCP.LOG_STEP_FREQUENCY: HParam(
                value=1, name=agents_constants.POMCP.LOG_STEP_FREQUENCY, descr="frequency of logging time-steps"),
            agents_constants.POMCP.VERBOSE: HParam(value=False, name=agents_constants.POMCP.VERBOSE,
                                                   descr="verbose logging flag"),
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=100, name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="number of evaluation episodes"),
            agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                value=0.95, name=agents_constants.COMMON.CONFIDENCE_INTERVAL,
                descr="confidence interval"),
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
