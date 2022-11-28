from typing import List, Dict, Any


class ObservationFunctionConfig:
    """
    DTO representing the configuration of the observation function of a simulation
    """

    def __init__(self, observation_tensor: List, component_observation_tensors: Dict[str, List]):
        """
        Initializes the DTO
        :param observation_tensor: the observation tensor
        """
        self.observation_tensor = observation_tensor
        self.component_observation_tensors = component_observation_tensors

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ObservationFunctionConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = ObservationFunctionConfig(
            observation_tensor=d["observation_tensor"],
            component_observation_tensors=d["component_observation_tensors"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["observation_tensor"] = self.observation_tensor
        d["component_observation_tensors"] = self.component_observation_tensors
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"observation tensor: {self.observation_tensor}, " \
               f"component_observation_tensors: {self.component_observation_tensors}"
