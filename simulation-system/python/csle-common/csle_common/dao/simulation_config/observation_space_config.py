from typing import List, Dict, Any
from csle_common.dao.simulation_config.value_type import ValueType
from csle_common.dao.simulation_config.observation import Observation


class ObservationSpaceConfig:
    """
    DTO representing the configuration of the observation space of a single player in a simulation environment
    """

    def __init__(self, observations: List[Observation], observation_type: ValueType, descr: str,
                 player_id: int, observation_component_name_to_index: Dict[str, int],
                 observation_id_to_observation_vector: Dict[int, List]):
        """
        Initializes the DTO

        :param observations: the list of observations
        :param observation_type: the observation type
        :param descr: a description of the observation space
        :param player_id: the id of the player
        :param observation_component_name_to_index
        :param observation_id_to_observation_vector
        """
        self.observations = observations
        self.observation_type = observation_type
        self.descr = descr
        self.player_id = player_id
        self.observation_component_name_to_index = observation_component_name_to_index
        self.observation_id_to_observation_vector = observation_id_to_observation_vector

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ObservationSpaceConfig":
        """
        Converts a dict representation to an instance
        :param d: the dict to convert
        :return: the created instance
        """
        obj = ObservationSpaceConfig(
            observations=list(map(lambda x: Observation.from_dict(x), d["observations"])),
            observation_type=d["observation_type"], descr=d["descr"],
            player_id=d["player_id"], observation_component_name_to_index=d["observation_component_name_to_index"],
            observation_id_to_observation_vector=d["observation_id_to_observation_vector"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["observations"] = list(map(lambda x: x.to_dict(), self.observations))
        d["observation_type"] = self.observation_type
        d["descr"]= self.descr
        d["player_id"]= self.player_id
        d["observation_component_name_to_index"] = self.observation_component_name_to_index
        d["observation_id_to_observation_vector"] = self.observation_id_to_observation_vector
        return d

    def __str__(self):
        """
        :return: a string representation of the object
        """
        return f"observations: {self.observations}, observation_type: {self.observation_type}, " \
               f"descr: {self.descr}, player_id: {self.player_id}, " \
               f"observation_component_name_to_index: {self.observation_component_name_to_index}, " \
               f"observation_id_to_observation_vector: {self.observation_id_to_observation_vector}"