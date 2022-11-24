from typing import List, Dict, Any
from csle_common.dao.simulation_config.observation_space_config import ObservationSpaceConfig


class JointObservationSpaceConfig:

    def __init__(self, observation_spaces: List[ObservationSpaceConfig]):
        self.observation_spaces = observation_spaces

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "JointObservationSpaceConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = JointObservationSpaceConfig(
            observation_spaces=list(map(lambda x: ObservationSpaceConfig.from_dict(x), d["observation_spaces"]))
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["observation_spaces"] = list(map(lambda x: x.to_dict(), self.observation_spaces))
        return d

    def __str__(self):
        """
        :return: a string representation of the object
        """
        return f"observation spaces: {list(map(lambda x: str(x), self.observation_spaces))}"
