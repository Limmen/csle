import json
import logging
from typing import List

import csle_common.constants.constants as constants
import pytest
from csle_cluster.cluster_manager.cluster_manager_pb2 import OperationOutcomeDTO
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import (
    EmulationAttackerAction,
)
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import (
    EmulationAttackerActionId,
)
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_outcome import (
    EmulationAttackerActionOutcome,
)
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import (
    EmulationAttackerActionType,
)
from csle_common.dao.emulation_action.defender.emulation_defender_action import (
    EmulationDefenderAction,
)
from csle_common.dao.emulation_action.defender.emulation_defender_action_id import (
    EmulationDefenderActionId,
)
from csle_common.dao.emulation_action.defender.emulation_defender_action_outcome import (
    EmulationDefenderActionOutcome,
)
from csle_common.dao.emulation_action.defender.emulation_defender_action_type import (
    EmulationDefenderActionType,
)
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.dao.emulation_config.default_network_firewall_config import (
    DefaultNetworkFirewallConfig,
)
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace
from csle_common.dao.emulation_config.kafka_config import KafkaConfig
from csle_common.dao.emulation_config.kafka_topic import KafkaTopic
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.dao.emulation_config.node_firewall_config import NodeFirewallConfig
from csle_common.dao.emulation_config.node_network_config import NodeNetworkConfig
from csle_common.dao.emulation_config.node_resources_config import NodeResourcesConfig
from csle_common.dao.emulation_config.packet_delay_distribution_type import (
    PacketDelayDistributionType,
)
from csle_common.dao.emulation_config.packet_loss_type import PacketLossType
from csle_common.dao.emulation_observation.attacker.emulation_attacker_observation_state import (
    EmulationAttackerObservationState,
)
from csle_common.dao.emulation_observation.defender.emulation_defender_observation_state import (
    EmulationDefenderObservationState,
)
from csle_common.dao.jobs.data_collection_job_config import DataCollectionJobConfig

import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesDataCollectionSuite:
    """
    Test suite for /data-collection-jobs resource
    """

    pytest.logger = logging.getLogger("resources_training_jobs_tests")

    @pytest.fixture
    def flask_app(self):
        """
        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def pid_true(self, mocker):
        """
        Pytest fixture for mocking the check_pid function
        :param mocker: The pytest mocker object
        :return: A mocker object with the mocked function
        """
        def check_pid(ip, port, pid) -> OperationOutcomeDTO:
            op_outcome = OperationOutcomeDTO(outcome=True)
            return op_outcome
        check_pid_mocker = mocker.MagicMock(side_effect=check_pid)

        return check_pid_mocker

    @pytest.fixture
    def pid_false(self, mocker):
        """
        Pytest fixture for mocking the check_pid function
        :param mocker: The pytest mocker object
        :return: A mocker object with the mocked function
        """
        def check_pid(ip, port, pid) -> OperationOutcomeDTO:
            op_outcome = OperationOutcomeDTO(outcome=False)
            return op_outcome
        check_pid_mocker = mocker.MagicMock(side_effect=check_pid)

        return check_pid_mocker

    @pytest.fixture
    def list_jobs(self, mocker):
        """
        Pytest fixture for mocking the list_data_collection_jobs function

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """
        def list_data_collection_jobs() -> List[DataCollectionJobConfig]:
            dc_job = TestResourcesDataCollectionSuite.get_example_job()
            return [dc_job]
        list_data_collection_jobs_mocker = mocker.MagicMock(side_effect=list_data_collection_jobs)
        return list_data_collection_jobs_mocker

    @pytest.fixture
    def remove(self, mocker):
        """
        Pytest fixture for mocking the remove_data_collection_job function

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """
        def remove_data_collection_job(data_collection_job: DataCollectionJobConfig) -> None:
            return None
        remove_data_collection_job_mocker = mocker.MagicMock(side_effect=remove_data_collection_job)
        return remove_data_collection_job_mocker

    @pytest.fixture
    def stop(self, mocker):
        """
        Pytest fixture mocking the stop_pid functio

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function

        """
        def stop_pid(ip, port, pid):
            return None
        stop_pid_mocker = mocker.MagicMock(side_effect=stop_pid)
        return stop_pid_mocker

    @pytest.fixture
    def start(self, mocker):
        """
        Pytest fixture for the start_training_job_in_background function

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """
        def start_training_job_in_background(training_job):
            return None
        start_training_job_in_background_mocker = mocker.MagicMock(
            side_effect=start_training_job_in_background)
        return start_training_job_in_background_mocker

    @pytest.fixture
    def get_job_config(self, mocker) -> DataCollectionJobConfig:
        """
        Pytest fixture for mocking the get_data_collection_job_config function

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """
        def get_data_collection_job_config(id: int) -> DataCollectionJobConfig:
            policy = TestResourcesDataCollectionSuite.get_example_job()
            return policy
        get_data_collection_job_config_mocker = mocker.MagicMock(side_effect=get_data_collection_job_config)
        return get_data_collection_job_config_mocker

    @staticmethod
    def get_example_job() -> DataCollectionJobConfig:
        """
        Utility function for getting an example instance of a PPOPolicy

        :return: an example isntance of a PPOPOlicy
        """
        nn_config = NodeNetworkConfig(packet_delay_distribution=PacketDelayDistributionType.PARETO.value,
                                      packet_loss_type=PacketLossType.GEMODEL.value)
        nc_config = NodeContainerConfig(name="JohnDoe",
                                        ips_and_networks=[("JDoe", ContainerNetwork(name="JohnDoe",
                                                                                    subnet_mask="JDoeMask",
                                                                                    bitmask="BitMask",
                                                                                    subnet_prefix="SubPrefix",
                                                                                    interface="eth0"))],
                                        version="version", level="level", restart_policy="restart_policy",
                                        suffix="suffix", os="os", execution_ip_first_octet=-1, docker_gw_bridge_ip="",
                                        physical_host_ip="123.456.78.99"),
        nr_config = NodeResourcesConfig(container_name="JDoeComntainer", num_cpus=5,
                                        available_memory_gb=5,
                                        ips_and_network_configs=[("123.456.78.99", nn_config)],
                                        docker_gw_bridge_ip="", physical_host_ip="123.456.78.99")
        nf_cofig = NodeFirewallConfig(
            ips_gw_default_policy_networks=[DefaultNetworkFirewallConfig(ip="123.456.78.99",
                                                                         default_gw="gateway",
                                                                         default_input="input",
                                                                         default_output="output",
                                                                         default_forward="forward",
                                                                         network=ContainerNetwork(name="JohnDoe",
                                                                                                  subnet_mask="JDoeMask",
                                                                                                  bitmask="BitMask",
                                                                                                  subnet_prefix="SubPrefix",
                                                                                                  interface="eth0")
                                                                         )],
            hostname="JohnDoe", output_accept={"out_accept"},
            input_accept={"in_accept"}, forward_accept={"forward_accept"},
            output_drop={"out_drop"}, input_drop={"in_drop"},
            forward_drop={"fwd_drop"}, routes={("routes", "routes")},
            docker_gw_bridge_ip="123.456.78.99", physical_host_ip="123.456.78.99")

        k_config = KafkaConfig(container=nc_config[0], resources=nr_config,
                               firewall_config=nf_cofig,
                               topics=[KafkaTopic(name="JohnDoe", num_partitions=5, num_replicas=5,
                                                  attributes=["attributes"], retention_time_hours=10)],
                               kafka_manager_log_file="log_file", kafka_manager_log_dir="log_dir",
                               kafka_manager_max_workers=5, kafka_port=9092, kafka_port_external=9292,
                               time_step_len_seconds=15, kafka_manager_port=50051, version="0.0.1")
        e_a_action = EmulationAttackerAction(id=EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST.value, name="JohnDoe",
                                             cmds=["JohnDoeCommands"], type=EmulationAttackerActionType.RECON.value,
                                             descr="null", ips=["JohnDoeIPs"], index=10,
                                             action_outcome=EmulationAttackerActionOutcome.INFORMATION_GATHERING.value,
                                             vulnerability="Vulnerability", alt_cmds=["JDoeCommands"],
                                             backdoor=False, execution_time=0.1, ts=1.1)
        e_d_action = EmulationDefenderAction(id=EmulationDefenderActionId.STOP.value, name="JohnDoe",
                                             cmds=["JohnDoeCommands"], type=EmulationDefenderActionType.STOP.value,
                                             descr="null", ips=["JohnDoeIPs"], index=10,
                                             action_outcome=EmulationDefenderActionOutcome.GAME_END.value,
                                             alt_cmds=["JDoeCommands"], execution_time=0.1, ts=1.1)
        e_d_o_state = EmulationDefenderObservationState(kafka_config=k_config,
                                                        client_population_metrics=None, docker_stats=None,
                                                        snort_ids_alert_counters=None, ossec_ids_alert_counters=None,
                                                        aggregated_host_metrics=None, defender_actions=None,
                                                        attacker_actions=None, snort_ids_rule_counters=None)
        e_trace = EmulationTrace(
            initial_attacker_observation_state=EmulationAttackerObservationState(catched_flags=7, agent_reachable=None),
            initial_defender_observation_state=e_d_o_state,
            emulation_name="JohnDoeEmulation")
        obj = DataCollectionJobConfig(emulation_env_name="JDoe_env", num_collected_steps=10,
                                      progress_percentage=20.5, attacker_sequence=[e_a_action], pid=5,
                                      repeat_times=5, emulation_statistic_id=5, num_sequences_completed=5,
                                      traces=[e_trace], save_emulation_traces_every=5, num_cached_traces=10,
                                      defender_sequence=[e_d_action], log_file_path="JohnDoeLog",
                                      physical_host_ip="123.456.78.99", descr="")
        return obj

    def test_d_c_jobs_get(self, flask_app, mocker, list_jobs,
                          logged_in, not_logged_in, logged_in_as_admin,
                          pid_true, pid_false,) -> None:
        """
        Testing for the GET HTTPS method in the /data-collection-jobs resource

        :param flask_app: the flask app for making the test requests
        :param mocker: the pytest mocker object
        :param list_ppo: the list_ppo fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param list_ppo_ids: the list_ppo_ids fixture
        :return: None
        """
        test_job = TestResourcesDataCollectionSuite.get_example_job()
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_data_collection_jobs",
                     side_effect=list_jobs)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
                     side_effect=pid_true)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in,)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in,)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        d_c_job_data = DataCollectionJobConfig.from_dict(response_data_list[0])
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert d_c_job_data.attacker_sequence[0].action_outcome == \
            test_job.attacker_sequence[0].action_outcome
        assert d_c_job_data.attacker_sequence[0].alt_cmds[0] == test_job.attacker_sequence[0].alt_cmds[0]
        assert d_c_job_data.attacker_sequence[0].backdoor == test_job.attacker_sequence[0].backdoor
        assert d_c_job_data.attacker_sequence[0].cmds[0] == test_job.attacker_sequence[0].cmds[0]
        assert d_c_job_data.attacker_sequence[0].descr == test_job.attacker_sequence[0].descr
        assert d_c_job_data.attacker_sequence[0].execution_time == \
            test_job.attacker_sequence[0].execution_time
        assert d_c_job_data.attacker_sequence[0].id == test_job.attacker_sequence[0].id
        assert d_c_job_data.attacker_sequence[0].index == test_job.attacker_sequence[0].index
        assert d_c_job_data.attacker_sequence[0].ips[0] == test_job.attacker_sequence[0].ips[0]
        assert d_c_job_data.attacker_sequence[0].name == test_job.attacker_sequence[0].name
        assert d_c_job_data.attacker_sequence[0].ts == test_job.attacker_sequence[0].ts
        assert d_c_job_data.attacker_sequence[0].type == test_job.attacker_sequence[0].type
        assert d_c_job_data.attacker_sequence[0].vulnerability == test_job.attacker_sequence[0].vulnerability
        assert d_c_job_data.defender_sequence[0].action_outcome == test_job.defender_sequence[0].action_outcome
        assert d_c_job_data.defender_sequence[0].alt_cmds[0] == test_job.defender_sequence[0].alt_cmds[0]
        assert d_c_job_data.defender_sequence[0].cmds[0] == test_job.defender_sequence[0].cmds[0]
        assert d_c_job_data.defender_sequence[0].descr == test_job.defender_sequence[0].descr
        # assert d_c_job_data.defender_sequence[0].execution_time == test_job.defender_sequence[0].execution_time
        assert d_c_job_data.defender_sequence[0].id == test_job.defender_sequence[0].id
        assert d_c_job_data.defender_sequence[0].index == test_job.defender_sequence[0].index
        assert d_c_job_data.defender_sequence[0].ips[0] == test_job.defender_sequence[0].ips[0]
        assert d_c_job_data.defender_sequence[0].ts == test_job.defender_sequence[0].ts
        assert d_c_job_data.defender_sequence[0].type == test_job.defender_sequence[0].type
        assert d_c_job_data.defender_sequence[0].name == test_job.defender_sequence[0].name
        assert d_c_job_data.running is True
        assert test_job.running is False
        assert d_c_job_data != test_job.running
        assert d_c_job_data.descr == test_job.descr
        assert d_c_job_data.emulation_env_name == test_job.emulation_env_name
        assert d_c_job_data.emulation_statistic_id == test_job.emulation_statistic_id
        assert d_c_job_data.id == test_job.id
        assert d_c_job_data.log_file_path == test_job.log_file_path
        assert d_c_job_data.num_cached_traces == test_job.num_cached_traces
        assert d_c_job_data.num_collected_steps == test_job.num_collected_steps
        assert d_c_job_data.num_sequences_completed == test_job.num_sequences_completed
        assert d_c_job_data.physical_host_ip == test_job.physical_host_ip
        assert d_c_job_data.pid == test_job.pid
        assert d_c_job_data.progress_percentage == test_job.progress_percentage
        assert d_c_job_data.repeat_times == test_job.repeat_times
        assert d_c_job_data.save_emulation_traces_every == test_job.save_emulation_traces_every
        assert d_c_job_data.traces[0].attacker_actions == test_job.traces[0].attacker_actions
        assert d_c_job_data.traces[0].attacker_observation_states == test_job.traces[0].attacker_observation_states
        assert d_c_job_data.traces[0].defender_actions == test_job.traces[0].defender_actions
        assert d_c_job_data.traces[0].defender_observation_states == test_job.traces[0].defender_actions
        assert d_c_job_data.traces[0].emulation_name == test_job.traces[0].emulation_name
        assert d_c_job_data.traces[0].id == test_job.traces[0].id
        assert d_c_job_data.traces[0].initial_attacker_observation_state.actions_tried == \
            test_job.traces[0].initial_attacker_observation_state.actions_tried
        assert d_c_job_data.traces[0].initial_attacker_observation_state.agent_reachable == \
            test_job.traces[0].initial_attacker_observation_state.agent_reachable
        assert d_c_job_data.traces[0].initial_attacker_observation_state.catched_flags == \
            test_job.traces[0].initial_attacker_observation_state.catched_flags
        assert d_c_job_data.traces[0].initial_attacker_observation_state.machines == \
            test_job.traces[0].initial_attacker_observation_state.machines
        assert d_c_job_data.traces[0].initial_defender_observation_state.actions_tried == \
            test_job.traces[0].initial_defender_observation_state.actions_tried
        assert d_c_job_data.traces[0].initial_defender_observation_state.aggregated_host_metrics.ip == \
            test_job.traces[0].initial_defender_observation_state.aggregated_host_metrics.ip
        assert d_c_job_data.traces[0].initial_defender_observation_state.aggregated_host_metrics. \
            num_failed_login_attempts == \
            test_job.traces[0].initial_defender_observation_state.aggregated_host_metrics.num_failed_login_attempts
        assert d_c_job_data.traces[0].initial_defender_observation_state.aggregated_host_metrics.num_logged_in_users == \
            test_job.traces[0].initial_defender_observation_state.aggregated_host_metrics.num_logged_in_users
        assert d_c_job_data.traces[0].initial_defender_observation_state.aggregated_host_metrics.num_login_events == \
            test_job.traces[0].initial_defender_observation_state.aggregated_host_metrics.num_login_events
        assert d_c_job_data.traces[0].initial_defender_observation_state.aggregated_host_metrics.num_open_connections == \
            test_job.traces[0].initial_defender_observation_state.aggregated_host_metrics.num_open_connections
        assert d_c_job_data.traces[0].initial_defender_observation_state.aggregated_host_metrics.num_processes == \
            test_job.traces[0].initial_defender_observation_state.aggregated_host_metrics.num_processes
        assert d_c_job_data.traces[0].initial_defender_observation_state.aggregated_host_metrics.num_users == \
            test_job.traces[0].initial_defender_observation_state.aggregated_host_metrics.num_users
        assert d_c_job_data.traces[0].initial_defender_observation_state.aggregated_host_metrics.ts == \
            test_job.traces[0].initial_defender_observation_state.aggregated_host_metrics.ts
        assert d_c_job_data.traces[0].initial_defender_observation_state.attacker_actions == \
            test_job.traces[0].initial_defender_observation_state.attacker_actions
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_client_population_metrics.ip == \
            test_job.traces[0].initial_defender_observation_state.avg_client_population_metrics.ip
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_client_population_metrics.num_clients == \
            test_job.traces[0].initial_defender_observation_state.avg_client_population_metrics.num_clients
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_client_population_metrics.rate == \
            test_job.traces[0].initial_defender_observation_state.avg_client_population_metrics.rate
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_client_population_metrics.service_time == \
            test_job.traces[0].initial_defender_observation_state.avg_client_population_metrics.service_time
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_client_population_metrics.ts == \
            test_job.traces[0].initial_defender_observation_state.avg_client_population_metrics.ts
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_docker_stats.blk_read == \
            test_job.traces[0].initial_defender_observation_state.avg_docker_stats.blk_read
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_docker_stats.blk_write == \
            test_job.traces[0].initial_defender_observation_state.avg_docker_stats.blk_write
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_docker_stats.container_name == \
            test_job.traces[0].initial_defender_observation_state.avg_docker_stats.container_name
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_docker_stats.cpu_percent == \
            test_job.traces[0].initial_defender_observation_state.avg_docker_stats.cpu_percent
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_docker_stats.mem_current == \
            test_job.traces[0].initial_defender_observation_state.avg_docker_stats.mem_current
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_docker_stats.mem_percent == \
            test_job.traces[0].initial_defender_observation_state.avg_docker_stats.mem_current
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_docker_stats.mem_total == \
            test_job.traces[0].initial_defender_observation_state.avg_docker_stats.mem_total
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_docker_stats.net_rx == \
            test_job.traces[0].initial_defender_observation_state.avg_docker_stats.net_rx
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_docker_stats.net_tx == \
            test_job.traces[0].initial_defender_observation_state.avg_docker_stats.net_tx
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_docker_stats.pids == \
            test_job.traces[0].initial_defender_observation_state.avg_docker_stats.pids
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_docker_stats.timestamp == \
            test_job.traces[0].initial_defender_observation_state.avg_docker_stats.timestamp
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.alerts_weighted_by_level == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.alerts_weighted_by_level
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.group_alerts == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.group_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.ip == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.ip
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.level_alerts == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.level_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.severe_alerts == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.severe_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.total_alerts == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.total_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.warning_alerts == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.warning_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.alerts_weighted_by_priority == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.alerts_weighted_by_priority
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.class_alerts == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.class_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.ip == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.ip
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.priority_alerts == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.priority_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.severe_alerts == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.severe_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.total_alerts == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.total_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.warning_alerts == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.warning_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_snort_ids_rule_counters.ip == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_snort_ids_rule_counters.ip
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_snort_ids_rule_counters.rule_alerts == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_snort_ids_rule_counters.rule_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_snort_ids_rule_counters.ts == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_snort_ids_rule_counters.ts
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            client_population_metrics.ip == \
            test_job.traces[0].initial_defender_observation_state. \
            client_population_metrics.ip
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            client_population_metrics.num_clients == \
            test_job.traces[0].initial_defender_observation_state. \
            client_population_metrics.num_clients
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            client_population_metrics.rate == \
            test_job.traces[0].initial_defender_observation_state. \
            client_population_metrics.rate
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            client_population_metrics.service_time == \
            test_job.traces[0].initial_defender_observation_state. \
            client_population_metrics.service_time
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            client_population_metrics.ts == \
            test_job.traces[0].initial_defender_observation_state. \
            client_population_metrics.ts
        assert d_c_job_data.traces[0].initial_defender_observation_state.defender_actions == \
            test_job.traces[0].initial_defender_observation_state.defender_actions
        assert d_c_job_data.traces[0].initial_defender_observation_state.docker_stats.blk_read == \
            test_job.traces[0].initial_defender_observation_state.docker_stats.blk_read
        assert d_c_job_data.traces[0].initial_defender_observation_state.docker_stats.blk_write == \
            test_job.traces[0].initial_defender_observation_state.docker_stats.blk_write
        assert d_c_job_data.traces[0].initial_defender_observation_state.docker_stats.container_name == \
            test_job.traces[0].initial_defender_observation_state.docker_stats.container_name
        assert d_c_job_data.traces[0].initial_defender_observation_state.docker_stats.container_name == \
            test_job.traces[0].initial_defender_observation_state.docker_stats.container_name
        assert d_c_job_data.traces[0].initial_defender_observation_state.docker_stats.cpu_percent == \
            test_job.traces[0].initial_defender_observation_state.docker_stats.cpu_percent
        assert d_c_job_data.traces[0].initial_defender_observation_state.docker_stats.mem_current == \
            test_job.traces[0].initial_defender_observation_state.docker_stats.mem_current
        assert d_c_job_data.traces[0].initial_defender_observation_state.docker_stats.mem_percent == \
            test_job.traces[0].initial_defender_observation_state.docker_stats.mem_percent
        assert d_c_job_data.traces[0].initial_defender_observation_state.docker_stats.mem_total == \
            test_job.traces[0].initial_defender_observation_state.docker_stats.mem_total
        assert d_c_job_data.traces[0].initial_defender_observation_state.docker_stats.net_rx == \
            test_job.traces[0].initial_defender_observation_state.docker_stats.net_rx
        assert d_c_job_data.traces[0].initial_defender_observation_state.docker_stats.net_tx == \
            test_job.traces[0].initial_defender_observation_state.docker_stats.net_tx
        assert d_c_job_data.traces[0].initial_defender_observation_state.docker_stats.pids == \
            test_job.traces[0].initial_defender_observation_state.docker_stats.pids
        assert d_c_job_data.traces[0].initial_defender_observation_state.docker_stats.timestamp == \
            test_job.traces[0].initial_defender_observation_state.docker_stats.timestamp
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            docker_gw_bridge_ip == test_job.traces[0].initial_defender_observation_state.\
            kafka_config.container.docker_gw_bridge_ip
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            execution_ip_first_octet == test_job.traces[0].initial_defender_observation_state.\
            kafka_config.container.execution_ip_first_octet
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            full_name_str == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.full_name_str
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            ips_and_networks[0][0] == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.ips_and_networks[0][0]
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            ips_and_networks[0][1].bitmask == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.ips_and_networks[0][1].bitmask
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            ips_and_networks[0][1].interface == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.ips_and_networks[0][1].interface
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            ips_and_networks[0][1].name == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.ips_and_networks[0][1].name
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            ips_and_networks[0][1].subnet_mask == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.ips_and_networks[0][1].subnet_mask
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            ips_and_networks[0][1].subnet_prefix == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.ips_and_networks[0][1].subnet_prefix        
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            level == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.level
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            name == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.name
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            os == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.os
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            physical_host_ip == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.physical_host_ip
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            restart_policy == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.restart_policy
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            suffix == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.suffix
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            version == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.version
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            docker_gw_bridge_ip == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            firewall_config.docker_gw_bridge_ip
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            forward_accept ==test_job.traces[0].initial_defender_observation_state.kafka_config. \
            firewall_config.forward_accept
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            forward_drop == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            firewall_config.forward_drop
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            input_accept == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            firewall_config.input_accept
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            input_drop == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            firewall_config.input_drop
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            ips_gw_default_policy_networks[0].default_forward == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.firewall_config.ips_gw_default_policy_networks[0].default_forward
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            ips_gw_default_policy_networks[0].default_gw == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.firewall_config.ips_gw_default_policy_networks[0].default_gw
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            ips_gw_default_policy_networks[0].default_input == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.firewall_config.ips_gw_default_policy_networks[0].default_input
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            ips_gw_default_policy_networks[0].default_output == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.firewall_config.ips_gw_default_policy_networks[0].default_output
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            ips_gw_default_policy_networks[0].ip == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            firewall_config.ips_gw_default_policy_networks[0].ip
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            ips_gw_default_policy_networks[0].network.bitmask == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.firewall_config.ips_gw_default_policy_networks[0].network.bitmask
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            ips_gw_default_policy_networks[0].network.interface == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            firewall_config.ips_gw_default_policy_networks[0].network.interface
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            ips_gw_default_policy_networks[0].network.name == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.firewall_config.ips_gw_default_policy_networks[0].network.name
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            ips_gw_default_policy_networks[0].network.subnet_mask == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            firewall_config.ips_gw_default_policy_networks[0].network.subnet_mask
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            ips_gw_default_policy_networks[0].network.subnet_prefix == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            firewall_config.ips_gw_default_policy_networks[0].network.subnet_prefix
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            output_accept == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            firewall_config.output_accept
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            output_drop == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            firewall_config.output_drop
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            physical_host_ip == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            firewall_config.physical_host_ip
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            routes == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            firewall_config.routes
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.kafka_manager_log_dir == \
            test_job.traces[0].initial_defender_observation_state.kafka_config. \
            kafka_manager_log_dir
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.kafka_manager_log_file == \
            test_job.traces[0].initial_defender_observation_state.kafka_config. \
            kafka_manager_log_file
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.kafka_manager_max_workers == \
            test_job.traces[0].initial_defender_observation_state.kafka_config. \
            kafka_manager_max_workers
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.kafka_manager_port == \
            test_job.traces[0].initial_defender_observation_state.kafka_config. \
            kafka_manager_port
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.kafka_port == \
            test_job.traces[0].initial_defender_observation_state.kafka_config. \
            kafka_port
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.kafka_port_external == \
            test_job.traces[0].initial_defender_observation_state.kafka_config. \
            kafka_port_external
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            available_memory_gb == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            resources.available_memory_gb
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            container_name == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            resources.container_name
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            docker_gw_bridge_ip == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            resources.docker_gw_bridge_ip
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][0] == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][0]
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].cell_overhead_bytes == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.resources.ips_and_network_configs[0][1].cell_overhead_bytes
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].interface == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.resources.ips_and_network_configs[0][1].interface
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].limit_packets_queue == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.resources.ips_and_network_configs[0][1].limit_packets_queue
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].loss_gemodel_h == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.resources.ips_and_network_configs[0][1].loss_gemodel_h
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].loss_gemodel_k == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.resources.ips_and_network_configs[0][1].loss_gemodel_k
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].loss_gemodel_p == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.resources.ips_and_network_configs[0][1].loss_gemodel_p
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].loss_gemodel_r == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.resources.ips_and_network_configs[0][1].loss_gemodel_r
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].loss_state_markov_chain_p13 == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].loss_state_markov_chain_p13
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].loss_state_markov_chain_p14 == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].loss_state_markov_chain_p14
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].loss_state_markov_chain_p23 == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].loss_state_markov_chain_p23
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].loss_state_markov_chain_p31 == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].loss_state_markov_chain_p31
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].loss_state_markov_chain_p32 == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].loss_state_markov_chain_p32
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_corrupt_correlation_percentage == test_job.traces[0].\
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].packet_corrupt_correlation_percentage
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_corrupt_percentage == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].packet_corrupt_percentage
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_delay_correlation_percentage == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].packet_delay_correlation_percentage
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_delay_distribution == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].packet_delay_distribution
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_delay_jitter_ms == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].packet_delay_jitter_ms
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_delay_ms == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.resources.ips_and_network_configs[0][1].packet_delay_ms
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_duplicate_percentage == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].packet_duplicate_percentage
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_duplicate_correlation_percentage == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].packet_duplicate_correlation_percentage
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_duplicate_percentage == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].packet_duplicate_percentage
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_loss_random_correlation_percentage == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].packet_loss_random_correlation_percentage
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_loss_rate_random_percentage == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].packet_loss_rate_random_percentage
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_loss_type == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.resources.ips_and_network_configs[0][1].packet_loss_type
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_overhead_bytes == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].packet_overhead_bytes
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_reorder_correlation_percentage == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].packet_reorder_correlation_percentage
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_reorder_gap == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.resources.ips_and_network_configs[0][1].packet_reorder_gap
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_reorder_percentage == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].packet_reorder_percentage
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].rate_limit_mbit == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.resources.ips_and_network_configs[0][1].rate_limit_mbit
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            num_cpus == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            resources.num_cpus
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            physical_host_ip == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            resources.physical_host_ip
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config. \
            time_step_len_seconds == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            time_step_len_seconds
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config. \
            time_step_len_seconds == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            time_step_len_seconds
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config. \
            topics[0].attributes == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            topics[0].attributes
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config. \
            topics[0].name == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            topics[0].name
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config. \
            topics[0].num_partitions == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            topics[0].num_partitions
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config. \
            topics[0].num_replicas == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            topics[0].num_replicas
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config. \
            topics[0].retention_time_hours == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            topics[0].retention_time_hours
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.version == \
            test_job.traces[0].initial_defender_observation_state.kafka_config.version
        assert d_c_job_data.traces[0].initial_defender_observation_state.machines == \
            test_job.traces[0].initial_defender_observation_state.machines
        assert d_c_job_data.traces[0].initial_defender_observation_state.ossec_ids_alert_counters. \
            alerts_weighted_by_level == test_job.traces[0].initial_defender_observation_state. \
            ossec_ids_alert_counters.alerts_weighted_by_level
        assert d_c_job_data.traces[0].initial_defender_observation_state.ossec_ids_alert_counters. \
            group_alerts == test_job.traces[0].initial_defender_observation_state. \
            ossec_ids_alert_counters.group_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state.ossec_ids_alert_counters. \
            ip == test_job.traces[0].initial_defender_observation_state. \
            ossec_ids_alert_counters.ip
        assert d_c_job_data.traces[0].initial_defender_observation_state.ossec_ids_alert_counters. \
            level_alerts == test_job.traces[0].initial_defender_observation_state. \
            ossec_ids_alert_counters.level_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state.ossec_ids_alert_counters. \
            severe_alerts == test_job.traces[0].initial_defender_observation_state. \
            ossec_ids_alert_counters.severe_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state.ossec_ids_alert_counters. \
            total_alerts == test_job.traces[0].initial_defender_observation_state. \
            ossec_ids_alert_counters.total_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state.ossec_ids_alert_counters. \
            ts == test_job.traces[0].initial_defender_observation_state. \
            ossec_ids_alert_counters.ts
        assert d_c_job_data.traces[0].initial_defender_observation_state.ossec_ids_alert_counters. \
            warning_alerts == test_job.traces[0].initial_defender_observation_state. \
            ossec_ids_alert_counters.warning_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state.snort_ids_alert_counters. \
            alerts_weighted_by_priority == test_job.traces[0].initial_defender_observation_state. \
            snort_ids_alert_counters.alerts_weighted_by_priority
        assert d_c_job_data.traces[0].initial_defender_observation_state.snort_ids_alert_counters. \
            class_alerts == test_job.traces[0].initial_defender_observation_state. \
            snort_ids_alert_counters.class_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state.snort_ids_alert_counters. \
            ip == test_job.traces[0].initial_defender_observation_state. \
            snort_ids_alert_counters.ip
        assert d_c_job_data.traces[0].initial_defender_observation_state.snort_ids_alert_counters. \
            priority_alerts == test_job.traces[0].initial_defender_observation_state. \
            snort_ids_alert_counters.priority_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state.snort_ids_alert_counters. \
            severe_alerts == test_job.traces[0].initial_defender_observation_state. \
            snort_ids_alert_counters.severe_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state.snort_ids_alert_counters. \
            total_alerts == test_job.traces[0].initial_defender_observation_state. \
            snort_ids_alert_counters.total_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state.snort_ids_alert_counters. \
            ts == test_job.traces[0].initial_defender_observation_state. \
            snort_ids_alert_counters.ts
        assert d_c_job_data.traces[0].initial_defender_observation_state.snort_ids_alert_counters. \
            warning_alerts == test_job.traces[0].initial_defender_observation_state. \
            snort_ids_alert_counters.warning_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state.snort_ids_rule_counters. \
            ip == test_job.traces[0].initial_defender_observation_state. \
            snort_ids_rule_counters.ip
        assert d_c_job_data.traces[0].initial_defender_observation_state.snort_ids_rule_counters. \
            rule_alerts == test_job.traces[0].initial_defender_observation_state. \
            snort_ids_rule_counters.rule_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state.snort_ids_rule_counters. \
            ts == test_job.traces[0].initial_defender_observation_state. \
            snort_ids_rule_counters.ts
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
                     side_effect=pid_false)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)

        d_c_job_data = DataCollectionJobConfig.from_dict(response_data_list[0])
        assert d_c_job_data.running is False
        assert test_job.running is False
        assert d_c_job_data.running == test_job.running
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
                     side_effect=pid_true)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin,)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)

        d_c_job_data = DataCollectionJobConfig.from_dict(response_data_list[0])
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert d_c_job_data.attacker_sequence[0].action_outcome == \
            test_job.attacker_sequence[0].action_outcome
        assert d_c_job_data.attacker_sequence[0].alt_cmds[0] == test_job.attacker_sequence[0].alt_cmds[0]
        assert d_c_job_data.attacker_sequence[0].backdoor == test_job.attacker_sequence[0].backdoor
        assert d_c_job_data.attacker_sequence[0].cmds[0] == test_job.attacker_sequence[0].cmds[0]
        assert d_c_job_data.attacker_sequence[0].descr == test_job.attacker_sequence[0].descr
        assert d_c_job_data.attacker_sequence[0].execution_time == \
            test_job.attacker_sequence[0].execution_time
        assert d_c_job_data.attacker_sequence[0].id == test_job.attacker_sequence[0].id
        assert d_c_job_data.attacker_sequence[0].index == test_job.attacker_sequence[0].index
        assert d_c_job_data.attacker_sequence[0].ips[0] == test_job.attacker_sequence[0].ips[0]
        assert d_c_job_data.attacker_sequence[0].name == test_job.attacker_sequence[0].name
        assert d_c_job_data.attacker_sequence[0].ts == test_job.attacker_sequence[0].ts
        assert d_c_job_data.attacker_sequence[0].type == test_job.attacker_sequence[0].type
        assert d_c_job_data.attacker_sequence[0].vulnerability == test_job.attacker_sequence[0].vulnerability
        assert d_c_job_data.defender_sequence[0].action_outcome == test_job.defender_sequence[0].action_outcome
        assert d_c_job_data.defender_sequence[0].alt_cmds[0] == test_job.defender_sequence[0].alt_cmds[0]
        assert d_c_job_data.defender_sequence[0].cmds[0] == test_job.defender_sequence[0].cmds[0]
        assert d_c_job_data.defender_sequence[0].descr == test_job.defender_sequence[0].descr
        # assert d_c_job_data.defender_sequence[0].execution_time == test_job.defender_sequence[0].execution_time
        assert d_c_job_data.defender_sequence[0].id == test_job.defender_sequence[0].id
        assert d_c_job_data.defender_sequence[0].index == test_job.defender_sequence[0].index
        assert d_c_job_data.defender_sequence[0].ips[0] == test_job.defender_sequence[0].ips[0]
        assert d_c_job_data.defender_sequence[0].ts == test_job.defender_sequence[0].ts
        assert d_c_job_data.defender_sequence[0].type == test_job.defender_sequence[0].type
        assert d_c_job_data.defender_sequence[0].name == test_job.defender_sequence[0].name
        assert d_c_job_data.running is True
        assert test_job.running is False
        assert d_c_job_data != test_job.running
        assert d_c_job_data.descr == test_job.descr
        assert d_c_job_data.emulation_env_name == test_job.emulation_env_name
        assert d_c_job_data.emulation_statistic_id == test_job.emulation_statistic_id
        assert d_c_job_data.id == test_job.id
        assert d_c_job_data.log_file_path == test_job.log_file_path
        assert d_c_job_data.num_cached_traces == test_job.num_cached_traces
        assert d_c_job_data.num_collected_steps == test_job.num_collected_steps
        assert d_c_job_data.num_sequences_completed == test_job.num_sequences_completed
        assert d_c_job_data.physical_host_ip == test_job.physical_host_ip
        assert d_c_job_data.pid == test_job.pid
        assert d_c_job_data.progress_percentage == test_job.progress_percentage
        assert d_c_job_data.repeat_times == test_job.repeat_times
        assert d_c_job_data.save_emulation_traces_every == test_job.save_emulation_traces_every
        assert d_c_job_data.traces[0].attacker_actions == test_job.traces[0].attacker_actions
        assert d_c_job_data.traces[0].attacker_observation_states == test_job.traces[0].attacker_observation_states
        assert d_c_job_data.traces[0].defender_actions == test_job.traces[0].defender_actions
        assert d_c_job_data.traces[0].defender_observation_states == test_job.traces[0].defender_actions
        assert d_c_job_data.traces[0].emulation_name == test_job.traces[0].emulation_name
        assert d_c_job_data.traces[0].id == test_job.traces[0].id
        assert d_c_job_data.traces[0].initial_attacker_observation_state.actions_tried == \
            test_job.traces[0].initial_attacker_observation_state.actions_tried
        assert d_c_job_data.traces[0].initial_attacker_observation_state.agent_reachable == \
            test_job.traces[0].initial_attacker_observation_state.agent_reachable
        assert d_c_job_data.traces[0].initial_attacker_observation_state.catched_flags == \
            test_job.traces[0].initial_attacker_observation_state.catched_flags
        assert d_c_job_data.traces[0].initial_attacker_observation_state.machines == \
            test_job.traces[0].initial_attacker_observation_state.machines
        assert d_c_job_data.traces[0].initial_defender_observation_state.actions_tried == \
            test_job.traces[0].initial_defender_observation_state.actions_tried
        assert d_c_job_data.traces[0].initial_defender_observation_state.aggregated_host_metrics.ip == \
            test_job.traces[0].initial_defender_observation_state.aggregated_host_metrics.ip
        assert d_c_job_data.traces[0].initial_defender_observation_state.aggregated_host_metrics. \
            num_failed_login_attempts == \
            test_job.traces[0].initial_defender_observation_state.aggregated_host_metrics.num_failed_login_attempts
        assert d_c_job_data.traces[0].initial_defender_observation_state.aggregated_host_metrics.num_logged_in_users == \
            test_job.traces[0].initial_defender_observation_state.aggregated_host_metrics.num_logged_in_users
        assert d_c_job_data.traces[0].initial_defender_observation_state.aggregated_host_metrics.num_login_events == \
            test_job.traces[0].initial_defender_observation_state.aggregated_host_metrics.num_login_events
        assert d_c_job_data.traces[0].initial_defender_observation_state.aggregated_host_metrics.num_open_connections == \
            test_job.traces[0].initial_defender_observation_state.aggregated_host_metrics.num_open_connections
        assert d_c_job_data.traces[0].initial_defender_observation_state.aggregated_host_metrics.num_processes == \
            test_job.traces[0].initial_defender_observation_state.aggregated_host_metrics.num_processes
        assert d_c_job_data.traces[0].initial_defender_observation_state.aggregated_host_metrics.num_users == \
            test_job.traces[0].initial_defender_observation_state.aggregated_host_metrics.num_users
        assert d_c_job_data.traces[0].initial_defender_observation_state.aggregated_host_metrics.ts == \
            test_job.traces[0].initial_defender_observation_state.aggregated_host_metrics.ts
        assert d_c_job_data.traces[0].initial_defender_observation_state.attacker_actions == \
            test_job.traces[0].initial_defender_observation_state.attacker_actions
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_client_population_metrics.ip == \
            test_job.traces[0].initial_defender_observation_state.avg_client_population_metrics.ip
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_client_population_metrics.num_clients == \
            test_job.traces[0].initial_defender_observation_state.avg_client_population_metrics.num_clients
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_client_population_metrics.rate == \
            test_job.traces[0].initial_defender_observation_state.avg_client_population_metrics.rate
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_client_population_metrics.service_time == \
            test_job.traces[0].initial_defender_observation_state.avg_client_population_metrics.service_time
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_client_population_metrics.ts == \
            test_job.traces[0].initial_defender_observation_state.avg_client_population_metrics.ts
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_docker_stats.blk_read == \
            test_job.traces[0].initial_defender_observation_state.avg_docker_stats.blk_read
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_docker_stats.blk_write == \
            test_job.traces[0].initial_defender_observation_state.avg_docker_stats.blk_write
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_docker_stats.container_name == \
            test_job.traces[0].initial_defender_observation_state.avg_docker_stats.container_name
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_docker_stats.cpu_percent == \
            test_job.traces[0].initial_defender_observation_state.avg_docker_stats.cpu_percent
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_docker_stats.mem_current == \
            test_job.traces[0].initial_defender_observation_state.avg_docker_stats.mem_current
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_docker_stats.mem_percent == \
            test_job.traces[0].initial_defender_observation_state.avg_docker_stats.mem_current
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_docker_stats.mem_total == \
            test_job.traces[0].initial_defender_observation_state.avg_docker_stats.mem_total
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_docker_stats.net_rx == \
            test_job.traces[0].initial_defender_observation_state.avg_docker_stats.net_rx
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_docker_stats.net_tx == \
            test_job.traces[0].initial_defender_observation_state.avg_docker_stats.net_tx
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_docker_stats.pids == \
            test_job.traces[0].initial_defender_observation_state.avg_docker_stats.pids
        assert d_c_job_data.traces[0].initial_defender_observation_state.avg_docker_stats.timestamp == \
            test_job.traces[0].initial_defender_observation_state.avg_docker_stats.timestamp
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.alerts_weighted_by_level == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.alerts_weighted_by_level
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.group_alerts == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.group_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.ip == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.ip
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.level_alerts == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.level_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.severe_alerts == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.severe_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.total_alerts == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.total_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.warning_alerts == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_ossec_ids_alert_counters.warning_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.alerts_weighted_by_priority == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.alerts_weighted_by_priority
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.class_alerts == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.class_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.ip == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.ip
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.priority_alerts == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.priority_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.severe_alerts == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.severe_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.total_alerts == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.total_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.warning_alerts == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_snort_ids_alert_counters.warning_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_snort_ids_rule_counters.ip == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_snort_ids_rule_counters.ip
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_snort_ids_rule_counters.rule_alerts == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_snort_ids_rule_counters.rule_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            avg_snort_ids_rule_counters.ts == \
            test_job.traces[0].initial_defender_observation_state. \
            avg_snort_ids_rule_counters.ts
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            client_population_metrics.ip == \
            test_job.traces[0].initial_defender_observation_state. \
            client_population_metrics.ip
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            client_population_metrics.num_clients == \
            test_job.traces[0].initial_defender_observation_state. \
            client_population_metrics.num_clients
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            client_population_metrics.rate == \
            test_job.traces[0].initial_defender_observation_state. \
            client_population_metrics.rate
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            client_population_metrics.service_time == \
            test_job.traces[0].initial_defender_observation_state. \
            client_population_metrics.service_time
        assert d_c_job_data.traces[0].initial_defender_observation_state. \
            client_population_metrics.ts == \
            test_job.traces[0].initial_defender_observation_state. \
            client_population_metrics.ts
        assert d_c_job_data.traces[0].initial_defender_observation_state.defender_actions == \
            test_job.traces[0].initial_defender_observation_state.defender_actions
        assert d_c_job_data.traces[0].initial_defender_observation_state.docker_stats.blk_read == \
            test_job.traces[0].initial_defender_observation_state.docker_stats.blk_read
        assert d_c_job_data.traces[0].initial_defender_observation_state.docker_stats.blk_write == \
            test_job.traces[0].initial_defender_observation_state.docker_stats.blk_write
        assert d_c_job_data.traces[0].initial_defender_observation_state.docker_stats.container_name == \
            test_job.traces[0].initial_defender_observation_state.docker_stats.container_name
        assert d_c_job_data.traces[0].initial_defender_observation_state.docker_stats.container_name == \
            test_job.traces[0].initial_defender_observation_state.docker_stats.container_name
        assert d_c_job_data.traces[0].initial_defender_observation_state.docker_stats.cpu_percent == \
            test_job.traces[0].initial_defender_observation_state.docker_stats.cpu_percent
        assert d_c_job_data.traces[0].initial_defender_observation_state.docker_stats.mem_current == \
            test_job.traces[0].initial_defender_observation_state.docker_stats.mem_current
        assert d_c_job_data.traces[0].initial_defender_observation_state.docker_stats.mem_percent == \
            test_job.traces[0].initial_defender_observation_state.docker_stats.mem_percent
        assert d_c_job_data.traces[0].initial_defender_observation_state.docker_stats.mem_total == \
            test_job.traces[0].initial_defender_observation_state.docker_stats.mem_total
        assert d_c_job_data.traces[0].initial_defender_observation_state.docker_stats.net_rx == \
            test_job.traces[0].initial_defender_observation_state.docker_stats.net_rx
        assert d_c_job_data.traces[0].initial_defender_observation_state.docker_stats.net_tx == \
            test_job.traces[0].initial_defender_observation_state.docker_stats.net_tx
        assert d_c_job_data.traces[0].initial_defender_observation_state.docker_stats.pids == \
            test_job.traces[0].initial_defender_observation_state.docker_stats.pids
        assert d_c_job_data.traces[0].initial_defender_observation_state.docker_stats.timestamp == \
            test_job.traces[0].initial_defender_observation_state.docker_stats.timestamp
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            docker_gw_bridge_ip == test_job.traces[0].initial_defender_observation_state.\
            kafka_config.container.docker_gw_bridge_ip
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            execution_ip_first_octet == test_job.traces[0].initial_defender_observation_state.\
            kafka_config.container.execution_ip_first_octet
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            full_name_str == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.full_name_str
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            ips_and_networks[0][0] == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.ips_and_networks[0][0]
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            ips_and_networks[0][1].bitmask == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.ips_and_networks[0][1].bitmask
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            ips_and_networks[0][1].interface == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.ips_and_networks[0][1].interface
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            ips_and_networks[0][1].name == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.ips_and_networks[0][1].name
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            ips_and_networks[0][1].subnet_mask == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.ips_and_networks[0][1].subnet_mask
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            ips_and_networks[0][1].subnet_prefix == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.ips_and_networks[0][1].subnet_prefix        
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            level == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.level
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            name == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.name
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            os == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.os
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            physical_host_ip == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.physical_host_ip
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            restart_policy == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.restart_policy
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            suffix == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.suffix
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.container.\
            version == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.container.version
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            docker_gw_bridge_ip == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            firewall_config.docker_gw_bridge_ip
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            forward_accept ==test_job.traces[0].initial_defender_observation_state.kafka_config. \
            firewall_config.forward_accept
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            forward_drop == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            firewall_config.forward_drop
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            input_accept == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            firewall_config.input_accept
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            input_drop == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            firewall_config.input_drop
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            ips_gw_default_policy_networks[0].default_forward == test_job.traces[0]. \
            initial_defender_observation_state. \
            kafka_config.firewall_config.ips_gw_default_policy_networks[0].default_forward
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            ips_gw_default_policy_networks[0].default_gw == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.firewall_config.ips_gw_default_policy_networks[0].default_gw
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            ips_gw_default_policy_networks[0].default_input == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.firewall_config.ips_gw_default_policy_networks[0].default_input
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            ips_gw_default_policy_networks[0].default_output == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.firewall_config.ips_gw_default_policy_networks[0].default_output
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            ips_gw_default_policy_networks[0].ip == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.firewall_config.ips_gw_default_policy_networks[0].ip
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            ips_gw_default_policy_networks[0].network.bitmask == test_job.traces[0].initial_defender_observation_state.\
            kafka_config.firewall_config.ips_gw_default_policy_networks[0].network.bitmask
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            ips_gw_default_policy_networks[0].network.interface == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            firewall_config.ips_gw_default_policy_networks[0].network.interface
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            ips_gw_default_policy_networks[0].network.name == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.firewall_config.ips_gw_default_policy_networks[0].network.name
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            ips_gw_default_policy_networks[0].network.subnet_mask == test_job.traces[0]. \
            initial_defender_observation_state. \
            kafka_config.firewall_config.ips_gw_default_policy_networks[0].network.subnet_mask
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            ips_gw_default_policy_networks[0].network.subnet_prefix == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            firewall_config.ips_gw_default_policy_networks[0].network.subnet_prefix
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            output_accept == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            firewall_config.output_accept
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            output_drop == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            firewall_config.output_drop
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            physical_host_ip == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            firewall_config.physical_host_ip
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.firewall_config.\
            routes == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            firewall_config.routes
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.kafka_manager_log_dir == \
            test_job.traces[0].initial_defender_observation_state.kafka_config. \
            kafka_manager_log_dir
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.kafka_manager_log_file == \
            test_job.traces[0].initial_defender_observation_state.kafka_config. \
            kafka_manager_log_file
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.kafka_manager_max_workers == \
            test_job.traces[0].initial_defender_observation_state.kafka_config. \
            kafka_manager_max_workers
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.kafka_manager_port == \
            test_job.traces[0].initial_defender_observation_state.kafka_config. \
            kafka_manager_port
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.kafka_port == \
            test_job.traces[0].initial_defender_observation_state.kafka_config. \
            kafka_port
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.kafka_port_external == \
            test_job.traces[0].initial_defender_observation_state.kafka_config. \
            kafka_port_external
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            available_memory_gb == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            resources.available_memory_gb
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            container_name == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            resources.container_name
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            docker_gw_bridge_ip == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            resources.docker_gw_bridge_ip
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][0] == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][0]
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].cell_overhead_bytes == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config.resources.ips_and_network_configs[0][1]. \
            cell_overhead_bytes
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].interface == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config.resources.ips_and_network_configs[0][1].interface
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].limit_packets_queue == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config.resources.ips_and_network_configs[0][1]. \
            limit_packets_queue
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].loss_gemodel_h == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config.resources.ips_and_network_configs[0][1].loss_gemodel_h
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].loss_gemodel_k == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.resources.ips_and_network_configs[0][1].loss_gemodel_k
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].loss_gemodel_p == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.resources.ips_and_network_configs[0][1].loss_gemodel_p
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].loss_gemodel_r == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.resources.ips_and_network_configs[0][1].loss_gemodel_r
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].loss_state_markov_chain_p13 == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].loss_state_markov_chain_p13
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].loss_state_markov_chain_p14 == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].loss_state_markov_chain_p14
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].loss_state_markov_chain_p23 == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].loss_state_markov_chain_p23
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].loss_state_markov_chain_p31 == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].loss_state_markov_chain_p31
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].loss_state_markov_chain_p32 == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].loss_state_markov_chain_p32
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_corrupt_correlation_percentage == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].packet_corrupt_correlation_percentage
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_corrupt_percentage == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].packet_corrupt_percentage
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_delay_correlation_percentage == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config.resources.ips_and_network_configs[0][1]. \
            packet_delay_correlation_percentage
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_delay_distribution == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].packet_delay_distribution
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_delay_jitter_ms == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].packet_delay_jitter_ms
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_delay_ms == test_job.traces[0].initial_defender_observation_state. \
                kafka_config.resources.ips_and_network_configs[0][1].packet_delay_ms
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_duplicate_percentage == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].packet_duplicate_percentage
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_duplicate_correlation_percentage == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].packet_duplicate_correlation_percentage
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_duplicate_percentage == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].packet_duplicate_percentage
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_loss_random_correlation_percentage == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].packet_loss_random_correlation_percentage
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_loss_rate_random_percentage == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].packet_loss_rate_random_percentage
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_loss_type == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.resources.ips_and_network_configs[0][1].packet_loss_type
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_overhead_bytes == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].packet_overhead_bytes
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_reorder_correlation_percentage == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].packet_reorder_correlation_percentage
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_reorder_gap == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.resources.ips_and_network_configs[0][1].packet_reorder_gap
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].packet_reorder_percentage == test_job.traces[0]. \
            initial_defender_observation_state.kafka_config. \
            resources.ips_and_network_configs[0][1].packet_reorder_percentage
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            ips_and_network_configs[0][1].rate_limit_mbit == test_job.traces[0].initial_defender_observation_state. \
            kafka_config.resources.ips_and_network_configs[0][1].rate_limit_mbit
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            num_cpus == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            resources.num_cpus
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.resources. \
            physical_host_ip == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            resources.physical_host_ip
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config. \
            time_step_len_seconds == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            time_step_len_seconds
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config. \
            time_step_len_seconds == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            time_step_len_seconds
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config. \
            topics[0].attributes == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            topics[0].attributes
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config. \
            topics[0].name == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            topics[0].name
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config. \
            topics[0].num_partitions == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            topics[0].num_partitions
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config. \
            topics[0].num_replicas == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            topics[0].num_replicas
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config. \
            topics[0].retention_time_hours == test_job.traces[0].initial_defender_observation_state.kafka_config. \
            topics[0].retention_time_hours
        assert d_c_job_data.traces[0].initial_defender_observation_state.kafka_config.version == \
            test_job.traces[0].initial_defender_observation_state.kafka_config.version
        assert d_c_job_data.traces[0].initial_defender_observation_state.machines == \
            test_job.traces[0].initial_defender_observation_state.machines
        assert d_c_job_data.traces[0].initial_defender_observation_state.ossec_ids_alert_counters. \
            alerts_weighted_by_level == test_job.traces[0].initial_defender_observation_state. \
            ossec_ids_alert_counters.alerts_weighted_by_level
        assert d_c_job_data.traces[0].initial_defender_observation_state.ossec_ids_alert_counters. \
            group_alerts == test_job.traces[0].initial_defender_observation_state. \
            ossec_ids_alert_counters.group_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state.ossec_ids_alert_counters. \
            ip == test_job.traces[0].initial_defender_observation_state. \
            ossec_ids_alert_counters.ip
        assert d_c_job_data.traces[0].initial_defender_observation_state.ossec_ids_alert_counters. \
            level_alerts == test_job.traces[0].initial_defender_observation_state. \
            ossec_ids_alert_counters.level_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state.ossec_ids_alert_counters. \
            severe_alerts == test_job.traces[0].initial_defender_observation_state. \
            ossec_ids_alert_counters.severe_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state.ossec_ids_alert_counters. \
            total_alerts == test_job.traces[0].initial_defender_observation_state. \
            ossec_ids_alert_counters.total_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state.ossec_ids_alert_counters. \
            ts == test_job.traces[0].initial_defender_observation_state. \
            ossec_ids_alert_counters.ts
        assert d_c_job_data.traces[0].initial_defender_observation_state.ossec_ids_alert_counters. \
            warning_alerts == test_job.traces[0].initial_defender_observation_state. \
            ossec_ids_alert_counters.warning_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state.snort_ids_alert_counters. \
            alerts_weighted_by_priority == test_job.traces[0].initial_defender_observation_state. \
            snort_ids_alert_counters.alerts_weighted_by_priority
        assert d_c_job_data.traces[0].initial_defender_observation_state.snort_ids_alert_counters. \
            class_alerts == test_job.traces[0].initial_defender_observation_state. \
            snort_ids_alert_counters.class_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state.snort_ids_alert_counters. \
            ip == test_job.traces[0].initial_defender_observation_state. \
            snort_ids_alert_counters.ip
        assert d_c_job_data.traces[0].initial_defender_observation_state.snort_ids_alert_counters. \
            priority_alerts == test_job.traces[0].initial_defender_observation_state. \
            snort_ids_alert_counters.priority_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state.snort_ids_alert_counters. \
            severe_alerts == test_job.traces[0].initial_defender_observation_state. \
            snort_ids_alert_counters.severe_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state.snort_ids_alert_counters. \
            total_alerts == test_job.traces[0].initial_defender_observation_state. \
            snort_ids_alert_counters.total_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state.snort_ids_alert_counters. \
            ts == test_job.traces[0].initial_defender_observation_state. \
            snort_ids_alert_counters.ts
        assert d_c_job_data.traces[0].initial_defender_observation_state.snort_ids_alert_counters. \
            warning_alerts == test_job.traces[0].initial_defender_observation_state. \
            snort_ids_alert_counters.warning_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state.snort_ids_rule_counters. \
            ip == test_job.traces[0].initial_defender_observation_state. \
            snort_ids_rule_counters.ip
        assert d_c_job_data.traces[0].initial_defender_observation_state.snort_ids_rule_counters. \
            rule_alerts == test_job.traces[0].initial_defender_observation_state. \
            snort_ids_rule_counters.rule_alerts
        assert d_c_job_data.traces[0].initial_defender_observation_state.snort_ids_rule_counters. \
            ts == test_job.traces[0].initial_defender_observation_state. \
            snort_ids_rule_counters.ts
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
                     side_effect=pid_false)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        d_c_job_data = DataCollectionJobConfig.from_dict(response_data_list[0])
        assert d_c_job_data.running is False
        assert test_job.running is False
        assert d_c_job_data.running == test_job.running

    def test_d_c_jobs_delete(self, flask_app, mocker, list_jobs, logged_in,
                             not_logged_in, logged_in_as_admin, remove, stop) -> None:
        """
        Tests the HTTP DELETE method on the /data-collection-jobs resource

        :param flask_app: the flask app for making the test requests
        :param mocker: the pytest mocker object
        :param list_ppo: the list_ppo fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param remove: the remove fixture
        :return: None
        """
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_data_collection_jobs",
                     side_effect=list_jobs)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_data_collection_job",
                     side_effect=remove)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_pid",
                     side_effect=stop)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}
