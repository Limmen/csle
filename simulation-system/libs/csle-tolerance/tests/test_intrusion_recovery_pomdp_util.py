from csle_tolerance.util.intrusion_recovery_pomdp_util import IntrusionRecoveryPomdpUtil


class TestIntrusionTolerancePomdpSuite:
    """
    Test suite for intrusion_recovery_pomdp_util.py
    """

    def test_initial_belief(self) -> None:
        """
        Tests the initial_belief function

        :return: None
        """
        assert sum(IntrusionRecoveryPomdpUtil.initial_belief(p_a=0.5)) == 1
