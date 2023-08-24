from csle_common.dao.emulation_config.node_beats_config import NodeBeatsConfig
from csle_common.dao.emulation_config.beats_config import BeatsConfig
from csle_common.dao.emulation_config.client_managers_info import ClientManagersInfo
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.dao.emulation_config.cluster_node import ClusterNode
from csle_common.dao.emulation_config.cluster_config import ClusterConfig
from csle_common.dao.emulation_config.config import Config
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_outcome import EmulationAttackerActionOutcome
from csle_common.dao.emulation_config.credential import Credential
from csle_common.dao.emulation_config.default_network_firewall_config import DefaultNetworkFirewallConfig
from csle_common.dao.emulation_config.node_firewall_config import NodeFirewallConfig
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_common.dao.emulation_config.docker_stats_manager_config import DockerStatsManagerConfig
from csle_common.dao.emulation_config.docker_stats_managers_info import DockerStatsManagersInfo
from csle_common.dao.emulation_config.node_network_config import NodeNetworkConfig
from csle_common.dao.emulation_config.packet_loss_type import PacketLossType
from csle_common.dao.emulation_config.packet_delay_distribution_type import PacketDelayDistributionType
from csle_common.dao.emulation_config.host_manager_config import HostManagerConfig
from csle_common.dao.emulation_config.snort_ids_manager_config import SnortIDSManagerConfig
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_config.node_resources_config import NodeResourcesConfig
from csle_common.dao.emulation_config.resources_config import ResourcesConfig
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.dao.emulation_config.node_services_config import NodeServicesConfig
from csle_common.dao.emulation_config.services_config import ServicesConfig
from csle_common.dao.emulation_config.users_config import UsersConfig
from csle_common.dao.emulation_config.traffic_config import TrafficConfig
from csle_common.dao.emulation_config.vulnerabilities_config import VulnerabilitiesConfig
from csle_common.dao.emulation_config.client_population_config import ClientPopulationConfig
from csle_common.dao.emulation_config.node_traffic_config import NodeTrafficConfig
from csle_common.dao.emulation_config.containers_config import ContainersConfig
from csle_common.dao.emulation_config.user import User
from csle_common.dao.emulation_config.node_users_config import NodeUsersConfig
from csle_common.dao.emulation_config.node_vulnerability_config import NodeVulnerabilityConfig
from csle_common.dao.emulation_config.flag import Flag
from csle_common.dao.emulation_config.node_flags_config import NodeFlagsConfig
from csle_common.dao.emulation_config.flags_config import FlagsConfig
from csle_common.dao.emulation_config.topology_config import TopologyConfig
from csle_common.dao.emulation_config.elk_config import ElkConfig
from csle_common.dao.emulation_config.elk_managers_info import ELKManagersInfo
from csle_common.dao.emulation_config.snort_managers_info import SnortIdsManagersInfo
from csle_common.dao.emulation_config.ossec_managers_info import OSSECIDSManagersInfo
from csle_common.dao.emulation_config.ryu_managers_info import RyuManagersInfo
from csle_common.dao.emulation_config.host_managers_info import HostManagersInfo
from csle_common.dao.emulation_config.kafka_managers_info import KafkaManagersInfo
from csle_common.dao.emulation_config.ossec_ids_manager_config import OSSECIDSManagerConfig
from csle_common.dao.emulation_config.sdn_controller_config import SDNControllerConfig
from csle_common.dao.emulation_config.sdn_controller_type import SDNControllerType
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.ovs_config import OVSConfig
from csle_common.dao.emulation_config.ovs_switch_config import OvsSwitchConfig
from csle_common.dao.emulation_config.kafka_config import KafkaConfig
from csle_common.dao.emulation_config.kafka_topic import KafkaTopic
from csle_common.dao.emulation_config.vulnerability_type import VulnType
from csle_common.dao.emulation_config.network_service import NetworkService
from csle_common.dao.emulation_observation.common.emulation_connection_observation_state import \
    EmulationConnectionObservationState
from csle_common.dao.emulation_config.connection_setup_dto import ConnectionSetupDTO
from csle_collector.client_manager.client_manager_pb2 import ClientsDTO
from csle_collector.docker_stats_manager.docker_stats_manager_pb2 import DockerStatsMonitorDTO
from csle_collector.elk_manager.elk_manager_pb2 import ElkDTO
from csle_collector.host_manager.host_manager_pb2 import HostStatusDTO
from csle_collector.snort_ids_manager.snort_ids_manager_pb2 import SnortIdsMonitorDTO
from csle_collector.ossec_ids_manager.ossec_ids_manager_pb2 import OSSECIdsMonitorDTO
from csle_collector.ryu_manager.ryu_manager_pb2 import RyuDTO
from csle_collector.kafka_manager.kafka_manager_pb2 import KafkaDTO
from csle_collector.client_manager.dao.client import Client
from csle_collector.client_manager.dao.constant_arrival_config import ConstantArrivalConfig
from csle_collector.client_manager.dao.workflows_config import WorkflowsConfig
from csle_collector.client_manager.dao.workflow_service import WorkflowService
from csle_collector.client_manager.dao.workflow_markov_chain import WorkflowMarkovChain


class TestEmulationConfigDaoSuite:
    """
    Test suite for datasets data access objects (DAOs)
    """

    def test_node_beats_config(self) -> None:
        """
        Tests creation and dict conversion of the NodeBeatsConfig DAO

        :return: None
        """
        node_beats_config = NodeBeatsConfig(
            ip="192.168.5.1", log_files_paths=["log1"], filebeat_modules=["mod1"], metricbeat_modules=["mod2"],
            heartbeat_hosts_to_monitor=["192.168.5.7"], kafka_input=False, start_heartbeat_automatically=True,
            start_packetbeat_automatically=True, start_metricbeat_automatically=True, start_filebeat_automatically=True
        )
        assert isinstance(node_beats_config.to_dict(), dict)
        assert isinstance(NodeBeatsConfig.from_dict(node_beats_config.to_dict()), NodeBeatsConfig)
        assert NodeBeatsConfig.from_dict(node_beats_config.to_dict()).to_dict() == node_beats_config.to_dict()
        assert NodeBeatsConfig.from_dict(node_beats_config.to_dict()) == node_beats_config

    def test_beats_config(self) -> None:
        """
        Tests creation and dict conversion of the BeatsConfig DAO

        :return: None
        """
        node_beats_config = NodeBeatsConfig(
            ip="192.168.5.1", log_files_paths=["log1"], filebeat_modules=["mod1"], metricbeat_modules=["mod2"],
            heartbeat_hosts_to_monitor=["192.168.5.7"], kafka_input=False, start_heartbeat_automatically=True,
            start_packetbeat_automatically=True, start_metricbeat_automatically=True, start_filebeat_automatically=True
        )
        beats_config = BeatsConfig(
            node_beats_configs=[node_beats_config], num_elastic_shards=19, reload_enabled=False
        )
        assert isinstance(beats_config.to_dict(), dict)
        assert isinstance(BeatsConfig.from_dict(beats_config.to_dict()), BeatsConfig)
        assert BeatsConfig.from_dict(beats_config.to_dict()).to_dict() == beats_config.to_dict()
        assert BeatsConfig.from_dict(beats_config.to_dict()) == beats_config

    def test_client_managers_info(self) -> None:
        """
        Tests creation and dict conversion of the client_managers_info_dto

        :return: None
        """
        client_manager_status = ClientsDTO(
            num_clients=19, client_process_active=True, producer_active=False, clients_time_step_len_seconds=30,
            producer_time_step_len_seconds=30)
        client_managers_info = ClientManagersInfo(
            ips=["192.168.25.12"], ports=[2333], emulation_name="test_em", execution_id=19,
            client_managers_running=[True], client_managers_statuses=[client_manager_status])
        assert isinstance(client_managers_info.to_dict(), dict)
        assert isinstance(ClientManagersInfo.from_dict(client_managers_info.to_dict()), ClientManagersInfo)
        assert ClientManagersInfo.from_dict(client_managers_info.to_dict()).to_dict() == client_managers_info.to_dict()
        assert ClientManagersInfo.from_dict(client_managers_info.to_dict()) == client_managers_info

    def test_container_network(self) -> None:
        """
        Tests creation and dict conversion of the ContainerNetwork DTO

        :return: None
        """
        container_network = ContainerNetwork(
            name="testnet", subnet_mask="/24", bitmask="255.255.255.0", subnet_prefix="192.168.5", interface="eth1")
        assert isinstance(container_network.to_dict(), dict)
        assert isinstance(ContainerNetwork.from_dict(container_network.to_dict()), ContainerNetwork)
        assert ContainerNetwork.from_dict(container_network.to_dict()).to_dict() == container_network.to_dict()
        assert ContainerNetwork.from_dict(container_network.to_dict()) == container_network

    def test_cluster_node(self) -> None:
        """
        Tests creation and dict conversion of the ClusterNode DTO

        :return: None
        """
        cluster_node = ClusterNode(ip="192.168.5.1", leader=False, cpus=123, gpus=5, RAM=128)
        assert isinstance(cluster_node.to_dict(), dict)
        assert isinstance(ClusterNode.from_dict(cluster_node.to_dict()), ClusterNode)
        assert ClusterNode.from_dict(cluster_node.to_dict()).to_dict() == cluster_node.to_dict()
        assert ClusterNode.from_dict(cluster_node.to_dict()) == cluster_node

    def test_cluster_config(self) -> None:
        """
        Tests creation and dict conversion of the ClusterConfig DTO

        :return: None
        """
        cluster_node = ClusterNode(ip="192.168.5.1", leader=False, cpus=123, gpus=5, RAM=128)
        cluster_config = ClusterConfig(cluster_nodes=[cluster_node])
        assert isinstance(cluster_config.to_dict(), dict)
        assert isinstance(ClusterConfig.from_dict(cluster_config.to_dict()), ClusterConfig)
        assert ClusterConfig.from_dict(cluster_config.to_dict()).to_dict() == cluster_config.to_dict()
        assert ClusterConfig.from_dict(cluster_config.to_dict()) == cluster_config

    def test_config(self) -> None:
        """
        Tests creation and dict conversion of the Config DTO

        :return: None
        """
        cluster_node = ClusterNode(ip="192.168.5.1", leader=False, cpus=123, gpus=5, RAM=128)
        cluster_config = ClusterConfig(cluster_nodes=[cluster_node])
        config = Config(
            management_admin_email_default="admin",
            management_admin_username_default="admin",
            management_admin_password_default="admin",
            management_admin_first_name_default="admin",
            management_admin_last_name_default="admin",
            management_admin_organization_default="admin",
            management_guest_username_default="admin",
            management_guest_password_default="admin",
            management_guest_first_name_default="admin",
            management_guest_last_name_default="admin",
            management_guest_email_default="admin",
            management_guest_organization_default="admin",
            ssh_admin_username="admin",
            ssh_admin_password="admin",
            ssh_agent_username="admin",
            ssh_agent_password="admin",
            metastore_user="admin",
            metastore_password="admin",
            metastore_database_name="admin",
            metastore_ip="admin",
            node_exporter_port=23,
            grafana_port=23,
            management_system_port=23,
            cadvisor_port=23,
            prometheus_port=23,
            node_exporter_pid_file="admin",
            pgadmin_port=23,
            csle_mgmt_webapp_pid_file="admin",
            docker_stats_manager_log_file="admin",
            docker_stats_manager_log_dir="admin",
            docker_stats_manager_port=23,
            docker_stats_manager_max_workers=23,
            docker_stats_manager_outfile="admin",
            docker_stats_manager_pidfile="admin",
            prometheus_pid_file="admin",
            prometheus_log_file="admin",
            prometheus_config_file="admin",
            default_log_dir="admin",
            cluster_config=cluster_config,
            node_exporter_log_file="admin",
            allow_registration=True,
            grafana_username="admin",
            grafana_password="admin",
            pgadmin_username="admin",
            pgadmin_password="admin",
            postgresql_log_dir="admin",
            nginx_log_dir="admin",
            flask_log_file="admin",
            cluster_manager_log_file="admin"
        )
        assert isinstance(config.to_dict(), dict)
        assert isinstance(Config.from_dict(config.to_dict()), Config)
        assert Config.from_dict(config.to_dict()).to_dict() == config.to_dict()
        assert Config.from_dict(config.to_dict()) == config

    def test_credential(self) -> None:
        """
        Tests creation and dict conversion of the Credential DTO

        :return: None
        """
        credential = Credential(username="testuser", pw="testpw", port=9311, protocol=TransportProtocol.UDP,
                                service="test", root=True)
        assert isinstance(credential.to_dict(), dict)
        assert isinstance(Credential.from_dict(credential.to_dict()), Credential)
        assert Credential.from_dict(credential.to_dict()).to_dict() == credential.to_dict()
        assert Credential.from_dict(credential.to_dict()) == credential

    def test_default_network_firewall_config(self) -> None:
        """
        Tests creation and dict conversion of the DefaultNetworkFirewallConfig DTO

        :return: None
        """
        container_network = ContainerNetwork(
            name="testnet", subnet_mask="/24", bitmask="255.255.255.0", subnet_prefix="192.168.5", interface="eth1")
        default_net_fw_config = DefaultNetworkFirewallConfig(
            ip="192.168.5.1", default_gw="192.168.5.29", default_output="ACCEPT", default_input="DROP",
            default_forward="ACCEPT", network=container_network
        )
        assert isinstance(default_net_fw_config.to_dict(), dict)
        assert isinstance(DefaultNetworkFirewallConfig.from_dict(default_net_fw_config.to_dict()),
                          DefaultNetworkFirewallConfig)
        assert DefaultNetworkFirewallConfig.from_dict(default_net_fw_config.to_dict()).to_dict() == \
               default_net_fw_config.to_dict()
        assert DefaultNetworkFirewallConfig.from_dict(default_net_fw_config.to_dict()) == default_net_fw_config

    def test_docker_stats_manager_config(self) -> None:
        """
        Tests creation and dict conversion of the DockerStatsManagerConfig DTO

        :return: None
        """
        docker_statsmanager_config = DockerStatsManagerConfig(
            docker_stats_manager_log_file="testlog", docker_stats_manager_log_dir="logdir",
            docker_stats_manager_max_workers=10, time_step_len_seconds=30, docker_stats_manager_port=19, version="0.0.1"
        )
        assert isinstance(docker_statsmanager_config.to_dict(), dict)
        assert isinstance(DockerStatsManagerConfig.from_dict(docker_statsmanager_config.to_dict()),
                          DockerStatsManagerConfig)
        assert DockerStatsManagerConfig.from_dict(docker_statsmanager_config.to_dict()).to_dict() == \
               docker_statsmanager_config.to_dict()
        assert DockerStatsManagerConfig.from_dict(docker_statsmanager_config.to_dict()) == docker_statsmanager_config

    def test_docker_stats_managers_info(self) -> None:
        """
        Tests creation and dict conversion of the DockerStatsManagersInfo DTO

        :return: None
        """
        docker_stats_monitor_dto = DockerStatsMonitorDTO(num_monitors=1, emulations=["testem"],
                                                         emulation_executions=[15])
        docker_statsmanagers_info = DockerStatsManagersInfo(
            ips=["192.168.1.1"], ports=[3333], emulation_name="testem", execution_id=15,
            docker_stats_managers_statuses=[docker_stats_monitor_dto], docker_stats_managers_running=[True])
        assert isinstance(docker_statsmanagers_info.to_dict(), dict)
        assert isinstance(DockerStatsManagersInfo.from_dict(docker_statsmanagers_info.to_dict()),
                          DockerStatsManagersInfo)
        assert DockerStatsManagersInfo.from_dict(docker_statsmanagers_info.to_dict()).to_dict() == \
               docker_statsmanagers_info.to_dict()
        assert DockerStatsManagersInfo.from_dict(docker_statsmanagers_info.to_dict()) == docker_statsmanagers_info

    def test_node_network_config(self) -> None:
        """
        Tests creation and dict conversion of the NodeNetworkConfig DTO

        :return: None
        """
        node_network_config = NodeNetworkConfig(
            interface="eth0", limit_packets_queue=3000, packet_delay_ms=0.1,
            packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
            packet_delay_distribution=PacketDelayDistributionType.PARETO,
            packet_loss_type=PacketLossType.GEMODEL, packet_loss_rate_random_percentage=2,
            packet_loss_random_correlation_percentage=25, loss_state_markov_chain_p13=0.1,
            loss_state_markov_chain_p31=0.1, loss_state_markov_chain_p32=0.1, loss_state_markov_chain_p23=0.1,
            loss_state_markov_chain_p14=0.1, loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
            loss_gemodel_h=0.0001, loss_gemodel_k=0.9999)
        assert isinstance(node_network_config.to_dict(), dict)
        assert isinstance(NodeNetworkConfig.from_dict(node_network_config.to_dict()), NodeNetworkConfig)
        assert NodeNetworkConfig.from_dict(node_network_config.to_dict()).to_dict() == node_network_config.to_dict()
        assert NodeNetworkConfig.from_dict(node_network_config.to_dict()) == node_network_config

    def test_node_resources_config(self) -> None:
        """
        Tests creation and dict conversion of the NodeResourcesConfig DTO

        :return: None
        """
        node_network_config = NodeNetworkConfig(
            interface="eth0", limit_packets_queue=3000, packet_delay_ms=0.1,
            packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
            packet_delay_distribution=PacketDelayDistributionType.PARETO,
            packet_loss_type=PacketLossType.GEMODEL, packet_loss_rate_random_percentage=2,
            packet_loss_random_correlation_percentage=25, loss_state_markov_chain_p13=0.1,
            loss_state_markov_chain_p31=0.1, loss_state_markov_chain_p32=0.1, loss_state_markov_chain_p23=0.1,
            loss_state_markov_chain_p14=0.1, loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
            loss_gemodel_h=0.0001, loss_gemodel_k=0.9999)
        node_resources_config = NodeResourcesConfig(
            container_name="my_container", num_cpus=10, available_memory_gb=100,
            ips_and_network_configs=[("net_1", node_network_config)], docker_gw_bridge_ip="docker_gw",
            physical_host_ip="192.168.1.1")
        assert isinstance(node_resources_config.to_dict(), dict)
        assert isinstance(NodeResourcesConfig.from_dict(node_resources_config.to_dict()), NodeResourcesConfig)
        assert NodeResourcesConfig.from_dict(node_resources_config.to_dict()).to_dict() == \
               node_resources_config.to_dict()
        assert NodeResourcesConfig.from_dict(node_resources_config.to_dict()) == node_resources_config

    def test_node_container_config(self) -> None:
        """
        Tests creation and dict conversion of the NodeContainerConfig DTO

        :return: None
        """
        container_network = ContainerNetwork(
            name="testnet", subnet_mask="/24", bitmask="255.255.255.0", subnet_prefix="192.168.5", interface="eth1")
        node_container_config = NodeContainerConfig(
            name="node_name", ips_and_networks=[("net_1", container_network)], version="1.0.0", level="4",
            restart_policy="always", suffix="_2", os="Ubuntu", execution_ip_first_octet=15,
            docker_gw_bridge_ip="7.7.7.7", physical_host_ip="8.8.8.8"
        )
        assert isinstance(node_container_config.to_dict(), dict)
        assert isinstance(NodeContainerConfig.from_dict(node_container_config.to_dict()), NodeContainerConfig)
        assert NodeContainerConfig.from_dict(node_container_config.to_dict()).to_dict() == \
               node_container_config.to_dict()
        assert NodeContainerConfig.from_dict(node_container_config.to_dict()) == node_container_config

    def test_node_firewall_config(self) -> None:
        """
        Tests creation and dict conversion of the NodeFirewallConfig DTO

        :return: None
        """
        container_network = ContainerNetwork(
            name="testnet", subnet_mask="/24", bitmask="255.255.255.0", subnet_prefix="192.168.5", interface="eth1")
        default_net_fw_config = DefaultNetworkFirewallConfig(
            ip="192.168.5.1", default_gw="192.168.5.29", default_output="ACCEPT", default_input="DROP",
            default_forward="ACCEPT", network=container_network
        )
        route = ("8.8.8.8", "7.7.7.7")
        routes = set()
        routes.add(route)
        node_firewall_config = NodeFirewallConfig(
            hostname="my_hostname", output_accept=set("8.8.8.8"), input_accept=set("8.8.8.8"),
            forward_accept=set("8.8.8.8"), output_drop=set("8.8.8.8"), input_drop=set("8.8.8.8"),
            forward_drop=set("8.8.8.8"), routes=routes, docker_gw_bridge_ip="8.8.8.8",
            physical_host_ip="192.172.1.1", ips_gw_default_policy_networks=[default_net_fw_config]
        )
        assert isinstance(node_firewall_config.to_dict(), dict)
        assert isinstance(NodeFirewallConfig.from_dict(node_firewall_config.to_dict()), NodeFirewallConfig)
        assert NodeFirewallConfig.from_dict(node_firewall_config.to_dict()).to_dict() == node_firewall_config.to_dict()
        assert NodeFirewallConfig.from_dict(node_firewall_config.to_dict()) == node_firewall_config

    def test_elk_config(self) -> None:
        """
        Tests creation and dict conversion of the ElkConfig DTO

        :return: None
        """
        container_network = ContainerNetwork(
            name="testnet", subnet_mask="/24", bitmask="255.255.255.0", subnet_prefix="192.168.5", interface="eth1")
        node_container_config = NodeContainerConfig(
            name="node_name", ips_and_networks=[("net_1", container_network)], version="1.0.0", level="4",
            restart_policy="always", suffix="_2", os="Ubuntu", execution_ip_first_octet=15,
            docker_gw_bridge_ip="7.7.7.7", physical_host_ip="8.8.8.8"
        )
        node_network_config = NodeNetworkConfig(
            interface="eth0", limit_packets_queue=3000, packet_delay_ms=0.1,
            packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
            packet_delay_distribution=PacketDelayDistributionType.PARETO,
            packet_loss_type=PacketLossType.GEMODEL, packet_loss_rate_random_percentage=2,
            packet_loss_random_correlation_percentage=25, loss_state_markov_chain_p13=0.1,
            loss_state_markov_chain_p31=0.1, loss_state_markov_chain_p32=0.1, loss_state_markov_chain_p23=0.1,
            loss_state_markov_chain_p14=0.1, loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
            loss_gemodel_h=0.0001, loss_gemodel_k=0.9999)
        node_resources_config = NodeResourcesConfig(
            container_name="my_container", num_cpus=10, available_memory_gb=100,
            ips_and_network_configs=[("net_1", node_network_config)], docker_gw_bridge_ip="docker_gw",
            physical_host_ip="192.168.1.1")
        container_network = ContainerNetwork(
            name="testnet", subnet_mask="/24", bitmask="255.255.255.0", subnet_prefix="192.168.5", interface="eth1")
        default_net_fw_config = DefaultNetworkFirewallConfig(
            ip="192.168.5.1", default_gw="192.168.5.29", default_output="ACCEPT", default_input="DROP",
            default_forward="ACCEPT", network=container_network
        )
        route = ("8.8.8.8", "7.7.7.7")
        routes = set()
        routes.add(route)
        node_firewall_config = NodeFirewallConfig(
            hostname="my_hostname", output_accept=set("8.8.8.8"), input_accept=set("8.8.8.8"),
            forward_accept=set("8.8.8.8"), output_drop=set("8.8.8.8"), input_drop=set("8.8.8.8"),
            forward_drop=set("8.8.8.8"), routes=routes, docker_gw_bridge_ip="8.8.8.8",
            physical_host_ip="192.172.1.1", ips_gw_default_policy_networks=[default_net_fw_config]
        )
        elk_config = ElkConfig(
            container=node_container_config, resources=node_resources_config, firewall_config=node_firewall_config,
            elk_manager_log_file="elk_manager.log", elk_manager_log_dir="/", elk_manager_max_workers=10,
            elastic_port=9200, kibana_port=5601, logstash_port=5044, time_step_len_seconds=15, elk_manager_port=50045,
            version="0.0.1")
        assert isinstance(elk_config.to_dict(), dict)
        assert isinstance(ElkConfig.from_dict(elk_config.to_dict()), ElkConfig)
        assert ElkConfig.from_dict(elk_config.to_dict()).to_dict() == elk_config.to_dict()
        assert ElkConfig.from_dict(elk_config.to_dict()) == elk_config

    def test_elk_managers_info(self) -> None:
        """
        Tests creation and dict conversion of the ElkManagersInfo DTO

        :return: None
        """
        elk_dto = ElkDTO(elasticRunning=False, kibanaRunning=True, logstashRunning=True)
        elk_managers_info_info = ELKManagersInfo(
            ips=["192.168.1.1"], ports=[3333], emulation_name="testem", execution_id=15,
            elk_managers_statuses=[elk_dto], elk_managers_running=[True], local_kibana_port=5050,
            physical_server_ip="8.8.8.8")
        assert isinstance(elk_managers_info_info.to_dict(), dict)
        assert isinstance(ELKManagersInfo.from_dict(elk_managers_info_info.to_dict()),
                          ELKManagersInfo)
        assert ELKManagersInfo.from_dict(elk_managers_info_info.to_dict()).to_dict() == \
               elk_managers_info_info.to_dict()
        assert ELKManagersInfo.from_dict(elk_managers_info_info.to_dict()) == elk_managers_info_info

    def test_snort_managers_info(self) -> None:
        """
        Tests creation and dict conversion of the SnortManagersInfo DTO

        :return: None
        """
        snort_dto = SnortIdsMonitorDTO(monitor_running=True, snort_ids_running=True)
        snort_managers_info = SnortIdsManagersInfo(
            ips=["192.168.1.1"], ports=[3333], emulation_name="testem", execution_id=15,
            snort_ids_managers_statuses=[snort_dto], snort_ids_managers_running=[True])
        assert isinstance(snort_managers_info.to_dict(), dict)
        assert isinstance(SnortIdsManagersInfo.from_dict(snort_managers_info.to_dict()),
                          SnortIdsManagersInfo)
        assert SnortIdsManagersInfo.from_dict(snort_managers_info.to_dict()).to_dict() == \
               snort_managers_info.to_dict()
        assert SnortIdsManagersInfo.from_dict(snort_managers_info.to_dict()) == snort_managers_info

    def test_ossec_managers_info(self) -> None:
        """
        Tests creation and dict conversion of the OSSECIDSManagersInfo DTO

        :return: None
        """
        ossec_dto = OSSECIdsMonitorDTO(monitor_running=True, ossec_ids_running=True)
        ossec_managers_info = OSSECIDSManagersInfo(
            ips=["192.168.1.1"], ports=[3333], emulation_name="testem", execution_id=15,
            ossec_ids_managers_statuses=[ossec_dto], ossec_ids_managers_running=[True])
        assert isinstance(ossec_managers_info.to_dict(), dict)
        assert isinstance(OSSECIDSManagersInfo.from_dict(ossec_managers_info.to_dict()),
                          OSSECIDSManagersInfo)
        assert OSSECIDSManagersInfo.from_dict(ossec_managers_info.to_dict()).to_dict() == \
               ossec_managers_info.to_dict()
        assert OSSECIDSManagersInfo.from_dict(ossec_managers_info.to_dict()) == ossec_managers_info

    def test_ryu_managers_info(self) -> None:
        """
        Tests creation and dict conversion of the RyuManagersInfo DTO

        :return: None
        """
        ryu_dto = RyuDTO(ryu_running=True, monitor_running=False, port=3000, web_port=8080, controller="8.8.8.8",
                         kafka_ip="7.7.7.7", kafka_port=9090, time_step_len=30)
        ryu_managers_info = RyuManagersInfo(
            ips=["192.168.1.1"], ports=[3333], emulation_name="testem", execution_id=15,
            ryu_managers_statuses=[ryu_dto], ryu_managers_running=[True])
        assert isinstance(ryu_managers_info.to_dict(), dict)
        assert isinstance(RyuManagersInfo.from_dict(ryu_managers_info.to_dict()),
                          RyuManagersInfo)
        assert RyuManagersInfo.from_dict(ryu_managers_info.to_dict()).to_dict() == \
               ryu_managers_info.to_dict()
        assert RyuManagersInfo.from_dict(ryu_managers_info.to_dict()) == ryu_managers_info

    def test_host_managers_info(self) -> None:
        """
        Tests creation and dict conversion of the HostManagersInfo DTO

        :return: None
        """
        host_dto = HostStatusDTO(
            monitor_running=True, filebeat_running=False, packetbeat_running=True, metricbeat_running=True,
            heartbeat_running=False)
        host_managers_info = HostManagersInfo(
            ips=["192.168.1.1"], ports=[3333], emulation_name="testem", execution_id=15,
            host_managers_statuses=[host_dto], host_managers_running=[True])
        assert isinstance(host_managers_info.to_dict(), dict)
        assert isinstance(HostManagersInfo.from_dict(host_managers_info.to_dict()),
                          HostManagersInfo)
        assert HostManagersInfo.from_dict(host_managers_info.to_dict()).to_dict() == \
               host_managers_info.to_dict()
        assert HostManagersInfo.from_dict(host_managers_info.to_dict()) == host_managers_info

    def test_kafka_managers_info(self) -> None:
        """
        Tests creation and dict conversion of the KafkaManagersInfo DTO

        :return: None
        """
        kafka_dto = KafkaDTO(running=True, topics=["topic1"])
        kafka_managers_info = KafkaManagersInfo(
            ips=["192.168.1.1"], ports=[3333], emulation_name="testem", execution_id=15,
            kafka_managers_statuses=[kafka_dto], kafka_managers_running=[True])
        assert isinstance(kafka_managers_info.to_dict(), dict)
        assert isinstance(KafkaManagersInfo.from_dict(kafka_managers_info.to_dict()),
                          KafkaManagersInfo)
        assert KafkaManagersInfo.from_dict(kafka_managers_info.to_dict()).to_dict() == \
               kafka_managers_info.to_dict()
        assert KafkaManagersInfo.from_dict(kafka_managers_info.to_dict()) == kafka_managers_info

    def test_kafka_topic(self) -> None:
        """
        Tests creation and dict conversion of the KafkaTopic DTO

        :return: None
        """
        kafka_topic = KafkaTopic(name="testname", num_replicas=10, num_partitions=15, attributes=["attr1"],
                                 retention_time_hours=10)
        assert isinstance(kafka_topic.to_dict(), dict)
        assert isinstance(KafkaTopic.from_dict(kafka_topic.to_dict()), KafkaTopic)
        assert KafkaTopic.from_dict(kafka_topic.to_dict()).to_dict() == kafka_topic.to_dict()
        assert KafkaTopic.from_dict(kafka_topic.to_dict()) == kafka_topic

    def test_kafka_config(self) -> None:
        """
        Tests creation and dict conversion of the KafkaConfig DTO

        :return: None
        """
        container_network = ContainerNetwork(
            name="testnet", subnet_mask="/24", bitmask="255.255.255.0", subnet_prefix="192.168.5", interface="eth1")
        node_container_config = NodeContainerConfig(
            name="node_name", ips_and_networks=[("net_1", container_network)], version="1.0.0", level="4",
            restart_policy="always", suffix="_2", os="Ubuntu", execution_ip_first_octet=15,
            docker_gw_bridge_ip="7.7.7.7", physical_host_ip="8.8.8.8"
        )
        node_network_config = NodeNetworkConfig(
            interface="eth0", limit_packets_queue=3000, packet_delay_ms=0.1,
            packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
            packet_delay_distribution=PacketDelayDistributionType.PARETO,
            packet_loss_type=PacketLossType.GEMODEL, packet_loss_rate_random_percentage=2,
            packet_loss_random_correlation_percentage=25, loss_state_markov_chain_p13=0.1,
            loss_state_markov_chain_p31=0.1, loss_state_markov_chain_p32=0.1, loss_state_markov_chain_p23=0.1,
            loss_state_markov_chain_p14=0.1, loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
            loss_gemodel_h=0.0001, loss_gemodel_k=0.9999)
        node_resources_config = NodeResourcesConfig(
            container_name="my_container", num_cpus=10, available_memory_gb=100,
            ips_and_network_configs=[("net_1", node_network_config)], docker_gw_bridge_ip="docker_gw",
            physical_host_ip="192.168.1.1")
        container_network = ContainerNetwork(
            name="testnet", subnet_mask="/24", bitmask="255.255.255.0", subnet_prefix="192.168.5", interface="eth1")
        default_net_fw_config = DefaultNetworkFirewallConfig(
            ip="192.168.5.1", default_gw="192.168.5.29", default_output="ACCEPT", default_input="DROP",
            default_forward="ACCEPT", network=container_network
        )
        route = ("8.8.8.8", "7.7.7.7")
        routes = set()
        routes.add(route)
        node_firewall_config = NodeFirewallConfig(
            hostname="my_hostname", output_accept=set("8.8.8.8"), input_accept=set("8.8.8.8"),
            forward_accept=set("8.8.8.8"), output_drop=set("8.8.8.8"), input_drop=set("8.8.8.8"),
            forward_drop=set("8.8.8.8"), routes=routes, docker_gw_bridge_ip="8.8.8.8",
            physical_host_ip="192.172.1.1", ips_gw_default_policy_networks=[default_net_fw_config]
        )
        kafka_topic = KafkaTopic(name="testname", num_replicas=10, num_partitions=15, attributes=["attr1"],
                                 retention_time_hours=10)
        kafka_config = KafkaConfig(
            container=node_container_config, resources=node_resources_config, firewall_config=node_firewall_config,
            kafka_manager_log_file="elk_manager.log", kafka_manager_log_dir="/", kafka_manager_max_workers=10,
            time_step_len_seconds=15, kafka_manager_port=50045, version="0.0.1", topics=[kafka_topic])
        assert isinstance(kafka_config.to_dict(), dict)
        assert isinstance(KafkaConfig.from_dict(kafka_config.to_dict()), KafkaConfig)
        assert KafkaConfig.from_dict(kafka_config.to_dict()).to_dict() == kafka_config.to_dict()
        assert KafkaConfig.from_dict(kafka_config.to_dict()) == kafka_config

    def test_network_service(self) -> None:
        """
        Tests creation and dict conversion of the NetworkService DTO

        :return: None
        """
        credential = Credential(username="testuser", pw="testpw", port=9311, protocol=TransportProtocol.UDP,
                                service="test", root=True)
        network_service = NetworkService(protocol=TransportProtocol.UDP, port=3000, name="testservice",
                                         credentials=[credential])
        assert isinstance(network_service.to_dict(), dict)
        assert isinstance(NetworkService.from_dict(network_service.to_dict()), NetworkService)
        assert NetworkService.from_dict(network_service.to_dict()).to_dict() == network_service.to_dict()
        assert NetworkService.from_dict(network_service.to_dict()) == network_service

    def test_flag(self) -> None:
        """
        Tests creation and dict conversion of the Flag DTO

        :return: None
        """
        flag = Flag(name="testflag", dir="/", id=10, path="/test.txt", requires_root=False, score=10)
        assert isinstance(flag.to_dict(), dict)
        assert isinstance(Flag.from_dict(flag.to_dict()), Flag)
        assert Flag.from_dict(flag.to_dict()).to_dict() == flag.to_dict()
        assert Flag.from_dict(flag.to_dict()) == flag

    def test_node_flags_config(self) -> None:
        """
        Tests creation and dict conversion of the NodeFlagsConfig DTO

        :return: None
        """
        flag = Flag(name="testflag", dir="/", id=10, path="/test.txt", requires_root=False, score=10)
        node_flags_config = NodeFlagsConfig(
            ip="8.8.8.8", flags=[flag], docker_gw_bridge_ip="9.9.9.9", physical_host_ip="168.22.11.2")
        assert isinstance(node_flags_config.to_dict(), dict)
        assert isinstance(NodeFlagsConfig.from_dict(node_flags_config.to_dict()), NodeFlagsConfig)
        assert NodeFlagsConfig.from_dict(node_flags_config.to_dict()).to_dict() == node_flags_config.to_dict()
        assert NodeFlagsConfig.from_dict(node_flags_config.to_dict()) == node_flags_config

    def test_node_services_config(self) -> None:
        """
        Tests creation and dict conversion of the NodeServicesConfig DTO

        :return: None
        """
        credential = Credential(username="testuser", pw="testpw", port=9311, protocol=TransportProtocol.UDP,
                                service="test", root=True)
        network_service = NetworkService(protocol=TransportProtocol.UDP, port=3000, name="testservice",
                                         credentials=[credential])
        node_services_config = NodeServicesConfig(ip="8.8.8.8", services=[network_service])
        assert isinstance(node_services_config.to_dict(), dict)
        assert isinstance(NodeServicesConfig.from_dict(node_services_config.to_dict()), NodeServicesConfig)
        assert NodeServicesConfig.from_dict(node_services_config.to_dict()).to_dict() == node_services_config.to_dict()
        assert NodeServicesConfig.from_dict(node_services_config.to_dict()) == node_services_config

    def test_node_traffic_config(self) -> None:
        """
        Tests creation and dict conversion of the NodeTrafficConfig DTO

        :return: None
        """
        node_traffic_config = NodeTrafficConfig(
            ip="8.8.8.8", commands=["ls"], traffic_manager_log_file="traffic_manager.log", traffic_manager_log_dir="/",
            traffic_manager_port=3000, traffic_manager_max_workers=10, docker_gw_bridge_ip="8.8.8.8",
            physical_host_ip="7.7.7.7")
        assert isinstance(node_traffic_config.to_dict(), dict)
        assert isinstance(NodeTrafficConfig.from_dict(node_traffic_config.to_dict()), NodeTrafficConfig)
        assert NodeTrafficConfig.from_dict(node_traffic_config.to_dict()).to_dict() == node_traffic_config.to_dict()
        assert NodeTrafficConfig.from_dict(node_traffic_config.to_dict()) == node_traffic_config

    def test_user(self) -> None:
        """
        Tests creation and dict conversion of the User DTO

        :return: None
        """
        user = User(username="testuser", pw="mypw", root=True)
        assert isinstance(user.to_dict(), dict)
        assert isinstance(User.from_dict(user.to_dict()), User)
        assert User.from_dict(user.to_dict()).to_dict() == user.to_dict()
        assert User.from_dict(user.to_dict()) == user

    def test_node_users_config(self) -> None:
        """
        Tests creation and dict conversion of the NodeUsersConfig DTO

        :return: None
        """
        user = User(username="testuser", pw="mypw", root=True)
        node_users_config = NodeUsersConfig(
            ip="8.8.8.8", docker_gw_bridge_ip="8.8.8.8", physical_host_ip="7.7.7.7", users=[user])
        assert isinstance(node_users_config.to_dict(), dict)
        assert isinstance(NodeUsersConfig.from_dict(node_users_config.to_dict()), NodeUsersConfig)
        assert NodeUsersConfig.from_dict(node_users_config.to_dict()).to_dict() == node_users_config.to_dict()
        assert NodeUsersConfig.from_dict(node_users_config.to_dict()) == node_users_config

    def test_node_vulnerability_config(self) -> None:
        """
        Tests creation and dict conversion of the NodeVulnerabilitiesConfig DTO

        :return: None
        """
        credential = Credential(username="testuser", pw="testpw", port=9311, protocol=TransportProtocol.UDP,
                                service="test", root=True)
        node_vuln_config = NodeVulnerabilityConfig(
            ip="8.8.8.8", docker_gw_bridge_ip="8.8.8.8", physical_host_ip="7.7.7.7",
            vuln_type=VulnType.RCE, protocol=TransportProtocol.TCP, credentials=[credential], cvss=2.0, cve="test_cve",
            service="myserv", root=True, name="testname", port=2510)
        assert isinstance(node_vuln_config.to_dict(), dict)
        assert isinstance(NodeVulnerabilityConfig.from_dict(node_vuln_config.to_dict()), NodeVulnerabilityConfig)
        assert NodeVulnerabilityConfig.from_dict(node_vuln_config.to_dict()).to_dict() == node_vuln_config.to_dict()
        assert NodeVulnerabilityConfig.from_dict(node_vuln_config.to_dict()) == node_vuln_config

    def test_ossec_ids_manager_config(self) -> None:
        """
        Tests creation and dict conversion of the OSSECIDSManagerConfig DTO

        :return: None
        """
        ossec_ids_manager_config = OSSECIDSManagerConfig(
            ossec_ids_manager_log_file="ossec.log", ossec_ids_manager_log_dir="/", ossec_ids_manager_max_workers=10,
            time_step_len_seconds=30, ossec_ids_manager_port=1515, version="0.0.1")
        assert isinstance(ossec_ids_manager_config.to_dict(), dict)
        assert isinstance(OSSECIDSManagerConfig.from_dict(ossec_ids_manager_config.to_dict()), OSSECIDSManagerConfig)
        assert OSSECIDSManagerConfig.from_dict(ossec_ids_manager_config.to_dict()).to_dict() == \
               ossec_ids_manager_config.to_dict()
        assert OSSECIDSManagerConfig.from_dict(ossec_ids_manager_config.to_dict()) == ossec_ids_manager_config

    def test_ovs_switch_config(self) -> None:
        """
        Tests creation and dict conversion of the OVSConfig DTO

        :return: None
        """
        ovs_switch_config = OvsSwitchConfig(
            container_name="testcontainer", ip="8.8.8.8", openflow_protocols=["v1.0.0"], controller_ip="8.8.8.8",
            controller_port=3000, controller_transport_protocol="UDP", docker_gw_bridge_ip="8.8.8.8",
            physical_host_ip="168.156.2.2")
        assert isinstance(ovs_switch_config.to_dict(), dict)
        assert isinstance(OvsSwitchConfig.from_dict(ovs_switch_config.to_dict()), OvsSwitchConfig)
        assert OvsSwitchConfig.from_dict(ovs_switch_config.to_dict()).to_dict() == ovs_switch_config.to_dict()
        assert OvsSwitchConfig.from_dict(ovs_switch_config.to_dict()) == ovs_switch_config

    def test_ovs_config(self) -> None:
        """
        Tests creation and dict conversion of the OVSConfig DTO

        :return: None
        """
        ovs_switch_config = OvsSwitchConfig(
            container_name="testcontainer", ip="8.8.8.8", openflow_protocols=["v1.0.0"], controller_ip="8.8.8.8",
            controller_port=3000, controller_transport_protocol="UDP", docker_gw_bridge_ip="8.8.8.8",
            physical_host_ip="168.156.2.2")
        ovs_config = OVSConfig(switch_configs=[ovs_switch_config])
        assert isinstance(ovs_config.to_dict(), dict)
        assert isinstance(OVSConfig.from_dict(ovs_config.to_dict()), OVSConfig)
        assert OVSConfig.from_dict(ovs_config.to_dict()).to_dict() == ovs_config.to_dict()
        assert OVSConfig.from_dict(ovs_config.to_dict()) == ovs_config

    def test_resources_config(self) -> None:
        """
        Tests creation and dict conversion of the ResourcesConfig DTO

        :return: None
        """
        node_network_config = NodeNetworkConfig(
            interface="eth0", limit_packets_queue=3000, packet_delay_ms=0.1,
            packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
            packet_delay_distribution=PacketDelayDistributionType.PARETO,
            packet_loss_type=PacketLossType.GEMODEL, packet_loss_rate_random_percentage=2,
            packet_loss_random_correlation_percentage=25, loss_state_markov_chain_p13=0.1,
            loss_state_markov_chain_p31=0.1, loss_state_markov_chain_p32=0.1, loss_state_markov_chain_p23=0.1,
            loss_state_markov_chain_p14=0.1, loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
            loss_gemodel_h=0.0001, loss_gemodel_k=0.9999)
        node_resources_config = NodeResourcesConfig(
            container_name="my_container", num_cpus=10, available_memory_gb=100,
            ips_and_network_configs=[("net_1", node_network_config)], docker_gw_bridge_ip="docker_gw",
            physical_host_ip="192.168.1.1")
        resources_config = ResourcesConfig(node_resources_configurations=[node_resources_config])
        assert isinstance(resources_config.to_dict(), dict)
        assert isinstance(ResourcesConfig.from_dict(resources_config.to_dict()), ResourcesConfig)
        assert ResourcesConfig.from_dict(resources_config.to_dict()).to_dict() == resources_config.to_dict()
        assert ResourcesConfig.from_dict(resources_config.to_dict()) == resources_config

    def test_sdn_controller_config(self) -> None:
        """
        Tests creation and dict conversion of the ResourcesConfig DTO

        :return: None
        """
        node_network_config = NodeNetworkConfig(
            interface="eth0", limit_packets_queue=3000, packet_delay_ms=0.1,
            packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
            packet_delay_distribution=PacketDelayDistributionType.PARETO,
            packet_loss_type=PacketLossType.GEMODEL, packet_loss_rate_random_percentage=2,
            packet_loss_random_correlation_percentage=25, loss_state_markov_chain_p13=0.1,
            loss_state_markov_chain_p31=0.1, loss_state_markov_chain_p32=0.1, loss_state_markov_chain_p23=0.1,
            loss_state_markov_chain_p14=0.1, loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
            loss_gemodel_h=0.0001, loss_gemodel_k=0.9999)
        node_resources_config = NodeResourcesConfig(
            container_name="my_container", num_cpus=10, available_memory_gb=100,
            ips_and_network_configs=[("net_1", node_network_config)], docker_gw_bridge_ip="docker_gw",
            physical_host_ip="192.168.1.1")
        container_network = ContainerNetwork(
            name="testnet", subnet_mask="/24", bitmask="255.255.255.0", subnet_prefix="192.168.5", interface="eth1")
        default_net_fw_config = DefaultNetworkFirewallConfig(
            ip="192.168.5.1", default_gw="192.168.5.29", default_output="ACCEPT", default_input="DROP",
            default_forward="ACCEPT", network=container_network
        )
        node_container_config = NodeContainerConfig(
            name="node_name", ips_and_networks=[("net_1", container_network)], version="1.0.0", level="4",
            restart_policy="always", suffix="_2", os="Ubuntu", execution_ip_first_octet=15,
            docker_gw_bridge_ip="7.7.7.7", physical_host_ip="8.8.8.8"
        )
        route = ("8.8.8.8", "7.7.7.7")
        routes = set()
        routes.add(route)
        node_firewall_config = NodeFirewallConfig(
            hostname="my_hostname", output_accept=set("8.8.8.8"), input_accept=set("8.8.8.8"),
            forward_accept=set("8.8.8.8"), output_drop=set("8.8.8.8"), input_drop=set("8.8.8.8"),
            forward_drop=set("8.8.8.8"), routes=routes, docker_gw_bridge_ip="8.8.8.8",
            physical_host_ip="192.172.1.1", ips_gw_default_policy_networks=[default_net_fw_config]
        )
        sdn_controller_config = SDNControllerConfig(
            manager_port=50042, version="0.0.1", time_step_len_seconds=15, manager_max_workers=10, manager_log_dir="/",
            manager_log_file="sdn.log", controller_port=7070, controller_module_name="learning_switch",
            controller_type=SDNControllerType.RYU, firewall_config=node_firewall_config,
            resources=node_resources_config, container=node_container_config, controller_web_api_port=6060
        )
        assert isinstance(sdn_controller_config.to_dict(), dict)
        assert isinstance(SDNControllerConfig.from_dict(sdn_controller_config.to_dict()), SDNControllerConfig)
        assert SDNControllerConfig.from_dict(sdn_controller_config.to_dict()).to_dict() == \
               sdn_controller_config.to_dict()
        assert SDNControllerConfig.from_dict(sdn_controller_config.to_dict()) == sdn_controller_config

    def test_services_config(self) -> None:
        """
        Tests creation and dict conversion of the ServicesConfig DTO

        :return: None
        """
        credential = Credential(username="testuser", pw="testpw", port=9311, protocol=TransportProtocol.UDP,
                                service="test", root=True)
        network_service = NetworkService(protocol=TransportProtocol.UDP, port=3000, name="testservice",
                                         credentials=[credential])
        node_services_config = NodeServicesConfig(ip="8.8.8.8", services=[network_service])
        services_config = ServicesConfig(services_configs=[node_services_config])
        assert isinstance(services_config.to_dict(), dict)
        assert isinstance(ServicesConfig.from_dict(services_config.to_dict()), ServicesConfig)
        assert ServicesConfig.from_dict(services_config.to_dict()).to_dict() == services_config.to_dict()
        assert ServicesConfig.from_dict(services_config.to_dict()) == services_config

    def test_users_config(self) -> None:
        """
        Tests creation and dict conversion of the UsersConfig DTO

        :return: None
        """
        user = User(username="testuser", pw="mypw", root=True)
        node_users_config = NodeUsersConfig(
            ip="8.8.8.8", docker_gw_bridge_ip="8.8.8.8", physical_host_ip="7.7.7.7", users=[user])
        users_config = UsersConfig(users_configs=[node_users_config])
        assert isinstance(users_config.to_dict(), dict)
        assert isinstance(UsersConfig.from_dict(users_config.to_dict()), UsersConfig)
        assert UsersConfig.from_dict(users_config.to_dict()).to_dict() == users_config.to_dict()
        assert UsersConfig.from_dict(users_config.to_dict()) == users_config

    def test_arrival_config(self) -> None:
        """
        Tests creation and dict conversion of the ArrivalConfig DTO

        :return: None
        """
        arrival_config = ConstantArrivalConfig(lamb=10.0)
        assert isinstance(arrival_config.to_dict(), dict)
        assert isinstance(ConstantArrivalConfig.from_dict(arrival_config.to_dict()), ConstantArrivalConfig)
        assert ConstantArrivalConfig.from_dict(arrival_config.to_dict()).to_dict() == arrival_config.to_dict()
        assert ConstantArrivalConfig.from_dict(arrival_config.to_dict()) == arrival_config

    def test_client(self) -> None:
        """
        Tests creation and dict conversion of the Client DTO

        :return: None
        """
        arrival_config = ConstantArrivalConfig(lamb=10.0)
        client = Client(id=10, workflow_distribution=[1], arrival_config=arrival_config, mu=4.0,
                        exponential_service_time=True)
        assert isinstance(client.to_dict(), dict)
        assert isinstance(Client.from_dict(client.to_dict()), Client)
        assert Client.from_dict(client.to_dict()).to_dict() == client.to_dict()
        assert Client.from_dict(client.to_dict()) == client

    def test_workflows_service(self) -> None:
        """n
        Tests creation and dict conversion of the WorkflowService DTO

        :return: None
        """
        workflows_service = WorkflowService(ips_and_commands=[("8.8.8.8", ["ls"])], id=10)
        assert isinstance(workflows_service.to_dict(), dict)
        assert isinstance(WorkflowService.from_dict(workflows_service.to_dict()), WorkflowService)
        assert WorkflowService.from_dict(workflows_service.to_dict()).to_dict() == workflows_service.to_dict()
        assert WorkflowService.from_dict(workflows_service.to_dict()) == workflows_service

    def test_workflow_markov_chain(self) -> None:
        """n
        Tests creation and dict conversion of the WorkflowMarkovChain DTO

        :return: None
        """
        workflow_mc = WorkflowMarkovChain(transition_matrix=[[0.2, 0.8]], initial_state=10, id=1)
        assert isinstance(workflow_mc.to_dict(), dict)
        assert isinstance(WorkflowMarkovChain.from_dict(workflow_mc.to_dict()), WorkflowMarkovChain)
        assert WorkflowMarkovChain.from_dict(workflow_mc.to_dict()).to_dict() == workflow_mc.to_dict()
        assert WorkflowMarkovChain.from_dict(workflow_mc.to_dict()) == workflow_mc

    def test_workflows_config(self) -> None:
        """n
        Tests creation and dict conversion of the WorkflowsConfig DTO

        :return: None
        """
        workflow_mc = WorkflowMarkovChain(transition_matrix=[[0.2, 0.8]], initial_state=10, id=1)
        workflows_service = WorkflowService(ips_and_commands=[("8.8.8.8", ["ls"])], id=10)
        workflows_config = WorkflowsConfig(workflow_markov_chains=[workflow_mc], workflow_services=[workflows_service])
        assert isinstance(workflows_config.to_dict(), dict)
        assert isinstance(WorkflowsConfig.from_dict(workflows_config.to_dict()), WorkflowsConfig)
        assert WorkflowsConfig.from_dict(workflows_config.to_dict()).to_dict() == workflows_config.to_dict()
        assert WorkflowsConfig.from_dict(workflows_config.to_dict()) == workflows_config

    def test_client_population_config(self) -> None:
        """
        Tests creation and dict conversion of the ClientPopulationConfig DTO

        :return: None
        """
        workflow_mc = WorkflowMarkovChain(transition_matrix=[[0.2, 0.8]], initial_state=10, id=1)
        workflows_service = WorkflowService(ips_and_commands=[("8.8.8.8", ["ls"])], id=10)
        workflows_config = WorkflowsConfig(workflow_markov_chains=[workflow_mc], workflow_services=[workflows_service])
        arrival_config = ConstantArrivalConfig(lamb=10.0)
        client = Client(id=10, workflow_distribution=[1], arrival_config=arrival_config, mu=4.0,
                        exponential_service_time=True)
        container_network = ContainerNetwork(
            name="testnet", subnet_mask="/24", bitmask="255.255.255.0", subnet_prefix="192.168.5", interface="eth1")
        client_population_config = ClientPopulationConfig(
            ip="8.8.8.8", networks=[container_network], client_manager_port=2020,
            client_manager_log_file="client_manager.log",
            client_manager_log_dir="/", client_manager_max_workers=10, clients=[client],
            workflows_config=workflows_config,
            client_time_step_len_seconds=30, docker_gw_bridge_ip="7.7.7.7", physical_host_ip="1.1.1.1",
        )
        assert isinstance(client_population_config.to_dict(), dict)
        assert isinstance(ClientPopulationConfig.from_dict(client_population_config.to_dict()), ClientPopulationConfig)
        assert ClientPopulationConfig.from_dict(client_population_config.to_dict()).to_dict() == \
               client_population_config.to_dict()
        assert ClientPopulationConfig.from_dict(client_population_config.to_dict()) == client_population_config

    def test_traffic_config(self) -> None:
        """
        Tests creation and dict conversion of the TrafficConfig DTO

        :return: None
        """
        workflow_mc = WorkflowMarkovChain(transition_matrix=[[0.2, 0.8]], initial_state=10, id=1)
        workflows_service = WorkflowService(ips_and_commands=[("8.8.8.8", ["ls"])], id=10)
        workflows_config = WorkflowsConfig(workflow_markov_chains=[workflow_mc], workflow_services=[workflows_service])
        arrival_config = ConstantArrivalConfig(lamb=10.0)
        client = Client(id=10, workflow_distribution=[1], arrival_config=arrival_config, mu=4.0,
                        exponential_service_time=True)
        container_network = ContainerNetwork(
            name="testnet", subnet_mask="/24", bitmask="255.255.255.0", subnet_prefix="192.168.5", interface="eth1")
        client_population_config = ClientPopulationConfig(
            ip="8.8.8.8", networks=[container_network], client_manager_port=2020,
            client_manager_log_file="client_manager.log",
            client_manager_log_dir="/", client_manager_max_workers=10, clients=[client],
            workflows_config=workflows_config,
            client_time_step_len_seconds=30, docker_gw_bridge_ip="7.7.7.7", physical_host_ip="1.1.1.1"
        )
        node_traffic_config = NodeTrafficConfig(
            ip="8.8.8.8", commands=["ls"], traffic_manager_log_file="traffic_manager.log", traffic_manager_log_dir="/",
            traffic_manager_port=3000, traffic_manager_max_workers=10, docker_gw_bridge_ip="8.8.8.8",
            physical_host_ip="7.7.7.7")
        traffic_config = TrafficConfig(node_traffic_configs=[node_traffic_config],
                                       client_population_config=client_population_config)
        assert isinstance(traffic_config.to_dict(), dict)
        assert isinstance(TrafficConfig.from_dict(traffic_config.to_dict()), TrafficConfig)
        assert TrafficConfig.from_dict(traffic_config.to_dict()).to_dict() == traffic_config.to_dict()
        assert TrafficConfig.from_dict(traffic_config.to_dict()) == traffic_config

    def test_vulnerabilities_config(self) -> None:
        """
        Tests creation and dict conversion of the VulnerabilitiesConfig DTO

        :return: None
        """
        credential = Credential(username="testuser", pw="testpw", port=9311, protocol=TransportProtocol.UDP,
                                service="test", root=True)
        node_vuln_config = NodeVulnerabilityConfig(
            ip="8.8.8.8", docker_gw_bridge_ip="8.8.8.8", physical_host_ip="7.7.7.7",
            vuln_type=VulnType.RCE, protocol=TransportProtocol.TCP, credentials=[credential], cvss=2.0, cve="test_cve",
            service="myserv", root=True, name="testname", port=2510)
        vuln_config = VulnerabilitiesConfig(node_vulnerability_configs=[node_vuln_config])
        assert isinstance(vuln_config.to_dict(), dict)
        assert isinstance(VulnerabilitiesConfig.from_dict(vuln_config.to_dict()), VulnerabilitiesConfig)
        assert VulnerabilitiesConfig.from_dict(vuln_config.to_dict()).to_dict() == vuln_config.to_dict()
        assert VulnerabilitiesConfig.from_dict(vuln_config.to_dict()) == vuln_config

    def test_emulation_connection_obs_state(self) -> None:
        """
        Tests creation and dict conversion of the VulnerabilitiesConfig DTO

        :return: None
        """
        credential = Credential(username="testuser", pw="testpw", port=9311, protocol=TransportProtocol.UDP,
                                service="test", root=True)
        emulation_connection_obs_state = EmulationConnectionObservationState(
            conn=None, credential=credential, root=True, service="serv", port=3030, tunnel_port=4000,
            tunnel_thread=None, interactive_shell=None, proxy=None, ip="8.8.8.8")
        assert isinstance(emulation_connection_obs_state.to_dict(), dict)
        assert isinstance(EmulationConnectionObservationState.from_dict(emulation_connection_obs_state.to_dict()),
                          EmulationConnectionObservationState)
        assert EmulationConnectionObservationState.from_dict(emulation_connection_obs_state.to_dict()).to_dict() \
               == emulation_connection_obs_state.to_dict()
        assert EmulationConnectionObservationState.from_dict(emulation_connection_obs_state.to_dict()) \
               == emulation_connection_obs_state

    def test_connection_setup_dto(self) -> None:
        """
        Tests creation and dict conversion of the ConnectionSetup DTO

        :return: None
        """
        credential = Credential(username="testuser", pw="testpw", port=9311, protocol=TransportProtocol.UDP,
                                service="test", root=True)
        emulation_connection_obs_state = EmulationConnectionObservationState(
            conn=None, credential=credential, root=True, service="serv", port=3030, tunnel_port=4000,
            tunnel_thread=None, interactive_shell=None, proxy=None, ip="8.8.8.8")
        conn_setup = ConnectionSetupDTO(
            connected=True, credentials=[credential], target_connections=[], tunnel_threads=[], forward_ports=[1101],
            ports=[3030], interactive_shells=[], non_failed_credentials=[credential],
            proxies=[emulation_connection_obs_state], ip="5.5.5.5", total_time=0.0)
        assert isinstance(conn_setup.to_dict(), dict)
        assert isinstance(ConnectionSetupDTO.from_dict(conn_setup.to_dict()), ConnectionSetupDTO)
        assert ConnectionSetupDTO.from_dict(conn_setup.to_dict()).to_dict() == conn_setup.to_dict()
        assert ConnectionSetupDTO.from_dict(conn_setup.to_dict()) == conn_setup

    def test_containers_config(self) -> None:
        """
        Tests creation and dict conversion of the ContainersConfig DTO

        :return: None
        """
        container_network = ContainerNetwork(
            name="testnet", subnet_mask="/24", bitmask="255.255.255.0", subnet_prefix="192.168.5", interface="eth1")
        node_container_config = NodeContainerConfig(
            name="node_name", ips_and_networks=[("net_1", container_network)], version="1.0.0", level="4",
            restart_policy="always", suffix="_2", os="Ubuntu", execution_ip_first_octet=15,
            docker_gw_bridge_ip="7.7.7.7", physical_host_ip="8.8.8.8"
        )
        containers_config = ContainersConfig(containers=[node_container_config], agent_ip="5.5.5.5",
                                             router_ip="2.2.2.2",
                                             networks=[container_network],
                                             ids_enabled=True, vulnerable_nodes=None, agent_reachable_nodes=None)
        assert isinstance(containers_config.to_dict(), dict)
        assert isinstance(ContainersConfig.from_dict(containers_config.to_dict()), ContainersConfig)
        assert ContainersConfig.from_dict(containers_config.to_dict()).to_dict() == containers_config.to_dict()
        assert ContainersConfig.from_dict(containers_config.to_dict()) == containers_config

    def test_flags_config(self) -> None:
        """
        Tests creation and dict conversion of the FlagsConfig DTO

        :return: None
        """
        flag = Flag(name="testflag", dir="/", id=10, path="/test.txt", requires_root=False, score=10)
        node_flags_config = NodeFlagsConfig(
            ip="8.8.8.8", flags=[flag], docker_gw_bridge_ip="9.9.9.9", physical_host_ip="168.22.11.2")
        flags_config = FlagsConfig(node_flag_configs=[node_flags_config])
        assert isinstance(flags_config.to_dict(), dict)
        assert isinstance(FlagsConfig.from_dict(flags_config.to_dict()), FlagsConfig)
        assert FlagsConfig.from_dict(flags_config.to_dict()).to_dict() == flags_config.to_dict()
        assert FlagsConfig.from_dict(flags_config.to_dict()) == flags_config

    def test_topology_config(self) -> None:
        """
        Tests creation and dict conversion of the TopologyConfig DTO

        :return: None
        """
        container_network = ContainerNetwork(
            name="testnet", subnet_mask="/24", bitmask="255.255.255.0", subnet_prefix="192.168.5", interface="eth1")
        default_net_fw_config = DefaultNetworkFirewallConfig(
            ip="192.168.5.1", default_gw="192.168.5.29", default_output="ACCEPT", default_input="DROP",
            default_forward="ACCEPT", network=container_network
        )
        route = ("8.8.8.8", "7.7.7.7")
        routes = set()
        routes.add(route)
        node_firewall_config = NodeFirewallConfig(
            hostname="my_hostname", output_accept=set("8.8.8.8"), input_accept=set("8.8.8.8"),
            forward_accept=set("8.8.8.8"), output_drop=set("8.8.8.8"), input_drop=set("8.8.8.8"),
            forward_drop=set("8.8.8.8"), routes=routes, docker_gw_bridge_ip="8.8.8.8",
            physical_host_ip="192.172.1.1", ips_gw_default_policy_networks=[default_net_fw_config]
        )
        topology_config = TopologyConfig(subnetwork_masks=["255.255.255.0"],
                                         node_configs=[node_firewall_config])
        assert isinstance(topology_config.to_dict(), dict)
        assert isinstance(TopologyConfig.from_dict(topology_config.to_dict()), TopologyConfig)
        assert TopologyConfig.from_dict(topology_config.to_dict()).to_dict() == topology_config.to_dict()
        assert TopologyConfig.from_dict(topology_config.to_dict()) == topology_config

    def test_host_manager_config(self) -> None:
        """
        Tests creation and dict conversion of the HostManagerConfig DTO

        :return: None
        """
        host_manager_config = HostManagerConfig(
            host_manager_log_file="host_manager.log", host_manager_log_dir="/", host_manager_max_workers=10,
            time_step_len_seconds=30, host_manager_port=3000, version="0.0.1")
        assert isinstance(host_manager_config.to_dict(), dict)
        assert isinstance(HostManagerConfig.from_dict(host_manager_config.to_dict()), HostManagerConfig)
        assert HostManagerConfig.from_dict(host_manager_config.to_dict()).to_dict() == host_manager_config.to_dict()
        assert HostManagerConfig.from_dict(host_manager_config.to_dict()) == host_manager_config

    def test_snort_ids_manager_config(self) -> None:
        """
        Tests creation and dict conversion of the SnortIDSManagerConfig DTO

        :return: None
        """
        snort_ids_manager_config = SnortIDSManagerConfig(
            snort_ids_manager_log_file="snort.log", snort_ids_manager_log_dir="/", snort_ids_manager_max_workers=10,
            time_step_len_seconds=30, snort_ids_manager_port=4000, version="0.0.1")
        assert isinstance(snort_ids_manager_config.to_dict(), dict)
        assert isinstance(SnortIDSManagerConfig.from_dict(snort_ids_manager_config.to_dict()), SnortIDSManagerConfig)
        assert SnortIDSManagerConfig.from_dict(snort_ids_manager_config.to_dict()).to_dict() == \
               snort_ids_manager_config.to_dict()
        assert SnortIDSManagerConfig.from_dict(snort_ids_manager_config.to_dict()) == snort_ids_manager_config

    def test_emulation_env_config(self) -> None:
        """
        Tests creation and dict conversion of the EmulationEnvConfig DTO

        :return: None
        """
        container_network = ContainerNetwork(
            name="testnet", subnet_mask="/24", bitmask="255.255.255.0", subnet_prefix="192.168.5", interface="eth1")
        node_container_config = NodeContainerConfig(
            name="node_name", ips_and_networks=[("net_1", container_network)], version="1.0.0", level="4",
            restart_policy="always", suffix="_2", os="Ubuntu", execution_ip_first_octet=15,
            docker_gw_bridge_ip="7.7.7.7", physical_host_ip="8.8.8.8"
        )
        containers_config = ContainersConfig(containers=[node_container_config], agent_ip="5.5.5.5",
                                             router_ip="2.2.2.2",
                                             networks=[container_network],
                                             ids_enabled=True, vulnerable_nodes=None, agent_reachable_nodes=None)
        user = User(username="testuser", pw="mypw", root=True)
        node_users_config = NodeUsersConfig(
            ip="8.8.8.8", docker_gw_bridge_ip="8.8.8.8", physical_host_ip="7.7.7.7", users=[user])
        users_config = UsersConfig(users_configs=[node_users_config])
        flag = Flag(name="testflag", dir="/", id=10, path="/test.txt", requires_root=False, score=10)
        node_flags_config = NodeFlagsConfig(
            ip="8.8.8.8", flags=[flag], docker_gw_bridge_ip="9.9.9.9", physical_host_ip="168.22.11.2")
        flags_config = FlagsConfig(node_flag_configs=[node_flags_config])
        default_net_fw_config = DefaultNetworkFirewallConfig(
            ip="192.168.5.1", default_gw="192.168.5.29", default_output="ACCEPT", default_input="DROP",
            default_forward="ACCEPT", network=container_network
        )
        route = ("8.8.8.8", "7.7.7.7")
        routes = set()
        routes.add(route)
        node_firewall_config = NodeFirewallConfig(
            hostname="my_hostname", output_accept=set("8.8.8.8"), input_accept=set("8.8.8.8"),
            forward_accept=set("8.8.8.8"), output_drop=set("8.8.8.8"), input_drop=set("8.8.8.8"),
            forward_drop=set("8.8.8.8"), routes=routes, docker_gw_bridge_ip="8.8.8.8",
            physical_host_ip="192.172.1.1", ips_gw_default_policy_networks=[default_net_fw_config]
        )
        topology_config = TopologyConfig(subnetwork_masks=["255.255.255.0"],
                                         node_configs=[node_firewall_config])
        credential = Credential(username="testuser", pw="testpw", port=9311, protocol=TransportProtocol.UDP,
                                service="test", root=True)
        node_vuln_config = NodeVulnerabilityConfig(
            ip="8.8.8.8", docker_gw_bridge_ip="8.8.8.8", physical_host_ip="7.7.7.7",
            vuln_type=VulnType.RCE, protocol=TransportProtocol.TCP, credentials=[credential], cvss=2.0, cve="test_cve",
            service="myserv", root=True, name="testname", port=2510)
        vuln_config = VulnerabilitiesConfig(node_vulnerability_configs=[node_vuln_config])
        workflow_mc = WorkflowMarkovChain(transition_matrix=[[0.2, 0.8]], initial_state=10, id=1)
        workflows_service = WorkflowService(ips_and_commands=[("8.8.8.8", ["ls"])], id=10)
        workflows_config = WorkflowsConfig(workflow_markov_chains=[workflow_mc], workflow_services=[workflows_service])
        arrival_config = ConstantArrivalConfig(lamb=10.0)
        client = Client(id=10, workflow_distribution=[1], arrival_config=arrival_config, mu=4.0,
                        exponential_service_time=True)
        container_network = ContainerNetwork(
            name="testnet", subnet_mask="/24", bitmask="255.255.255.0", subnet_prefix="192.168.5", interface="eth1")
        client_population_config = ClientPopulationConfig(
            ip="8.8.8.8", networks=[container_network], client_manager_port=2020,
            client_manager_log_file="client_manager.log",
            client_manager_log_dir="/", client_manager_max_workers=10, clients=[client],
            workflows_config=workflows_config,
            client_time_step_len_seconds=30, docker_gw_bridge_ip="7.7.7.7", physical_host_ip="1.1.1.1"
        )
        node_traffic_config = NodeTrafficConfig(
            ip="8.8.8.8", commands=["ls"], traffic_manager_log_file="traffic_manager.log", traffic_manager_log_dir="/",
            traffic_manager_port=3000, traffic_manager_max_workers=10, docker_gw_bridge_ip="8.8.8.8",
            physical_host_ip="7.7.7.7")
        traffic_config = TrafficConfig(node_traffic_configs=[node_traffic_config],
                                       client_population_config=client_population_config)
        node_network_config = NodeNetworkConfig(
            interface="eth0", limit_packets_queue=3000, packet_delay_ms=0.1,
            packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
            packet_delay_distribution=PacketDelayDistributionType.PARETO,
            packet_loss_type=PacketLossType.GEMODEL, packet_loss_rate_random_percentage=2,
            packet_loss_random_correlation_percentage=25, loss_state_markov_chain_p13=0.1,
            loss_state_markov_chain_p31=0.1, loss_state_markov_chain_p32=0.1, loss_state_markov_chain_p23=0.1,
            loss_state_markov_chain_p14=0.1, loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
            loss_gemodel_h=0.0001, loss_gemodel_k=0.9999)
        node_resources_config = NodeResourcesConfig(
            container_name="my_container", num_cpus=10, available_memory_gb=100,
            ips_and_network_configs=[("net_1", node_network_config)], docker_gw_bridge_ip="docker_gw",
            physical_host_ip="192.168.1.1")
        resources_config = ResourcesConfig(node_resources_configurations=[node_resources_config])
        kafka_topic = KafkaTopic(name="testname", num_replicas=10, num_partitions=15, attributes=["attr1"],
                                 retention_time_hours=10)
        kafka_config = KafkaConfig(
            container=node_container_config, resources=node_resources_config, firewall_config=node_firewall_config,
            kafka_manager_log_file="elk_manager.log", kafka_manager_log_dir="/", kafka_manager_max_workers=10,
            time_step_len_seconds=15, kafka_manager_port=50045, version="0.0.1", topics=[kafka_topic])
        network_service = NetworkService(protocol=TransportProtocol.UDP, port=3000, name="testservice",
                                         credentials=[credential])
        node_services_config = NodeServicesConfig(ip="8.8.8.8", services=[network_service])
        services_config = ServicesConfig(services_configs=[node_services_config])
        ovs_switch_config = OvsSwitchConfig(
            container_name="testcontainer", ip="8.8.8.8", openflow_protocols=["v1.0.0"], controller_ip="8.8.8.8",
            controller_port=3000, controller_transport_protocol="UDP", docker_gw_bridge_ip="8.8.8.8",
            physical_host_ip="168.156.2.2")
        ovs_config = OVSConfig(switch_configs=[ovs_switch_config])
        host_manager_config = HostManagerConfig(
            host_manager_log_file="host_manager.log", host_manager_log_dir="/", host_manager_max_workers=10,
            time_step_len_seconds=30, host_manager_port=3000, version="0.0.1")
        elk_config = ElkConfig(
            container=node_container_config, resources=node_resources_config, firewall_config=node_firewall_config,
            elk_manager_log_file="elk_manager.log", elk_manager_log_dir="/", elk_manager_max_workers=10,
            elastic_port=9200, kibana_port=5601, logstash_port=5044, time_step_len_seconds=15, elk_manager_port=50045,
            version="0.0.1")
        node_beats_config = NodeBeatsConfig(
            ip="192.168.5.1", log_files_paths=["log1"], filebeat_modules=["mod1"], metricbeat_modules=["mod2"],
            heartbeat_hosts_to_monitor=["192.168.5.7"], kafka_input=False, start_heartbeat_automatically=True,
            start_packetbeat_automatically=True, start_metricbeat_automatically=True, start_filebeat_automatically=True
        )
        beats_config = BeatsConfig(
            node_beats_configs=[node_beats_config], num_elastic_shards=19, reload_enabled=False
        )
        docker_statsmanager_config = DockerStatsManagerConfig(
            docker_stats_manager_log_file="testlog", docker_stats_manager_log_dir="logdir",
            docker_stats_manager_max_workers=10, time_step_len_seconds=30, docker_stats_manager_port=19, version="0.0.1"
        )
        snort_ids_manager_config = SnortIDSManagerConfig(
            snort_ids_manager_log_file="snort.log", snort_ids_manager_log_dir="/", snort_ids_manager_max_workers=10,
            time_step_len_seconds=30, snort_ids_manager_port=4000, version="0.0.1")
        ossec_ids_manager_config = OSSECIDSManagerConfig(
            ossec_ids_manager_log_file="ossec.log", ossec_ids_manager_log_dir="/", ossec_ids_manager_max_workers=10,
            time_step_len_seconds=30, ossec_ids_manager_port=1515, version="0.0.1")
        static_sequence = [
            EmulationAttackerAction(
                id=EmulationAttackerActionId.CONTINUE, name="test", cmds=["cmd1"],
                type=EmulationAttackerActionType.CONTINUE, descr="testtest", ips=["ip1"], index=0,
                action_outcome=EmulationAttackerActionOutcome.CONTINUE, vulnerability="test", alt_cmds=["altcmd1"],
                backdoor=False, execution_time=0.0, ts=0.0
            )
        ]
        em_config = EmulationEnvConfig(name="emulation", containers_config=containers_config,
                                       users_config=users_config, flags_config=flags_config,
                                       vuln_config=vuln_config, topology_config=topology_config,
                                       traffic_config=traffic_config,
                                       resources_config=resources_config,
                                       kafka_config=kafka_config, services_config=services_config,
                                       descr="testdescr", static_attacker_sequences={"t": static_sequence},
                                       ovs_config=ovs_config,
                                       sdn_controller_config=None, host_manager_config=host_manager_config,
                                       snort_ids_manager_config=snort_ids_manager_config,
                                       ossec_ids_manager_config=ossec_ids_manager_config,
                                       docker_stats_manager_config=docker_statsmanager_config, elk_config=elk_config,
                                       beats_config=beats_config,
                                       level=10, version="0.0.1", execution_id=16, csle_collector_version="latest",
                                       csle_ryu_version="latest")
        assert isinstance(em_config.to_dict(), dict)
        assert isinstance(EmulationEnvConfig.from_dict(em_config.to_dict()), EmulationEnvConfig)
        assert EmulationEnvConfig.from_dict(em_config.to_dict()).to_dict() == em_config.to_dict()
        assert EmulationEnvConfig.from_dict(em_config.to_dict()) == em_config
