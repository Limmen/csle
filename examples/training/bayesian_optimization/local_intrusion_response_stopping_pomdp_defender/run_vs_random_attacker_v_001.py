import numpy as np
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.bayesian_optimization.bayes_opt_agent import BayesOptAgent
import csle_agents.constants.constants as agents_constants
from gym_csle_intrusion_response_game.dao.local_intrusion_response_game_config import LocalIntrusionResponseGameConfig
from gym_csle_intrusion_response_game.util.intrusion_response_game_util import IntrusionResponseGameUtil
import gym_csle_intrusion_response_game.constants.constants as env_constants
from csle_common.dao.training.tabular_policy import TabularPolicy
from csle_common.dao.training.policy_type import PolicyType
from gym_csle_intrusion_response_game.envs.intrusion_response_game_local_stopping_pomdp_defender import \
    IntrusionResponseGameLocalStoppingPOMDPDefenderEnv

if __name__ == '__main__':
    emulation_name = "csle-level9-090"
    emulation_env_config = MetastoreFacade.get_emulation_by_name(emulation_name)
    if emulation_env_config is None:
        raise ValueError(f"Could not find an emulation environment with the name: {emulation_name}")
    simulation_name = "csle-intrusion-response-game-local-pomdp-defender-001"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    number_of_zones = 6
    X_max = 100
    eta = 0.5
    reachable = True
    beta = 3
    gamma = 0.99
    initial_zone = 3
    initial_state = [initial_zone, 0]
    zones = IntrusionResponseGameUtil.zones(num_zones=number_of_zones)
    Z_D_P = np.array([0, 0.8, 0.5, 0.1, 0.05, 0.025])
    S = IntrusionResponseGameUtil.local_state_space(number_of_zones=number_of_zones)
    states_to_idx = {}
    for i, s in enumerate(S):
        states_to_idx[(s[env_constants.STATES.D_STATE_INDEX], s[env_constants.STATES.A_STATE_INDEX])] = i
    S_A = IntrusionResponseGameUtil.local_attacker_state_space()
    S_D = IntrusionResponseGameUtil.local_defender_state_space(number_of_zones=number_of_zones)
    A1 = IntrusionResponseGameUtil.local_defender_actions(number_of_zones=number_of_zones)
    C_D = np.array([0, 35, 30, 25, 20, 20, 20, 15])
    A2 = IntrusionResponseGameUtil.local_attacker_actions()
    A_P = np.array([1, 1, 0.75, 0.85])
    O = IntrusionResponseGameUtil.local_observation_space(X_max=X_max)
    T = np.array([IntrusionResponseGameUtil.local_transition_tensor(S=S, A1=A1, A2=A2, Z_D=Z_D_P, A_P=A_P)])
    Z = IntrusionResponseGameUtil.local_observation_tensor_betabinom(S=S, A1=A1, A2=A2, O=O)
    Z_U = np.array([0, 0, 2.5, 5, 10, 15])
    R = np.array(
        [IntrusionResponseGameUtil.local_reward_tensor(eta=eta, C_D=C_D, A1=A1, A2=A2, reachable=reachable, beta=beta,
                                                       S=S, Z_U=Z_U, initial_zone=initial_zone)])
    d_b1 = IntrusionResponseGameUtil.local_initial_defender_belief(S_A=S_A)
    a_b1 = IntrusionResponseGameUtil.local_initial_attacker_belief(S_D=S_D, initial_zone=initial_zone)
    initial_state_idx = states_to_idx[(initial_state[env_constants.STATES.D_STATE_INDEX],
                                       initial_state[env_constants.STATES.A_STATE_INDEX])]
    env_name = "csle-intrusion-response-game-pomdp-defender-v1"
    attacker_stage_strategy = np.zeros((len(IntrusionResponseGameUtil.local_attacker_state_space()), len(A2)))
    for i, s_a in enumerate(IntrusionResponseGameUtil.local_attacker_state_space()):
        if s_a == env_constants.ATTACK_STATES.HEALTHY:
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.WAIT] = 0.9
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.RECON] = 0.1
        elif s_a == env_constants.ATTACK_STATES.RECON:
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.WAIT] = 0
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.BRUTE_FORCE] = 0.5
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.EXPLOIT] = 0.5
        else:
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.WAIT] = 1
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.BRUTE_FORCE] = 0.
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.EXPLOIT] = 0
    attacker_strategy = TabularPolicy(
        player_type=PlayerType.ATTACKER, actions=A2,
        simulation_name="csle-intrusion-response-game-pomdp-defender-001",
        value_function=None, q_table=None,
        lookup_table=list(attacker_stage_strategy.tolist()),
        agent_type=AgentType.RANDOM, avg_R=-1)
    simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config = \
        LocalIntrusionResponseGameConfig(
            env_name=env_name, T=T, O=O, Z=Z, R=R, S=S, S_A=S_A, S_D=S_D, s_1_idx=initial_state_idx, zones=zones,
            A1=A1, A2=A2, d_b1=d_b1, a_b1=a_b1, gamma=gamma, beta=beta, C_D=C_D, A_P=A_P, Z_D_P=Z_D_P, Z_U=Z_U,
            eta=eta
        )
    simulation_env_config.gym_env_name = "csle-intrusion-response-game-local-stopping-pomdp-defender-v1"
    simulation_env_config.simulation_env_input_config.attacker_strategy = attacker_strategy
    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}bayes_opt_ir_game", title="Bayesian Optimization IR game",
        random_seeds=[399, 98912, 999, 555],
        agent_type=AgentType.BAYESIAN_OPTIMIZATION,
        log_every=1,
        hparams={
            agents_constants.BAYESIAN_OPTIMIZATION.N: HParam(value=500, name=constants.T_SPSA.N,
                                                             descr="the number of training iterations"),
            agents_constants.BAYESIAN_OPTIMIZATION.L: HParam(value=1, name="L", descr="the number of stop actions"),
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=100, name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="number of iterations to evaluate theta"),
            agents_constants.BAYESIAN_OPTIMIZATION.THETA1: HParam(
                value=[0, 0], name=agents_constants.BAYESIAN_OPTIMIZATION.THETA1,
                descr="initial coefficients"),
            agents_constants.COMMON.SAVE_EVERY: HParam(value=1000, name=agents_constants.COMMON.SAVE_EVERY,
                                                       descr="how frequently to save the model"),
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
                value=1, name=agents_constants.COMMON.GAMMA,
                descr="the discount factor"),
            agents_constants.BAYESIAN_OPTIMIZATION.UTILITY_FUNCTION: HParam(
                value=agents_constants.BAYESIAN_OPTIMIZATION.UCB,
                name=agents_constants.BAYESIAN_OPTIMIZATION.UTILITY_FUNCTION,
                descr="utility/acquisition function"),
            agents_constants.BAYESIAN_OPTIMIZATION.UCB_KAPPA: HParam(
                value=2.5,
                name=agents_constants.BAYESIAN_OPTIMIZATION.UCB_KAPPA,
                descr="kappa parameter for the ucb utility function"),
            agents_constants.BAYESIAN_OPTIMIZATION.UCB_XI: HParam(
                value=0,
                name=agents_constants.BAYESIAN_OPTIMIZATION.UCB_XI,
                descr="kappa parameter for the xi utility function"),
            agents_constants.BAYESIAN_OPTIMIZATION.PARAMETER_BOUNDS: HParam(
                value=[(-5, 5), (-5, 5)],
                name=agents_constants.BAYESIAN_OPTIMIZATION.PARAMETER_BOUNDS,
                descr="parameter bounds"),
            agents_constants.BAYESIAN_OPTIMIZATION.POLICY_TYPE: HParam(
                value=PolicyType.LINEAR_THRESHOLD, name=agents_constants.BAYESIAN_OPTIMIZATION.POLICY_TYPE,
                descr="policy type for the execution")
        },
        player_type=PlayerType.DEFENDER, player_idx=0
    )
    env = IntrusionResponseGameLocalStoppingPOMDPDefenderEnv(config=simulation_env_config.simulation_env_input_config)
    agent = BayesOptAgent(emulation_env_config=emulation_env_config, simulation_env_config=simulation_env_config,
                          experiment_config=experiment_config, env=env)
    experiment_execution = agent.train()
    MetastoreFacade.save_experiment_execution(experiment_execution)
    for policy in experiment_execution.result.policies.values():
        if experiment_config.hparams[agents_constants.DIFFERENTIAL_EVOLUTION.POLICY_TYPE].value == \
                PolicyType.MULTI_THRESHOLD:
            MetastoreFacade.save_multi_threshold_stopping_policy(multi_threshold_stopping_policy=policy)
        elif experiment_config.hparams[agents_constants.DIFFERENTIAL_EVOLUTION.POLICY_TYPE].value \
                == PolicyType.LINEAR_THRESHOLD:
            MetastoreFacade.save_linear_threshold_stopping_policy(linear_threshold_stopping_policy=policy)
        else:
            raise ValueError("Policy type: "
                             f"{experiment_config.hparams[agents_constants.DIFFERENTIAL_EVOLUTION.POLICY_TYPE].value} "
                             f"not recognized for differential evolution")
