from csle_tolerance.util.general_util import GeneralUtil
import numpy as np
import pytest_mock


class TestIntrusionToleranceGeneralSuite:
    """
    Test suite for general_util.py
    """

    def test_threshold_probability(self) -> None:
        """
        Tests the functuon of returning the probability of taking an action given a belief and a threshold

        :return: None
        """
        b1 = 0.5
        threshold = 0.3
        expected = 1
        assert (
            round(GeneralUtil.threshold_probability(b1, threshold, -20), 1) == expected
        )

    def test_sigmoid(self) -> None:
        """
        Tests the sigmoid function

        :return: None
        """
        x = 1
        expected = 0.7
        assert round(GeneralUtil.sigmoid(x), 1) == expected

    def test_inverse_sigmoid(self) -> None:
        """
        Tests the inverse sigmoid function

        :return: None
        """
        x = 0.1
        expected = -2.2
        assert round(GeneralUtil.inverse_sigmoid(x), 1) == expected

    def test_sample_next_state(self) -> None:
        """
        Tests the function of sampling the next state of a MDP or POMDP

        :return: None
        """
        transition_tensor = [[[0.6, 0.4], [0.4, 0.6]]]
        s = 0
        a = 0
        states = [0, 1]
        expected = np.arange(0, len(states))
        assert (
            GeneralUtil.sample_next_state(transition_tensor, s, a, states) in expected
        )

    def test_register_envs(self, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the utility method for registering Gymnasum environments

        :return: None
        """
        mocked_register = mocker.MagicMock()
        mocker.patch(
            "gymnasium.envs.registration.register", return_value=mocked_register
        )
        mocked_register.configure_mock(**{"__enter__.return_value": None})
        return_value = GeneralUtil.register_envs()
        assert return_value is None
