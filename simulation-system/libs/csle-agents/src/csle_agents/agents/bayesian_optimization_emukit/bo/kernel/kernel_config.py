from typing import Dict, Any
from abc import ABC, abstractmethod
import GPy.kern
from csle_base.encoding.np_encoder import NpEncoder


class KernelConfig(ABC):
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

    def to_json_file(self, json_file_path: str) -> None:
        """
        Saves the object to a json file

        :param json_file_path: the json file path to save  the DTO to
        :return: None
        """
        import io
        json_str = self.to_json_str()
        with io.open(json_file_path, 'w', encoding='utf-8') as f:
            f.write(json_str)

    def to_json_str(self) -> str:
        """
        Converts the DTO into a json string

        :return: the json string representation of the DTO
        """
        import json
        json_str = json.dumps(self.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
        return json_str

    def __eq__(self, other: object) -> bool:
        """
        Compares equality with another object

        :param other: the object to compare with
        :return: True if equals, False otherwise
        """
        if not isinstance(other, KernelConfig):
            return False
        else:
            return self.to_dict() == other.to_dict()
