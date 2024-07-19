from csle_common.util.plotting_util import PlottingUtil
from scipy import stats
import numpy as np


class TestPlottingUtilSuite:
    """
    Test suite for plotting util
    """

    def test_running_average(self) -> None:
        """
        Test the function used to compute the running average of the last N elements of a vector x

        :return: None
        """
        x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        N = 3
        expected = np.array([1, 2, 3, 3, 4, 5, 6, 7, 8, 9])
        result = PlottingUtil.running_average(x, N)
        assert result.any() == expected.any()

    def test_mean_confidence_interval(self) -> None:
        """
        Test function that computes confidence intervals

        :return: None
        """
        data = np.array([1, 2, 3, 4, 5])
        mean, h = PlottingUtil.mean_confidence_interval(data=data, confidence=0.95)
        expected_mean = np.mean(data)
        expected_se = stats.sem(data)
        expected_h = expected_se * stats.t.ppf((1 + 0.95) / 2.0, len(data) - 1)
        assert expected_mean == mean
        assert expected_h == h

    def test_min_max_norm(self) -> None:
        """
        Test function that computes min-max normalization of a vector

        :return: None
        """
        vec = np.array([1, 2, 3, 4, 5])
        min_val = 1
        max_val = 5
        expected = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
        result = PlottingUtil.min_max_norm(vec, max_val, min_val)
        assert result.any() == expected.any()
