from csle_tolerance.dao.intrusion_response_cmdp_config import (
    IntrusionResponseCmdpConfig,
)
from csle_tolerance.envs.intrusion_response_cmdp_env import IntrusionResponseCmdpEnv
from unittest.mock import patch, Mock
import csle_tolerance.constants.constants as env_constants
import csle_common.constants.constants as constants
import pytest


class TestInstrusionResponseCmdpEnvSuite:
    """
    Test suite for intrusion_response_pomdp_env.py
    """

    def test__init__(self) -> None:
        """
        Tests the function of initializing the environment

        :return: None
        """
        env = IntrusionResponseCmdpConfig(
            p_a=0.2,
            p_c=0.5,
            p_u=0.3,
            s_max=2,
            transition_tensor=[[[0.8, 0.2], [0.6, 0.4]]],
            cost_tensor=[0.1, 0.5],
            negate_costs=True,
            seed=1,
            states=[0, 1],
            actions=[0],
            initial_state=0,
            constraint_cost_tensor=[0.2, 0.7],
            f=1,
            epsilon_a=0.3,
            simulation_env_name="env",
            gym_env_name="gym",
            discount_factor=0.5,
        )
        assert IntrusionResponseCmdpEnv(env).t == 1
        assert IntrusionResponseCmdpEnv(env).s == env.initial_state
        assert IntrusionResponseCmdpEnv(env).traces == []

    def test_step(self) -> None:
        """
        Tests the step function (Takes a step in the environment
        by executing the given action)

        :return: None
        """
        env = IntrusionResponseCmdpConfig(
            p_a=0.2,
            p_c=0.5,
            p_u=0.3,
            s_max=2,
            transition_tensor=[[[0.8, 0.2], [0.6, 0.4]]],
            cost_tensor=[0.1, 0.5],
            negate_costs=True,
            seed=1,
            states=[0, 1],
            actions=[0],
            initial_state=0,
            constraint_cost_tensor=[0.2, 0.7],
            f=1,
            epsilon_a=0.3,
            simulation_env_name="env",
            gym_env_name="gym",
            discount_factor=0.5,
        )
        a = 0
        c = 0.1
        assert IntrusionResponseCmdpEnv(env).step(a)[1] == c
        assert not IntrusionResponseCmdpEnv(env).step(a)[2]
        assert (
            IntrusionResponseCmdpEnv(env).step(a)[4][
                env_constants.ENV_METRICS.TIME_STEP
            ]
            == 2
        )
        assert (
            IntrusionResponseCmdpEnv(env).step(a)[4][
                env_constants.ENV_METRICS.DEFENDER_ACTION
            ]
            == a
        )

    def test_reset(self) -> None:
        """
        Tests the reset function (Resets the environment state)

        :return: None
        """
        env = IntrusionResponseCmdpConfig(
            p_a=0.2,
            p_c=0.5,
            p_u=0.3,
            s_max=2,
            transition_tensor=[[[0.8, 0.2], [0.6, 0.4]]],
            cost_tensor=[0.1, 0.5],
            negate_costs=True,
            seed=1,
            states=[0, 1],
            actions=[0],
            initial_state=0,
            constraint_cost_tensor=[0.2, 0.7],
            f=1,
            epsilon_a=0.3,
            simulation_env_name="env",
            gym_env_name="gym",
            discount_factor=0.5,
        )
        assert IntrusionResponseCmdpEnv(env).reset()[0] == 0
        assert not IntrusionResponseCmdpEnv(env).reset()[1]

    def test_info(self) -> None:
        """
        Tests the function of adding the cumulative reward and episode length to the info dict

        :return: None
        """
        env = IntrusionResponseCmdpConfig(
            p_a=0.2,
            p_c=0.5,
            p_u=0.3,
            s_max=2,
            transition_tensor=[[[0.8, 0.2], [0.6, 0.4]]],
            cost_tensor=[0.1, 0.5],
            negate_costs=True,
            seed=1,
            states=[0, 1],
            actions=[0],
            initial_state=0,
            constraint_cost_tensor=[0.2, 0.7],
            f=1,
            epsilon_a=0.3,
            simulation_env_name="env",
            gym_env_name="gym",
            discount_factor=0.5,
        )
        info = {}
        assert IntrusionResponseCmdpEnv(env)._info(info) is not None

    def test_render(self) -> None:
        """
        Tests the funtion of rendering the environment

        :return: None
        """
        env = IntrusionResponseCmdpConfig(
            p_a=0.2,
            p_c=0.5,
            p_u=0.3,
            s_max=2,
            transition_tensor=[[[0.8, 0.2], [0.6, 0.4]]],
            cost_tensor=[0.1, 0.5],
            negate_costs=True,
            seed=1,
            states=[0, 1],
            actions=[0],
            initial_state=0,
            constraint_cost_tensor=[0.2, 0.7],
            f=1,
            epsilon_a=0.3,
            simulation_env_name="env",
            gym_env_name="gym",
            discount_factor=0.5,
        )
        with pytest.raises(NotImplementedError):
            IntrusionResponseCmdpEnv(env).render()

    def test_get_traces(self) -> None:
        """
        Tests the function of getting the list of simulation traces

        :return: None
        """
        env = IntrusionResponseCmdpConfig(
            p_a=0.2,
            p_c=0.5,
            p_u=0.3,
            s_max=2,
            transition_tensor=[[[0.8, 0.2], [0.6, 0.4]]],
            cost_tensor=[0.1, 0.5],
            negate_costs=True,
            seed=1,
            states=[0, 1],
            actions=[0],
            initial_state=0,
            constraint_cost_tensor=[0.2, 0.7],
            f=1,
            epsilon_a=0.3,
            simulation_env_name="env",
            gym_env_name="gym",
            discount_factor=0.5,
        )
        returned_traces = IntrusionResponseCmdpEnv(env).get_traces()
        assert not returned_traces

    def test_reset_traces(self) -> None:
        """
        Tests the function of reseting the list of traces

        :return: None
        """
        env = IntrusionResponseCmdpConfig(
            p_a=0.2,
            p_c=0.5,
            p_u=0.3,
            s_max=2,
            transition_tensor=[[[0.8, 0.2], [0.6, 0.4]]],
            cost_tensor=[0.1, 0.5],
            negate_costs=True,
            seed=1,
            states=[0, 1],
            actions=[0],
            initial_state=0,
            constraint_cost_tensor=[0.2, 0.7],
            f=1,
            epsilon_a=0.3,
            simulation_env_name="env",
            gym_env_name="gym",
            discount_factor=0.5,
        )
        assert not IntrusionResponseCmdpEnv(env).reset_traces()

    @patch("time.time")  # Mock the time.time function
    @patch(
        "csle_common.dao.simulation_config.simulation_trace.SimulationTrace.save_traces"
    )  # Mock the method
    def test_checkpoint_traces(self, mock_save_traces, mock_time) -> None:
        """
        Tests the function of checkpointing agent traces

        :param mock_save_traces: _description_
        :type mock_save_traces: _type_
        :param mock_time: _description_
        :type mock_time: _type_
        """
        env = IntrusionResponseCmdpConfig(
            p_a=0.2,
            p_c=0.5,
            p_u=0.3,
            s_max=2,
            transition_tensor=[[[0.8, 0.2], [0.6, 0.4]]],
            cost_tensor=[0.1, 0.5],
            negate_costs=True,
            seed=1,
            states=[0, 1],
            actions=[0],
            initial_state=0,
            constraint_cost_tensor=[0.2, 0.7],
            f=1,
            epsilon_a=0.3,
            simulation_env_name="env",
            gym_env_name="gym",
            discount_factor=0.5,
        )
        mock_time.return_value = 1234567890
        environment = IntrusionResponseCmdpEnv(env)
        environment._IntrusionResponseCmdpEnv__checkpoint_traces()
        mock_save_traces.assert_called_once_with(
            traces_save_dir=constants.LOGGING.DEFAULT_LOG_DIR,
            traces=environment.traces,
            traces_file=f"taus{mock_time.return_value}.json",
        )

    def test_set_model(self) -> None:
        """
        Tests the function of setting the model

        :return: None
        """
        mock_model = Mock()
        env = IntrusionResponseCmdpConfig(
            p_a=0.2,
            p_c=0.5,
            p_u=0.3,
            s_max=2,
            transition_tensor=[[[0.8, 0.2], [0.6, 0.4]]],
            cost_tensor=[0.1, 0.5],
            negate_costs=True,
            seed=1,
            states=[0, 1],
            actions=[0],
            initial_state=0,
            constraint_cost_tensor=[0.2, 0.7],
            f=1,
            epsilon_a=0.3,
            simulation_env_name="env",
            gym_env_name="gym",
            discount_factor=0.5,
        )
        environment = IntrusionResponseCmdpEnv(env)
        environment.set_model(mock_model)
        assert environment.model == mock_model

    def test_set_state(self) -> None:
        """
        Tests the function of setting the state

        :return: None
        """
        mock_state = Mock()
        env = IntrusionResponseCmdpConfig(
            p_a=0.2,
            p_c=0.5,
            p_u=0.3,
            s_max=2,
            transition_tensor=[[[0.8, 0.2], [0.6, 0.4]]],
            cost_tensor=[0.1, 0.5],
            negate_costs=True,
            seed=1,
            states=[0, 1],
            actions=[0],
            initial_state=0,
            constraint_cost_tensor=[0.2, 0.7],
            f=1,
            epsilon_a=0.3,
            simulation_env_name="env",
            gym_env_name="gym",
            discount_factor=0.5,
        )
        environment = IntrusionResponseCmdpEnv(env)
        environment.set_state(mock_state)
        assert environment.s == mock_state
