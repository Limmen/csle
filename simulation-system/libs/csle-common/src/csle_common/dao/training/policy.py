from typing import Union, List, Dict, Any
from abc import abstractmethod
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType
from csle_base.json_serializable import JSONSerializable


class Policy(JSONSerializable):
    """
    An abstract class representing a policy
    """

    def __init__(self, agent_type: AgentType, player_type: PlayerType) -> None:
        """
        Initializes the object

        :param agent_type: the type of the agent using the policy
        :param player_type: the type of player using the policy (e.g. defender or attacker)
        """
        self.agent_type = agent_type
        self.player_type = player_type

    @abstractmethod
    def action(self, o: Union[List[Union[int, float]], int, float]) -> Union[int, float]:
        """
        Calculates the next action

        :param o: the input observation
        :return: the action
        """
        pass

    @abstractmethod
    def to_dict(self) -> Dict[Any, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        pass

    @abstractmethod
    def stage_policy(self, o: Union[List[Union[int, float]], int, float]) -> List[List[float]]:
        """
        Returns a stage policy (see Horak & Bosansky 2019)

        :param o: the observation for the stage
        :return: the stage policy
        """
        pass

    @staticmethod
    @abstractmethod
    def from_dict(d: Dict[Any, Any]) -> "Policy":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict representation to convert
        :return: the converted object
        """
        pass

    @abstractmethod
    def probability(self, o: Union[List[Union[int, float]], int, float], a: int) -> float:
        """
        Calculates the probability of a given action for a given observation

        :param o: the observation
        :param a: the action
        :return: the probability
        """
        pass

    @abstractmethod
    def copy(self) -> "Policy":
        """
        :return: a copy of the object
        """
        pass

    @staticmethod
    @abstractmethod
    def from_json_file(json_file_path: str) -> "Policy":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        pass
