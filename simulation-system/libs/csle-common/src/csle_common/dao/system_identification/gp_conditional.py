from typing import List, Dict, Any, Union
import gpytorch
from numpy.typing import NDArray
import torch
from csle_common.dao.system_identification.gp_regression_model_with_gauissan_noise import \
    GPRegressionModelWithGaussianNoise
from csle_base.json_serializable import JSONSerializable


class GPConditional(JSONSerializable):
    """
    A DTO representing a Gaussian process conditional distribution
    """

    def __init__(self, conditional_name: str, metric_name: str,
                 sample_space: List[int],
                 observed_x: List[Union[float, int]], observed_y: List[Union[float, int]],
                 scale_parameter: float, noise_parameter: float) -> None:
        """
        Initializes the DTO

        :param conditional_name: the name of the conditional
        :param metric_name: the name of the metric
        :param sample_space: the sample space (the domain of the distribution)
        :param observed_x: the observed x samples
        :param observed_y: the observed y samples
        :param scale_parameter: the scale parameter for the scale kernel
        :param noise_parameter: the noise parameter for the Gaussian noise likelihood
        """
        self.conditional_name = conditional_name
        self.metric_name = metric_name
        self.sample_space = sample_space
        self.observed_x = observed_x
        self.observed_y = observed_y
        self.scale_parameter = scale_parameter
        self.noise_parameter = noise_parameter
        self.distribution: List[NDArray[Any]] = []

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "GPConditional":
        """
        Converts a dict representation of the DTO into an instance

        :param d: the dict to convert
        :return: the converted instance
        """
        return GPConditional(
            conditional_name=d["conditional_name"], metric_name=d["metric_name"],
            sample_space=d["sample_space"], observed_x=d["observed_x"], observed_y=d["observed_y"],
            scale_parameter=d["scale_parameter"], noise_parameter=d["noise_parameter"]
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["conditional_name"] = self.conditional_name
        d["metric_name"] = self.metric_name
        d["sample_space"] = self.sample_space
        d["observed_x"] = self.observed_x
        d["observed_y"] = self.observed_y
        d["scale_parameter"] = self.scale_parameter
        d["noise_parameter"] = self.noise_parameter
        d["distribution"] = self.distribution
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return f"conditional_name:{self.conditional_name}, metric_name: {self.metric_name}, " \
               f"sample_space: {self.sample_space}, observed_x: {self.observed_x}, observed_y: {self.observed_y}," \
               f"scale_parameter: {self.scale_parameter}, noise_parameter: {self.noise_parameter}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "GPConditional":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return GPConditional.from_dict(json.loads(json_str))

    def generate_distribution(self) -> None:
        """
        Updates the distribution

        :return: None
        """
        self.sample_space.sort()
        self.distribution = list(self.generate_distributions_for_samples(samples=self.sample_space).tolist())

    def generate_distributions_for_samples(self, samples) -> Any:
        """
        Generates distributions for a given sample

        :param samples: the sample
        :return: the created distributions
        """
        samples = torch.tensor(samples)
        likelihood = gpytorch.likelihoods.GaussianLikelihood()
        model = GPRegressionModelWithGaussianNoise(torch.tensor(self.observed_x), torch.tensor(self.observed_y),
                                                   likelihood)
        model.covar_module.base_kernel.lengthscale = torch.tensor(self.scale_parameter)
        model.likelihood.noise = torch.tensor(self.noise_parameter)

        model.eval()
        likelihood.eval()
        # Make predictions by feeding model through likelihood
        with torch.no_grad(), gpytorch.settings.fast_pred_var():
            test_x = torch.tensor(samples)
            dist = likelihood(model(test_x)).mean.numpy()
            return dist
