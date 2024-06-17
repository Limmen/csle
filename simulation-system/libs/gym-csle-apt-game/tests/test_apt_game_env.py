from gym_csle_apt_game.envs.apt_game_env import AptGameEnv
from gym_csle_apt_game.dao.apt_game_config import AptGameConfig
from gym_csle_apt_game.util.apt_game_util import AptGameUtil
from gym_csle_apt_game.dao.apt_game_state import AptGameState
from unittest.mock import patch, MagicMock
import csle_common.constants.constants as constants
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
import pytest
import numpy as np


class TestAptGameEnvSuite:
    """
    Test suite for apt_game_env.py
    """

    @pytest.fixture(autouse=True)
    def setup_env(self) -> None:
        """
        Sets up the configuration of the apt game

        :return: None
        """
        env_name = "test_env"
        N = 3
        p_a = 0.5
        T = AptGameUtil.transition_tensor(N, p_a)
        O = AptGameUtil.observation_space(100)
        Z = AptGameUtil.observation_tensor(100, N)
        C = AptGameUtil.cost_tensor(N)
        S = AptGameUtil.state_space(N=3)
        A1 = AptGameUtil.defender_actions()
        A2 = AptGameUtil.attacker_actions()
        b1 = AptGameUtil.b1(N=3)
        save_dir = "save_directory"
        checkpoint_traces_freq = 100
        gamma = 0.9
        self.config = AptGameConfig(
            env_name,
            T,
            O,
            Z,
            C,
            S,
            A1,
            A2,
            b1,
            N,
            p_a,
            save_dir,
            checkpoint_traces_freq,
            gamma,
        )
        self.env = AptGameEnv(self.config)

    def test_init_(self) -> None:
        """
        Tests the initializing function

        :return: None
        """
        assert self.env.config == self.config
        assert self.env.state == AptGameState(b1=self.config.b1)
        assert (
            self.env.attacker_observation_space
            == self.config.attacker_observation_space()
        )
        assert (
            self.env.defender_observation_space
            == self.config.defender_observation_space()
        )
        assert self.env.attacker_action_space == self.config.attacker_action_space()
        assert self.env.defender_action_space == self.config.defender_action_space()
        assert self.env.action_space == self.config.defender_action_space()
        assert self.env.observation_space == self.config.defender_observation_space()
        assert isinstance(self.env.traces, list)
        assert isinstance(self.env.trace, SimulationTrace)
        assert self.env.trace.simulation_env == self.config.env_name

    def test_step(self) -> None:
        """
        Tests the function for taking a step in the environment by executing the given action

        :return: None
        """
        initial_state = self.env.state.s
        action_profile = (
            0,
            (np.array([[0.5, 0.5], [0.5, 0.5], [0.4, 0.6], [0.5, 0.5]]), 1),
        )
        obs, reward, terminated, truncated, info = self.env.step(action_profile)
        assert obs[0].all() == self.env.state.defender_observation().all()
        assert obs[1] == self.env.state.attacker_observation()
        assert isinstance(terminated, bool)  # type: ignore
        assert isinstance(truncated, bool)  # type: ignore
        assert reward == (
            self.config.C[action_profile[0]][initial_state],
            -self.config.C[action_profile[0]][initial_state],
        )
        assert isinstance(info, dict)  # type: ignore

    def test_mean(self) -> None:
        """
        Tests the utility function for getting the mean of a vector

        :return: None
        """
        test_cases = [
            ([], 0),  # Test case for an empty vector
            ([5], 0),  # Test case for a vector with a single element
            ([0.2, 0.3, 0.5], 1.3),  # Test case for a vector with multiple elements
        ]
        for prob_vector, expected_mean in test_cases:
            result = AptGameEnv(self.config).mean(prob_vector)
            assert result == expected_mean

    def test_info(self) -> None:
        """
        Tests the function for adding the cumulative reward and episode length to the info dict

        :return: None
        """
        info = {} # type: ignore
        assert isinstance(self.env._info(info), dict)  # type: ignore

    def test_reset(self) -> None:
        """
        Tests the function for reseting the environment state

        :return: None
        """
        self.env.trace.attacker_rewards = [1, 2, 3]
        self.env.trace.attacker_observations = ["obs1", "obs2"]
        self.env.trace.defender_observations = ["obs1", "obs2"]
        initial_trace_count = len(self.env.traces)
        AptGameState.reset = lambda self: None # type: ignore
        initial_obs, info = self.env.reset(seed=10, soft=False, options=None)
        assert len(self.env.traces) == initial_trace_count + 1
        assert isinstance(self.env.trace, SimulationTrace)
        assert self.env.trace.simulation_env == self.config.env_name
        assert self.env.trace.attacker_observations == [initial_obs[1]]
        assert self.env.trace.defender_observations == [initial_obs[0]]
        assert info == {}

    def test_render(self) -> None:
        """
        Tests the function of rendering the environment

        :return: None
        """
        with pytest.raises(NotImplementedError):
            self.env.render()

    def test_is_defense_action_legal(self) -> None:
        """
        Tests the function of checking whether a defender action in the environment is legal or not

        :return: None
        """
        assert self.env.is_defense_action_legal(1)

    def test_is_attack_action_legal(self) -> None:
        """
        Tests the function of checking whether an attacker action in the environment is legal or not

        :return: None
        """
        assert self.env.is_attack_action_legal(1)

    def test_get_traces(self) -> None:
        """
        Tests the function of getting the list of simulation traces

        :return: None
        """
        assert self.env.get_traces() == self.env.traces

    def test_reset_traces(self) -> None:
        """
        Tests the function of resetting the list  of traces

        :return: None
        """
        self.env.traces = ["trace1", "trace2"]
        self.env.reset_traces()
        assert self.env.traces == []

    def test_checkpoint_traces(self) -> None:
        """
        Tests the function of checkpointing agent traces

        :return: None
        """

        fixed_timestamp = 123
        with patch("time.time", return_value=fixed_timestamp):
            with patch(
                "csle_common.dao.simulation_config.simulation_trace.SimulationTrace.save_traces"
            ) as mock_save_traces:
                self.env.traces = ["trace1", "trace2"]
                self.env._AptGameEnv__checkpoint_traces()
                mock_save_traces.assert_called_once_with(
                    traces_save_dir=constants.LOGGING.DEFAULT_LOG_DIR,
                    traces=self.env.traces,
                    traces_file=f"taus{fixed_timestamp}.json",
                )

    def test_set_model(self) -> None:
        """
        Tests the function of setting the model

        :return: None
        """
        mock_model = MagicMock()
        self.env.set_model(mock_model)
        assert self.env.model == mock_model

    def test_set_state(self) -> None:
        """
        Tests the function of setting the state

        :return: None
        """
        self.env.state = MagicMock()
        mock_state = MagicMock(spec=AptGameState)
        self.env.set_state(mock_state)
        assert self.env.state == mock_state

        state_int = 5
        self.env.set_state(state_int)
        assert self.env.state.s == state_int

        with pytest.raises(ValueError):
            self.env.set_state([1, 2, 3])  # type: ignore
