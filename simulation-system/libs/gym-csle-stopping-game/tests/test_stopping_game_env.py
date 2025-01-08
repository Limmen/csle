from typing import Dict, Any
import pytest
from unittest.mock import patch, MagicMock
from gymnasium.spaces import Box, Discrete
import numpy as np
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from gym_csle_stopping_game.envs.stopping_game_env import StoppingGameEnv
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from gym_csle_stopping_game.dao.stopping_game_state import StoppingGameState
import gym_csle_stopping_game.constants.constants as env_constants
from csle_common.constants import constants


class TestStoppingGameEnvSuite:
    """
    Test suite for stopping_game_env.py
    """

    @pytest.fixture(autouse=True)
    def setup_env(self) -> None:
        """
        Sets up the configuration of the stopping game
        
        :return: None
        """
        env_name = "test_env"
        T = StoppingGameUtil.transition_tensor(L=3)
        O = StoppingGameUtil.observation_space(n=100)
        Z = StoppingGameUtil.observation_tensor(n=100)
        R = np.zeros((2, 3, 3, 3))
        S = StoppingGameUtil.state_space()
        A1 = StoppingGameUtil.defender_actions()
        A2 = StoppingGameUtil.attacker_actions()
        L = 2
        R_INT = 1
        R_COST = 2
        R_SLA = 3
        R_ST = 4
        b1 = StoppingGameUtil.b1()
        save_dir = "save_directory"
        checkpoint_traces_freq = 100
        gamma = 0.9
        compute_beliefs = True
        save_trace = True
        self.config = StoppingGameConfig(
            env_name,
            T,
            O,
            Z,
            R,
            S,
            A1,
            A2,
            L,
            R_INT,
            R_COST,
            R_SLA,
            R_ST,
            b1,
            save_dir,
            checkpoint_traces_freq,
            gamma,
            compute_beliefs,
            save_trace,
        )

    def test_stopping_game_init_(self) -> None:
        """
        Tests the initializing function

        :return: None
        """
        T = StoppingGameUtil.transition_tensor(L=3)
        O = StoppingGameUtil.observation_space(n=100)
        A1 = StoppingGameUtil.defender_actions()
        A2 = StoppingGameUtil.attacker_actions()
        L = 2
        b1 = StoppingGameUtil.b1()
        attacker_observation_space = Box(
            low=np.array([0.0, 0.0, 0.0]),
            high=np.array([float(L), 1.0, 2.0]),
            dtype=np.float64,
        )
        defender_observation_space = Box(
            low=np.array([0.0, 0.0]),
            high=np.array([float(L), 1.0]),
            dtype=np.float64,
        )
        attacker_action_space = Discrete(len(A2))
        defender_action_space = Discrete(len(A1))

        assert self.config.T.any() == T.any()
        assert self.config.O.any() == O.any()
        assert self.config.b1.any() == b1.any()
        assert self.config.L == L

        env = StoppingGameEnv(self.config)
        assert env.config == self.config
        assert env.attacker_observation_space.low.any() == attacker_observation_space.low.any()
        assert env.defender_observation_space.low.any() == defender_observation_space.low.any()
        assert env.attacker_action_space.n == attacker_action_space.n
        assert env.defender_action_space.n == defender_action_space.n
        assert env.traces == []

        with patch("gym_csle_stopping_game.dao.stopping_game_state.StoppingGameState") as MockStoppingGameState:
            MockStoppingGameState(b1=self.config.b1, L=self.config.L)
            with patch("gym_csle_stopping_game.util.stopping_game_util.StoppingGameUtil.sample_initial_state"
                       ) as MockSampleInitialState:
                MockSampleInitialState.return_value = 0
                StoppingGameEnv(self.config)
                MockSampleInitialState.assert_called()
                MockStoppingGameState.assert_called_once_with(b1=self.config.b1, L=self.config.L)

        with patch("csle_common.dao.simulation_config.simulation_trace.SimulationTrace") as MockSimulationTrace:
            MockSimulationTrace(self.config.env_name).return_value
            StoppingGameEnv(self.config)
            MockSimulationTrace.assert_called_once_with(self.config.env_name)

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
            result = StoppingGameEnv(self.config).mean(prob_vector)
            assert result == expected_mean

    def test_weighted_intrusion_prediction_distance(self) -> None:
        """
        Tests the function of computing the weighed intrusion start time prediction distance
        """
        # Test case when first_stop is before intrusion_start
        result1 = StoppingGameEnv(self.config).weighted_intrusion_prediction_distance(5, 3)
        assert result1 == 0

        # Test case when first_stop is after intrusion_start
        result2 = StoppingGameEnv(self.config).weighted_intrusion_prediction_distance(3, 5)
        assert result2 == 0.95

        # Test case when first_stop is equal to intrusion_start
        result3 = StoppingGameEnv(self.config).weighted_intrusion_prediction_distance(3, 3)
        assert result3 == 0

    def test_reset(self) -> None:
        """
        Tests the reset function for reseting the environment state

        :return: None
        """
        env = StoppingGameEnv(self.config)
        env.state = MagicMock()
        env.state.l = 10
        env.state.s = "initial_state"
        env.state.t = 0
        env.state.attacker_observation.return_value = np.array([1, 2, 3])
        env.state.defender_observation.return_value = np.array([4, 5, 6])

        env.trace = MagicMock()
        env.trace.attacker_rewards = [1]
        env.traces = []
        # Call the reset method
        observation, info = env.reset()
        # Assertions
        assert env.state.reset.called, "State's reset method was not called."
        assert env.trace.simulation_env == self.config.env_name, "Trace was not initialized correctly."
        assert observation[0].all() == np.array([4, 5, 6]).all(), "Observation does not match expected values."
        assert info[env_constants.ENV_METRICS.STOPS_REMAINING] == env.state.l, \
            "Stops remaining does not match expected value."
        assert info[env_constants.ENV_METRICS.STATE] == env.state.s, "State info does not match expected value."
        assert info[env_constants.ENV_METRICS.OBSERVATION] == 0, "Observation info does not match expected value."
        assert info[env_constants.ENV_METRICS.TIME_STEP] == env.state.t, "Time step info does not match expected value."

        # Check if trace was appended correctly
        if len(env.trace.attacker_rewards) > 0:
            assert env.traces[-1] == env.trace, "Trace was not appended correctly."

    def test_render(self) -> None:
        """
        Tests the function of rendering the environment

        :return: None
        """
        with pytest.raises(NotImplementedError):
            StoppingGameEnv(self.config).render()

    def test_is_defense_action_legal(self) -> None:
        """
        Tests the function of checking whether a defender action in the environment is legal or not

        :return: None
        """
        assert StoppingGameEnv(self.config).is_defense_action_legal(1)

    def test_is_attack_action_legal(self) -> None:
        """
        Tests the function of checking whether an attacker action in the environment is legal or not

        :return: None
        """
        assert StoppingGameEnv(self.config).is_attack_action_legal(1)

    def test_get_traces(self) -> None:
        """
        Tests the function of getting the list of simulation traces

        :return: None
        """
        assert StoppingGameEnv(self.config).get_traces() == StoppingGameEnv(self.config).traces

    def test_reset_traces(self) -> None:
        """
        Tests the function of resetting the list  of traces

        :return: None
        """
        env = StoppingGameEnv(self.config)
        env.traces = ["trace1", "trace2"]
        env.reset_traces()
        assert env.traces == []

    def test_checkpoint_traces(self) -> None:
        """
        Tests the function of checkpointing agent traces

        :return: None
        """
        env = StoppingGameEnv(self.config)
        fixed_timestamp = 123
        with patch("time.time", return_value=fixed_timestamp):
            with patch(
                    "csle_common.dao.simulation_config.simulation_trace.SimulationTrace.save_traces"
            ) as mock_save_traces:
                env.traces = ["trace1", "trace2"]
                env._StoppingGameEnv__checkpoint_traces()
                mock_save_traces.assert_called_once_with(
                    traces_save_dir=constants.LOGGING.DEFAULT_LOG_DIR,
                    traces=env.traces,
                    traces_file=f"taus{fixed_timestamp}.json",
                )

    def test_set_model(self) -> None:
        """
        Tests the function of setting the model

        :return: None
        """
        env = StoppingGameEnv(self.config)
        mock_model = MagicMock()
        env.set_model(mock_model)
        assert env.model == mock_model

    def test_set_state(self) -> None:
        """
        Tests the function of setting the state

        :return: None
        """
        env = StoppingGameEnv(self.config)
        env.state = MagicMock()

        mock_state = MagicMock(spec=StoppingGameState)
        env.set_state(mock_state)
        assert env.state == mock_state

        state_int = 5
        env.set_state(state_int)
        assert env.state.s == state_int
        assert env.state.l == self.config.L

        state_tuple = (3, 7)
        env.set_state(state_tuple)
        assert env.state.s == state_tuple[0]
        assert env.state.l == state_tuple[1]

        with pytest.raises(ValueError):
            env.set_state([1, 2, 3])  # type: ignore

    def test_is_state_terminal(self) -> None:
        """
        Tests the function of checking whether a given state is terminal or not

        :return: None
        """
        env = StoppingGameEnv(self.config)
        env.state = MagicMock()

        mock_state = MagicMock(spec=StoppingGameState)
        mock_state.s = 2
        assert env.is_state_terminal(mock_state)
        mock_state.s = 1
        assert not env.is_state_terminal(mock_state)
        state_int = 2
        assert env.is_state_terminal(state_int)
        state_int = 1
        assert not env.is_state_terminal(state_int)
        state_tuple = (2, 5)
        assert env.is_state_terminal(state_tuple)
        state_tuple = (1, 5)
        assert not env.is_state_terminal(state_tuple)

        with pytest.raises(ValueError):
            env.is_state_terminal([1, 2, 3])  # type: ignore

    def test_get_observation_from_history(self) -> None:
        """
        Tests the function of getting a hidden observation based on a history

        :return: None
        """
        env = StoppingGameEnv(self.config)
        history = [1, 2, 3, 4, 5]
        pi2 = np.array([0.1, 0.9])
        l = 3
        observation = env.get_observation_from_history(history, pi2, l)
        assert observation == [5]

        history = []
        with pytest.raises(ValueError, match="History must not be empty"):
            env.get_observation_from_history(history, pi2, l)

    def test_generate_random_particles(self) -> None:
        """
        Tests the funtion of generating a random list of state particles from a given observation

        :return: None
        """
        env = StoppingGameEnv(self.config)
        num_particles = 10
        particles = env.generate_random_particles(o=1, num_particles=num_particles)
        assert len(particles) == num_particles
        assert all(p in [0, 1] for p in particles)

        num_particles = 0
        particles = env.generate_random_particles(o=1, num_particles=num_particles)
        assert len(particles) == num_particles

    def test_step(self) -> None:
        """
        Tests the funtion of taking a step in the environment by executing  the given action

        :return: None
        """
        env = StoppingGameEnv(self.config)
        with patch("gym_csle_stopping_game.util.stopping_game_util.StoppingGameUtil.sample_next_state",
                   return_value=2):
            with patch("gym_csle_stopping_game.util.stopping_game_util.StoppingGameUtil.sample_next_observation",
                       return_value=1):
                with patch("gym_csle_stopping_game.util.stopping_game_util.StoppingGameUtil.next_belief",
                           return_value=np.array([0.3, 0.7, 0.0])):
                    action_profile = (
                        1,
                        (
                            np.array(
                                [[0.2, 0.8], [0.6, 0.4], [0.5, 0.5]]
                            ),
                            2,
                        ),
                    )
                    observations, rewards, terminated, truncated, info = env.step(
                        action_profile
                    )
                    assert observations[0].all() == np.array([1, 0.7]).all(), "Incorrect defender observations"
                    assert observations[1].all() == np.array([1, 2, 3]).all(), "Incorrect attacker observations"
                    assert rewards == (0, 0)
                    assert not terminated
                    assert not truncated
        
    def test_info(self) -> None:
        """
        Tests the function of adding the cumulative reward and episode length to the info dict
        
        :return: None
        """
        env = StoppingGameEnv(self.config)
        env.trace = MagicMock()
        env.trace.defender_rewards = [1, 2]
        env.trace.attacker_actions = [0, 1]
        env.trace.defender_actions = [0, 1]
        env.trace.states = [0, 1]
        env.trace.infrastructure_metrics = [0, 1]
        info: Dict[str, Any] = {}
        updated_info = env._info(info)
        assert updated_info[env_constants.ENV_METRICS.RETURN] == sum(env.trace.defender_rewards)
