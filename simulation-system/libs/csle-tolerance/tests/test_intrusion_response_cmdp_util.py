from csle_tolerance.util.intrusion_response_cmdp_util import IntrusionResponseCmdpUtil


class TestInstrusionToleranceCmdpSuite:
    """
    Test suite for intrusion_response_cmdp_util.py
    """
    
    def test_state_space(self) -> None:
        """
        Tests the state space of the CMDP

        :return: None
        """
        assert len(IntrusionResponseCmdpUtil.state_space(2)) != 0
        assert IntrusionResponseCmdpUtil.state_space(1) is not  None
        assert IntrusionResponseCmdpUtil.state_space(0) == [0]
        assert all(isinstance(n,int) for n in IntrusionResponseCmdpUtil.state_space(3))
    
    def test_action_space(self) -> None:
        """
        Tests the action space of the CMDP

        :return: None
        """
        assert IntrusionResponseCmdpUtil.action_space() == [0,1]

    def test_cost_function(self) -> None:
        """
        Tests the cost function of the CMDP

        :return: None
        """
        s = 1
        assert IntrusionResponseCmdpUtil.cost_function(s,True) == -1.0
        assert IntrusionResponseCmdpUtil.cost_function(s,False) == 1.0
        assert isinstance(IntrusionResponseCmdpUtil.cost_function(s,False),float)

    

    


