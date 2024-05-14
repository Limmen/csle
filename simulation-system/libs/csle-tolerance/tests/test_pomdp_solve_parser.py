from csle_tolerance.util.pomdp_solve_parser import PomdpSolveParser
import pytest
import tempfile
import numpy as np


class TestInstrusionTolerancePomdpSolveParserSuite:
    """
    Test suite for pomdp_solve_parser.py
    """

    def test_parse_alpha_vectors(self) -> None:
        """
        Tests the function of parsing alpha vectors from a given file location

        :return: None
        """
        # test for a scenario where the file does not exist
        with pytest.raises(FileNotFoundError):
            file_path = "file.txt"
            PomdpSolveParser.parse_alpha_vectors(file_path)
        # test case for correct parsing
        file_content = "0\n0.1 0.2 0.3\n1\n0.4 0.5 0.6"
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write(file_content)
            f.flush()
            file_path = f.name
            result = PomdpSolveParser.parse_alpha_vectors(file_path)
            expected = [(0, [0.1, 0.2, 0.3]), (1, [0.4, 0.5, 0.6])]
            assert result == expected
        # test case for incorrect file format
        file_content = "Invalid content"
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write(file_content)
            f.flush()
            file_path = f.name
            result = PomdpSolveParser.parse_alpha_vectors(file_path)
            assert result == []

    def test_optimal_avg_value(self) -> None:
        """
        Tests the function of computing the optimal average value given a set of alpha vectors

        :return: None
        """
        alpha_vectors_content = "0\n0.1 0.2 0.3\n1\n0.4 0.5 0.6"
        initial_belief = 0.5
        btr = 10
        with tempfile.NamedTemporaryFile(mode="w") as f:
            f.write(alpha_vectors_content)
            f.flush()
            result = PomdpSolveParser.optimal_avg_value(f.name, initial_belief, btr)
        expected = -0.45 / btr
        assert np.isclose(result, expected)
