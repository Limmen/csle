from gym_csle_intrusion_response_game.util.intrusion_response_game_util import IntrusionResponseGameUtil
import numpy as np


class TestIntrusionResponseGameUtilSuite(object):
    """
    Test suite for stopping_game_util.py
    """

    def test_is_local_state_terminal(self) -> None:
        """
        Tests the is_local_state_terminal function

        :return: None
        """
        assert IntrusionResponseGameUtil.is_local_state_terminal(np.array([-1, -1]))
        assert not IntrusionResponseGameUtil.is_local_state_terminal(np.array([0, -1]))
        assert not IntrusionResponseGameUtil.is_local_state_terminal(np.array([-1, 0]))
        assert not IntrusionResponseGameUtil.is_local_state_terminal(np.array([0, 0]))
