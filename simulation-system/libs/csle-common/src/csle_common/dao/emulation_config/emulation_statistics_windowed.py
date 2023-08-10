from typing import Dict, Any, List, Tuple
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_base.json_serializable import JSONSerializable


class EmulationStatisticsWindowed(JSONSerializable):
    """
    Windowed emulation statistic. The statistic is updated with the last <window size> samples
    """

    def __init__(self, window_size: int, emulation_name: str, descr: str):
        """
        Initializes the DTO

        :param window_size: the window size
        :param emulation_name: the emulation name
        :param descr: the description
        """
        self.window_size = window_size
        self.initial_states: List[EmulationEnvState] = []
        self.state_transitions: List[Tuple[EmulationEnvState, EmulationEnvState, EmulationDefenderAction,
                                           EmulationAttackerAction]] = []
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

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EmulationStatisticsWindowed":
        """
        Converts a dict representation of the object into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = EmulationStatisticsWindowed(
            window_size=d["window_size"], emulation_name=d["emulation_name"], descr=d["descr"]
        )
        obj.emulation_statistics = EmulationStatistics.from_dict(d["emulation_statistics"])
        obj.statistics_id = d["statistics_id"]
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["window_size"] = self.window_size
        d["initial_states"] = list(map(lambda x: x.to_dict(), self.initial_states))
        d["state_transitions"] = list(map(lambda x: (x[0].to_dict(), x[1].to_dict(), x[2].to_dict(), x[3].to_dict()),
                                          self.state_transitions))
        d["emulation_name"] = self.emulation_name
        d["descr"] = self.descr
        d["emulation_statistics"] = self.emulation_statistics.to_dict()
        d["statistics_id"] = self.statistics_id
        return d

    @staticmethod
    def from_json_file(json_file_path: str) -> "EmulationStatisticsWindowed":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return EmulationStatisticsWindowed.from_dict(json.loads(json_str))
