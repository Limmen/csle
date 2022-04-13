from typing import Dict, Any, List
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction


class SystemIdentificationJobConfig:
    """
    DTO representing the configuration of a system identification job
    """

    def __init__(self, emulation_env_name: str, num_collected_steps : int,
                 progress_percentage: float, attacker_sequence: List[EmulationAttackerAction], pid: int,
                 defender_sequence: List[EmulationDefenderAction]):
        """
        Initializes the DTO

        :param emulation_env_name: the emulation environment name
        :param experiment_config:
        :param average_r:
        :param progress_percentage:
        """
        self.emulation_env_name = emulation_env_name
        self.progress_percentage = round(progress_percentage,3)
        self.pid = pid
        self.num_collected_steps = num_collected_steps
        self.progress_percentage = self.progress_percentage
        self.attacker_sequence = attacker_sequence
        self.defender_sequence = defender_sequence
        self.id = -1

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["emulation_env_name"] = self.emulation_env_name
        d["progress_percentage"] = round(self.progress_percentage,2)
        d["pid"] = self.pid
        d["num_collected_steps"] = self.num_collected_steps
        d["progress_percentage"] = self.progress_percentage
        d["attacker_sequence"] = list(map(lambda x: x.to_dict(), self.attacker_sequence))
        d["defender_sequence"] = list(map(lambda x: x.to_dict(), self.defender_sequence))
        d["id"] = self.id
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SystemIdentificationJobConfig":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = SystemIdentificationJobConfig(
            emulation_env_name=d["emulation_env_name"], pid=d["pid"], num_collected_steps=d["num_collected_steps"],
            progress_percentage=d["progress_percentage"],
            attacker_sequence=list(map(lambda x: EmulationAttackerAction.from_dict(x), d["attacker_sequence"])),
            defender_sequence=list(map(lambda x: EmulationDefenderAction.from_dict(x), d["defender_sequence"]))
        )
        obj.id = d["id"]
        return obj

    def __str__(self):
        """
        :return: a string representation of the object
        """
        return f"emulation_env_name: {self.emulation_env_name}, pid: {self.pid}, " \
               f"progress_percentage: {self.progress_percentage}, " \
               f"attacker_sequence={list(map(lambda x: str(x), self.attacker_sequence))}," \
               f"defender_sequence={list(map(lambda x: str(x), self.defender_sequence))}, id: {self.id}"