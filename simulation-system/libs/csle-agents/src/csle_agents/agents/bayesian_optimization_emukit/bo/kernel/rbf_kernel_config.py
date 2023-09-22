from typing import Dict, Any
import GPy
from csle_agents.agents.bayesian_optimization_emukit.bo.kernel.kernel_config import KernelConfig


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

    def create_kernel(self, input_dim: int, var_function: Any = None) -> GPy.kern.RBF:
        """
        Creates the GPy kernel

        :param input_dim: the dimension of the input of the function to model
        :param var_function: the variance function of the kernel
        :return: the created GPy RBF kernel
        """
        return GPy.kern.RBF(input_dim, lengthscale=self.lengthscale_rbf_kernel, variance=self.variance_rbf_kernel)

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "RBFKernelConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        dto = RBFKernelConfig(lengthscale_rbf_kernel=d["lengthscale_rbf_kernel"],
                              variance_rbf_kernel=d["variance_rbf_kernel"])
        return dto

    def to_dict(self) -> Dict[str, Any]:
        """
        Gets a dict representation of the object

        :return: A dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["lengthscale_rbf_kernel"] = self.lengthscale_rbf_kernel
        d["variance_rbf_kernel"] = self.variance_rbf_kernel
        return d

    @staticmethod
    def from_json_file(json_file_path: str) -> "RBFKernelConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return RBFKernelConfig.from_dict(json.loads(json_str))
