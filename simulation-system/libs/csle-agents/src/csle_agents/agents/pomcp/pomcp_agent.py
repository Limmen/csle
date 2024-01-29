from typing import Union, List, Dict, Optional
import math
import time
import random
import gymnasium as gym
import os
import numpy as np
import gym_csle_stopping_game.constants.constants as env_constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.training.agent_type import AgentType
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.logging.log import Logger
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_common.util.general_util import GeneralUtil
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_agents.agents.base.base_agent import BaseAgent
import csle_agents.constants.constants as agents_constants
from csle_agents.agents.pomcp.pomcp import POMCP


class POMCPAgent(BaseAgent):
    """
    POMCP Agent
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 emulation_env_config: Union[None, EmulationEnvConfig],
                 experiment_config: ExperimentConfig, env: Optional[BaseEnv] = None,
                 training_job: Optional[TrainingJobConfig] = None, save_to_metastore: bool = True) -> None:
        """
        Initializes the POMCP Agent

        :param simulation_env_config: the simulation env config
        :param emulation_env_config: the emulation env config
        :param experiment_config: the experiment config
        :param env: (optional) the gym environment to use for simulation
        :param training_job: (optional) a training job configuration
        :param save_to_metastore: boolean flag that can be set to avoid saving results and progress to the metastore
        """
        super().__init__(simulation_env_config=simulation_env_config, emulation_env_config=emulation_env_config,
                         experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.POMCP
        self.env = env
        self.training_job = training_job
        self.save_to_metastore = save_to_metastore

    def train(self) -> ExperimentExecution:
        """
        Performs the policy training for the given random seeds using POMCP

        :return: the training metrics and the trained policies
        """
        pid = os.getpid()

        # Initialize metrics
        exp_result = ExperimentResult()
        exp_result.plot_metrics.append(agents_constants.COMMON.AVERAGE_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_RETURN)
        exp_result.plot_metrics.append(env_constants.ENV_METRICS.TIME_HORIZON)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNTIME)

        descr = f"{self.experiment_config.title}. \n Training of policies with the POMCP search algorithm using " \
                f"simulation:{self.simulation_env_config.name}"
        for seed in self.experiment_config.random_seeds:
            exp_result.all_metrics[seed] = {}
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON] = []
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.TIME_HORIZON] = []
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

        for seed in self.experiment_config.random_seeds:
            ExperimentUtil.set_seed(seed)
            exp_result = self.pomcp(exp_result=exp_result, seed=seed, training_job=self.training_job,
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
        return [agents_constants.POMCP.OBJECTIVE_TYPE, agents_constants.POMCP.ROLLOUT_POLICY,
                agents_constants.POMCP.VALUE_FUNCTION, agents_constants.POMCP.N, agents_constants.POMCP.REINVIGORATION,
                agents_constants.POMCP.A, agents_constants.POMCP.GAMMA,
                agents_constants.POMCP.INITIAL_BELIEF, agents_constants.POMCP.PLANNING_TIME,
                agents_constants.POMCP.LOG_STEP_FREQUENCY, agents_constants.POMCP.VERBOSE,
                agents_constants.POMCP.DEFAULT_NODE_VALUE, agents_constants.POMCP.MAX_NEGATIVE_SAMPLES,
                agents_constants.POMCP.MAX_PARTICLES, agents_constants.POMCP.C,
                agents_constants.POMCP.MAX_PLANNING_DEPTH, agents_constants.POMCP.PARALLEL_ROLLOUT,
                agents_constants.POMCP.NUM_PARALLEL_PROCESSES, agents_constants.POMCP.NUM_EVALS_PER_PROCESS,
                agents_constants.POMCP.PRIOR_WEIGHT,
                agents_constants.COMMON.EVAL_BATCH_SIZE, agents_constants.COMMON.CONFIDENCE_INTERVAL,
                agents_constants.COMMON.RUNNING_AVERAGE, agents_constants.COMMON.MAX_ENV_STEPS]

    def pomcp(self, exp_result: ExperimentResult, seed: int,
              training_job: TrainingJobConfig, random_seeds: List[int]) -> ExperimentResult:
        """
        Runs the POMCP algorithm

        :param exp_result: the experiment result object to store the result
        :param seed: the seed
        :param training_job: the training job config
        :param random_seeds: list of seeds
        :return: the updated experiment result and the trained policy
        """
        start: float = time.time()
        rollout_policy = self.experiment_config.hparams[agents_constants.POMCP.ROLLOUT_POLICY].value
        value_function = self.experiment_config.hparams[agents_constants.POMCP.VALUE_FUNCTION].value
        log_steps_frequency = self.experiment_config.hparams[agents_constants.POMCP.LOG_STEP_FREQUENCY].value
        verbose = self.experiment_config.hparams[agents_constants.POMCP.VERBOSE].value
        default_node_value = self.experiment_config.hparams[agents_constants.POMCP.DEFAULT_NODE_VALUE].value
        max_negative_samples = self.experiment_config.hparams[agents_constants.POMCP.MAX_NEGATIVE_SAMPLES].value
        parallel_rollout = self.experiment_config.hparams[agents_constants.POMCP.PARALLEL_ROLLOUT].value
        num_processes = self.experiment_config.hparams[agents_constants.POMCP.NUM_PARALLEL_PROCESSES].value
        num_evals_per_process = self.experiment_config.hparams[agents_constants.POMCP.NUM_EVALS_PER_PROCESS].value
        prior_weight = self.experiment_config.hparams[agents_constants.POMCP.PRIOR_WEIGHT].value
        max_env_steps = self.experiment_config.hparams[agents_constants.COMMON.MAX_ENV_STEPS].value
        N = self.experiment_config.hparams[agents_constants.POMCP.N].value
        A = self.experiment_config.hparams[agents_constants.POMCP.A].value
        reinvigoration = self.experiment_config.hparams[agents_constants.POMCP.REINVIGORATION].value
        gamma = self.experiment_config.hparams[agents_constants.POMCP.GAMMA].value
        b1 = self.experiment_config.hparams[agents_constants.POMCP.INITIAL_BELIEF].value
        planning_time = self.experiment_config.hparams[agents_constants.POMCP.PLANNING_TIME].value
        max_particles = self.experiment_config.hparams[agents_constants.POMCP.MAX_PARTICLES].value
        c = self.experiment_config.hparams[agents_constants.POMCP.C].value
        max_rollout_depth = self.experiment_config.hparams[agents_constants.POMCP.MAX_ROLLOUT_DEPTH].value
        max_planning_depth = self.experiment_config.hparams[agents_constants.POMCP.MAX_PLANNING_DEPTH].value
        config = self.simulation_env_config.simulation_env_input_config
        eval_env: BaseEnv = gym.make(self.simulation_env_config.gym_env_name, config=config)

        # Run N episodes
        for i in range(N):
            done = False
            action_sequence = []
            eval_env = gym.make(self.simulation_env_config.gym_env_name, config=config)
            train_env: BaseEnv = gym.make(self.simulation_env_config.gym_env_name, config=config)

            _, info = eval_env.reset()
            s = info[agents_constants.COMMON.STATE]
            train_env.reset()
            belief = b1.copy()
            pomcp = POMCP(A=A, gamma=gamma, env=train_env, c=c, initial_belief=belief,
                          planning_time=planning_time, max_particles=max_particles, rollout_policy=rollout_policy,
                          value_function=value_function, reinvigoration=reinvigoration, verbose=verbose,
                          default_node_value=default_node_value, parallel_rollout=parallel_rollout,
                          num_parallel_processes=num_processes, num_evals_per_process=num_evals_per_process,
                          prior_weight=prior_weight)
            R = 0
            t = 1
            if t % log_steps_frequency == 0:
                Logger.__call__().get_logger().info(f"[POMCP] t: {t}, b: {belief}, s: {s}")
            # Run episode
            while not done and t <= max_env_steps:
                pomcp.solve(max_rollout_depth=max_rollout_depth, max_planning_depth=max_planning_depth)
                action = pomcp.get_action()
                o, r, done, _, info = eval_env.step(action)
                action_sequence.append(action)
                s_prime = info[agents_constants.COMMON.STATE]
                obs_id = info[agents_constants.COMMON.OBSERVATION]
                belief = pomcp.update_tree_with_new_samples(action_sequence=action_sequence, observation=obs_id,
                                                            max_negative_samples=max_negative_samples,
                                                            observation_vector=o)
                R += r
                t += 1
                if t % log_steps_frequency == 0:
                    rollout_action = -1
                    if rollout_policy is not None:
                        rollout_action = rollout_policy.action(o=o)
                    b = list(map(lambda x: belief[x], random.sample(list(belief.keys()), min(10, len(belief.keys())))))
                    Logger.__call__().get_logger().info(f"[POMCP] t: {t}, a: {action}, r: {r}, o: {obs_id}, "
                                                        f"s_prime: {s_prime}, b: {b}, rollout action: {rollout_action}"
                                                        f", action sequence: {action_sequence}")
                    # Logger.__call__().get_logger().info(f"action: {eval_env.action_id_to_type_and_host[action]}")

            if i % self.experiment_config.log_every == 0:
                # Logging
                exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN].append(R)
                running_avg_J = ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN],
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value)
                exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN].append(running_avg_J)
                progress = round((i + 1) / N, 2)
                time_elapsed_minutes = round((time.time() - start) / 60, 3)
                Logger.__call__().get_logger().info(
                    f"[POMCP] episode: {i}, J:{R}, "
                    f"J_avg_{self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value}:"
                    f"{running_avg_J}, "
                    f"progress: {round(progress * 100, 2)}%, "
                    f"runtime: {time_elapsed_minutes} min")

                # Update training job
                total_iterations = len(random_seeds) * N
                iterations_done = (random_seeds.index(seed)) * N + i
                progress = round(iterations_done / total_iterations, 2)
                training_job.progress_percentage = progress
                training_job.experiment_result = exp_result
                if eval_env is not None and len(eval_env.get_traces()) > 0:
                    training_job.simulation_traces.append(eval_env.get_traces()[-1])
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

        if eval_env is not None:
            # Save latest trace
            if self.save_to_metastore:
                MetastoreFacade.save_simulation_trace(eval_env.get_traces()[-1])
            eval_env.reset_traces()
        return exp_result

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
