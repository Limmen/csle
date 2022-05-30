from typing import Dict, Any
from abc import ABC, abstractmethod


class SystemModel(ABC):
    """
    Abstract system model
    """

    def __init__(self):
        pass

    @abstractmethod
    def to_dict(self)-> Dict[str, Any]:
        pass

    @staticmethod
    @abstractmethod
    def from_dict(d: Dict[str, Any])-> "SystemModel":
        pass