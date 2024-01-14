from gym_csle_stopping_game.dao.stopping_game_attacker_mdp_config import StoppingGameAttackerMdpConfig
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
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
