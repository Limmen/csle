from typing import Callable
from abc import ABC, abstractmethod
import GPy.kern


class KernelConfig(ABC):
    """
    Abstract class representing a kernel configuration
    """

    def __init__(self):
        pass

    @abstractmethod
    def create_kernel(self, input_dim: int, var_function : Callable = None) -> GPy.kern.Kern:
        """
        Abstract method for creating the kernel (returning a GPy kernel) that each subclass should implement

        :param input_dim: the input dimension of the function of the GP
        :param var_function: the variance function of the kernel
        :return: the GPY kernel
        """
        pass
