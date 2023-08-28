from csle_common.dao.emulation_observation.common.emulation_port_observation_state import EmulationPortObservationState
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_common.dao.emulation_observation.attacker.\
    emulation_attacker_machine_observation_state import EmulationAttackerMachineObservationState
from csle_common.dao.emulation_observation.attacker.\
    emulation_attacker_observation_state import EmulationAttackerObservationState
from csle_common.dao.emulation_observation.common.emulation_connection_observation_state \
    import EmulationConnectionObservationState
from csle_common.dao.emulation_config.credential import Credential
from csle_common.dao.emulation_observation.common.emulation_vulnerability_observation_state \
    import EmulationVulnerabilityObservationState
from csle_common.dao.emulation_observation.defender.emulation_defender_machine_observation_state import \
    EmulationDefenderMachineObservationState
from csle_common.dao.emulation_config.kafka_config import KafkaConfig
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.dao.emulation_config.node_resources_config import NodeResourcesConfig
from csle_common.dao.emulation_config.node_firewall_config import NodeFirewallConfig
from csle_common.dao.emulation_config.kafka_topic import KafkaTopic
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.dao.emulation_config.node_network_config import NodeNetworkConfig
from csle_common.dao.emulation_config.default_network_firewall_config import DefaultNetworkFirewallConfig
from csle_collector.host_manager.dao.host_metrics import HostMetrics
from csle_collector.docker_stats_manager.dao.docker_stats import DockerStats
from csle_collector.snort_ids_manager.dao.snort_ids_ip_alert_counters import SnortIdsIPAlertCounters
from csle_collector.ossec_ids_manager.dao.ossec_ids_alert_counters import OSSECIdsAlertCounters
from csle_common.dao.emulation_observation.defender.emulation_defender_observation_state import \
    EmulationDefenderObservationState
from csle_collector.client_manager.client_population_metrics import ClientPopulationMetrics
from csle_collector.snort_ids_manager.dao.snort_ids_alert_counters import SnortIdsAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_rule_counters import SnortIdsRuleCounters
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action_id import EmulationDefenderActionId
from csle_common.dao.emulation_action.defender.emulation_defender_action_type import EmulationDefenderActionType
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType


class TestEmulationObservationDaoSuite:
    """
    Test suite for emulation observation data access objects (DAOs)
    """

    def test_emulation_port_observation_state(self) -> None:
        """
        Tests creation and dict conversion of the EmulationPortObservationState DAO

        :return: None
        """

        emulation_port_observation_state = EmulationPortObservationState(
            port=3333, open=False, service="myservice", protocol=TransportProtocol.TCP, http_enum="testenum",
            http_grep="testgrep", vulscan="vulscantest", version="myversion", fingerprint="myfp")

        assert isinstance(emulation_port_observation_state.to_dict(), dict)
        assert isinstance(EmulationPortObservationState.from_dict(emulation_port_observation_state.to_dict()),
                          EmulationPortObservationState)
        assert (EmulationPortObservationState.from_dict(emulation_port_observation_state.to_dict()).to_dict() ==
                emulation_port_observation_state.to_dict())
        assert (EmulationPortObservationState.from_dict(emulation_port_observation_state.to_dict()) ==
                emulation_port_observation_state)

    def test_emulation_attacker_machine_observation_state(self) -> None:
        """
        Tests creation and dict conversion of the EmulationAttackerMachineObservationState DAO

        :return: None
        """

        emulation_attack_machine_observation_state = (EmulationAttackerMachineObservationState
                                                      (ips=["172.31.212.1", "172.31.212.2"]))

        assert isinstance(emulation_attack_machine_observation_state.to_dict(), dict)

        assert isinstance(EmulationAttackerMachineObservationState.from_dict
                          (emulation_attack_machine_observation_state.to_dict()),
                          EmulationAttackerMachineObservationState)
        assert (EmulationAttackerMachineObservationState.from_dict
                (emulation_attack_machine_observation_state.to_dict()).to_dict() ==
                emulation_attack_machine_observation_state.to_dict())
        assert (EmulationAttackerMachineObservationState.from_dict
                (emulation_attack_machine_observation_state.to_dict()) ==
                emulation_attack_machine_observation_state)

    def test_emulation_attacker_observation_state(self) -> None:
        """
        Tests creation and dict conversion of the EmulationAttackerObservationState DAO

        :return: None
        """

        emulation_attack_observation_state = (EmulationAttackerObservationState
                                              (catched_flags=1, agent_reachable=set(["test1", "test2"])))

        assert isinstance(emulation_attack_observation_state.to_dict(), dict)

        assert isinstance(EmulationAttackerObservationState.from_dict
                          (emulation_attack_observation_state.to_dict()),
                          EmulationAttackerObservationState)
        assert (EmulationAttackerObservationState.from_dict
                (emulation_attack_observation_state.to_dict()).to_dict() ==
                emulation_attack_observation_state.to_dict())
        assert (EmulationAttackerObservationState.from_dict
                (emulation_attack_observation_state.to_dict()) ==
                emulation_attack_observation_state)

    def test_emulation_connection_observation_state(self) -> None:
        """
        Tests creation and dict conversion of the EmulationConnectionObservationState DAO

        :return: None
        """
        emulation_connection_observation_state = (EmulationConnectionObservationState
                                                  (conn=None, credential=Credential(username="shahab", pw="123"),
                                                   root=False, service="test1", port=123))

        assert isinstance(emulation_connection_observation_state.to_dict(), dict)

        assert isinstance(EmulationConnectionObservationState.from_dict
                          (emulation_connection_observation_state.to_dict()),
                          EmulationConnectionObservationState)
        assert (EmulationConnectionObservationState.from_dict
                (emulation_connection_observation_state.to_dict()).to_dict() ==
                emulation_connection_observation_state.to_dict())
        assert (EmulationConnectionObservationState.from_dict
                (emulation_connection_observation_state.to_dict()) ==
                emulation_connection_observation_state)

    def test_emulation_vulnerability_observation_state(self) -> None:
        """
        Tests creation and dict conversion of the EmulationVulnerabilityObservationState DAO

        :return: None
        """
        emulation_vulnerability_observation_state = (EmulationVulnerabilityObservationState
                                                     (name="test", port=123, protocol=TransportProtocol.TCP, cvss=0.1,
                                                      credentials=[]))

        assert isinstance(emulation_vulnerability_observation_state.to_dict(), dict)

        assert isinstance(EmulationVulnerabilityObservationState.from_dict
                          (emulation_vulnerability_observation_state.to_dict()),
                          EmulationVulnerabilityObservationState)
        assert (EmulationVulnerabilityObservationState.from_dict
                (emulation_vulnerability_observation_state.to_dict()).to_dict() ==
                emulation_vulnerability_observation_state.to_dict())
        assert (EmulationVulnerabilityObservationState.from_dict
                (emulation_vulnerability_observation_state.to_dict()) ==
                emulation_vulnerability_observation_state)

    def test_emulation_defender_machine_observation_state(self) -> None:
        """
        Tests creation and dict conversion of the EmulationDefenderMachineObservationState DAO

        :return: None
        """

        ips = ["10.10.10.10", "20.20.20.20"]
        container_network = ContainerNetwork(name="test1", subnet_mask="0.0.0.0",
                                             bitmask="0.0.0.0", subnet_prefix="0.0.0.0")
        ips_and_networks = [("container_network_test", container_network)]
        container = NodeContainerConfig("test1", ips_and_networks=ips_and_networks, version="1.0", level="1",
                                        restart_policy="test1", suffix="test2", os="ubuntu")
        ips_and_network_configs = [("test2", NodeNetworkConfig())]
        resources = NodeResourcesConfig(container_name="test1", num_cpus=1,
                                        available_memory_gb=100, ips_and_network_configs=ips_and_network_configs)

        default_network_firewall_config = DefaultNetworkFirewallConfig(ip="1.1.1.1",
                                                                       default_gw="2.3.3.4",
                                                                       default_input="test",
                                                                       default_output="tets",
                                                                       default_forward="test",
                                                                       network=container_network)
        ips_gw_default_policy_networks = [default_network_firewall_config]
        firewall_config = NodeFirewallConfig(ips_gw_default_policy_networks=ips_gw_default_policy_networks,
                                             hostname="test1", output_accept={"test1", "test2"},
                                             forward_accept={"test1", "test2"}, output_drop={"test"},
                                             input_drop={"test2"}, forward_drop={"test3"},
                                             input_accept={"test"},
                                             routes={("test", "test")})
        topics = [
            KafkaTopic(name="test", num_partitions=1, num_replicas=2, attributes=["test"], retention_time_hours=1)]

        kafka_config = KafkaConfig(container=container, resources=resources, firewall_config=firewall_config,
                                   topics=topics, kafka_manager_log_file="test", kafka_manager_log_dir="test",
                                   kafka_manager_max_workers=10)

        emulation_defender_machine_observation_state = (EmulationDefenderMachineObservationState
                                                        (ips=ips, kafka_config=kafka_config, host_metrics=HostMetrics(),
                                                         docker_stats=DockerStats(),
                                                         snort_ids_ip_alert_counters=SnortIdsIPAlertCounters(),
                                                         ossec_ids_alert_counters=OSSECIdsAlertCounters()))

        assert isinstance(emulation_defender_machine_observation_state.to_dict(), dict)

        assert isinstance(EmulationDefenderMachineObservationState.from_dict
                          (emulation_defender_machine_observation_state.to_dict()),
                          EmulationDefenderMachineObservationState)
        assert (EmulationDefenderMachineObservationState.from_dict
                (emulation_defender_machine_observation_state.to_dict()).to_dict() ==
                emulation_defender_machine_observation_state.to_dict())
        assert (EmulationDefenderMachineObservationState.from_dict
                (emulation_defender_machine_observation_state.to_dict()) ==
                emulation_defender_machine_observation_state)

    def test_emulation_defender_observation_state(self) -> None:
        """
        Tests creation and dict conversion of the EmulationDefenderObservationState DAO

        :return: None
        """

        ips = ["10.10.10.10", "20.20.20.20"]
        container_network = ContainerNetwork(name="test1", subnet_mask="0.0.0.0",
                                             bitmask="0.0.0.0", subnet_prefix="0.0.0.0")
        ips_and_networks = [("container_network_test", container_network)]
        container = NodeContainerConfig("test1", ips_and_networks=ips_and_networks, version="1.0", level="1",
                                        restart_policy="test1", suffix="test2", os="ubuntu")
        ips_and_network_configs = [("test2", NodeNetworkConfig())]
        resources = NodeResourcesConfig(container_name="test1", num_cpus=1,
                                        available_memory_gb=100, ips_and_network_configs=ips_and_network_configs)

        default_network_firewall_config = DefaultNetworkFirewallConfig(ip="1.1.1.1",
                                                                       default_gw="2.3.3.4",
                                                                       default_input="test",
                                                                       default_output="tets",
                                                                       default_forward="test",
                                                                       network=container_network)
        ips_gw_default_policy_networks = [default_network_firewall_config]
        firewall_config = NodeFirewallConfig(ips_gw_default_policy_networks=ips_gw_default_policy_networks,
                                             hostname="test1", output_accept={"test1", "test2"},
                                             forward_accept={"test1", "test2"}, output_drop={"test"},
                                             input_drop={"test2"}, forward_drop={"test3"},
                                             input_accept={"test"},
                                             routes={("test", "test")})
        topics = [
            KafkaTopic(name="test", num_partitions=1, num_replicas=2, attributes=["test"], retention_time_hours=1)]

        kafka_config = KafkaConfig(container=container, resources=resources, firewall_config=firewall_config,
                                   topics=topics, kafka_manager_log_file="test", kafka_manager_log_dir="test",
                                   kafka_manager_max_workers=10)
        emulation_defender_action = EmulationDefenderAction(id=EmulationDefenderActionId.CONTINUE, name="test",
                                                            cmds=["test", "test2"],
                                                            type=EmulationDefenderActionType.CONTINUE,
                                                            descr="test", ips=ips, index=1)
        emulation_attacker_action = EmulationAttackerAction(id=EmulationAttackerActionId.NETWORK_SERVICE_LOGIN,
                                                            name="test",
                                                            cmds=["test", "test2"],
                                                            type=EmulationAttackerActionType.PRIVILEGE_ESCALATION,
                                                            descr="test", ips=ips, index=1)

        emulation_defender_observation_state = (EmulationDefenderObservationState(
            kafka_config=kafka_config, client_population_metrics=ClientPopulationMetrics(), docker_stats=DockerStats(),
            snort_ids_alert_counters=SnortIdsAlertCounters(), ossec_ids_alert_counters=OSSECIdsAlertCounters(),
            aggregated_host_metrics=HostMetrics(), defender_actions=[emulation_defender_action],
            attacker_actions=[emulation_attacker_action],
            snort_ids_rule_counters=SnortIdsRuleCounters()
        ))

        assert isinstance(emulation_defender_observation_state.to_dict(), dict)

        assert isinstance(EmulationDefenderObservationState.from_dict
                          (emulation_defender_observation_state.to_dict()),
                          EmulationDefenderObservationState)
        assert (EmulationDefenderObservationState.from_dict
                (emulation_defender_observation_state.to_dict()).to_dict() ==
                emulation_defender_observation_state.to_dict())
        assert (EmulationDefenderObservationState.from_dict
                (emulation_defender_observation_state.to_dict()) ==
                emulation_defender_observation_state)
