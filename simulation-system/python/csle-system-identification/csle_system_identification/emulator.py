from typing import List, Tuple
import time
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
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


class Emulator:
    """
    Class for running episodes in the emulation system
    """

    @staticmethod
    def run_action_sequences(emulation_env_config: EmulationEnvConfig,
                             attacker_sequence: List[EmulationAttackerAction],
                             defender_sequence: List[EmulationDefenderAction],
                             repeat_times:int = 1, sleep_time : int = 1, save_dir: str = None,
                             emulation_statistics: EmulationStatistics = None, descr: str = "",
                             save: bool = True) -> None:
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
        :return: None
        """
        logger = Logger.__call__().get_logger()
        if save_dir is None:
            save_dir = ExperimentUtil.default_output_dir() + "/results"
        assert len(attacker_sequence) == len(defender_sequence)
        if emulation_statistics is None:
            emulation_statistics = EmulationStatistics(emulation_name=emulation_env_config.name, descr=descr)
        if emulation_statistics.id == -1 or emulation_statistics.id is None and save:
            statistics_id = MetastoreFacade.save_emulation_statistic(emulation_statistics=emulation_statistics)
        else:
            statistics_id = -1
            if emulation_statistics is not None:
                statistics_id = emulation_statistics.id
        T = len(attacker_sequence)
        s = EmulationEnvState(emulation_env_config=emulation_env_config)
        s.initialize_defender_machines()
        emulation_traces = []
        for i in range(repeat_times):
            logger.info(f"Starting execution of static action sequences, iteration :{i}")
            s.reset()
            emulation_trace = EmulationTrace(initial_attacker_observation_state=s.attacker_obs_state,
                                   initial_defender_observation_state=s.defender_obs_state,
                                   emulation_name=emulation_env_config.name)
            time.sleep(sleep_time)
            emulation_statistics.update_initial_statistics(s=s)
            print(emulation_statistics)
            for t in range(T):
                old_state = s.copy()
                a1 = defender_sequence[t]
                a2 = attacker_sequence[t]
                print(f"a1:{a1}, a2:{a2}")
                emulation_trace, s = Emulator.run_actions(
                    emulation_env_config=emulation_env_config,  attacker_action=a2, defender_action=a1,
                    sleep_time=sleep_time, trace=emulation_trace, s=s)
                emulation_statistics.update_delta_statistics(s=old_state, s_prime=s, a1=a1, a2=a2)
                print(emulation_statistics.conditionals["intrusion"]["total_alerts"])
                print(emulation_statistics.conditionals["no_intrusion"]["total_alerts"])
                print(statistics_id)
            if save:
                id = MetastoreFacade.save_emulation_trace(emulation_trace)
                MetastoreFacade.update_emulation_statistic(emulation_statistics=emulation_statistics, id=statistics_id)
                print(f"saving emulation trace, id:{id}")
            emulation_traces.append(emulation_trace)
        logger.info(f"All sequences completed, saving traces and emulation statistics")
        if save:
            EmulationTrace.save_traces_to_disk(traces_save_dir=save_dir, traces=emulation_traces)
            MetastoreFacade.update_emulation_statistic(emulation_statistics=emulation_statistics, id=statistics_id)
        s.cleanup()


    @staticmethod
    def run_actions(emulation_env_config: EmulationEnvConfig, attacker_action: EmulationAttackerAction,
                    s: EmulationEnvState,
                    defender_action: EmulationDefenderAction, trace: EmulationTrace,
                    sleep_time : int = 1) -> Tuple[EmulationTrace, EmulationEnvState]:
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
        s_prime = Attacker.attacker_transition(s=s, attacker_action=attacker_action, simulation=False)
        logger.debug(f"Attacker action complete, attacker state:{s_prime.attacker_obs_state}")
        EnvDynamicsUtil.cache_attacker_action(a=attacker_action, s=s_prime)
        logger.debug(f"Executing defender action:{defender_action.name} on machine index: {defender_action.index}")
        s_prime_prime = Defender.defender_transition(s=s_prime, defender_action=defender_action, simulation=False)
        logger.debug(f"Defender action complete, defender state:{s_prime.defender_obs_state}, "
                     f"ips:{defender_action.ips}")
        EnvDynamicsUtil.cache_defender_action(a=defender_action, s=s_prime_prime)
        s = s_prime_prime
        time.sleep(sleep_time)
        trace.attacker_observation_states.append(s_prime_prime.attacker_obs_state.copy())
        trace.defender_observation_states.append(s_prime_prime.defender_obs_state.copy())
        trace.attacker_actions.append(attacker_action)
        trace.defender_actions.append(defender_action)
        return trace, s
