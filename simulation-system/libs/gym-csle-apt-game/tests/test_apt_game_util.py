from gym_csle_apt_game.util.apt_game_util import AptGameUtil
from csle_common.dao.training.multi_threshold_stopping_policy import (
    MultiThresholdStoppingPolicy,
)
from gym_csle_apt_game.dao.apt_game_config import AptGameConfig
import numpy as np


class TestAptGameUtilSuite(object):
    """
    Test suite for apt_game_util.py
    """

    def test_b1(self) -> None:
        """
        Tests the b1 function

        :return: None
        """
        assert sum(AptGameUtil.b1(N=5)) == 1

    def test_state_space(self) -> None:
        """
        Tests the state space function

        :return: None
        """
        assert sum(AptGameUtil.state_space(N=5)) == 15
        assert len(AptGameUtil.state_space(N=5)) == 6

    def test_defender_actions(self) -> None:
        """
        Tests the defender actions function

        :return: None
        """
        assert sum(AptGameUtil.defender_actions()) == 1
        assert len(AptGameUtil.defender_actions()) == 2

    def test_attacker_actions(self) -> None:
        """
        Tests the attacker actions function

        :return: None
        """
        assert sum(AptGameUtil.attacker_actions()) == 1
        assert len(AptGameUtil.attacker_actions()) == 2

    def test_observation_space(self) -> None:
        """
        Tests the observation space function

        :return: None
        """
        n = 6
        assert len(AptGameUtil.observation_space(n)) == n

    def test_transition_tensor(self, example_apt_game_util: AptGameUtil) -> None:
        """
        Tests the transition tensor function

        :param: example_apt_game_util an example object of AptGameUtil
        :return: None
        """
        example_transition_tensor = AptGameUtil.transition_tensor(N=5, p_a=0.1)
        assert example_transition_tensor.shape == (
            len(example_apt_game_util.defender_actions()),
            len(example_apt_game_util.attacker_actions()),
            len(example_apt_game_util.state_space(N=5)),
            len(example_apt_game_util.state_space(N=5)),
        )

    def test_observation_tensor(self, example_apt_game_util: AptGameUtil) -> None:
        """
        Tests the observation tensor function

        :param: example_apt_game_util an example object of AptGameUtil
        :return: None
        """
        n = 6
        example_observation_tensor = AptGameUtil.observation_tensor(
            num_observations=n, N=5
        )
        assert example_observation_tensor.shape == (
            len(example_apt_game_util.state_space(N=5)),
            n,
        )

    def test_sample_next_state(self, example_apt_game_util: AptGameUtil) -> None:
        """
        Tests the sample next state function

        :param: example_apt_game_util an example object of AptGameUtil
        :return: None
        """
        example_sample_next_state = AptGameUtil.sample_next_state(
            T=example_apt_game_util.transition_tensor(N=5, p_a=0.1),
            s=2,
            a1=1,
            a2=1,
            S=example_apt_game_util.state_space(N=5),
        )
        assert example_sample_next_state in example_apt_game_util.state_space(N=5)

    def test_sample_initial_state(self, example_apt_game_util: AptGameUtil) -> None:
        """
        Tests the sample initial state function

        :param: example_apt_game_util an example object of AptGameUtil
        :return: None
        """
        example_sample_initial_state = AptGameUtil.sample_initial_state(
            example_apt_game_util.b1(N=5)
        )
        assert example_sample_initial_state in example_apt_game_util.b1(N=5)
        assert sum(example_apt_game_util.b1(N=5)) == 1

    def test_sample_next_observation(self, example_apt_game_util: AptGameUtil) -> None:
        """
        Tests the sample next observation function

        :param: example_apt_game_util an example object of AptGameUtil
        :return: None
        """
        n = 6
        z = example_apt_game_util.observation_tensor(num_observations=n, N=5)
        O = AptGameUtil.observation_space(num_observations=n)
        example_next_obs = AptGameUtil.sample_next_observation(Z=z, s_prime=2, O=O)
        assert example_next_obs in O

    def test_bayes_filter(
        self,
        example_apt_game_util: AptGameUtil,
        example_attacker_strategy: MultiThresholdStoppingPolicy,
        example_apt_game_config: AptGameConfig,
    ) -> None:
        """
        Tests the byte filter function

        :param: example_apt_game_util an example object of AptGameUtil
        :return: None
        """
        b_prime_s_prime = AptGameUtil.bayes_filter(
            s_prime=0,
            o=0,
            a1=0,
            b=example_apt_game_util.b1(N=5),
            pi2=example_attacker_strategy.stage_policy([0, 0]),
            config=example_apt_game_config,
        )
        assert b_prime_s_prime <= 1 and b_prime_s_prime >= 0

    def test_next_belief(
        self,
        example_apt_game_config: AptGameConfig,
        example_attacker_strategy: MultiThresholdStoppingPolicy,
    ) -> None:
        """
        Tests the next_belief function

        :param: example_apt_game_config an example object of AptGameConfig
        :param: example_attacker_strategy an example object of MultiThresholdStoppingPolicy
        :param: example_apt_game_util an example object of AptGameUtil
        :return: None
        """
        pi2 = example_attacker_strategy.stage_policy([0, 0])

        example_next_belief = AptGameUtil.next_belief(
            o=0,
            a1=0,
            b=AptGameUtil.b1(N=5),
            pi2=pi2,
            config=example_apt_game_config,
            a2=1,
            s=0,
        )
        assert isinstance(example_next_belief, np.ndarray)
        assert sum(example_next_belief) == 1

    def test_sample_attacker_action(
        self, example_attacker_strategy: MultiThresholdStoppingPolicy
    ) -> None:
        """
        Tests the byte filter function

        :param: example_attacker_strategy an example object of MultiThresholdStoppingPolicy
        :return: None
        """
        example_sample_attacker_action = AptGameUtil.sample_attacker_action(
            pi2=example_attacker_strategy.stage_policy([0, 0]), s=1
        )
        assert example_sample_attacker_action in AptGameUtil.attacker_actions()

    def test_generate_transitions(self, example_apt_game_config: AptGameConfig) -> None:
        """
        Tests generate_transitions function

        :return: None
        """
        assert AptGameUtil.generate_transitions(example_apt_game_config)

    def test_generate_rewards(self, example_apt_game_config: AptGameConfig) -> None:
        """
        Tests generate_rewards function

        :return: None
        """
        assert AptGameUtil.generate_rewards(example_apt_game_config)

    def test_generate_os_posg_game_file(
        self, example_apt_game_config: AptGameConfig
    ) -> None:
        """
        Tests generate_os_posg_game_file function

        :return: None
        """
        assert AptGameUtil.generate_os_posg_game_file(example_apt_game_config)

    def test_expected_cost(self) -> None:
        """
        Tests expected_cost function

        :return: None
        """
        C = [[10.0, 20.0, 30.0], [15.0, 25.0, 35.0]]
        b = [0.2, 0.5, 0.3]
        S = [0, 1, 2]
        a1 = 0
        cost = AptGameUtil.expected_cost(C, b, S, a1)
        expected_cost_value = b[0] * C[a1][0] + b[1] * C[a1][1] + b[2] * C[a1][2]
        assert cost == expected_cost_value
