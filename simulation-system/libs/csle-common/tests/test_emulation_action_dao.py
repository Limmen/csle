from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_outcome import EmulationAttackerActionOutcome
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_common.dao.emulation_action.defender.emulation_defender_action_id import EmulationDefenderActionId
from csle_common.dao.emulation_action.defender.emulation_defender_action_outcome import EmulationDefenderActionOutcome
from csle_common.dao.emulation_action.defender.emulation_defender_action_type import EmulationDefenderActionType
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_config import EmulationAttackerActionConfig
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.defender.emulation_defender_action_config import EmulationDefenderActionConfig


class TestEmulationActionDaoSuite:
    """
    Test suite for emulation action data access objects (DAOs)
    """

    def test_emulation_attacker_action(self) -> None:
        """
        Tests creation and dict conversion of the EmulationAttackerAction DAO

        :return: None
        """
        emulation_attacker_action = EmulationAttackerAction(
            id=EmulationAttackerActionId.CONTINUE, name="test", cmds=["cmd1"],
            type=EmulationAttackerActionType.CONTINUE, descr="testtest", ips=["ip1"], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, vulnerability="test", alt_cmds=["altcmd1"],
            backdoor=False, execution_time=0.0, ts=0.0
        )
        assert isinstance(emulation_attacker_action.to_dict(), dict)
        assert isinstance(EmulationAttackerAction.from_dict(emulation_attacker_action.to_dict()),
                          EmulationAttackerAction)
        assert EmulationAttackerAction.from_dict(emulation_attacker_action.to_dict()).to_dict() == \
               emulation_attacker_action.to_dict()
        assert EmulationAttackerAction.from_dict(emulation_attacker_action.to_dict()) == emulation_attacker_action

    def test_emulation_attacker_action_config(self) -> None:
        """
        Tests creation and dict conversion of the EmulationAttackerActionConfig DAO

        :return: None
        """
        emulation_attacker_action = EmulationAttackerAction(
            id=EmulationAttackerActionId.CONTINUE, name="test", cmds=["cmd1"],
            type=EmulationAttackerActionType.CONTINUE, descr="testtest", ips=["ip1"], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, vulnerability="test", alt_cmds=["altcmd1"],
            backdoor=False, execution_time=0.0, ts=0.0
        )
        emulation_attacker_action_config = EmulationAttackerActionConfig(
            num_indices=10, actions=[emulation_attacker_action],
            nmap_action_ids=[EmulationAttackerActionId.NMAP_VULNERS_ALL],
            network_service_action_ids=[EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST],
            shell_action_ids=[EmulationAttackerActionId.CVE_2015_1427_EXPLOIT],
            nikto_action_ids=[EmulationAttackerActionId.NIKTO_WEB_HOST_SCAN],
            masscan_action_ids=[EmulationAttackerActionId.MASSCAN_ALL_SCAN],
            stopping_action_ids=[EmulationAttackerActionId.STOP, EmulationAttackerActionId.CONTINUE])
        assert isinstance(emulation_attacker_action_config.to_dict(), dict)
        assert isinstance(EmulationAttackerActionConfig.from_dict(emulation_attacker_action_config.to_dict()),
                          EmulationAttackerActionConfig)
        assert EmulationAttackerActionConfig.from_dict(emulation_attacker_action_config.to_dict()).to_dict() == \
               emulation_attacker_action_config.to_dict()
        assert EmulationAttackerActionConfig.from_dict(emulation_attacker_action_config.to_dict()) == \
               emulation_attacker_action_config

    def test_emulation_defender_action(self) -> None:
        """
        Tests creation and dict conversion of the EmulationDefenderAction DAO

        :return: None
        """
        emulation_defender_action = EmulationDefenderAction(
            id=EmulationDefenderActionId.STOP, name="testname", cmds=["cmd1"],
            type=EmulationDefenderActionType.CONTINUE, ips=["ip1", "ip2"], index=0,
            action_outcome=EmulationDefenderActionOutcome.CONTINUE, alt_cmds=["alt1"], execution_time=0.0,
            ts=0.0, descr="testdescr")
        assert isinstance(emulation_defender_action.to_dict(), dict)
        assert isinstance(EmulationDefenderAction.from_dict(emulation_defender_action.to_dict()),
                          EmulationDefenderAction)
        assert EmulationDefenderAction.from_dict(emulation_defender_action.to_dict()).to_dict() == \
               emulation_defender_action.to_dict()
        assert EmulationDefenderAction.from_dict(emulation_defender_action.to_dict()) == emulation_defender_action

    def test_emulation_defender_action_config(self) -> None:
        """
        Tests creation and dict conversion of the EmulationDefenderActionConfig DAO

        :return: None
        """
        emulation_defender_action = EmulationDefenderAction(
            id=EmulationDefenderActionId.STOP, name="testname", cmds=["cmd1"],
            type=EmulationDefenderActionType.CONTINUE, ips=["ip1", "ip2"], index=0,
            action_outcome=EmulationDefenderActionOutcome.CONTINUE, alt_cmds=["alt1"], execution_time=0.0,
            ts=0.0, descr="testdescr")
        emulation_defender_action_config = EmulationDefenderActionConfig(
            num_indices=10, actions=[emulation_defender_action],
            stopping_action_ids=[EmulationDefenderActionId.STOP, EmulationDefenderActionId.CONTINUE],
            multiple_stop_actions=[],
            multiple_stop_actions_ids=[EmulationDefenderActionId.STOP, EmulationDefenderActionId.CONTINUE])
        assert isinstance(emulation_defender_action_config.to_dict(), dict)
        assert isinstance(EmulationDefenderActionConfig.from_dict(emulation_defender_action_config.to_dict()),
                          EmulationDefenderActionConfig)
        assert EmulationDefenderActionConfig.from_dict(emulation_defender_action_config.to_dict()).to_dict() == \
               emulation_defender_action_config.to_dict()
        assert EmulationDefenderActionConfig.from_dict(emulation_defender_action_config.to_dict()) == \
               emulation_defender_action_config
