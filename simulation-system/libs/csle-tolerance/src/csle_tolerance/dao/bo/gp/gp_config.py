import numpy as np
import GPy
from emukit.model_wrappers.gpy_model_wrappers import GPyModelWrapper
from csle_tolerance.dao.bo.kernel.kernel_config import KernelConfig


class GPConfig:
    """
    DTO class representing the configuration of a Gaussian Process (GP) based on GPy
    """

    def __init__(self, kernel_config: KernelConfig, obs_likelihood_variance: float = 1e-10) -> None:
        """
        Initializes the DTO

        :param kernel_config: the kernel config
        :param obs_likelihood_variance: the likelihood model of the variance when sampling from the true function
        """
        self.kernel_config = kernel_config
        self.obs_likelihood_variance = obs_likelihood_variance

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return f"kernel_config: {self.kernel_config}, obs_Likelihood_variance: {self.obs_likelihood_variance}"

    def create_gp(self, X: np.ndarray, Y: np.ndarray, input_dim: int) -> GPyModelWrapper:
        """
        Creates the GP model

        :param X: the initial X values
        :param Y: the initial Y values
        :param input_dim: the dimension of the X-values
        :return: the GP model (wrapped in emukit object)
        """
        return GPyModelWrapper(GPy.models.GPRegression(
            X, Y, self.kernel_config.create_kernel(input_dim=input_dim), noise_var=self.obs_likelihood_variance))
