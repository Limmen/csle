from gym_csle_apt_game.dao.apt_game_attacker_mdp_config import AptGameAttackerMdpConfig
from gym_csle_apt_game.dao.apt_game_config import AptGameConfig
from gym_csle_apt_game.dao.apt_game_defender_pomdp_config import AptGameDefenderPomdpConfig
from gym_csle_apt_game.dao.apt_game_state import AptGameState
from gym_csle_apt_game.util.apt_game_util import AptGameUtil
from csle_common.dao.training.policy import Policy


class TestAptGameDaoSuite(object):
    """
    Test suite for apt game data access objects (DAOs)
    """

    def test_apt_game_attacker_mdp_config(self, example_apt_game_config: AptGameConfig,
                                          example_defender_strategy: Policy) -> None:
        """
        Tests the apt_game_attacker_mdp_config dao

        :param: example_apt_game_config an example object of AptGameConfig
        :param: example_defender_strategy an example object of Policy
        :return: None
        """

        example_apt_game_attacker_mdp_config = AptGameAttackerMdpConfig(
            env_name="test_env", apt_game_config=example_apt_game_config,
            defender_strategy=example_defender_strategy)
        assert isinstance(example_apt_game_attacker_mdp_config.to_dict(), dict)
        assert isinstance(AptGameAttackerMdpConfig.from_dict(example_apt_game_attacker_mdp_config.to_dict()),
                          AptGameAttackerMdpConfig)
        assert (AptGameAttackerMdpConfig.from_dict(example_apt_game_attacker_mdp_config.to_dict()).to_dict()
                == example_apt_game_attacker_mdp_config.to_dict())
        assert (AptGameAttackerMdpConfig.from_dict(example_apt_game_attacker_mdp_config.to_dict()) ==
                example_apt_game_attacker_mdp_config)

    def test_apt_game_config(self, example_apt_game_config: AptGameConfig) -> None:
        """
        Tests the apt_game_config dao

        :param: example_apt_game_config an example object of AptGameConfig
        :return: None
        """
        assert isinstance(example_apt_game_config.to_dict(), dict)
        assert isinstance(AptGameConfig.from_dict(example_apt_game_config.to_dict()), AptGameConfig)
        assert (AptGameConfig.from_dict(example_apt_game_config.to_dict()).to_dict() ==
                example_apt_game_config.to_dict())
        assert (AptGameConfig.from_dict(example_apt_game_config.to_dict()) == example_apt_game_config)

    def test_apt_game_defender_pomdp_config(self, example_apt_game_config: AptGameConfig,
                                            example_attacker_strategy: Policy) -> None:
        """
        Tests the apt_game_defender_pomdp_config dao

        :param: example_apt_game_config an example object of AptGameConfig
        :return: None
        """
        example_apt_game_defender_pomdp_config = AptGameDefenderPomdpConfig(
            env_name="test", apt_game_config=example_apt_game_config, attacker_strategy=example_attacker_strategy)
        assert isinstance(example_apt_game_defender_pomdp_config.to_dict(), dict)
        assert isinstance(AptGameDefenderPomdpConfig.from_dict(
            example_apt_game_defender_pomdp_config.to_dict()), AptGameDefenderPomdpConfig)
        assert (AptGameDefenderPomdpConfig.from_dict
                (example_apt_game_defender_pomdp_config.to_dict()).to_dict() ==
                example_apt_game_defender_pomdp_config.to_dict())
        assert (AptGameDefenderPomdpConfig.from_dict(example_apt_game_defender_pomdp_config.to_dict()) ==
                example_apt_game_defender_pomdp_config)

    def test_game_state(self, example_apt_game_util: AptGameUtil) -> None:
        """
        Tests the apt_game_state dao

        :param: AptGameUtil example object of AptGameUtil
        :return: None
        """
        example_apt_game_state = AptGameState(b1=example_apt_game_util.b1(N=1))
        assert isinstance(example_apt_game_state.to_dict(), dict)
        assert isinstance(AptGameState.from_dict(
            example_apt_game_state.to_dict()), AptGameState)
        assert (AptGameState.from_dict(
            example_apt_game_state.to_dict()).to_dict() == example_apt_game_state.to_dict())
        assert (AptGameState.from_dict(example_apt_game_state.to_dict()) == example_apt_game_state)
