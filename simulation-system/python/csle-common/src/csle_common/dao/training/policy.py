from typing import Union, List, Dict
from abc import ABC, abstractmethod
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType


class Policy(ABC):

    def __init__(self, agent_type: AgentType, player_type: PlayerType):
        self.agent_type = agent_type
        self.player_type = player_type

    @abstractmethod
    def action(self, o: Union[List[Union[int, float]], int, float]) -> Union[int, float]:
        pass

    @abstractmethod
    def to_dict(self) -> Dict:
        pass

    @abstractmethod
    def stage_policy(self, o: Union[List[Union[int, float]], int, float]) -> List[List[float]]:
        pass

    @staticmethod
    @abstractmethod
    def from_dict(d: Dict) -> "Policy":
        pass

    @abstractmethod
    def probability(self, o: Union[List[Union[int, float]], int, float], a: int) -> float:
        pass

    @abstractmethod
    def copy(self) -> "Policy":
        pass
