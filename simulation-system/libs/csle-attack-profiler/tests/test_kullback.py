from csle_attack_profiler.dao.kullback_for_all import KullbackLeibler
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
import os


class TestKullbackSuite:
    """
    Test suite for the Kullback-Leibler divergence calculation class.
    """

    def test_kullback_counts(self) -> None:
        """
        Test the Kullback-Leibler divergence for two lists of counts.
        """
        p = [1, 4, 1, 4]
        q = [5, 3, 5, 1]

        kl_div = KullbackLeibler.kullback_leibler_divergence_for_counts(p, q)

        assert round(kl_div, 2) == round(0.68, 2)

    def test_kullback_statistics(self) -> None:
        """
        Test the Kullback-Leibler divergence for two lists of statistics.
        """
        current_dir = os.path.dirname(__file__)
        path = os.path.join(current_dir, "statistics_test.json")
        statistics = EmulationStatistics.from_json_file(path)

        kl_div, kl_div2 = KullbackLeibler.kullback_leibler_for_metric("alerts_weighted_by_priority",
                                                                      "A:MyTest", statistics)
        assert kl_div is not None
        assert round(float(kl_div), 2) == 12.27
        assert kl_div2 is not None
        assert round(float(kl_div2), 2) == 8.52
