from typing import List, Tuple
import numpy as np


class PomdpSolveParser:
    """
    Parser of the results of the pomdp-solver by Cassandra et. al. (See http://www.pomdp.org/)
    """

    @staticmethod
    def parse_alpha_vectors(file_path: str) -> List[Tuple[int, List[float]]]:
        """
        Parses alpha vectors from a given file location

        :param file_path: path to the file where the alpha vectors are solved
        :return: a list with (action, alphavector)
        """
        with open(file_path, 'r') as f:
            file_contents_str = f.read()
            lines = file_contents_str.split("\n")
            non_empty_lines = list(filter(lambda x: x != "", lines))
            num_vectors = int(len(non_empty_lines) / 2)
            alpha_vectors = []
            for i in range(num_vectors):
                line_index = i * 2
                action = int(non_empty_lines[line_index])
                alpha_vector = list(map(lambda x: round(float(x), 5),
                                        list(filter(lambda x: x != '', non_empty_lines[line_index + 1].split(" ")))))
                alpha_vectors.append((action, alpha_vector))
            return alpha_vectors

    @staticmethod
    def optimal_avg_value(file_path_to_alpha_vectors: str, initial_belief: float, btr: int) -> float:
        """
        Computes the optimal average value given a set of alpha vectors

        :param file_path_to_alpha_vectors:
        :param initial_belief: the belief to compute the value for
        :param btr: the BTR constraint/horizon
        :return: the optimal average value
        """
        alpha_vectors = PomdpSolveParser.parse_alpha_vectors(file_path=file_path_to_alpha_vectors)
        b_vec: List[float] = [1.0 - initial_belief, initial_belief]
        dot_vals: List[float] = []
        for i in range(len(alpha_vectors)):
            dot_vals.append(-np.dot(b_vec, alpha_vectors[i][1][0:2]))
        min_index: int = int(np.argmin(dot_vals))
        value: float = dot_vals[min_index]
        return float(value / btr)
