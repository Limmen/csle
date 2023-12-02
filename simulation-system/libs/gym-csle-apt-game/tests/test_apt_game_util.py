from gym_csle_apt_game.util.apt_game_util import AptGameUtil


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
