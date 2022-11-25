import random
from typing import List, Optional, Dict, Tuple
import time
import gym
import os
import sys
import numpy as np
import threading
import gym_csle_stopping_game.constants.constants as env_constants
from csle_system_identification.emulator import Emulator
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_config.emulation_execution import EmulationExecution
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.dao.jobs.data_collection_job_config import DataCollectionJobConfig
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace
from csle_common.logging.log import Logger
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
from csle_agents.agents.base.base_agent import BaseAgent
from csle_common.dao.emulation_action.attacker.emulation_attacker_stopping_actions \
    import EmulationAttackerStoppingActions
from csle_common.dao.emulation_action.defender.emulation_defender_stopping_actions \
    import EmulationDefenderStoppingActions
import csle_agents.constants.constants as agents_constants
from csle_system_identification.expectation_maximization.expectation_maximization_algorithm \
    import ExpectationMaximizationAlgorithm
from csle_common.dao.system_identification.gaussian_mixture_system_model import GaussianMixtureSystemModel
from csle_agents.agents.t_spsa.t_spsa_agent import TSPSAAgent
import csle_system_identification.constants.constants as system_identification_constants
from csle_common.dao.system_identification.system_identification_config import SystemIdentificationConfig
from csle_common.dao.training.policy import Policy
from csle_common.util.read_emulation_statistics_util import ReadEmulationStatisticsUtil
from csle_common.dao.emulation_config.static_emulation_attacker_type import StaticEmulationAttackerType
from csle_common.dao.emulation_config.emulation_statistics_windowed import EmulationStatisticsWindowed


class DataCollectorProcess(threading.Thread):
    """
    Process that interacts with an emulation execution to generate data
    """

    def __init__(self, emulation_execution: EmulationExecution,
                 attacker_sequence: List[EmulationAttackerAction],
                 defender_sequence: List[EmulationDefenderAction],
                 worker_id: int,
                 emulation_statistics_windowed: EmulationStatisticsWindowed,
                 sleep_time: int = 30,
                 emulation_traces_to_save_with_data_collection_job: int = 1,
                 intrusion_start_p: float = 0.1) -> None:
        """
        Initializes the thread

        :param emulation_execution:  the emulation execution to use for data collection
        :param attacker_sequence: the attacker sequence to use for emulating the attacker
        :param defender_sequence: the defender sequence to use for emulating the defender
        :param worker_id: the worker id
        :param sleep_time: the sleep time between actions
        :param emulation_statistics_windowed: the emulation statistics object
        :param emulation_traces_to_save_with_data_collection_job: the number of traces to save with the
                                                                  data collection job
        :param intrusion_start_p: the p parameter in the geometric distribution of the intrusion start time.
        """
        threading.Thread.__init__(self)
        self.running = True
        self.emulation_execution = emulation_execution
        self.attacker_sequence = attacker_sequence
        self.defender_sequence = defender_sequence
        self.sleep_time = sleep_time
        self.worker_id = worker_id
        self.emulation_statistics_windowed = emulation_statistics_windowed
        self.emulation_traces_to_save_with_data_collection_job = emulation_traces_to_save_with_data_collection_job
        self.intrusion_start_p = intrusion_start_p
        self.pid = os.getpid()
        self.data_collection_job = DataCollectionJobConfig(
            emulation_env_name=self.emulation_execution.emulation_env_config.name,
            num_collected_steps=0, progress_percentage=0.0,
            attacker_sequence=attacker_sequence, defender_sequence=defender_sequence,
            pid=self.pid, descr=f"Data collection process in DynaSec with id: {self.worker_id}",
            repeat_times=10000, emulation_statistic_id=self.emulation_statistics_windowed.statistics_id,
            traces=[],
            num_sequences_completed=0, save_emulation_traces_every=1000000,
            num_cached_traces=emulation_traces_to_save_with_data_collection_job,
            log_file_path=Logger.__call__().get_log_file_path())
        self.job_id = MetastoreFacade.save_data_collection_job(
            data_collection_job=self.data_collection_job)
        self.data_collection_job.id = self.job_id
        self.emulation_traces = []
        self.statistics_id = self.emulation_statistics_windowed.statistics_id
        self.completed_episodes = 0

    def run(self) -> None:
        """
        Runs the thread

        :return: None
        """
        s = EmulationEnvState(emulation_env_config=self.emulation_execution.emulation_env_config)
        s.initialize_defender_machines()
        i = 0
        collected_steps = 0
        while self.running:
            intrusion_start_time = np.random.geometric(p=self.intrusion_start_p, size=1)[0]
            attacker_wait_seq = [EmulationAttackerStoppingActions.CONTINUE(index=-1)] * intrusion_start_time
            defender_wait_seq = [EmulationDefenderStoppingActions.CONTINUE(index=-1)] * intrusion_start_time
            full_attacker_sequence = attacker_wait_seq + self.attacker_sequence
            full_defender_sequence = defender_wait_seq + self.defender_sequence
            T = len(full_attacker_sequence)
            assert len(full_defender_sequence) == len(full_attacker_sequence)
            Logger.__call__().get_logger().info(f"Worker {self.worker_id} in DynaSec starting execution of "
                                                f"static action sequences, iteration:{i}, T:{T}, "
                                                f"I_t:{intrusion_start_time}")
            sys.stdout.flush()
            s.reset()
            emulation_trace = EmulationTrace(initial_attacker_observation_state=s.attacker_obs_state,
                                             initial_defender_observation_state=s.defender_obs_state,
                                             emulation_name=self.emulation_execution.emulation_env_config.name)
            s.defender_obs_state.reset_metric_lists()
            time.sleep(self.sleep_time)
            s.defender_obs_state.average_metric_lists()
            self.emulation_statistics_windowed.add_initial_state(s=s.copy())
            for t in range(T):
                old_state = s.copy()
                a1 = full_defender_sequence[t]
                a2 = full_attacker_sequence[t]
                s.defender_obs_state.reset_metric_lists()
                try:
                    emulation_trace, s = Emulator.run_actions(
                        emulation_env_config=self.emulation_execution.emulation_env_config,
                        attacker_action=a2, defender_action=a1,
                        sleep_time=self.sleep_time, trace=emulation_trace, s=s)
                    s.defender_obs_state.average_metric_lists()
                except Exception:
                    Logger.__call__().get_logger().info(f"error in worker: {self.worker_id}")
                    raise Exception(f"error in worker: {self.worker_id}")
                self.emulation_statistics_windowed.add_state_transition(s=old_state.copy(), s_prime=s.copy(),
                                                                        a1=a1.copy(), a2=a2.copy())
                self.emulation_statistics_windowed.update_emulation_statistics()
                total_steps = 10000
                collected_steps += 1
                self.data_collection_job.num_collected_steps = collected_steps
                self.data_collection_job.progress_percentage = (round(collected_steps / total_steps, 2))
                self.data_collection_job.num_sequences_completed = i
                Logger.__call__().get_logger().debug(
                    f"Worker {self.worker_id}, "
                    f"job updated, steps collected: {self.data_collection_job.num_collected_steps}, "
                    f"progress: {self.data_collection_job.progress_percentage}, "
                    f"sequences completed: {i}")
                sys.stdout.flush()
                try:
                    MetastoreFacade.update_data_collection_job(data_collection_job=self.data_collection_job,
                                                               id=self.data_collection_job.id)
                except Exception:
                    pass

            self.emulation_traces = self.emulation_traces + [emulation_trace]
            if len(self.emulation_traces) > self.data_collection_job.num_cached_traces:
                self.data_collection_job.traces = \
                    self.emulation_traces[-self.data_collection_job.num_cached_traces:]
            else:
                self.data_collection_job.traces = self.emulation_traces
            i += 1
            self.completed_episodes += 1


class SystemIdentificationProcess(threading.Thread):
    """
    Process that uses collected data from data collectors to estimate a system model of the data
    """

    def __init__(self, system_identification_config: SystemIdentificationConfig,
                 emulation_statistics: EmulationStatistics, emulation_env_config: EmulationEnvConfig,
                 sleep_time: float, periodic: bool = False) -> None:
        """
        Initializes the thread

        :param system_identification_config: the configuration of the system identification algorithm
        :param emulation_statistics: the emulation statistics to use for system identification
        :param emulation_env_config: the emulation environment configuration
        :param sleep_time: the sleep time
        :param periodic: a boolean flag indicating whether the model should be learned periodically or not
        """
        self.system_identification_config = system_identification_config
        self.emulation_env_config = emulation_env_config
        self.emulation_statistics = emulation_statistics
        threading.Thread.__init__(self)
        self.running = True
        self.system_model = None
        self.periodic = periodic
        self.sleep_time = sleep_time
        self.model_id = None

    def run(self) -> None:
        """
        Runs the thread

        :return: None
        """
        if self.periodic:
            while self.running:
                self.algorithm = ExpectationMaximizationAlgorithm(
                    emulation_env_config=self.emulation_env_config, emulation_statistics=self.emulation_statistics,
                    system_identification_config=self.system_identification_config)
                self.system_model = self.algorithm.fit()
                MetastoreFacade.save_gaussian_mixture_system_model(gaussian_mixture_system_model=self.system_model)
                time.sleep(self.sleep_time * 3)
        else:
            self.algorithm = ExpectationMaximizationAlgorithm(
                emulation_env_config=self.emulation_env_config, emulation_statistics=self.emulation_statistics,
                system_identification_config=self.system_identification_config)
            self.system_model = self.algorithm.fit()
            if self.model_id is None:
                self.model_id = MetastoreFacade.save_gaussian_mixture_system_model(
                    gaussian_mixture_system_model=self.system_model)
            else:
                self.system_model.id = self.model_id
                MetastoreFacade.update_gaussian_mixture_system_model(
                    gaussian_mixture_system_model=self.system_model, id=self.model_id)
            self.running = False


class PolicyOptimizationProcess(threading.Thread):
    """
    Process that optimizes a policy through reinforcement learning and interaction with a system model.
    """

    def __init__(self, system_model: GaussianMixtureSystemModel, experiment_config: ExperimentConfig,
                 emulation_env_config: EmulationEnvConfig, simulation_env_config: SimulationEnvConfig,
                 sleep_time: float, periodic: bool = False) -> None:
        """
        Initializes the thread

        :param system_model: the system model to use for learning
        :param experiment_config: the experiment configuration
        :param emulation_env_config: the configuration of the emulation environment
        :param simulation_env_config: the configuration of the simulation environment
        :param periodic: whether the process should be executed periodically or not
        :param sleep_time: the sleep time
        """
        threading.Thread.__init__(self)
        self.system_model = system_model
        self.emulation_env_config = emulation_env_config
        self.experiment_config = experiment_config
        self.simulation_env_config = simulation_env_config
        self.experiment_execution = None
        self.running = True
        self.periodic = periodic
        self.sleep_time = sleep_time
        self.training_job = None
        self.policy = None

    def run(self) -> None:
        """
        Runs the thread

        :return: None
        """
        if not self.periodic:
            sample_space = self.simulation_env_config.simulation_env_input_config.stopping_game_config.O.tolist()
            self.simulation_env_config.simulation_env_input_config.stopping_game_config.Z, _, _ = \
                DynaSecAgent.get_Z_from_system_model(system_model=self.system_model,
                                                     sample_space=sample_space)
            self.agent = TSPSAAgent(emulation_env_config=self.emulation_env_config,
                                    simulation_env_config=self.simulation_env_config,
                                    experiment_config=self.experiment_config)
            self.experiment_execution = self.agent.train()
            MetastoreFacade.save_experiment_execution(self.experiment_execution)
            # for policy in self.experiment_execution.result.policies.values():
            #     MetastoreFacade.save_multi_threshold_stopping_policy(multi_threshold_stopping_policy=policy)
            self.running = False
        else:
            while self.running:
                sample_space = self.simulation_env_config.simulation_env_input_config.stopping_game_config.O.tolist()
                self.simulation_env_config.simulation_env_input_config.stopping_game_config.Z, _, _ = \
                    DynaSecAgent.get_Z_from_system_model(system_model=self.system_model, sample_space=sample_space)
                self.agent = TSPSAAgent(emulation_env_config=self.emulation_env_config,
                                        simulation_env_config=self.simulation_env_config,
                                        experiment_config=self.experiment_config, training_job=self.training_job)
                self.experiment_execution = self.agent.train()
                self.training_job = self.agent.training_job
                MetastoreFacade.save_experiment_execution(self.experiment_execution)
                # for policy in self.experiment_execution.result.policies.values():
                #     MetastoreFacade.save_multi_threshold_stopping_policy(multi_threshold_stopping_policy=policy)
                self.policy = list(self.experiment_execution.result.policies.values())[0]
                time.sleep(self.sleep_time * 3)


class EmulationMonitorThread(threading.Thread):
    """
    Process collects data from the emulation
    """

    def __init__(self, exp_result: ExperimentResult, emulation_env_config: EmulationEnvConfig,
                 sleep_time_minutes: int, seed: int) -> None:
        """
        Initializes the thread

        :param exp_result: the object to track data
        :param emulation_env_config: the emulation environment configuration
        :param sleep_time_minutes: sleep time between measurements
        :param seed: the random seed
        """
        threading.Thread.__init__(self)
        self.exp_result = exp_result
        self.emulation_env_config = emulation_env_config
        self.sleep_time_minutes = sleep_time_minutes
        self.running = True
        self.seed = seed

    def run(self) -> None:
        """
        Runs the thread

        :return: None
        """
        Logger.__call__().get_logger().info("[DynaSec] starting emulation monitor thread")
        while self.running:
            time.sleep(self.sleep_time_minutes)
            metrics = ReadEmulationStatisticsUtil.read_all(emulation_env_config=self.emulation_env_config,
                                                           time_window_minutes=self.sleep_time_minutes)
            if len(metrics.client_metrics) > 0:
                num_clients = metrics.client_metrics[0].num_clients
                self.exp_result.all_metrics[self.seed][agents_constants.DYNASEC.NUM_CLIENTS].append(num_clients)
                clients_arrival_rate = metrics.client_metrics[0].rate
                self.exp_result.all_metrics[self.seed][agents_constants.DYNASEC.CLIENTS_ARRIVAL_RATE].append(
                    clients_arrival_rate)


class EmulationStatisticsThread(threading.Thread):
    """
    Process that tracks the emulation statistics
    """

    def __init__(self, exp_result: ExperimentResult, emulation_env_config: EmulationEnvConfig,
                 sleep_time: int, seed: int,
                 data_collector_processes: List[DataCollectorProcess]) -> None:
        """
        Initializes the thread

        :param exp_result: the object to track data
        :param emulation_env_config: the emulation environment configuration
        :param sleep_time: sleep time between measurements
        :param replay_window_size: the replay window size
        :param seed: the random seed
        :param emulation_statistics: the emulation statistics
        :param data_collector_processes: the data collector processes to monitor
        """
        threading.Thread.__init__(self)
        self.exp_result = exp_result
        self.emulation_env_config = emulation_env_config
        self.sleep_time = sleep_time
        self.running = True
        self.seed = seed
        self.new_traces = []
        self.data_collector_processes = data_collector_processes

    def run(self) -> None:
        """
        Runs the thread

        :return: None
        """
        Logger.__call__().get_logger().info("[DynaSec] starting emulation statistics aggeregation thread")
        while self.running:
            time.sleep(self.sleep_time)
            for dcp in self.data_collector_processes:
                if len(dcp.emulation_traces) > 0:
                    self.new_traces = self.new_traces + dcp.emulation_traces
                    dcp.emulation_traces = []


class PolicyEvaluationThread(threading.Thread):
    """
    Process that evaluates the policies periodically
    """

    def __init__(self, exp_result: ExperimentResult, emulation_env_config: EmulationEnvConfig,
                 sleep_time: int, seed: int, policy: Policy, baseline_policy: Policy,
                 emulation_statistics_thread: EmulationStatisticsThread,
                 system_model: GaussianMixtureSystemModel,
                 baseline_system_model: GaussianMixtureSystemModel, max_steps: int,
                 experiment_config: ExperimentConfig, simulation_env_config: SimulationEnvConfig,
                 env: gym.Env) -> None:
        """
        Initializes the thread

        :param exp_result: the experiment result
        :param emulation_env_config: the emulation env config
        :param sleep_time: the sleep time
        :param seed: the seed of the experiment
        :param policy: the policy to evaluate
        :param baseline_policy: the baseline policy to evaluate
        :param emulation_statistics_thread: the thread managing emulation statistics
        :param system_model: the system model to use for evaluation
        :param baseline_system_model: the baseline system model to use for evaluation
        :param max_steps: max environment steps for evaluation
        :param experiment_config: the experiment config
        :param simulation_env_config: the simulation env config
        :param env: the env for evaluation
        """
        threading.Thread.__init__(self)
        self.exp_result = exp_result
        self.emulation_env_config = emulation_env_config
        self.sleep_time = sleep_time
        self.running = True
        self.seed = seed
        self.policy = policy
        self.baseline_policy = baseline_policy
        self.emulation_statistics_thread = emulation_statistics_thread
        self.system_model = system_model
        self.baseline_system_model = baseline_system_model
        self.max_steps = max_steps
        self.experiment_config = experiment_config
        self.simulation_env_config = simulation_env_config
        self.env = env

    def record_metrics(self, exp_result: ExperimentResult, seed: int, metrics_dict: Dict,
                       eval: bool = False, baseline: bool = False):
        if not eval and baseline:
            exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                         agents_constants.COMMON.AVERAGE_RETURN].append(
                metrics_dict[seed][
                    env_constants.ENV_METRICS.RETURN])
            exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                         agents_constants.COMMON.RUNNING_AVERAGE_RETURN].append(
                ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                                 agents_constants.COMMON.AVERAGE_RETURN],
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))
            exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                         env_constants.ENV_METRICS.INTRUSION_LENGTH].append(
                metrics_dict[seed][env_constants.ENV_METRICS.INTRUSION_LENGTH])
            exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                         agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH].append(
                ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                                 env_constants.ENV_METRICS.INTRUSION_LENGTH],
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_START].append(
                metrics_dict[seed][
                    env_constants.ENV_METRICS.INTRUSION_START])
            exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                         env_constants.ENV_METRICS.TIME_HORIZON].append(
                metrics_dict[seed][
                    env_constants.ENV_METRICS.TIME_HORIZON])
            exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                         agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON].append(
                ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                                 env_constants.ENV_METRICS.TIME_HORIZON],
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))
            for l in range(1, self.experiment_config.hparams[agents_constants.T_SPSA.L].value + 1):
                exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                             env_constants.ENV_METRICS.STOP + f"_{l}"].append(
                    metrics_dict[seed][
                        env_constants.ENV_METRICS.STOP + f"_{l}"])
                exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                             env_constants.ENV_METRICS.STOP + f"_running_average_{l}"].append(
                    ExperimentUtil.running_average(
                        exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                                     env_constants.ENV_METRICS.STOP + f"_{l}"],
                        self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))
            exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                         env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN].append(
                metrics_dict[seed][
                    env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN])
            exp_result.all_metrics[seed][
                agents_constants.COMMON.BASELINE_PREFIX +
                env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN].append(
                metrics_dict[seed][
                    env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN])
        else:
            exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                         agents_constants.COMMON.AVERAGE_RETURN].append(
                metrics_dict[seed][
                    env_constants.ENV_METRICS.RETURN])
            exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                         agents_constants.COMMON.RUNNING_AVERAGE_RETURN].append(
                ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                                 agents_constants.COMMON.AVERAGE_RETURN],
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))
            exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                         env_constants.ENV_METRICS.INTRUSION_LENGTH].append(
                metrics_dict[seed][env_constants.ENV_METRICS.INTRUSION_LENGTH])
            exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                         agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH].append(
                ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                                 env_constants.ENV_METRICS.INTRUSION_LENGTH],
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_START].append(
                metrics_dict[seed][
                    env_constants.ENV_METRICS.INTRUSION_START])
            exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                         env_constants.ENV_METRICS.TIME_HORIZON].append(
                metrics_dict[seed][
                    env_constants.ENV_METRICS.TIME_HORIZON])
            exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                         agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON].append(
                ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                                 env_constants.ENV_METRICS.TIME_HORIZON],
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))
            for l in range(1, self.experiment_config.hparams[agents_constants.T_SPSA.L].value + 1):
                exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                             env_constants.ENV_METRICS.STOP + f"_{l}"].append(
                    metrics_dict[seed][
                        env_constants.ENV_METRICS.STOP + f"_{l}"])
                exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                             env_constants.ENV_METRICS.STOP + f"_running_average_{l}"].append(
                    ExperimentUtil.running_average(
                        exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                                     env_constants.ENV_METRICS.STOP + f"_{l}"],
                        self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))
            exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                         env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN].append(
                metrics_dict[seed][
                    env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN])
            exp_result.all_metrics[seed][
                agents_constants.COMMON.EVAL_PREFIX +
                env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN].append(
                metrics_dict[seed][
                    env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN])
        return exp_result

    def eval_traces(self, traces: List[EmulationTrace], defender_policy: Policy, max_steps: int,
                    system_model: GaussianMixtureSystemModel, baseline: bool = False):
        sample_space = self.simulation_env_config.simulation_env_input_config.stopping_game_config.O.tolist()
        old_Z = self.simulation_env_config.simulation_env_input_config.stopping_game_config.Z.copy()
        self.simulation_env_config.simulation_env_input_config.stopping_game_config.Z, int_mean, no_int_mean = \
            DynaSecAgent.get_Z_from_system_model(system_model=system_model, sample_space=sample_space)
        if baseline:
            self.exp_result.all_metrics[self.seed][
                agents_constants.DYNASEC.NO_INTRUSION_ALERTS_MEAN_BASELINE].append(no_int_mean)
            self.exp_result.all_metrics[self.seed][
                agents_constants.DYNASEC.INTRUSION_ALERTS_MEAN_BASELINE].append(int_mean)
        else:
            self.exp_result.all_metrics[self.seed][
                agents_constants.DYNASEC.NO_INTRUSION_ALERTS_MEAN].append(no_int_mean)
            self.exp_result.all_metrics[self.seed][agents_constants.DYNASEC.INTRUSION_ALERTS_MEAN].append(int_mean)
        metrics = {}
        for trace in traces:
            done = False
            o = self.env.reset()
            l = int(o[0])
            b1 = o[1]
            t = 1
            r = 0
            a = 0
            info = {}
            while not done and t <= max_steps:
                Logger.__call__().get_logger().debug(f"t:{t}, a: {a}, b1:{b1}, r:{r}, l:{l}, info:{info}")
                a = defender_policy.action(o=o)
                o, r, done, info = self.env.step_trace(trace=trace, a1=a)
                l = int(o[0])
                b1 = o[1]
                t += 1
            metrics = TSPSAAgent.update_metrics(metrics=metrics, info=info)
        avg_metrics = TSPSAAgent.compute_avg_metrics(metrics=metrics)
        self.simulation_env_config.simulation_env_input_config.stopping_game_config.Z = old_Z
        return avg_metrics

    def run(self) -> None:
        """
        Runs the thread

        :return: None
        """
        Logger.__call__().get_logger().info("[DynaSec] starting the policy evaluation thread")
        evaluation_traces = []
        while self.running:
            time.sleep(self.sleep_time)
            new_traces = self.emulation_statistics_thread.new_traces
            if len(new_traces) > 0:
                # evaluation_traces = evaluation_traces + new_traces
                evaluation_traces = new_traces
                self.emulation_statistics_thread.new_traces = []
                print(f"num evaluation traces: {len(evaluation_traces)}")
                if len(evaluation_traces) > 50:
                    evaluation_traces = evaluation_traces[-50:]
                avg_metrics = self.eval_traces(traces=evaluation_traces, defender_policy=self.policy,
                                               max_steps=self.max_steps,
                                               system_model=self.system_model, baseline=False)
                avg_metrics_seed = {}
                avg_metrics_seed[self.seed] = avg_metrics
                self.exp_result = self.record_metrics(
                    exp_result=self.exp_result, seed=self.seed,
                    metrics_dict=avg_metrics_seed, eval=True, baseline=False)

                avg_metrics = self.eval_traces(traces=evaluation_traces, defender_policy=self.baseline_policy,
                                               max_steps=self.max_steps,
                                               system_model=self.baseline_system_model, baseline=True)
                avg_metrics_seed = {}
                avg_metrics_seed[self.seed] = avg_metrics
                self.exp_result = self.record_metrics(
                    exp_result=self.exp_result, seed=self.seed,
                    metrics_dict=avg_metrics_seed, baseline=True, eval=False)


class DynaSecAgent(BaseAgent):
    """
    DynaSec
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 emulation_executions: List[EmulationExecution],
                 attacker_sequence: List[EmulationAttackerAction], defender_sequence: List[EmulationDefenderAction],
                 system_identification_config: SystemIdentificationConfig,
                 experiment_config: ExperimentConfig, env: Optional[gym.Env] = None,
                 training_job: Optional[TrainingJobConfig] = None, save_to_metastore: bool = True):
        """
        Initializes the DynaSec agent

        :param simulation_env_config: the simulation env config
        :param emulation_env_config: the emulation env config
        :param system_identification_config: the system identification config
        :param attacker_sequence: attacker sequence to emulate intrusions
        :param defender_sequence: defender sequence to emulate defense
        :param experiment_config: the experiment config
        :param env: (optional) the gym environment to use for simulation
        :param training_job: (optional) a training job configuration
        :param save_to_metastore: boolean flag that can be set to avoid saving results and progress to the metastore
        """
        assert len(emulation_executions) > 0
        super().__init__(simulation_env_config=simulation_env_config,
                         emulation_env_config=emulation_executions[0].emulation_env_config,
                         experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.DYNA_SEC
        self.env = env
        self.training_job = training_job
        self.save_to_metastore = save_to_metastore
        self.attacker_sequence = attacker_sequence
        self.defender_sequence = defender_sequence
        self.emulation_executions = emulation_executions
        self.system_identification_config = system_identification_config

    def get_spsa_experiment_config(self) -> ExperimentConfig:
        """
        :return: the experiment configuration for SPSA training
        """
        hparams = {
            agents_constants.T_SPSA.N: self.experiment_config.hparams[agents_constants.T_SPSA.N],
            agents_constants.T_SPSA.c: self.experiment_config.hparams[agents_constants.T_SPSA.c],
            agents_constants.T_SPSA.a: self.experiment_config.hparams[agents_constants.T_SPSA.a],
            agents_constants.T_SPSA.A: self.experiment_config.hparams[agents_constants.T_SPSA.A],
            agents_constants.T_SPSA.LAMBDA: self.experiment_config.hparams[agents_constants.T_SPSA.LAMBDA],
            agents_constants.T_SPSA.EPSILON: self.experiment_config.hparams[agents_constants.T_SPSA.EPSILON],
            agents_constants.T_SPSA.L: self.experiment_config.hparams[agents_constants.T_SPSA.L],
            agents_constants.COMMON.EVAL_BATCH_SIZE: self.experiment_config.hparams[
                agents_constants.COMMON.EVAL_BATCH_SIZE],
            agents_constants.COMMON.CONFIDENCE_INTERVAL: self.experiment_config.hparams[
                agents_constants.COMMON.CONFIDENCE_INTERVAL],
            agents_constants.COMMON.MAX_ENV_STEPS: self.experiment_config.hparams[
                agents_constants.COMMON.MAX_ENV_STEPS],
            agents_constants.T_SPSA.GRADIENT_BATCH_SIZE: self.experiment_config.hparams[
                agents_constants.T_SPSA.GRADIENT_BATCH_SIZE],
            agents_constants.COMMON.RUNNING_AVERAGE: self.experiment_config.hparams[
                agents_constants.COMMON.RUNNING_AVERAGE],
            agents_constants.COMMON.GAMMA: self.experiment_config.hparams[
                agents_constants.COMMON.GAMMA],
            agents_constants.T_SPSA.THETA1: self.experiment_config.hparams[agents_constants.T_SPSA.THETA1]
        }
        return ExperimentConfig(
            output_dir=str(self.experiment_config.output_dir),
            title="Learning a policy through T-SPSA",
            random_seeds=self.experiment_config.random_seeds, agent_type=AgentType.T_SPSA,
            log_every=self.experiment_config.log_every,
            hparams=hparams,
            player_type=self.experiment_config.player_type, player_idx=self.experiment_config.player_idx
        )

    def train(self) -> ExperimentExecution:
        """
        Performs the policy training for the given random seeds using T-SPSA

        :return: the training metrics and the trained policies
        """
        pid = os.getpid()

        # Initialize metrics
        exp_result = ExperimentResult()
        exp_result.plot_metrics.append(agents_constants.DYNASEC.NUM_CLIENTS)
        exp_result.plot_metrics.append(agents_constants.DYNASEC.INTRUSION_ALERTS_MEAN)
        exp_result.plot_metrics.append(agents_constants.DYNASEC.NO_INTRUSION_ALERTS_MEAN)
        exp_result.plot_metrics.append(agents_constants.DYNASEC.INTRUSION_ALERTS_MEAN_BASELINE)
        exp_result.plot_metrics.append(agents_constants.DYNASEC.NO_INTRUSION_ALERTS_MEAN_BASELINE)
        exp_result.plot_metrics.append(agents_constants.DYNASEC.CLIENTS_ARRIVAL_RATE)
        exp_result.plot_metrics.append(agents_constants.DYNASEC.STATIC_ATTACKER_TYPE)
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

        exp_result.plot_metrics.append(agents_constants.COMMON.EVAL_PREFIX +
                                       agents_constants.COMMON.AVERAGE_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.EVAL_PREFIX +
                                       agents_constants.COMMON.RUNNING_AVERAGE_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.EVAL_PREFIX +
                                       env_constants.ENV_METRICS.INTRUSION_LENGTH)
        exp_result.plot_metrics.append(agents_constants.COMMON.EVAL_PREFIX +
                                       agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH)
        exp_result.plot_metrics.append(agents_constants.COMMON.EVAL_PREFIX +
                                       env_constants.ENV_METRICS.INTRUSION_START)
        exp_result.plot_metrics.append(agents_constants.COMMON.EVAL_PREFIX +
                                       agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_START)
        exp_result.plot_metrics.append(agents_constants.COMMON.EVAL_PREFIX +
                                       env_constants.ENV_METRICS.TIME_HORIZON)
        exp_result.plot_metrics.append(agents_constants.COMMON.EVAL_PREFIX +
                                       agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON)
        exp_result.plot_metrics.append(agents_constants.COMMON.EVAL_PREFIX +
                                       env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.EVAL_PREFIX +
                                       env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN)

        exp_result.plot_metrics.append(agents_constants.COMMON.BASELINE_PREFIX +
                                       agents_constants.COMMON.AVERAGE_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.BASELINE_PREFIX +
                                       agents_constants.COMMON.RUNNING_AVERAGE_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.BASELINE_PREFIX +
                                       env_constants.ENV_METRICS.INTRUSION_LENGTH)
        exp_result.plot_metrics.append(agents_constants.COMMON.BASELINE_PREFIX +
                                       agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH)
        exp_result.plot_metrics.append(agents_constants.COMMON.BASELINE_PREFIX +
                                       env_constants.ENV_METRICS.INTRUSION_START)
        exp_result.plot_metrics.append(agents_constants.COMMON.BASELINE_PREFIX +
                                       agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_START)
        exp_result.plot_metrics.append(agents_constants.COMMON.BASELINE_PREFIX +
                                       env_constants.ENV_METRICS.TIME_HORIZON)
        exp_result.plot_metrics.append(agents_constants.COMMON.BASELINE_PREFIX +
                                       agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON)
        exp_result.plot_metrics.append(agents_constants.COMMON.BASELINE_PREFIX +
                                       env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.BASELINE_PREFIX +
                                       env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN)

        for l in range(1, self.experiment_config.hparams[agents_constants.T_SPSA.L].value + 1):
            exp_result.plot_metrics.append(env_constants.ENV_METRICS.STOP + f"_{l}")
            exp_result.plot_metrics.append(env_constants.ENV_METRICS.STOP + f"_running_average_{l}")
            exp_result.plot_metrics.append(agents_constants.COMMON.EVAL_PREFIX +
                                           env_constants.ENV_METRICS.STOP + f"_{l}")
            exp_result.plot_metrics.append(agents_constants.COMMON.EVAL_PREFIX +
                                           env_constants.ENV_METRICS.STOP + f"_running_average_{l}")
            exp_result.plot_metrics.append(agents_constants.COMMON.BASELINE_PREFIX +
                                           env_constants.ENV_METRICS.STOP + f"_{l}")
            exp_result.plot_metrics.append(agents_constants.COMMON.BASELINE_PREFIX +
                                           env_constants.ENV_METRICS.STOP + f"_running_average_{l}")

        descr = f"Training of policies with the DynaSec algorithm using " \
                f"simulation:{self.simulation_env_config.name} and {len(self.emulation_executions)} " \
                f"emulation executions of emulation {self.emulation_executions[0].emulation_env_config.name}"

        for seed in self.experiment_config.random_seeds:
            exp_result.all_metrics[seed] = {}
            exp_result.all_metrics[seed][agents_constants.DYNASEC.NUM_CLIENTS] = []
            exp_result.all_metrics[seed][agents_constants.DYNASEC.INTRUSION_ALERTS_MEAN] = []
            exp_result.all_metrics[seed][agents_constants.DYNASEC.NO_INTRUSION_ALERTS_MEAN] = []
            exp_result.all_metrics[seed][agents_constants.DYNASEC.INTRUSION_ALERTS_MEAN_BASELINE] = []
            exp_result.all_metrics[seed][agents_constants.DYNASEC.NO_INTRUSION_ALERTS_MEAN_BASELINE] = []
            exp_result.all_metrics[seed][agents_constants.DYNASEC.CLIENTS_ARRIVAL_RATE] = []
            exp_result.all_metrics[seed][agents_constants.DYNASEC.STATIC_ATTACKER_TYPE] = []
            exp_result.all_metrics[seed][agents_constants.T_SPSA.THETAS] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.T_SPSA.THRESHOLDS] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                         agents_constants.COMMON.AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                         agents_constants.COMMON.RUNNING_AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                         agents_constants.COMMON.AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                         agents_constants.COMMON.RUNNING_AVERAGE_RETURN] = []
            if self.experiment_config.player_type == PlayerType.DEFENDER:
                for l in range(1, self.experiment_config.hparams[agents_constants.T_SPSA.L].value + 1):
                    exp_result.all_metrics[seed][agents_constants.T_SPSA.STOP_DISTRIBUTION_DEFENDER + f"_l={l}"] = []
            else:
                for s in self.simulation_env_config.state_space_config.states:
                    for l in range(1, self.experiment_config.hparams[agents_constants.T_SPSA.L].value + 1):
                        exp_result.all_metrics[seed][agents_constants.T_SPSA.STOP_DISTRIBUTION_ATTACKER
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

            exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                         agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_START] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                         agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                         agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                         env_constants.ENV_METRICS.INTRUSION_START] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                         env_constants.ENV_METRICS.INTRUSION_LENGTH] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                         env_constants.ENV_METRICS.TIME_HORIZON] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                         env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN] = []
            exp_result.all_metrics[seed][
                agents_constants.COMMON.EVAL_PREFIX +
                env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN] = []

            exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                         agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_START] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                         agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                         agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                         env_constants.ENV_METRICS.INTRUSION_START] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                         env_constants.ENV_METRICS.INTRUSION_LENGTH] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                         env_constants.ENV_METRICS.TIME_HORIZON] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                         env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN] = []
            exp_result.all_metrics[seed][
                agents_constants.COMMON.BASELINE_PREFIX +
                env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN] = []

            for l in range(1, self.experiment_config.hparams[agents_constants.T_SPSA.L].value + 1):
                exp_result.all_metrics[seed][env_constants.ENV_METRICS.STOP + f"_{l}"] = []
                exp_result.all_metrics[seed][env_constants.ENV_METRICS.STOP + f"_running_average_{l}"] = []
                exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                             env_constants.ENV_METRICS.STOP + f"_{l}"] = []
                exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                             env_constants.ENV_METRICS.STOP + f"_running_average_{l}"] = []
                exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                             env_constants.ENV_METRICS.STOP + f"_{l}"] = []
                exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                             env_constants.ENV_METRICS.STOP + f"_running_average_{l}"] = []

        # Initialize training job
        if self.training_job is None:
            self.training_job = TrainingJobConfig(
                simulation_env_name=self.simulation_env_config.name, experiment_config=self.experiment_config,
                progress_percentage=0, pid=pid, experiment_result=exp_result,
                emulation_env_name=self.emulation_env_config.name, simulation_traces=[],
                num_cached_traces=agents_constants.COMMON.NUM_CACHED_SIMULATION_TRACES,
                log_file_path=Logger.__call__().get_log_file_path(), descr=descr)
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
        seed = self.experiment_config.random_seeds[0]
        ExperimentUtil.set_seed(seed)

        # Hyperparameters
        spsa_experiment_config = self.get_spsa_experiment_config()
        training_epochs = self.experiment_config.hparams[agents_constants.DYNASEC.TRAINING_EPOCHS].value
        sleep_time = self.experiment_config.hparams[agents_constants.DYNASEC.SLEEP_TIME].value
        intrusion_start_p = self.experiment_config.hparams[agents_constants.DYNASEC.INTRUSION_START_P].value
        emulation_traces_to_save_with_data_collection_job = self.experiment_config.hparams[
            agents_constants.DYNASEC.EMULATION_TRACES_TO_SAVE_W_DATA_COLLECTION_JOB].value
        warmup_episodes = self.experiment_config.hparams[agents_constants.DYNASEC.WARMUP_EPISODES].value
        max_steps = self.experiment_config.hparams[agents_constants.COMMON.MAX_ENV_STEPS].value
        emulation_monitor_sleep_time = self.experiment_config.hparams[
            agents_constants.DYNASEC.EMULATION_MONITOR_SLEEP_TIME].value
        replay_window_size = self.experiment_config.hparams[agents_constants.DYNASEC.REPLAY_WINDOW_SIZE].value

        # Start data collection processes
        data_collector_processes = []
        windowed_emulation_statistics = EmulationStatisticsWindowed(
            window_size=replay_window_size, emulation_name=self.emulation_executions[0].emulation_env_config.name,
            descr=descr)
        for i, execution in enumerate(self.emulation_executions):
            data_collector_process = DataCollectorProcess(
                emulation_execution=execution, attacker_sequence=self.attacker_sequence,
                defender_sequence=self.defender_sequence, worker_id=i, sleep_time=sleep_time,
                emulation_statistics_windowed=windowed_emulation_statistics,
                emulation_traces_to_save_with_data_collection_job=emulation_traces_to_save_with_data_collection_job,
                intrusion_start_p=intrusion_start_p
            )
            data_collector_process.start()
            data_collector_processes.append(data_collector_process)
            time.sleep(sleep_time / 10)

        # Start emulation monitor
        emulation_monitor_process = EmulationMonitorThread(
            exp_result=exp_result, emulation_env_config=self.emulation_executions[0].emulation_env_config,
            sleep_time_minutes=emulation_monitor_sleep_time, seed=seed)
        emulation_monitor_process.start()

        # Start stats aggregation thread
        statistic_aggregation_process = EmulationStatisticsThread(
            exp_result=exp_result, emulation_env_config=self.emulation_executions[0].emulation_env_config,
            sleep_time=sleep_time, seed=seed, data_collector_processes=data_collector_processes)
        statistic_aggregation_process.start()

        # Warmup phase
        completed_warmup_episodes = 0
        while completed_warmup_episodes < warmup_episodes:
            for i, dpc in enumerate(data_collector_processes):
                if not dpc.is_alive():
                    data_collector_processes[i] = DataCollectorProcess(
                        emulation_execution=dpc.emulation_execution, attacker_sequence=dpc.attacker_sequence,
                        defender_sequence=dpc.defender_sequence, worker_id=dpc.worker_id, sleep_time=dpc.sleep_time,
                        emulation_statistics_windowed=dpc.emulation_statistics_windowed,
                        emulation_traces_to_save_with_data_collection_job=(
                            dpc.emulation_traces_to_save_with_data_collection_job),
                        intrusion_start_p=dpc.intrusion_start_p
                    )
                    data_collector_processes[i].start()
            completed_warmup_episodes = sum(list(map(lambda x: x.completed_episodes, data_collector_processes)))
            Logger.__call__().get_logger().info(f"[DynaSec] [warmup] "
                                                f" completed episodes: "
                                                f"{completed_warmup_episodes}/{warmup_episodes}")
            time.sleep(sleep_time / 2)
        sys_id_process = SystemIdentificationProcess(
            system_identification_config=self.system_identification_config,
            emulation_statistics=windowed_emulation_statistics.emulation_statistics,
            emulation_env_config=self.emulation_executions[0].emulation_env_config, sleep_time=sleep_time,
            periodic=False)
        sys_id_process.start()
        sys_id_process.join()
        initial_system_model = sys_id_process.system_model

        policy_optimization_process = PolicyOptimizationProcess(
            system_model=initial_system_model, experiment_config=spsa_experiment_config,
            emulation_env_config=self.emulation_executions[0].emulation_env_config,
            simulation_env_config=self.simulation_env_config, periodic=False, sleep_time=sleep_time)
        policy_optimization_process.start()
        policy_optimization_process.join()
        initial_policy = list(policy_optimization_process.experiment_execution.result.policies_page_bp.values())[0]

        policy = initial_policy.copy()
        system_model = initial_system_model.copy()
        attacker_type = StaticEmulationAttackerType.EXPERT

        policies = []
        system_models = []
        policies.append(policy)
        system_models.append(system_model)

        # Start policy evaluation thread
        policy_evaluation_thread = PolicyEvaluationThread(
            exp_result=exp_result, emulation_env_config=self.emulation_executions[0].emulation_env_config,
            sleep_time=sleep_time, seed=seed, policy=policy,
            emulation_statistics_thread=statistic_aggregation_process, system_model=system_model,
            baseline_system_model=initial_system_model, max_steps=max_steps,
            experiment_config=self.experiment_config, simulation_env_config=self.simulation_env_config, env=self.env,
            baseline_policy=initial_policy.copy())
        policy_evaluation_thread.start()

        # Start system identification thread
        sys_id_process = SystemIdentificationProcess(
            system_identification_config=self.system_identification_config,
            emulation_statistics=windowed_emulation_statistics.emulation_statistics,
            emulation_env_config=self.emulation_executions[0].emulation_env_config, sleep_time=sleep_time,
            periodic=True)
        sys_id_process.system_model = initial_system_model
        Logger.__call__().get_logger().info("[DynaSec] starting system identification process")
        sys_id_process.start()

        # Start policy optimization process
        policy_optimization_process = PolicyOptimizationProcess(
            system_model=system_model, experiment_config=spsa_experiment_config,
            emulation_env_config=self.emulation_executions[0].emulation_env_config,
            simulation_env_config=self.simulation_env_config, periodic=True, sleep_time=sleep_time)
        policy_optimization_process.policy = initial_policy.copy()
        policy_optimization_process.start()

        # Parameter server
        training_epoch = 0
        while training_epoch < training_epochs:
            time.sleep(sleep_time)

            # Record metrics
            training_epoch += 1
            if policy_optimization_process.experiment_execution is not None:
                policy_evaluation_thread.exp_result = self.record_metrics(
                    exp_result=policy_evaluation_thread.exp_result, seed=seed,
                    metrics_dict=policy_optimization_process.experiment_execution.result.all_metrics)

            # Failure detection on data collector processes
            for i, dpc in enumerate(data_collector_processes):
                if not dpc.is_alive():
                    data_collector_processes[i] = DataCollectorProcess(
                        emulation_execution=dpc.emulation_execution, attacker_sequence=dpc.attacker_sequence,
                        defender_sequence=dpc.defender_sequence, worker_id=dpc.worker_id, sleep_time=dpc.sleep_time,
                        emulation_statistics_windowed=dpc.emulation_statistics_windowed,
                        emulation_traces_to_save_with_data_collection_job=(
                            dpc.emulation_traces_to_save_with_data_collection_job),
                        intrusion_start_p=dpc.intrusion_start_p
                    )
                    data_collector_processes[i].start()
            if random.random() < 0.1:
                attacker_type = random.randint(0, 2)
            policy_evaluation_thread.exp_result.all_metrics[seed][agents_constants.DYNASEC.STATIC_ATTACKER_TYPE].append(
                attacker_type)

            if training_epoch % self.experiment_config.log_every == 0 and (
                    training_epoch > 0 and len(policy_evaluation_thread.exp_result.all_metrics[seed][
                    agents_constants.COMMON.AVERAGE_RETURN]) > 0
                    and len(policy_evaluation_thread.exp_result.all_metrics[seed][
                    agents_constants.COMMON.RUNNING_AVERAGE_RETURN]) > 0
                    and len(policy_evaluation_thread.exp_result.all_metrics[seed][
                    agents_constants.COMMON.EVAL_PREFIX + agents_constants.COMMON.AVERAGE_RETURN]) > 0
                    and len(policy_evaluation_thread.exp_result.all_metrics[seed][
                    agents_constants.COMMON.EVAL_PREFIX + agents_constants.COMMON.RUNNING_AVERAGE_RETURN]) > 0
                    and len(policy_evaluation_thread.exp_result.all_metrics[seed][
                    agents_constants.COMMON.BASELINE_PREFIX + agents_constants.COMMON.AVERAGE_RETURN]) > 0
                    and len(policy_evaluation_thread.exp_result.all_metrics[seed][
                    agents_constants.COMMON.BASELINE_PREFIX + agents_constants.COMMON.RUNNING_AVERAGE_RETURN]) > 0):

                # Update emulation statistics for system identification
                sys_id_process.emulation_statistics = windowed_emulation_statistics.emulation_statistics
                system_models.append(sys_id_process.system_model)

                # Update system model for policy learning process
                policy_optimization_process.system_model = sys_id_process.system_model
                policies.append(policy_optimization_process.policy)

                # Update policy and model for evaluation
                policy_evaluation_thread.policy = policy_optimization_process.policy
                policy_evaluation_thread.system_model = sys_id_process.system_model

                # Update training job
                total_iterations = training_epochs
                iterations_done = training_epoch
                progress = round(iterations_done / total_iterations, 2)
                self.training_job.progress_percentage = progress
                self.training_job.experiment_result = policy_evaluation_thread.exp_result
                if len(self.env.get_traces()) > 0:
                    self.training_job.simulation_traces.append(self.env.get_traces()[-1])
                if len(self.training_job.simulation_traces) > self.training_job.num_cached_traces:
                    self.training_job.simulation_traces = self.training_job.simulation_traces[1:]
                if self.save_to_metastore:
                    MetastoreFacade.update_training_job(training_job=self.training_job, id=self.training_job.id)

                # Update execution
                ts = time.time()
                self.exp_execution.timestamp = ts
                self.exp_execution.result = policy_evaluation_thread.exp_result
                if self.save_to_metastore:
                    MetastoreFacade.update_experiment_execution(experiment_execution=self.exp_execution,
                                                                id=self.exp_execution.id)
                J_train = policy_evaluation_thread.exp_result.all_metrics[seed][
                    agents_constants.COMMON.AVERAGE_RETURN][-1]
                J_train_avg = policy_evaluation_thread.exp_result.all_metrics[seed][
                    agents_constants.COMMON.RUNNING_AVERAGE_RETURN][-1]
                J_eval = policy_evaluation_thread.exp_result.all_metrics[seed][
                    agents_constants.COMMON.EVAL_PREFIX + agents_constants.COMMON.AVERAGE_RETURN][-1]
                J_eval_avg = policy_evaluation_thread.exp_result.all_metrics[seed][
                    agents_constants.COMMON.EVAL_PREFIX + agents_constants.COMMON.RUNNING_AVERAGE_RETURN][-1]
                J_baseline = policy_evaluation_thread.exp_result.all_metrics[seed][
                    agents_constants.COMMON.BASELINE_PREFIX + agents_constants.COMMON.AVERAGE_RETURN][-1]
                J_baseline_avg = policy_evaluation_thread.exp_result.all_metrics[seed][
                    agents_constants.COMMON.BASELINE_PREFIX + agents_constants.COMMON.RUNNING_AVERAGE_RETURN][-1]
                Logger.__call__().get_logger().info(
                    f"[DynaSec] i: {training_epoch}, "
                    f"policy:{policy_evaluation_thread.policy.thresholds()} "
                    f"baseline policy:{policy_evaluation_thread.baseline_policy.thresholds()}"
                    f"J_train:{J_train}, "
                    f"J_train_avg_{self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value}:"
                    f"{J_train_avg}, "
                    f"J_eval:{J_eval}, "
                    f"J_eval_avg_{self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value}:"
                    f"{J_eval_avg}, "
                    f"J_baseline:{J_baseline}, "
                    f"J_baseline_avg_{self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value}:"
                    f"{J_baseline_avg}, "
                    f"progress: {round(progress*100,2)}%")
        return self.exp_execution

    def record_metrics(self, exp_result: ExperimentResult, seed: int, metrics_dict: Dict) -> ExperimentResult:
        """
        Utility function for recording the metrics of a metrics dict and importing them into the experiment result

        :param exp_result: the experiment result to update
        :param seed: the random seed of the experiment
        :param metrics_dict: the metrics dict with the new metrics
        :return: the updated experiment result
        """
        exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN].append(
            metrics_dict[seed][
                agents_constants.COMMON.AVERAGE_RETURN][-1])
        exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN].append(
            metrics_dict[seed][
                agents_constants.COMMON.RUNNING_AVERAGE_RETURN][-1])
        exp_result.all_metrics[seed][agents_constants.T_SPSA.THETAS].append(
            metrics_dict[seed][
                agents_constants.T_SPSA.THETAS][-1])
        exp_result.all_metrics[seed][agents_constants.T_SPSA.THRESHOLDS].append(
            metrics_dict[seed][
                agents_constants.T_SPSA.THRESHOLDS][-1])
        exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_LENGTH].append(
            metrics_dict[seed][
                env_constants.ENV_METRICS.INTRUSION_LENGTH][-1])
        exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH].append(
            metrics_dict[seed][
                agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH][-1])
        exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_START].append(
            metrics_dict[seed][
                env_constants.ENV_METRICS.INTRUSION_START][-1])
        exp_result.all_metrics[seed][env_constants.ENV_METRICS.TIME_HORIZON].append(
            metrics_dict[seed][
                env_constants.ENV_METRICS.TIME_HORIZON][-1])
        exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON].append(
            metrics_dict[seed][
                agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON][-1])
        for l in range(1, self.experiment_config.hparams[agents_constants.T_SPSA.L].value + 1):
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.STOP + f"_{l}"].append(
                metrics_dict[seed][
                    env_constants.ENV_METRICS.STOP + f"_{l}"][-1])
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.STOP + f"_running_average_{l}"].append(
                metrics_dict[seed][
                    env_constants.ENV_METRICS.STOP + f"_running_average_{l}"][-1])
        exp_result.all_metrics[seed][env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN].append(
            metrics_dict[seed][
                env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN][-1])
        exp_result.all_metrics[seed][
            env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN].append(
            metrics_dict[seed][
                env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN][-1])
        return exp_result

    @staticmethod
    def get_Z_from_system_model(system_model: GaussianMixtureSystemModel, sample_space: List) -> Tuple[np.ndarray,
                                                                                                       float, float]:
        intrusion_dist = np.zeros(len(sample_space))
        no_intrusion_dist = np.zeros(len(sample_space))
        terminal_dist = np.zeros(len(sample_space))
        terminal_dist[-1] = 1
        for metric_conds in system_model.conditional_metric_distributions:
            for metric_cond in metric_conds:
                if metric_cond.conditional_name == "intrusion" \
                        and metric_cond.metric_name == "warning_alerts":
                    intrusion_dist[0] = sum(metric_cond.generate_distributions_for_samples(
                        samples=list(range(-len(sample_space), 1))))
                    intrusion_dist[1:] = metric_cond.generate_distributions_for_samples(samples=sample_space[1:])
                if metric_cond.conditional_name == "no_intrusion" \
                        and metric_cond.metric_name == "warning_alerts":
                    no_intrusion_dist[0] = sum(metric_cond.generate_distributions_for_samples(
                        samples=list(range(-len(sample_space), 1))))
                    no_intrusion_dist[1:] = metric_cond.generate_distributions_for_samples(samples=sample_space[1:])
        intrusion_dist = list(np.array(intrusion_dist) * (1 / sum(intrusion_dist)))
        no_intrusion_dist = list(np.array(no_intrusion_dist) * (1 / sum(no_intrusion_dist)))
        int_mean = DynaSecAgent.mean(intrusion_dist)
        no_int_mean = DynaSecAgent.mean(no_intrusion_dist)
        Z = np.array(
            [
                [
                    [
                        no_intrusion_dist,
                        intrusion_dist,
                        terminal_dist
                    ],
                    [
                        no_intrusion_dist,
                        intrusion_dist,
                        terminal_dist
                    ],
                ],
                [
                    [
                        no_intrusion_dist,
                        intrusion_dist,
                        terminal_dist
                    ],
                    [
                        no_intrusion_dist,
                        intrusion_dist,
                        terminal_dist
                    ],
                ]
            ]
        )
        return Z, int_mean, no_int_mean

    @staticmethod
    def mean(prob_vector):
        m = 0
        for i in range(len(prob_vector)):
            m += prob_vector[i] * i
        return m

    def hparam_names(self) -> List[str]:
        """
        :return: a list with the hyperparameter names
        """
        return [agents_constants.T_SPSA.a, agents_constants.T_SPSA.c, agents_constants.T_SPSA.LAMBDA,
                agents_constants.T_SPSA.A, agents_constants.T_SPSA.EPSILON, agents_constants.T_SPSA.N,
                agents_constants.T_SPSA.L, agents_constants.T_SPSA.THETA1, agents_constants.COMMON.EVAL_BATCH_SIZE,
                agents_constants.T_SPSA.GRADIENT_BATCH_SIZE, agents_constants.COMMON.CONFIDENCE_INTERVAL,
                agents_constants.COMMON.RUNNING_AVERAGE,
                system_identification_constants.SYSTEM_IDENTIFICATION.CONDITIONAL_DISTRIBUTIONS,
                system_identification_constants.EXPECTATION_MAXIMIZATION.NUM_MIXTURES_PER_CONDITIONAL,
                agents_constants.DYNASEC.TRAINING_EPOCHS, agents_constants.DYNASEC.SLEEP_TIME,
                agents_constants.DYNASEC.INTRUSION_START_P,
                agents_constants.DYNASEC.EMULATION_TRACES_TO_SAVE_W_DATA_COLLECTION_JOB,
                agents_constants.DYNASEC.EMULATION_MONITOR_SLEEP_TIME,
                agents_constants.DYNASEC.REPLAY_WINDOW_SIZE
                ]
