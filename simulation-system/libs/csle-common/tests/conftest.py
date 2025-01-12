import time
import numpy as np
import pytest
from typing import Dict
import csle_collector.constants.constants as collector_constants
import csle_common.constants.constants as constants
from csle_collector.client_manager.dao.client import Client
from csle_collector.client_manager.dao.constant_arrival_config import ConstantArrivalConfig
from csle_collector.client_manager.dao.workflow_markov_chain import WorkflowMarkovChain
from csle_collector.client_manager.dao.workflow_service import WorkflowService
from csle_collector.client_manager.dao.workflows_config import WorkflowsConfig
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_outcome import EmulationAttackerActionOutcome
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_common.dao.emulation_config.beats_config import BeatsConfig
from csle_common.dao.emulation_config.client_population_config import ClientPopulationConfig
from csle_common.dao.emulation_config.cluster_config import ClusterConfig
from csle_common.dao.emulation_config.cluster_node import ClusterNode
from csle_common.dao.emulation_config.config import Config
from csle_common.dao.emulation_config.containers_config import ContainersConfig
from csle_common.dao.emulation_config.docker_stats_manager_config import DockerStatsManagerConfig
from csle_common.dao.emulation_config.elk_config import ElkConfig
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.emulation_execution import EmulationExecution
from csle_common.dao.emulation_config.flag import Flag
from csle_common.dao.emulation_config.flags_config import FlagsConfig
from csle_common.dao.emulation_config.host_manager_config import HostManagerConfig
from csle_common.dao.emulation_config.network_service import NetworkService
from csle_common.dao.emulation_config.node_beats_config import NodeBeatsConfig
from csle_common.dao.emulation_config.node_flags_config import NodeFlagsConfig
from csle_common.dao.emulation_config.node_services_config import NodeServicesConfig
from csle_common.dao.emulation_config.node_traffic_config import NodeTrafficConfig
from csle_common.dao.emulation_config.node_users_config import NodeUsersConfig
from csle_common.dao.emulation_config.node_vulnerability_config import NodeVulnerabilityConfig
from csle_common.dao.emulation_config.ossec_ids_manager_config import OSSECIDSManagerConfig
from csle_common.dao.emulation_config.ovs_config import OVSConfig
from csle_common.dao.emulation_config.ovs_switch_config import OvsSwitchConfig
from csle_common.dao.emulation_config.packet_delay_distribution_type import PacketDelayDistributionType
from csle_common.dao.emulation_config.packet_loss_type import PacketLossType
from csle_common.dao.emulation_config.resources_config import ResourcesConfig
from csle_common.dao.emulation_config.sdn_controller_config import SDNControllerConfig
from csle_common.dao.emulation_config.sdn_controller_type import SDNControllerType
from csle_common.dao.emulation_config.services_config import ServicesConfig
from csle_common.dao.emulation_config.snort_ids_manager_config import SnortIDSManagerConfig
from csle_common.dao.emulation_config.topology_config import TopologyConfig
from csle_common.dao.emulation_config.traffic_config import TrafficConfig
from csle_common.dao.emulation_config.user import User
from csle_common.dao.emulation_config.users_config import UsersConfig
from csle_common.dao.emulation_config.vulnerabilities_config import VulnerabilitiesConfig
from csle_common.dao.emulation_config.vulnerability_type import VulnType
from csle_common.dao.datasets.statistics_dataset import StatisticsDataset
from csle_common.dao.datasets.traces_dataset import TracesDataset
from csle_common.dao.docker.docker_container_metadata import DockerContainerMetadata
from csle_common.dao.docker.docker_env_metadata import DockerEnvMetadata
from csle_common.dao.emulation_action.defender.emulation_defender_action_id import EmulationDefenderActionId
from csle_common.dao.emulation_action.defender.emulation_defender_action_outcome import EmulationDefenderActionOutcome
from csle_common.dao.emulation_action.defender.emulation_defender_action_type import EmulationDefenderActionType
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_config import EmulationAttackerActionConfig
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.defender.emulation_defender_action_config import EmulationDefenderActionConfig
from csle_common.dao.emulation_action_result.nikto_scan_result import NiktoScanResult
from csle_common.dao.emulation_action_result.nikto_vuln import NiktoVuln
from csle_common.dao.emulation_action_result.nmap_brute_credentials import NmapBruteCredentials
from csle_common.dao.emulation_action_result.nmap_hop import NmapHop
from csle_common.dao.emulation_action_result.nmap_http_enum import NmapHttpEnum
from csle_common.dao.emulation_action_result.nmap_http_grep import NmapHttpGrep
from csle_common.dao.emulation_action_result.nmap_os import NmapOs
from csle_common.dao.emulation_action_result.nmap_port import NmapPort
from csle_common.dao.emulation_action_result.nmap_port_status import NmapPortStatus
from csle_common.dao.emulation_action_result.nmap_host_status import NmapHostStatus
from csle_common.dao.emulation_action_result.nmap_vulscan import NmapVulscan
from csle_common.dao.emulation_action_result.nmap_trace import NmapTrace
from csle_common.dao.emulation_action_result.nmap_vuln import NmapVuln
from csle_common.dao.emulation_action_result.nmap_host_result import NmapHostResult
from csle_common.dao.emulation_action_result.nmap_scan_result import NmapScanResult
from csle_common.dao.emulation_config.client_managers_info import ClientManagersInfo
from csle_common.dao.emulation_config.docker_stats_managers_info import DockerStatsManagersInfo
from csle_common.dao.emulation_config.elk_managers_info import ELKManagersInfo
from csle_common.dao.emulation_config.snort_managers_info import SnortIdsManagersInfo
from csle_common.dao.emulation_config.ossec_managers_info import OSSECIDSManagersInfo
from csle_common.dao.emulation_config.ryu_managers_info import RyuManagersInfo
from csle_common.dao.emulation_config.host_managers_info import HostManagersInfo
from csle_common.dao.emulation_config.kafka_managers_info import KafkaManagersInfo
from csle_common.dao.emulation_observation.common.emulation_port_observation_state import EmulationPortObservationState
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_common.dao.emulation_observation.attacker. \
    emulation_attacker_machine_observation_state import EmulationAttackerMachineObservationState
from csle_common.dao.emulation_observation.common.emulation_connection_observation_state \
    import EmulationConnectionObservationState
from csle_common.dao.emulation_config.credential import Credential
from csle_common.dao.emulation_observation.common.emulation_vulnerability_observation_state \
    import EmulationVulnerabilityObservationState
from csle_common.dao.emulation_observation.defender.emulation_defender_machine_observation_state import \
    EmulationDefenderMachineObservationState
from csle_common.dao.jobs.data_collection_job_config import DataCollectionJobConfig
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace
from csle_common.dao.emulation_observation.attacker. \
    emulation_attacker_observation_state import EmulationAttackerObservationState
from csle_common.dao.emulation_config.kafka_config import KafkaConfig
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.dao.emulation_config.node_resources_config import NodeResourcesConfig
from csle_common.dao.emulation_config.node_firewall_config import NodeFirewallConfig
from csle_common.dao.emulation_config.kafka_topic import KafkaTopic
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.dao.emulation_config.node_network_config import NodeNetworkConfig
from csle_common.dao.emulation_config.default_network_firewall_config import DefaultNetworkFirewallConfig
from csle_common.dao.training.alpha_vectors_policy import AlphaVectorsPolicy
from csle_common.dao.training.dqn_policy import DQNPolicy
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.dao.training.fnn_with_softmax_policy import FNNWithSoftmaxPolicy
from csle_common.dao.training.linear_tabular_policy import LinearTabularPolicy
from csle_common.dao.training.linear_threshold_stopping_policy import LinearThresholdStoppingPolicy
from csle_common.dao.training.tabular_policy import TabularPolicy
from csle_common.dao.training.mixed_linear_tabular import MixedLinearTabularPolicy
from csle_common.dao.training.mixed_ppo_policy import MixedPPOPolicy
from csle_common.dao.training.ppo_policy import PPOPolicy
from csle_common.dao.training.random_policy import RandomPolicy
from csle_common.dao.training.vector_policy import VectorPolicy
from csle_common.dao.training.mixed_multi_threshold_stopping_policy import MixedMultiThresholdStoppingPolicy
from csle_common.dao.training.multi_threshold_stopping_policy import MultiThresholdStoppingPolicy
from csle_common.dao.jobs.system_identification_job_config import SystemIdentificationJobConfig
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.management.management_user import ManagementUser
from csle_common.dao.management.session_token import SessionToken
from csle_common.dao.emulation_observation.defender.emulation_defender_observation_state import \
    EmulationDefenderObservationState
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.simulation_config.action_space_config import ActionSpaceConfig
from csle_common.dao.simulation_config.value_type import ValueType
from csle_common.dao.simulation_config.agent_log import AgentLog
from csle_common.dao.simulation_config.env_parameter import EnvParameter
from csle_common.dao.simulation_config.env_parameters_config import EnvParametersConfig
from csle_common.dao.simulation_config.initial_state_distribution_config import InitialStateDistributionConfig
from csle_common.dao.simulation_config.joint_action_space_config import JointActionSpaceConfig
from csle_common.dao.simulation_config.joint_observation_space_config import JointObservationSpaceConfig
from csle_common.dao.simulation_config.observation_space_config import ObservationSpaceConfig
from csle_common.dao.simulation_config.observation import Observation
from csle_common.dao.simulation_config.observation_function_config import ObservationFunctionConfig
from csle_common.dao.simulation_config.player_config import PlayerConfig
from csle_common.dao.simulation_config.players_config import PlayersConfig
from csle_common.dao.simulation_config.reward_function_config import RewardFunctionConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.simulation_config.state_space_config import StateSpaceConfig
from csle_common.dao.simulation_config.state import State
from csle_common.dao.simulation_config.state_type import StateType
from csle_common.dao.simulation_config.time_step_type import TimeStepType
from csle_common.dao.simulation_config.transition_operator_config import TransitionOperatorConfig
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
from csle_common.dao.simulation_config.simulation_env_input_config import SimulationEnvInputConfig
from csle_common.dao.system_identification.empirical_conditional import EmpiricalConditional
from csle_common.dao.system_identification.empirical_system_model import EmpiricalSystemModel
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
from csle_common.dao.system_identification.gaussian_mixture_conditional import GaussianMixtureConditional
from csle_common.dao.system_identification.gaussian_mixture_system_model import GaussianMixtureSystemModel
from csle_common.dao.system_identification.gp_conditional import GPConditional
from csle_common.dao.system_identification.gp_system_model import GPSystemModel
from csle_common.dao.system_identification.mcmc_posterior import MCMCPosterior
from csle_common.dao.system_identification.mcmc_system_model import MCMCSystemModel
from csle_common.dao.system_identification.system_identification_config import SystemIdentificationConfig
from csle_common.dao.system_identification.system_model_type import SystemModelType
from csle_common.dao.training.hparam import HParam
from csle_collector.host_manager.dao.host_metrics import HostMetrics
from csle_collector.docker_stats_manager.dao.docker_stats import DockerStats
from csle_collector.snort_ids_manager.dao.snort_ids_ip_alert_counters import SnortIdsIPAlertCounters
from csle_collector.ossec_ids_manager.dao.ossec_ids_alert_counters import OSSECIdsAlertCounters
from csle_collector.client_manager.client_population_metrics import ClientPopulationMetrics
from csle_collector.snort_ids_manager.dao.snort_ids_alert_counters import SnortIdsAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_rule_counters import SnortIdsRuleCounters
from csle_common.dao.emulation_config.connection_setup_dto import ConnectionSetupDTO
from csle_collector.client_manager.client_manager_pb2 import ClientsDTO
from csle_collector.docker_stats_manager.docker_stats_manager_pb2 import DockerStatsMonitorDTO
from csle_collector.elk_manager.elk_manager_pb2 import ElkDTO
from csle_collector.host_manager.host_manager_pb2 import HostStatusDTO
from csle_collector.snort_ids_manager.snort_ids_manager_pb2 import SnortIdsMonitorDTO
from csle_collector.ossec_ids_manager.ossec_ids_manager_pb2 import OSSECIdsMonitorDTO
from csle_collector.ryu_manager.ryu_manager_pb2 import RyuDTO
from csle_collector.kafka_manager.kafka_manager_pb2 import KafkaDTO


class ExampleInputConfig(SimulationEnvInputConfig):
    """
    Test instance of the abstract SimulationEnvInputConfig class
    """

    def __init__(self, x: int) -> None:
        """
        Initializes the object

        :param x: the input parameter
        :return: None
        """
        self.x = x

    def to_dict(self) -> Dict[str, int]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, int] = {}
        d["x"] = self.x
        return d

    @staticmethod
    def from_dict(d: Dict[str, int]) -> "ExampleInputConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = ExampleInputConfig(x=d["x"])
        return obj

    @staticmethod
    def from_json_file(json_file_path: str) -> "ExampleInputConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return ExampleInputConfig.from_dict(json.loads(json_str))


@pytest.fixture
def example_client_manager_status() -> ClientsDTO:
    """
    Fixture that returns an example ClientsDTO object

    :return: an example ClientsDTO object
    """
    return ClientsDTO(num_clients=19, client_process_active=True, producer_active=False,
                      clients_time_step_len_seconds=30, producer_time_step_len_seconds=30)


@pytest.fixture
def example_docker_stats_monitor_dto() -> DockerStatsMonitorDTO:
    """
    Fixture that returns an example DockerStatsMonitorDTO object

    :return: an example DockerStatsMonitorDTO object
    """
    return DockerStatsMonitorDTO(num_monitors=1, emulations=["testem"], emulation_executions=[15])


@pytest.fixture
def example_elk_manager_status_dto() -> ElkDTO:
    """
    Fixture that returns an example ElkDTO object

    :return: an example ElkDTO object
    """
    return ElkDTO(elasticRunning=False, kibanaRunning=True, logstashRunning=True)


@pytest.fixture
def example_snort_ids_manager_status_dto() -> SnortIdsMonitorDTO:
    """
    Fixture that returns an example SnortIdsMonitorDTO object

    :return: an example SnortIdsMonitorDTO object
    """
    return SnortIdsMonitorDTO(monitor_running=True, snort_ids_running=True)


@pytest.fixture
def example_ossec_ids_manager_status_dto() -> OSSECIdsMonitorDTO:
    """
    Fixture that returns an example OSSECIdsMonitorDTO object

    :return: an example OSSECIdsMonitorDTO object
    """
    return OSSECIdsMonitorDTO(monitor_running=True, ossec_ids_running=True)


@pytest.fixture
def example_host_manager_status_dto() -> HostStatusDTO:
    """
    Fixture that returns an example HostStatusDTO object

    :return: an example HostStatusDTO object
    """
    return HostStatusDTO(monitor_running=True, filebeat_running=False, packetbeat_running=True, metricbeat_running=True,
                         heartbeat_running=False)


@pytest.fixture
def example_kafka_manager_status_dto() -> KafkaDTO:
    """
    Fixture that returns an example KafkaDTO object

    :return: an example KafkaDTO object
    """
    return KafkaDTO(running=True, topics=["topic1"])


@pytest.fixture
def example_kafka_managers_info(example_kafka_manager_status_dto: KafkaDTO) -> KafkaManagersInfo:
    """
    Fixture that returns an example KafkaManagersInfo object

    :param example_kafka_manager_status_dto: an example KafkaDTO
    :return: an example KafkaManagersInfo object
    """
    return KafkaManagersInfo(
        ips=["192.168.1.1"], ports=[3333], emulation_name="testem", execution_id=15,
        kafka_managers_statuses=[example_kafka_manager_status_dto], kafka_managers_running=[True])


@pytest.fixture
def example_host_managers_info(example_host_manager_status_dto: HostStatusDTO) -> HostManagersInfo:
    """
    Fixture that returns an example HostManagersInfo object

    :param example_host_manager_status_dto: an example HostStatusDTO
    :return: an example HostManagersInfo object
    """
    return HostManagersInfo(
        ips=["192.168.1.1"], ports=[3333], emulation_name="testem", execution_id=15,
        host_managers_statuses=[example_host_manager_status_dto], host_managers_running=[True])


@pytest.fixture
def example_ryu_manager_status_dto() -> RyuDTO:
    """
    Fixture that returns an example RyuDTO object

    :return: an example RyuDTO object
    """
    return RyuDTO(ryu_running=True, monitor_running=False, port=3000, web_port=8080, controller="8.8.8.8",
                  kafka_ip="7.7.7.7", kafka_port=9090, time_step_len=30)


@pytest.fixture
def example_ryu_managers_info(example_ryu_manager_status_dto: RyuDTO) -> RyuManagersInfo:
    """
    Fixture that returns an example RyuManagersInfo object

    :param example_ryu_manager_status_dto: an example RyuDTO
    :return: an example RyuManagersInfo object
    """
    return RyuManagersInfo(
        ips=["192.168.1.1"], ports=[3333], emulation_name="testem", execution_id=15,
        ryu_managers_statuses=[example_ryu_manager_status_dto], ryu_managers_running=[True])


@pytest.fixture
def example_ossec_ids_managers_info(example_ossec_ids_manager_status_dto: OSSECIdsMonitorDTO) -> OSSECIDSManagersInfo:
    """
    Fixture that returns an example OSSECIDSManagersInfo object

    :param example_ossec_ids_manager_status_dto: an example OSSECIdsMonitorDTO
    :return: an example OSSECIDSManagersInfo object
    """
    return OSSECIDSManagersInfo(
        ips=["192.168.1.1"], ports=[3333], emulation_name="testem", execution_id=15,
        ossec_ids_managers_statuses=[example_ossec_ids_manager_status_dto], ossec_ids_managers_running=[True])


@pytest.fixture
def example_snort_ids_managers_info(example_snort_ids_manager_status_dto: SnortIdsMonitorDTO) -> SnortIdsManagersInfo:
    """
    Fixture that returns an example SnortIdsManagersInfo object

    :param example_snort_ids_manager_status_dto: an example SnortIdsMonitorDTO
    :return: an example SnortIdsManagersInfo object
    """
    return SnortIdsManagersInfo(
        ips=["192.168.1.1"], ports=[3333], emulation_name="testem", execution_id=15,
        snort_ids_managers_statuses=[example_snort_ids_manager_status_dto], snort_ids_managers_running=[True])


@pytest.fixture
def example_elk_managers_info(example_elk_manager_status_dto: ElkDTO) -> ELKManagersInfo:
    """
    Fixture that returns an example ELKManagersInfo object

    :param example_elk_manager_status_dto: an example ElkDTO
    :return: an example ELKManagersInfo object
    """
    return ELKManagersInfo(
        ips=["192.168.1.1"], ports=[3333], emulation_name="testem", execution_id=15,
        elk_managers_statuses=[example_elk_manager_status_dto], elk_managers_running=[True], local_kibana_port=5050,
        physical_server_ip="8.8.8.8")


@pytest.fixture
def example_docker_stats_managers_info(example_docker_stats_monitor_dto: DockerStatsMonitorDTO) \
        -> DockerStatsManagersInfo:
    """
    Fixture that returns an example DockerStatsManagersInfo object

    :param example_docker_stats_monitor_dto: an example DockerStatsMonitorDTO
    :return: an example DockerStatsManagersInfo object
    """
    return DockerStatsManagersInfo(
        ips=["192.168.1.1"], ports=[3333], emulation_name="testem", execution_id=15,
        docker_stats_managers_statuses=[example_docker_stats_monitor_dto], docker_stats_managers_running=[True])


@pytest.fixture
def example_client_managers_info(example_client_manager_status: ClientsDTO) -> ClientManagersInfo:
    """
    Fixture that returns an example ClientManagersInfo object

    :param example_client_manager_status: an example ClientsDTO
    :return: an example ClientManagersInfo object
    """
    return ClientManagersInfo(
        ips=["192.168.25.12"], ports=[2333], emulation_name="test_em", execution_id=19,
        client_managers_running=[True], client_managers_statuses=[example_client_manager_status])


@pytest.fixture
def example_credential() -> Credential:
    """
    Fixture that returns an example Credential object

    :return: an example Credential object
    """
    return Credential(username="testuser", pw="testpw", port=2911, protocol=TransportProtocol.UDP,
                      service="myservice", root=False)


@pytest.fixture
def example_traces_dataset() -> TracesDataset:
    """
    Fixture that returns an example TracesDataset object

    :return: an example TracesDataset object
    """
    return TracesDataset(name="test_dataset", description="test_descr", download_count=100,
                         file_path="test_path", url="test_url", date_added=time.time(),
                         size_in_gb=5, compressed_size_in_gb=17, citation="test_citation",
                         num_files=50, file_format="json", added_by="testadded", columns="col1,col2",
                         data_schema={}, num_attributes_per_time_step=10, num_traces=15)


@pytest.fixture
def example_statistics_dataset() -> StatisticsDataset:
    """
    Fixture that returns an example StatisticsDataset object

    :return: an example StatisticsDataset object
    """
    return StatisticsDataset(name="test_dataset", description="test_descr", download_count=100,
                             file_path="test_path", url="test_url", date_added=time.time(), num_measurements=100,
                             num_metrics=10, size_in_gb=5, compressed_size_in_gb=17, citation="test_citation",
                             num_files=50, file_format="json", added_by="testadded", conditions="cond1,cond2",
                             metrics="metric1,metric2", num_conditions=10)


@pytest.fixture
def example_docker_container_metadata() -> DockerContainerMetadata:
    """
    Fixture that returns an example DockerContainerMetadata object

    :return: an example DockerContainerMetadata object
    """
    return DockerContainerMetadata(
        name="cont1", status="test", short_id="shortid", image_short_id="imgshort", image_tags=[], id="testid",
        created="1 Aug", ip="testIp", network_id=5, gateway="gw", mac="mymac", ip_prefix_len=16,
        name2="secondname", level="level1", hostname="host1", image_name="img1", net="mynet", dir="mydir",
        config_path="mycfg", container_handle=None, kafka_container="kafkacont", emulation="myem")


@pytest.fixture
def example_docker_env_metadata(example_docker_container_metadata: DockerContainerMetadata) \
        -> DockerEnvMetadata:
    """
    Fixture that returns an example DockerEnvMetadata object

    :param example_docker_container_metadata: an example DockerContainerMetadata
    :return: an example DockerEnvMetadata object
    """
    return DockerEnvMetadata(
        containers=[example_docker_container_metadata], name="myenv", subnet_prefix="myprefix", subnet_mask="mymask",
        level="mylevel", config=None, kafka_config=None)


@pytest.fixture
def example_emulation_attacker_action() -> EmulationAttackerAction:
    """
    Fixture that returns an example DockerContainerMetadata object

    :return: an example EmulationAttackerAction object
    """
    return EmulationAttackerAction(
        id=EmulationAttackerActionId.CONTINUE, name="test", cmds=["cmd1"],
        type=EmulationAttackerActionType.CONTINUE, descr="testtest", ips=["ip1"], index=0,
        action_outcome=EmulationAttackerActionOutcome.CONTINUE, vulnerability="test", alt_cmds=["altcmd1"],
        backdoor=False, execution_time=0.0, ts=0.0
    )


@pytest.fixture
def example_emulation_attacker_action_config(example_emulation_attacker_action: EmulationAttackerAction) \
        -> EmulationAttackerActionConfig:
    """
    Fixture that returns an example EmulationAttackerActionConfig object

    :param example_emulation_attacker_action: an example EmulationAttackerAction
    :return: an example EmulationAttackerActionConfig object
    """
    return EmulationAttackerActionConfig(
        num_indices=10, actions=[example_emulation_attacker_action],
        nmap_action_ids=[EmulationAttackerActionId.NMAP_VULNERS_ALL],
        network_service_action_ids=[EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST],
        shell_action_ids=[EmulationAttackerActionId.CVE_2015_1427_EXPLOIT],
        nikto_action_ids=[EmulationAttackerActionId.NIKTO_WEB_HOST_SCAN],
        masscan_action_ids=[EmulationAttackerActionId.MASSCAN_ALL_SCAN],
        stopping_action_ids=[EmulationAttackerActionId.STOP, EmulationAttackerActionId.CONTINUE])


@pytest.fixture
def example_emulation_defender_action() -> EmulationDefenderAction:
    """
    Fixture that returns an example EmulationDefenderAction object

    :return: an example EmulationDefenderAction object
    """
    return EmulationDefenderAction(
        id=EmulationDefenderActionId.STOP, name="testname", cmds=["cmd1"],
        type=EmulationDefenderActionType.CONTINUE, ips=["ip1", "ip2"], index=0,
        action_outcome=EmulationDefenderActionOutcome.CONTINUE, alt_cmds=["alt1"], execution_time=0.0,
        ts=0.0, descr="testdescr")


@pytest.fixture
def example_emulation_defender_action_config(example_emulation_defender_action: EmulationDefenderAction) \
        -> EmulationDefenderActionConfig:
    """
    Fixture that returns an example EmulationAttackerActionConfig object

    :param example_emulation_defender_action: an example EmulationDefenderAction
    :return: an example EmulationAttackerActionConfig object
    """
    return EmulationDefenderActionConfig(
        num_indices=10, actions=[example_emulation_defender_action],
        stopping_action_ids=[EmulationDefenderActionId.STOP, EmulationDefenderActionId.CONTINUE],
        multiple_stop_actions=[],
        multiple_stop_actions_ids=[EmulationDefenderActionId.STOP, EmulationDefenderActionId.CONTINUE])


@pytest.fixture
def example_cluster_node() -> ClusterNode:
    """
    Fixture that returns an example ClusterNode object

    :return: an example ClusterNode object
    """
    return ClusterNode(ip="123.456.78.99", leader=True, cpus=1, gpus=2, RAM=3)


@pytest.fixture
def example_cluster_config(example_cluster_node: ClusterNode) -> ClusterConfig:
    """
    Fixture that returns an example ClusterConfig object

    :param example_cluster_node: an example ClusterNode
    :return: an example ClusterConfig object
    """
    return ClusterConfig([example_cluster_node])


@pytest.fixture
def example_config(example_cluster_config: ClusterConfig) -> Config:
    """
    Help function that returns a config class when making fixtures and testing

    :param example_cluster_config: an example ClusterConfig
    :return: Config class
    """
    config = Config(
        management_admin_username_default="admin",
        management_admin_password_default="admin",
        management_admin_first_name_default="Admin",
        management_admin_last_name_default="Adminson",
        management_admin_email_default="admin@CSLE.com",
        management_admin_organization_default="CSLE",
        management_guest_username_default="guest",
        management_guest_password_default="guest",
        management_guest_first_name_default="Guest",
        management_guest_last_name_default="Guestson",
        management_guest_email_default="guest@CSLE.com",
        management_guest_organization_default="CSLE",
        ssh_admin_username="null",
        ssh_admin_password="null",
        ssh_agent_username="null",
        ssh_agent_password="null",
        metastore_user="null",
        metastore_password="null",
        metastore_database_name="null",
        metastore_ip="null",
        node_exporter_port=1,
        grafana_port=1,
        management_system_port=1,
        cadvisor_port=1,
        prometheus_port=1,
        node_exporter_pid_file="null",
        pgadmin_port=1,
        csle_mgmt_webapp_pid_file="null",
        docker_stats_manager_log_file="null",
        docker_stats_manager_log_dir="null",
        docker_stats_manager_port=1,
        docker_stats_manager_max_workers=1,
        docker_stats_manager_outfile="null",
        docker_stats_manager_pidfile="null",
        prometheus_pid_file="null",
        prometheus_log_file="null",
        prometheus_config_file="null",
        default_log_dir="null",
        cluster_config=example_cluster_config,
        node_exporter_log_file="null",
        allow_registration=True,
        grafana_username="null",
        grafana_password="null",
        pgadmin_username="null",
        pgadmin_password="null",
        postgresql_log_dir="null",
        nginx_log_dir="null",
        flask_log_file="null",
        cluster_manager_log_file="null",
        version="0.0.6",
        localhost=False
    )
    return config


@pytest.fixture
def example_container_network() -> ContainerNetwork:
    """
    Fixture that returns an example ContainerNetwork object

    :return: an example ContainerNetwork object
    """
    return ContainerNetwork(name=f'{constants.CSLE.CSLE_NETWORK_PREFIX}1', subnet_mask="Subnet1", bitmask="null",
                            subnet_prefix="null", interface="eth0")


@pytest.fixture
def example_user() -> User:
    """
    Fixture that returns an example User object

    :return: an example User object
    """
    return User(username="JDoe", pw="JDoe", root=True)


@pytest.fixture
def example_node_container_config(example_container_network: ContainerNetwork) -> NodeContainerConfig:
    """
    Fixture that returns an example NodeContainerConfig object

    :param example_container_network: an example ContainerNetwork
    :return: an example NodeContainerConfig object
    """
    return NodeContainerConfig(name="csle_",
                               ips_and_networks=[("123.456.78.99", example_container_network)],
                               version="null", level="csle",
                               restart_policy="JDoePolicy", suffix="null",
                               os="null", execution_ip_first_octet=-1,
                               docker_gw_bridge_ip="123.456.78.99",
                               physical_host_ip="123.456.78.99")


@pytest.fixture
def example_containers_config(example_container_network: ContainerNetwork,
                              example_node_container_config: NodeContainerConfig) -> ContainersConfig:
    """
    Fixture that returns an example ContainersConfig object

    :param example_container_network: an example ContainerNetwork
    :param example_node_container_config: an example NodeContainerConfig
    :return: an example ContainersConfig object
    """
    return ContainersConfig(containers=[example_node_container_config],
                            agent_ip="123.456.78.99",
                            router_ip="123.456.78.99",
                            networks=[example_container_network],
                            ids_enabled=False,
                            vulnerable_nodes=None,
                            agent_reachable_nodes=None)


@pytest.fixture
def example_node_users_config(example_user: User) -> NodeUsersConfig:
    """
    Fixture that returns an example NodeUsersConfig object

    :param example_user: an example User
    :return: an example NodeUsersConfig object
    """
    return NodeUsersConfig(ip="123.456.78.99", users=[User(username="JDoe", pw="JDoe", root=True)],
                           docker_gw_bridge_ip="null", physical_host_ip="123.456.78.99")


@pytest.fixture
def example_users_config(example_node_users_config: NodeUsersConfig) -> UsersConfig:
    """
    Fixture that returns an example UsersConfig object

    :param example_node_users_config: an example NodeUsersConfig
    :return: an example UsersConfig object
    """
    return UsersConfig(users_configs=[example_node_users_config])


@pytest.fixture
def example_flag() -> Flag:
    """
    Fixture that returns an example Flag object

    :return: an example Flag object
    """
    return Flag(name="JohnDoe", dir="null", id=1, path="null", requires_root=False, score=1)


@pytest.fixture
def example_node_flags_config(example_flag: Flag) -> NodeFlagsConfig:
    """
    Fixture that returns an example NodeFlagsConfig object

    :param example_flag: an example Flag
    :return: an example NodeFlagsConfig object
    """
    return NodeFlagsConfig(ip="123.456.78.99", flags=[example_flag], docker_gw_bridge_ip="null",
                           physical_host_ip="123.456.78.99")


@pytest.fixture
def example_node_vulnerability_config(example_credential: Credential) -> NodeVulnerabilityConfig:
    """
    Fixture that returns an example NodeVulnerabilityConfig object

    :param example_credential: an example Credential
    :return: an example NodeVulnerabilityConfig object
    """
    return NodeVulnerabilityConfig(ip="123.456.78.99", vuln_type=VulnType.WEAK_PW, name="JohnDoe", port=1,
                                   protocol=TransportProtocol.TCP, credentials=[example_credential], cvss=2.0,
                                   cve=None, service="null", root=False, docker_gw_bridge_ip="123.456.78.99",
                                   physical_host_ip="123.456.78.99")


@pytest.fixture
def example_emulation_connection_observation_state(example_credential: Credential) \
        -> EmulationConnectionObservationState:
    """
    Fixture that returns an example EmulationConnectionObservationState object

    :param example_credential: an example Credential
    :return: an example EmulationConnectionObservationState object
    """
    return EmulationConnectionObservationState(
        conn=None, credential=example_credential, root=True, service="serv", port=3030, tunnel_port=4000,
        tunnel_thread=None, interactive_shell=None, proxy=None, ip="8.8.8.8")


@pytest.fixture
def example_connection_setup_dto(example_credential: Credential,
                                 example_emulation_connection_observation_state: EmulationConnectionObservationState) \
        -> ConnectionSetupDTO:
    """
    Fixture that returns an example ConnectionSetupDTO object

    :param example_credential: an example Credential
    :param example_emulation_connection_observation_state: an example EmulationConnectionObservationState
    :return: an example ConnectionSetupDTO object
    """
    return ConnectionSetupDTO(
        connected=True, credentials=[example_credential], target_connections=[], tunnel_threads=[],
        forward_ports=[1101],
        ports=[3030], interactive_shells=[], non_failed_credentials=[example_credential],
        proxies=[example_emulation_connection_observation_state], ip="5.5.5.5", total_time=0.0)


@pytest.fixture
def example_vulnerabilities_config(example_node_vulnerability_config: NodeVulnerabilityConfig) \
        -> VulnerabilitiesConfig:
    """
    Fixture that returns an example VulnerabilitiesConfig object

    :param example_node_vulnerability_config: an example NodeVulnerabilityConfig
    :return: an example VulnerabilitiesConfig object
    """
    return VulnerabilitiesConfig(node_vulnerability_configs=[example_node_vulnerability_config])


@pytest.fixture
def example_default_network_firewall_config(example_container_network: ContainerNetwork) \
        -> DefaultNetworkFirewallConfig:
    """
    Fixture that returns an example DefaultNetworkFirewallConfig object

    :param example_container_network: an example ContainerNetwork
    :return: an example DefaultNetworkFirewallConfig object
    """
    return DefaultNetworkFirewallConfig(ip=None, default_gw="null", default_input="null",
                                        default_output="null", default_forward="null",
                                        network=example_container_network)


@pytest.fixture
def example_node_firewall_config(example_default_network_firewall_config: DefaultNetworkFirewallConfig) \
        -> NodeFirewallConfig:
    """
    Fixture that returns an example NodeFirewallConfig object

    :param example_default_network_firewall_config: an example DefaultNetworkFirewallConfig
    :return: an example NodeFirewallConfig object
    """
    return NodeFirewallConfig(ips_gw_default_policy_networks=[example_default_network_firewall_config],
                              hostname="JohnDoe", output_accept={"null"},
                              input_accept={"null"}, forward_accept={"null"},
                              output_drop={"null"}, input_drop={"null"},
                              forward_drop={"null"}, routes={("null", "null")},
                              docker_gw_bridge_ip="123.456.78.99",
                              physical_host_ip="123.456.78.99")


@pytest.fixture
def example_topology_config(example_node_firewall_config: NodeFirewallConfig) -> TopologyConfig:
    """
    Fixture that returns an example NodeFirewallConfig object

    :param example_node_firewall_config: an example NodeFirewallConfig
    :return: an example NodeFirewallConfig object
    """
    return TopologyConfig(node_configs=[example_node_firewall_config], subnetwork_masks=["null"])


@pytest.fixture
def example_node_traffic_config() -> NodeTrafficConfig:
    """
    Fixture that returns an example NodeTrafficConfig object

    :return: an example NodeTrafficConfig object
    """
    return NodeTrafficConfig(ip="123.456.78.99",
                             commands=["JDoeCommands"],
                             traffic_manager_log_file="null",
                             traffic_manager_log_dir="null",
                             traffic_manager_max_workers=5,
                             traffic_manager_port=50043,
                             docker_gw_bridge_ip="123.456.78.99",
                             physical_host_ip="123.456.78.99")


@pytest.fixture
def example_node_network_config() -> NodeNetworkConfig:
    """
    Fixture that returns an example NodeNetworkConfig object

    :return: an example NodeNetworkConfig object
    """
    return NodeNetworkConfig(interface=constants.NETWORKING.ETH0, limit_packets_queue=30000,
                             packet_delay_ms=0.1, packet_delay_jitter_ms=0.025,
                             packet_delay_correlation_percentage=25.5,
                             packet_delay_distribution=PacketDelayDistributionType.PARETONORMAL,
                             packet_loss_type=PacketLossType.GEMODEL,
                             packet_loss_rate_random_percentage=2.3,
                             packet_loss_random_correlation_percentage=25.6,
                             loss_state_markov_chain_p13=0.1,
                             loss_state_markov_chain_p31=0.1,
                             loss_state_markov_chain_p32=0.1,
                             loss_state_markov_chain_p23=0.1,
                             loss_state_markov_chain_p14=0.1,
                             loss_gemodel_p=0.0001,
                             loss_gemodel_r=0.999,
                             loss_gemodel_h=0.0001,
                             loss_gemodel_k=0.9999,
                             packet_corrupt_percentage=0.00001,
                             packet_corrupt_correlation_percentage=25.7,
                             packet_duplicate_percentage=0.00001,
                             packet_duplicate_correlation_percentage=25,
                             packet_reorder_percentage=0.0025,
                             packet_reorder_correlation_percentage=25,
                             packet_reorder_gap=5,
                             rate_limit_mbit=100,
                             packet_overhead_bytes=0,
                             cell_overhead_bytes=0)


@pytest.fixture
def example_node_resources_config(example_node_network_config: NodeNetworkConfig) -> NodeResourcesConfig:
    """
    Fixture that returns an example NodeResourcesConfig object

    :param example_node_network_config: an example NodeNetworkConfig
    :return: an example NodeResourcesConfig object
    """
    return NodeResourcesConfig(container_name="Johndoe",
                               num_cpus=5, available_memory_gb=5,
                               ips_and_network_configs=[("null", example_node_network_config)],
                               docker_gw_bridge_ip="123.456.78.99",
                               physical_host_ip="123.456.78.99")


@pytest.fixture
def example_constant_arrival_config() -> ConstantArrivalConfig:
    """
    Fixture that returns an example ConstantArrivalConfig object

    :return: an example ConstantArrivalConfig object
    """
    return ConstantArrivalConfig(lamb=1.0)


@pytest.fixture
def example_client(example_constant_arrival_config: ConstantArrivalConfig) -> Client:
    """
    Fixture that returns an example Client object

    :param example_constant_arrival_config: an example ConstantArrivalConfig
    :return: an example Client object
    """
    return Client(id=1, workflow_distribution=[1.0],
                  arrival_config=example_constant_arrival_config,
                  mu=4, exponential_service_time=False)


@pytest.fixture
def example_workflow_markov_chain() -> WorkflowMarkovChain:
    """
    Fixture that returns an example WorkflowMarkovChain object

    :return: an example WorkflowMarkovChain object
    """
    return WorkflowMarkovChain(transition_matrix=[[1.0]], initial_state=1, id=1)


@pytest.fixture
def example_workflow_service() -> WorkflowService:
    """
    Fixture that returns an example WorkflowService object

    :return: an example WorkflowService object
    """
    return WorkflowService(ips_and_commands=[("null", ["null"])], id=1)


@pytest.fixture
def example_workflows_config(example_workflow_service: WorkflowService,
                             example_workflow_markov_chain: WorkflowMarkovChain) -> WorkflowsConfig:
    """
    Fixture that returns an example WorkflowService object

    :param example_workflow_service: an example WorkflowService
    :param example_workflow_markov_chain: an example WorkflowMarkovChain
    :return: an example WorkflowService object
    """
    return WorkflowsConfig(workflow_markov_chains=[example_workflow_markov_chain],
                           workflow_services=[example_workflow_service])


@pytest.fixture
def example_client_population_config(example_client: Client, example_container_network: ContainerNetwork,
                                     example_workflows_config: WorkflowsConfig) -> ClientPopulationConfig:
    """
    Fixture that returns an example ClientPopulationConfig object

    :param example_container_network: an example ContainerNetwork
    :param example_client: an example Client
    :param example_workflows_config: an example WorkflowsConfig
    :return: an example ClientPopulationConfig object
    """
    return ClientPopulationConfig(ip="123.456.78.99",
                                  networks=[example_container_network],
                                  client_manager_port=5,
                                  client_manager_log_file="null",
                                  client_manager_log_dir="null",
                                  client_manager_max_workers=5,
                                  clients=[example_client],
                                  workflows_config=example_workflows_config,
                                  client_time_step_len_seconds=1,
                                  docker_gw_bridge_ip="null",
                                  physical_host_ip="123.456.78.99")


@pytest.fixture
def example_resources_config(example_node_resources_config: NodeResourcesConfig) -> ResourcesConfig:
    """
    Fixture that returns an example ResourcesConfig object

    :param example_node_resources_config: an example NodeResourcesConfig
    :return: an example ResourcesConfig object
    """
    return ResourcesConfig(node_resources_configurations=[example_node_resources_config])


@pytest.fixture
def example_traffic_config(example_node_traffic_config: NodeTrafficConfig,
                           example_client_population_config: ClientPopulationConfig) -> TrafficConfig:
    """
    Fixture that returns an example TrafficConfig object

    :param example_node_traffic_config: an example NodeTrafficConfig
    :param example_client_population_config: an example ClientPopulationConfig
    :return: an example TrafficConfig object
    """
    return TrafficConfig(node_traffic_configs=[example_node_traffic_config],
                         client_population_config=example_client_population_config)


@pytest.fixture
def example_kafka_topic() -> KafkaTopic:
    """
    Fixture that returns an example KafkaTopic object

    :return: an example KafkaTopic object
    """
    return KafkaTopic(name="JohhnDoe", num_partitions=3, num_replicas=5, attributes=["null"], retention_time_hours=3)


@pytest.fixture
def example_kafka_config(example_kafka_topic: KafkaTopic, example_node_resources_config: NodeResourcesConfig,
                         example_node_container_config: NodeContainerConfig,
                         example_node_firewall_config: NodeFirewallConfig) -> KafkaConfig:
    """
    Fixture that returns an example KafkaConfig object

    :param example_kafka_topic: an example KafkaTopic
    :param example_node_resources_config: an example NodeResourcesConfig
    :param example_node_container_config: an example NodeContainerConfig
    :param example_node_firewall_config: an example NodeFirewallConfig
    :return: an example KafkaConfig object
    """
    return KafkaConfig(container=example_node_container_config, resources=example_node_resources_config,
                       firewall_config=example_node_firewall_config,
                       topics=[example_kafka_topic], kafka_manager_log_file="null", kafka_manager_log_dir="null",
                       kafka_manager_max_workers=9, kafka_port=9092, kafka_port_external=9292,
                       time_step_len_seconds=15, kafka_manager_port=50051, version="0.0.1")


@pytest.fixture
def example_network_service() -> NetworkService:
    """
    Fixture that returns an example NetworkService object

    :return: an example NetworkService object
    """
    return NetworkService(protocol=TransportProtocol.TCP, port=1, name="JohnDoe", credentials=None)


@pytest.fixture
def example_node_services_config(example_network_service: NetworkService) -> NodeServicesConfig:
    """
    Fixture that returns an example NodeServicesConfig object

    :param example_network_service: an example NetworkService
    :return: an example NodeServicesConfig object
    """
    return NodeServicesConfig(ip="123.456.78.99", services=[example_network_service])


@pytest.fixture
def example_services_config(example_node_services_config: NodeServicesConfig) -> ServicesConfig:
    """
    Fixture that returns an example ServicesConfig object

    :param example_node_services_config: an example NodeServicesConfig
    :return: an example ServicesConfig object
    """
    return ServicesConfig(services_configs=[example_node_services_config])


@pytest.fixture
def example_ovs_switch_config() -> OvsSwitchConfig:
    """
    Fixture that returns an example OvsSwitchConfig object

    :return: an example OvsSwitchConfig object
    """
    return OvsSwitchConfig(container_name="JohnDoe", ip="123.456.78.99", openflow_protocols=["null"],
                           controller_ip="123.456.78.99", controller_port=2,
                           controller_transport_protocol="null",
                           docker_gw_bridge_ip="null", physical_host_ip="123.456.78.99")


@pytest.fixture
def example_ovs_config(example_ovs_switch_config: OvsSwitchConfig) -> OVSConfig:
    """
    Fixture that returns an example OVSConfig object

    :param example_ovs_switch_config: an example OvsSwitchConfig
    :return: an example OVSConfig object
    """
    return OVSConfig(switch_configs=[example_ovs_switch_config])


@pytest.fixture
def example_sdn_controller_config(example_node_container_config: NodeContainerConfig,
                                  example_node_firewall_config: NodeFirewallConfig,
                                  example_node_resources_config: NodeResourcesConfig) -> SDNControllerConfig:
    """
    Fixture that returns an example SDNControllerConfig object

    :param example_node_container_config: an example NodeContainerConfig
    :param example_node_firewall_config: an example NodeFirewallConfig
    :param example_node_resources_config: an example NodeResourcesConfig
    :return: an example SDNControllerConfig object
    """
    return SDNControllerConfig(container=example_node_container_config, resources=example_node_resources_config,
                               firewall_config=example_node_firewall_config,
                               controller_port=4, controller_type=SDNControllerType.RYU,
                               controller_module_name="null", controller_web_api_port=5,
                               manager_log_file="null", manager_log_dir="null", manager_max_workers=10,
                               time_step_len_seconds=15, version="0.0.1", manager_port=50042)


@pytest.fixture
def example_host_manager_config() -> HostManagerConfig:
    """
    Fixture that returns an example HostManagerConfig object

    :return: an example HostManagerConfig object
    """
    return HostManagerConfig(host_manager_log_file="null", host_manager_log_dir="null",
                             host_manager_max_workers=5, time_step_len_seconds=15, host_manager_port=50049,
                             version="0.0.1")


@pytest.fixture
def example_snort_ids_manager_config() -> SnortIDSManagerConfig:
    """
    Fixture that returns an example SnortIDSManagerConfig object

    :return: an example SnortIDSManagerConfig object
    """
    return SnortIDSManagerConfig(snort_ids_manager_log_file="null", snort_ids_manager_log_dir="null",
                                 snort_ids_manager_max_workers=5, time_step_len_seconds=15,
                                 snort_ids_manager_port=50048, version="0.0.1")


@pytest.fixture
def example_ossec_ids_manager_config() -> OSSECIDSManagerConfig:
    """
    Fixture that returns an example OSSECIDSManagerConfig object

    :return: an example OSSECIDSManagerConfig object
    """
    return OSSECIDSManagerConfig(ossec_ids_manager_log_file="null", ossec_ids_manager_log_dir="null",
                                 ossec_ids_manager_max_workers=5, time_step_len_seconds=15,
                                 ossec_ids_manager_port=50047, version="0.0.1")


@pytest.fixture
def example_docker_stats_manager_config() -> DockerStatsManagerConfig:
    """
    Fixture that returns an example DockerStatsManagerConfig object

    :return: an example DockerStatsManagerConfig object
    """
    return DockerStatsManagerConfig(docker_stats_manager_log_file="null",
                                    docker_stats_manager_log_dir="null",
                                    docker_stats_manager_max_workers=5, time_step_len_seconds=15,
                                    docker_stats_manager_port=50046, version="0.0.1")


@pytest.fixture
def example_elk_config(example_node_container_config: NodeContainerConfig,
                       example_node_firewall_config: NodeFirewallConfig,
                       example_node_resources_config: NodeResourcesConfig) -> ElkConfig:
    """
    Fixture that returns an example ElkConfig object

    :param example_node_container_config: an example NodeContainerConfig
    :param example_node_firewall_config: an example NodeFirewallConfig
    :param example_node_resources_config: an example NodeResourcesConfig
    :return: an example ElkConfig object
    """
    return ElkConfig(container=example_node_container_config, resources=example_node_resources_config,
                     firewall_config=example_node_firewall_config,
                     elk_manager_log_file="null", elk_manager_log_dir="null", elk_manager_max_workers=5,
                     elastic_port=9200, kibana_port=5601, logstash_port=5044, time_step_len_seconds=15,
                     elk_manager_port=50045, version="0.0.1")


@pytest.fixture
def example_node_beats_config() -> NodeBeatsConfig:
    """
    Fixture that returns an example NodeBeatsConfig object

    :return: an example NodeBeatsConfig object
    """
    return NodeBeatsConfig(ip="123.456.78.99", log_files_paths=["null"], filebeat_modules=["null"],
                           metricbeat_modules=["null"], heartbeat_hosts_to_monitor=["null"],
                           kafka_input=False, start_filebeat_automatically=False,
                           start_packetbeat_automatically=False, start_metricbeat_automatically=False,
                           start_heartbeat_automatically=False)


@pytest.fixture
def example_beats_config(example_node_beats_config: NodeBeatsConfig) -> BeatsConfig:
    """
    Fixture that returns an example BeatsConfig object

    :param example_node_beats_config: an example NodeBeatsConfig
    :return: an example BeatsConfig object
    """
    return BeatsConfig(node_beats_configs=[example_node_beats_config], num_elastic_shards=3, reload_enabled=True)


@pytest.fixture
def example_flags_config(example_node_flags_config: NodeFlagsConfig) -> FlagsConfig:
    """
    Fixture that returns an example FlagsConfig object

    :param example_node_flags_config: an example NodeFlagsConfig
    :return: an example FlagsConfig object
    """
    return FlagsConfig(node_flag_configs=[example_node_flags_config])


@pytest.fixture
def example_emulation_env_config(
        example_container_network: ContainerNetwork, example_node_container_config: NodeContainerConfig,
        example_containers_config: ContainersConfig, example_node_users_config: NodeUsersConfig,
        example_users_config: UsersConfig, example_flags_config: FlagsConfig,
        example_credential: Credential, example_vulnerabilities_config: VulnerabilitiesConfig,
        example_topology_config: TopologyConfig,
        example_emulation_attacker_action: EmulationAttackerAction, example_kafka_config: KafkaConfig,
        example_traffic_config: TrafficConfig, example_services_config: ServicesConfig,
        example_resources_config: ResourcesConfig, example_sdn_controller_config: SDNControllerConfig,
        example_ovs_config: OVSConfig, example_elk_config: ElkConfig,
        example_host_manager_config: HostManagerConfig, example_snort_ids_manager_config: SnortIDSManagerConfig,
        example_ossec_ids_manager_config: OSSECIDSManagerConfig,
        example_docker_stats_manager_config: DockerStatsManagerConfig, example_beats_config: BeatsConfig) \
        -> EmulationEnvConfig:
    """
    Fixture that returns an example EmulationEnvConfig object

    :param example_container_network: an example ContainerNetwork
    :param example_node_container_config: an example NodeContainerConfig
    :param example_containers_config: an example ContainersConfig
    :param example_node_users_config: an example NodeUsersConfig
    :param example_users_config: an example UsersConfig
    :param example_flags_config: an example FlagsConfig
    :param example_credential: an example Credential
    :param example_vulnerabilities_config: an example VulnerabilitiesConfig
    :param example_topology_config: an example TopologyConfig
    :param example_resources_config: an example ResourcesConfig
    :param example_emulation_attacker_action: an example EmulationAttackerAction
    :param example_kafka_config: an example KafkaConfig
    :param example_traffic_config: an example TrafficConfig
    :param example_services_config: an example ServicesConfig
    :param example_sdn_controller_config: an example SDNControllerConfig
    :param example_ovs_config: an example OVSConfig
    :param example_elk_config: an example ElkConfig
    :param example_host_manager_config: an example HostManagerConfig
    :param example_snort_ids_manager_config: an example SnortIDSManagerConfig
    :param example_ossec_ids_manager_config: an example OSSECIDSManagerConfig
    :param example_docker_stats_manager_config: an example DockerStatsManagerConfig
    :param example_beats_config: an example BeatsConfig
    :return: example EmulationEnvConfig object
    """
    return EmulationEnvConfig(name="JDoeEmulation", containers_config=example_containers_config,
                              users_config=example_users_config,
                              flags_config=example_flags_config,
                              vuln_config=example_vulnerabilities_config,
                              topology_config=example_topology_config,
                              traffic_config=example_traffic_config, resources_config=example_resources_config,
                              kafka_config=example_kafka_config, services_config=example_services_config,
                              descr="null",
                              static_attacker_sequences={"E_A_action": [example_emulation_attacker_action]},
                              ovs_config=example_ovs_config,
                              sdn_controller_config=example_sdn_controller_config,
                              host_manager_config=example_host_manager_config,
                              snort_ids_manager_config=example_snort_ids_manager_config,
                              ossec_ids_manager_config=example_ossec_ids_manager_config,
                              docker_stats_manager_config=example_docker_stats_manager_config,
                              elk_config=example_elk_config,
                              beats_config=example_beats_config,
                              level=5, version="null", execution_id=10,
                              csle_collector_version=collector_constants.LATEST_VERSION,
                              csle_ryu_version=collector_constants.LATEST_VERSION)


@pytest.fixture
def example_emulation_execution(example_emulation_env_config: EmulationEnvConfig) -> EmulationExecution:
    """
    Fixture that returns an example EmulationExecution object

    :param example_emulation_env_config: fixture returning an example EmulationEnvConfig
    :return: an example EmulationExecution object
    """
    em_env = example_emulation_env_config
    em_ex = EmulationExecution(emulation_name="JohbnDoeEmulation", timestamp=1.5, ip_first_octet=-1,
                               emulation_env_config=em_env, physical_servers=["JohnDoeServer"])
    return em_ex


@pytest.fixture
def example_nikto_vuln() -> NiktoVuln:
    """
    Fixture that returns an example NiktoVuln object

    :return: an example NiktoVuln object
    """
    return NiktoVuln(id="testid", osvdb_id=15, method="test", iplink="test2", namelink="test3", uri="test4",
                     description="test5")


@pytest.fixture
def example_nikto_scan_result(example_nikto_vuln: NiktoVuln) -> NiktoScanResult:
    """
    Fixture that returns an example NiktoScanResult object

    :param example_nikto_vuln: an example NiktoVuln
    :return: an example NiktoScanResult object
    """
    return NiktoScanResult(port=3333, ip="192.168.1.1", sitename="test", vulnerabilities=[example_nikto_vuln])


@pytest.fixture
def example_nmap_brute_credentials() -> NmapBruteCredentials:
    """
    Fixture that returns an example NmapBruteCredentials object

    :return: an example NmapBruteCredentials object
    """
    return NmapBruteCredentials(
        username="testuser", pw="testpw", state="teststate", port=3333, protocol=TransportProtocol.TCP,
        service="testservice")


@pytest.fixture
def example_nmap_hop() -> NmapHop:
    """
    Fixture that returns an example NmapHop object

    :return: an example NmapHop object
    """
    return NmapHop(ttl=20, ipaddr="testip", rtt=0.0, host="testhost")


@pytest.fixture
def example_nmap_http_enum() -> NmapHttpEnum:
    """
    Fixture that returns an example NmapHttpEnum object

    :return: an example NmapHttpEnum object
    """
    return NmapHttpEnum(output="testout")


@pytest.fixture
def example_nmap_http_grep() -> NmapHttpGrep:
    """
    Fixture that returns an example NmapHttpEnum object

    :return: an example NmapHttpEnum object
    """
    return NmapHttpGrep(output="testout")


@pytest.fixture
def example_nmap_vulscan() -> NmapVulscan:
    """
    Fixture that returns an example NmapVulscan object

    :return: an example NmapVulscan object
    """
    return NmapVulscan(output="testout")


@pytest.fixture
def example_nmap_os() -> NmapOs:
    """
    Fixture that returns an example NmapOs object

    :return: an example NmapOs object
    """
    return NmapOs(name="testosName", vendor="osvendor", osfamily="osfam", accuracy=5)


@pytest.fixture
def example_nmap_port(example_nmap_http_grep: NmapHttpGrep, example_nmap_http_enum: NmapHttpEnum,
                      example_nmap_vulscan: NmapVulscan) -> NmapPort:
    """
    Fixture that returns an example NmapPort object

    :param example_nmap_http_grep: an example NmapHttpGrep
    :param example_nmap_http_enum: an example NmapHttpEnum
    :param example_nmap_vulscan: an example NmapVulscan
    :return: an example NmapPort object
    """
    return NmapPort(port_id=1, protocol=TransportProtocol.UDP, status=NmapPortStatus.UP,
                    service_version="testservice", http_enum=example_nmap_http_enum, http_grep=example_nmap_http_grep,
                    service_fp="test_fp", vulscan=example_nmap_vulscan, service_name="testervicename")


@pytest.fixture
def example_nmap_trace(example_nmap_hop: NmapHop) -> NmapTrace:
    """
    Fixture that returns an example NmapTrace object

    :param example_nmap_hop: an example NmapHop
    :return: an example NmapTrace object
    """
    return NmapTrace(hops=[example_nmap_hop])


@pytest.fixture
def example_nmap_vuln(example_credential: Credential) -> NmapVuln:
    """
    Fixture that returns an example NmapVuln object

    :param example_credential: an example Credential
    :return: an example NmapVuln object
    """
    return NmapVuln(name="vuln_name", port=4443, protocol=TransportProtocol.TCP, cvss=0.1,
                    service="testservice", credentials=[example_credential])


@pytest.fixture
def example_nmap_host_result(example_nmap_port: NmapPort, example_nmap_os: NmapOs,
                             example_nmap_vuln: NmapVuln,
                             example_nmap_brute_credentials: NmapBruteCredentials,
                             example_nmap_trace: NmapTrace) -> NmapHostResult:
    """
    Fixture that returns an example NmapHostResult object

    :param example_nmap_port: an example NmapPort
    :param example_nmap_os: an example NmapOs
    :param example_nmap_vuln: an example NmapVuln
    :param example_nmap_brute_credentials: an example NmapBruteCredentials
    :param example_nmap_trace: an example NmapTrace
    :return: an example NmapHostResult object
    """
    return NmapHostResult(
        status=NmapHostStatus.UP, ips=["172.151.51.2"], mac_addr="00-B0-D0-63-C2-26", hostnames=["testhost"],
        ports=[example_nmap_port], os=example_nmap_os, os_matches=[example_nmap_os],
        vulnerabilities=[example_nmap_vuln], credentials=[example_nmap_brute_credentials], trace=example_nmap_trace)


@pytest.fixture
def example_nmap_scan_result(example_nmap_host_result: NmapHostResult) -> NmapScanResult:
    """
    Fixture that returns an example NmapScanResult object

    :param example_nmap_host_result: an example NmapHostResult
    :return: an example NmapScanResult object
    """
    return NmapScanResult(hosts=[example_nmap_host_result], ips=["192.168.5.1"])


@pytest.fixture
def example_emulation_port_observation_state() -> EmulationPortObservationState:
    """
    Fixture that returns an example EmulationPortObservationState object

    :return: an example EmulationPortObservationState object
    """
    return EmulationPortObservationState(
        port=3333, open=False, service="myservice", protocol=TransportProtocol.TCP, http_enum="testenum",
        http_grep="testgrep", vulscan="vulscantest", version="myversion", fingerprint="myfp")


@pytest.fixture
def example_emulation_attacker_observation_state() -> EmulationAttackerObservationState:
    """
    Fixture that returns an example EmulationAttackerObservationState object

    :return: an example EmulationAttackerObservationState object
    """
    return EmulationAttackerObservationState(catched_flags=1, agent_reachable={"test1", "test2"})


@pytest.fixture
def example_emulation_vulnerability_observation_state(example_credential: Credential) \
        -> EmulationVulnerabilityObservationState:
    """
    Fixture that returns an example EmulationVulnerabilityObservationState object

    :param example_credential: an example Credential
    :return: an example EmulationVulnerabilityObservationState object
    """
    return EmulationVulnerabilityObservationState(
        name="test", port=123, protocol=TransportProtocol.TCP, cvss=0.1, credentials=[])


@pytest.fixture
def example_emulation_defender_machine_observation_state(example_kafka_config: KafkaConfig) \
        -> EmulationDefenderMachineObservationState:
    """
    Fixture that returns an example EmulationDefenderMachineObservationState object

    :param example_kafka_config: an example KafkaConfig
    :return: an example EmulationDefenderMachineObservationState object
    """
    ips = ["10.10.10.10", "20.20.20.20"]
    return EmulationDefenderMachineObservationState(
        ips=ips, kafka_config=example_kafka_config, host_metrics=HostMetrics(), docker_stats=DockerStats(),
        snort_ids_ip_alert_counters=SnortIdsIPAlertCounters(), ossec_ids_alert_counters=OSSECIdsAlertCounters())


@pytest.fixture
def example_emulation_defender_observation_state(
        example_kafka_config: KafkaConfig, example_emulation_attacker_action: EmulationAttackerAction,
        example_emulation_defender_action: EmulationDefenderAction) \
        -> EmulationDefenderObservationState:
    """
    Fixture that returns an example EmulationDefenderObservationState object

    :param example_kafka_config: an example KafkaConfig
    :param example_emulation_defender_action: an example EmulationDefenderAction
    :param example_emulation_attacker_action: an example EmulationAttackerAction
    :return: an example EmulationDefenderObservationState object
    """
    return EmulationDefenderObservationState(
        kafka_config=example_kafka_config, client_population_metrics=ClientPopulationMetrics(),
        docker_stats=DockerStats(),
        snort_ids_alert_counters=SnortIdsAlertCounters(), ossec_ids_alert_counters=OSSECIdsAlertCounters(),
        aggregated_host_metrics=HostMetrics(), defender_actions=[example_emulation_defender_action],
        attacker_actions=[example_emulation_attacker_action],
        snort_ids_rule_counters=SnortIdsRuleCounters())


@pytest.fixture
def example_emulation_attacker_machine_observation_state() -> EmulationAttackerMachineObservationState:
    """
    Fixture that returns an example EmulationAttackerMachineObservationState object

    :return: an example EmulationAttackerMachineObservationState object
    """
    return EmulationAttackerMachineObservationState(ips=["172.31.212.1", "172.31.212.2"])


@pytest.fixture
def example_hparam() -> HParam:
    """
    Fixture that returns an example HParam object

    :return: an example HParam object
    """
    return HParam(value=1, name="test", descr="test")


@pytest.fixture
def example_system_identification_config(example_hparam: HParam) -> SystemIdentificationConfig:
    """
    Fixture that returns an example SystemIdentificationConfig object

    :param example_hparam: an example HParam
    :return: an example SystemIdentificationConfig object
    """
    hparams = dict()
    hparams["test"] = example_hparam
    return SystemIdentificationConfig(
        model_type=SystemModelType.GAUSSIAN_MIXTURE, hparams=hparams,
        output_dir="test/test", title="test", log_every=10)


@pytest.fixture
def example_experiment_config(example_hparam: HParam) -> ExperimentConfig:
    """
    Fixture that returns an example ExperimentConfig object

    :param example_hparam: an example HParam
    :return: an example ExperimentConfig object
    """
    hparams = dict()
    hparams["test"] = example_hparam
    return ExperimentConfig(output_dir="test/test", title="test1", random_seeds=[1],
                            agent_type=AgentType.PPO, hparams=hparams, log_every=10,
                            player_type=PlayerType.DEFENDER, player_idx=2)


@pytest.fixture
def example_experiment_result() -> ExperimentResult:
    """
    Fixture that returns an example ExperimentConfig object

    :return: an example ExperimentConfig object
    """
    return ExperimentResult()


@pytest.fixture
def example_simulation_trace() -> SimulationTrace:
    """
    Fixture that returns an example SimulationTrace object

    :return: an example SimulationTrace object
    """
    return SimulationTrace(simulation_env="test1")


@pytest.fixture
def example_training_job_config(example_experiment_config: ExperimentConfig,
                                example_experiment_result: ExperimentResult,
                                example_simulation_trace: SimulationTrace) -> TrainingJobConfig:
    """
    Fixture that returns an example TrainingJobConfig object

    :param example_experiment_config: an example ExperimentConfig
    :param example_experiment_result: an example ExperimentResult
    :param example_simulation_trace: an example SimulationTrace
    :return: an example TrainingJobConfig object
    """
    return TrainingJobConfig(simulation_env_name="test", progress_percentage=0.5,
                             pid=1, emulation_env_name="test", num_cached_traces=1,
                             log_file_path="test/test", descr="test", physical_host_ip="1.1.1.1",
                             experiment_config=example_experiment_config,
                             experiment_result=example_experiment_result,
                             simulation_traces=[example_simulation_trace])


@pytest.fixture
def example_system_identification_job_config(
        example_system_identification_config: SystemIdentificationConfig) -> SystemIdentificationJobConfig:
    """
    Fixture that returns an example SystemIdentificationConfig object

    :param example_system_identification_config: an example SystemIdentificationConfig
    :return: an example SystemIdentificationJobConfig object
    """
    return SystemIdentificationJobConfig(emulation_env_name="test", emulation_statistics_id=1, pid=123,
                                         log_file_path="test/test",
                                         system_identification_config=example_system_identification_config,
                                         physical_host_ip="1.1.1.1", progress_percentage=0.5)


@pytest.fixture
def example_emulation_trace(
        example_emulation_defender_observation_state: EmulationDefenderObservationState) -> EmulationTrace:
    """
    Fixture that returns an example EmulationTrace object

    :param example_emulation_defender_observation_state: an example EmulationDefenderObservationState
    :return: an example EmulationTrace object
    """
    return EmulationTrace(initial_attacker_observation_state=EmulationAttackerObservationState(
        catched_flags=1, agent_reachable={"yes"}),
        initial_defender_observation_state=example_emulation_defender_observation_state,
        emulation_name="test")


@pytest.fixture
def example_data_collection_job(
        example_emulation_attacker_action: EmulationAttackerAction,
        example_emulation_defender_action: EmulationDefenderAction, example_emulation_trace: EmulationTrace) \
        -> DataCollectionJobConfig:
    """
    Fixture that returns an example EmulationAttackerObservationState object

    :param example_emulation_attacker_action: an example EmulationAttackerAction
    :param example_emulation_defender_action: an example EmulationDefenderAction
    :param example_emulation_trace: an example EmulationTrace
    :return: an example EmulationAttackerObservationState object
    """
    return DataCollectionJobConfig(emulation_env_name="test", num_collected_steps=1,
                                   progress_percentage=0.1,
                                   attacker_sequence=[example_emulation_attacker_action],
                                   pid=123, repeat_times=5, emulation_statistic_id=10,
                                   num_sequences_completed=10, traces=[example_emulation_trace],
                                   save_emulation_traces_every=1, num_cached_traces=10,
                                   defender_sequence=[example_emulation_defender_action],
                                   log_file_path="test/test", physical_host_ip="1.1.1.1")


@pytest.fixture
def example_management_user() -> ManagementUser:
    """
    Fixture that returns an example ManagementUser object

    :return: an example ManagementUser object
    """
    return ManagementUser(username="test1", password="test2", email="test@test.test", first_name="test3",
                          last_name="test4", organization="testi", admin=False, salt="test")


@pytest.fixture
def example_session_token() -> SessionToken:
    """
    Fixture that returns an example SessionToken object

    :return: an example SessionToken object
    """
    return SessionToken(token="test_token", timestamp=11.11, username="test")


@pytest.fixture
def example_action() -> Action:
    """
    Fixture that returns an example Action object

    :return: an example Action object
    """
    return Action(id=1, descr="test")


@pytest.fixture
def example_action_space_config(example_action: Action) -> ActionSpaceConfig:
    """
    Fixture that returns an example ActionSpaceConfig object

    :param example_action: an example Action
    :return: an example ActionSpaceConfig object
    """
    return ActionSpaceConfig(actions=[example_action], player_id=1, action_type=ValueType.INTEGER)


@pytest.fixture
def example_agent_log() -> AgentLog:
    """
    Fixture that returns an example AgentLog object

    :return: an example AgentLog object
    """
    return AgentLog()


@pytest.fixture
def example_env_parameter() -> EnvParameter:
    """
    Fixture that returns an example EnvParameter object

    :return: an example EnvParameter object
    """
    return EnvParameter(id=1, name="test", descr="test1")


@pytest.fixture
def example_env_parameters_config(example_env_parameter: EnvParameter) -> EnvParametersConfig:
    """
    Fixture that returns an example EnvParametersConfig object

    :param example_env_parameter: an example EnvParameter
    :return: an example EnvParametersConfig object
    """
    return EnvParametersConfig(parameters=[example_env_parameter])


@pytest.fixture
def example_initial_state_distribution_config() -> InitialStateDistributionConfig:
    """
    Fixture that returns an example InitialStateDistributionConfig object

    :return: an example InitialStateDistributionConfig object
    """
    return InitialStateDistributionConfig(initial_state_distribution=[0.1, 0.9])


@pytest.fixture
def example_joint_action_space_config(example_action_space_config: ActionSpaceConfig) -> JointActionSpaceConfig:
    """
    Fixture that returns an example JointActionSpaceConfig object

    :param example_action_space_config: an example ActionSpaceConfig
    :return: an example JointActionSpaceConfig object
    """
    return JointActionSpaceConfig(
        action_spaces=[ActionSpaceConfig(actions=[Action(id=1, descr="test")], player_id=1,
                                         action_type=ValueType.INTEGER)])


@pytest.fixture
def example_observation() -> Observation:
    """
    Fixture that returns an example Observation object

    :return: an example Observation object
    """
    return Observation(id=1, val=2, descr="test")


@pytest.fixture
def example_observation_space_config(example_observation: Observation) -> ObservationSpaceConfig:
    """
    Fixture that returns an example ObservationSpaceConfig object

    :param example_observation: an example Observation
    :return: an example ObservationSpaceConfig object
    """
    observation = Observation(id=1, val=2, descr="test")
    observation_component_name_to_index = dict()
    observation_component_name_to_index["test"] = 1
    observation_id_to_observation_id_vector = dict()
    observation_id_to_observation_id_vector[0] = [1, 2, 3]
    observation_id_to_observation_vector = dict()
    observation_id_to_observation_vector[4] = [4, 5, 6]
    component_observations = dict()
    component_observations["test1"] = [observation]
    return ObservationSpaceConfig(
        observations=[example_observation], observation_type=ValueType.INTEGER, descr="test", player_id=2,
        observation_component_name_to_index=observation_component_name_to_index,
        observation_id_to_observation_id_vector=observation_id_to_observation_id_vector,
        observation_id_to_observation_vector=observation_id_to_observation_vector,
        component_observations=component_observations)


@pytest.fixture
def example_joint_observation_space_config(example_observation_space_config: ObservationSpaceConfig) \
        -> JointObservationSpaceConfig:
    """
    Fixture that returns an example JointObservationSpaceConfig object

    :param example_observation_space_config: an example ObservationSpaceConfig
    :return: an example ObservationSpaceConfig object
    """
    return JointObservationSpaceConfig(observation_spaces=[example_observation_space_config])


@pytest.fixture
def example_observation_function_config() -> ObservationFunctionConfig:
    """
    Fixture that returns an example ObservationFunctionConfig object

    :return: an example ObservationFunctionConfig object
    """
    observation_tensor = np.array([1, 2, 3])
    component_observation_tensors = dict()
    component_observation_tensors["test"] = np.array([1, 2, 3])
    return ObservationFunctionConfig(observation_tensor=observation_tensor,
                                     component_observation_tensors=component_observation_tensors)


@pytest.fixture
def example_player_config() -> PlayerConfig:
    """
    Fixture that returns an example PlayerConfig object

    :return: an example PlayerConfig object
    """
    return PlayerConfig(name="test", id=2)


@pytest.fixture
def example_players_config(example_player_config: PlayerConfig) -> PlayersConfig:
    """
    Fixture that returns an example PlayerConfig object

    :param example_player_config: an example PlayerConfig
    :return: an example PlayerConfig object
    """
    return PlayersConfig(player_configs=[example_player_config])


@pytest.fixture
def example_reward_function_config() -> RewardFunctionConfig:
    """
    Fixture that returns an example RewardFunctionConfig object

    :return: an example RewardFunctionConfig object
    """
    return RewardFunctionConfig(reward_tensor=np.array([1, 3, 7]))


@pytest.fixture
def example_input_config() -> ExampleInputConfig:
    """
    Fixture that returns an example ExampleInputConfig object

    :return: an example ExampleInputConfig object
    """
    return ExampleInputConfig(x=5)


@pytest.fixture
def example_state() -> State:
    """
    Fixture that returns an example State object

    :return: an example State object
    """
    return State(id=1, name="test", descr="test1", state_type=StateType.TERMINAL)


@pytest.fixture
def example_state_space_config(example_state: State) -> StateSpaceConfig:
    """
    Fixture that returns an example StateSpaceConfig object

    :param example_state: an example State
    :return: an example StateSpaceConfig object
    """
    return StateSpaceConfig(states=[State(id=1, name="test", descr="test1",
                                          state_type=StateType.TERMINAL)])


@pytest.fixture
def example_transition_operator_config() -> TransitionOperatorConfig:
    """
    Fixture that returns an example TransitionOperatorConfig object

    :return: an example TransitionOperatorConfig object
    """
    return TransitionOperatorConfig(transition_tensor=np.array([1, 2, 3]))


@pytest.fixture
def example_simulation_env_config(
        example_player_config: PlayerConfig, example_input_config: ExampleInputConfig,
        example_joint_action_space_config: JointActionSpaceConfig,
        example_joint_observation_space_config: JointObservationSpaceConfig,
        example_reward_function_config: RewardFunctionConfig,
        example_transition_operator_config: TransitionOperatorConfig,
        example_observation_function_config: ObservationFunctionConfig,
        example_initial_state_distribution_config: InitialStateDistributionConfig,
        example_env_parameters_config: EnvParametersConfig) -> SimulationEnvConfig:
    """
    Fixture that returns an example SimulationEnvConfig object

    :param example_player_config: an example PlayerConfig
    :param example_input_config: an example ExampleInputConfig
    :param example_joint_action_space_config: an example JointActionSpaceConfig
    :param example_joint_observation_space_config: an example JointObservationSpaceConfig
    :param example_reward_function_config: an example RewardFunctionConfig
    :param example_transition_operator_config: an example TransitionOperatorConfig
    :param example_observation_function_config: an example ObservationFunctionConfig
    :param example_initial_state_distribution_config: an example InitialStateDistributionConfig
    :param example_env_parameters_config: an example EnvParametersConfig
    :return: an example SimulationEnvConfig object
    """
    return SimulationEnvConfig(
        name="test", descr="test1", version="1.0", gym_env_name="gym_test",
        simulation_env_input_config=example_input_config,
        players_config=PlayersConfig(player_configs=[PlayerConfig(name="test", id=4)]),
        state_space_config=StateSpaceConfig(
            states=[State(id=1, name="test", descr="test1", state_type=StateType.ACTIVE)]),
        joint_action_space_config=example_joint_action_space_config,
        joint_observation_space_config=example_joint_observation_space_config, time_step_type=TimeStepType.CONTINUOUS,
        reward_function_config=example_reward_function_config,
        transition_operator_config=example_transition_operator_config,
        observation_function_config=example_observation_function_config,
        initial_state_distribution_config=example_initial_state_distribution_config,
        env_parameters_config=example_env_parameters_config)


@pytest.fixture
def example_empirical_conditional() -> EmpiricalConditional:
    """
    Fixture that returns an example EmpiricalConditional object

    :return: an example EmpiricalConditional object
    """
    return EmpiricalConditional(conditional_name="test", metric_name="test2", sample_space=[1, 2, 3],
                                probabilities=[0.2, 0.8])


@pytest.fixture
def example_empirical_system_model(example_empirical_conditional: EmpiricalConditional) -> EmpiricalSystemModel:
    """
    Fixture that returns an example EmpiricalSystemModel object

    :param example_empirical_conditional: an example EmpiricalConditional
    :return: an example EmpiricalSystemModel object
    """
    return EmpiricalSystemModel(emulation_env_name="test", emulation_statistic_id=1,
                                conditional_metric_distributions=[[example_empirical_conditional]], descr="test1")


@pytest.fixture
def example_emulation_statistics() -> EmulationStatistics:
    """
    Fixture that returns an example EmulationStatistics object

    :return: an example EmulationStatistics object
    """
    return EmulationStatistics(emulation_name="test")


@pytest.fixture
def example_gaussian_mixture_conditional() -> GaussianMixtureConditional:
    """
    Fixture that returns an example GaussianMixtureConditional object

    :return: an example GaussianMixtureConditional object
    """
    return GaussianMixtureConditional(
        conditional_name="test", metric_name="test1", num_mixture_components=2, dim=2,
        mixtures_means=[[0.4], [0.7]], mixtures_covariance_matrix=[[[0.5]]], mixture_weights=[0.6, 0.3],
        sample_space=[2, 5])


@pytest.fixture
def example_gaussian_mixture_system_model(
        example_gaussian_mixture_conditional: GaussianMixtureConditional) -> GaussianMixtureSystemModel:
    """
    Fixture that returns an example GaussianMixtureSystemModel object

    :param example_gp_conditional: an example GPConditional
    :return: an example GaussianMixtureSystemModel object
    """
    return GaussianMixtureSystemModel(
        emulation_env_name="test", emulation_statistic_id=2,
        conditional_metric_distributions=[[example_gaussian_mixture_conditional]], descr="test3")


@pytest.fixture
def example_gp_conditional() -> GPConditional:
    """
    Fixture that returns an example GPConditional object

    :return: an example GPConditional object
    """
    return GPConditional(
        conditional_name="test", metric_name="test1", sample_space=[1, 2, 3], observed_x=[1, 2],
        observed_y=[1.5, 3.4], scale_parameter=5.5, noise_parameter=3.2)


@pytest.fixture
def example_gp_system_model(example_gp_conditional: GPConditional) -> GPSystemModel:
    """
    Fixture that returns an example GPSystemModel object

    :param example_gp_conditional: an example GPConditional
    :return: an example GPSystemModel object
    """
    return GPSystemModel(emulation_env_name="test", emulation_statistic_id=1,
                         conditional_metric_distributions=[[example_gp_conditional]], descr="test")


@pytest.fixture
def example_mcmc_posterior() -> MCMCPosterior:
    """
    Fixture that returns an example MCMCPosterior object

    :return: an example MCMCPosterior object
    """
    return MCMCPosterior(posterior_name="test", samples=[1.5], densities=[4.5], sample_space=[3.5])


@pytest.fixture
def example_mcmc_system_model(example_mcmc_posterior: MCMCPosterior) -> MCMCSystemModel:
    """
    Fixture that returns an example MCMCSystemModel object

    :param example_mcmc_posterior: an example MCMCPosterior
    :return: an example MCMCSystemModel object
    """
    return MCMCSystemModel(emulation_env_name="test", emulation_statistic_id=0,
                           posteriors=[example_mcmc_posterior], descr="test1")


@pytest.fixture
def example_alpha_vectors_policy(example_state: State, example_action: Action) -> AlphaVectorsPolicy:
    """
    Fixture that returns an example AlphaVectorsPolicy object

    :param example_state: an example State
    :param example_action: an example Action
    :return: an example AlphaVectorsPolicy object
    """
    return AlphaVectorsPolicy(
        player_type=PlayerType.DEFENDER, actions=[example_action], alpha_vectors=[1, 2], transition_tensor=[1, 3],
        reward_tensor=[5, 6], states=[example_state], agent_type=AgentType.PPO, simulation_name="test", avg_R=0.3)


@pytest.fixture
def example_dqn_policy(example_state: State, example_action: Action,
                       example_experiment_config: ExperimentConfig) -> DQNPolicy:
    """
    Fixture that returns an example DQNPolicy object

    :param example_state: an example State
    :param example_action: an example Action
    :param example_experiment_config: an example ExperimentConfig
    :return: an example DQNPolicy object
    """
    return DQNPolicy(model=None, simulation_name="test", save_path="test/test",
                     player_type=PlayerType.ATTACKER, states=[example_state], actions=[example_action], avg_R=0.6,
                     experiment_config=example_experiment_config)


@pytest.fixture
def example_experiment_execution(
        example_experiment_config: ExperimentConfig, example_experiment_result: ExperimentResult) \
        -> ExperimentExecution:
    """
    Fixture that returns an example ExperimentExecution object

    :param example_experiment_config: an example ExperimentConfig
    :param example_experiment_result: an example ExperimentResult
    :return: an example ExperimentExecution object
    """
    return ExperimentExecution(
        config=example_experiment_config, result=example_experiment_result, timestamp=10.10, emulation_name="test",
        simulation_name="test1", descr="test2", log_file_path="test/test")


@pytest.fixture
def example_fnn_with_softmax_policy(example_state: State, example_action: Action,
                                    example_experiment_config: ExperimentConfig) -> FNNWithSoftmaxPolicy:
    """
    Fixture that returns an example FNNWithSoftmaxPolicy object

    :param example_state: an example State
    :param example_action: an example Action
    :param example_experiment_config: an example ExperimentConfig
    :return: an example FNNWithSoftmaxPolicy object
    """
    return FNNWithSoftmaxPolicy(
        None, simulation_name="test", save_path="test/test", player_type=PlayerType.DEFENDER,
        states=[example_state], actions=[example_action], experiment_config=example_experiment_config, avg_R=0.1,
        input_dim=100,
        output_dim=10)


@pytest.fixture
def example_tabular_policy(example_action: Action) -> TabularPolicy:
    """
    Fixture that returns an example TabularPolicy object

    :param example_action: an example Actionp
    :return: an example TabularPolicy object
    """
    return TabularPolicy(player_type=PlayerType.DEFENDER, actions=[example_action], lookup_table=[[1.4]],
                         simulation_name="test", avg_R=8.1, agent_type=AgentType.SONDIK_VALUE_ITERATION)


@pytest.fixture
def example_linear_threshold_stopping_policy(
        example_state: State, example_action: Action, example_experiment_config: ExperimentConfig) \
        -> LinearThresholdStoppingPolicy:
    """
    Fixture that returns an example LinearThresholdStoppingPolicy object

    :param example_state: an example State
    :param example_action: an example Action
    :param example_experiment_config: an example ExperimentConfig
    :return: an example LinearThresholdStoppingPolicy object
    """
    return LinearThresholdStoppingPolicy(
        [0.1], simulation_name="test", L=1, states=[example_state], player_type=PlayerType.SELF_PLAY,
        actions=[example_action], experiment_config=example_experiment_config, avg_R=0.2, agent_type=AgentType.RANDOM)


@pytest.fixture
def example_linear_tabular_policy(
        example_state: State, example_action: Action, example_experiment_config: ExperimentConfig,
        example_tabular_policy: TabularPolicy,
        example_linear_threshold_stopping_policy: LinearThresholdStoppingPolicy) \
        -> LinearTabularPolicy:
    """
    Fixture that returns an example LinearTabularPolicy object

    :param example_state: an example State
    :param example_action: an example Action
    :param example_experiment_config: an example ExperimentConfig
    :return: an example LinearTabularPolicy object
    """
    return LinearTabularPolicy(
        stopping_policy=example_linear_threshold_stopping_policy, action_policy=example_tabular_policy,
        player_type=PlayerType.DEFENDER,
        actions=[example_action], avg_R=0.1, agent_type=AgentType.T_SPSA,
        states=[example_state], simulation_name="test2", experiment_config=example_experiment_config)


@pytest.fixture
def example_mixed_linear_tabular(
        example_state: State, example_action: Action, example_experiment_config: ExperimentConfig) \
        -> MixedLinearTabularPolicy:
    """
    Fixture that returns an example MixedLinearTabularPolicy object

    :param example_state: an example State
    :param example_action: an example Action
    :param example_experiment_config: an example ExperimentConfig
    :return: an example MixedLinearTabularPolicy object
    """
    return MixedLinearTabularPolicy(
        simulation_name="test", player_type=PlayerType.DEFENDER, states=[example_state],
        actions=[example_action], experiment_config=example_experiment_config, avg_R=0.9)


@pytest.fixture
def example_mixed_multi_threshold_stopping_policy(
        example_state: State, example_action: Action, example_experiment_config: ExperimentConfig) \
        -> MixedMultiThresholdStoppingPolicy:
    """
    Fixture that returns an example MixedMultiThresholdStoppingPolicy object

    :param example_state: an example State
    :param example_action: an example Action
    :param example_experiment_config: an example ExperimentConfig
    :return: an example MixedMultiThresholdStoppingPolicy object
    """
    defender_Theta = [[[0.2, 0.8]]]
    attacker_Theta = [[[[0.2, 0.8]]]]
    return MixedMultiThresholdStoppingPolicy(
        defender_Theta=defender_Theta, attacker_Theta=attacker_Theta,
        simulation_name="test", L=2, player_type=PlayerType.DEFENDER, states=[example_state],
        actions=[example_action], experiment_config=example_experiment_config, avg_R=0.9,
        agent_type=AgentType.T_SPSA, opponent_strategy=None)


@pytest.fixture
def example_mixed_ppo_policy(
        example_state: State, example_action: Action, example_experiment_config: ExperimentConfig) \
        -> MixedPPOPolicy:
    """
    Fixture that returns an example MixedPPOPolicy object

    :param example_state: an example State
    :param example_action: an example Action
    :param example_experiment_config: an example ExperimentConfig
    :return: an example MixedPPOPolicy object
    """
    return MixedPPOPolicy(simulation_name="test", player_type=PlayerType.DEFENDER, states=[example_state],
                          actions=[example_action], experiment_config=example_experiment_config, avg_R=0.8)


@pytest.fixture
def example_multi_threshold_stopping_policy(
        example_state: State, example_action: Action, example_experiment_config: ExperimentConfig) \
        -> MultiThresholdStoppingPolicy:
    """
    Fixture that returns an example MultiThresholdStoppingPolicy object

    :param example_state: an example State
    :param example_action: an example Action
    :param example_experiment_config: an example ExperimentConfig
    :return: an example MultiThresholdStoppingPolicy object
    """
    theta = [0.2, 0.8]
    return MultiThresholdStoppingPolicy(
        theta=theta, simulation_name="test", L=2, player_type=PlayerType.DEFENDER, states=[example_state],
        actions=[example_action], experiment_config=example_experiment_config, avg_R=0.9, agent_type=AgentType.T_SPSA,
        opponent_strategy=None)


@pytest.fixture
def example_ppo_policy(
        example_state: State, example_action: Action, example_experiment_config: ExperimentConfig) \
        -> PPOPolicy:
    """
    Fixture that returns an example PPOPolicy object

    :param example_state: an example State
    :param example_action: an example Action
    :param example_experiment_config: an example ExperimentConfig
    :return: an example PPOPolicy object
    """
    return PPOPolicy(
        model=None, simulation_name="test", save_path="test/test", player_type=PlayerType.DEFENDER,
        states=[example_state],
        actions=[example_action], experiment_config=example_experiment_config, avg_R=10)


@pytest.fixture
def example_random_policy(example_action: Action) -> RandomPolicy:
    """
    Fixture that returns an example RandomPolicy object

    :param example_state: an example State
    :param example_action: an example Action
    :param example_experiment_config: an example ExperimentConfig
    :return: an example RandomPolicy object
    """
    return RandomPolicy(player_type=PlayerType.DEFENDER, actions=[example_action], stage_policy_tensor=None)


@pytest.fixture
def example_vector_policy() -> VectorPolicy:
    """
    Fixture that returns an example VectorPolicy object

    :return: an example VectorPolicy object
    """
    return VectorPolicy(player_type=PlayerType.DEFENDER, actions=[1, 3], policy_vector=[2.3],
                        agent_type=AgentType.LINEAR_PROGRAMMING_NORMAL_FORM, simulation_name="test",
                        avg_R=0.4)
