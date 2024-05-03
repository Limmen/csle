from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
from typing import List, Tuple, Union
import numpy as np


class KullbackLeibler:
    """
    Utility class for computing KL values
    """

    @staticmethod
    def kullback_leibler_divergence_for_counts(p: List[int], q: List[int]) -> float:
        """
        Compute the Kullback-Leibler divergence for a counts distribution.

        :param p: the counts distribution p
        :param q: the counts distribution q
        :return: the Kullback-Leibler divergence
        """
        probs_p = p / np.sum(p, dtype=float)
        probs_q = q / np.sum(q, dtype=float)
        kl_div: float = np.sum(probs_p * np.log(probs_p / probs_q), dtype=float)
        return kl_div

    @staticmethod
    def kullback_leibler_for_metric(metric_kl: str, attacker_action: str, statistics_object: EmulationStatistics) \
            -> Tuple[Union[float, None], Union[float, None]]:
        """
        Compute the Kullback-Leibler divergence for a metric.

        :param metric: the metric
        :return: the Kullback-Leibler divergence
        """
        KLD_PQ = 0.0
        KLD_QP = 0.0
        statistics = statistics_object

        cond = ''
        for condition, _ in statistics.conditionals_probs.items():
            condition_parts = condition.split('_')
            if condition_parts[0] != attacker_action:
                print("continue")
                continue
            else:
                cond = condition
                break
        if cond == '':
            return None, None
        attacker_actions = statistics.conditionals_probs[cond][metric_kl]
        X = list(map(lambda x: float(x), list(attacker_actions.keys())))
        Y = list(map(lambda x: float(x), list(attacker_actions.values())))
        # Out p(x)
        no_intrusion = statistics.conditionals_probs["no_intrusion"][metric_kl]
        # no_intrusion = statistics.conditionals_counts["no_intrusion"][metric]
        X_no_intrusion = list(map(lambda x: float(x), list(no_intrusion.keys())))
        Y_no_intrusion = list(map(lambda x: float(x), list(no_intrusion.values())))
        if len(X) >= 10:
            P = X
            Q = X_no_intrusion
            CP = len(P)
            CQ = len(Q)
            SU = list(set(X + X_no_intrusion))
            epsilon = 0.0000001
            SU_disjoint_P = len(list(set(SU) - set(P)))
            SU_disjoint_Q = len(list(set(SU) - set(Q)))

            pc = (sum(Y) + epsilon * (SU_disjoint_P) - 1) / CP
            qc = (sum(Y_no_intrusion) + epsilon * (SU_disjoint_Q) - 1) / CQ
            p_prime = []
            q_prime = []

            for val in SU:
                if val in P:
                    p_prime.append((Y[X.index(val)] - pc))
                else:
                    p_prime.append(epsilon)
                if val in X_no_intrusion:
                    q_prime.append((Y_no_intrusion[X_no_intrusion.index(val)] - qc))
                else:
                    q_prime.append(epsilon)

            p_prime_np = np.array(p_prime) / np.sum(p_prime)
            q_prime_np = np.array(q_prime) / np.sum(q_prime)

            KLD_PQ = np.around(np.sum(p_prime_np * np.log(p_prime_np / q_prime_np)), 4)
            KLD_QP = np.around(np.sum(q_prime_np * np.log(q_prime_np / p_prime_np)), 4)

        return float(KLD_PQ), float(KLD_QP)


if __name__ == '__main__':

    statistics = EmulationStatistics.from_json_file("./../../../tests/statistics_test.json")
    KLD_PQ, KLD_QP = KullbackLeibler.kullback_leibler_for_metric('alerts_weighted_by_priority', 'A:MyTest', statistics)

    print(KLD_PQ, KLD_QP)
