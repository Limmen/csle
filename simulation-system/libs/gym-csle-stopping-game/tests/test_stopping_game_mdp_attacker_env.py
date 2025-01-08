from gym_csle_stopping_game.envs.stopping_game_mdp_attacker_env import (
    StoppingGameMdpAttackerEnv,
)
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from gym_csle_stopping_game.dao.stopping_game_attacker_mdp_config import (
    StoppingGameAttackerMdpConfig,
)
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from gym_csle_stopping_game.envs.stopping_game_env import StoppingGameEnv
from csle_common.dao.training.policy import Policy
from csle_common.dao.training.random_policy import RandomPolicy
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.simulation_config.action import Action
import pytest
from unittest.mock import MagicMock
import numpy as np


class TestStoppingGameMdpAttackerEnvSuite:
    """
    Test suite for stopping_game_mdp_attacker_env.py
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

    def test_init_(self) -> None:
        """
        Tests the initializing function

        :return: None
        """
        # Mock the defender strategy
        defender_strategy = MagicMock(spec=Policy)
        # Create the attacker MDP configuration
        attacker_mdp_config = StoppingGameAttackerMdpConfig(
            env_name="test_env",
            stopping_game_config=self.config,
            defender_strategy=defender_strategy,
            stopping_game_name="csle-stopping-game-v1",
        )
        # Initialize the StoppingGameMdpAttackerEnv
        env = StoppingGameMdpAttackerEnv(config=attacker_mdp_config)
        assert env.config == attacker_mdp_config
        assert env.observation_space == self.config.attacker_observation_space()
        assert env.action_space == self.config.attacker_action_space()
        assert env.static_defender_strategy == defender_strategy
        # print(env.latest_defender_obs)
        # assert not env.latest_defender_obs
        # assert not env.latest_attacker_obs
        assert not env.model
        assert not env.viewer

    def test_reset(self) -> None:
        """
        Tests the function for reseting the environment state

        :return: None
        """
        defender_strategy = MagicMock(spec=Policy)
        attacker_mdp_config = StoppingGameAttackerMdpConfig(
            env_name="test_env",
            stopping_game_config=self.config,
            defender_strategy=defender_strategy,
            stopping_game_name="csle-stopping-game-v1",
        )

        env = StoppingGameMdpAttackerEnv(config=attacker_mdp_config)
        info = env.reset()
        assert info[-1] == {}

    def test_set_model(self) -> None:
        """
        Tests the function for setting the model

        :return: None
        """
        defender_strategy = MagicMock(spec=Policy)
        attacker_mdp_config = StoppingGameAttackerMdpConfig(
            env_name="test_env",
            stopping_game_config=self.config,
            defender_strategy=defender_strategy,
            stopping_game_name="csle-stopping-game-v1",
        )
        env = StoppingGameMdpAttackerEnv(config=attacker_mdp_config)
        mock_model = MagicMock()
        env.set_model(mock_model)
        assert env.model == mock_model

    def test_set_state(self) -> None:
        """
        Tests the function for setting the state

        :return: None
        """
        defender_strategy = MagicMock(spec=Policy)
        attacker_mdp_config = StoppingGameAttackerMdpConfig(
            env_name="test_env",
            stopping_game_config=self.config,
            defender_strategy=defender_strategy,
            stopping_game_name="csle-stopping-game-v1",
        )

        env = StoppingGameMdpAttackerEnv(config=attacker_mdp_config)
        assert not env.set_state(1)  # type: ignore

    def test_calculate_stage_policy(self) -> None:
        """
        Tests the function for calculating the stage policy of a given model and observation

        :return: None
        """
        defender_strategy = MagicMock(spec=Policy)
        attacker_mdp_config = StoppingGameAttackerMdpConfig(
            env_name="test_env",
            stopping_game_config=self.config,
            defender_strategy=defender_strategy,
            stopping_game_name="csle-stopping-game-v1",
        )

        env = StoppingGameMdpAttackerEnv(config=attacker_mdp_config)
        env.model = None
        observation = [1, 0.5]
        stage_policy = env.calculate_stage_policy(o=observation)
        expected_stage_policy = np.array([[1.0, 0.0], [1.0, 0.0], [0.5, 0.5]])
        assert stage_policy.all() == expected_stage_policy.all()

    def test_get_attacker_dist(self) -> None:
        """
        Tests the function for getting the attacker's action distribution based on a given observation

        :return: None
        """
        defender_strategy = MagicMock(spec=Policy)
        attacker_mdp_config = StoppingGameAttackerMdpConfig(
            env_name="test_env",
            stopping_game_config=self.config,
            defender_strategy=defender_strategy,
            stopping_game_name="csle-stopping-game-v1",
        )

        env = StoppingGameMdpAttackerEnv(config=attacker_mdp_config)
        env.model = None
        observation = [1, 0.5, 0]
        with pytest.raises(ValueError, match="Model is None"):
            env._get_attacker_dist(observation)

    def test_render(self) -> None:
        """
        Tests the function for rendering the environment

        :return: None
        """
        defender_strategy = MagicMock(spec=Policy)
        attacker_mdp_config = StoppingGameAttackerMdpConfig(
            env_name="test_env",
            stopping_game_config=self.config,
            defender_strategy=defender_strategy,
            stopping_game_name="csle-stopping-game-v1",
        )

        env = StoppingGameMdpAttackerEnv(config=attacker_mdp_config)
        with pytest.raises(NotImplementedError):
            env.render("human")

    def test_is_defense_action_legal(self) -> None:
        """
        Tests the function of checking whether a defender action in the environment is legal or not

        :return: None
        """
        defender_strategy = MagicMock(spec=Policy)
        attacker_mdp_config = StoppingGameAttackerMdpConfig(
            env_name="test_env",
            stopping_game_config=self.config,
            defender_strategy=defender_strategy,
            stopping_game_name="csle-stopping-game-v1",
        )

        env = StoppingGameMdpAttackerEnv(config=attacker_mdp_config)
        assert env.is_defense_action_legal(1)

    def test_is_attack_action_legal(self) -> None:
        """
        Tests the function of checking whether an attacker action in the environment is legal or not

        :return: None
        """
        defender_strategy = MagicMock(spec=Policy)
        attacker_mdp_config = StoppingGameAttackerMdpConfig(
            env_name="test_env",
            stopping_game_config=self.config,
            defender_strategy=defender_strategy,
            stopping_game_name="csle-stopping-game-v1",
        )

        env = StoppingGameMdpAttackerEnv(config=attacker_mdp_config)
        assert env.is_attack_action_legal(1)

    def test_get_traces(self) -> None:
        """
        Tests the function of getting the list of simulation traces

        :return: None
        """
        defender_strategy = MagicMock(spec=Policy)
        attacker_mdp_config = StoppingGameAttackerMdpConfig(
            env_name="test_env",
            stopping_game_config=self.config,
            defender_strategy=defender_strategy,
            stopping_game_name="csle-stopping-game-v1",
        )

        env = StoppingGameMdpAttackerEnv(config=attacker_mdp_config)
        assert env.get_traces() == StoppingGameEnv(self.config).traces

    def test_reset_traces(self) -> None:
        """
        Tests the function of resetting the list  of traces

        :return: None
        """
        defender_strategy = MagicMock(spec=Policy)
        attacker_mdp_config = StoppingGameAttackerMdpConfig(
            env_name="test_env",
            stopping_game_config=self.config,
            defender_strategy=defender_strategy,
            stopping_game_name="csle-stopping-game-v1",
        )

        env = StoppingGameMdpAttackerEnv(config=attacker_mdp_config)
        env.traces = ["trace1", "trace2"]
        env.reset_traces()
        assert StoppingGameEnv(self.config).traces == []

    def test_generate_random_particles(self) -> None:
        """
        Tests the funtion of generating a random list of state particles from a given observation

        :return: None
        """
        defender_strategy = MagicMock(spec=Policy)
        attacker_mdp_config = StoppingGameAttackerMdpConfig(
            env_name="test_env",
            stopping_game_config=self.config,
            defender_strategy=defender_strategy,
            stopping_game_name="csle-stopping-game-v1",
        )

        env = StoppingGameMdpAttackerEnv(config=attacker_mdp_config)
        num_particles = 10
        particles = env.generate_random_particles(o=1, num_particles=num_particles)
        assert len(particles) == num_particles
        assert all(p in [0, 1] for p in particles)

        num_particles = 0
        particles = env.generate_random_particles(o=1, num_particles=num_particles)
        assert len(particles) == num_particles

    def test_get_actions_from_particles(self) -> None:
        """
        Tests the function for pruning the set of actions based on the current particle set

        :return: None
        """
        defender_strategy = MagicMock(spec=Policy)
        attacker_mdp_config = StoppingGameAttackerMdpConfig(
            env_name="test_env",
            stopping_game_config=self.config,
            defender_strategy=defender_strategy,
            stopping_game_name="csle-stopping-game-v1",
        )

        env = StoppingGameMdpAttackerEnv(config=attacker_mdp_config)
        particles = [1, 2, 3]
        t = 0
        observation = 0
        expected_actions = [0, 1]
        assert (
            env.get_actions_from_particles(particles, t, observation)
            == expected_actions
        )

    def test_step(self) -> None:
        """
        Tests the function for taking a step in the environment by executing the given action

        :return: None
        """
        defender_stage_strategy = np.zeros((3, 2))
        defender_stage_strategy[0][0] = 0.9
        defender_stage_strategy[0][1] = 0.1
        defender_stage_strategy[1][0] = 0.9
        defender_stage_strategy[1][1] = 0.1
        defender_actions = list(map(lambda x: Action(id=x, descr=""), self.config.A1))
        defender_strategy = RandomPolicy(
            actions=defender_actions,
            player_type=PlayerType.DEFENDER,
            stage_policy_tensor=list(defender_stage_strategy),
        )
        attacker_mdp_config = StoppingGameAttackerMdpConfig(
            env_name="test_env",
            stopping_game_config=self.config,
            defender_strategy=defender_strategy,
            stopping_game_name="csle-stopping-game-v1",
        )
        env = StoppingGameMdpAttackerEnv(config=attacker_mdp_config)
        env.reset()
        pi2 = env.calculate_stage_policy(o=list(env.latest_attacker_obs), a2=0)  # type: ignore
        attacker_obs, reward, terminated, truncated, info = env.step(pi2)
        assert isinstance(attacker_obs[0], float)  # type: ignore
        assert isinstance(terminated, bool)  # type: ignore
        assert isinstance(truncated, bool)  # type: ignore
        assert isinstance(reward, float)  # type: ignore
        assert isinstance(info, dict)  # type: ignore
