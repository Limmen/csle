import pytest
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id \
    import EmulationAttackerActionId
from csle_attack_profiler.hmm_profiling import HMMProfiler
import numpy as np
import os


class TestHMMProfilerSuite:
    """
    Test suite for the HMMProfiler class.
    """

    def test_viterbi(self) -> None:
        """
        Test the viterbi algorithm.
        Source: https://www.cis.upenn.edu/~cis2620/notes/Example-Viterbi-DNA.pdf
        """

        hidden_states = [EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST,
                         EmulationAttackerActionId.PING_SCAN_HOST]  # States H=0 and L=1
        init_probs = [0.5, 0.5]
        trans_matrix = [
            [0.5, 0.5],
            [0.4, 0.6]
        ]
        
        emissions_list = [0, 1, 2, 3]  # A,C,G,T
        emission_matrix = [
            [0.2, 0.3, 0.3, 0.2],
            [0.3, 0.2, 0.2, 0.3]
        ]
        # Consider the sequence GGCACTGAA
        seq = [2, 2, 1, 0, 1, 3, 2, 0, 0]

        # Run the Viterbi algorithm
        path = HMMProfiler.viterbi(hidden_states, init_probs, trans_matrix, emission_matrix, seq, emissions_list)

        # Expected path: HHHLLLLLL
        expected_path = [0, 0, 0, 1, 1, 1, 1, 1, 1]
        assert np.array_equal(path, expected_path), f"Test failed! Expected: {expected_path}, Actual: {path}"

    @pytest.mark.skip(reason="integration test, takes too long to run")
    def test_hmm_profiler_test_data(self) -> None:
        """
        Test the HMMProfiler class with test statistics.
        """
        STATES = ['no_intrusion', 'A:CVE-2015-1427 exploit']
    
        TRANSITION_MATRIX = [[1 / 3, 2 / 3], [1 / 2, 1 / 2]]

        METRIC = 'alerts_weighted_by_priority'

        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "statistics_test.json")
        statistics = EmulationStatistics.from_json_file(file_path)

        model = HMMProfiler([statistics])

        model.create_model(TRANSITION_MATRIX, STATES, METRIC)
        state_seq, observation_seq = model.generate_sequence(2, 0, 42)
        path = model.profile_sequence(observation_seq)
        converted_path = model.convert_states_to_profiles(path[:1])

        assert path[0] == 'A:CVE-2015-1427 exploit', "Test failed! The first profiled action in path is incorrect."
        assert state_seq[0] == 'no_intrusion', "Test failed!"
        "The first profiled action in simulated state sequence is incorrect."
        if not isinstance(converted_path[0], str):
            assert converted_path[0].action_id == EmulationAttackerActionId.CVE_2015_1427_EXPLOIT, "Test failed!"
            "The converted path fails."
