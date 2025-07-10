from typing import Union, List, Dict, Optional, Tuple, Any
import math
import time
import gymnasium as gym
import os
import numpy as np
import numpy.typing as npt
import gym_csle_stopping_game.constants.constants as env_constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.training.agent_type import AgentType
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.logging.log import Logger
from csle_common.dao.training.vector_policy import VectorPolicy
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_common.util.general_util import GeneralUtil
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_agents.agents.base.base_agent import BaseAgent
import csle_agents.constants.constants as agents_constants


class FictitiousPlayAgent(BaseAgent):
    """
    Fictitious Play Agent for Normal-form Games (Brown 1951)
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 experiment_config: ExperimentConfig, env: Optional[BaseEnv] = None,
                 emulation_env_config: Union[None, EmulationEnvConfig] = None,
                 training_job: Optional[TrainingJobConfig] = None, save_to_metastore: bool = True):
        """
        Initializes the Fictitious play agent

        :param simulation_env_config: the simulation env config
        :param emulation_env_config: the emulation env config
        :param experiment_config: the experiment config
        :param env: (optional) the gym environment to use for simulation
        :param training_job: (optional) a training job configuration
        :param save_to_metastore: boolean flag that can be set to avoid saving results and progress to the metastore
        """
        super().__init__(simulation_env_config=simulation_env_config, emulation_env_config=emulation_env_config,
                         experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.FICTITIOUS_PLAY
        self.env = env
        self.training_job = training_job
        self.save_to_metastore = save_to_metastore

    def train(self) -> ExperimentExecution:
        """
        Performs the policy training for the given random seeds using fictitious play

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

        descr = f"Training of policies with the fictitious play algorithm using " \
                f"simulation:{self.simulation_env_config.name}"
        for seed in self.experiment_config.random_seeds:
            exp_result.all_metrics[seed] = {}
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_START] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH] = []
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_START] = []
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_LENGTH] = []
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.TIME_HORIZON] = []
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN] = []
            exp_result.all_metrics[seed][
                env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN] = []

        # Initialize training job
        if self.training_job is None:
            self.training_job = TrainingJobConfig(
                simulation_env_name=self.simulation_env_config.name, experiment_config=self.experiment_config,
                progress_percentage=0, pid=pid, experiment_result=exp_result,
                emulation_env_name=None, simulation_traces=[],
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
        emulation_name = None
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
            exp_result = self.fictitious_play(exp_result=exp_result, seed=seed, training_job=self.training_job,
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
        return [agents_constants.FICTITIOUS_PLAY.N, agents_constants.FICTITIOUS_PLAY.PAYOFF_MATRIX,
                agents_constants.COMMON.EVAL_BATCH_SIZE,
                agents_constants.COMMON.CONFIDENCE_INTERVAL,
                agents_constants.COMMON.RUNNING_AVERAGE]

    def fictitious_play(self, exp_result: ExperimentResult, seed: int,
                        training_job: TrainingJobConfig, random_seeds: List[int]) -> ExperimentResult:
        """
        Runs the fictitious play algorithm

        :param exp_result: the experiment result object to store the result
        :param seed: the seed
        :param training_job: the training job config
        :param random_seeds: list of seeds
        :return: the updated experiment result and the trained policy
        """
        # Hyperparameters
        N = self.experiment_config.hparams[agents_constants.FICTITIOUS_PLAY.N].value
        payoff_matrix = np.array(self.experiment_config.hparams[agents_constants.FICTITIOUS_PLAY.PAYOFF_MATRIX].value)
        p1_prior = self.experiment_config.hparams[agents_constants.FICTITIOUS_PLAY.PLAYER_1_PRIOR].value
        p2_prior = self.experiment_config.hparams[agents_constants.FICTITIOUS_PLAY.PLAYER_2_PRIOR].value

        p1_empirical_strategies = []
        p2_empirical_strategies = []
        p1_best_responses = []
        p2_best_responses = []
        p1_payoffs = []
        p2_payoffs = []

        p1_counts_list = []
        p2_counts_list = []

        p1_counts_list.append(p1_prior)
        p2_counts_list.append(p2_prior)
        p1_empirical_strategy = p1_prior
        p2_empirical_strategy = p2_prior
        J = 0.0
        for i in range(N):
            p1_empirical_strategy = self.compute_empirical_strategy(p1_counts_list[-1])
            p2_empirical_strategy = self.compute_empirical_strategy(p2_counts_list[-1])
            p1_best_response, p1_payoff = self.best_response(p2_empirical_strategy, A=payoff_matrix, maximize=True)
            p2_best_response, p2_payoff = self.best_response(p1_empirical_strategy, A=payoff_matrix, maximize=False)

            p1_empirical_strategies.append(p1_empirical_strategy)
            p2_empirical_strategies.append(p2_empirical_strategy)
            p1_best_responses.append(p1_best_response)
            p2_best_responses.append(p2_best_response)
            p1_payoffs.append(p1_payoff)
            p2_payoffs.append(p2_payoff)

            latest_counts_p1 = p1_counts_list[-1].copy()
            latest_counts_p2 = p2_counts_list[-1].copy()

            latest_counts_p1[p1_best_response] += 1
            latest_counts_p2[p2_best_response] += 1

            p1_counts_list.append(latest_counts_p1)
            p2_counts_list.append(latest_counts_p2)

            # Log average return
            J = p1_payoff
            # policy.avg_R = J
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN].append(J)
            running_avg_J = ExperimentUtil.running_average(
                exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN],
                self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value)
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN].append(running_avg_J)

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
                    f"[FICTITIOUS-PLAY] i: {i}, J:{J}, "
                    f"J_avg_{self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value}:"
                    f"{running_avg_J}")

        p1_policy = VectorPolicy(policy_vector=p1_empirical_strategy, simulation_name=self.simulation_env_config.name,
                                 player_type=self.experiment_config.player_type,
                                 actions=list(range(len(p1_empirical_strategy))),
                                 avg_R=J, agent_type=AgentType.FICTITIOUS_PLAY)
        p2_policy = VectorPolicy(policy_vector=p2_empirical_strategy, simulation_name=self.simulation_env_config.name,
                                 player_type=self.experiment_config.player_type,
                                 actions=list(range(len(p2_empirical_strategy))),
                                 avg_R=J,
                                 agent_type=AgentType.FICTITIOUS_PLAY)
        exp_result.policies[seed] = p1_policy
        exp_result.policies[seed + 1] = p2_policy
        # Save policy
        if self.save_to_metastore:
            MetastoreFacade.save_vector_policy(vector_policy=p1_policy)
            MetastoreFacade.save_vector_policy(vector_policy=p2_policy)
        return exp_result

    def compute_empirical_strategy(self, counts) -> List[float]:
        """
        Computes the empirical strategy from a list of counts

        :param counts: the list of counts
        :return: the empirical strategy
        """
        s = []
        counts_sum = sum(counts)
        for i in range(len(counts)):
            s.append(counts[i] / counts_sum)
        return s

    def best_response(self, p: List[float], A: npt.NDArray[Any], maximize: bool = True) \
            -> Tuple[int, float]:
        """
        Computes a best response against p

        :param p: the opponents strategy vector
        :param A: the payoff matrix
        :param maximize: whether it is a maximizer player or minimizer player
        :return: the best response action and its payoff (value)
        """
        if maximize:
            payoffs = A.dot(np.array(p))
            br = np.argmax(payoffs)
            return int(br), payoffs[int(br)]
        else:
            payoffs = np.array(p).transpose().dot(A)
            br = np.argmin(payoffs)
            return int(br), payoffs[int(br)]

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
    def round_vec(vec) -> List[float]:
        """
        Rounds a vector to 3 decimals

        :param vec: the vector to round
        :return: the rounded vector
        """
        return list(map(lambda x: round(x, 3), vec))
