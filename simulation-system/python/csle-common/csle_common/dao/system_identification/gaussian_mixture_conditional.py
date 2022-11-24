from typing import List, Dict, Any
from sklearn.mixture import GaussianMixture
from scipy.stats import norm
import numpy as np


class GaussianMixtureConditional:
    """
    A DTO representing a Gaussian Mixture Conditional Distribution
    """

    def __init__(self, conditional_name: str, metric_name: str, num_mixture_components: int,
                 dim: int, mixtures_means: List[List[float]],
                 mixtures_covariance_matrix: List[List[List[float]]], mixture_weights: List[float],
                 sample_space: List[int]) -> None:
        """
        Initializes the DTO

        :param conditional_name: the name of the conditional
        :param num_mixture_components: the number of mixture components
        :param dim: the dimension of the distribution, i.e. if it is multivariate
        :param mixtures_means: the means of the mixtures
        :param mixtures_covariance_matrix: the covariance matrices of the mixtures
        :param mixture_weights: the mixture weights
        :param sample_space: the sampĺe space
        """
        self.conditional_name = conditional_name
        self.dim = dim
        self.num_mixture_components = num_mixture_components
        self.mixtures_means = mixtures_means
        self.mixtures_covariance_matrix = mixtures_covariance_matrix
        self.mixture_weights = mixture_weights
        self.metric_name = metric_name
        self.sample_space = sample_space
        self.weighted_mixture_distributions = []
        self.generate_distributions()
        self.combined_distribution = []

    def generate_distributions(self):
        self.sample_space.sort()
        dists = []
        for weight, mean, covar in zip(self.mixture_weights, self.mixtures_means, self.mixtures_covariance_matrix):
            dists.append(list(weight * norm.pdf(self.sample_space, mean, np.sqrt(covar)).ravel()))
        self.weighted_mixture_distributions = dists
        combined_dist = np.zeros(len(self.sample_space))
        for dist in dists:
            d_arr = np.array(dist)
            combined_dist = combined_dist + d_arr
        self.combined_distribution = list(combined_dist)

    def generate_distributions_for_samples(self, samples, normalize: bool = False):
        samples.sort()
        dists = []
        for weight, mean, covar in zip(self.mixture_weights, self.mixtures_means, self.mixtures_covariance_matrix):
            density_dist = list(weight * norm.pdf(samples, mean, np.sqrt(covar)).ravel())
            dists.append(density_dist)
        combined_density_dist = np.zeros(len(samples))
        for density_dist in dists:
            d_arr = np.array(density_dist)
            combined_density_dist = combined_density_dist + d_arr
        combined_density_dist = list(combined_density_dist)
        if normalize:
            combined_prob_dist = list(np.array(combined_density_dist) * (1 / sum(combined_density_dist)))
        else:
            combined_prob_dist = combined_density_dist
        return combined_prob_dist

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "GaussianMixtureConditional":
        """
        Converts a dict representation of the DTO into an instance

        :param d: the dict to convert
        :return: the converted instance
        """
        return GaussianMixtureConditional(
            conditional_name=d["conditional_name"],
            num_mixture_components=d["num_mixture_components"],
            dim=d["dim"], mixtures_means=d["mixture_means"],
            mixtures_covariance_matrix=d["mixtures_covariance_matrix"],
            mixture_weights=d["mixture_weights"], metric_name=d["metric_name"],
            sample_space=d["sample_space"]
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the DTO
        """
        d = {}
        d["conditional_name"] = self.conditional_name
        d["dim"] = self.dim
        d["num_mixture_components"] = self.num_mixture_components
        d["mixture_means"] = self.mixtures_means
        d["mixtures_covariance_matrix"] = self.mixtures_covariance_matrix
        d["mixture_weights"] = self.mixture_weights
        d["metric_name"] = self.metric_name
        d["sample_space"] = self.sample_space
        d["weighted_mixture_distributions"] = self.weighted_mixture_distributions
        d["combined_distribution"] = self.combined_distribution
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return f"conditional_name:{self.conditional_name}, num_mixture_components: {self.num_mixture_components}, " \
               f"dim: {self.dim}, mixtures_means: {self.mixtures_means}, " \
               f"mixtures_covariance_matrix: {self.mixtures_covariance_matrix}, " \
               f"mixture_weights: {self.mixture_weights}," \
               f"metric_name: {self.metric_name}, sample space: {self.sample_space}, " \
               f"combined distribution: {self.combined_distribution}"

    def to_json_str(self) -> str:
        """
        Converts the DTO into a json string

        :return: the json string representation of the DTO
        """
        import json
        json_str = json.dumps(self.to_dict(), indent=4, sort_keys=True)
        return json_str

    def to_json_file(self, json_file_path: str) -> None:
        """
        Saves the DTO to a json file

        :param json_file_path: the json file path to save  the DTO to
        :return: None
        """
        import io
        json_str = self.to_json_str()
        with io.open(json_file_path, 'w', encoding='utf-8') as f:
            f.write(json_str)

    @staticmethod
    def from_sklearn_gaussian_mixture(gmm: GaussianMixture, conditional_name: str, metric_name: str,
                                      num_components: int, sample_space: List[int],
                                      dim: int = 1) -> "GaussianMixtureConditional":
        """
        Creates the DTO from a Gaussian mixture fitted with sklearn

        :param gmm: the sklearn model
        :param conditional_name: the name of the conditional
        :param metric_name: the metric name
        :param num_components: the number of components of the mixture
        :param dim: the dimension of the mixture
        :param sample_space: the sample space
        :return: a GaussianMixtureConditional instance
        """
        mixture_weights = list(gmm.weights_)
        means = list(gmm.means_.tolist())
        covariances = list(gmm.covariances_.tolist())
        return GaussianMixtureConditional(
            conditional_name=conditional_name, metric_name=metric_name, num_mixture_components=num_components,
            mixtures_means=means, mixtures_covariance_matrix=covariances, mixture_weights=mixture_weights, dim=dim,
            sample_space=sample_space)
