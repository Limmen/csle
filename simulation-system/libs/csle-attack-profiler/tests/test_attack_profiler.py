from csle_common.dao.emulation_action.attacker.emulation_attacker_action \
    import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id \
    import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_outcome \
    import EmulationAttackerActionOutcome
from csle_attack_profiler.attack_profiler import AttackProfiler


class TestAttackProfilerSuite:
    """
    Test suite for attack_profiler.py
    """

    # Test case for get_attack_profile returns the attack profile of the actions
    def test_get_attack_profile(self) -> None:
        
        # Create an instance of EmulationAttackerAction
        attacker_action = EmulationAttackerAction(
            id=EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST,
            name="TCP SYN (Stealth) Scan",
            cmds=[],
            type=None,
            descr="TCP_SYN_STEALTH_SCAN_HOST",
            ips=[],
            index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE,
            backdoor=False
        )

        # Call the method under test
        result = AttackProfiler.get_attack_profile(attacker_action)

        # Assertions
        assert result.techniques_tactics == {'Active Scanning': ['reconnaissance'], 
                                             'Gather Victim Host Information': ['reconnaissance'], 
                                             'Network Service Discovery': ['discovery']} 
        assert result.mitigations == {'Active Scanning': ['Pre-compromise'],
                                      'Gather Victim Host Information': ['Pre-compromise'],
                                      'Network Service Discovery': ['Disable or Remove Feature or Program',
                                                                    'Network Intrusion Prevention',
                                                                    'Network Segmentation']}
        assert result.data_sources == {'Active Scanning': ['Network Traffic: Network Traffic Flow', 'Network Traffic: Network Traffic Content'],
                                       'Gather Victim Host Information': ['Internet Scan: Response Content'],
                                       'Network Service Discovery': ['Network Traffic: Network Traffic Flow', 'Command: Command Execution', 'Cloud Service: Cloud Service Enumeration']}
        assert result.subtechniques == {}


    # Test case for get_attack_profile returns an empty attack profile
    def test_get_attack_profile_error(self) -> None:

        # Create an instance of EmulationAttackerAction (invalid one)
        attacker_action = EmulationAttackerAction(
            id="NONE",
            name="test",
            cmds=[],
            type=None,
            descr="test",
            ips=[],
            index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE,
            backdoor=False
        )

        result = AttackProfiler.get_attack_profile(attacker_action)

        assert result.techniques_tactics == {}
        assert result.mitigations == {}
        assert result.data_sources == {}
        assert result.subtechniques == {}


    # Test case for all ActionIds
    def test_attack_profile_all_actionid(self) -> None:

        # Loop over all the EmulationAttackerActionId
        for action_id in EmulationAttackerActionId:
            # Create an instance of EmulationAttackerAction
            attacker_action = EmulationAttackerAction(
                id=action_id,
                name="test",
                cmds=[],
                type=None,
                descr="test",
                ips=[],
                index=0,
                action_outcome=EmulationAttackerActionOutcome.CONTINUE,
                backdoor=False
            )

            result = AttackProfiler.get_attack_profile(attacker_action)

            if action_id == EmulationAttackerActionId.CONTINUE or action_id == EmulationAttackerActionId.STOP:
                assert result.techniques_tactics == {}
                assert result.mitigations == {}
                assert result.data_sources == {}
                assert result.subtechniques == {}
            else:
                # Assert that each tactic, mitigation, and data source is not empty and is related to a technique
                assert result.techniques_tactics != {}
                assert result.mitigations != {}
                assert result.data_sources != {} # Gather Victim Network Information
                # Assert that each mitigation is related to a technique
                for technique in result.mitigations:
                    assert result.techniques_tactics[technique]
                # Assert that each data source is related to a technique
                for technique in result.data_sources:
                    assert result.techniques_tactics[technique]
                # Assert that each subtechnique is related to a technique
                for technique in result.subtechniques:
                    assert result.techniques_tactics[technique]
