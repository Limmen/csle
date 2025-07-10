from typing import Union, List, Dict, Optional, Any
import math
import time
import gymnasium as gym
import os
import numpy as np
import numpy.typing as npt
from emukit.core import ParameterSpace, ContinuousParameter
import gym_csle_stopping_game.constants.constants as env_constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.logging.log import Logger
from csle_common.dao.training.multi_threshold_stopping_policy import MultiThresholdStoppingPolicy
from csle_common.dao.training.linear_threshold_stopping_policy import LinearThresholdStoppingPolicy
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_common.util.general_util import GeneralUtil
from csle_common.dao.training.policy_type import PolicyType
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_agents.agents.base.base_agent import BaseAgent
import csle_agents.constants.constants as agents_constants
from csle_agents.agents.bayesian_optimization_emukit.bo.bo_config import BOConfig
from csle_agents.agents.bayesian_optimization_emukit.bo.bo_results import BOResults
from csle_agents.agents.bayesian_optimization_emukit.bo.acquisition.acquisition_optimizer_type import (
    AcquisitionOptimizerType)
from csle_agents.agents.bayesian_optimization_emukit.bo.acquisition.acquisition_function_type import (
    AcquisitionFunctionType)
from csle_agents.agents.bayesian_optimization_emukit.bo.kernel.rbf_kernel_config import RBFKernelConfig
from csle_agents.agents.bayesian_optimization_emukit.bo.gp.gp_config import GPConfig
from csle_agents.agents.bayesian_optimization_emukit.bo.kernel.kernel_type import KernelType
from csle_agents.common.objective_type import ObjectiveType


class BayesOptEmukitAgent(BaseAgent):
    """
    Bayesian Optimization Agent based on the EmuKit framework
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 emulation_env_config: Union[None, EmulationEnvConfig],
                 experiment_config: ExperimentConfig, env: Optional[BaseEnv] = None,
                 training_job: Optional[TrainingJobConfig] = None, save_to_metastore: bool = True):
        """
        Initializes the Bayesian Optimization Agent based on the EmuKit framework

        :param simulation_env_config: the simulation env config
        :param emulation_env_config: the emulation env config
        :param experiment_config: the experiment config
        :param env: (optional) the gym environment to use for simulation
        :param training_job: (optional) a training job configuration
        :param save_to_metastore: boolean flag that can be set to avoid saving results and progress to the metastore
        """
        super().__init__(simulation_env_config=simulation_env_config, emulation_env_config=emulation_env_config,
                         experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.BAYESIAN_OPTIMIZATION_EMUKIT
        self.env = env
        self.training_job = training_job
        self.save_to_metastore = save_to_metastore

    def train(self) -> ExperimentExecution:
        """
        Performs the policy training for the given random seeds using Bayesian Optimization

        :return: the training metrics and the trained policies
        """
        pid = os.getpid()

        # Initialize metrics
        exp_result = ExperimentResult()
        exp_result.plot_metrics.append(agents_constants.COMMON.AVERAGE_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_RETURN)
        exp_result.plot_metrics.append(env_constants.ENV_METRICS.INTRUSION_LENGTH)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH)
        exp_result.plot_metrics.append(env_constants.ENV_METRICS.INTRUSION_START)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_START)
        exp_result.plot_metrics.append(env_constants.ENV_METRICS.TIME_HORIZON)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON)
        exp_result.plot_metrics.append(env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN)
        exp_result.plot_metrics.append(env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN)
        for l in range(1, self.experiment_config.hparams[agents_constants.BAYESIAN_OPTIMIZATION.L].value + 1):
            exp_result.plot_metrics.append(f"{env_constants.ENV_METRICS.STOP}_{l}")
            exp_result.plot_metrics.append(f"{env_constants.ENV_METRICS.STOP}_running_average_{l}")

        descr = f"Training of policies with the Bayesian Optimization Emukit algorithm using " \
                f"simulation:{self.simulation_env_config.name}"
        for seed in self.experiment_config.random_seeds:
            exp_result.all_metrics[seed] = {}
            exp_result.all_metrics[seed][agents_constants.BAYESIAN_OPTIMIZATION.THETAS] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.BAYESIAN_OPTIMIZATION.THRESHOLDS] = []
            if self.experiment_config.player_type == PlayerType.DEFENDER:
                for l in range(1, self.experiment_config.hparams[agents_constants.BAYESIAN_OPTIMIZATION.L].value + 1):
                    exp_result.all_metrics[seed][
                        f"{agents_constants.BAYESIAN_OPTIMIZATION.STOP_DISTRIBUTION_DEFENDER}_l={l}"] = []
            else:
                for s in self.simulation_env_config.state_space_config.states:
                    for l in range(1,
                                   self.experiment_config.hparams[agents_constants.BAYESIAN_OPTIMIZATION.L].value + 1):
                        exp_result.all_metrics[seed][agents_constants.BAYESIAN_OPTIMIZATION.STOP_DISTRIBUTION_ATTACKER
                                                     + f"_l={l}_s={s.id}"] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_START] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH] = []
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_START] = []
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_LENGTH] = []
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.TIME_HORIZON] = []
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN] = []
            exp_result.all_metrics[seed][
                env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN] = []
            for l in range(1, self.experiment_config.hparams[agents_constants.BAYESIAN_OPTIMIZATION.L].value + 1):
                exp_result.all_metrics[seed][f"{env_constants.ENV_METRICS.STOP}_{l}"] = []
                exp_result.all_metrics[seed][f"{env_constants.ENV_METRICS.STOP}_running_average_{l}"] = []

        # Initialize training job
        if self.training_job is None:
            emulation_name = ""
            if self.emulation_env_config is not None:
                emulation_name = self.emulation_env_config.name
            self.training_job = TrainingJobConfig(
                simulation_env_name=self.simulation_env_config.name, experiment_config=self.experiment_config,
                progress_percentage=0, pid=pid, experiment_result=exp_result,
                emulation_env_name=emulation_name, simulation_traces=[],
                num_cached_traces=agents_constants.COMMON.NUM_CACHED_SIMULATION_TRACES,
                log_file_path=Logger.__call__().get_log_file_path(), descr=descr,
                physical_host_ip=GeneralUtil.get_host_ip())
            if self.save_to_metastore:
                training_job_id = MetastoreFacade.save_training_job(training_job=self.training_job)
                self.training_job.id = training_job_id
        else:
            self.training_job.pid = pid
            self.training_job.progress_percentage = 0
            self.training_job.experiment_result = exp_result
            if self.save_to_metastore:
                MetastoreFacade.update_training_job(training_job=self.training_job, id=self.training_job.id)

        # Initialize execution result
        ts = time.time()
        emulation_name = ""
        if self.emulation_env_config is not None:
            emulation_name = self.emulation_env_config.name
        simulation_name = self.simulation_env_config.name
        self.exp_execution = ExperimentExecution(
            result=exp_result, config=self.experiment_config, timestamp=ts,
            emulation_name=emulation_name, simulation_name=simulation_name,
            descr=descr, log_file_path=self.training_job.log_file_path)
        if self.save_to_metastore:
            exp_execution_id = MetastoreFacade.save_experiment_execution(self.exp_execution)
            self.exp_execution.id = exp_execution_id

        config = self.simulation_env_config.simulation_env_input_config
        if self.env is None:
            self.env = gym.make(self.simulation_env_config.gym_env_name, config=config)
        for seed in self.experiment_config.random_seeds:
            ExperimentUtil.set_seed(seed)
            exp_result = self.bayesian_optimization(exp_result=exp_result, seed=seed, training_job=self.training_job,
                                                    random_seeds=self.experiment_config.random_seeds)

        # Calculate average and std metrics
        exp_result.avg_metrics = {}
        exp_result.std_metrics = {}
        for metric in exp_result.all_metrics[self.experiment_config.random_seeds[0]].keys():
            value_vectors = []
            for seed in self.experiment_config.random_seeds:
                value_vectors.append(exp_result.all_metrics[seed][metric])

            avg_metrics = []
            std_metrics = []
            for i in range(len(value_vectors[0])):
                if type(value_vectors[0][0]) is int or type(value_vectors[0][0]) is float \
                        or type(value_vectors[0][0]) is np.int64 or type(value_vectors[0][0]) is np.float64:
                    seed_values = []
                    for seed_idx in range(len(self.experiment_config.random_seeds)):
                        seed_values.append(value_vectors[seed_idx][i])
                    avg = ExperimentUtil.mean_confidence_interval(
                        data=seed_values,
                        confidence=self.experiment_config.hparams[agents_constants.COMMON.CONFIDENCE_INTERVAL].value)[0]
                    if not math.isnan(avg):
                        avg_metrics.append(avg)
                    ci = ExperimentUtil.mean_confidence_interval(
                        data=seed_values,
                        confidence=self.experiment_config.hparams[agents_constants.COMMON.CONFIDENCE_INTERVAL].value)[1]
                    if not math.isnan(ci):
                        std_metrics.append(ci)
                    else:
                        std_metrics.append(-1)
                else:
                    avg_metrics.append(-1)
                    std_metrics.append(-1)
                exp_result.avg_metrics[metric] = avg_metrics
                exp_result.std_metrics[metric] = std_metrics

        ts = time.time()
        self.exp_execution.timestamp = ts
        self.exp_execution.result = exp_result
        if self.save_to_metastore:
            MetastoreFacade.update_experiment_execution(experiment_execution=self.exp_execution,
                                                        id=self.exp_execution.id)
        return self.exp_execution

    def hparam_names(self) -> List[str]:
        """
        :return: a list with the hyperparameter names
        """
        return [agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.POLICY_TYPE,
                agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.EVALUATION_BUDGET,
                agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.LENGTHSCALE_RBF_KERNEL,
                agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.VARIANCE_RBF_KERNEL,
                agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.OBS_LIKELIHOOD_VARIANCE,
                agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.BETA,
                agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.INPUT_SPACE_DIM,
                agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.KERNEL_TYPE,
                agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.ACQUISITION_FUNCTION_TYPE,
                agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.ACQUISITION_OPTIMIZER_TYPE,
                agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.X_init,
                agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.Y_init,
                agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.PARAMS,
                agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.OBJECTIVE_TYPE,
                agents_constants.COMMON.EVAL_BATCH_SIZE,
                agents_constants.COMMON.CONFIDENCE_INTERVAL,
                agents_constants.COMMON.RUNNING_AVERAGE]

    def bayesian_optimization(self, exp_result: ExperimentResult, seed: int,
                              training_job: TrainingJobConfig, random_seeds: List[int]) -> ExperimentResult:
        """
        Runs the Bayesian Optimization algorithm

        :param exp_result: the experiment result object to store the result
        :param seed: the seed
        :param training_job: the training job config
        :param random_seeds: list of seeds
        :return: the updated experiment result and the trained policy
        """
        evaluation_budget = self.experiment_config.hparams[
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.EVALUATION_BUDGET].value
        lengthscale_rbf_kernel = self.experiment_config.hparams[
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.LENGTHSCALE_RBF_KERNEL].value
        variance_rbf_kernel = self.experiment_config.hparams[
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.VARIANCE_RBF_KERNEL].value
        obs_likelihood_variance = self.experiment_config.hparams[
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.OBS_LIKELIHOOD_VARIANCE].value
        beta = self.experiment_config.hparams[
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.BETA].value
        input_space_dim = self.experiment_config.hparams[
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.INPUT_SPACE_DIM].value
        kernel_type = self.experiment_config.hparams[
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.KERNEL_TYPE].value
        acquisition_function_type = self.experiment_config.hparams[
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.ACQUISITION_FUNCTION_TYPE].value
        acquisition_optimizer_type = self.experiment_config.hparams[
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.ACQUISITION_OPTIMIZER_TYPE].value
        objective_type = self.experiment_config.hparams[
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.OBJECTIVE_TYPE].value
        X_init = self.experiment_config.hparams[
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.X_init].value.copy()
        Y_init = self.experiment_config.hparams[
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.Y_init].value.copy()
        params = self.experiment_config.hparams[
            agents_constants.BAYESIAN_OPTIMIZATION_EMUKIT.PARAMS].value
        if kernel_type == KernelType.RBF.value:
            kernel_config = RBFKernelConfig(lengthscale_rbf_kernel=lengthscale_rbf_kernel,
                                            variance_rbf_kernel=variance_rbf_kernel)
        else:
            raise ValueError(f"Kernel type: {kernel_type} not recognized")
        gp_config = GPConfig(kernel_config=kernel_config, obs_likelihood_variance=obs_likelihood_variance)

        # Initial eval
        if len(Y_init) == 0:
            theta = BayesOptEmukitAgent.initial_theta(L=input_space_dim)
            policy = self.get_policy(theta=list(theta), L=input_space_dim)
            avg_metrics = self.eval_theta(
                policy=policy,
                max_steps=self.experiment_config.hparams[agents_constants.COMMON.MAX_ENV_STEPS].value)
            J = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
            X_init.append(theta)
            X_init = np.array(X_init).reshape(1, input_space_dim)
            Y_init.append(J)
            Y_init = np.array(Y_init).reshape(1, 1)
        else:
            X_init = np.array(X_init)
            Y_init = np.array(Y_init)
        J = round(Y_init[0][0], 3)
        exp_result.all_metrics[seed][agents_constants.BAYESIAN_OPTIMIZATION.THETAS].append(
            BayesOptEmukitAgent.round_vec(X_init[0]))
        exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN].append(J)
        exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN].append(J)

        parameters = []
        for i in range(len(params)):
            parameters.append(ContinuousParameter(str(params[i][0]), min_value=float(params[i][1]),
                                                  max_value=float(params[i][2])))
        input_space = ParameterSpace(parameters=parameters)
        bo_config = BOConfig(
            X_init=np.array(X_init),
            Y_init=np.array(Y_init),
            input_space=input_space, evaluation_budget=evaluation_budget, gp_config=gp_config,
            acquisition_function_type=AcquisitionFunctionType(acquisition_function_type),
            acquisition_optimizer_type=AcquisitionOptimizerType(acquisition_optimizer_type),
            objective_type=ObjectiveType(objective_type), beta=beta)

        Logger.__call__().get_logger().info("Starting BO execution")
        results = BOResults(remaining_budget=bo_config.evaluation_budget)

        # If the initial data is empty, pick the first point randomly so that we can initialize surrogate models
        if len(bo_config.X_init) == 0:
            x = []
            for i in range(len(bo_config.input_space.parameters)):
                level = np.random.uniform(bo_config.input_space.parameters[i].min,
                                          bo_config.input_space.parameters[i].max)
                x.append(level)
            bo_config.X_init = np.array([x])
            Y_init = []
            for i in range(len(X_init)):
                theta = X_init[i]
                policy = self.get_policy(theta=list(theta), L=input_space_dim)
                avg_metrics = self.eval_theta(
                    policy=policy,
                    max_steps=self.experiment_config.hparams[agents_constants.COMMON.MAX_ENV_STEPS].value)
                Y_init.append(round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3))
            bo_config.Y_init = np.array(Y_init)

            # Compute cost of the initial point
            results.cumulative_cost += 1
            results.C = np.array([[results.cumulative_cost]])
        else:
            results.C = np.array([[0]])
            results.cumulative_cost = 0

        # Initialize the dataset
        results.X = bo_config.X_init.copy()
        results.Y = bo_config.Y_init.copy()

        # Initialize the best point and initial cost
        if bo_config.objective_type == ObjectiveType.MIN:
            best_index = np.argmin(results.Y)
        else:
            best_index = np.argmax(results.Y)
        results.Y_best = np.array([results.Y[best_index]])
        results.X_best = np.array([results.X[best_index]])

        # Fit the GP surrogate model based on the initial data
        results.surrogate_model = bo_config.gp_config.create_gp(X=bo_config.X_init, Y=bo_config.Y_init,
                                                                input_dim=len(bo_config.input_space.parameters))

        # Define the acquisition function
        results.acquisition = bo_config.get_acquisition_function(surrogate_model=results.surrogate_model)

        # Define the acquisition function optimizer
        results.acquisition_optimizer = bo_config.get_acquisition_optimizer()

        while results.remaining_budget > 0:
            # Update GP model
            results.surrogate_model.optimize()

            # Optimize acquisition function to get next evaluation point
            x, _ = results.acquisition_optimizer.optimize(results.acquisition)

            # Evaluate the objective function at the new point
            policy = self.get_policy(theta=list(x[0]), L=input_space_dim)
            avg_metrics = self.eval_theta(
                policy=policy,
                max_steps=self.experiment_config.hparams[agents_constants.COMMON.MAX_ENV_STEPS].value)
            y = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)

            # Append the new data point to the dataset
            results.X = np.append(results.X, x, axis=0)
            results.Y = np.append(results.Y, [[y]], axis=0)

            # Log average return
            policy.avg_R = y
            running_avg_J = ExperimentUtil.running_average(
                exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN],
                self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value)
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN].append(y)
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN].append(running_avg_J)

            # Log thetas
            exp_result.all_metrics[seed][agents_constants.BAYESIAN_OPTIMIZATION.THETAS].append(
                BayesOptEmukitAgent.round_vec(x[0]))

            if self.experiment_config.hparams[agents_constants.BAYESIAN_OPTIMIZATION.POLICY_TYPE] \
                    == PolicyType.MULTI_THRESHOLD:
                # Log thresholds
                exp_result.all_metrics[seed][agents_constants.BAYESIAN_OPTIMIZATION.THRESHOLDS].append(
                    BayesOptEmukitAgent.round_vec(policy.thresholds()))

            # Log time horizon
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.TIME_HORIZON].append(
                round(avg_metrics[env_constants.ENV_METRICS.TIME_HORIZON], 3))
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON].append(
                ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][env_constants.ENV_METRICS.TIME_HORIZON],
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))

            if results.iteration % self.experiment_config.log_every == 0 and results.iteration > 0:
                # Update training job
                total_iterations = len(random_seeds) * bo_config.evaluation_budget
                iterations_done = (random_seeds.index(seed)) * bo_config.evaluation_budget + results.iteration
                progress = round(iterations_done / total_iterations, 2)
                training_job.progress_percentage = progress
                training_job.experiment_result = exp_result
                if len(training_job.simulation_traces) > training_job.num_cached_traces:
                    training_job.simulation_traces = training_job.simulation_traces[1:]
                if self.save_to_metastore:
                    MetastoreFacade.update_training_job(training_job=training_job, id=training_job.id)

                # Update execution
                ts = time.time()
                self.exp_execution.timestamp = ts
                self.exp_execution.result = exp_result
                if self.save_to_metastore:
                    MetastoreFacade.update_experiment_execution(experiment_execution=self.exp_execution,
                                                                id=self.exp_execution.id)
                Logger.__call__().get_logger().info(
                    f"[BAYES-OPT-EMUKIT] i: {results.iteration}, Best J:{results.Y_best[-1]}, J: {J} "
                    f"J_avg_{self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value}:"
                    f"{running_avg_J}, remaining budget: {results.remaining_budget}, "
                    f"theta:{policy.theta}, progress: {round(progress * 100, 2)}%")

            # Update the GP surrogate model with the new data
            results.surrogate_model.set_data(results.X, results.Y)

            # Compute cost
            results.cumulative_cost += 1
            results.C = np.append(results.C, np.array([[results.cumulative_cost]]), axis=0)

            # Get current optimum
            if bo_config.objective_type == ObjectiveType.MIN:
                best_index_y = np.argmin(results.Y)
            else:
                best_index_y = np.argmax(results.Y)
            results.Y_best = np.append(results.Y_best, [results.Y[best_index_y]], axis=0)
            results.X_best = np.append(results.X_best, [results.X[best_index_y]], axis=0)

            # Move to next iteration
            results.iteration += 1
            results.remaining_budget -= 1

        results.total_time = time.time() - results.start_time
        Logger.__call__().get_logger().info(f"BO execution complete, total time: {round(results.total_time, 2)}s")
        policy = self.get_policy(theta=list(results.X_best[-1]), L=input_space_dim)
        exp_result.policies[seed] = policy

        # Save policy
        if self.save_to_metastore:
            MetastoreFacade.save_multi_threshold_stopping_policy(multi_threshold_stopping_policy=policy)
        return exp_result

    def eval_theta(self, policy: Union[MultiThresholdStoppingPolicy, LinearThresholdStoppingPolicy],
                   max_steps: int = 200) -> Dict[str, Any]:
        """
        Evaluates a given threshold policy by running monte-carlo simulations

        :param policy: the policy to evaluate
        :return: the average metrics of the evaluation
        """
        if self.env is None:
            raise ValueError("An environment need to specified to run the evaluation")
        eval_batch_size = self.experiment_config.hparams[agents_constants.COMMON.EVAL_BATCH_SIZE].value
        metrics: Dict[str, Any] = {}
        for j in range(eval_batch_size):
            done = False
            o, _ = self.env.reset()
            l = int(o[0])
            b1 = o[1]
            t = 1
            r = 0
            a = 0
            info: Dict[str, Any] = {}
            while not done and t <= max_steps:
                Logger.__call__().get_logger().debug(f"t:{t}, a: {a}, b1:{b1}, r:{r}, l:{l}, info:{info}")
                if self.experiment_config.player_type == PlayerType.ATTACKER:
                    policy.opponent_strategy = self.env.unwrapped.static_defender_strategy
                    a = policy.action(o=o)
                else:
                    a = policy.action(o=o)
                o, r, done, _, info = self.env.step(a)
                l = int(o[0])
                b1 = o[1]
                t += 1
            metrics = BayesOptEmukitAgent.update_metrics(metrics=metrics, info=info)
        avg_metrics = BayesOptEmukitAgent.compute_avg_metrics(metrics=metrics)
        return avg_metrics

    @staticmethod
    def update_metrics(metrics: Dict[str, List[Union[float, int]]], info: Dict[str, Union[float, int]]) \
            -> Dict[str, List[Union[float, int]]]:
        """
        Update a dict with aggregated metrics using new information from the environment

        :param metrics: the dict with the aggregated metrics
        :param info: the new information
        :return: the updated dict
        """
        for k, v in info.items():
            if k in metrics:
                metrics[k].append(round(v, 3))
            else:
                metrics[k] = [v]
        return metrics

    @staticmethod
    def compute_avg_metrics(metrics: Dict[str, List[Union[float, int]]]) -> Dict[str, Union[float, int]]:
        """
        Computes the average metrics of a dict with aggregated metrics

        :param metrics: the dict with the aggregated metrics
        :return: the average metrics
        """
        avg_metrics = {}
        for k, v in metrics.items():
            avg = round(sum(v) / len(v), 2)
            avg_metrics[k] = avg
        return avg_metrics

    @staticmethod
    def initial_theta(L: int) -> npt.NDArray[Any]:
        """
        Initializes theta randomly

        :param L: the dimension of theta
        :return: the initialized theta vector
        """
        theta_1 = []
        for k in range(L):
            theta_1.append(np.random.uniform(-3, 3))
        return np.array(theta_1)

    @staticmethod
    def round_vec(vec) -> List[float]:
        """
        Rounds a vector to 3 decimals

        :param vec: the vector to round
        :return: the rounded vector
        """
        return list(map(lambda x: round(x, 3), vec))

    @staticmethod
    def get_theta_vector_from_param_dict(param_dict: Dict[str, float]) -> List[float]:
        """
        Extracts the theta vector from the parameter dict

        :param param_dict: the parameter dict
        :return: the theta vector
        """
        return list(param_dict.values())

    def get_policy(self, theta: List[float], L: int) \
            -> Union[MultiThresholdStoppingPolicy, LinearThresholdStoppingPolicy]:
        """
        Utility method for getting the policy of a given parameter vector

        :param theta: the parameter vector
        :param L: the number of parameters
        :return: the policy
        """
        if self.experiment_config.hparams[agents_constants.BAYESIAN_OPTIMIZATION.POLICY_TYPE].value \
                == PolicyType.MULTI_THRESHOLD.value:
            policy = MultiThresholdStoppingPolicy(
                theta=list(theta), simulation_name=self.simulation_env_config.name,
                states=self.simulation_env_config.state_space_config.states,
                player_type=self.experiment_config.player_type, L=L,
                actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                    self.experiment_config.player_idx].actions, experiment_config=self.experiment_config, avg_R=-1,
                agent_type=AgentType.BAYESIAN_OPTIMIZATION_EMUKIT)
        else:
            policy = LinearThresholdStoppingPolicy(
                theta=list(theta), simulation_name=self.simulation_env_config.name,
                states=self.simulation_env_config.state_space_config.states,
                player_type=self.experiment_config.player_type, L=L,
                actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                    self.experiment_config.player_idx].actions, experiment_config=self.experiment_config, avg_R=-1,
                agent_type=AgentType.BAYESIAN_OPTIMIZATION_EMUKIT)
        return policy
