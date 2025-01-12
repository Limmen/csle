import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.bayesian_optimization_emukit.bayes_opt_emukit_agent import BayesOptEmukitAgent
import csle_agents.constants.constants as agents_constants
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from csle_common.dao.training.policy_type import PolicyType
from csle_agents.agents.bayesian_optimization_emukit.bo.kernel.kernel_type import KernelType
from csle_agents.agents.bayesian_optimization_emukit.bo.acquisition.acquisition_function_type \
    import AcquisitionFunctionType
from csle_agents.agents.bayesian_optimization_emukit.bo.acquisition.acquisition_optimizer_type \
    import AcquisitionOptimizerType
from csle_agents.common.objective_type import ObjectiveType

if __name__ == '__main__':
    emulation_name = "csle-level9-070"
    emulation_env_config = MetastoreFacade.get_emulation_by_name(emulation_name)
    if emulation_env_config is None:
        raise ValueError(f"Could not find an emulation environment with the name: {emulation_name}")
    simulation_name = "csle-stopping-pomdp-defender-002"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}bayes_opt_test", title="Bayesian Optimization with Emukit test",
        random_seeds=[399, 98912],
        agent_type=AgentType.BAYESIAN_OPTIMIZATION_EMUKIT,
        log_every=1,
        hparams={
            agents_constants.BAYESIAN_OPTIMIZATION.N: HParam(value=500, name=constants.T_SPSA.N,
                                                             descr="the number of training iterations"),
            agents_constants.BAYESIAN_OPTIMIZATION.L: HParam(value=3, name="L", descr="the number of stop actions"),
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=100, name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="number of iterations to evaluate theta"),
            agents_constants.BAYESIAN_OPTIMIZATION.THETA1: HParam(
                value=[0, 0, 0], name=agents_constants.BAYESIAN_OPTIMIZATION.THETA1,
                descr="initial thresholds"),
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
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.POLICY_TYPE: HParam(
                value=PolicyType.MULTI_THRESHOLD, name=agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.POLICY_TYPE,
                descr="policy type for the execution"),
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.EVALUATION_BUDGET: HParam(
                value=100, name=agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.EVALUATION_BUDGET,
                descr="evaluation budget"),
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.LENGTHSCALE_RBF_KERNEL: HParam(
                value=1.0, name=agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.LENGTHSCALE_RBF_KERNEL,
                descr="Lengthscale for the RBF kernel"),
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.VARIANCE_RBF_KERNEL: HParam(
                value=1.0, name=agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.VARIANCE_RBF_KERNEL,
                descr="Variance for the RBF kernel"),
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.OBS_LIKELIHOOD_VARIANCE: HParam(
                value=1.0, name=agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.OBS_LIKELIHOOD_VARIANCE,
                descr="Observation likelihood variance"),
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.BETA: HParam(
                value=100, name=agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.BETA,
                descr="The beta parameter for GP-UCB"),
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.INPUT_SPACE_DIM: HParam(
                value=3, name=agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.INPUT_SPACE_DIM,
                descr="Dimension of the input space"),
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.KERNEL_TYPE: HParam(
                value=KernelType.RBF, name=agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.KERNEL_TYPE,
                descr="The type of kernel"),
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.ACQUISITION_FUNCTION_TYPE: HParam(
                value=AcquisitionFunctionType.NEGATIVE_LOWER_CONFIDENCE_BOUND,
                name=agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.ACQUISITION_FUNCTION_TYPE,
                descr="The type of acquisition function"),
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.ACQUISITION_OPTIMIZER_TYPE: HParam(
                value=AcquisitionOptimizerType.GRADIENT,
                name=agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.ACQUISITION_OPTIMIZER_TYPE,
                descr="The type of acquisition optimizer"),
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.OBJECTIVE_TYPE: HParam(
                value=ObjectiveType.MAX,
                name=agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.OBJECTIVE_TYPE,
                descr="The type of objective (min or max)"),
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.X_init: HParam(
                value=[],
                name=agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.X_init,
                descr="The initial X data"),
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.Y_init: HParam(
                value=[],
                name=agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.Y_init,
                descr="The initial Y data"),
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.PARAMS: HParam(
                value=[
                    ("Threshold_1", -5, 5),
                    ("Threshold_2", -5, 5),
                    ("Threshold_3", -5, 5)
                ],
                name=agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.PARAMS,
                descr="The parameters of the optimization")
        },
        player_type=PlayerType.DEFENDER, player_idx=0
    )
    agent = BayesOptEmukitAgent(
        emulation_env_config=emulation_env_config, simulation_env_config=simulation_env_config,
        experiment_config=experiment_config, save_to_metastore=False)
    simulation_env_config.simulation_env_input_config.stopping_game_config.R = list(StoppingGameUtil.reward_tensor(
        R_INT=-1, R_COST=-2, R_SLA=0, R_ST=2, L=3))
    simulation_env_config.simulation_env_input_config.stopping_game_config.L = 3
    experiment_execution = agent.train()
    MetastoreFacade.save_experiment_execution(experiment_execution)
    for policy in experiment_execution.result.policies.values():
        if experiment_config.hparams[agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.POLICY_TYPE].value == \
                PolicyType.MULTI_THRESHOLD:
            MetastoreFacade.save_multi_threshold_stopping_policy(multi_threshold_stopping_policy=policy)
        elif experiment_config.hparams[agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.POLICY_TYPE].value \
                == PolicyType.LINEAR_THRESHOLD:
            MetastoreFacade.save_linear_threshold_stopping_policy(linear_threshold_stopping_policy=policy)
        else:
            raise ValueError(
                "Policy type: "
                f"{experiment_config.hparams[agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.POLICY_TYPE].value} "
                f"not recognized for Bayesian optimization with Emukit")
