from unittest.mock import patch, Mock
from csle_tolerance.envs.intrusion_recovery_pomdp_env import IntrusionRecoveryPomdpEnv
from csle_tolerance.dao.intrusion_recovery_pomdp_config import (
    IntrusionRecoveryPomdpConfig,
)
import csle_tolerance.constants.constants as env_constants
import csle_common.constants.constants as constants
import numpy as np
import pytest
from typing import Dict, Any


class TestInstrusionRecoveryPomdpEnvSuite:
    """
    Test suite for intrusion_recovery_pomdp_env.py
    """

    def test__init__(self) -> None:
        """
        Tests the function of initializing the environment

        :return: None
        """
        config = IntrusionRecoveryPomdpConfig(
            eta=0.1,
            p_a=0.2,
            p_c_1=0.2,
            p_c_2=0.3,
            p_u=0.3,
            BTR=1,
            negate_costs=True,
            seed=1,
            discount_factor=0.5,
            states=[0, 1],
            actions=[0],
            observations=[0, 1],
            cost_tensor=[[0.1, 0.5], [0.5, 0.6]],
            observation_tensor=[[0.8, 0.2], [0.4, 0.6]],
            transition_tensor=[[[0.8, 0.2], [0.6, 0.4]]],
            b1=[1, 0],
            T=3,
            simulation_env_name="env",
            gym_env_name="gym",
            max_horizon=np.inf,
        )
        assert IntrusionRecoveryPomdpEnv(config).t == 1
        assert IntrusionRecoveryPomdpEnv(config).s == 0
        assert IntrusionRecoveryPomdpEnv(config).o == 0

    def test_step(self) -> None:
        """
        Tests the step function (Takes a step in the environment
        by executing the given action)

        :return: None
        """
        config = IntrusionRecoveryPomdpConfig(
            eta=0.1,
            p_a=0.2,
            p_c_1=0.2,
            p_c_2=0.3,
            p_u=0.3,
            BTR=1,
            negate_costs=True,
            seed=1,
            discount_factor=0.5,
            states=[0, 1],
            actions=[0],
            observations=[0, 1],
            cost_tensor=[[0.1, 0.5], [0.5, 0.6]],
            observation_tensor=[[0.8, 0.2], [0.4, 0.6]],
            transition_tensor=[[[0.8, 0.2], [0.6, 0.4]]],
            b1=[1, 0],
            T=3,
            simulation_env_name="env",
            gym_env_name="gym",
            max_horizon=np.inf,
        )
        a = 0
        c = 0.1

        assert IntrusionRecoveryPomdpEnv(config).step(a)[0][0] == 2
        assert IntrusionRecoveryPomdpEnv(config).step(a)[1] == c
        assert (
            IntrusionRecoveryPomdpEnv(config).step(a)[4][
                env_constants.ENV_METRICS.DEFENDER_ACTION
            ]
            == 0
        )
        assert (
            IntrusionRecoveryPomdpEnv(config).step(a)[4][
                env_constants.ENV_METRICS.TIME_STEP
            ]
            == 2
        )

    def test_reset(self) -> None:
        """
        Tests the reset function (Resets the environment state)

        :return: None
        """
        config = IntrusionRecoveryPomdpConfig(
            eta=0.1,
            p_a=0.2,
            p_c_1=0.2,
            p_c_2=0.3,
            p_u=0.3,
            BTR=1,
            negate_costs=True,
            seed=1,
            discount_factor=0.5,
            states=[0, 1],
            actions=[0],
            observations=[0, 1],
            cost_tensor=[[0.1, 0.5], [0.5, 0.6]],
            observation_tensor=[[0.8, 0.2], [0.4, 0.6]],
            transition_tensor=[[[0.8, 0.2], [0.6, 0.4]]],
            b1=[1, 0],
            T=3,
            simulation_env_name="env",
            gym_env_name="gym",
            max_horizon=np.inf,
        )
        assert IntrusionRecoveryPomdpEnv(config).reset()[0][0] == 1
        assert IntrusionRecoveryPomdpEnv(config).reset()[0][1] == 0
        assert IntrusionRecoveryPomdpEnv(config).reset()[0][2] == 0

    def test_info(self) -> None:
        """
        Tests the function of adding the cumulative reward and episode length to the info dict

        :return: None
        """
        config = IntrusionRecoveryPomdpConfig(
            eta=0.1,
            p_a=0.2,
            p_c_1=0.2,
            p_c_2=0.3,
            p_u=0.3,
            BTR=1,
            negate_costs=True,
            seed=1,
            discount_factor=0.5,
            states=[0, 1],
            actions=[0],
            observations=[0, 1],
            cost_tensor=[[0.1, 0.5], [0.5, 0.6]],
            observation_tensor=[[0.8, 0.2], [0.4, 0.6]],
            transition_tensor=[[[0.8, 0.2], [0.6, 0.4]]],
            b1=[1, 0],
            T=3,
            simulation_env_name="env",
            gym_env_name="gym",
            max_horizon=np.inf,
        )
        info: Dict[str, Any] = {}
        with pytest.raises(IndexError):
            assert IntrusionRecoveryPomdpEnv(config)._info(info) is not None

    def test_render(self) -> None:
        """
        Tests the function of rendering the environment.

        :return: None
        """
        config = IntrusionRecoveryPomdpConfig(
            eta=0.1,
            p_a=0.2,
            p_c_1=0.2,
            p_c_2=0.3,
            p_u=0.3,
            BTR=1,
            negate_costs=True,
            seed=1,
            discount_factor=0.5,
            states=[0, 1],
            actions=[0],
            observations=[0, 1],
            cost_tensor=[[0.1, 0.5], [0.5, 0.6]],
            observation_tensor=[[0.8, 0.2], [0.4, 0.6]],
            transition_tensor=[[[0.8, 0.2], [0.6, 0.4]]],
            b1=[1, 0],
            T=3,
            simulation_env_name="env",
            gym_env_name="gym",
            max_horizon=np.inf,
        )
        with pytest.raises(NotImplementedError):
            IntrusionRecoveryPomdpEnv(config).render()

    def test_get_traces(self) -> None:
        """
        Tests the function of getting the list of simulation traces

        :return: None
        """
        config = IntrusionRecoveryPomdpConfig(
            eta=0.1,
            p_a=0.2,
            p_c_1=0.2,
            p_c_2=0.3,
            p_u=0.3,
            BTR=1,
            negate_costs=True,
            seed=1,
            discount_factor=0.5,
            states=[0, 1],
            actions=[0],
            observations=[0, 1],
            cost_tensor=[[0.1, 0.5], [0.5, 0.6]],
            observation_tensor=[[0.8, 0.2], [0.4, 0.6]],
            transition_tensor=[[[0.8, 0.2], [0.6, 0.4]]],
            b1=[1, 0],
            T=3,
            simulation_env_name="env",
            gym_env_name="gym",
            max_horizon=np.inf,
        )
        returned_traces = IntrusionRecoveryPomdpEnv(config).get_traces()
        assert not returned_traces

    def test_reset_traces(self) -> None:
        """
        Tests the function of reseting the list of traces

        :return: None
        """
        config = IntrusionRecoveryPomdpConfig(
            eta=0.1,
            p_a=0.2,
            p_c_1=0.2,
            p_c_2=0.3,
            p_u=0.3,
            BTR=1,
            negate_costs=True,
            seed=1,
            discount_factor=0.5,
            states=[0, 1],
            actions=[0],
            observations=[0, 1],
            cost_tensor=[[0.1, 0.5], [0.5, 0.6]],
            observation_tensor=[[0.8, 0.2], [0.4, 0.6]],
            transition_tensor=[[[0.8, 0.2], [0.6, 0.4]]],
            b1=[1, 0],
            T=3,
            simulation_env_name="env",
            gym_env_name="gym",
            max_horizon=np.inf,
        )
        assert not IntrusionRecoveryPomdpEnv(config).reset_traces()

    @patch("time.time")  # Mock the time.time function
    @patch(
        "csle_common.dao.simulation_config.simulation_trace.SimulationTrace.save_traces"
    )  # Mock the method
    def test_checkpoint_traces(self, mock_save_traces, mock_time) -> None:
        """
        Tests the function of checkpointing agent traces

        :return: None
        """
        config = IntrusionRecoveryPomdpConfig(
            eta=0.1,
            p_a=0.2,
            p_c_1=0.2,
            p_c_2=0.3,
            p_u=0.3,
            BTR=1,
            negate_costs=True,
            seed=1,
            discount_factor=0.5,
            states=[0, 1],
            actions=[0],
            observations=[0, 1],
            cost_tensor=[[0.1, 0.5], [0.5, 0.6]],
            observation_tensor=[[0.8, 0.2], [0.4, 0.6]],
            transition_tensor=[[[0.8, 0.2], [0.6, 0.4]]],
            b1=[1, 0],
            T=3,
            simulation_env_name="env",
            gym_env_name="gym",
            max_horizon=np.inf,
        )
        mock_time.return_value = 1234567890
        environment = IntrusionRecoveryPomdpEnv(config)
        environment._IntrusionRecoveryPomdpEnv__checkpoint_traces()
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
        config = IntrusionRecoveryPomdpConfig(
            eta=0.1,
            p_a=0.2,
            p_c_1=0.2,
            p_c_2=0.3,
            p_u=0.3,
            BTR=1,
            negate_costs=True,
            seed=1,
            discount_factor=0.5,
            states=[0, 1],
            actions=[0],
            observations=[0, 1],
            cost_tensor=[[0.1, 0.5], [0.5, 0.6]],
            observation_tensor=[[0.8, 0.2], [0.4, 0.6]],
            transition_tensor=[[[0.8, 0.2], [0.6, 0.4]]],
            b1=[1, 0],
            T=3,
            simulation_env_name="env",
            gym_env_name="gym",
            max_horizon=np.inf,
        )
        environment = IntrusionRecoveryPomdpEnv(config)
        environment.set_model(mock_model)
        assert environment.model == mock_model

    def test_set_state(self) -> None:
        """
        Tests the function of setting the state

        :return: None
        """
        mock_state = Mock()
        config = IntrusionRecoveryPomdpConfig(
            eta=0.1,
            p_a=0.2,
            p_c_1=0.2,
            p_c_2=0.3,
            p_u=0.3,
            BTR=1,
            negate_costs=True,
            seed=1,
            discount_factor=0.5,
            states=[0, 1],
            actions=[0],
            observations=[0, 1],
            cost_tensor=[[0.1, 0.5], [0.5, 0.6]],
            observation_tensor=[[0.8, 0.2], [0.4, 0.6]],
            transition_tensor=[[[0.8, 0.2], [0.6, 0.4]]],
            b1=[1, 0],
            T=3,
            simulation_env_name="env",
            gym_env_name="gym",
            max_horizon=np.inf,
        )
        environment = IntrusionRecoveryPomdpEnv(config)
        environment.set_state(mock_state)
        assert environment.s == mock_state
