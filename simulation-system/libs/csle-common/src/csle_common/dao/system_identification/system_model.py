from typing import Dict, Any
from abc import ABC, abstractmethod
from csle_common.dao.system_identification.system_model_type import SystemModelType


class SystemModel(ABC):
    """
    Abstract system model
    """

    def __init__(self, descr: str, model_type: SystemModelType):
        """
        Abstract constructor

        :param descr: the description of the system model
        :param model_type: the type of the system model
        """
        self.descr = descr
        self.model_type = model_type

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

    @staticmethod
    @abstractmethod
    def from_dict(d: Dict[str, Any]) -> "SystemModel":
        pass

    @abstractmethod
    def copy(self) -> "SystemModel":
        pass
