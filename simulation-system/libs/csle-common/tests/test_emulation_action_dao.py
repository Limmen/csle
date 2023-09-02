from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_config import EmulationAttackerActionConfig
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.defender.emulation_defender_action_config import EmulationDefenderActionConfig


class TestEmulationActionDaoSuite:
    """
    Test suite for emulation action data access objects (DAOs)
    """

    def test_emulation_attacker_action(self, example_emulation_attacker_action: EmulationAttackerAction) -> None:
        """
        Tests creation and dict conversion of the EmulationAttackerAction DAO

        :param example_emulation_attacker_action: an example DAO
        :return: None
        """
        assert isinstance(example_emulation_attacker_action.to_dict(), dict)
        assert isinstance(EmulationAttackerAction.from_dict(example_emulation_attacker_action.to_dict()),
                          EmulationAttackerAction)
        assert EmulationAttackerAction.from_dict(example_emulation_attacker_action.to_dict()).to_dict() == \
               example_emulation_attacker_action.to_dict()
        assert EmulationAttackerAction.from_dict(example_emulation_attacker_action.to_dict()) \
               == example_emulation_attacker_action

    def test_emulation_attacker_action_config(
            self, example_emulation_attacker_action_config: EmulationAttackerActionConfig) -> None:
        """
        Tests creation and dict conversion of the EmulationAttackerActionConfig DAO

        :param example_emulation_attacker_action: an example DAO
        :return: None
        """
        assert isinstance(example_emulation_attacker_action_config.to_dict(), dict)
        assert isinstance(EmulationAttackerActionConfig.from_dict(example_emulation_attacker_action_config.to_dict()),
                          EmulationAttackerActionConfig)
        assert EmulationAttackerActionConfig.from_dict(example_emulation_attacker_action_config.to_dict()).to_dict() == \
               example_emulation_attacker_action_config.to_dict()
        assert EmulationAttackerActionConfig.from_dict(example_emulation_attacker_action_config.to_dict()) == \
               example_emulation_attacker_action_config

    def test_emulation_defender_action(self, example_emulation_defender_action: EmulationDefenderAction) -> None:
        """
        Tests creation and dict conversion of the EmulationDefenderAction DAO

        :param example_emulation_defender_action: an example DAO
        :return: None
        """
        assert isinstance(example_emulation_defender_action.to_dict(), dict)
        assert isinstance(EmulationDefenderAction.from_dict(example_emulation_defender_action.to_dict()),
                          EmulationDefenderAction)
        assert EmulationDefenderAction.from_dict(example_emulation_defender_action.to_dict()).to_dict() == \
               example_emulation_defender_action.to_dict()
        assert EmulationDefenderAction.from_dict(example_emulation_defender_action.to_dict()) == \
               example_emulation_defender_action

    def test_emulation_defender_action_config(
            self, example_emulation_defender_action_config: EmulationDefenderActionConfig) -> None:
        """
        Tests creation and dict conversion of the EmulationDefenderActionConfig DAO

        :param example_emulation_defender_action_config: an example DAO
        :return: None
        """
        assert isinstance(example_emulation_defender_action_config.to_dict(), dict)
        assert isinstance(EmulationDefenderActionConfig.from_dict(example_emulation_defender_action_config.to_dict()),
                          EmulationDefenderActionConfig)
        assert EmulationDefenderActionConfig.from_dict(example_emulation_defender_action_config.to_dict()).to_dict() == \
               example_emulation_defender_action_config.to_dict()
        assert EmulationDefenderActionConfig.from_dict(example_emulation_defender_action_config.to_dict()) == \
               example_emulation_defender_action_config
