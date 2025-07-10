from typing import Union, List, Dict, Optional, Any
import math
import random
import time
import gymnasium as gym
import os
import numpy as np
import numpy.typing as npt
from scipy import stats
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
from csle_common.dao.training.policy_type import PolicyType
from csle_common.util.general_util import GeneralUtil
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_agents.agents.base.base_agent import BaseAgent
import csle_agents.constants.constants as agents_constants
from csle_agents.common.objective_type import ObjectiveType


class CrossEntropyAgent(BaseAgent):
    """
    Cross-Entropy Agent
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 emulation_env_config: Union[None, EmulationEnvConfig],
                 experiment_config: ExperimentConfig, env: Optional[BaseEnv] = None,
                 training_job: Optional[TrainingJobConfig] = None, save_to_metastore: bool = True):
        """
        Initializes the Cross-Entropy Agent

        :param simulation_env_config: the simulation env config
        :param emulation_env_config: the emulation env config
        :param experiment_config: the experiment config
        :param env: (optional) the gym environment to use for simulation
        :param training_job: (optional) a training job configuration
        :param save_to_metastore: boolean flag that can be set to avoid saving results and progress to the metastore
        """
        super().__init__(simulation_env_config=simulation_env_config, emulation_env_config=emulation_env_config,
                         experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.CROSS_ENTROPY
        self.env = env
        self.training_job = training_job
        self.save_to_metastore = save_to_metastore

    def train(self) -> ExperimentExecution:
        """
        Performs the policy training for the given random seeds using cross-entropy method

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
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNTIME)
        for l in range(1, self.experiment_config.hparams[agents_constants.CROSS_ENTROPY.L].value + 1):
            exp_result.plot_metrics.append(env_constants.ENV_METRICS.STOP + f"_{l}")
            exp_result.plot_metrics.append(env_constants.ENV_METRICS.STOP + f"_running_average_{l}")

        descr = f"Training of policies with the cross-entropy algorithm using " \
                f"simulation:{self.simulation_env_config.name}"
        for seed in self.experiment_config.random_seeds:
            exp_result.all_metrics[seed] = {}
            exp_result.all_metrics[seed][agents_constants.CROSS_ENTROPY.THETAS] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.CROSS_ENTROPY.THRESHOLDS] = []
            if self.experiment_config.player_type == PlayerType.DEFENDER:
                for l in range(1, self.experiment_config.hparams[agents_constants.CROSS_ENTROPY.L].value + 1):
                    exp_result.all_metrics[seed][
                        agents_constants.CROSS_ENTROPY.STOP_DISTRIBUTION_DEFENDER + f"_l={l}"] = []
            else:
                for s in self.simulation_env_config.state_space_config.states:
                    for l in range(1, self.experiment_config.hparams[agents_constants.CROSS_ENTROPY.L].value + 1):
                        exp_result.all_metrics[seed][agents_constants.CROSS_ENTROPY.STOP_DISTRIBUTION_ATTACKER
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
            for l in range(1, self.experiment_config.hparams[agents_constants.CROSS_ENTROPY.L].value + 1):
                exp_result.all_metrics[seed][env_constants.ENV_METRICS.STOP + f"_{l}"] = []
                exp_result.all_metrics[seed][env_constants.ENV_METRICS.STOP + f"_running_average_{l}"] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNTIME] = []

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
            result=exp_result, config=self.experiment_config, timestamp=ts, emulation_name=emulation_name,
            simulation_name=simulation_name, descr=descr, log_file_path=self.training_job.log_file_path)
        if self.save_to_metastore:
            exp_execution_id = MetastoreFacade.save_experiment_execution(self.exp_execution)
            self.exp_execution.id = exp_execution_id

        config = self.simulation_env_config.simulation_env_input_config
        if self.env is None:
            self.env = gym.make(self.simulation_env_config.gym_env_name, config=config)
        for seed in self.experiment_config.random_seeds:
            ExperimentUtil.set_seed(seed)
            exp_result = self.cross_entropy(exp_result=exp_result, seed=seed, training_job=self.training_job,
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
        return [agents_constants.CROSS_ENTROPY.N,
                agents_constants.CROSS_ENTROPY.L, agents_constants.CROSS_ENTROPY.THETA1,
                agents_constants.CROSS_ENTROPY.OBJECTIVE_TYPE,
                agents_constants.COMMON.EVAL_BATCH_SIZE,
                agents_constants.COMMON.CONFIDENCE_INTERVAL,
                agents_constants.COMMON.RUNNING_AVERAGE]

    def cross_entropy(self, exp_result: ExperimentResult, seed: int, training_job: TrainingJobConfig,
                      random_seeds: List[int]) -> ExperimentResult:
        """
        Runs the cross-entropy algorithm

        :param exp_result: the experiment result object to store the result
        :param seed: the seed
        :param training_job: the training job config
        :param random_seeds: list of seeds
        :return: the updated experiment result and the trained policy
        """
        start: float = time.time()
        objective_type = ObjectiveType(
            self.experiment_config.hparams[agents_constants.CROSS_ENTROPY.OBJECTIVE_TYPE].value)
        L = self.experiment_config.hparams[agents_constants.CROSS_ENTROPY.L].value
        if agents_constants.CROSS_ENTROPY.THETA1 in self.experiment_config.hparams:
            theta = self.experiment_config.hparams[agents_constants.CROSS_ENTROPY.THETA1].value
        else:
            if self.experiment_config.player_type == PlayerType.DEFENDER:
                theta = CrossEntropyAgent.initial_theta(L=L)
            else:
                theta = CrossEntropyAgent.initial_theta(L=2 * L)

        # Initial eval
        policy = self.get_policy(theta=list(theta), L=L)
        avg_metrics = self.eval_theta(
            policy=policy, max_steps=self.experiment_config.hparams[agents_constants.COMMON.MAX_ENV_STEPS].value)
        J = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
        J_opt = -1
        if agents_constants.COMMON.AVERAGE_UPPER_BOUND_RETURN in avg_metrics:
            J_opt = round(avg_metrics[agents_constants.COMMON.AVERAGE_UPPER_BOUND_RETURN], 3)
        policy.avg_R = J
        exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN].append(J)
        exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN].append(J)
        exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_UPPER_BOUND_RETURN].append(J_opt)
        exp_result.all_metrics[seed][agents_constants.CROSS_ENTROPY.THETAS].append(CrossEntropyAgent.round_vec(theta))
        time_elapsed_minutes = round((time.time() - start) / 60, 3)
        exp_result.all_metrics[seed][agents_constants.COMMON.RUNTIME].append(time_elapsed_minutes)

        Logger.__call__().get_logger().info(
            f"[CROSS-ENTROPY] i: {0}, J:{J}, J_opt:{J_opt}, "
            f"J_avg_{self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value}:"
            f"{J}, sigmoid(theta):{policy.thresholds()}, progress: {0}%")

        # Hyperparameters
        N = self.experiment_config.hparams[agents_constants.CROSS_ENTROPY.N].value
        K = self.experiment_config.hparams[agents_constants.CROSS_ENTROPY.K].value
        lamb = self.experiment_config.hparams[agents_constants.CROSS_ENTROPY.LAMB].value

        means = []
        stds = []
        for l in range(L):
            means.append(random.uniform(0.1, 0.9))
            stds.append(random.uniform(0.01, 0.1))

        for i in range(N):
            theta_samples_and_returns = []
            norm_dist = stats.multivariate_normal(mean=means, cov=np.diag(stds))
            for k in range(K):
                theta_sample = norm_dist.rvs(1)
                if isinstance(theta_sample, np.floating):
                    theta_sample = np.array([theta_sample])
                policy = self.get_policy(theta=list(theta_sample), L=L)
                print(f"{k}/{K}")
                avg_metrics = self.eval_theta(
                    policy=policy,
                    max_steps=self.experiment_config.hparams[agents_constants.COMMON.MAX_ENV_STEPS].value)
                J = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
                OPT_J = -1
                if agents_constants.COMMON.AVERAGE_UPPER_BOUND_RETURN in avg_metrics:
                    OPT_J = round(avg_metrics[agents_constants.COMMON.AVERAGE_UPPER_BOUND_RETURN], 3)
                theta_samples_and_returns.append((theta_sample, J, OPT_J))
            if objective_type == ObjectiveType.MAX:
                sorted_samples = sorted(theta_samples_and_returns, key=lambda x: x[1], reverse=True)
            else:
                sorted_samples = sorted(theta_samples_and_returns, key=lambda x: x[1], reverse=False)
            top_k_index = max(1, int(K * lamb))
            top_k_samples = sorted_samples[0:top_k_index]
            means = np.mean(np.array(list(map(lambda x: x[0], top_k_samples))), axis=0)
            stds = np.std(np.array(list(map(lambda x: x[0], top_k_samples))), axis=0)
            for j in range(len(stds)):
                if stds[j] <= 0:
                    stds[j] = 0.01
            J = top_k_samples[0][1]
            J_opt = top_k_samples[0][2]

            # Log average return
            policy.avg_R = J
            running_avg_J = ExperimentUtil.running_average(
                exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN],
                self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value)
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN].append(J)
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN].append(running_avg_J)

            # Log runtime
            time_elapsed_minutes = round((time.time() - start) / 60, 3)
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNTIME].append(time_elapsed_minutes)

            # Log thresholds
            exp_result.all_metrics[seed][
                agents_constants.CROSS_ENTROPY.THETAS].append(CrossEntropyAgent.round_vec(theta))
            exp_result.all_metrics[seed][agents_constants.CROSS_ENTROPY.THRESHOLDS].append(
                CrossEntropyAgent.round_vec(policy.thresholds()))

            # Log stop distribution
            for k, v in policy.stop_distributions().items():
                exp_result.all_metrics[seed][k].append(v)

            # Log intrusion lengths
            if env_constants.ENV_METRICS.INTRUSION_LENGTH in avg_metrics:
                exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_LENGTH].append(
                    round(avg_metrics[env_constants.ENV_METRICS.INTRUSION_LENGTH], 3))
                exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH].append(
                    ExperimentUtil.running_average(
                        exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_LENGTH],
                        self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))

            # Log stopping times
            if env_constants.ENV_METRICS.INTRUSION_START in avg_metrics:
                exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_START].append(
                    round(avg_metrics[env_constants.ENV_METRICS.INTRUSION_START], 3))
                exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_START].append(
                    ExperimentUtil.running_average(
                        exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_START],
                        self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.TIME_HORIZON].append(
                round(avg_metrics[env_constants.ENV_METRICS.TIME_HORIZON], 3))
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON].append(
                ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][env_constants.ENV_METRICS.TIME_HORIZON],
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))
            for l in range(1, self.experiment_config.hparams[agents_constants.CROSS_ENTROPY.L].value + 1):
                if env_constants.ENV_METRICS.STOP + f"_{l}" in avg_metrics:
                    exp_result.plot_metrics.append(env_constants.ENV_METRICS.STOP + f"_{l}")
                    exp_result.all_metrics[seed][env_constants.ENV_METRICS.STOP + f"_{l}"].append(
                        round(avg_metrics[env_constants.ENV_METRICS.STOP + f"_{l}"], 3))
                    exp_result.all_metrics[seed][env_constants.ENV_METRICS.STOP + f"_running_average_{l}"].append(
                        ExperimentUtil.running_average(
                            exp_result.all_metrics[seed][env_constants.ENV_METRICS.STOP + f"_{l}"],
                            self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))

            # Log baseline returns
            if env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN in avg_metrics:
                exp_result.all_metrics[seed][env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN].append(
                    round(avg_metrics[env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN], 3))
            if env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN in avg_metrics:
                exp_result.all_metrics[seed][
                    env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN].append(
                    round(avg_metrics[env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN],
                          3))

            if i % self.experiment_config.log_every == 0 and i > 0:
                # Update training job
                total_iterations = len(random_seeds) * N
                iterations_done = (random_seeds.index(seed)) * N + i
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
                    f"[CROSS-ENTROPY] i: {i}/{N}, J:{J}, "
                    f"J_avg_{self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value}:"
                    f"{running_avg_J}, "
                    f"opt_J:{J_opt}, "
                    f"sigmoid(theta):{policy.thresholds()}, progress: {round(progress * 100, 2)}%, "
                    f"runtime: {time_elapsed_minutes} min")

        policy = self.get_policy(theta=list(theta), L=L)
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
        :param max_steps: the maximum number of steps in the environment
        :return: the average metrics of the evaluation
        """
        if self.env is None:
            raise ValueError("An environment has to be specified to run the evaluation")
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
            metrics = CrossEntropyAgent.update_metrics(metrics=metrics, info=info)
        avg_metrics = CrossEntropyAgent.compute_avg_metrics(metrics=metrics)
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

    def get_policy(self, theta: List[float], L: int) -> Union[LinearThresholdStoppingPolicy,
                                                              MultiThresholdStoppingPolicy]:
        """
        Utility method for getting the policy of a given parameter vector

        :param theta: the parameter vector
        :param L: the number of parameters
        :return: the policy
        """
        if self.experiment_config.hparams[agents_constants.CROSS_ENTROPY.POLICY_TYPE].value \
                == PolicyType.MULTI_THRESHOLD.value:
            policy = MultiThresholdStoppingPolicy(
                theta=theta, simulation_name=self.simulation_env_config.name,
                states=self.simulation_env_config.state_space_config.states,
                player_type=self.experiment_config.player_type, L=L,
                actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                    self.experiment_config.player_idx].actions, experiment_config=self.experiment_config, avg_R=-1,
                agent_type=AgentType.CROSS_ENTROPY)
        else:
            policy = LinearThresholdStoppingPolicy(
                theta=theta, simulation_name=self.simulation_env_config.name,
                states=self.simulation_env_config.state_space_config.states,
                player_type=self.experiment_config.player_type, L=L,
                actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                    self.experiment_config.player_idx].actions, experiment_config=self.experiment_config, avg_R=-1,
                agent_type=AgentType.CROSS_ENTROPY)
        return policy
