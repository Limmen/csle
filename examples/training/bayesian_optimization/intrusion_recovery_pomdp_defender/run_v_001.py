import numpy as np
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.bayesian_optimization.bayes_opt_agent import BayesOptAgent
import csle_agents.constants.constants as agents_constants
from csle_common.dao.training.policy_type import PolicyType
from csle_agents.common.objective_type import ObjectiveType
from csle_tolerance.dao.intrusion_recovery_pomdp_config import IntrusionRecoveryPomdpConfig
from csle_tolerance.util.intrusion_recovery_pomdp_util import IntrusionRecoveryPomdpUtil

if __name__ == '__main__':
    emulation_name = "csle-level9-070"
    emulation_env_config = MetastoreFacade.get_emulation_by_name(emulation_name)
    if emulation_env_config is None:
        raise ValueError(f"Could not find an emulation environment with the name: {emulation_name}")
    simulation_name = "csle-tolerance-intrusion-recovery-pomdp-defender-001"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    input_config: IntrusionRecoveryPomdpConfig = simulation_env_config.simulation_env_input_config
    eta = 1
    p_a = 0.1
    p_c_1 = 0.00001
    p_c_2 = 0.001
    p_u = 0.02
    BTR = np.inf
    negate_costs = False
    discount_factor = 1
    num_observations = 1000
    cost_tensor = IntrusionRecoveryPomdpUtil.cost_tensor(eta=eta, states=IntrusionRecoveryPomdpUtil.state_space(),
                                                         actions=IntrusionRecoveryPomdpUtil.action_space(),
                                                         negate=negate_costs)
    observation_tensor = IntrusionRecoveryPomdpUtil.observation_tensor(
        states=IntrusionRecoveryPomdpUtil.state_space(),
        observations=IntrusionRecoveryPomdpUtil.observation_space(num_observations=num_observations))
    transition_tensor = IntrusionRecoveryPomdpUtil.transition_tensor(
        states=IntrusionRecoveryPomdpUtil.state_space(), actions=IntrusionRecoveryPomdpUtil.action_space(), p_a=p_a,
        p_c_1=p_c_1, p_c_2=p_c_2, p_u=p_u)
    input_config = IntrusionRecoveryPomdpConfig(
        eta=eta, p_a=p_a, p_c_1=p_c_1, p_c_2=p_c_2, p_u=p_u, BTR=BTR, negate_costs=negate_costs, seed=999,
        discount_factor=discount_factor, states=IntrusionRecoveryPomdpUtil.state_space(),
        actions=IntrusionRecoveryPomdpUtil.action_space(),
        observations=IntrusionRecoveryPomdpUtil.observation_space(num_observations=num_observations),
        cost_tensor=cost_tensor, observation_tensor=observation_tensor, transition_tensor=transition_tensor,
        b1=IntrusionRecoveryPomdpUtil.initial_belief(), T=BTR,
        simulation_env_name=simulation_name, gym_env_name="csle-tolerance-intrusion-recovery-pomdp-v1"
    )
    simulation_env_config.simulation_env_input_config = input_config
    L = 1
    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}bayes_opt_test", title="Bayesian Optimization test",
        random_seeds=[561512, 351, 5126, 2350, 16391, 52101, 3520210, 11124, 61912, 888812, 235610, 12511,
                      44102, 21501, 5112, 35011, 7776612, 22212, 2019850, 98212, 333901],
        agent_type=AgentType.BAYESIAN_OPTIMIZATION,
        log_every=1,
        hparams={
            agents_constants.BAYESIAN_OPTIMIZATION.N: HParam(value=500, name=constants.T_SPSA.N,
                                                             descr="the number of training iterations"),
            agents_constants.BAYESIAN_OPTIMIZATION.L: HParam(value=L, name="L", descr="the number of stop actions"),
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=50, name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="number of iterations to evaluate theta"),
            agents_constants.BAYESIAN_OPTIMIZATION.THETA1: HParam(
                value=[0] * L, name=agents_constants.BAYESIAN_OPTIMIZATION.THETA1,
                descr="initial thresholds"),
            agents_constants.COMMON.SAVE_EVERY: HParam(value=1000, name=agents_constants.COMMON.SAVE_EVERY,
                                                       descr="how frequently to save the model"),
            agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                value=0.95, name=agents_constants.COMMON.CONFIDENCE_INTERVAL,
                descr="confidence interval"),
            agents_constants.COMMON.MAX_ENV_STEPS: HParam(
                value=25, name=agents_constants.COMMON.MAX_ENV_STEPS,
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
                descr="xi parameter for the xi utility function"),
            agents_constants.BAYESIAN_OPTIMIZATION.PARAMETER_BOUNDS: HParam(
                value=[(-5, 5)] * L,
                name=agents_constants.BAYESIAN_OPTIMIZATION.PARAMETER_BOUNDS,
                descr="parameter bounds"),
            agents_constants.BAYESIAN_OPTIMIZATION.POLICY_TYPE: HParam(
                value=PolicyType.MULTI_THRESHOLD, name=agents_constants.BAYESIAN_OPTIMIZATION.POLICY_TYPE,
                descr="policy type for the execution"),
            agents_constants.BAYESIAN_OPTIMIZATION.OBJECTIVE_TYPE: HParam(
                value=ObjectiveType.MIN, name=agents_constants.BAYESIAN_OPTIMIZATION.OBJECTIVE_TYPE,
                descr="objetive type for the optimization")
        },
        player_type=PlayerType.DEFENDER, player_idx=0
    )
    agent = BayesOptAgent(emulation_env_config=emulation_env_config, simulation_env_config=simulation_env_config,
                          experiment_config=experiment_config, save_to_metastore=False)
    experiment_execution = agent.train()
    MetastoreFacade.save_experiment_execution(experiment_execution)
    for policy in experiment_execution.result.policies.values():
        if experiment_config.hparams[agents_constants.BAYESIAN_OPTIMIZATION.POLICY_TYPE].value == \
                PolicyType.MULTI_THRESHOLD:
            MetastoreFacade.save_multi_threshold_stopping_policy(multi_threshold_stopping_policy=policy)
        elif experiment_config.hparams[agents_constants.BAYESIAN_OPTIMIZATION.POLICY_TYPE].value \
                == PolicyType.LINEAR_THRESHOLD:
            MetastoreFacade.save_linear_threshold_stopping_policy(linear_threshold_stopping_policy=policy)
        else:
            raise ValueError("Policy type: "
                             f"{experiment_config.hparams[agents_constants.BAYESIAN_OPTIMIZATION.POLICY_TYPE].value} "
                             f"not recognized for Bayesian optimization")
