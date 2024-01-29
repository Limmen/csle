from gym_csle_stopping_game.dao.stopping_game_attacker_mdp_config import StoppingGameAttackerMdpConfig
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from gym_csle_stopping_game.dao.stopping_game_defender_pomdp_config import StoppingGameDefenderPomdpConfig
from gym_csle_stopping_game.dao.stopping_game_state import StoppingGameState
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from csle_common.dao.training.policy import Policy


class TestStoppingGameDaoSuite(object):
    """
    Test suite for stopping game data access objects (DAOs)
    """

    def test_stopping_game_attacker_mdp_config(
            self, example_stopping_game_config: StoppingGameConfig, example_defender_strategy: Policy) -> None:
        """
        Tests the stopping_game_attacker_mdp_config dao

        :param example_stopping_game_config example object of StoppingGameConfig
        :param example_defender_strategy an example object of MultiThresholdStoppingPolicy
        :return: None
        """
        example_stopping_game_attacker_mdp_config = StoppingGameAttackerMdpConfig(
            env_name="test_env", stopping_game_config=example_stopping_game_config,
            defender_strategy=example_defender_strategy)
        assert isinstance(example_stopping_game_attacker_mdp_config.to_dict(), dict)
        assert isinstance(StoppingGameAttackerMdpConfig.from_dict(example_stopping_game_attacker_mdp_config.to_dict()),
                          StoppingGameAttackerMdpConfig)
        assert (StoppingGameAttackerMdpConfig.from_dict(example_stopping_game_attacker_mdp_config.to_dict()).to_dict()
                == example_stopping_game_attacker_mdp_config.to_dict())
        assert (StoppingGameAttackerMdpConfig.from_dict(example_stopping_game_attacker_mdp_config.to_dict()) ==
                example_stopping_game_attacker_mdp_config)

    def test_stopping_game_config(self, example_stopping_game_config: StoppingGameConfig) -> None:
        """
        Tests the stopping_game_config dao

        :param example_stopping_game_config example object of StoppingGameConfig
        :return: None
        """
        assert isinstance(example_stopping_game_config.to_dict(), dict)
        assert isinstance(StoppingGameConfig.from_dict(example_stopping_game_config.to_dict()),
                          StoppingGameConfig)
        assert (StoppingGameConfig.from_dict(example_stopping_game_config.to_dict()).to_dict()
                == example_stopping_game_config.to_dict())
        assert (StoppingGameConfig.from_dict(example_stopping_game_config.to_dict()) ==
                example_stopping_game_config)

    def test_stopping_game_defender_pomdp_config(self, example_stopping_game_config: StoppingGameConfig,
                                                 example_attacker_strategy: Policy) -> None:
        """
        Tests the stopping_game_defender_pomdp_config dao

        :param example_stopping_game_config example object of StoppingGameConfig
        :param example_attacker_strategy an example object of MultiThresholdStoppingPolicy
        :return: None
        """
        example_stopping_game_defender_pomdp_config = StoppingGameDefenderPomdpConfig(
            env_name="test", stopping_game_config=example_stopping_game_config,
            attacker_strategy=example_attacker_strategy)
        assert isinstance(example_stopping_game_defender_pomdp_config.to_dict(), dict)
        assert isinstance(StoppingGameDefenderPomdpConfig.from_dict(
            example_stopping_game_defender_pomdp_config.to_dict()), StoppingGameDefenderPomdpConfig)
        assert (StoppingGameDefenderPomdpConfig.from_dict
                (example_stopping_game_defender_pomdp_config.to_dict()).to_dict() ==
                example_stopping_game_defender_pomdp_config.to_dict())
        assert (StoppingGameDefenderPomdpConfig.from_dict(example_stopping_game_defender_pomdp_config.to_dict()) ==
                example_stopping_game_defender_pomdp_config)

    def test_stopping_game_state(self, example_stopping_game_util: StoppingGameUtil) -> None:
        """
        Tests the stopping_game_state dao

        :param: StoppingGameUtil example object of StoppingGameUtil
        :return: None
        """
        example_stopping_game_state = StoppingGameState(b1=example_stopping_game_util.b1(), L=1)
        assert isinstance(example_stopping_game_state.to_dict(), dict)
        assert isinstance(StoppingGameState.from_dict(
            example_stopping_game_state.to_dict()), StoppingGameState)
        assert (StoppingGameState.from_dict(
            example_stopping_game_state.to_dict()).to_dict() == example_stopping_game_state.to_dict())
        assert (StoppingGameState.from_dict(example_stopping_game_state.to_dict()) == example_stopping_game_state)
