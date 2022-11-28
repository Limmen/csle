from typing import List, Tuple, Optional
import time
import os
import sys
import numpy as np
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.util.env_dynamics_util import EnvDynamicsUtil
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.logging.log import Logger
from csle_attacker.attacker import Attacker
from csle_defender.defender import Defender
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
from csle_common.dao.jobs.data_collection_job_config import DataCollectionJobConfig
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_stopping_actions \
    import EmulationAttackerStoppingActions
from csle_common.dao.emulation_action.defender.emulation_defender_stopping_actions \
    import EmulationDefenderStoppingActions


class Emulator:
    """
    Class for running episodes in the emulation system
    """

    @staticmethod
    def run_action_sequences(
            emulation_env_config: EmulationEnvConfig, attacker_sequence: List[EmulationAttackerAction],
            defender_sequence: List[EmulationDefenderAction],
            repeat_times: int = 1, sleep_time: int = 1, save_dir: str = None,
            emulation_statistics: EmulationStatistics = None, descr: str = "", save: bool = True,
            data_collection_job: Optional[DataCollectionJobConfig] = None,
            save_emulation_traces_every: int = 10,
            emulation_traces_to_save_with_data_collection_job: int = 3,
            intrusion_start_p: float = 0.1, intrusion_continue: float = 0.3) -> None:
        """
        Runs an attacker and defender sequence in the emulation <repeat_times> times

        :param emulation_env_config: the configuration of the emulation
        :param attacker_sequence: the sequence of attacker actions
        :param defender_sequence: the sequenceo of defender actions
        :param repeat_times: the number of times to repeat the sequences
        :param sleep_time: the number of seconds to sleep between time-steps
        :param save_dir: the directory to save the collected traces
        :param emulation_statistics: the emulation statistics to update
        :param descr: descr of the execution
        :param save: boolean parameter indicating whether traces and statistics should be saved or not
        :param data_collection_job: the system identification job configuration
        :param save_emulation_traces_every: how frequently to save emulation traces
        :param emulation_traces_to_save_with_data_collection_job: num traces to save with the job
        :param intrusion_start_p: the p parameter for the geometric distribution that determines
                                  when an intrusion starts
        :param intrusion_continue: the p parameter for the geometric distribution that determines
                                   when an intrusion continues
        :return: None
        """
        logger = Logger.__call__().get_logger()

        # Setup save dir
        if save_dir is None:
            save_dir = ExperimentUtil.default_output_dir() + "/results"
        assert len(attacker_sequence) == len(defender_sequence)

        # Setup emulation statistic
        if emulation_statistics is None:
            emulation_statistics = EmulationStatistics(emulation_name=emulation_env_config.name, descr=descr)
        if emulation_statistics.id == -1 or emulation_statistics.id is None and save:
            statistics_id = MetastoreFacade.save_emulation_statistic(emulation_statistics=emulation_statistics)
        else:
            statistics_id = -1
            if emulation_statistics is not None:
                statistics_id = emulation_statistics.id

        # Setup data collection job
        pid = os.getpid()
        if data_collection_job is None:
            data_collection_job = DataCollectionJobConfig(
                emulation_env_name=emulation_env_config.name, num_collected_steps=0, progress_percentage=0.0,
                attacker_sequence=attacker_sequence, defender_sequence=defender_sequence,
                pid=pid, descr=descr, repeat_times=repeat_times, emulation_statistic_id=statistics_id, traces=[],
                num_sequences_completed=0, save_emulation_traces_every=save_emulation_traces_every,
                num_cached_traces=emulation_traces_to_save_with_data_collection_job,
                log_file_path=Logger.__call__().get_log_file_path())
            job_id = MetastoreFacade.save_data_collection_job(
                data_collection_job=data_collection_job)
            data_collection_job.id = job_id
        else:
            data_collection_job.pid = pid
            data_collection_job.num_collected_steps = 0
            data_collection_job.progress_percentage = 0.0
            data_collection_job.num_sequences_completed = 0
            data_collection_job.traces = []
            data_collection_job.log_file_path = Logger.__call__().get_log_file_path()
            MetastoreFacade.update_data_collection_job(data_collection_job=data_collection_job,
                                                       id=data_collection_job.id)

        # Start the collection
        s = EmulationEnvState(emulation_env_config=emulation_env_config)
        s.initialize_defender_machines()
        emulation_traces = []
        collected_steps = 0
        for i in range(repeat_times):
            intrusion_start_time = np.random.geometric(p=intrusion_start_p, size=1)[0]
            attacker_wait_seq = [EmulationAttackerStoppingActions.CONTINUE(index=-1)] * intrusion_start_time
            defender_wait_seq = [EmulationDefenderStoppingActions.CONTINUE(index=-1)] * intrusion_start_time
            full_attacker_sequence = attacker_wait_seq
            full_defender_sequence = defender_wait_seq
            for i in range(len(attacker_sequence)):
                num_wait_steps = np.random.geometric(p=intrusion_continue, size=1)[0] - 1
                wait_steps = [EmulationAttackerStoppingActions.CONTINUE(index=-1)] * num_wait_steps
                full_attacker_sequence = full_attacker_sequence + wait_steps
                full_attacker_sequence = full_attacker_sequence + [attacker_sequence[i]]
                full_defender_sequence = full_defender_sequence + [
                    EmulationDefenderStoppingActions.CONTINUE(index=-1)] * (num_wait_steps + 1)
            T = len(full_attacker_sequence)
            assert len(full_defender_sequence) == len(full_attacker_sequence)
            logger.info(f"Starting execution of static action sequences, iteration:{i}, T:{T}, "
                        f"I_t:{intrusion_start_time}")
            sys.stdout.flush()
            s.reset()
            emulation_trace = EmulationTrace(initial_attacker_observation_state=s.attacker_obs_state,
                                             initial_defender_observation_state=s.defender_obs_state,
                                             emulation_name=emulation_env_config.name)
            s.defender_obs_state.reset_metric_lists()
            time.sleep(sleep_time)
            s.defender_obs_state.average_metric_lists()
            emulation_statistics.update_initial_statistics(s=s)
            traces = emulation_traces + [emulation_trace]
            if len(traces) > data_collection_job.num_cached_traces:
                data_collection_job.traces = traces[-data_collection_job.num_cached_traces:]
            else:
                data_collection_job.traces = traces
            for t in range(T):
                old_state = s.copy()
                a1 = full_defender_sequence[t]
                a2 = full_attacker_sequence[t]
                logger.info(f"t:{t}, a1: {a1}, a2: {a2}")
                s.defender_obs_state.reset_metric_lists()
                emulation_trace, s = Emulator.run_actions(
                    emulation_env_config=emulation_env_config, attacker_action=a2, defender_action=a1,
                    sleep_time=sleep_time, trace=emulation_trace, s=s)
                emulation_statistics.update_delta_statistics(s=old_state, s_prime=s, a1=a1, a2=a2)
                total_steps = (1 / intrusion_start_p) * repeat_times
                collected_steps += 1
                data_collection_job.num_collected_steps = collected_steps
                data_collection_job.progress_percentage = (round(collected_steps / total_steps, 2))
                data_collection_job.num_sequences_completed = i
                data_collection_job.traces[-1] = emulation_trace
                logger.debug(f"job updated, steps collected: {data_collection_job.num_collected_steps}, "
                             f"progress: {data_collection_job.progress_percentage}, "
                             f"sequences completed: {i}/{repeat_times}")
                sys.stdout.flush()
                MetastoreFacade.update_data_collection_job(data_collection_job=data_collection_job,
                                                           id=data_collection_job.id)
                MetastoreFacade.update_emulation_statistic(emulation_statistics=emulation_statistics, id=statistics_id)

            if save and i % save_emulation_traces_every == 0:
                MetastoreFacade.save_emulation_trace(emulation_trace)
            emulation_traces.append(emulation_trace)

        logger.info("All sequences completed, saving traces and emulation statistics")
        sys.stdout.flush()
        if save:
            EmulationTrace.save_traces_to_disk(traces_save_dir=save_dir, traces=emulation_traces)
            MetastoreFacade.update_emulation_statistic(emulation_statistics=emulation_statistics, id=statistics_id)
        s.cleanup()
        MetastoreFacade.remove_data_collection_job(data_collection_job=data_collection_job)

    @staticmethod
    def run_actions(emulation_env_config: EmulationEnvConfig, attacker_action: EmulationAttackerAction,
                    s: EmulationEnvState,
                    defender_action: EmulationDefenderAction, trace: EmulationTrace,
                    sleep_time: int = 1) -> Tuple[EmulationTrace, EmulationEnvState]:
        """
        Runs a pair of actions in the emulation and updates a provided trace

        :param emulation_env_config: configuration of the emulation environment
        :param attacker_action: the attacker action
        :param s: the current emulation state
        :param defender_action: the defender action
        :param trace: the trace to update
        :param sleep_time: the time-step length
        :return: the updated trace and state
        """
        logger = Logger.__call__().get_logger()
        attacker_action.ips = s.attacker_obs_state.get_action_ips(a=attacker_action,
                                                                  emulation_env_config=emulation_env_config)
        defender_action.ips = s.defender_obs_state.get_action_ips(a=defender_action,
                                                                  emulation_env_config=emulation_env_config)
        logger.debug(f"Executing attacker action:{attacker_action.name} on machine index: {attacker_action.index}, "
                     f"ips:{attacker_action.ips}")
        s_prime = Attacker.attacker_transition(s=s, attacker_action=attacker_action)
        logger.debug(f"Attacker action complete, attacker state:{s_prime.attacker_obs_state}")
        EnvDynamicsUtil.cache_attacker_action(a=attacker_action, s=s_prime)
        logger.debug(f"Executing defender action:{defender_action.name} on machine index: {defender_action.index}")
        s_prime_prime = Defender.defender_transition(s=s_prime, defender_action=defender_action)
        logger.debug(f"Defender action complete, defender state:{s_prime.defender_obs_state}, "
                     f"ips:{defender_action.ips}")
        sys.stdout.flush()
        EnvDynamicsUtil.cache_defender_action(a=defender_action, s=s_prime_prime)
        time.sleep(sleep_time)
        s_prime_prime.defender_obs_state.average_metric_lists()
        trace.attacker_observation_states.append(s_prime_prime.attacker_obs_state.copy())
        trace.defender_observation_states.append(s_prime_prime.defender_obs_state.copy())
        trace.attacker_actions.append(attacker_action)
        trace.defender_actions.append(defender_action)
        s = s_prime_prime
        return trace, s
