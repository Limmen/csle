from typing import Union, List, Dict, Optional, Any
import math
import time
import gymnasium as gym
import cma
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
from csle_agents.common.objective_type import ObjectiveType
from csle_agents.agents.base.base_agent import BaseAgent
import csle_agents.constants.constants as agents_constants


class CMAESAgent(BaseAgent):
    """
    Covariance Matrix Adaptation Evolution Strategy (CMA-ES) Agent
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 emulation_env_config: Union[None, EmulationEnvConfig],
                 experiment_config: ExperimentConfig, env: Optional[BaseEnv] = None,
                 training_job: Optional[TrainingJobConfig] = None, save_to_metastore: bool = True):
        """
        Initializes the CMA-ES Agent

        :param simulation_env_config: the simulation env config
        :param emulation_env_config: the emulation env config
        :param experiment_config: the experiment config
        :param env: (optional) the gym environment to use for simulation
        :param training_job: (optional) a training job configuration
        :param save_to_metastore: boolean flag that can be set to avoid saving results and progress to the metastore
        """
        super().__init__(simulation_env_config=simulation_env_config, emulation_env_config=emulation_env_config,
                         experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.CMA_ES
        self.env = env
        self.training_job = training_job
        self.save_to_metastore = save_to_metastore

    def train(self) -> ExperimentExecution:
        """
        Performs the policy training for the given random seeds using CMA-ES

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
        for l in range(1, self.experiment_config.hparams[agents_constants.CMA_ES_OPTIMIZATION.L].value + 1):
            exp_result.plot_metrics.append(f"{env_constants.ENV_METRICS.STOP}_{l}")
            exp_result.plot_metrics.append(f"{env_constants.ENV_METRICS.STOP}_running_average_{l}")

        descr = f"Training of policies with the CMA-ES algorithm using " \
                f"simulation:{self.simulation_env_config.name}"
        for seed in self.experiment_config.random_seeds:
            exp_result.all_metrics[seed] = {}
            exp_result.all_metrics[seed][agents_constants.CMA_ES_OPTIMIZATION.THETAS] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.CMA_ES_OPTIMIZATION.THRESHOLDS] = []
            if self.experiment_config.player_type == PlayerType.DEFENDER:
                for l in range(1, self.experiment_config.hparams[agents_constants.CMA_ES_OPTIMIZATION.L].value + 1):
                    exp_result.all_metrics[seed][
                        f"{agents_constants.CMA_ES_OPTIMIZATION.STOP_DISTRIBUTION_DEFENDER}_l={l}"] = []
            else:
                for s in self.simulation_env_config.state_space_config.states:
                    for l in range(1,
                                   self.experiment_config.hparams[agents_constants.CMA_ES_OPTIMIZATION.L].value + 1):
                        exp_result.all_metrics[seed][agents_constants.CMA_ES_OPTIMIZATION.STOP_DISTRIBUTION_ATTACKER
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
            for l in range(1, self.experiment_config.hparams[agents_constants.CMA_ES_OPTIMIZATION.L].value + 1):
                exp_result.all_metrics[seed][f"{env_constants.ENV_METRICS.STOP}_{l}"] = []
                exp_result.all_metrics[seed][f"{env_constants.ENV_METRICS.STOP}_running_average_{l}"] = []
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
            exp_result = self.cma_es(exp_result=exp_result, seed=seed, training_job=self.training_job,
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
                        if i < len(value_vectors[seed_idx]):
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
        return [agents_constants.CMA_ES_OPTIMIZATION.N,
                agents_constants.CMA_ES_OPTIMIZATION.L, agents_constants.CMA_ES_OPTIMIZATION.THETA1,
                agents_constants.CMA_ES_OPTIMIZATION.UTILITY_FUNCTION,
                agents_constants.CMA_ES_OPTIMIZATION.UCB_KAPPA,
                agents_constants.CMA_ES_OPTIMIZATION.UCB_XI,
                agents_constants.CMA_ES_OPTIMIZATION.PARAMETER_BOUNDS,
                agents_constants.COMMON.EVAL_BATCH_SIZE,
                agents_constants.COMMON.CONFIDENCE_INTERVAL,
                agents_constants.COMMON.RUNNING_AVERAGE]

    def cma_es(self, exp_result: ExperimentResult, seed: int,
               training_job: TrainingJobConfig, random_seeds: List[int]) -> ExperimentResult:
        """
        Runs the CMA-ES algorithm

        :param exp_result: the experiment result object to store the result
        :param seed: the seed
        :param training_job: the training job config
        :param random_seeds: list of seeds
        :return: the updated experiment result and the trained policy
        """
        start: float = time.time()
        L = self.experiment_config.hparams[agents_constants.CMA_ES_OPTIMIZATION.L].value
        objective_type_param = (
            self.experiment_config.hparams[agents_constants.CMA_ES_OPTIMIZATION.OBJECTIVE_TYPE].value)
        if not isinstance(objective_type_param, ObjectiveType):
            raise ValueError("Invalid objective type")
        else:
            objective_type: ObjectiveType = objective_type_param
        if agents_constants.CMA_ES_OPTIMIZATION.THETA1 in self.experiment_config.hparams:
            theta = self.experiment_config.hparams[agents_constants.CMA_ES_OPTIMIZATION.THETA1].value
        else:
            if self.experiment_config.player_type == PlayerType.DEFENDER:
                theta = CMAESAgent.initial_theta(L=L)
            else:
                theta = CMAESAgent.initial_theta(L=2 * L)

        # Initial eval
        policy = self.get_policy(theta=list(theta), L=L)
        if self.env is not None:
            if self.experiment_config.player_type == PlayerType.DEFENDER:
                self.env.unwrapped.static_defender_strategy = policy
            if self.experiment_config.player_type == PlayerType.ATTACKER:
                self.env.unwrapped.static_attacker_strategy = policy
        J = self.J(theta, objetive_type=objective_type)
        policy.avg_R = J
        exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN].append(J)
        exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN].append(J)
        exp_result.all_metrics[seed][agents_constants.CMA_ES_OPTIMIZATION.THETAS].append(
            CMAESAgent.round_vec(theta))
        time_elapsed_minutes = round((time.time() - start) / 60, 3)
        exp_result.all_metrics[seed][agents_constants.COMMON.RUNTIME].append(time_elapsed_minutes)

        # Hyperparameters
        N = self.experiment_config.hparams[agents_constants.CMA_ES_OPTIMIZATION.N].value
        parameter_bounds = self.experiment_config.hparams[agents_constants.BAYESIAN_OPTIMIZATION.PARAMETER_BOUNDS].value
        es = cma.CMAEvolutionStrategy(theta, L / N, {'verb_log': False, 'verbose': False, 'verb_disp': False,
                                                     'verb_time': False, 'bounds': parameter_bounds})
        for i in range(N):
            if es.stop():
                break
            solutions = es.ask()
            values = list(map(lambda x: self.J(x, objetive_type=objective_type), solutions))
            es.tell(solutions, values)
            J = es.result.fbest
            theta = es.result.xbest
            if objective_type == ObjectiveType.MAX:
                J = -J
            policy = self.get_policy(theta=theta, L=L)
            policy.avg_R = J
            running_avg_J = ExperimentUtil.running_average(
                exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN],
                self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value)
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN].append(J)
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN].append(running_avg_J)

            avg_metrics = self.eval_theta(theta)

            # Log runtime
            time_elapsed_minutes = round((time.time() - start) / 60, 3)
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNTIME].append(time_elapsed_minutes)

            # Log thetas
            exp_result.all_metrics[seed][agents_constants.CMA_ES_OPTIMIZATION.THETAS].append(
                CMAESAgent.round_vec(theta))

            if self.experiment_config.hparams[agents_constants.CMA_ES_OPTIMIZATION.POLICY_TYPE] \
                    == PolicyType.MULTI_THRESHOLD:
                # Log thresholds
                exp_result.all_metrics[seed][agents_constants.CMA_ES_OPTIMIZATION.THRESHOLDS].append(
                    CMAESAgent.round_vec(policy.thresholds()))

                # Log stop distribution
                for k, v in policy.stop_distributions().items():
                    exp_result.all_metrics[seed][k].append(v)

            # Log intrusion lengths
            if env_constants.ENV_METRICS.INTRUSION_LENGTH in exp_result.all_metrics:
                exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_LENGTH].append(
                    round(avg_metrics[env_constants.ENV_METRICS.INTRUSION_LENGTH], 3))
            if agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH in exp_result.all_metrics:
                exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH].append(
                    ExperimentUtil.running_average(
                        exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_LENGTH],
                        self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))

            # Log stopping times
            if env_constants.ENV_METRICS.INTRUSION_START in exp_result.all_metrics:
                exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_START].append(
                    round(avg_metrics[env_constants.ENV_METRICS.INTRUSION_START], 3))
            if agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_START in exp_result.all_metrics:
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
            for l in range(1, self.experiment_config.hparams[agents_constants.CMA_ES_OPTIMIZATION.L].value + 1):
                if env_constants.ENV_METRICS.STOP + f"_{l}" in avg_metrics:
                    exp_result.plot_metrics.append(env_constants.ENV_METRICS.STOP + f"_{l}")
                    exp_result.all_metrics[seed][env_constants.ENV_METRICS.STOP + f"_{l}"].append(
                        round(avg_metrics[env_constants.ENV_METRICS.STOP + f"_{l}"], 3))
                    exp_result.all_metrics[seed][env_constants.ENV_METRICS.STOP + f"_running_average_{l}"].append(
                        ExperimentUtil.running_average(
                            exp_result.all_metrics[seed][env_constants.ENV_METRICS.STOP + f"_{l}"],
                            self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))

            # Log baseline returns
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
                    f"[CMA-ES] i: {i}, J:{J}, "
                    f"J_avg_{self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value}:"
                    f"{running_avg_J}, "
                    f"opt_J:{exp_result.all_metrics[seed][env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN][-1]}, "
                    f"theta:{policy.theta}, progress: {round(progress * 100, 2)}%, "
                    f"runtime: {time_elapsed_minutes} min")
        policy = self.get_policy(theta=list(theta), L=L)
        exp_result.policies[seed] = policy
        # Save policy
        if self.save_to_metastore:
            MetastoreFacade.save_multi_threshold_stopping_policy(multi_threshold_stopping_policy=policy)
        return exp_result

    def J(self, theta: List[float], objetive_type: ObjectiveType) -> float:
        """
        The objective function to minimize

        :param theta: the theta vector to evaluate
        :param objetive_type: the objective type
        :return: the objective function value
        """
        if objetive_type == ObjectiveType.MIN:
            return float(round(self.eval_theta(theta)[env_constants.ENV_METRICS.RETURN], 3))
        else:
            return -float(round(self.eval_theta(theta)[env_constants.ENV_METRICS.RETURN], 3))

    def eval_theta(self, theta) -> Dict[str, Any]:
        """
        Evaluates a given threshold policy by running monte-carlo simulations

        :param policy: the policy to evaluate
        :return: the average metrics of the evaluation
        """
        max_steps = self.experiment_config.hparams[agents_constants.COMMON.MAX_ENV_STEPS].value
        L = self.experiment_config.hparams[agents_constants.CMA_ES_OPTIMIZATION.L].value
        if self.experiment_config.hparams[agents_constants.CMA_ES_OPTIMIZATION.POLICY_TYPE].value \
                == PolicyType.MULTI_THRESHOLD.value:
            policy = MultiThresholdStoppingPolicy(
                theta=list(theta), simulation_name=self.simulation_env_config.name,
                states=self.simulation_env_config.state_space_config.states,
                player_type=self.experiment_config.player_type, L=L,
                actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                    self.experiment_config.player_idx].actions, experiment_config=self.experiment_config, avg_R=-1,
                agent_type=AgentType.CMA_ES)
        else:
            policy = LinearThresholdStoppingPolicy(
                theta=list(theta), simulation_name=self.simulation_env_config.name,
                states=self.simulation_env_config.state_space_config.states,
                player_type=self.experiment_config.player_type, L=L,
                actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                    self.experiment_config.player_idx].actions, experiment_config=self.experiment_config, avg_R=-1,
                agent_type=AgentType.CMA_ES)
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
            metrics = CMAESAgent.update_metrics(metrics=metrics, info=info)
        avg_metrics = CMAESAgent.compute_avg_metrics(metrics=metrics)
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

    def get_policy(self, theta: List[float], L: int) \
            -> Union[MultiThresholdStoppingPolicy, LinearThresholdStoppingPolicy]:
        """
        Utility method for getting the policy of a given parameter vector

        :param theta: the parameter vector
        :param L: the number of parameters
        :return: the policy
        """
        if self.experiment_config.hparams[agents_constants.CMA_ES_OPTIMIZATION.POLICY_TYPE].value \
                == PolicyType.MULTI_THRESHOLD.value:
            policy = MultiThresholdStoppingPolicy(
                theta=list(theta), simulation_name=self.simulation_env_config.name,
                states=self.simulation_env_config.state_space_config.states,
                player_type=self.experiment_config.player_type, L=L,
                actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                    self.experiment_config.player_idx].actions, experiment_config=self.experiment_config, avg_R=-1,
                agent_type=AgentType.CMA_ES)
        else:
            policy = LinearThresholdStoppingPolicy(
                theta=list(theta), simulation_name=self.simulation_env_config.name,
                states=self.simulation_env_config.state_space_config.states,
                player_type=self.experiment_config.player_type, L=L,
                actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                    self.experiment_config.player_idx].actions, experiment_config=self.experiment_config, avg_R=-1,
                agent_type=AgentType.CMA_ES)
        return policy
