from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
from csle_attack_profiler.hmm_profiling import HMMProfiler 
import numpy as np

class TestHMMProfilerSuite:


    def test_viterbi(self):
        """
        Test the viterbi algorithm.
        Source: https://www.cis.upenn.edu/~cis2620/notes/Example-Viterbi-DNA.pdf
        """

        hidden_states = [0, 1] # States H=0 and L=1
        init_probs = [0.5, 0.5]
        trans_matrix = [
            [0.5, 0.5],  
            [0.4, 0.6]   
        ]
        
        emissions_list = [0, 1, 2, 3] # A,C,G,T
        emission_matrix = [
            [0.2, 0.3, 0.3, 0.2],  
            [0.3, 0.2, 0.2, 0.3]   
        ]
        # Consider the sequence GGCACTGAA
        seq = [2, 2, 1, 0, 1, 3, 2, 0, 0]

        # Define the list of possible emissions

        # Run the Viterbi algorithm
        path = HMMProfiler.viterbi(hidden_states, init_probs, trans_matrix, emission_matrix, seq, emissions_list)

        # Expected path: HHHLLLLLL
        expected_path = [0, 0, 0, 1, 1, 1, 1, 1, 1]
        assert np.array_equal(path, expected_path), f"Test failed! Expected: {expected_path}, Actual: {path}"

    def test_hmm_profiler(self):
        """
        Test the HMMProfiler class.
        """

        STATES = ['no_intrusion', 'A:TCP SYN (Stealth) Scan', 'A:SSH dictionary attack for username=pw', 
                                  'A:Telnet dictionary attack for username=pw', 'A:FTP dictionary attack for username=pw', 
                                  'A:Network service login','A:Install tools', 'ssh backdoor', 'A:ShellShock Explolit', 'A:CVE-2010-0426 exploit', 
                                  'A:Ping Scan', 'A:Sambacry Explolit', 'A:DVWA SQL Injection Exploit', 'A:CVE-2015-1427 exploit']
    
        TRANSITION_MATRIX = [[1/10, 3/10, 0, 0, 0, 0, 0, 0, 0, 0, 6/10, 0, 0, 0],
                         [0, 0, 0.5, 0, 0, 0, 0, 0, 0.5, 0, 0, 0, 0, 0],
                         [0, 0, 0, 1/3, 0, 2/3, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 9/11, 0, 0, 2/11, 0, 0, 0, 0],
                         [0, 0, 1/9, 0, 0, 0, 0, 1/9, 0, 0, 7/9, 0, 0, 0],
                         [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0.5, 0, 0, 0],
                         [0, 0, 1/8, 0, 0, 0, 0, 0, 0, 0, 0, 3/8, 1/4, 1/4],
                         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]]
    
        METRICS = ['alerts_weighted_by_priority', 'cpu_percent', 'default-login-attempt_alerts', 'mem_current',
                    'net_rx', 'net_tx', 'num_clients', 'num_failed_login_attempts', 'num_open_connections', 'num_processes',
                    'pids', 'priority_3_alerts', 'priority_4_alerts', 'successful-user_alerts', 'total_alerts',
                    'warning_alerts']

        statistics = EmulationStatistics.from_json_file("./statistics.json")
        statistics = EmulationStatistics.from_json_file("./statistics2.json")
        model = HMMProfiler([statistics])

        model.create_model(TRANSITION_MATRIX, STATES, METRICS[0]) 
        state_seq, observation_seq = model.generate_sequence(10, 0, 42)
        path = model.profile_sequence(observation_seq)
        converted_state_seq = model.convert_states_to_profiles(state_seq)
        
        converted_path = model.convert_states_to_profiles(path) # Delete before commit
        
        for i in range(len(path)):
            assert path[i] == state_seq[i], f"Test failed! Expected: {state_seq}, Actual: {path}"
        assert path == state_seq, "Test failed! The path is None."
        assert converted_path == converted_state_seq, f"Test failed! Expected: {converted_state_seq}, Actual: {converted_path}" # Delete before commit


        # Test the get_transition_matrix method



