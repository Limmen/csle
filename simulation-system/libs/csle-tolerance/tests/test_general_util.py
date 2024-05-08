from csle_tolerance.util.general_util import GeneralUtil
import math
import numpy as np
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
        assert round(GeneralUtil.threshold_probability(b1,threshold,-20) == math.pow(1 + math.pow(((b1 * (1 - threshold)) / (threshold * (1 - b1))), -20), -1),1) == expected

    def test_sigmoid(self) -> None:
        """
        Tests the sigmoid function

        :return: None
        """
        x = 1
        expected = 0.7
        assert round(GeneralUtil.sigmoid(x),1) == expected

    def test_inverse_sigmoid(self) -> None:
        """
        Tests the inverse sigmoid function

        :return: None
        """
        x = 0.1
        expected = -2.2
        assert round(GeneralUtil.inverse_sigmoid(x),1) == expected

    def test_sample_next_state(self) -> None:
        """
        Tests the function of sampling the next state of a MDP or POMDP

        :return: None
        """
        transition_tensor = [[[0.6,0.4],[0.4,0.6]]]
        s = 0
        a = 0
        states = [0,1]
        state_probs = [0.6,0.4]
        expected = np.arange(0,len(states))
        assert GeneralUtil.sample_next_state(transition_tensor,s,a,states) in expected
        
    def test_register_envs(self) -> None:
        """
        Tests the utility method for registering Gymnasum environments

        :return: None
        """
        pass
