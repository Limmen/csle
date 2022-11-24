from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.metastore.metastore_facade import MetastoreFacade


class EmulationStatisticsWindowed:
    """
    Windowed emulation statistic. The statistic is updated with the last <window size> sampels
    """

    def __init__(self, window_size: int, emulation_name: str, descr: str):
        """
        Initializes the DTO

        :param window_size: the window size
        :param emulation_name: the emulation name
        :param descr: the description
        """
        self.window_size = window_size
        self.initial_states = []
        self.state_transitions = []
        self.emulation_name = emulation_name
        self.descr = descr
        self.emulation_statistics = EmulationStatistics(emulation_name=self.emulation_name, descr=self.descr)
        self.statistics_id = MetastoreFacade.save_emulation_statistic(emulation_statistics=self.emulation_statistics)

    def add_initial_state(self, s: EmulationEnvState) -> None:
        """
        Adds an initial state sample

        :param s: the initial state
        :return: None
        """
        if len(self.initial_states) >= self.window_size:
            self.initial_states.pop(0)
        self.initial_states.append(s)

    def add_state_transition(self, s: EmulationEnvState, s_prime: EmulationEnvState, a1: EmulationDefenderAction,
                             a2: EmulationAttackerAction) -> None:
        """
        Adds a state transition samlpe

        :param s: the state
        :param s_prime: the next state
        :param a1: the defender action
        :param a2: the attacker action
        :return: None
        """
        if len(self.state_transitions) >= self.window_size:
            self.state_transitions.pop(0)
        self.state_transitions.append((s, s_prime, a1, a2))

    def update_emulation_statistics(self) -> None:
        """
        Updates the emulation statistic using the current window of samples

        :return: None
        """
        if len(self.state_transitions) == 0:
            return
        try:
            new_emulation_statistics = EmulationStatistics(emulation_name=self.emulation_name, descr=self.descr)
            print(f"updating statistic, num samples: {len(self.state_transitions)}")
            for i in range(len(self.state_transitions)):
                new_emulation_statistics.update_delta_statistics(
                    s=self.state_transitions[i][0], s_prime=self.state_transitions[i][1],
                    a1=self.state_transitions[i][2], a2=self.state_transitions[i][3])
            for i in range(len(self.initial_states)):
                new_emulation_statistics.update_initial_statistics(s=self.initial_states[i])
            self.emulation_statistics = new_emulation_statistics
            self.emulation_statistics.id = self.statistics_id
            MetastoreFacade.update_emulation_statistic(emulation_statistics=self.emulation_statistics,
                                                       id=self.statistics_id)
        except Exception:
            pass
