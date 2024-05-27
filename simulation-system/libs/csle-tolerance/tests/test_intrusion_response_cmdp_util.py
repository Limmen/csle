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
        assert IntrusionResponseCmdpUtil.state_space(1) is not None
        assert IntrusionResponseCmdpUtil.state_space(0) == [0]
        assert all(isinstance(n, int) for n in IntrusionResponseCmdpUtil.state_space(3))

    def test_action_space(self) -> None:
        """
        Tests the action space of the CMDP

        :return: None
        """
        assert IntrusionResponseCmdpUtil.action_space() == [0, 1]

    def test_cost_function(self) -> None:
        """
        Tests the cost function of the CMDP

        :return: None
        """
        s = 1
        assert IntrusionResponseCmdpUtil.cost_function(s, True) == -1.0
        assert IntrusionResponseCmdpUtil.cost_function(s, False) == 1.0
        assert isinstance(IntrusionResponseCmdpUtil.cost_function(s, False), float)
        assert isinstance(IntrusionResponseCmdpUtil.cost_function(s, True), float)

    def test_cost_tensor(self) -> None:
        """
        Tests the function of creating a tensor with the costs of the CMDP

        :return: None
        """
        states = [0, 1, 2, 3]
        expected = [-0.0, -1.0, -2.0, -3.0]
        assert IntrusionResponseCmdpUtil.cost_tensor(states, True) == expected
        assert IntrusionResponseCmdpUtil.cost_tensor(states, False) == [
            -item for item in expected
        ]

    def test_constraint_cost_function(self) -> None:
        """
        Tests the constraint cost function of the CMDP

        :return: None
        """
        states = [1, 2]
        f = 5
        expected = [0.0, 0.0]
        assert (
            IntrusionResponseCmdpUtil.constraint_cost_function(states[0], f)
            == expected[0]
        )
        assert (
            IntrusionResponseCmdpUtil.constraint_cost_function(states[1], f)
            == expected[1]
        )

    def test_constraint_cost_tensor(self) -> None:
        """
        Tests the function of creating a tensor with the constrained costs of the CMDP

        :return: None
        """
        states = [1, 2]
        f = 5
        expected = [0.0, 0.0]
        assert IntrusionResponseCmdpUtil.constraint_cost_tensor(states, f) == expected

    def test_delta_function(self) -> None:
        """
        Tests the delta function that gives the probability of the change in the number of the healthy nodes

        :return: None
        """
        s = 1
        s_max = 2
        p_a = 0.2
        p_c = 0.5
        p_u = 0.7
        delta = 1
        expected = 1.35
        assert (
            round(
                IntrusionResponseCmdpUtil.delta_function(
                    s, p_a, p_c, p_u, delta, s_max
                ),
                2,
            )
            == expected
        )

    def test_transition_function(self) -> None:
        """
        Tests the transition function of the CMDP

        :return: None
        """
        s = 0
        s_prime = 1
        a = 1
        s_max = 2
        p_a = 0.2
        p_c = 0.3
        p_u = 0.5
        delta = s_prime - a - s
        assert (
            IntrusionResponseCmdpUtil.delta_function(s, p_a, p_c, p_u, delta, s_max)
            == 3
        )

    def test_transition_tensor(self) -> None:
        """
        Tests the transition tensor function of the CMDP

        :return: None
        """
        states = [0, 1]
        actions = [0]
        s_max = 2
        p_a = 0.2
        p_c = 0.3
        p_u = 0.5
        expected = [[[3 / 5, 2 / 5], [2 / 5, 3 / 5]]]
        transition_tensor = IntrusionResponseCmdpUtil.transition_tensor(
            states, actions, p_a, p_c, p_u, s_max
        )
        for i in range(len(transition_tensor)):
            for j in range(len(transition_tensor[i])):
                for k in range(len(transition_tensor[i][j])):
                    transition_tensor[i][j][k] = round(transition_tensor[i][j][k], 1)
        assert transition_tensor == expected
