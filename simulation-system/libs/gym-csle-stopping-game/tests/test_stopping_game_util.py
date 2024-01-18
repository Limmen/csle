from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil


class TestStoppingGameUtilSuite(object):
    """
    Test suite for stopping_game_util.py
    """

    def test_b1(self) -> None:
        """
        Tests the b1 function

        :return: None
        """
        assert sum(StoppingGameUtil.b1()) == 1

    def test_state_space(self) -> None:
        """
        Tests the state space function

        :return: None
        """
        assert sum(StoppingGameUtil.state_space()) == 3
        assert len(StoppingGameUtil.state_space()) == 3

    def test_defender_actions(self) -> None:
        """
                Tests the defender actions function

                :return: None
                """
        assert sum(StoppingGameUtil.defender_actions()) == 1
        assert len(StoppingGameUtil.defender_actions()) == 2

    def test_attacker_actions(self) -> None:
        """
        Tests the attacker actions function

        :return: None
        """
        assert sum(StoppingGameUtil.attacker_actions()) == 1
        assert len(StoppingGameUtil.attacker_actions()) == 2

    def test_observation_space(self) -> None:
        """
        Tests the observation space function

        :return: None
        """
        n = 6
        assert len(StoppingGameUtil.observation_space(n)) == n + 1

    def test_reward_tensor(self) -> None:
        """
        Tests the observation space function

        :return: None
        """
        l = 6
        example_reward_vector = StoppingGameUtil.reward_tensor(R_SLA=1, R_INT=3, R_COST=2, L=l, R_ST=5)
        assert example_reward_vector.shape == (l, 2, 2, 3)
