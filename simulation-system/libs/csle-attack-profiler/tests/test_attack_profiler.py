import pytest
from csle_common.dao.emulation_action.attacker.emulation_attacker_action \
    import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id \
    import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_outcome \
    import EmulationAttackerActionOutcome
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_attack_profiler.attack_profiler import AttackProfiler
from csle_attack_profiler.dao.tactics import Tactics
from csle_attack_profiler.dao.attack_graph import AttackGraph


class TestAttackProfilerSuite:
    """
    Test suite for attack_profiler.py
    """

    @pytest.mark.skip(reason="integration test, takes too long to run")
    def test_get_attack_profile(self) -> None:
        """
        Test case for get_attack_profile returns the attack profile for a given attacker action
        """
        # Create an instance of EmulationAttackerAction
        attacker_action = EmulationAttackerAction(
            id=EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST,
            name="TCP SYN (Stealth) Scan",
            cmds=[],
            type=EmulationAttackerActionType.RECON,
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
        assert result.data_sources == {'Active Scanning': ['Network Traffic: Network Traffic Flow',
                                                           'Network Traffic: Network Traffic Content'],
                                       'Gather Victim Host Information': ['Internet Scan: Response Content'],
                                       'Network Service Discovery': ['Network Traffic: Network Traffic Flow',
                                                                     'Command: Command Execution',
                                                                     'Cloud Service: Cloud Service Enumeration']}
        assert result.subtechniques == {}

    @pytest.mark.skip(reason="integration test, takes too long to run")
    def test_get_attack_profile_error(self) -> None:
        """
        Test case for get_attack_profile returns an empty attack profile for an invalid attacker action
        """
        # Create an instance of EmulationAttackerAction (invalid one)
        attacker_action = EmulationAttackerAction(
            id=EmulationAttackerActionId.CONTINUE,
            name="test",
            cmds=[],
            type=EmulationAttackerActionType.RECON,
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

    @pytest.mark.skip(reason="integration test, takes too long to run")
    def test_attack_profile_all_actionid(self) -> None:
        """
        Test case for get_attack_profile returns the attack profile for all the EmulationAttackerActionId
        """
        # Loop over all the EmulationAttackerActionId
        for action_id in EmulationAttackerActionId:
            # Create an instance of EmulationAttackerAction
            attacker_action = EmulationAttackerAction(
                id=action_id,
                name="test",
                cmds=[],
                type=EmulationAttackerActionType.RECON,
                descr="test",
                ips=[],
                index=0,
                action_outcome=EmulationAttackerActionOutcome.CONTINUE,
                backdoor=False
            )

            result = AttackProfiler.get_attack_profile(attacker_action)
            # Logging for test purposes
            print("Action ID: ", action_id)
            if action_id == EmulationAttackerActionId.CONTINUE or action_id == EmulationAttackerActionId.STOP:
                assert result.techniques_tactics == {}
                assert result.mitigations == {}
                assert result.data_sources == {}
                assert result.subtechniques == {}
            else:
                # Assert that each tactic, mitigation, and data source is not empty and is related to a technique
                assert result.techniques_tactics != {}
                assert result.mitigations != {}
                assert result.data_sources != {}  # Gather Victim Network Information
                # Assert that each mitigation is related to a technique
                for technique in result.mitigations:
                    assert result.techniques_tactics[technique]
                # Assert that each data source is related to a technique
                for technique in result.data_sources:
                    assert result.techniques_tactics[technique]
                # Assert that each subtechnique is related to a technique
                for technique in result.subtechniques:
                    assert result.techniques_tactics[technique]

    @pytest.mark.skip(reason="integration test, takes too long to run")
    def test_attack_profiler_sequence_no_graph(self) -> None:
        """
        Test the get_attack_profile_sequence method without providing an attack graph
        """
        attacker_action = EmulationAttackerAction(
            id=EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST,
            name="TCP SYN (Stealth) Scan",
            cmds=[],
            type=EmulationAttackerActionType.RECON,
            descr="TCP_SYN_STEALTH_SCAN_HOST",
            ips=[],
            index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE,
            backdoor=False
        )

        attacker_action = [attacker_action]
        # Call the method under test
        result = AttackProfiler.get_attack_profile_sequence(attacker_action)

        assert result[0].techniques_tactics == {'Active Scanning': ['reconnaissance'],
                                                'Gather Victim Host Information': ['reconnaissance']}
        assert result[0].mitigations == {'Active Scanning': ['Pre-compromise'],
                                         'Gather Victim Host Information': ['Pre-compromise']}
        assert result[0].data_sources == {'Active Scanning': [
            'Network Traffic: Network Traffic Flow',
            'Network Traffic: Network Traffic Content'],
            'Gather Victim Host Information': ['Internet Scan: Response Content']}
        assert result[0].subtechniques == {}

    @pytest.mark.skip(reason="integration test, takes too long to run")
    def test_attack_profiler_sequence_graph(self) -> None:
        """
        Test get_attack_profile_sequence method providing an attack graph Graph:
        Reconnaisance
        Credential ->  Initial Access
        
        """
        # Partial sequence attack graph
        attack_graph = AttackGraph()
        attack_graph.add_node(Tactics.RECONNAISSANCE, node_id=1)
        attack_graph.add_node(Tactics.CREDENTIAL_ACCESS, node_id=2)
        attack_graph.add_node(Tactics.INITIAL_ACCESS, node_id=3)
        attack_graph.add_edge(Tactics.RECONNAISSANCE, 1, Tactics.CREDENTIAL_ACCESS, 2)
        attack_graph.add_edge(Tactics.RECONNAISSANCE, 1, Tactics.INITIAL_ACCESS, 3)
        attack_graph.add_edge(Tactics.CREDENTIAL_ACCESS, 2, Tactics.INITIAL_ACCESS, 3)

        attacker_action1 = EmulationAttackerAction(
            id=EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST,
            name="TCP SYN (Stealth) Scan",
            cmds=[],
            type=EmulationAttackerActionType.RECON,
            descr="TCP_SYN_STEALTH_SCAN_HOST",
            ips=[],
            index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE,
            backdoor=False
        )
        attacker_action2 = EmulationAttackerAction(
            id=EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST,
            name="SSH Dictionary attack",
            cmds=[],
            type=EmulationAttackerActionType.EXPLOIT,
            descr="SSH Dictionary attack",
            ips=[],
            index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE,
            backdoor=False
        )

        attacker_action3 = EmulationAttackerAction(
            id=EmulationAttackerActionId.NETWORK_SERVICE_LOGIN,
            name="Login",
            cmds=[],
            type=EmulationAttackerActionType.POST_EXPLOIT,
            descr="Login",
            ips=[],
            index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE,
            backdoor=False
        )

        attacker_action = [attacker_action1, attacker_action2, attacker_action3]

        # Call the method under test
        result = AttackProfiler.get_attack_profile_sequence(attacker_action, attack_graph)

        assert result[0].techniques_tactics == {'Active Scanning': ['reconnaissance'],
                                                'Gather Victim Host Information': ['reconnaissance']}
        assert result[0].mitigations == {'Active Scanning': ['Pre-compromise'],
                                         'Gather Victim Host Information': ['Pre-compromise']}
        assert result[0].data_sources == {'Active Scanning': [
            'Network Traffic: Network Traffic Flow',
            'Network Traffic: Network Traffic Content'],
            'Gather Victim Host Information': ['Internet Scan: Response Content']}
        assert result[0].subtechniques == {}

        assert result[1].techniques_tactics == {'Brute Force': ['credential-access'],
                                                'Valid Accounts': [
                                                    'defense-evasion', 'persistence', 'privilege-escalation',
                                                    'initial-access']}
        assert result[1].mitigations == {'Brute Force': [
            'User Account Management', 'Account Use Policies',
            'Multi-factor Authentication', 'Password Policies'],
            'Valid Accounts': ['Password Policies', 'User Account Management',
                               'Privileged Account Management',
                               'Application Developer Guidance',
                               'User Training', 'Active Directory Configuration',
                               'Account Use Policies']}
        assert result[1].data_sources == {'Brute Force': [
            'User Account: User Account Authentication',
            'Command: Command Execution',
            'Application Log: Application Log Content'],
            'Valid Accounts': ['Logon Session: Logon Session Creation',
                               'User Account: User Account Authentication',
                               'Logon Session: Logon Session Metadata']}
        assert result[1].subtechniques == {'Brute Force': 'Credential Stuffing', 'Valid Accounts': 'Default Accounts'}
        assert result[2].techniques_tactics == {'External Remote Services': ['persistence',
                                                                             'initial-access'],
                                                'Valid Accounts': ['defense-evasion',
                                                                   'persistence',
                                                                   'privilege-escalation',
                                                                   'initial-access']}
        assert result[2].mitigations == {'External Remote Services': [
            'Network Segmentation',
            'Disable or Remove Feature or Program',
            'Limit Access to Resource Over Network',
            'Multi-factor Authentication'],
            'Valid Accounts': [
                'Password Policies', 'User Account Management', 'Privileged Account Management',
                'Application Developer Guidance', 'User Training', 'Active Directory Configuration',
                'Account Use Policies']}
        assert result[2].data_sources == {'External Remote Services': [
            'Network Traffic: Network Connection Creation', 'Network Traffic: Network Traffic Flow',
            'Logon Session: Logon Session Metadata', 'Application Log: Application Log Content',
            'Network Traffic: Network Traffic Content'],
            'Valid Accounts': ['Logon Session: Logon Session Creation', 'User Account: User Account Authentication',
                               'Logon Session: Logon Session Metadata']}
        assert result[2].subtechniques == {}

    @pytest.mark.skip(reason="integration test, takes too long to run")
    def test_attack_profiler_sequence_graph2(self) -> None:
        """
        Test get_attack_profile_sequence method providing an attack graph, Graph:
        Recon /    \
        Initial   Execution
        /
        {Execution, Command and Control, Defense Evasion, Lateral Movement}
        """
        # Partial sequence attack graph
        attack_graph = AttackGraph()
        # Nodes
        attack_graph.add_node(Tactics.RECONNAISSANCE, node_id=1)
        attack_graph.add_node(Tactics.EXECUTION, node_id=2)
        attack_graph.add_node(Tactics.INITIAL_ACCESS, node_id=3)
        attack_graph.add_node(Tactics.EXECUTION, node_id=4)
        attack_graph.add_node(Tactics.COMMAND_AND_CONTROL, node_id=5)
        attack_graph.add_node(Tactics.DEFENSE_EVASION, node_id=6)
        attack_graph.add_node(Tactics.LATERAL_MOVEMENT, node_id=7)
        # Edges
        attack_graph.add_edge(Tactics.RECONNAISSANCE, 1, Tactics.INITIAL_ACCESS, 3)
        attack_graph.add_edge(Tactics.RECONNAISSANCE, 1, Tactics.EXECUTION, 2)
        attack_graph.add_edge(Tactics.INITIAL_ACCESS, 3, Tactics.EXECUTION, 4)
        attack_graph.add_edge(Tactics.INITIAL_ACCESS, 3, Tactics.COMMAND_AND_CONTROL, 5)
        attack_graph.add_edge(Tactics.INITIAL_ACCESS, 3, Tactics.DEFENSE_EVASION, 6)
        attack_graph.add_edge(Tactics.INITIAL_ACCESS, 3, Tactics.LATERAL_MOVEMENT, 7)

        attacker_action1 = EmulationAttackerAction(
            id=EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST,
            name="TCP SYN (Stealth) Scan", cmds=[], type=EmulationAttackerActionType.RECON,
            descr="TCP_SYN_STEALTH_SCAN_HOST", ips=[],
            index=0, action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action2 = EmulationAttackerAction(
            id=EmulationAttackerActionId.SAMBACRY_EXPLOIT,
            name="SSH Dictionary attack", cmds=[], type=EmulationAttackerActionType.EXPLOIT,
            descr="SSH Dictionary attack", ips=[],
            index=0, action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )

        attacker_action3 = EmulationAttackerAction(
            id=EmulationAttackerActionId.NETWORK_SERVICE_LOGIN,
            name="Login", cmds=[], type=EmulationAttackerActionType.POST_EXPLOIT, descr="Login", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )

        attacker_action4 = EmulationAttackerAction(
            id=EmulationAttackerActionId.CVE_2015_1427_EXPLOIT,
            name="CVE", cmds=[], type=EmulationAttackerActionType.EXPLOIT, descr="CVE", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )

        attacker_action = [attacker_action1, attacker_action2, attacker_action3, attacker_action4]

        # Call the method under test
        result = AttackProfiler.get_attack_profile_sequence(attacker_action, attack_graph)

        action1_tactics = [tactic for sublist in result[0].techniques_tactics.values() for tactic in sublist]
        assert 'reconnaissance' in action1_tactics
        assert 'discovery' not in action1_tactics

        action2_tactics = [tactic for sublist in result[1].techniques_tactics.values() for tactic in sublist]
        assert 'initial-access' in action2_tactics
        assert 'lateral-movement' not in action2_tactics

        action3_tactics = [tactic for sublist in result[2].techniques_tactics.values() for tactic in sublist]
        assert 'initial-access' in action3_tactics
        assert 'lateral-movement' not in action3_tactics

        # CVE_2015_1427_EXPLOIT will not prune any techniques
        assert result[3].techniques_tactics['Exploit Public-Facing Application']

    @pytest.mark.skip(reason="integration test, takes too long to run")
    def test_attack_profiler_sequence_novice(self) -> None:
        """
        Test the get_attack_profile_sequence for the novice sequence. Expected pruning of techniques
        in the graph approach.
        https://github.com/Kim-Hammar/csle/blob/d9fd28cf44a4ac0d9521368747d4b9c3fff37587/emulation-system/envs/050/level_9/config.py#L5035
        
        """
        attacker_action1 = EmulationAttackerAction(
            id=EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST,
            name="TCP SYN (Stealth) Scan", cmds=[], type=EmulationAttackerActionType.RECON,
            descr="TCP_SYN_STEALTH_SCAN_HOST", ips=[], index=0, action_outcome=EmulationAttackerActionOutcome.CONTINUE,
            backdoor=False
        )
        attacker_action2 = EmulationAttackerAction(
            id=EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_ALL,
            name="", cmds=[], type=EmulationAttackerActionType.EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action3 = EmulationAttackerAction(
            id=EmulationAttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_ALL,
            name="", cmds=[], type=EmulationAttackerActionType.EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action4 = EmulationAttackerAction(
            id=EmulationAttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_ALL,
            name="", cmds=[], type=EmulationAttackerActionType.EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action5 = EmulationAttackerAction(
            id=EmulationAttackerActionId.NETWORK_SERVICE_LOGIN,
            name="", cmds=[], type=EmulationAttackerActionType.POST_EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action6 = EmulationAttackerAction(
            id=EmulationAttackerActionId.INSTALL_TOOLS,
            name="", cmds=[], type=EmulationAttackerActionType.POST_EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action7 = EmulationAttackerAction(
            id=EmulationAttackerActionId.SSH_BACKDOOR,
            name="", cmds=[], type=EmulationAttackerActionType.POST_EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action8 = EmulationAttackerAction(
            id=EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST,
            name="", cmds=[], type=EmulationAttackerActionType.RECON, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action9 = EmulationAttackerAction(
            id=EmulationAttackerActionId.SHELLSHOCK_EXPLOIT,
            name="", cmds=[], type=EmulationAttackerActionType.EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action10 = EmulationAttackerAction(
            id=EmulationAttackerActionId.NETWORK_SERVICE_LOGIN,
            name="", cmds=[], type=EmulationAttackerActionType.POST_EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action11 = EmulationAttackerAction(
            id=EmulationAttackerActionId.INSTALL_TOOLS,
            name="", cmds=[], type=EmulationAttackerActionType.POST_EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action12 = EmulationAttackerAction(
            id=EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST,
            name="", cmds=[], type=EmulationAttackerActionType.EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action13 = EmulationAttackerAction(
            id=EmulationAttackerActionId.NETWORK_SERVICE_LOGIN,
            name="", cmds=[], type=EmulationAttackerActionType.POST_EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action14 = EmulationAttackerAction(
            id=EmulationAttackerActionId.CVE_2010_0426_PRIV_ESC,
            name="", cmds=[], type=EmulationAttackerActionType.PRIVILEGE_ESCALATION, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action15 = EmulationAttackerAction(
            id=EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST,
            name="", cmds=[], type=EmulationAttackerActionType.RECON, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )

        attack_sequence = [attacker_action1, attacker_action2, attacker_action3,
                           attacker_action4, attacker_action5, attacker_action6,
                           attacker_action7, attacker_action8, attacker_action9,
                           attacker_action10, attacker_action11, attacker_action12,
                           attacker_action13, attacker_action14, attacker_action15]

        # First the naive approach
        result_naive = []
        for action in attack_sequence:
            result_naive.append(AttackProfiler.get_attack_profile(action))
        # Count the number of techniques in the naive approach
        techniques_naive = []
        for result in result_naive:
            for technique in result.techniques_tactics:
                techniques_naive.append(technique)
        # Print the number of techniques in the naive approach
        print("Number of techniques in the naive approach: ", len(techniques_naive))

        # Now the graph approach
        attack_graph = AttackGraph()
        attack_graph.add_node(Tactics.RECONNAISSANCE, node_id=1)
        attack_graph.add_node(Tactics.CREDENTIAL_ACCESS, node_id=2)
        attack_graph.add_node(Tactics.INITIAL_ACCESS, node_id=3)
        attack_graph.add_node(Tactics.COMMAND_AND_CONTROL, node_id=4)
        attack_graph.add_node(Tactics.PERSISTENCE, node_id=5)
        attack_graph.add_node(Tactics.DISCOVERY, node_id=6)
        attack_graph.add_node(Tactics.EXECUTION, node_id=7)
        attack_graph.add_node(Tactics.LATERAL_MOVEMENT, node_id=8)
        attack_graph.add_node(Tactics.PRIVILEGE_ESCALATION, node_id=9)

        attack_graph.add_edge(Tactics.RECONNAISSANCE, 1, Tactics.CREDENTIAL_ACCESS, 2)
        attack_graph.add_edge(Tactics.RECONNAISSANCE, 1, Tactics.INITIAL_ACCESS, 3)
        attack_graph.add_edge(Tactics.CREDENTIAL_ACCESS, 2, Tactics.LATERAL_MOVEMENT, 8)
        attack_graph.add_edge(Tactics.INITIAL_ACCESS, 3, Tactics.COMMAND_AND_CONTROL, 4)
        attack_graph.add_edge(Tactics.COMMAND_AND_CONTROL, 4, Tactics.CREDENTIAL_ACCESS, 2)
        attack_graph.add_edge(Tactics.COMMAND_AND_CONTROL, 4, Tactics.PERSISTENCE, 5)
        attack_graph.add_edge(Tactics.PERSISTENCE, 5, Tactics.DISCOVERY, 6)
        attack_graph.add_edge(Tactics.DISCOVERY, 6, Tactics.EXECUTION, 7)
        attack_graph.add_edge(Tactics.DISCOVERY, 6, Tactics.LATERAL_MOVEMENT, 8)
        attack_graph.add_edge(Tactics.LATERAL_MOVEMENT, 8, Tactics.COMMAND_AND_CONTROL, 4)
        attack_graph.add_edge(Tactics.LATERAL_MOVEMENT, 8, Tactics.DISCOVERY, 6)
        attack_graph.add_edge(Tactics.LATERAL_MOVEMENT, 8, Tactics.EXECUTION, 7)
        attack_graph.add_edge(Tactics.LATERAL_MOVEMENT, 8, Tactics.PRIVILEGE_ESCALATION, 9)

        result_graph = AttackProfiler.get_attack_profile_sequence(attack_sequence, attack_graph)

        # Count the number of techniques in the graph approach
        techniques_graph = []
        for result in result_graph:
            for technique in result.techniques_tactics:
                techniques_graph.append(technique)
        # Print the number of techniques in the graph approach

        print("Number of techniques in the graph approach: ", len(techniques_graph))

        # Assert that the number of techniques in the graph approach is less than
        # the number of techniques in the naive approach
        assert len(techniques_graph) < len(techniques_naive)

    @pytest.mark.skip(reason="integration test, takes too long to run")
    def test_attack_profiler_sequence_experienced(self) -> None:
        """
        Test the get_attack_profile_sequence for the experienced sequence.
        Expected pruning of techniques in the graph approach.
        https://github.com/Kim-Hammar/csle/blob/d9fd28cf44a4ac0d9521368747d4b9c3fff37587/emulation-system/envs/050/level_9/config.py#L5035
        """

        attacker_action1 = EmulationAttackerAction(
            id=EmulationAttackerActionId.PING_SCAN_HOST,
            name="TCP SYN (Stealth) Scan", cmds=[], type=EmulationAttackerActionType.RECON,
            descr="TCP_SYN_STEALTH_SCAN_HOST", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action2 = EmulationAttackerAction(
            id=EmulationAttackerActionId.SAMBACRY_EXPLOIT,
            name="", cmds=[], type=EmulationAttackerActionType.EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action3 = EmulationAttackerAction(
            id=EmulationAttackerActionId.NETWORK_SERVICE_LOGIN,
            name="", cmds=[], type=EmulationAttackerActionType.POST_EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action4 = EmulationAttackerAction(
            id=EmulationAttackerActionId.INSTALL_TOOLS,
            name="", cmds=[], type=EmulationAttackerActionType.POST_EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action5 = EmulationAttackerAction(
            id=EmulationAttackerActionId.PING_SCAN_HOST,
            name="", cmds=[], type=EmulationAttackerActionType.RECON, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action6 = EmulationAttackerAction(
            id=EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST,
            name="", cmds=[], type=EmulationAttackerActionType.EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action7 = EmulationAttackerAction(
            id=EmulationAttackerActionId.NETWORK_SERVICE_LOGIN,
            name="", cmds=[], type=EmulationAttackerActionType.POST_EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action8 = EmulationAttackerAction(
            id=EmulationAttackerActionId.CVE_2010_0426_PRIV_ESC,
            name="", cmds=[], type=EmulationAttackerActionType.PRIVILEGE_ESCALATION, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action9 = EmulationAttackerAction(
            id=EmulationAttackerActionId.PING_SCAN_HOST,
            name="", cmds=[], type=EmulationAttackerActionType.RECON, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action10 = EmulationAttackerAction(
            id=EmulationAttackerActionId.DVWA_SQL_INJECTION,
            name="", cmds=[], type=EmulationAttackerActionType.EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action11 = EmulationAttackerAction(
            id=EmulationAttackerActionId.NETWORK_SERVICE_LOGIN,
            name="", cmds=[], type=EmulationAttackerActionType.POST_EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action12 = EmulationAttackerAction(
            id=EmulationAttackerActionId.INSTALL_TOOLS,
            name="", cmds=[], type=EmulationAttackerActionType.POST_EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action13 = EmulationAttackerAction(
            id=EmulationAttackerActionId.PING_SCAN_HOST,
            name="", cmds=[], type=EmulationAttackerActionType.RECON, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action14 = EmulationAttackerAction(
            id=EmulationAttackerActionId.CVE_2015_1427_EXPLOIT,
            name="", cmds=[], type=EmulationAttackerActionType.EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action15 = EmulationAttackerAction(
            id=EmulationAttackerActionId.NETWORK_SERVICE_LOGIN,
            name="", cmds=[], type=EmulationAttackerActionType.POST_EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action16 = EmulationAttackerAction(
            id=EmulationAttackerActionId.INSTALL_TOOLS,
            name="", cmds=[], type=EmulationAttackerActionType.POST_EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action17 = EmulationAttackerAction(
            id=EmulationAttackerActionId.PING_SCAN_HOST,
            name="", cmds=[], type=EmulationAttackerActionType.RECON, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )

        # Create a list of attacker actions
        attack_sequence = [attacker_action1, attacker_action2, attacker_action3,
                           attacker_action4, attacker_action5, attacker_action6,
                           attacker_action7, attacker_action8, attacker_action9,
                           attacker_action10, attacker_action11, attacker_action12,
                           attacker_action13, attacker_action14, attacker_action15,
                           attacker_action16, attacker_action17]

        # First the naive approach
        result_naive = []
        for action in attack_sequence:
            result_naive.append(AttackProfiler.get_attack_profile(action))

        # Count the number of techniques in the naive approach
        techniques_naive = []
        for result in result_naive:
            for technique in result.techniques_tactics:
                techniques_naive.append(technique)

        # Print the number of techniques in the naive approach
        print("Number of techniques in the naive approach: ", len(techniques_naive))

        # Now the graph approach
        attack_graph = AttackGraph()
        attack_graph.add_node(Tactics.RECONNAISSANCE, node_id=1)
        attack_graph.add_node(Tactics.INITIAL_ACCESS, node_id=2)
        attack_graph.add_node(Tactics.COMMAND_AND_CONTROL, node_id=3)
        attack_graph.add_node(Tactics.DISCOVERY, node_id=4)
        attack_graph.add_node(Tactics.LATERAL_MOVEMENT, node_id=5)
        attack_graph.add_node(Tactics.CREDENTIAL_ACCESS, node_id=6)
        attack_graph.add_node(Tactics.EXECUTION, node_id=8)
        attack_graph.add_node(Tactics.PRIVILEGE_ESCALATION, node_id=9)

        attack_graph.add_edge(Tactics.RECONNAISSANCE, 1, Tactics.INITIAL_ACCESS, 2)
        attack_graph.add_edge(Tactics.RECONNAISSANCE, 1, Tactics.EXECUTION, 8)
        attack_graph.add_edge(Tactics.INITIAL_ACCESS, 2, Tactics.COMMAND_AND_CONTROL, 3)
        attack_graph.add_edge(Tactics.COMMAND_AND_CONTROL, 3, Tactics.DISCOVERY, 4)
        attack_graph.add_edge(Tactics.DISCOVERY, 4, Tactics.COMMAND_AND_CONTROL, 3)
        attack_graph.add_edge(Tactics.DISCOVERY, 4, Tactics.LATERAL_MOVEMENT, 5)
        attack_graph.add_edge(Tactics.DISCOVERY, 4, Tactics.CREDENTIAL_ACCESS, 6)
        attack_graph.add_edge(Tactics.DISCOVERY, 4, Tactics.EXECUTION, 8)
        attack_graph.add_edge(Tactics.CREDENTIAL_ACCESS, 6, Tactics.LATERAL_MOVEMENT, 5)
        attack_graph.add_edge(Tactics.LATERAL_MOVEMENT, 5, Tactics.PRIVILEGE_ESCALATION, 9)
        attack_graph.add_edge(Tactics.LATERAL_MOVEMENT, 5, Tactics.EXECUTION, 8)
        attack_graph.add_edge(Tactics.LATERAL_MOVEMENT, 5, Tactics.COMMAND_AND_CONTROL, 3)
        attack_graph.add_edge(Tactics.LATERAL_MOVEMENT, 5, Tactics.DISCOVERY, 4)

        result_graph = AttackProfiler.get_attack_profile_sequence(attack_sequence, attack_graph)

        # Count the number of techniques in the graph approach
        techniques_graph = []
        for result in result_graph:
            for technique in result.techniques_tactics:
                techniques_graph.append(technique)

        print("Number of techniques in the graph approach: ", len(techniques_graph))

        # Assert that the number of techniques in the graph approach is less
        # than the number of techniques in the naive approach
        assert len(techniques_graph) < len(techniques_naive)

    @pytest.mark.skip(reason="integration test, takes too long to run")
    def test_attack_profiler_sequence_expert(self) -> None:
        """
        Test the get_attack_profile_sequence for the experienced sequence.
        Expected pruning of techniques in the graph approach.
        https://github.com/Kim-Hammar/csle/blob/d9fd28cf44a4ac0d9521368747d4b9c3fff37587/emulation-system/envs/050/level_9/config.py#L5035
        """

        attacker_action1 = EmulationAttackerAction(
            id=EmulationAttackerActionId.PING_SCAN_HOST,
            name="TCP SYN (Stealth) Scan", cmds=[], type=EmulationAttackerActionType.RECON,
            descr="TCP_SYN_STEALTH_SCAN_HOST", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action2 = EmulationAttackerAction(
            id=EmulationAttackerActionId.SAMBACRY_EXPLOIT,
            name="", cmds=[], type=EmulationAttackerActionType.EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action3 = EmulationAttackerAction(
            id=EmulationAttackerActionId.NETWORK_SERVICE_LOGIN,
            name="", cmds=[], type=EmulationAttackerActionType.POST_EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action4 = EmulationAttackerAction(
            id=EmulationAttackerActionId.INSTALL_TOOLS,
            name="", cmds=[], type=EmulationAttackerActionType.POST_EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action5 = EmulationAttackerAction(
            id=EmulationAttackerActionId.PING_SCAN_HOST,
            name="", cmds=[], type=EmulationAttackerActionType.RECON, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action6 = EmulationAttackerAction(
            id=EmulationAttackerActionId.DVWA_SQL_INJECTION,
            name="", cmds=[], type=EmulationAttackerActionType.EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action7 = EmulationAttackerAction(
            id=EmulationAttackerActionId.INSTALL_TOOLS,
            name="", cmds=[], type=EmulationAttackerActionType.POST_EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action8 = EmulationAttackerAction(
            id=EmulationAttackerActionId.NETWORK_SERVICE_LOGIN,
            name="", cmds=[], type=EmulationAttackerActionType.POST_EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action10 = EmulationAttackerAction(
            id=EmulationAttackerActionId.CVE_2015_1427_EXPLOIT,
            name="", cmds=[], type=EmulationAttackerActionType.EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action11 = EmulationAttackerAction(
            id=EmulationAttackerActionId.NETWORK_SERVICE_LOGIN,
            name="", cmds=[], type=EmulationAttackerActionType.POST_EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action12 = EmulationAttackerAction(
            id=EmulationAttackerActionId.INSTALL_TOOLS,
            name="", cmds=[], type=EmulationAttackerActionType.POST_EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action13 = EmulationAttackerAction(
            id=EmulationAttackerActionId.PING_SCAN_HOST,
            name="", cmds=[], type=EmulationAttackerActionType.RECON, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action14 = EmulationAttackerAction(
            id=EmulationAttackerActionId.SAMBACRY_EXPLOIT,
            name="", cmds=[], type=EmulationAttackerActionType.EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action15 = EmulationAttackerAction(
            id=EmulationAttackerActionId.NETWORK_SERVICE_LOGIN,
            name="", cmds=[], type=EmulationAttackerActionType.POST_EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action16 = EmulationAttackerAction(
            id=EmulationAttackerActionId.INSTALL_TOOLS,
            name="", cmds=[], type=EmulationAttackerActionType.POST_EXPLOIT, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )
        attacker_action17 = EmulationAttackerAction(
            id=EmulationAttackerActionId.PING_SCAN_HOST,
            name="", cmds=[], type=EmulationAttackerActionType.RECON, descr="", ips=[], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, backdoor=False
        )

        attack_sequence = [attacker_action1, attacker_action2, attacker_action3,
                           attacker_action4, attacker_action5, attacker_action6,
                           attacker_action7, attacker_action8, attacker_action10,
                           attacker_action11, attacker_action12, attacker_action13,
                           attacker_action14, attacker_action15, attacker_action16,
                           attacker_action17]

        # First with the graph approach
        attack_graph = AttackGraph()
        attack_graph.add_node(Tactics.RECONNAISSANCE, node_id=1)
        attack_graph.add_node(Tactics.INITIAL_ACCESS, node_id=2)
        attack_graph.add_node(Tactics.COMMAND_AND_CONTROL, node_id=3)
        attack_graph.add_node(Tactics.DISCOVERY, node_id=4)
        attack_graph.add_node(Tactics.CREDENTIAL_ACCESS, node_id=5)
        attack_graph.add_node(Tactics.LATERAL_MOVEMENT, node_id=6)
        attack_graph.add_node(Tactics.EXECUTION, node_id=7)

        attack_graph.add_edge(Tactics.RECONNAISSANCE, 1, Tactics.INITIAL_ACCESS, 2)
        attack_graph.add_edge(Tactics.RECONNAISSANCE, 1, Tactics.EXECUTION, 7)
        attack_graph.add_edge(Tactics.INITIAL_ACCESS, 2, Tactics.COMMAND_AND_CONTROL, 3)
        attack_graph.add_edge(Tactics.COMMAND_AND_CONTROL, 3, Tactics.DISCOVERY, 4)
        attack_graph.add_edge(Tactics.DISCOVERY, 4, Tactics.CREDENTIAL_ACCESS, 5)
        attack_graph.add_edge(Tactics.DISCOVERY, 4, Tactics.EXECUTION, 7)
        attack_graph.add_edge(Tactics.DISCOVERY, 4, Tactics.LATERAL_MOVEMENT, 6)
        attack_graph.add_edge(Tactics.DISCOVERY, 4, Tactics.COMMAND_AND_CONTROL, 3)
        attack_graph.add_edge(Tactics.CREDENTIAL_ACCESS, 5, Tactics.LATERAL_MOVEMENT, 6)
        attack_graph.add_edge(Tactics.LATERAL_MOVEMENT, 6, Tactics.COMMAND_AND_CONTROL, 3)

        result_graph = AttackProfiler.get_attack_profile_sequence(attack_sequence, attack_graph)

        # Count the number of techniques in the graph approach
        techniques_graph = []
        for result in result_graph:
            for technique in result.techniques_tactics:
                techniques_graph.append(technique)

        print("Number of techniques with the graph approach:  ", len(techniques_graph))

        # Now with the naive approach
        result_naive = []
        for action in attack_sequence:
            result_naive.append(AttackProfiler.get_attack_profile(action))

        # Count the number of techniques in the naive approach
        techniques_naive = []
        for result in result_naive:
            for technique in result.techniques_tactics:
                techniques_naive.append(technique)

        print("Number of techniques with the naive approach:  ", len(techniques_naive))

        # Assert that the number of techniques in the graph approach is less
        # than the number of techniques in the naive approach
        assert len(techniques_graph) < len(techniques_naive)

    def test_graph(self) -> None:
        """
        Test the AttackGraph class
        """
        attack_graph = AttackGraph()
        attack_graph.add_node(Tactics.RECONNAISSANCE, [(Tactics.CREDENTIAL_ACCESS, 2)], 1)
        attack_graph.add_node(Tactics.CREDENTIAL_ACCESS, [(Tactics.INITIAL_ACCESS, 3)], 2)
        attack_graph.add_node(Tactics.CREDENTIAL_ACCESS, [], 4)
        attack_graph.add_node(Tactics.INITIAL_ACCESS, [], 3)

        assert attack_graph.get_node(Tactics.RECONNAISSANCE, 1) == (Tactics.RECONNAISSANCE,
                                                                    [(Tactics.CREDENTIAL_ACCESS, 2)], 1)
        assert attack_graph.get_node(Tactics.CREDENTIAL_ACCESS, 2) == (Tactics.CREDENTIAL_ACCESS,
                                                                       [(Tactics.INITIAL_ACCESS, 3)], 2)
        assert attack_graph.get_node(Tactics.INITIAL_ACCESS, 3) == (Tactics.INITIAL_ACCESS, [], 3)

        assert attack_graph.get_root_node() == (Tactics.RECONNAISSANCE, [(Tactics.CREDENTIAL_ACCESS, 2)], 1)
