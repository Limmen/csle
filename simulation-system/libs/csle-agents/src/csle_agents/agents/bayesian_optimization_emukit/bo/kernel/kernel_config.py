from typing import Dict, Any
from abc import ABC, abstractmethod
import GPy.kern
from csle_base.json_serializable import JSONSerializable


class KernelConfig(ABC, JSONSerializable):
    """
    Abstract class representing a kernel configuration
    """

    @abstractmethod
    def create_kernel(self, input_dim: int, var_function: Any) -> GPy.kern.Kern:
        """
        Abstract method for creating the kernel (returning a GPy kernel) that each subclass should implement

        :param input_dim: the input dimension of the function of the GP
        :param var_function: the variance function of the kernel
        :return: the GPY kernel
        """
        pass

    @staticmethod
    @abstractmethod
    def from_dict(d: Dict[str, Any]) -> "KernelConfig":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the converted instance
        """
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        pass

    @staticmethod
    @abstractmethod
    def from_json_file(json_file_path: str) -> "KernelConfig":
        """
        Reads a json file and converts it to an object

        :param json_file_path: the json file path
        :return: the object
        """
        pass
