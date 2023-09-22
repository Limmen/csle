from typing import Dict, Any
import numpy.typing as npt
import GPy
from emukit.model_wrappers.gpy_model_wrappers import GPyModelWrapper
from csle_agents.agents.bayesian_optimization_emukit.bo.kernel.kernel_config import KernelConfig


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

    def create_gp(self, X: npt.NDArray[Any], Y: npt.NDArray[Any], input_dim: int) -> GPyModelWrapper:
        """
        Creates the GP model

        :param X: the initial X values
        :param Y: the initial Y values
        :param input_dim: the dimension of the X-values
        :return: the GP model (wrapped in emukit object)
        """
        return GPyModelWrapper(GPy.models.GPRegression(
            X, Y, self.kernel_config.create_kernel(input_dim=input_dim, var_function=None),
            noise_var=self.obs_likelihood_variance))

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "GPConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        from csle_agents.agents.bayesian_optimization_emukit.bo.kernel.rbf_kernel_config import RBFKernelConfig
        dto = GPConfig(
            kernel_config=RBFKernelConfig.from_dict(d["kernel_config"]),
            obs_likelihood_variance=d["obs_likelihood_variance"]
        )
        return dto

    def to_dict(self) -> Dict[str, Any]:
        """
        Gets a dict representation of the object

        :return: A dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["obs_likelihood_variance"] = self.obs_likelihood_variance
        d["kernel_config"] = self.kernel_config.to_dict()
        return d

    @staticmethod
    def from_json_file(json_file_path: str) -> "GPConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return GPConfig.from_dict(json.loads(json_str))
