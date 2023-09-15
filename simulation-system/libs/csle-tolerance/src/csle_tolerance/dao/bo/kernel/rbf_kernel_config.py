from typing import Callable
import GPy
from csle_tolerance.dao.bo.kernel.kernel_config import KernelConfig


class RBFKernelConfig(KernelConfig):
    """
    DTO representing the configuration of the RBF Kernel, based on the implementation in GPy.
    """

    def __init__(self, lengthscale_rbf_kernel: float = 1., variance_rbf_kernel: float = 1.) -> None:
        """
        Initializes the DTO

        :param lengthscale_rbf_kernel: the lengthscale hyperparameter of the RBF kernel
        :param variance_rbf_kernel: the variance hyperparameter of the RBF kernel
        """
        super().__init__()
        self.lengthscale_rbf_kernel = lengthscale_rbf_kernel
        self.variance_rbf_kernel = variance_rbf_kernel

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"lengthscale_rbf_kernel: {self.lengthscale_rbf_kernel}, " \
               f"variance_rbf_kernel: {self.variance_rbf_kernel}"

    def create_kernel(self, input_dim: int, var_function: Callable = None) -> GPy.kern.RBF:
        """
        Creates the GPy kernel

        :param input_dim: the dimension of the input of the function to model
        :param var_function: the variance function of the kernel
        :return: the created GPy RBF kernel
        """
        return GPy.kern.RBF(input_dim, lengthscale=self.lengthscale_rbf_kernel, variance=self.variance_rbf_kernel)
