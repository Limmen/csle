from typing import Tuple
import numpy as np
import scipy.stats as stats


class PlottingUtil:
    """
    Class with utility functions related to plotting
    """

    @staticmethod
    def running_average(x: np.ndarray, N: int) -> np.ndarray:
        """
        Function used to compute the running average of the last N elements of a vector x

        :param x: the vector to average
        :param N: the length of the running average
        :return: the averaged vector
        """
        if len(x) >= N:
            y = np.copy(x)
            y[N - 1:] = np.convolve(x, np.ones((N,)) / N, mode='valid')
        else:
            y = np.zeros_like(x)
        return y

    @staticmethod
    def running_average_list(x: np.ndarray, N: int) -> np.ndarray:
        """
        Function used to compute the running average of the last N elements of a vector x

        :param x: the vector to average
        :param N: the length of the running average
        :return:
        """
        if len(x) >= N:
            y = np.copy(x)
            y[N - 1:] = np.convolve(x, np.ones((N,)) / N, mode='valid')
        else:
            y = np.zeros_like(x)
        return y

    @staticmethod
    def mean_confidence_interval(data: np.ndarray, confidence=0.95) -> Tuple[float, float]:
        """
        Compute confidence intervals

        :param data: the data
        :param confidence: the interval confidence
        :return: the mean, the lower confidence interval, the upper confidence interval
        """
        a = 1.0 * np.array(data)
        n = len(a)
        m, se = np.mean(a), stats.sem(a)
        h = se * stats.t.ppf((1 + confidence) / 2., n - 1)
        return m, h

    @staticmethod
    def min_max_norm(vec: np.ndarray, max_val: float, min_val: float) -> np.ndarray:
        """
        Min-max normalization of a vector

        :param vec: the vector to normalize
        :param max_val: the maximum value for the normalization
        :param min_val: the minimuim value for the normalization
        :return: the normalized vector
        """
        return np.array(list(map(lambda x: (x - min_val) / (max_val - min_val), vec.tolist())))
