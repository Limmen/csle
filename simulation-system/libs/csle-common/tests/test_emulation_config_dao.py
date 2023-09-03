from csle_common.dao.emulation_config.node_beats_config import NodeBeatsConfig
from csle_common.dao.emulation_config.beats_config import BeatsConfig
from csle_common.dao.emulation_config.client_managers_info import ClientManagersInfo
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.dao.emulation_config.cluster_node import ClusterNode
from csle_common.dao.emulation_config.cluster_config import ClusterConfig
from csle_common.dao.emulation_config.config import Config
from csle_common.dao.emulation_config.credential import Credential
from csle_common.dao.emulation_config.default_network_firewall_config import DefaultNetworkFirewallConfig
from csle_common.dao.emulation_config.node_firewall_config import NodeFirewallConfig
from csle_common.dao.emulation_config.docker_stats_manager_config import DockerStatsManagerConfig
from csle_common.dao.emulation_config.docker_stats_managers_info import DockerStatsManagersInfo
from csle_common.dao.emulation_config.node_network_config import NodeNetworkConfig
from csle_common.dao.emulation_config.host_manager_config import HostManagerConfig
from csle_common.dao.emulation_config.snort_ids_manager_config import SnortIDSManagerConfig
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
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.ovs_config import OVSConfig
from csle_common.dao.emulation_config.ovs_switch_config import OvsSwitchConfig
from csle_common.dao.emulation_config.kafka_config import KafkaConfig
from csle_common.dao.emulation_config.kafka_topic import KafkaTopic
from csle_common.dao.emulation_config.network_service import NetworkService
from csle_common.dao.emulation_observation.common.emulation_connection_observation_state import \
    EmulationConnectionObservationState
from csle_common.dao.emulation_config.connection_setup_dto import ConnectionSetupDTO
from csle_collector.client_manager.dao.client import Client
from csle_collector.client_manager.dao.constant_arrival_config import ConstantArrivalConfig
from csle_collector.client_manager.dao.workflow_markov_chain import WorkflowMarkovChain
from csle_collector.client_manager.dao.workflow_service import WorkflowService
from csle_collector.client_manager.dao.workflows_config import WorkflowsConfig


class TestEmulationConfigDaoSuite:
    """
    Test suite for datasets data access objects (DAOs)
    """

    def test_node_beats_config(self, example_node_beats_config: NodeBeatsConfig) -> None:
        """
        Tests creation and dict conversion of the NodeBeatsConfig DAO

        :param example_node_beats_config: an example NodeBeatsConfig
        :return: None
        """
        assert isinstance(example_node_beats_config.to_dict(), dict)
        assert isinstance(NodeBeatsConfig.from_dict(example_node_beats_config.to_dict()), NodeBeatsConfig)
        assert NodeBeatsConfig.from_dict(example_node_beats_config.to_dict()).to_dict() == \
               example_node_beats_config.to_dict()
        assert NodeBeatsConfig.from_dict(example_node_beats_config.to_dict()) == example_node_beats_config

    def test_beats_config(self, example_beats_config: BeatsConfig) -> None:
        """
        Tests creation and dict conversion of the BeatsConfig DAO

        :param example_beats_config: an example BeatsConfig
        :return: None
        """
        assert isinstance(example_beats_config.to_dict(), dict)
        assert isinstance(BeatsConfig.from_dict(example_beats_config.to_dict()), BeatsConfig)
        assert BeatsConfig.from_dict(example_beats_config.to_dict()).to_dict() == example_beats_config.to_dict()
        assert BeatsConfig.from_dict(example_beats_config.to_dict()) == example_beats_config

    def test_client_managers_info(self, example_client_managers_info: ClientManagersInfo) -> None:
        """
        Tests creation and dict conversion of the client_managers_info_dto

        :param example_client_managers_info: an example ClientManagersInfo
        :return: None
        """
        assert isinstance(example_client_managers_info.to_dict(), dict)
        assert isinstance(ClientManagersInfo.from_dict(example_client_managers_info.to_dict()), ClientManagersInfo)
        assert ClientManagersInfo.from_dict(example_client_managers_info.to_dict()).to_dict() == \
               example_client_managers_info.to_dict()
        assert ClientManagersInfo.from_dict(example_client_managers_info.to_dict()) == example_client_managers_info

    def test_container_network(self, example_container_network: ContainerNetwork) -> None:
        """
        Tests creation and dict conversion of the ContainerNetwork DTO

        :param example_container_network: an example ContainerNetwork
        :return: None
        """
        assert isinstance(example_container_network.to_dict(), dict)
        assert isinstance(ContainerNetwork.from_dict(example_container_network.to_dict()), ContainerNetwork)
        assert ContainerNetwork.from_dict(example_container_network.to_dict()).to_dict() == \
               example_container_network.to_dict()
        assert ContainerNetwork.from_dict(example_container_network.to_dict()) == \
               example_container_network

    def test_cluster_node(self, example_cluster_node: ClusterNode) -> None:
        """
        Tests creation and dict conversion of the ClusterNode DTO

        :param example_cluster_node: an example ClusterNode
        :return: None
        """
        assert isinstance(example_cluster_node.to_dict(), dict)
        assert isinstance(ClusterNode.from_dict(example_cluster_node.to_dict()), ClusterNode)
        assert ClusterNode.from_dict(example_cluster_node.to_dict()).to_dict() == example_cluster_node.to_dict()
        assert ClusterNode.from_dict(example_cluster_node.to_dict()) == example_cluster_node

    def test_cluster_config(self, example_cluster_config: ClusterConfig) -> None:
        """
        Tests creation and dict conversion of the ClusterConfig DTO

        :param example_cluster_config: an example ClusterConfig
        :return: None
        """
        assert isinstance(example_cluster_config.to_dict(), dict)
        assert isinstance(ClusterConfig.from_dict(example_cluster_config.to_dict()), ClusterConfig)
        assert ClusterConfig.from_dict(example_cluster_config.to_dict()).to_dict() == example_cluster_config.to_dict()
        assert ClusterConfig.from_dict(example_cluster_config.to_dict()) == example_cluster_config

    def test_config(self, example_config: Config) -> None:
        """
        Tests creation and dict conversion of the Config DTO

        :param example_config: an example Config
        :return: None
        """
        assert isinstance(example_config.to_dict(), dict)
        assert isinstance(Config.from_dict(example_config.to_dict()), Config)
        assert Config.from_dict(example_config.to_dict()).to_dict() == example_config.to_dict()
        assert Config.from_dict(example_config.to_dict()) == example_config

    def test_credential(self, example_credential: Credential) -> None:
        """
        Tests creation and dict conversion of the Credential DTO

        :param example_credential: an example Credential
        :return: None
        """
        assert isinstance(example_credential.to_dict(), dict)
        assert isinstance(Credential.from_dict(example_credential.to_dict()), Credential)
        assert Credential.from_dict(example_credential.to_dict()).to_dict() == example_credential.to_dict()
        assert Credential.from_dict(example_credential.to_dict()) == example_credential

    def test_default_network_firewall_config(
            self, example_default_network_firewall_config: DefaultNetworkFirewallConfig) -> None:
        """
        Tests creation and dict conversion of the DefaultNetworkFirewallConfig DTO

        :param example_default_network_firewall_config: an example DefaultNetworkFirewallConfig
        :return: None
        """
        assert isinstance(example_default_network_firewall_config.to_dict(), dict)
        assert isinstance(DefaultNetworkFirewallConfig.from_dict(example_default_network_firewall_config.to_dict()),
                          DefaultNetworkFirewallConfig)
        assert DefaultNetworkFirewallConfig.from_dict(example_default_network_firewall_config.to_dict()).to_dict() == \
               example_default_network_firewall_config.to_dict()
        assert DefaultNetworkFirewallConfig.from_dict(example_default_network_firewall_config.to_dict()) == \
               example_default_network_firewall_config

    def test_docker_stats_manager_config(self, example_docker_stats_manager_config: DockerStatsManagerConfig) -> None:
        """
        Tests creation and dict conversion of the DockerStatsManagerConfig DTO

        :param example_docker_stats_manager_config: an example DockerStatsManagerConfig
        :return: None
        """
        assert isinstance(example_docker_stats_manager_config.to_dict(), dict)
        assert isinstance(DockerStatsManagerConfig.from_dict(example_docker_stats_manager_config.to_dict()),
                          DockerStatsManagerConfig)
        assert DockerStatsManagerConfig.from_dict(example_docker_stats_manager_config.to_dict()).to_dict() == \
               example_docker_stats_manager_config.to_dict()
        assert DockerStatsManagerConfig.from_dict(example_docker_stats_manager_config.to_dict()) == \
               example_docker_stats_manager_config

    def test_docker_stats_managers_info(self, example_docker_stats_managers_info: DockerStatsManagersInfo) -> None:
        """
        Tests creation and dict conversion of the DockerStatsManagersInfo DTO

        :param example_docker_stats_managers_info: an example DockerStatsManagersInfo
        :return: None
        """
        assert isinstance(example_docker_stats_managers_info.to_dict(), dict)
        assert isinstance(DockerStatsManagersInfo.from_dict(example_docker_stats_managers_info.to_dict()),
                          DockerStatsManagersInfo)
        assert DockerStatsManagersInfo.from_dict(example_docker_stats_managers_info.to_dict()).to_dict() == \
               example_docker_stats_managers_info.to_dict()
        assert DockerStatsManagersInfo.from_dict(example_docker_stats_managers_info.to_dict()) == \
               example_docker_stats_managers_info

    def test_node_network_config(self, example_node_network_config: NodeNetworkConfig) -> None:
        """
        Tests creation and dict conversion of the NodeNetworkConfig DTO

        :param example_node_network_config: an example NodeNetworkConfig
        :return: None
        """
        assert isinstance(example_node_network_config.to_dict(), dict)
        assert isinstance(NodeNetworkConfig.from_dict(example_node_network_config.to_dict()), NodeNetworkConfig)
        assert NodeNetworkConfig.from_dict(example_node_network_config.to_dict()).to_dict() == \
               example_node_network_config.to_dict()
        assert NodeNetworkConfig.from_dict(example_node_network_config.to_dict()) == example_node_network_config

    def test_node_resources_config(self, example_node_resources_config: NodeResourcesConfig) -> None:
        """
        Tests creation and dict conversion of the NodeResourcesConfig DTO

        :param example_node_resources_config: an example NodeResourcesConfig
        :return: None
        """
        assert isinstance(example_node_resources_config.to_dict(), dict)
        assert isinstance(NodeResourcesConfig.from_dict(example_node_resources_config.to_dict()), NodeResourcesConfig)
        assert NodeResourcesConfig.from_dict(example_node_resources_config.to_dict()).to_dict() == \
               example_node_resources_config.to_dict()
        assert NodeResourcesConfig.from_dict(example_node_resources_config.to_dict()) == example_node_resources_config

    def test_node_container_config(self, example_node_container_config: NodeContainerConfig) -> None:
        """
        Tests creation and dict conversion of the NodeContainerConfig DTO

        :param example_node_container_config: an example NodeContainerConfig
        :return: None
        """
        assert isinstance(example_node_container_config.to_dict(), dict)
        assert isinstance(NodeContainerConfig.from_dict(example_node_container_config.to_dict()), NodeContainerConfig)
        assert NodeContainerConfig.from_dict(example_node_container_config.to_dict()).to_dict() == \
               example_node_container_config.to_dict()
        assert NodeContainerConfig.from_dict(example_node_container_config.to_dict()) == example_node_container_config

    def test_node_firewall_config(self, example_node_firewall_config: NodeFirewallConfig) -> None:
        """
        Tests creation and dict conversion of the NodeFirewallConfig DTO

        :param example_node_firewall_config: an example NodeFirewallConfig
        :return: None
        """
        assert isinstance(example_node_firewall_config.to_dict(), dict)
        assert isinstance(NodeFirewallConfig.from_dict(example_node_firewall_config.to_dict()), NodeFirewallConfig)
        assert NodeFirewallConfig.from_dict(example_node_firewall_config.to_dict()).to_dict() == \
               example_node_firewall_config.to_dict()
        assert NodeFirewallConfig.from_dict(example_node_firewall_config.to_dict()) == example_node_firewall_config

    def test_elk_config(self, example_elk_config: ElkConfig) -> None:
        """
        Tests creation and dict conversion of the ElkConfig DTO

        :param example_elk_config: an example ElkConfig
        :return: None
        """
        assert isinstance(example_elk_config.to_dict(), dict)
        assert isinstance(ElkConfig.from_dict(example_elk_config.to_dict()), ElkConfig)
        assert ElkConfig.from_dict(example_elk_config.to_dict()).to_dict() == example_elk_config.to_dict()
        assert ElkConfig.from_dict(example_elk_config.to_dict()) == example_elk_config

    def test_elk_managers_info(self, example_elk_managers_info: ELKManagersInfo) -> None:
        """
        Tests creation and dict conversion of the ElkManagersInfo DTO

        :param example_elk_managers_info: an example ELKManagersInfo
        :return: None
        """
        assert isinstance(example_elk_managers_info.to_dict(), dict)
        assert isinstance(ELKManagersInfo.from_dict(example_elk_managers_info.to_dict()),
                          ELKManagersInfo)
        assert ELKManagersInfo.from_dict(example_elk_managers_info.to_dict()).to_dict() == \
               example_elk_managers_info.to_dict()
        assert ELKManagersInfo.from_dict(example_elk_managers_info.to_dict()) == example_elk_managers_info

    def test_snort_managers_info(self, example_snort_ids_managers_info: SnortIdsManagersInfo) -> None:
        """
        Tests creation and dict conversion of the SnortManagersInfo DTO

        :param example_snort_ids_managers_info: an example SnortIdsManagersInfo
        :return: None
        """
        assert isinstance(example_snort_ids_managers_info.to_dict(), dict)
        assert isinstance(SnortIdsManagersInfo.from_dict(example_snort_ids_managers_info.to_dict()),
                          SnortIdsManagersInfo)
        assert SnortIdsManagersInfo.from_dict(example_snort_ids_managers_info.to_dict()).to_dict() == \
               example_snort_ids_managers_info.to_dict()
        assert SnortIdsManagersInfo.from_dict(example_snort_ids_managers_info.to_dict()) == \
               example_snort_ids_managers_info

    def test_ossec_managers_info(self, example_ossec_ids_managers_info: OSSECIDSManagersInfo) -> None:
        """
        Tests creation and dict conversion of the OSSECIDSManagersInfo DTO

        :param example_ossec_ids_managers_info: an example OSSECIDSManagersInfo
        :return: None
        """
        assert isinstance(example_ossec_ids_managers_info.to_dict(), dict)
        assert isinstance(OSSECIDSManagersInfo.from_dict(example_ossec_ids_managers_info.to_dict()),
                          OSSECIDSManagersInfo)
        assert OSSECIDSManagersInfo.from_dict(example_ossec_ids_managers_info.to_dict()).to_dict() == \
               example_ossec_ids_managers_info.to_dict()
        assert OSSECIDSManagersInfo.from_dict(example_ossec_ids_managers_info.to_dict()) == \
               example_ossec_ids_managers_info

    def test_ryu_managers_info(self, example_ryu_managers_info: RyuManagersInfo) -> None:
        """
        Tests creation and dict conversion of the RyuManagersInfo DTO

        :param example_ryu_managers_info: an example RyuManagersInfo
        :return: None
        """
        assert isinstance(example_ryu_managers_info.to_dict(), dict)
        assert isinstance(RyuManagersInfo.from_dict(example_ryu_managers_info.to_dict()),
                          RyuManagersInfo)
        assert RyuManagersInfo.from_dict(example_ryu_managers_info.to_dict()).to_dict() == \
               example_ryu_managers_info.to_dict()
        assert RyuManagersInfo.from_dict(example_ryu_managers_info.to_dict()) == example_ryu_managers_info

    def test_host_managers_info(self, example_host_managers_info: HostManagersInfo) -> None:
        """
        Tests creation and dict conversion of the HostManagersInfo DTO

        :param example_host_managers_info: an example HostManagersInfo
        :return: None
        """
        assert isinstance(example_host_managers_info.to_dict(), dict)
        assert isinstance(HostManagersInfo.from_dict(example_host_managers_info.to_dict()),
                          HostManagersInfo)
        assert HostManagersInfo.from_dict(example_host_managers_info.to_dict()).to_dict() == \
               example_host_managers_info.to_dict()
        assert HostManagersInfo.from_dict(example_host_managers_info.to_dict()) == example_host_managers_info

    def test_kafka_managers_info(self, example_kafka_managers_info: KafkaManagersInfo) -> None:
        """
        Tests creation and dict conversion of the KafkaManagersInfo DTO

        :param example_kafka_managers_info: an example KafkaManagersInfo
        :return: None
        """
        assert isinstance(example_kafka_managers_info.to_dict(), dict)
        assert isinstance(KafkaManagersInfo.from_dict(example_kafka_managers_info.to_dict()),
                          KafkaManagersInfo)
        assert KafkaManagersInfo.from_dict(example_kafka_managers_info.to_dict()).to_dict() == \
               example_kafka_managers_info.to_dict()
        assert KafkaManagersInfo.from_dict(example_kafka_managers_info.to_dict()) == example_kafka_managers_info

    def test_kafka_topic(self, example_kafka_topic: KafkaTopic) -> None:
        """
        Tests creation and dict conversion of the KafkaTopic DTO

        :param example_kafka_topic: an example KafkaTopic
        :return: None
        """
        assert isinstance(example_kafka_topic.to_dict(), dict)
        assert isinstance(KafkaTopic.from_dict(example_kafka_topic.to_dict()), KafkaTopic)
        assert KafkaTopic.from_dict(example_kafka_topic.to_dict()).to_dict() == example_kafka_topic.to_dict()
        assert KafkaTopic.from_dict(example_kafka_topic.to_dict()) == example_kafka_topic

    def test_kafka_config(self, example_kafka_config: KafkaConfig) -> None:
        """
        Tests creation and dict conversion of the KafkaConfig DTO

        :param example_kafka_config: an example KafkaConfig
        :return: None
        """
        assert isinstance(example_kafka_config.to_dict(), dict)
        assert isinstance(KafkaConfig.from_dict(example_kafka_config.to_dict()), KafkaConfig)
        assert KafkaConfig.from_dict(example_kafka_config.to_dict()).to_dict() == example_kafka_config.to_dict()
        assert KafkaConfig.from_dict(example_kafka_config.to_dict()) == example_kafka_config

    def test_network_service(self, example_network_service: NetworkService) -> None:
        """
        Tests creation and dict conversion of the NetworkService DTO

        :param example_network_service: an example NetworkService
        :return: None
        """
        assert isinstance(example_network_service.to_dict(), dict)
        assert isinstance(NetworkService.from_dict(example_network_service.to_dict()), NetworkService)
        assert NetworkService.from_dict(example_network_service.to_dict()).to_dict() == \
               example_network_service.to_dict()
        assert NetworkService.from_dict(example_network_service.to_dict()) == example_network_service

    def test_flag(self, example_flag: Flag) -> None:
        """
        Tests creation and dict conversion of the Flag DTO

        :param example_flag: an example Flag
        :return: None
        """
        assert isinstance(example_flag.to_dict(), dict)
        assert isinstance(Flag.from_dict(example_flag.to_dict()), Flag)
        assert Flag.from_dict(example_flag.to_dict()).to_dict() == example_flag.to_dict()
        assert Flag.from_dict(example_flag.to_dict()) == example_flag

    def test_node_flags_config(self, example_node_flags_config: NodeFlagsConfig) -> None:
        """
        Tests creation and dict conversion of the NodeFlagsConfig DTO

        :param example_node_flags_config: an example NodeFlagsConfig
        :return: None
        """
        assert isinstance(example_node_flags_config.to_dict(), dict)
        assert isinstance(NodeFlagsConfig.from_dict(example_node_flags_config.to_dict()), NodeFlagsConfig)
        assert NodeFlagsConfig.from_dict(example_node_flags_config.to_dict()).to_dict() == \
               example_node_flags_config.to_dict()
        assert NodeFlagsConfig.from_dict(example_node_flags_config.to_dict()) == example_node_flags_config

    def test_node_services_config(self, example_node_services_config: NodeServicesConfig) -> None:
        """
        Tests creation and dict conversion of the NodeServicesConfig DTO

        :param example_node_services_config: an example NodeServicesConfig
        :return: None
        """
        assert isinstance(example_node_services_config.to_dict(), dict)
        assert isinstance(NodeServicesConfig.from_dict(example_node_services_config.to_dict()), NodeServicesConfig)
        assert NodeServicesConfig.from_dict(example_node_services_config.to_dict()).to_dict() == \
               example_node_services_config.to_dict()
        assert NodeServicesConfig.from_dict(example_node_services_config.to_dict()) == example_node_services_config

    def test_node_traffic_config(self, example_node_traffic_config: NodeTrafficConfig) -> None:
        """
        Tests creation and dict conversion of the NodeTrafficConfig DTO

        :param example_node_traffic_config: an example NodeTrafficConfig
        :return: None
        """
        assert isinstance(example_node_traffic_config.to_dict(), dict)
        assert isinstance(NodeTrafficConfig.from_dict(example_node_traffic_config.to_dict()), NodeTrafficConfig)
        assert NodeTrafficConfig.from_dict(example_node_traffic_config.to_dict()).to_dict() == \
               example_node_traffic_config.to_dict()
        assert NodeTrafficConfig.from_dict(example_node_traffic_config.to_dict()) == example_node_traffic_config

    def test_user(self, example_user: User) -> None:
        """
        Tests creation and dict conversion of the User DTO

        :param example_user: an example User
        :return: None
        """
        assert isinstance(example_user.to_dict(), dict)
        assert isinstance(User.from_dict(example_user.to_dict()), User)
        assert User.from_dict(example_user.to_dict()).to_dict() == example_user.to_dict()
        assert User.from_dict(example_user.to_dict()) == example_user

    def test_node_users_config(self, example_node_users_config: NodeUsersConfig) -> None:
        """
        Tests creation and dict conversion of the NodeUsersConfig DTO

        :param example_node_users_config: an example NodeUsersConfig
        :return: None
        """
        assert isinstance(example_node_users_config.to_dict(), dict)
        assert isinstance(NodeUsersConfig.from_dict(example_node_users_config.to_dict()), NodeUsersConfig)
        assert NodeUsersConfig.from_dict(example_node_users_config.to_dict()).to_dict() == \
               example_node_users_config.to_dict()
        assert NodeUsersConfig.from_dict(example_node_users_config.to_dict()) == example_node_users_config

    def test_node_vulnerability_config(self, example_node_vulnerability_config: NodeVulnerabilityConfig) -> None:
        """
        Tests creation and dict conversion of the NodeVulnerabilitiesConfig DTO

        :param example_node_vulnerability_config: an example NodeVulnerabilityConfig
        :return: None
        """
        assert isinstance(example_node_vulnerability_config.to_dict(), dict)
        assert isinstance(NodeVulnerabilityConfig.from_dict(example_node_vulnerability_config.to_dict()),
                          NodeVulnerabilityConfig)
        assert NodeVulnerabilityConfig.from_dict(example_node_vulnerability_config.to_dict()).to_dict() == \
               example_node_vulnerability_config.to_dict()
        assert NodeVulnerabilityConfig.from_dict(example_node_vulnerability_config.to_dict()) == \
               example_node_vulnerability_config

    def test_ossec_ids_manager_config(self, example_ossec_ids_manager_config: OSSECIDSManagerConfig) -> None:
        """
        Tests creation and dict conversion of the OSSECIDSManagerConfig DTO

        :param example_ossec_ids_manager_config: an example OSSECIDSManagerConfig
        :return: None
        """
        assert isinstance(example_ossec_ids_manager_config.to_dict(), dict)
        assert isinstance(OSSECIDSManagerConfig.from_dict(example_ossec_ids_manager_config.to_dict()),
                          OSSECIDSManagerConfig)
        assert OSSECIDSManagerConfig.from_dict(example_ossec_ids_manager_config.to_dict()).to_dict() == \
               example_ossec_ids_manager_config.to_dict()
        assert OSSECIDSManagerConfig.from_dict(example_ossec_ids_manager_config.to_dict()) == \
               example_ossec_ids_manager_config

    def test_ovs_switch_config(self, example_ovs_switch_config: OvsSwitchConfig) -> None:
        """
        Tests creation and dict conversion of the OVSConfig DTO

        :param example_ovs_switch_config: an example OvsSwitchConfig
        :return: None
        """
        assert isinstance(example_ovs_switch_config.to_dict(), dict)
        assert isinstance(OvsSwitchConfig.from_dict(example_ovs_switch_config.to_dict()), OvsSwitchConfig)
        assert OvsSwitchConfig.from_dict(example_ovs_switch_config.to_dict()).to_dict() == \
               example_ovs_switch_config.to_dict()
        assert OvsSwitchConfig.from_dict(example_ovs_switch_config.to_dict()) == example_ovs_switch_config

    def test_ovs_config(self, example_ovs_config: OVSConfig) -> None:
        """
        Tests creation and dict conversion of the OVSConfig DTO

        :param example_ovs_config: an example OVSConfig
        :return: None
        """
        assert isinstance(example_ovs_config.to_dict(), dict)
        assert isinstance(OVSConfig.from_dict(example_ovs_config.to_dict()), OVSConfig)
        assert OVSConfig.from_dict(example_ovs_config.to_dict()).to_dict() == example_ovs_config.to_dict()
        assert OVSConfig.from_dict(example_ovs_config.to_dict()) == example_ovs_config

    def test_resources_config(self, example_resources_config: ResourcesConfig) -> None:
        """
        Tests creation and dict conversion of the ResourcesConfig DTO

        :param example_resources_config: an example ResourcesConfig
        :return: None
        """
        assert isinstance(example_resources_config.to_dict(), dict)
        assert isinstance(ResourcesConfig.from_dict(example_resources_config.to_dict()), ResourcesConfig)
        assert ResourcesConfig.from_dict(example_resources_config.to_dict()).to_dict() == \
               example_resources_config.to_dict()
        assert ResourcesConfig.from_dict(example_resources_config.to_dict()) == example_resources_config

    def test_sdn_controller_config(self, example_sdn_controller_config: SDNControllerConfig) -> None:
        """
        Tests creation and dict conversion of the ResourcesConfig DTO

        :param example_sdn_controller_config: an example SDNControllerConfig
        :return: None
        """
        assert isinstance(example_sdn_controller_config.to_dict(), dict)
        assert isinstance(SDNControllerConfig.from_dict(example_sdn_controller_config.to_dict()), SDNControllerConfig)
        assert SDNControllerConfig.from_dict(example_sdn_controller_config.to_dict()).to_dict() == \
               example_sdn_controller_config.to_dict()
        assert SDNControllerConfig.from_dict(example_sdn_controller_config.to_dict()) == example_sdn_controller_config

    def test_services_config(self, example_services_config: ServicesConfig) -> None:
        """
        Tests creation and dict conversion of the ServicesConfig DTO

        :param example_services_config: an example ServicesConfig
        :return: None
        """
        assert isinstance(example_services_config.to_dict(), dict)
        assert isinstance(ServicesConfig.from_dict(example_services_config.to_dict()), ServicesConfig)
        assert ServicesConfig.from_dict(
            example_services_config.to_dict()).to_dict() == example_services_config.to_dict()
        assert ServicesConfig.from_dict(example_services_config.to_dict()) == example_services_config

    def test_users_config(self, example_users_config: UsersConfig) -> None:
        """
        Tests creation and dict conversion of the UsersConfig DTO

        :param example_users_config: an example UsersConfig
        :return: None
        """
        assert isinstance(example_users_config.to_dict(), dict)
        assert isinstance(UsersConfig.from_dict(example_users_config.to_dict()), UsersConfig)
        assert UsersConfig.from_dict(example_users_config.to_dict()).to_dict() == example_users_config.to_dict()
        assert UsersConfig.from_dict(example_users_config.to_dict()) == example_users_config

    def test_arrival_config(self, example_constant_arrival_config: ConstantArrivalConfig) -> None:
        """
        Tests creation and dict conversion of the ArrivalConfig DTO

        :param example_constant_arrival_config: an example ConstantArrivalConfig
        :return: None
        """
        assert isinstance(example_constant_arrival_config.to_dict(), dict)
        assert isinstance(ConstantArrivalConfig.from_dict(example_constant_arrival_config.to_dict()),
                          ConstantArrivalConfig)
        assert ConstantArrivalConfig.from_dict(example_constant_arrival_config.to_dict()).to_dict() == \
               example_constant_arrival_config.to_dict()
        assert ConstantArrivalConfig.from_dict(example_constant_arrival_config.to_dict()) == \
               example_constant_arrival_config

    def test_client(self, example_client: Client) -> None:
        """
        Tests creation and dict conversion of the Client DTO

        :param example_client: an example Client
        :return: None
        """
        assert isinstance(example_client.to_dict(), dict)
        assert isinstance(Client.from_dict(example_client.to_dict()), Client)
        assert Client.from_dict(example_client.to_dict()).to_dict() == example_client.to_dict()
        assert Client.from_dict(example_client.to_dict()) == example_client

    def test_workflows_service(self, example_workflow_service: WorkflowService) -> None:
        """n
        Tests creation and dict conversion of the WorkflowService DTO

        :param example_workflow_service: an example WorkflowService
        :return: None
        """
        assert isinstance(example_workflow_service.to_dict(), dict)
        assert isinstance(WorkflowService.from_dict(example_workflow_service.to_dict()), WorkflowService)
        assert WorkflowService.from_dict(example_workflow_service.to_dict()).to_dict() == \
               example_workflow_service.to_dict()
        assert WorkflowService.from_dict(example_workflow_service.to_dict()) == example_workflow_service

    def test_workflow_markov_chain(self, example_workflow_markov_chain: WorkflowMarkovChain) -> None:
        """n
        Tests creation and dict conversion of the WorkflowMarkovChain DTO

        :param example_workflow_markov_chain: an example WorkflowMarkovChain
        :return: None
        """
        assert isinstance(example_workflow_markov_chain.to_dict(), dict)
        assert isinstance(WorkflowMarkovChain.from_dict(example_workflow_markov_chain.to_dict()), WorkflowMarkovChain)
        assert WorkflowMarkovChain.from_dict(example_workflow_markov_chain.to_dict()).to_dict() == \
               example_workflow_markov_chain.to_dict()
        assert WorkflowMarkovChain.from_dict(example_workflow_markov_chain.to_dict()) == example_workflow_markov_chain

    def test_workflows_config(self, example_workflows_config: WorkflowsConfig) -> None:
        """n
        Tests creation and dict conversion of the WorkflowsConfig DTO

        :param example_workflows_config: an example WorkflowsConfig
        :return: None
        """
        assert isinstance(example_workflows_config.to_dict(), dict)
        assert isinstance(WorkflowsConfig.from_dict(example_workflows_config.to_dict()), WorkflowsConfig)
        assert WorkflowsConfig.from_dict(example_workflows_config.to_dict()).to_dict() == \
               example_workflows_config.to_dict()
        assert WorkflowsConfig.from_dict(example_workflows_config.to_dict()) == example_workflows_config

    def test_client_population_config(self, example_client_population_config: ClientPopulationConfig) -> None:
        """
        Tests creation and dict conversion of the ClientPopulationConfig DTO

        :param example_client_population_config: an example ClientPopulationConfig
        :return: None
        """
        assert isinstance(example_client_population_config.to_dict(), dict)
        assert isinstance(ClientPopulationConfig.from_dict(example_client_population_config.to_dict()),
                          ClientPopulationConfig)
        assert ClientPopulationConfig.from_dict(example_client_population_config.to_dict()).to_dict() == \
               example_client_population_config.to_dict()
        assert ClientPopulationConfig.from_dict(example_client_population_config.to_dict()) == \
               example_client_population_config

    def test_traffic_config(self, example_traffic_config: TrafficConfig) -> None:
        """
        Tests creation and dict conversion of the TrafficConfig DTO

        :param example_traffic_config: an example TrafficConfig
        :return: None
        """
        assert isinstance(example_traffic_config.to_dict(), dict)
        assert isinstance(TrafficConfig.from_dict(example_traffic_config.to_dict()), TrafficConfig)
        assert TrafficConfig.from_dict(example_traffic_config.to_dict()).to_dict() == example_traffic_config.to_dict()
        assert TrafficConfig.from_dict(example_traffic_config.to_dict()) == example_traffic_config

    def test_vulnerabilities_config(self, example_vulnerabilities_config: VulnerabilitiesConfig) -> None:
        """
        Tests creation and dict conversion of the VulnerabilitiesConfig DTO

        :param example_vulnerabilities_config: an example VulnerabilitiesConfig
        :return: None
        """
        assert isinstance(example_vulnerabilities_config.to_dict(), dict)
        assert isinstance(VulnerabilitiesConfig.from_dict(example_vulnerabilities_config.to_dict()),
                          VulnerabilitiesConfig)
        assert VulnerabilitiesConfig.from_dict(example_vulnerabilities_config.to_dict()).to_dict() == \
               example_vulnerabilities_config.to_dict()
        assert VulnerabilitiesConfig.from_dict(example_vulnerabilities_config.to_dict()) == \
               example_vulnerabilities_config

    def test_emulation_connection_obs_state(
            self, example_emulation_connection_observation_state: EmulationConnectionObservationState) -> None:
        """
        Tests creation and dict conversion of the VulnerabilitiesConfig DTO

        :param example_emulation_connection_observation_state: an example EmulationConnectionObservationState
        :return: None
        """
        assert isinstance(example_emulation_connection_observation_state.to_dict(), dict)
        assert isinstance(
            EmulationConnectionObservationState.from_dict(example_emulation_connection_observation_state.to_dict()),
            EmulationConnectionObservationState)
        d1 = EmulationConnectionObservationState.from_dict(
            example_emulation_connection_observation_state.to_dict()).to_dict()
        d2 = example_emulation_connection_observation_state.to_dict()
        assert d1 == d2
        assert EmulationConnectionObservationState.from_dict(
            example_emulation_connection_observation_state.to_dict()) == example_emulation_connection_observation_state

    def test_connection_setup_dto(self, example_connection_setup_dto: ConnectionSetupDTO) -> None:
        """
        Tests creation and dict conversion of the ConnectionSetup DTO

        :param example_connection_setup_dto: an example ConnectionSetupDTO
        :return: None
        """
        assert isinstance(example_connection_setup_dto.to_dict(), dict)
        assert isinstance(ConnectionSetupDTO.from_dict(example_connection_setup_dto.to_dict()), ConnectionSetupDTO)
        assert ConnectionSetupDTO.from_dict(example_connection_setup_dto.to_dict()).to_dict() == \
               example_connection_setup_dto.to_dict()
        assert ConnectionSetupDTO.from_dict(example_connection_setup_dto.to_dict()) == example_connection_setup_dto

    def test_containers_config(self, example_containers_config: ContainersConfig) -> None:
        """
        Tests creation and dict conversion of the ContainersConfig DTO

        :param example_containers_config: an example ContainersConfig
        :return: None
        """
        assert isinstance(example_containers_config.to_dict(), dict)
        assert isinstance(ContainersConfig.from_dict(example_containers_config.to_dict()), ContainersConfig)
        assert ContainersConfig.from_dict(example_containers_config.to_dict()).to_dict() == \
               example_containers_config.to_dict()
        assert ContainersConfig.from_dict(example_containers_config.to_dict()) == example_containers_config

    def test_flags_config(self, example_flags_config: FlagsConfig) -> None:
        """
        Tests creation and dict conversion of the FlagsConfig DTO

        :param example_flags_config: an example FlagsConfig
        :return: None
        """
        assert isinstance(example_flags_config.to_dict(), dict)
        assert isinstance(FlagsConfig.from_dict(example_flags_config.to_dict()), FlagsConfig)
        assert FlagsConfig.from_dict(example_flags_config.to_dict()).to_dict() == example_flags_config.to_dict()
        assert FlagsConfig.from_dict(example_flags_config.to_dict()) == example_flags_config

    def test_topology_config(self, example_topology_config: TopologyConfig) -> None:
        """
        Tests creation and dict conversion of the TopologyConfig DTO

        :param example_topology_config: an example TopologyConfig
        :return: None
        """
        assert isinstance(example_topology_config.to_dict(), dict)
        assert isinstance(TopologyConfig.from_dict(example_topology_config.to_dict()), TopologyConfig)
        assert TopologyConfig.from_dict(example_topology_config.to_dict()).to_dict() == \
               example_topology_config.to_dict()
        assert TopologyConfig.from_dict(example_topology_config.to_dict()) == example_topology_config

    def test_host_manager_config(self, example_host_manager_config: HostManagerConfig) -> None:
        """
        Tests creation and dict conversion of the HostManagerConfig DTO

        :param example_host_manager_config: an example HostManagerConfig
        :return: None
        """
        assert isinstance(example_host_manager_config.to_dict(), dict)
        assert isinstance(HostManagerConfig.from_dict(example_host_manager_config.to_dict()), HostManagerConfig)
        assert HostManagerConfig.from_dict(example_host_manager_config.to_dict()).to_dict() == \
               example_host_manager_config.to_dict()
        assert HostManagerConfig.from_dict(example_host_manager_config.to_dict()) == example_host_manager_config

    def test_snort_ids_manager_config(self, example_snort_ids_manager_config: SnortIDSManagerConfig) -> None:
        """
        Tests creation and dict conversion of the SnortIDSManagerConfig DTO

        :param example_snort_ids_manager_config: an example SnortIDSManagerConfig
        :return: None
        """
        assert isinstance(example_snort_ids_manager_config.to_dict(), dict)
        assert isinstance(SnortIDSManagerConfig.from_dict(example_snort_ids_manager_config.to_dict()),
                          SnortIDSManagerConfig)
        assert SnortIDSManagerConfig.from_dict(example_snort_ids_manager_config.to_dict()).to_dict() == \
               example_snort_ids_manager_config.to_dict()
        assert SnortIDSManagerConfig.from_dict(example_snort_ids_manager_config.to_dict()) == \
               example_snort_ids_manager_config

    def test_emulation_env_config(self, example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Tests creation and dict conversion of the EmulationEnvConfig DTO

        :param example_emulation_env_config: an example EmulationEnvConfig
        :return: None
        """
        assert isinstance(example_emulation_env_config.to_dict(), dict)
        assert isinstance(EmulationEnvConfig.from_dict(example_emulation_env_config.to_dict()), EmulationEnvConfig)
        assert EmulationEnvConfig.from_dict(example_emulation_env_config.to_dict()).to_dict() == \
               example_emulation_env_config.to_dict()
        assert EmulationEnvConfig.from_dict(example_emulation_env_config.to_dict()) == example_emulation_env_config
