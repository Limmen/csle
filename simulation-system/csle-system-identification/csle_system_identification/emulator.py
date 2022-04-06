import time
from typing import List
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
                             emulation_statistics: EmulationStatistics = None) -> None:
        """
        Runs an attacker and defender sequence in the emulation <repeat_times> times

        :param emulation_env_config: the configuration of the emulation
        :param attacker_sequence: the sequence of attacker actions
        :param defender_sequence: the sequenceo of defender actions
        :param repeat_times: the number of times to repeat the sequences
        :param sleep_time: the number of seconds to sleep between time-steps
        :param save_dir: the directory to save the collected traces
        :param emulation_statistics: the emulation statistics to update
        :return: None
        """
        logger = Logger.__call__().get_logger()
        if save_dir is None:
            save_dir = ExperimentUtil.default_output_dir() + "/results"
        assert len(attacker_sequence) == len(defender_sequence)
        if emulation_statistics is None:
            emulation_statistics = EmulationStatistics(emulation_name=emulation_env_config.name)
        T = len(attacker_sequence)
        s = EmulationEnvState(emulation_env_config=emulation_env_config)
        emulation_traces = []
        for i in range(repeat_times):
            logger.info(f"Starting execution of static action sequences, iteration :{i}")
            emulation_trace = EmulationTrace(initial_attacker_observation_state=s.attacker_obs_state,
                                   initial_defender_observation_state=s.defender_obs_state,
                                   emulation_name=emulation_env_config.name)
            time.sleep(sleep_time)
            for t in range(T):
                old_state = s.copy()
                a1 = defender_sequence[t]
                a2 = attacker_sequence[t]
                a2.ips = s.attacker_obs_state.get_action_ips(a=a2, emulation_env_config=emulation_env_config)
                a1.ips = s.defender_obs_state.get_action_ips(a=a1, emulation_env_config=emulation_env_config)
                logger.debug(f"Executing attacker action:{a2.name} on machine index: {a2.index}, t={t}, ips:{a2.ips}")
                s_prime = Attacker.attacker_transition(s=s, attacker_action=a2, simulation=False)
                logger.debug(f"Attacker action complete, attacker state:{s_prime.attacker_obs_state}")
                EnvDynamicsUtil.cache_attacker_action(a=a2, s=s_prime)
                logger.debug(f"Executing defender action:{a1.name} on machine index: {a1.index}, t={t}")
                s_prime_prime = Defender.defender_transition(s=s_prime, defender_action=a1, simulation=False)
                logger.debug(f"Defender action complete, defender state:{s_prime.defender_obs_state}, ips:{a1.ips}")
                EnvDynamicsUtil.cache_defender_action(a=a1, s=s_prime_prime)
                s = s_prime_prime
                emulation_trace.attacker_observation_states.append(s_prime_prime.attacker_obs_state.copy())
                emulation_trace.defender_observation_states.append(s_prime_prime.defender_obs_state.copy())
                emulation_trace.attacker_actions.append(a2)
                emulation_trace.defender_actions.append(a1)
                time.sleep(sleep_time)
                emulation_statistics.update_statistics(s=old_state, s_prime=s, a1=a1, a2=a2)
            MetastoreFacade.save_emulation_trace(emulation_trace)
            emulation_traces.append(emulation_trace)
        logger.info(f"All sequences completed, saving traces and emulation statistics")
        EmulationTrace.save_traces_to_disk(traces_save_dir=save_dir, traces=emulation_traces)
        MetastoreFacade.save_emulation_statistic(emulation_statistics=emulation_statistics)
