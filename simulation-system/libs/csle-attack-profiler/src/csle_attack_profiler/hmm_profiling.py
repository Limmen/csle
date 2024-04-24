from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id \
    import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_action \
    import EmulationAttackerAction
from csle_attack_profiler.attack_profiler import AttackProfiler
from typing import List
import numpy as np
import random as random
import sys
import seaborn as seaborn
import matplotlib.pyplot as plt

class HMMProfiler:
    

    def __init__(self, statistics: List[EmulationStatistics], model_name: str = None):
        """
        Class constructor

        :param statistics: The list of EmulationStatistics objects
        :param model_name: The name of the model
        """
        self.statistics = statistics
        self.transition_matrix = None
        self.emission_matrix = []
        self.hidden_states = None
        self.emission_matrix_observations = []
        self.start_state_probs = []
        self.model_name = None
        


    def create_model(self, transition_matrix: List[List[float]], hidden_states: List[str], metric: str, save_model: bool = False, location: str = ".") -> None:
        """
        Creates the HMM model based on the given transition matrix, states and metrics.
        If save = True, matrices are saved to given location

        :param transition_matrix: The transition matrix
        :param states: The list of states of the HMM (format: 'A:attack_name' or 'no_intrusion' based on emulation statistics file)
        :param metrics: The list of metrics to profile
        :param save: Whether to save the matrices to a file
        :param location: The location to save the matrices, if save = True, e.g "./resources", default is current directory

        """
        emission_matrix, emission_matrix_observations = self.get_matrices_of_observation(self.statistics, metric, hidden_states)
        self.emission_matrix = emission_matrix
        self.emission_matrix_observations = emission_matrix_observations
        self.transition_matrix = transition_matrix
        self.start_state_probs = self.calculate_initial_states(self.transition_matrix)
        self.hidden_states = hidden_states
        if save_model and location:
            np.save(f'{location}/transition_matrix.npy', transition_matrix)
            np.save(f'{location}/hidden_states.npy', hidden_states)
            np.save(f'{location}/start_state_probs.npy', self.start_state_probs) 
            np.save(f'{location}/emission_matrix_{metric}.npy', emission_matrix)
            np.save(f'{location}/emission_matrix_observations_{metric}.npy', emission_matrix_observations)

    def load_model(self, location: str, metric: str) -> None:
        """
        Loads the HMM model from the given location.

        :param location: The location of the model files, default is current directory
        """
        self.transition_matrix = np.load(f'{location}/transition_matrix.npy')
        self.hidden_states = np.load(f'{location}/hidden_states.npy')
        self.start_state_probs = np.load(f'{location}/start_state_probs.npy')
        self.emission_matrix = np.load(f'{location}/emission_matrix_{metric}.npy')
        self.emission_matrix_observations = np.load(f'{location}/emission_matrix_observations_{metric}.npy')

    def profile_sequence(self, sequence: List[int]) -> List[str]:
        """
        Profiles a sequence of observations based on the HMM model.

        :param sequence: The sequence of observations
        

        :return: The most likely sequence of states
        """
        
        path = HMMProfiler.viterbi(self.hidden_states, self.start_state_probs, self.transition_matrix, self.emission_matrix, sequence, self.emission_matrix_observations)
        profiled_sequence = []
        for i in range(len(path)):
            profiled_sequence.append(self.hidden_states[int(path[i])])

        #profiled_sequence = HMMProfiler.convert_states_to_profiles(profiled_sequence)
        
        return profiled_sequence


    def get_matrices_of_observation(self, statistics: List[EmulationStatistics], metric: str, states: List[str]) -> (List[List[float]], List[int]):
        """
        Creates the emission matrix for a given metric based on the statistics from the EmulationStatistics objects.

        :param statistics: The list of EmulationStatistics objects
        :param metric: The metric to get the emission matrix for

        :return: The emission matrix, the list of observations, the list of states
        """
        emission_matrix = []
        attack_observations = {}
        attack_observations_total_counts = {}
        all_keys = set()
        
        for stats in statistics: 
            for condition, metric_distribution in stats.conditionals_counts.items():
                action = condition.split('_')
                if action[0] == 'no':
                    action[0] = 'no_intrusion'
                if action[0] not in attack_observations:
                    # We are not intrested in the observations from 'intrusion' or 'A:Continue'
                    if action[0] == 'intrusion' or action[0] == 'A:Continue':
                        continue
                    else:
                        # Add the observations of the attack to the dictionary
                        if metric in metric_distribution: 
                            attack_observations[action[0]] = metric_distribution[metric]
                        # Sum the total counts of the observations
                            attack_observations_total_counts[action[0]] = sum(attack_observations[action[0]].values()) 
                # Aggregate the counts from the metric distribution
                else:       
                    counts_observation = metric_distribution[metric]
                    for element in counts_observation:
                        if element in attack_observations[action[0]]:
                            # Aggregate the counts if the element is already in the dictionary
                            attack_observations[action[0]][element] += counts_observation[element]
                        else:
                            attack_observations[action[0]][element] = counts_observation[element]
                    # Sum the total counts of the observations
                    attack_observations_total_counts[action[0]] += sum(attack_observations[action[0]].values())

                # Store all possible values for the observation
                if action[0] in attack_observations:
                    all_keys.update(attack_observations[action[0]])
        
        # Normalize the counts
        hm = 0
        roller = False
        for attack, _ in attack_observations.items():
            attack_observations_total_counts[attack] = sum(attack_observations[attack].values())  
            for key in all_keys:
                int_key = int(key)
                if key in attack_observations[attack]:
                    count = attack_observations[attack].pop(key, 0) 
                    attack_observations[attack][int_key] = count / attack_observations_total_counts[attack]
                else:
                    attack_observations[attack][int_key] = 0
                if not roller:
                    hm += 1
            roller = True 
            # Sort the dictionary by key
            attack_observations[attack] = dict(sorted(attack_observations[attack].items()))


        # Take any attack as the reference to get the keys
        emission_matrix_observations = []
        emission_matrix_states = []
        # Create the emission matrix
        for state in states:
            if state in attack_observations:
                # Normalize the and then append
                emission_matrix.append(list(attack_observations[state].values()))
                # Get the keys of all observations
                emission_matrix_observations = list(attack_observations[state].keys())
                emission_matrix_states.append(state)
            else:
                # LaPlace smoothing for missing observations
                num_keys = len(all_keys)
                laplace_probability = 1 / (num_keys + 2)
                laplace_sum = laplace_probability * num_keys
                laplace_probability_adj = laplace_probability / laplace_sum
                emission_matrix.append([laplace_probability_adj] * num_keys)
                emission_matrix_states.append(state)


        # Check if the sum of the probabilities is 1
        for i in range(len(emission_matrix)):
            sum_prob = round(sum(emission_matrix[i]), 10)
            if sum_prob != 1:
                print(f'Sum of probabilities for state {emission_matrix_states[i]} is {sum_prob}')

        
        return (emission_matrix, emission_matrix_observations)


    def convert_states_to_profiles(self, states: List[str]) -> List[EmulationAttackerActionId]:
        """
        Converts a list of states to a list of EmulationAttackerActionId.
        TODO: 
        Converts a list of states to a list of attacker actions, in other words make the profiling.
        So we need to create an EmulationAttackerAction and then make the call. 

        :param states: The list of states to convert

        :return: The list of EmulationAttackerActionId
        """

        new_states = [] 
        for state in states:
            if state == 'A:Continue':
                new_states.append(EmulationAttackerActionId.CONTINUE)
                """
                attacker_action = EmulationAttackerAction(
                id=EmulationAttackerActionId.CONTINUE,
                name="TCP SYN (Stealth) Scan",cmds=[],type=None,descr="CONTINUE",ips=[],index=0,action_outcome=EmulationAttackerActionOutcome.CONTINUE,backdoor=False
                )
                """
            elif state == 'A:CVE-2015-1427 exploit':
                new_states.append(EmulationAttackerActionId.CVE_2015_1427_EXPLOIT)
            elif state == 'A:DVWA SQL Injection Exploit':
                new_states.append(EmulationAttackerActionId.DVWA_SQL_INJECTION)
            elif state == 'A:Install tools':
                new_states.append(EmulationAttackerActionId.INSTALL_TOOLS)
            elif state == 'A:Network service login':
                new_states.append(EmulationAttackerActionId.NETWORK_SERVICE_LOGIN)
            elif state == 'A:Ping Scan':
                new_states.append(EmulationAttackerActionId.PING_SCAN_HOST)
            elif state == 'A:Sambacry Explolit':
                new_states.append(EmulationAttackerActionId.SAMBACRY_EXPLOIT)
            elif state == 'A:ShellShock Explolit':
                new_states.append(EmulationAttackerActionId.SHELLSHOCK_EXPLOIT)
            elif state == 'A:SSH dictionary attack for username=pw':
                new_states.append(EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST)
            elif state == 'A:FTP dictionary attack for username=pw':
                new_states.append(EmulationAttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST)
            elif state == 'A:Telnet dictionary attack for username=pw':
                new_states.append(EmulationAttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST)
            elif state == 'A:CVE-2010-0426 exploit':
                new_states.append(EmulationAttackerActionId.CVE_2010_0426_PRIV_ESC)
            elif state == 'A:TCP SYN (Stealth) Scan':
                new_states.append(EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST)
            elif state == 'ssh backdoor':
                new_states.append(EmulationAttackerActionId.SSH_BACKDOOR)
            else:
                new_states.append(state)

        return new_states
   
    def calculate_initial_states(self, transition_matrix: List[List[float]]) -> List[float]:
        """
        Calculates the initial states probabilities based on the transition matrix.

        1 / (# of states)

        :param transition_matrix: The transition matrix

        :return: The start states probabilities
        """
        start_states = []
        total_states = len(transition_matrix)
        for _ in range(total_states):
            start_states.append(1 / total_states)

        return start_states

    @staticmethod
    def viterbi(hidden_states: List[EmulationAttackerActionId], init_probs: List[float], trans_matrix: List[List[float]], emission_matrix: List[List[float]], obs: List[int], emissions_list: List[int]) -> List[float]:
        """
        Viterbi algorithm for Hidden Markov Models (HMM).

        :param hidden_states: The hidden states
        :param init_probs: The initial probabilities of the hidden states
        :param trans_matrix: The transition matrix
        :param emission_matrix: The emission matrix
        :param obs: The observation sequence
        :param emissions_list: The list of possible observations

        :return: The most likely sequence of hidden states
        """
        # Convert the emissions list to a numpy array, to use the where function
        if type(emissions_list) != np.ndarray: 
            emissions_list = np.array(emissions_list)
        # Check that the sum equals 1
        for i in range(len(emission_matrix)):
            if round(sum(emission_matrix[i]), 10) != 1:
                print(f'Sum of probabilities for state {hidden_states[i]} is not 1')
                print(f'Sum of probabilities: {sum(emission_matrix[i])}')

        # The number of hidden states
        S = len(hidden_states)
        # The number of observations
        T = len(obs)

        # The Viterbi matrix (prob) T x S matrix of zeroes
        prob = np.zeros((T, S))
        # The backpointer matrix (prev)
        prev = np.empty((T, S))
        # Initialization
        for i in range(S):
            # Fetch the index of the observation in the emission_matrix
            index, = np.where(emissions_list == obs[0])
            if index[0].size > 0: 
                prob[0][i] = init_probs[i] * emission_matrix[i][index[0]]
            else:
                print(f'Observation {obs[0]} not found in the emission matrix')
                sys.exit(1)
        

        # Recursion
        for t in range(1, T):
            index, = np.where(emissions_list == obs[t])
            for i in range(S):
                max_prob = -1
                max_state = -1
                for j in range(S):
                    new_prob = prob[t-1][j] * trans_matrix[j][i] * emission_matrix[i][index[0]]
                    if new_prob > max_prob:
                        max_prob = new_prob
                        max_state = j
                prob[t][i] = max_prob
                prev[t][i] = max_state


        path = np.zeros(T)
        path[T-1] = np.argmax(prob[T-1])
        for t in range(T-2, -1, -1):
            path[t] = prev[t+1][int(path[t+1])]

        return path


    def generate_sequence(self, intrusion_length: int, initial_state_index: int, seed: int = None) -> (List[str], List[int]):
        """
        Generates a sequence of states and corresponding observations based on the given emission matrix, and transition matrix.
        First, a sequence of observation from 'no intrusion' is generated based on the geometric distribution of the initial state.
        Then, a sequence observations and states are generated based on emission matrix and transition matrix. The length of this intrusion
        sequence is given by the intrusion_length parameter.

        :param P_obs: The emission matrix
        :param P_states: The transition matrix
        :param states: The list of states
        :param observations: The list of observations
        :param intrusion_length: The length of the intrusion
        :param initial_state: The initial state
        
        return: The sequence of states and observations
        """
        P_obs = self.emission_matrix
        P_states = self.transition_matrix
        states = self.hidden_states
        observations = self.emission_matrix_observations
        if seed:
            np.random.seed(42)
        obs_len = len(observations)
        states_len = len(states)

        # Return the geometric distribution of the initial state
        dist = np.random.geometric(p=P_states[initial_state_index][0], size=1000) 
        T_i = round(sum(dist) / len(dist))


        state_seq = [states[initial_state_index]] * T_i
        obs_seq = []
        for i in range(T_i):

            o_i = np.random.choice(obs_len, p=P_obs[initial_state_index])
            obs_seq.append(observations[o_i])

        recon_states_sum = np.sum(P_states[initial_state_index][1:])
        recon_states = P_states[initial_state_index][1:] / recon_states_sum

        intrusion_start_state = np.random.choice(states_len - 1, p=recon_states)
        intrusion_start_observation = np.random.choice(obs_len, p=P_obs[intrusion_start_state])
        state_seq.append(states[intrusion_start_state])
        obs_seq.append(observations[intrusion_start_observation])


        s_i = intrusion_start_state
        for i in range(intrusion_length):
            # si ~ Ps(si | si-1)
            s_i = np.random.choice(states_len, p=P_states[s_i])
            # oi ~ Po(oi | si)
            o_i = np.random.choice(obs_len, p=P_obs[s_i])
            state_seq.append(states[s_i])
            obs_seq.append(observations[o_i])

        #print(state_seq)
        #print(obs_seq)
        
        return state_seq, obs_seq
        

    