from csle_common.dao.emulation_config.node_beats_config import NodeBeatsConfig
from csle_common.dao.emulation_config.beats_config import BeatsConfig
from csle_common.dao.emulation_config.client_managers_info import ClientManagersInfo
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.dao.emulation_config.cluster_node import ClusterNode
from csle_common.dao.emulation_config.cluster_config import ClusterConfig
from csle_common.dao.emulation_config.config import Config
from csle_common.dao.emulation_config.credential import Credential
from csle_common.dao.emulation_config.default_network_firewall_config import DefaultNetworkFirewallConfig
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_common.dao.emulation_config.docker_stats_manager_config import DockerStatsManagerConfig
from csle_common.dao.emulation_config.docker_stats_managers_info import DockerStatsManagersInfo
from csle_common.dao.emulation_config.node_network_config import NodeNetworkConfig
from csle_common.dao.emulation_config.packet_loss_type import PacketLossType
from csle_common.dao.emulation_config.packet_delay_distribution_type import PacketDelayDistributionType
from csle_collector.client_manager.client_manager_pb2 import ClientsDTO
from csle_collector.docker_stats_manager.docker_stats_manager_pb2 import DockerStatsMonitorDTO


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
        assert isinstance(NodeNetworkConfig.from_dict(node_network_config.to_dict()),
                          NodeNetworkConfig)
        assert NodeNetworkConfig.from_dict(node_network_config.to_dict()).to_dict() == \
               node_network_config.to_dict()
        assert NodeNetworkConfig.from_dict(node_network_config.to_dict()) == node_network_config
