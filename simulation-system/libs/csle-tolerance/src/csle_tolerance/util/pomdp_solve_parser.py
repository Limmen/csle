from typing import List, Tuple


class PomdpSolveParser:

    @staticmethod
    def parse_alpha_vectors(file_path: str) -> List[Tuple[int, List[float]]]:
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
                                        list(filter(lambda x: x!= '', non_empty_lines[line_index + 1].split(" ")))))
                alpha_vectors.append((action, alpha_vector))
            return alpha_vectors
