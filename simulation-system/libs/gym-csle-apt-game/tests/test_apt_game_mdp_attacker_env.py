from gym_csle_apt_game.dao.apt_game_config import AptGameConfig
from gym_csle_apt_game.util.apt_game_util import AptGameUtil
from gym_csle_apt_game.envs.apt_game_env import AptGameEnv
from gym_csle_apt_game.envs.apt_game_mdp_attacker_env import AptGameMdpAttackerEnv
from gym_csle_apt_game.dao.apt_game_attacker_mdp_config import AptGameAttackerMdpConfig
from csle_common.dao.training.policy import Policy
from csle_common.dao.training.random_policy import RandomPolicy
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.simulation_config.action import Action
import pytest
from unittest.mock import MagicMock
import numpy as np


class TestAptGameMdpAttackerEnvSuite:
    """
    Test suite for apt_game_mdp_attacker_env.py
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
        self.defender_strategy = MagicMock(spec=Policy)
        self.attacker_mdp_config = AptGameAttackerMdpConfig(
            env_name="test_env",
            apt_game_config=self.config,
            defender_strategy=self.defender_strategy,
            apt_game_name="csle-apt-game-v1",
        )
        self.env = AptGameMdpAttackerEnv(self.attacker_mdp_config)

    def test_init_(self) -> None:
        """
        Tests the initializing function

        :return: None
        """
        assert self.env.config == self.attacker_mdp_config
        assert self.env.observation_space == self.config.attacker_observation_space()
        assert self.env.action_space == self.config.attacker_action_space()
        assert self.env.static_defender_strategy == self.defender_strategy
        assert not self.env.model
        assert not self.env.viewer

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
        attacker_mdp_config = AptGameAttackerMdpConfig(
            env_name="test_env",
            apt_game_config=self.config,
            defender_strategy=defender_strategy,
            apt_game_name="csle-apt-game-v1",
        )
        env = AptGameMdpAttackerEnv(config=attacker_mdp_config)
        env.reset()
        pi2 = env.calculate_stage_policy(o=list(env.latest_attacker_obs), a2=0)  # type: ignore
        attacker_obs, reward, terminated, truncated, info = env.step(pi2)
        assert isinstance(attacker_obs[0], float)  # type: ignore
        assert isinstance(terminated, bool)  # type: ignore
        assert isinstance(truncated, bool)  # type: ignore
        assert isinstance(reward, float)  # type: ignore
        assert isinstance(info, dict)  # type: ignore

    def test_reset(self) -> None:
        """
        Tests the function for reseting the environment state

        :return: None
        """
        info = self.env.reset()
        assert info[-1] == {}

    def test_set_model(self) -> None:
        """
        Tests the function for setting the model

        :return: None
        """
        mock_model = MagicMock()
        self.env.set_model(mock_model)
        assert self.env.model == mock_model

    def test_set_state(self) -> None:
        """
        Tests the function for setting the state

        :return: None
        """
        assert not self.env.set_state(1)  # type: ignore

    def test_calculate_stage_policy(self) -> None:
        """
        Tests the function for calculating the stage policy of a given model and observation

        :return: None
        """
        self.env.model = None
        observation = [1, 0.5]
        stage_policy = self.env.calculate_stage_policy(o=observation)
        expected_stage_policy = np.array([[1.0, 0.0], [1.0, 0.0], [0.5, 0.5]])
        assert stage_policy.all() == expected_stage_policy.all()

    def test_get_attacker_dist(self) -> None:
        """
        Tests the function for getting the attacker's action distribution based on a given observation

        :return: None
        """
        self.env.model = None
        observation = [1, 0.5, 0]
        with pytest.raises(ValueError, match="Model is None"):
            self.env._get_attacker_dist(observation)

    def test_render(self) -> None:
        """
        Tests the function for rendering the environment

        :return: None
        """
        with pytest.raises(NotImplementedError):
            self.env.render("human")

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
        assert self.env.get_traces() == AptGameEnv(self.config).traces

    def test_reset_traces(self) -> None:
        """
        Tests the function of resetting the list  of traces

        :return: None
        """
        self.env.traces = ["trace1", "trace2"]
        self.env.reset_traces()
        assert AptGameEnv(self.config).traces == []
