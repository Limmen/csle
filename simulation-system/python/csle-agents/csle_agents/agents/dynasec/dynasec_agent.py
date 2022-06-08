from typing import List, Optional, Dict
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
from csle_common.util.read_emulation_statistics import ReadEmulationStatistics
from csle_common.dao.emulation_config.static_emulation_attacker_type import StaticEmulationAttackerType


class DataCollectorProcess(threading.Thread):
    """
    Process that interacts with an emulation execution to generate data
    """

    def __init__(self, emulation_execution: EmulationExecution,
                 attacker_sequence: List[EmulationAttackerAction],
                 defender_sequence: List[EmulationDefenderAction],
                 worker_id: int,
                 sleep_time : int = 30, emulation_statistics: EmulationStatistics = None,
                 emulation_traces_to_save_with_data_collection_job : int = 1,
                 intrusion_start_p: float = 0.1) -> None:
        """
        Initializes the thread

        :param emulation_execution:  the emulation execution to use for data collection
        :param attacker_sequence: the attacker sequence to use for emulating the attacker
        :param defender_sequence: the defender sequence to use for emulating the defender
        :param worker_id: the worker id
        :param sleep_time: the sleep time between actions
        :param emulation_statistics: the emulation statistics object
        :param emulation_traces_to_save_with_data_collection_job: the number of traces to save with the
                                                                  data collection job
        :param intrusion_start_p: the p parameter in the geometric distribution of the intrusion start time.
        """
        threading.Thread.__init__(self)
        self.running =True
        self.emulation_execution = emulation_execution
        self.attacker_sequence = attacker_sequence
        self.defender_sequence = defender_sequence
        self.sleep_time = sleep_time
        self.worker_id = worker_id
        self.emulation_statistics = emulation_statistics
        self.emulation_traces_to_save_with_data_collection_job = emulation_traces_to_save_with_data_collection_job
        self.intrusion_start_p = intrusion_start_p
        self.pid = os.getpid()
        self.data_collection_job = DataCollectionJobConfig(
            emulation_env_name=self.emulation_execution.emulation_env_config.name,
            num_collected_steps=0, progress_percentage=0.0,
            attacker_sequence=attacker_sequence, defender_sequence=defender_sequence,
            pid=self.pid, descr=f"Data collection process in DynaSec with id: {self.worker_id}",
            repeat_times=10000, emulation_statistic_id=self.emulation_statistics.id, traces=[],
            num_sequences_completed=0, save_emulation_traces_every=1000000,
            num_cached_traces=emulation_traces_to_save_with_data_collection_job,
            log_file_path=Logger.__call__().get_log_file_path())
        self.job_id = MetastoreFacade.save_data_collection_job(
            data_collection_job=self.data_collection_job)
        self.data_collection_job.id = self.job_id
        self.emulation_traces = []
        self.statistics_id = self.emulation_statistics.id

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
            assert  len(full_defender_sequence) == len(full_attacker_sequence)
            Logger.__call__().get_logger().info(f"Worker {self.worker_id} in DynaSec "
                        f"starting execution of static action sequences, iteration:{i}, T:{T}, "
                                                f"I_t:{intrusion_start_time}")
            sys.stdout.flush()
            s.reset()
            emulation_trace = EmulationTrace(initial_attacker_observation_state=s.attacker_obs_state,
                                             initial_defender_observation_state=s.defender_obs_state,
                                             emulation_name=self.emulation_execution.emulation_env_config.name)
            s.defender_obs_state.reset_metric_lists()
            time.sleep(self.sleep_time)
            s.defender_obs_state.average_metric_lists()
            self.emulation_statistics.update_initial_statistics(s=s)
            for t in range(T):
                old_state = s.copy()
                a1 = full_defender_sequence[t]
                a2 = full_attacker_sequence[t]
                Logger.__call__().get_logger().info(f"Worker {self.worker_id}, t:{t}, a1: {a1}, a2: {a2}")
                s.defender_obs_state.reset_metric_lists()
                emulation_trace, s = Emulator.run_actions(
                    emulation_env_config=self.emulation_execution.emulation_env_config,
                    attacker_action=a2, defender_action=a1,
                    sleep_time=self.sleep_time, trace=emulation_trace, s=s)
                s.defender_obs_state.average_metric_lists()
                self.emulation_statistics = MetastoreFacade.get_emulation_statistic(self.statistics_id)
                self.emulation_statistics.update_delta_statistics(s=old_state, s_prime=s, a1=a1, a2=a2)
                MetastoreFacade.update_emulation_statistic(emulation_statistics=self.emulation_statistics,
                                                           id=self.statistics_id)
                total_steps = 10000
                collected_steps += 1
                self.data_collection_job.num_collected_steps=collected_steps
                self.data_collection_job.progress_percentage = (round(collected_steps / total_steps, 2))
                self.data_collection_job.num_sequences_completed = i
                Logger.__call__().get_logger().debug(
                    f"Worker {self.worker_id}, "
                    f"job updated, steps collected: {self.data_collection_job.num_collected_steps}, "
                    f"progress: {self.data_collection_job.progress_percentage}, "
                    f"sequences completed: {i}")
                sys.stdout.flush()
                MetastoreFacade.update_data_collection_job(data_collection_job=self.data_collection_job,
                                                           id=self.data_collection_job.id)

            self.emulation_traces = self.emulation_traces + [emulation_trace]
            if len(self.emulation_traces) > self.data_collection_job.num_cached_traces:
                self.data_collection_job.traces = \
                    self.emulation_traces[-self.data_collection_job.num_cached_traces:]
            else:
                self.data_collection_job.traces = self.emulation_traces
            i+=1


class SystemIdentificationProcess(threading.Thread):
    """
    Process that uses collected data from data collectors to estimate a system model of the data
    """

    def __init__(self, system_identification_config: SystemIdentificationConfig,
                 emulation_statistics: EmulationStatistics, emulation_env_config: EmulationEnvConfig) -> None:
        """
        Initializes the thread

        :param system_identification_config: the configuration of the system identification algorithm
        :param emulation_statistics: the emulation statistics to use for system identification
        :param emulation_env_config: the emulation environment configuration
        """
        self.system_identification_config = system_identification_config
        self.emulation_env_config = emulation_env_config
        self.emulation_statistics = emulation_statistics
        self.algorithm = ExpectationMaximizationAlgorithm(
            emulation_env_config=self.emulation_env_config, emulation_statistics=self.emulation_statistics,
            system_identification_config=self.system_identification_config)
        threading.Thread.__init__(self)
        self.running =True
        self.system_model = None

    def run(self) -> None:
        """
        Runs the thread

        :return: None
        """
        Logger.__call__().get_logger().info(f"[DynaSec] starting system identification algorithm")
        self.system_model = self.algorithm.fit()
        Logger.__call__().get_logger().info(f"[DynaSec] system identification algorithm complete")
        MetastoreFacade.save_gaussian_mixture_system_model(gaussian_mixture_system_model=self.system_model)
        self.running = False


class PolicyOptimizationProcess(threading.Thread):
    """
    Process that optimizes a policy through reinforcement learning and interaction with a system model.
    """

    def __init__(self, system_model: GaussianMixtureSystemModel, experiment_config: ExperimentConfig,
                 emulation_env_config: EmulationEnvConfig, simulation_env_config: SimulationEnvConfig) -> None:
        """
        Initializes the thread

        :param system_model: the system model to use for learning
        :param experiment_config: the experiment configuration
        :param emulation_env_config: the configuration of the emulation environment
        :param simulation_env_config: the configuration of the simulation environment
        """
        threading.Thread.__init__(self)
        self.system_model = system_model
        self.emulation_env_config = emulation_env_config
        self.experiment_config = experiment_config
        self.simulation_env_config = simulation_env_config
        sample_space = self.simulation_env_config.simulation_env_input_config.stopping_game_config.O.tolist()
        self.simulation_env_config.simulation_env_input_config.stopping_game_config.Z = \
            DynaSecAgent.get_Z_from_system_model(system_model=system_model, sample_space=sample_space)
        self.agent = TSPSAAgent(emulation_env_config=self.emulation_env_config,
                                simulation_env_config=simulation_env_config, experiment_config=self.experiment_config)
        self.experiment_execution = None
        self.running =True

    def run(self) -> None:
        """
        Runs the thread

        :return: None
        """
        self.experiment_execution = self.agent.train()

        MetastoreFacade.save_experiment_execution(self.experiment_execution)
        for policy in self.experiment_execution.result.policies.values():
            MetastoreFacade.save_multi_threshold_stopping_policy(multi_threshold_stopping_policy=policy)


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
        self.running =True
        self.seed = seed

    def run(self) -> None:
        """
        Runs the thread

        :return: None
        """
        Logger.__call__().get_logger().info(f"[DynaSec] starting emulation monitor thread")
        while self.running:
            time.sleep(self.sleep_time_minutes)
            metrics = ReadEmulationStatistics.read_all(emulation_env_config=self.emulation_env_config,
                                             time_window_minutes=self.sleep_time_minutes)
            if len(metrics.client_metrics) > 0:
                num_clients = metrics.client_metrics[0].num_clients
                self.exp_result.all_metrics[self.seed][agents_constants.DYNASEC.NUM_CLIENTS].append(num_clients)


class DynaSecAgent(BaseAgent):
    """
    DynaSec
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 emulation_executions: List[EmulationExecution],
                 attacker_sequence: List[EmulationAttackerAction], defender_sequence: List[EmulationDefenderAction],
                 system_identification_config: SystemIdentificationConfig,
                 experiment_config: ExperimentConfig, env: Optional[gym.Env] = None,
                 training_job: Optional[TrainingJobConfig] = None, save_to_metastore : bool = True):
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
        hparams= {
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


        for l in range(1,self.experiment_config.hparams[agents_constants.T_SPSA.L].value+1):
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
                for l in range(1,self.experiment_config.hparams[agents_constants.T_SPSA.L].value+1):
                    exp_result.all_metrics[seed][agents_constants.T_SPSA.STOP_DISTRIBUTION_DEFENDER + f"_l={l}"] = []
            else:
                for s in self.simulation_env_config.state_space_config.states:
                    for l in range(1,self.experiment_config.hparams[agents_constants.T_SPSA.L].value+1):
                        exp_result.all_metrics[seed][agents_constants.T_SPSA.STOP_DISTRIBUTION_ATTACKER
                                                     + f"_l={l}_s={s.id}"] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_START] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH] = []
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_START] = []
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_LENGTH] = []
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.TIME_HORIZON] = []
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN] = []
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN] = []

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
            exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
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
            exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                         env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN] = []

            for l in range(1,self.experiment_config.hparams[agents_constants.T_SPSA.L].value+1):
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
        self.exp_execution = ExperimentExecution(result=exp_result, config=self.experiment_config, timestamp=ts,
                                            emulation_name=emulation_name, simulation_name=simulation_name,
                                            descr=descr, log_file_path=self.training_job.log_file_path)
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
        episodes_between_model_updates = self.experiment_config.hparams[
            agents_constants.DYNASEC.EPISODES_BETWEEN_MODEL_UPDATES].value
        sleep_time = self.experiment_config.hparams[agents_constants.DYNASEC.SLEEP_TIME].value
        intrusion_start_p = self.experiment_config.hparams[agents_constants.DYNASEC.INTRUSION_START_P].value
        emulation_traces_to_save_with_data_collection_job = self.experiment_config.hparams[
            agents_constants.DYNASEC.EMULATION_TRACES_TO_SAVE_W_DATA_COLLECTION_JOB].value
        warmup_episodes = self.experiment_config.hparams[agents_constants.DYNASEC.WARMUP_EPISODES].value
        max_steps = self.experiment_config.hparams[agents_constants.COMMON.MAX_ENV_STEPS].value
        emulation_monitor_sleep_time = self.experiment_config.hparams[
            agents_constants.DYNASEC.EMULATION_MONITOR_SLEEP_TIME].value

        # Start data collection processes
        data_collector_processes = []
        emulation_statistics = EmulationStatistics(
            emulation_name=self.emulation_executions[0].emulation_env_config.name, descr=descr)
        statistics_id = MetastoreFacade.save_emulation_statistic(emulation_statistics=emulation_statistics)
        emulation_statistics.id = statistics_id
        for i, execution in enumerate(self.emulation_executions):
            data_collector_process = DataCollectorProcess(
                emulation_execution=execution, attacker_sequence=self.attacker_sequence,
                defender_sequence=self.defender_sequence, worker_id=i, sleep_time=sleep_time,
                emulation_statistics=emulation_statistics,
                emulation_traces_to_save_with_data_collection_job=emulation_traces_to_save_with_data_collection_job,
                intrusion_start_p=intrusion_start_p
            )
            data_collector_process.start()
            data_collector_processes.append(data_collector_process)
            time.sleep(sleep_time)

        # Start emulation monitor
        emulation_monitor_process = EmulationMonitorThread(
            exp_result=exp_result,  emulation_env_config=self.emulation_executions[0].emulation_env_config,
            sleep_time_minutes=emulation_monitor_sleep_time, seed=seed)
        emulation_monitor_process.start()

        # Warmup phase
        completed_warmup_episodes = 0
        while completed_warmup_episodes < warmup_episodes:
            completed_warmup_episodes = sum(list(map(lambda x: len(x.emulation_traces), data_collector_processes)))
            Logger.__call__().get_logger().info(f"[DynaSec] [warmup] "
                                                f" collected traces: "
                                                f"{completed_warmup_episodes}/{warmup_episodes}")
            time.sleep(sleep_time)
        emulation_statistics = MetastoreFacade.get_emulation_statistic(id=statistics_id)
        new_emulation_statistics = EmulationStatistics(
            emulation_name=self.emulation_executions[0].emulation_env_config.name, descr=descr)
        statistics_id = MetastoreFacade.save_emulation_statistic(emulation_statistics=new_emulation_statistics)
        new_emulation_statistics.id = statistics_id
        for data_collector_process in data_collector_processes:
            data_collector_process.emulation_statistics = new_emulation_statistics
            data_collector_process.statistics_id = statistics_id
            data_collector_process.emulation_traces = []

        sys_id_process = SystemIdentificationProcess(
            system_identification_config=self.system_identification_config,
            emulation_statistics=emulation_statistics,
            emulation_env_config=self.emulation_executions[0].emulation_env_config)
        Logger.__call__().get_logger().info(f"[DynaSec] [warmup] starting system identification process")
        sys_id_process.start()
        sys_id_process.join()
        initial_system_model = sys_id_process.system_model
        Logger.__call__().get_logger().info(f"[DynaSec] [warmup] system identification process completed")

        policy_optimization_process = PolicyOptimizationProcess(
            system_model=initial_system_model,  experiment_config=spsa_experiment_config,
            emulation_env_config=self.emulation_executions[0].emulation_env_config,
            simulation_env_config=self.simulation_env_config)
        Logger.__call__().get_logger().info(f"[DynaSec] [warmup] starting policy optimization process")
        policy_optimization_process.start()
        policy_optimization_process.join()
        Logger.__call__().get_logger().info(f"[DynaSec] [warmup] policy optimization process completed")
        initial_policy = list(policy_optimization_process.experiment_execution.result.policies.values())[0]
        self.record_metrics(
            exp_result=exp_result, seed=seed,
            metrics_dict=policy_optimization_process.experiment_execution.result.all_metrics)
        baseline = (initial_system_model, initial_policy)

        policy = initial_policy.copy()
        system_model = initial_system_model.copy()
        attacker_type = StaticEmulationAttackerType.EXPERT

        # Training
        training_epoch = 0
        while training_epoch < training_epochs:
            new_traces = []
            exp_result.all_metrics[seed][agents_constants.DYNASEC.STATIC_ATTACKER_TYPE].append(attacker_type)
            while len(new_traces) < episodes_between_model_updates:
                n_traces = []
                for dcp in data_collector_processes:
                    if len(dcp.emulation_traces) > 0:
                        n_traces.append(dcp.emulation_traces[0])
                        dcp.emulation_traces = []
                if len(n_traces) > 0:
                    Logger.__call__().get_logger().info(f"[DynaSec] eval "
                                                        f"{len(new_traces)}/{episodes_between_model_updates}")
                    avg_metrics = self.eval_traces(traces=n_traces, defender_policy=policy, max_steps=max_steps,
                                                   system_model=system_model)
                    avg_metrics_seed = {}
                    avg_metrics_seed[seed] = avg_metrics
                    print(avg_metrics_seed[seed])
                    print(avg_metrics)
                    self.record_metrics(
                        exp_result=exp_result, seed=seed,
                        metrics_dict=avg_metrics_seed, eval=True, baseline=False)
                    avg_metrics = self.eval_traces(traces=n_traces, defender_policy=initial_policy, max_steps=max_steps,
                                                   system_model=initial_system_model)
                    avg_metrics_seed = {}
                    avg_metrics_seed[seed] = avg_metrics
                    self.record_metrics(
                        exp_result=exp_result, seed=seed,
                        metrics_dict=avg_metrics_seed, baseline=True, eval=False)
                new_traces = new_traces + n_traces
                Logger.__call__().get_logger().info(f"[DynaSec] waiting to collect enough traces. "
                                                    f"Number of new traces: "
                                                    f"{len(new_traces)}/{episodes_between_model_updates}")
                time.sleep(sleep_time)
            emulation_statistics = MetastoreFacade.get_emulation_statistic(id=statistics_id)
            new_emulation_statistics = EmulationStatistics(
                emulation_name=self.emulation_executions[0].emulation_env_config.name, descr=descr)
            statistics_id = MetastoreFacade.save_emulation_statistic(emulation_statistics=new_emulation_statistics)
            new_emulation_statistics.id = statistics_id
            evaluation_traces = []
            for data_collector_process in data_collector_processes:
                data_collector_process.emulation_statistics = new_emulation_statistics
                data_collector_process.statistics_id = statistics_id
                evaluation_traces = evaluation_traces + data_collector_process.emulation_traces
                data_collector_process.emulation_traces = []

            sys_id_process = SystemIdentificationProcess(
                system_identification_config=self.system_identification_config,
                emulation_statistics=emulation_statistics,
                emulation_env_config=self.emulation_executions[0].emulation_env_config)
            Logger.__call__().get_logger().info(f"[DynaSec] starting system identification process")
            sys_id_process.start()
            sys_id_process.join()
            system_model = sys_id_process.system_model
            Logger.__call__().get_logger().info(f"[DynaSec] system identification process completed")
            policy_optimization_process = PolicyOptimizationProcess(
                system_model=system_model,  experiment_config=spsa_experiment_config,
                emulation_env_config=self.emulation_executions[0].emulation_env_config,
                simulation_env_config=self.simulation_env_config)
            Logger.__call__().get_logger().info(f"[DynaSec] starting policy optimization process")
            policy_optimization_process.start()
            policy_optimization_process.join()
            policy = list(policy_optimization_process.experiment_execution.result.policies.values())[0]
            Logger.__call__().get_logger().info(f"[DynaSec] policy optimization process completed")
            training_epoch += 1

            # Record metrics
            self.record_metrics(
                exp_result=exp_result, seed=seed,
                metrics_dict=policy_optimization_process.experiment_execution.result.all_metrics)
            if training_epoch % self.experiment_config.log_every == 0 and training_epoch > 0:
                # Update training job
                total_iterations = training_epochs
                iterations_done = training_epoch
                progress = round(iterations_done / total_iterations, 2)
                self.training_job.progress_percentage = progress
                self.training_job.experiment_result = exp_result
                if len(self.env.get_traces()) > 0:
                    self.training_job.simulation_traces.append(self.env.get_traces()[-1])
                if len(self.training_job.simulation_traces) > self.training_job.num_cached_traces:
                    self.training_job.simulation_traces = self.training_job.simulation_traces[1:]
                if self.save_to_metastore:
                    MetastoreFacade.update_training_job(training_job=self.training_job, id=self.training_job.id)

                # Update execution
                ts = time.time()
                self.exp_execution.timestamp = ts
                self.exp_execution.result = exp_result
                if self.save_to_metastore:
                    MetastoreFacade.update_experiment_execution(experiment_execution=self.exp_execution,
                                                                id=self.exp_execution.id)

                Logger.__call__().get_logger().info(
                    f"[DynaSec] i: {training_epoch}, "
                    f"J:{exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN][-1]}, "
                    f"J_avg_{self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value}:"
                    f"{exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN][-1]}, "
                    f"opt_J:{exp_result.all_metrics[seed][env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN][-1]}, "
                    f"int_len:{exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_LENGTH][-1]}, "
                    f"sigmoid(theta):{exp_result.all_metrics[seed][agents_constants.T_SPSA.THRESHOLDS][-1]}, "
                    f"progress: {round(progress*100,2)}%")
        return self.exp_execution

    def eval_traces(self, traces: List[EmulationTrace], defender_policy: Policy, max_steps : int,
                    system_model: GaussianMixtureSystemModel):
        sample_space = self.simulation_env_config.simulation_env_input_config.stopping_game_config.O.tolist()
        old_Z = self.simulation_env_config.simulation_env_input_config.stopping_game_config.Z.copy()
        self.simulation_env_config.simulation_env_input_config.stopping_game_config.Z = \
            DynaSecAgent.get_Z_from_system_model(system_model=system_model, sample_space=sample_space)
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

    def record_metrics(self, exp_result :ExperimentResult, seed: int,
                       metrics_dict: Dict,
                       eval: bool = False, baseline: bool = False):
        if not eval and not baseline:
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
            for l in range(1,self.experiment_config.hparams[agents_constants.T_SPSA.L].value+1):
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
        elif not eval and baseline:
            exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                         agents_constants.COMMON.AVERAGE_RETURN].append(
                metrics_dict[seed][
                    agents_constants.COMMON.AVERAGE_RETURN][-1])
            exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                         agents_constants.COMMON.RUNNING_AVERAGE_RETURN].append(
                metrics_dict[seed][
                    agents_constants.COMMON.RUNNING_AVERAGE_RETURN][-1])
            exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                         env_constants.ENV_METRICS.INTRUSION_LENGTH].append(
                metrics_dict[seed][
                    env_constants.ENV_METRICS.INTRUSION_LENGTH][-1])
            exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                         agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH].append(
                metrics_dict[seed][
                    agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH][-1])
            exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                         env_constants.ENV_METRICS.INTRUSION_START].append(
                metrics_dict[seed][
                    env_constants.ENV_METRICS.INTRUSION_START][-1])
            exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                         env_constants.ENV_METRICS.TIME_HORIZON].append(
                metrics_dict[seed][
                    env_constants.ENV_METRICS.TIME_HORIZON][-1])
            exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                         agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON].append(
                metrics_dict[seed][
                    agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON][-1])
            for l in range(1,self.experiment_config.hparams[agents_constants.T_SPSA.L].value+1):
                exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                             env_constants.ENV_METRICS.STOP + f"_{l}"].append(
                    metrics_dict[seed][
                        env_constants.ENV_METRICS.STOP + f"_{l}"][-1])
                exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                             env_constants.ENV_METRICS.STOP + f"_running_average_{l}"].append(
                    metrics_dict[seed][
                        env_constants.ENV_METRICS.STOP + f"_running_average_{l}"][-1])
            exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                         env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN].append(
                metrics_dict[seed][
                    env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN][-1])
            exp_result.all_metrics[seed][
                agents_constants.COMMON.BASELINE_PREFIX +
                env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN].append(
                metrics_dict[seed][
                    env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN][-1])
        else:
            exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                         agents_constants.COMMON.AVERAGE_RETURN].append(
                metrics_dict[seed][
                    agents_constants.COMMON.AVERAGE_RETURN][-1])
            exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                         agents_constants.COMMON.RUNNING_AVERAGE_RETURN].append(
                metrics_dict[seed][
                    agents_constants.COMMON.RUNNING_AVERAGE_RETURN][-1])
            exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                         env_constants.ENV_METRICS.INTRUSION_LENGTH].append(
                metrics_dict[seed][
                    env_constants.ENV_METRICS.INTRUSION_LENGTH][-1])
            exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                         agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH].append(
                metrics_dict[seed][
                    agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH][-1])
            exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                         env_constants.ENV_METRICS.INTRUSION_START].append(
                metrics_dict[seed][
                    env_constants.ENV_METRICS.INTRUSION_START][-1])
            exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                         env_constants.ENV_METRICS.TIME_HORIZON].append(
                metrics_dict[seed][
                    env_constants.ENV_METRICS.TIME_HORIZON][-1])
            exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                         agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON].append(
                metrics_dict[seed][
                    agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON][-1])
            for l in range(1,self.experiment_config.hparams[agents_constants.T_SPSA.L].value+1):
                exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                             env_constants.ENV_METRICS.STOP + f"_{l}"].append(
                    metrics_dict[seed][
                        env_constants.ENV_METRICS.STOP + f"_{l}"][-1])
                exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                             env_constants.ENV_METRICS.STOP + f"_running_average_{l}"].append(
                    metrics_dict[seed][
                        env_constants.ENV_METRICS.STOP + f"_running_average_{l}"][-1])
            exp_result.all_metrics[seed][agents_constants.COMMON.EVAL_PREFIX +
                                         env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN].append(
                metrics_dict[seed][
                    env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN][-1])
            exp_result.all_metrics[seed][
                agents_constants.COMMON.EVAL_PREFIX +
                env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN].append(
                metrics_dict[seed][
                    env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN][-1])
        return exp_result

    @staticmethod
    def get_Z_from_system_model(system_model: GaussianMixtureSystemModel, sample_space: List) -> np.ndarray:
        intrusion_dist = np.zeros(len(sample_space))
        no_intrusion_dist = np.zeros(len(sample_space))
        terminal_dist = np.zeros(len(sample_space))
        terminal_dist[-1] = 1
        for metric_conds in system_model.conditional_metric_distributions:
            for metric_cond in metric_conds:
                if metric_cond.conditional_name == "intrusion" \
                        and metric_cond.metric_name == "alerts_weighted_by_priority":
                    intrusion_dist[0] = sum(metric_cond.generate_distributions_for_samples(
                        samples=list(range(-len(sample_space), 1))))
                    intrusion_dist[1:] = metric_cond.generate_distributions_for_samples(samples=sample_space[1:])
                if metric_cond.conditional_name == "no_intrusion" \
                        and metric_cond.metric_name == "alerts_weighted_by_priority":
                    no_intrusion_dist[0] = sum(metric_cond.generate_distributions_for_samples(
                        samples=list(range(-len(sample_space), 1))))
                    no_intrusion_dist[1:] = metric_cond.generate_distributions_for_samples(samples=sample_space[1:])
        intrusion_dist = list(np.array(intrusion_dist)*(1/sum(intrusion_dist)))
        no_intrusion_dist = list(np.array(no_intrusion_dist)*(1/sum(no_intrusion_dist)))
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
        return Z

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
                agents_constants.DYNASEC.WARMUP_EPISODES, agents_constants.DYNASEC.EPISODES_BETWEEN_MODEL_UPDATES,
                agents_constants.DYNASEC.TRAINING_EPOCHS, agents_constants.DYNASEC.SLEEP_TIME,
                agents_constants.DYNASEC.INTRUSION_START_P,
                agents_constants.DYNASEC.EMULATION_TRACES_TO_SAVE_W_DATA_COLLECTION_JOB,
                agents_constants.DYNASEC.EMULATION_MONITOR_SLEEP_TIME
                ]
