import time
from typing import List
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.util.env_dynamics_util import EnvDynamicsUtil
from csle_attacker.attacker import Attacker
from csle_defender.defender import Defender


class Emulator:

    @staticmethod
    def run_action_sequences(emulation_env_config: EmulationEnvConfig,
                             attacker_sequence: List[EmulationAttackerAction], defender_sequence: List[EmulationDefenderAction],
                             repeat_times:int = 1, sleep_time : int = 1) -> None:
        """
        Runs an attacker and defender sequence in the emulation <repeat_times> times

        :param emulation_env_config: the configuration of the emulation
        :param attacker_sequence: the sequence of attacker actions
        :param defender_sequence: the sequenceo of defender actions
        :param repeat_times: the number of times to repeat the sequences
        :param sleep_time: the number of seconds to sleep betwen time-steps
        :return: None
        """
        # TODO save traces
        # TODO tensorboard?
        assert len(attacker_sequence) == len(defender_sequence)
        T = len(attacker_sequence)
        s = EmulationEnvState(emulation_env_config=emulation_env_config)
        for i in range(repeat_times):
            print(f"Starting execution of static action sequences, iteration :{i}")
            for t in range(T):
                a1 = defender_sequence[t]
                a2 = attacker_sequence[t]
                a2.ips = s.attacker_obs_state.get_action_ips(a=a2, emulation_env_config=emulation_env_config)
                a1.ips = s.defender_obs_state.get_action_ips(a=a1, emulation_env_config=emulation_env_config)
                print(f"Executing attacker action:{a2.name} on machine index: {a2.index}, t={t}, ips:{a2.ips}")
                s_prime = Attacker.attacker_transition(s=s, attacker_action=a2, simulation=False)
                print(f"Attacker action complete, attacker state:{s_prime.attacker_obs_state}")
                EnvDynamicsUtil.cache_attacker_action(emulation_env_config=emulation_env_config,
                                                      a=a2, s=s_prime)
                print(f"Executing defender action:{a1.name} on machine index: {a1.index}, t={t}")
                s_prime_prime = Defender.defender_transition(s=s_prime, defender_action=a1, simulation=False)
                print(f"Defender action complete, defender state:{s_prime.defender_obs_state}, ips:{a1.ips}")
                EnvDynamicsUtil.cache_defender_action(emulation_env_config=emulation_env_config, a=a1,
                                                      s=s_prime_prime)
                s = s_prime_prime
                time.sleep(sleep_time)
