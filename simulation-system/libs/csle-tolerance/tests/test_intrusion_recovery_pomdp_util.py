from csle_tolerance.util.intrusion_recovery_pomdp_util import IntrusionRecoveryPomdpUtil


class TestIntrusionTolerancePomdpSuite(object):
    """
    Test suite for stopping_game_util.py
    """

    def test_initial_belief(self) -> None:
        """
        Tests the initial_belief function

        :return: None
        """
        assert sum(IntrusionRecoveryPomdpUtil.initial_belief(p_a=0.5)) == 1
