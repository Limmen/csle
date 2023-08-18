from typing import List
import json
import pytest
import pytest_mock
import csle_common.constants.constants as constants
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_outcome import EmulationAttackerActionOutcome
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.defender.emulation_defender_action_id import EmulationDefenderActionId
from csle_common.dao.emulation_action.defender.emulation_defender_action_outcome import EmulationDefenderActionOutcome
from csle_common.dao.emulation_action.defender.emulation_defender_action_type import EmulationDefenderActionType
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.dao.emulation_config.default_network_firewall_config import DefaultNetworkFirewallConfig
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace
from csle_common.dao.emulation_config.kafka_config import KafkaConfig
from csle_common.dao.emulation_config.kafka_topic import KafkaTopic
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.dao.emulation_config.node_firewall_config import NodeFirewallConfig
from csle_common.dao.emulation_config.node_network_config import NodeNetworkConfig
from csle_common.dao.emulation_config.node_resources_config import NodeResourcesConfig
from csle_common.dao.emulation_config.packet_delay_distribution_type import PacketDelayDistributionType
from csle_common.dao.emulation_config.packet_loss_type import PacketLossType
from csle_common.dao.emulation_observation.attacker.emulation_attacker_observation_state import \
    EmulationAttackerObservationState
from csle_common.dao.emulation_observation.defender.emulation_defender_observation_state import \
    EmulationDefenderObservationState
from csle_collector.client_manager.client_population_metrics import ClientPopulationMetrics
from csle_collector.docker_stats_manager.dao.docker_stats import DockerStats
from csle_collector.snort_ids_manager.dao.snort_ids_alert_counters import SnortIdsAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_rule_counters import SnortIdsRuleCounters
from csle_collector.ossec_ids_manager.dao.ossec_ids_alert_counters import OSSECIdsAlertCounters
from csle_collector.host_manager.dao.host_metrics import HostMetrics
from csle_common.dao.jobs.data_collection_job_config import DataCollectionJobConfig
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesDataCollectionSuite:
    """
    Test suite for /data-collection-jobs resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def list_jobs(self, mocker: pytest_mock.MockFixture):
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
    def remove(self, mocker: pytest_mock.MockFixture):
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
    def start(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for the start_data_collection_job_in_background function

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """

        def start_data_collection_job_in_background(data_collection_job: DataCollectionJobConfig) -> None:
            return None

        start_data_collection_job_in_background_mocker = mocker.MagicMock(
            side_effect=start_data_collection_job_in_background)
        return start_data_collection_job_in_background_mocker

    @pytest.fixture
    def get_job_config(self, mocker: pytest_mock.MockFixture) -> DataCollectionJobConfig:
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
        Utility function for getting an example instance of a data-collection-job configuration

        :return: an example instance of a data-collection-job configuration
        """
        nn_config = NodeNetworkConfig(packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                      packet_loss_type=PacketLossType.GEMODEL)
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
            ips_gw_default_policy_networks=[
                DefaultNetworkFirewallConfig(ip="123.456.78.99", default_gw="gateway", default_input="input",
                                             default_output="output", default_forward="forward",
                                             network=ContainerNetwork(name="JohnDoe", subnet_mask="JDoeMask",
                                                                      bitmask="BitMask", subnet_prefix="SubPrefix",
                                                                      interface="eth0"))],
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
        e_a_action = EmulationAttackerAction(id=EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST,
                                             name="JohnDoe", cmds=["JohnDoeCommands"],
                                             type=EmulationAttackerActionType.RECON,
                                             descr="null", ips=["JohnDoeIPs"], index=10,
                                             action_outcome=EmulationAttackerActionOutcome.INFORMATION_GATHERING,
                                             vulnerability="Vulnerability", alt_cmds=["JDoeCommands"],
                                             backdoor=False, execution_time=0.1, ts=1.1)
        e_d_action = EmulationDefenderAction(id=EmulationDefenderActionId.STOP, name="JohnDoe",
                                             cmds=["JohnDoeCommands"], type=EmulationDefenderActionType.STOP,
                                             descr="null", ips=["JohnDoeIPs"], index=10,
                                             action_outcome=EmulationDefenderActionOutcome.GAME_END,
                                             alt_cmds=["JDoeCommands"], execution_time=0.1, ts=1.1)
        e_d_o_state = EmulationDefenderObservationState(
            kafka_config=k_config, client_population_metrics=ClientPopulationMetrics(),
            docker_stats=DockerStats(), snort_ids_alert_counters=SnortIdsAlertCounters(),
            snort_ids_rule_counters=SnortIdsRuleCounters(), ossec_ids_alert_counters=OSSECIdsAlertCounters(),
            aggregated_host_metrics=HostMetrics(), defender_actions=[], attacker_actions=[])
        e_trace = EmulationTrace(
            initial_attacker_observation_state=EmulationAttackerObservationState(catched_flags=7,
                                                                                 agent_reachable=set()),
            initial_defender_observation_state=e_d_o_state,
            emulation_name="JohnDoeEmulation")
        obj = DataCollectionJobConfig(emulation_env_name="JDoe_env", num_collected_steps=10,
                                      progress_percentage=20.5, attacker_sequence=[e_a_action], pid=5,
                                      repeat_times=5, emulation_statistic_id=5, num_sequences_completed=5,
                                      traces=[e_trace], save_emulation_traces_every=5, num_cached_traces=10,
                                      defender_sequence=[e_d_action], log_file_path="JohnDoeLog",
                                      physical_host_ip="123.456.78.99", descr="")
        return obj

    def test_d_c_jobs_get(self, flask_app, mocker: pytest_mock.MockFixture, list_jobs,
                          logged_in, not_logged_in, logged_in_as_admin,
                          pid_true, pid_false, ) -> None:
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
        mocker.patch('time.sleep', return_value=None)
        test_job = TestResourcesDataCollectionSuite.get_example_job()
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_data_collection_jobs",
                     side_effect=list_jobs)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
                     side_effect=pid_true)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response_data_list[0][api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == test_job.emulation_env_name
        assert response_data_list[0][api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] is True
        assert response_data_list[0][api_constants.MGMT_WEBAPP.ID_PROPERTY] == test_job.id
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        d_c_job_data = DataCollectionJobConfig.from_dict(response_data_list[0])
        d_c_job_data_dict = d_c_job_data.to_dict()
        test_job_dict = test_job.to_dict()
        for k in d_c_job_data_dict:
            if k != api_constants.MGMT_WEBAPP.RUNNING_PROPERTY:
                assert d_c_job_data_dict[k] == test_job_dict[k]
            else:
                continue
        assert d_c_job_data.running is True
        assert test_job.running is False
        assert d_c_job_data != test_job.running
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
                     side_effect=pid_false)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response_data_list[0][api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == test_job.emulation_env_name
        assert response_data_list[0][api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] is False
        assert response_data_list[0][api_constants.MGMT_WEBAPP.ID_PROPERTY] == test_job.id
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        d_c_job_data = DataCollectionJobConfig.from_dict(response_data_list[0])
        d_c_job_data_dict = d_c_job_data.to_dict()
        test_job_dict = test_job.to_dict()
        for k in d_c_job_data_dict:
            if k != api_constants.MGMT_WEBAPP.RUNNING_PROPERTY:
                assert d_c_job_data_dict[k] == test_job_dict[k]
            else:
                continue
        assert d_c_job_data.running is False
        assert test_job.running is False
        assert d_c_job_data.running == test_job.running
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
                     side_effect=pid_true)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response_data_list[0][api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == test_job.emulation_env_name
        assert response_data_list[0][api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] is True
        assert response_data_list[0][api_constants.MGMT_WEBAPP.ID_PROPERTY] == test_job.id
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        d_c_job_data = DataCollectionJobConfig.from_dict(response_data_list[0])
        d_c_job_data_dict = d_c_job_data.to_dict()
        test_job_dict = test_job.to_dict()
        for k in d_c_job_data_dict:
            if k != api_constants.MGMT_WEBAPP.RUNNING_PROPERTY:
                assert d_c_job_data_dict[k] == test_job_dict[k]
            else:
                continue
        assert d_c_job_data.running is True
        assert test_job.running is False
        assert d_c_job_data.running != test_job.running
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
                     side_effect=pid_false)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        d_c_job_data = DataCollectionJobConfig.from_dict(response_data_list[0])
        d_c_job_data_dict = d_c_job_data.to_dict()
        test_job_dict = test_job.to_dict()
        for k in d_c_job_data_dict:
            if k != api_constants.MGMT_WEBAPP.RUNNING_PROPERTY:
                assert d_c_job_data_dict[k] == test_job_dict[k]
            else:
                continue
        assert d_c_job_data.running is False
        assert test_job.running is False
        assert d_c_job_data.running == test_job.running
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response_data_list[0][api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == test_job.emulation_env_name
        assert response_data_list[0][api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] is False
        assert response_data_list[0][api_constants.MGMT_WEBAPP.ID_PROPERTY] == test_job.id

    def test_d_c_jobs_delete(self, flask_app, mocker: pytest_mock.MockFixture, list_jobs, logged_in,
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
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_data_collection_jobs",
                     side_effect=list_jobs)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_data_collection_job",
                     side_effect=remove)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_pid", side_effect=stop)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}

    def test_d_c_jobs_id_get(self, flask_app, mocker: pytest_mock.MockFixture, logged_in, not_logged_in,
                             logged_in_as_admin, get_job_config, pid_true, pid_false) -> None:
        """
        Tests the HTTPS GET method for the /data-collection-jobs/id resource

        :param flask_app: the flask app for making the test requests
        :param mocker: the pytest mocker object
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_job_config: the get_job_config fixture
        :param pid_true: the pid_true fixture
        :param pid_false: the pid_false fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        test_job = TestResourcesDataCollectionSuite.get_example_job()
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_data_collection_job_config",
                     side_effect=get_job_config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
                     side_effect=pid_true)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        d_c_job_data = DataCollectionJobConfig.from_dict(response_data_list)
        d_c_job_data_dict = d_c_job_data.to_dict()
        test_job_dict = test_job.to_dict()
        for k in d_c_job_data_dict:
            if k != api_constants.MGMT_WEBAPP.RUNNING_PROPERTY:
                assert d_c_job_data_dict[k] == test_job_dict[k]
            else:
                continue
        assert d_c_job_data.running is True
        assert test_job.running is False
        assert d_c_job_data != test_job.running
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
                     side_effect=pid_false)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        d_c_job_data = DataCollectionJobConfig.from_dict(response_data_list)
        d_c_job_data_dict = d_c_job_data.to_dict()
        test_job_dict = test_job.to_dict()
        for k in d_c_job_data_dict:
            if k != api_constants.MGMT_WEBAPP.RUNNING_PROPERTY:
                assert d_c_job_data_dict[k] == test_job_dict[k]
            else:
                continue
        assert d_c_job_data.running is False
        assert test_job.running is False
        assert d_c_job_data.running == test_job.running
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
                     side_effect=pid_true)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        d_c_job_data = DataCollectionJobConfig.from_dict(response_data_list)
        d_c_job_data_dict = d_c_job_data.to_dict()
        test_job_dict = test_job.to_dict()
        for k in d_c_job_data_dict:
            if k != api_constants.MGMT_WEBAPP.RUNNING_PROPERTY:
                assert d_c_job_data_dict[k] == test_job_dict[k]
            else:
                continue
        assert d_c_job_data.running is True
        assert test_job.running is False
        assert d_c_job_data.running != test_job.running
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.check_pid",
                     side_effect=pid_false)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        d_c_job_data = DataCollectionJobConfig.from_dict(response_data_list)
        d_c_job_data_dict = d_c_job_data.to_dict()
        test_job_dict = test_job.to_dict()
        for k in d_c_job_data_dict:
            if k != api_constants.MGMT_WEBAPP.RUNNING_PROPERTY:
                assert d_c_job_data_dict[k] == test_job_dict[k]
            else:
                continue
        assert d_c_job_data.running is False
        assert test_job.running is False
        assert d_c_job_data.running == test_job.running

    def test_d_c_jobs_id_delete(self, flask_app, mocker: pytest_mock.MockFixture, logged_in_as_admin, logged_in,
                                not_logged_in, get_job_config, remove, stop) -> None:
        """
        Tests the HTTPS DELETE method for the /data-collection-jobs/id resource

        :param flask_app: the flask app for making the tests requests
        :param mocker: the pytest mocker object
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin:  the logged_in_as_admin fixure
        :param get_job_config: the get_job_config fixture
        :param remove: the remove fixture
        :param stop: the stop fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_data_collection_job_config",
                     side_effect=get_job_config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_pid", side_effect=stop)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_data_collection_job",
                     side_effect=remove)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}"f"/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}

    def test_d_c_jobs_id_post(self, flask_app, mocker: pytest_mock.MockFixture, logged_in_as_admin, logged_in,
                              not_logged_in, get_job_config, start, stop) -> None:
        """
        Tests the HTTPS DELETE method for the /data-collection-jobs/id resource

        :param flask_app: the flask app for making the tests requests
        :param mocker: the pytest mocker object
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin:  the logged_in_as_admin fixture
        :param get_job_config: the get_job_config fixture
        :param remove: the remove fixture
        :param stop: the stop fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_data_collection_job_config",
                     side_effect=get_job_config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_pid", side_effect=stop)
        mocker.patch("csle_system_identification.job_controllers.data_collection_job_manager.DataCollectionJobManager."
                     "start_data_collection_job_in_background", side_effect=start)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}/10"
                                                f"?{api_constants.MGMT_WEBAPP.STOP_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.DATA_COLLECTION_JOBS_RESOURCE}/10"
                                                f"?{api_constants.MGMT_WEBAPP.STOP_QUERY_PARAM}=false")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}
