from csle_tolerance.util.intrusion_recovery_pomdp_util import IntrusionRecoveryPomdpUtil
from csle_tolerance.dao.intrusion_recovery_pomdp_config import (
    IntrusionRecoveryPomdpConfig,
)
from csle_tolerance.dao.intrusion_recovery_game_config import (
    IntrusionRecoveryGameConfig,
)
import numpy as np
import pytest


class TestIntrusionTolerancePomdpSuite:
    """
    Test suite for intrusion_recovery_pomdp_util.py
    """

    def test__state_space(self) -> None:
        """
        Tests the state space of the POMDP

        :return: None
        """
        assert (isinstance(item, int) for item in IntrusionRecoveryPomdpUtil.state_space())
        assert IntrusionRecoveryPomdpUtil.state_space() is not None
        assert IntrusionRecoveryPomdpUtil.state_space() == [0, 1, 2]

    def test_initial_belief(self) -> None:
        """
        Tests the initial_belief function

        :return: None
        """
        assert sum(IntrusionRecoveryPomdpUtil.initial_belief()) == 1

    def test_action_space(self) -> None:
        """
        Tests the action space of the POMDP

        :return: None
        """
        assert (isinstance(item, int) for item in IntrusionRecoveryPomdpUtil.action_space())
        assert IntrusionRecoveryPomdpUtil.action_space() is not None
        assert IntrusionRecoveryPomdpUtil.action_space() == [0, 1]

    def test_observation_space(self) -> None:
        """
        Tests the observation space of the POMDP

        :return: None
        """
        num_observation = 3
        expected = [0, 1, 2]
        assert IntrusionRecoveryPomdpUtil.observation_space(num_observation) == expected

    def test_cost_function(self) -> None:
        """
        Tests the cost function of the POMDP

        :return: None
        """
        s = 1
        a = 0
        eta = 0.5
        negate = False
        assert IntrusionRecoveryPomdpUtil.cost_function(s, a, eta, negate) == 0.5

    def test_cost_tensor(self) -> None:
        """
        Tests the function of creating a tensor with the costs of the POMDP

        :return: None
        """
        eta = 0.5
        states = [0, 1]
        actions = [0]
        negate = False
        expected = [[0, 0.5]]
        assert IntrusionRecoveryPomdpUtil.cost_tensor(eta, states, actions, negate) == expected

    def test_observation_function(self) -> None:
        """
        Tests the observation function of the POMDP

        :return: None
        """
        s = 1
        o = 1
        num_observations = 2
        assert round(IntrusionRecoveryPomdpUtil.observation_function(s, o, num_observations), 1)

    def test_observation_tensor(self) -> None:
        """
        Tests the function of creating a tensor with observation probabilities

        :return: None
        """
        states = [0, 1]
        observations = [0, 1]
        expected = [[0.8, 0.2], [0.4, 0.6]]
        obs_tensor = IntrusionRecoveryPomdpUtil.observation_tensor(states, observations)
        for i in range(len(obs_tensor)):
            for j in range(len(obs_tensor[i])):
                obs_tensor[i][j] = round(obs_tensor[i][j], 1)
            assert sum(obs_tensor[i]) == 1
        assert obs_tensor == expected

    def test_transition_function(self) -> None:
        """
        Tests the transition function of the POMDP

        :return: None
        """
        s = 0
        s_prime = 1
        a = 0
        p_a = 0.2
        p_c_1 = 0.1
        p_c_2 = 0.2
        p_u = 0.5
        assert (round(IntrusionRecoveryPomdpUtil.transition_function(s, s_prime, a, p_a, p_c_1, p_c_2, p_u), 1) == 0.2)

    def test_transition_function_game(self) -> None:
        """
        Tests the transition function of the POSG

        :return: None
        """
        s = 0
        s_prime = 1
        a1 = 0
        a2 = 1
        p_a = 0.2
        p_c_1 = 0.1
        assert (round(IntrusionRecoveryPomdpUtil.transition_function_game(s, s_prime, a1, a2, p_a, p_c_1), 2) == 0.18)

    def test_transition_tensor(self) -> None:
        """
        Tests the function of creating  a tensor with the transition probabilities of the POMDP

        :return: None
        """
        states = [0, 1, 2]
        actions = [0]
        p_a = 0.2
        p_c_1 = 0.1
        p_c_2 = 0.2
        p_u = 0.5
        expected = [[[0.7, 0.2, 0.1], [0.4, 0.4, 0.2], [0, 0, 1.0]]]
        transition_tensor = IntrusionRecoveryPomdpUtil.transition_tensor(states, actions, p_a, p_c_1, p_c_2, p_u)
        for i in range(len(transition_tensor)):
            for j in range(len(transition_tensor[i])):
                for k in range(len(transition_tensor[i][j])):
                    transition_tensor[i][j][k] = round(transition_tensor[i][j][k], 1)
        assert transition_tensor == expected
        states = [0, 1]
        with pytest.raises(AssertionError):
            IntrusionRecoveryPomdpUtil.transition_tensor(states, actions, p_a, p_c_1, p_c_2, p_u)

    def test_transition_tensor_game(self) -> None:
        """
        Tests the function of creating a tensor with the transition probabilities of the POSG

        :return: None
        """
        states = [0, 1, 2]
        defender_actions = [0, 1]
        attacker_actions = [0, 1]
        p_a = 0.5
        p_c_1 = 0.3
        result = IntrusionRecoveryPomdpUtil.transition_tensor_game(states, defender_actions, attacker_actions, p_a,
                                                                   p_c_1)
        assert len(result) == len(defender_actions)
        assert all(len(a1) == len(attacker_actions) for a1 in result)
        assert all(len(a2) == len(states) for a1 in result for a2 in a1)
        assert all(len(s) == len(states) for a1 in result for a2 in a1 for s in a2)
        assert result[0][1][0][0] == (1 - p_a) * (1 - p_c_1)
        assert result[1][0][1][1] == 0
        assert result[1][1][2][2] == 1.0
        assert result[0][1][0][1] == (1 - p_c_1) * p_a
        assert result[0][0][0][2] == p_c_1

    def test_sample_initial_state(self) -> None:
        """
        Tests the function of sampling the initial state

        :return: None
        """
        b1 = [0.2, 0.8]
        assert isinstance(IntrusionRecoveryPomdpUtil.sample_initial_state(b1), int)
        assert IntrusionRecoveryPomdpUtil.sample_initial_state(b1) <= len(b1)
        assert IntrusionRecoveryPomdpUtil.sample_initial_state(b1) >= 0
        b1 = [1.0, 0]
        assert IntrusionRecoveryPomdpUtil.sample_initial_state(b1) == 0
        b1 = [0.0, 1.0]
        assert IntrusionRecoveryPomdpUtil.sample_initial_state(b1) == 1

    def test_sampe_next_observation(self) -> None:
        """
        Tests the function of sampling the next observation

        :return: None
        """
        observation_tensor = [[0.8, 0.2], [0.4, 0.6]]
        s_prime = 1
        observations = [0, 1]
        assert isinstance(IntrusionRecoveryPomdpUtil.sample_next_observation(observation_tensor, s_prime, observations),
                          int)

    def test_bayes_filter(self) -> None:
        """
        Tests the function of a bayesian filter to computer b[s_prime] of the POMDP

        :return: None
        """
        s_prime = 1
        o = 0
        a = 0
        b = [0.2, 0.8]
        states = [0, 1]
        observations = [0, 1]
        observation_tensor = [[0.8, 0.2], [0.4, 0.6]]
        transition_tensor = [[[0.6, 0.4], [0.1, 0.9]]]
        b_prime_s_prime = 0.7
        assert (round(IntrusionRecoveryPomdpUtil.bayes_filter(s_prime, o, a, b, states, observations,
                                                              observation_tensor, transition_tensor), 1)
                == b_prime_s_prime)

    def test_p_o_given_b_a1_a2(self) -> None:
        """
        Tests the function of computing P[o|a,b] of the POMDP

        :return: None
        """
        o = 0
        b = [0.2, 0.8]
        a = 0
        states = [0, 1]
        observation_tensor = [[0.8, 0.2], [0.4, 0.6]]
        transition_tensor = [[[0.6, 0.4], [0.1, 0.9]]]
        expected = 0.5
        assert (round(IntrusionRecoveryPomdpUtil.p_o_given_b_a1_a2(o, b, a, states, transition_tensor,
                                                                   observation_tensor), 1) == expected)

    def test_next_belief(self) -> None:
        """
        Tests the funtion of computing the next belief using a Bayesian filter

        :return: None
        """
        o = 0
        a = 0
        b = [0.2, 0.8]
        states = [0, 1]
        observations = [0, 1]
        observation_tensor = [[0.8, 0.2], [0.4, 0.6]]
        transition_tensor = [[[0.3, 0.7], [0.6, 0.4]]]
        assert (round(sum(IntrusionRecoveryPomdpUtil.next_belief(o, a, b, states, observations, observation_tensor,
                                                                 transition_tensor)), 1) == 1)

    def test_pomdp_solver_file(self) -> None:
        """
        Tests the function of getting the POMDP environment specification

        :return: None
        """

        assert (IntrusionRecoveryPomdpUtil.pomdp_solver_file(
            IntrusionRecoveryPomdpConfig(eta=0.1, p_a=0.2, p_c_1=0.2, p_c_2=0.3, p_u=0.3, BTR=1, negate_costs=True,
                                         seed=1, discount_factor=0.5, states=[0, 1], actions=[0], observations=[0, 1],
                                         cost_tensor=[[0.1, 0.5], [0.5, 0.6]],
                                         observation_tensor=[[0.8, 0.2], [0.4, 0.6]],
                                         transition_tensor=[[[0.8, 0.2], [0.6, 0.4]]], b1=[0.3, 0.7], T=3,
                                         simulation_env_name="env", gym_env_name="gym", max_horizon=np.inf))
                is not None)

    def test_sample_next_state_game(self) -> None:
        """
        Tests the function of sampling the next observation

        :return: None
        """
        np.random.seed(40)
        transition_tensor = [
            [
                [[0.1, 0.9], [0.7, 0.3], [0.5, 0.5]],
                [[0.2, 0.8], [0.6, 0.4], [0.4, 0.6]],
            ],
            [
                [[0.3, 0.7], [0.8, 0.2], [0.6, 0.4]],
                [[0.4, 0.6], [0.5, 0.5], [0.3, 0.7]],
            ],
        ]

        s = 0
        a1 = 0
        a2 = 0

        count = [0, 0]
        for _ in range(1000):
            s_prime = IntrusionRecoveryPomdpUtil.sample_next_state_game(
                transition_tensor, s, a1, a2
            )
            count[s_prime] += 1
        assert 850 <= count[1] <= 950
        assert 50 <= count[0] <= 150

    def test_generate_transitions(self) -> None:
        """
        Tests the function of generating the transition rows of the POSG config file of HSVI

        :return: None
        """
        dto = IntrusionRecoveryGameConfig(
            eta=0.5,
            p_a=0.8,
            p_c_1=0.1,
            BTR=10,
            negate_costs=True,
            seed=123,
            discount_factor=0.9,
            states=[0, 1, 2],
            actions=[0, 1],
            observations=[0, 1],
            cost_tensor=[[1, 2], [3, 4]],
            observation_tensor=[[0.6, 0.4], [0.5, 0.5]],
            transition_tensor=[
                [
                    [
                        [0.1, 0.2, 0.7],
                        [0.3, 0.4, 0.3],
                        [0.2, 0.2, 0.6],
                    ],
                    [
                        [0.2, 0.3, 0.5],
                        [0.4, 0.3, 0.3],
                        [0.3, 0.3, 0.4],
                    ],
                ],
                [
                    [
                        [0.5, 0.3, 0.2],
                        [0.3, 0.5, 0.2],
                        [0.4, 0.3, 0.3],
                    ],
                    [
                        [0.3, 0.4, 0.3],
                        [0.5, 0.4, 0.1],
                        [0.2, 0.5, 0.3],
                    ],
                ],
            ],
            b1=[0.1, 0.9],
            T=100,
            simulation_env_name="sim_env",
            gym_env_name="gym_env",
            max_horizon=1000,
        )
        assert IntrusionRecoveryPomdpUtil.generate_transitions(dto)[0] == "0 0 0 0 0 0.06"

    def test_generate_rewards(self) -> None:
        """
        Tests the function of generating the reward rows of the POSG config file of HSVI

        :return: None
        """
        dto = IntrusionRecoveryGameConfig(
            eta=0.5,
            p_a=0.8,
            p_c_1=0.1,
            BTR=10,
            negate_costs=True,
            seed=123,
            discount_factor=0.9,
            states=[0, 1, 2],
            actions=[0, 1],
            observations=[0, 1],
            cost_tensor=[[1, 2, 3], [4, 5, 6]],
            observation_tensor=[[0.6, 0.4], [0.5, 0.5]],
            transition_tensor=[
                [
                    [
                        [0.1, 0.2, 0.7],
                        [0.3, 0.4, 0.3],
                        [0.2, 0.2, 0.6],
                    ],
                    [
                        [0.2, 0.3, 0.5],
                        [0.4, 0.3, 0.3],
                        [0.3, 0.3, 0.4],
                    ],
                ],
                [
                    [
                        [0.5, 0.3, 0.2],
                        [0.3, 0.5, 0.2],
                        [0.4, 0.3, 0.3],
                    ],
                    [
                        [0.3, 0.4, 0.3],
                        [0.5, 0.4, 0.1],
                        [0.2, 0.5, 0.3],
                    ],
                ],
            ],
            b1=[0.1, 0.9],
            T=100,
            simulation_env_name="sim_env",
            gym_env_name="gym_env",
            max_horizon=1000,
        )
        assert IntrusionRecoveryPomdpUtil.generate_rewards(dto)[0] == "0 0 0 -1"

    def test_generate_os_posg_game_file(self) -> None:
        """
        Tests the generate_os_posg_game function

        :return: None
        """

        states = [0, 1, 2]
        actions = [0, 1]
        observations = [0, 1]

        transition_tensor = [
            [
                [
                    [0.1, 0.2, 0.7],
                    [0.3, 0.4, 0.3],
                    [0.2, 0.2, 0.6],
                ],
                [
                    [0.2, 0.3, 0.5],
                    [0.4, 0.3, 0.3],
                    [0.3, 0.3, 0.4],
                ],
            ],
            [
                [
                    [0.5, 0.3, 0.2],
                    [0.3, 0.5, 0.2],
                    [0.4, 0.3, 0.3],
                ],
                [
                    [0.3, 0.4, 0.3],
                    [0.5, 0.4, 0.1],
                    [0.2, 0.5, 0.3],
                ],
            ],
        ]

        observation_tensor = [
            [0.6, 0.4],
            [0.5, 0.5],
        ]

        cost_tensor = [
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
        ]

        game_config = IntrusionRecoveryGameConfig(
            eta=0.5,
            p_a=0.8,
            p_c_1=0.1,
            BTR=10,
            negate_costs=True,
            seed=123,
            discount_factor=0.9,
            states=states,
            actions=actions,
            observations=observations,
            cost_tensor=cost_tensor,
            observation_tensor=observation_tensor,
            transition_tensor=transition_tensor,
            b1=[0.1, 0.9],
            T=100,
            simulation_env_name="sim_env",
            gym_env_name="gym_env",
            max_horizon=1000,
        )

        game_file_str = IntrusionRecoveryPomdpUtil.generate_os_posg_game_file(
            game_config
        )

        expected_game_description = "3 1 2 2 2 72 12 0.9"
        expected_state_descriptions = ["0 0", "1 0", "2 0"]
        expected_player_1_actions = ["WAIT", "RECOVER"]
        expected_player_2_actions = ["FALSEALARM", "ATTACK"]
        expected_obs_descriptions = ["o_0", "o_1"]
        expected_player_2_legal_actions = ["0 1", "0 1", "0 1"]
        expected_player_1_legal_actions = ["0 1"]

        output_lines = game_file_str.split("\n")

        assert (output_lines[0] == expected_game_description), f"Game description mismatch: {output_lines[0]}"
        assert (output_lines[1:4] == expected_state_descriptions), f"State descriptions mismatch: {output_lines[1:4]}"
        assert (output_lines[4:6] == expected_player_1_actions), f"Player 1 actions mismatch: {output_lines[4:6]}"
        assert (output_lines[6:8] == expected_player_2_actions), f"Player 2 actions mismatch: {output_lines[6:8]}"
        assert (output_lines[8:10] == expected_obs_descriptions), \
            f"Observation descriptions mismatch: {output_lines[8:10]}"
        assert (output_lines[10:13] == expected_player_2_legal_actions), \
            f"Player 2 legal actions mismatch: {output_lines[10:13]}"
        assert (output_lines[13:14] == expected_player_1_legal_actions), \
            f"Player 1 legal actions mismatch: {output_lines[13:14]}"
