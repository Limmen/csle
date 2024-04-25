
from csle_attack_profiler.dao.kullback_for_all import KullbackLeibler
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
import os

class TestKullbackSuite:

    def test_kullback_counts(self) -> None:
        """
        Test the Kullback-Leibler divergence for two lists of counts.
        """
        p = [1, 4, 1, 4]
        q = [5, 3, 5, 1]

        kl_div = KullbackLeibler.kullback_leibler_divergence_for_counts(p, q)

        assert kl_div == 0.6841752275630617, f"Test failed! Expected: 0.03669001465441545, Actual: {kl_div}"

    def test_kullback_statistics(self) -> None:
        """
        Test the Kullback-Leibler divergence for two lists of statistics.
        """
        current_dir = os.path.dirname(__file__)
        path = os.path.join(current_dir, "statistics_test.json")
        statistics = EmulationStatistics.from_json_file(path)

        kl_div, kl_div2 = KullbackLeibler.kullback_leibler_for_metric("alerts_weighted_by_priority", "A:MyTest", statistics)

        assert kl_div and kl_div2, f"Test failed! Expect values, Actual: {kl_div}, {kl_div2}"