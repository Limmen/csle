from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState


class DefenderStoppingMiddleware:
    """
    Class that implements optimal stopping actions for the defender.
    """

    @staticmethod
    def stop_monitor(s: EmulationEnvState) -> EmulationEnvState:
        """
        Performs a stopping action for the defender (reports an intrusion)

        :param s: the current state
        :param defender_action: the action to take
        :param attacker_action: the previous action of the attacker
        :param emulation_env_config: the emulation environment configuration
        :return: s_prime
        """
        s_prime = s
        if s.defender_obs_state is not None:
            s_prime.defender_obs_state.stopped = True
        return s_prime

    @staticmethod
    def continue_monitor(s: EmulationEnvState) -> EmulationEnvState:
        """
        Performs a "continue" action for the defender (continues monitoring)

        :param s: the current state
        :param defender_action: the action to take
        :param attacker_action: the previous action of the attacker
        :param emulation_env_config: the emulation environment configuration
        :return: s_prime, reward, done
        """
        s_prime = s
        return s_prime
