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
