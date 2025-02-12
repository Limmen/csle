from gym_csle_apt_game.dao.apt_game_config import AptGameConfig
from gym_csle_apt_game.util.apt_game_util import AptGameUtil
from gym_csle_apt_game.envs.apt_game_env import AptGameEnv
from gym_csle_apt_game.envs.apt_game_pomdp_defender_env import AptGamePomdpDefenderEnv
from gym_csle_apt_game.dao.apt_game_defender_pomdp_config import AptGameDefenderPomdpConfig
from csle_common.dao.training.policy import Policy
from csle_common.dao.training.random_policy import RandomPolicy
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.simulation_config.action import Action
import pytest
from unittest.mock import MagicMock
import numpy as np


class TestAptGamePomdpEnvSuite:
    """
    Test suite for apt_game_pomdp_defender_env.py
    """

    @pytest.fixture(autouse=True)
    def setup_env(self) -> None:
        """
        Sets up the configuration of the apt game

        :return: None
        """
        env_name = "test_env"
        N = 2
        p_a = 0.5
        T = AptGameUtil.transition_tensor(N, p_a)
        O = AptGameUtil.observation_space(100)
        Z = AptGameUtil.observation_tensor(100, N)
        C = AptGameUtil.cost_tensor(N)
        S = AptGameUtil.state_space(N)
        A1 = AptGameUtil.defender_actions()
        A2 = AptGameUtil.attacker_actions()
        b1 = AptGameUtil.b1(N)
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
        self.attacker_strategy = MagicMock(spec=Policy)
        self.defender_pomdp_config = AptGameDefenderPomdpConfig(
            env_name="test_env",
            apt_game_config=self.config,
            attacker_strategy=self.attacker_strategy,
            apt_game_name="csle-apt-game-v1",
        )
        self.env = AptGamePomdpDefenderEnv(self.defender_pomdp_config)

    def test_init_(self) -> None:
        """
        Tests the initializing function

        :return: None
        """
        assert self.env.config == self.defender_pomdp_config
        assert self.env.observation_space == self.config.defender_observation_space()
        assert self.env.action_space == self.config.defender_action_space()
        assert self.env.static_attacker_strategy == self.attacker_strategy
        assert not self.env.viewer

    def test_step(self) -> None:
        """
        Tests the function for taking a step in the environment by executing the given action

        :return: None
        """
        attacker_stage_strategy = np.zeros((3, 2))
        attacker_stage_strategy[0][0] = 0.9
        attacker_stage_strategy[0][1] = 0.1
        attacker_stage_strategy[1][0] = 0.9
        attacker_stage_strategy[1][1] = 0.1
        attacker_stage_strategy[2] = attacker_stage_strategy[1]
        attacker_actions = list(map(lambda x: Action(id=x, descr=""), self.config.A1))
        attacker_strategy = RandomPolicy(
            actions=attacker_actions,
            player_type=PlayerType.DEFENDER,
            stage_policy_tensor=list(attacker_stage_strategy),
        )
        defender_pomdp_config = AptGameDefenderPomdpConfig(
            env_name="test_env",
            apt_game_config=self.config,
            attacker_strategy=attacker_strategy,
            apt_game_name="csle-apt-game-v1",
        )
        env = AptGamePomdpDefenderEnv(config=defender_pomdp_config)
        a1 = 1
        env.reset()
        defender_obs, reward, terminated, truncated, info = env.step(a1)
        assert len(defender_obs) == 2
        assert isinstance(terminated, bool)  # type: ignore
        assert isinstance(truncated, bool)  # type: ignore
        assert isinstance(reward, float)  # type: ignore
        assert isinstance(info, dict)  # type: ignore

    def test_reset(self) -> None:
        """
        Tests the function for reseting the environment state

        :return: None
        """
        _, info = self.env.reset()
        assert info == {}

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
