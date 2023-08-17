import json
from typing import List, Tuple
import pytest
import pytest_mock
import logging
import csle_common.constants.constants as constants
from csle_cluster.cluster_manager.cluster_manager_pb2 import OperationOutcomeDTO, RunningEmulationsDTO
from csle_collector.client_manager.client_population_metrics import ClientPopulationMetrics
from csle_collector.docker_stats_manager.dao.docker_stats import DockerStats
from csle_collector.host_manager.dao.host_metrics import HostMetrics
from csle_collector.ossec_ids_manager.dao.ossec_ids_alert_counters import OSSECIdsAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_alert_counters import SnortIdsAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_ip_alert_counters import SnortIdsIPAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_rule_counters import SnortIdsRuleCounters
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_outcome import EmulationAttackerActionOutcome
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.defender.emulation_defender_action_id import EmulationDefenderActionId
from csle_common.dao.emulation_action.defender.emulation_defender_action_outcome import EmulationDefenderActionOutcome
from csle_common.dao.emulation_action.defender.emulation_defender_action_type import EmulationDefenderActionType
from csle_common.dao.emulation_config.config import Config
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.emulation_execution import EmulationExecution
from csle_common.dao.emulation_config.emulation_metrics_time_series import EmulationMetricsTimeSeries
from csle_ryu.dao.agg_flow_statistic import AggFlowStatistic
from csle_ryu.dao.avg_flow_statistic import AvgFlowStatistic
from csle_ryu.dao.avg_port_statistic import AvgPortStatistic
from csle_ryu.dao.flow_statistic import FlowStatistic
from csle_ryu.dao.port_statistic import PortStatistic
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesEmulationsSuite:
    """
    Test suite for /emulations resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def config(self, mocker: pytest_mock.MockFixture, example_config: Config):
        """
        Pytest fixture for mocking the get_config function

        :param mocker: the pytest mocker object
        :param example_config: The example_config function fetched from conftest.py
        :return: the mocked function
        """

        def get_config(id: int) -> Config:
            config = example_config
            return config

        get_config_mocker = mocker.MagicMock(side_effect=get_config)
        return get_config_mocker

    @pytest.fixture
    def emulations(self, mocker: pytest_mock.MockFixture, get_ex_em_env: EmulationEnvConfig):
        """
        Pytest fixture for mocking the list_emulations function

        :param mocker: the pytest mocker object
        :param get_ex_em_env: fixture returning an example EmulationEnvConfig
        :return: the mocked function
        """

        def list_emulations() -> List[EmulationEnvConfig]:
            em_env = get_ex_em_env
            return [em_env]

        list_emulations_mocker = mocker.MagicMock(side_effect=list_emulations)
        return list_emulations_mocker

    @pytest.fixture
    def emulation_id(self, mocker: pytest_mock.MockFixture, get_ex_em_env: EmulationEnvConfig):
        """
        Pytest fixture for mocking the get_emulation function

        :param mocker: the pytest mocker object
        :param get_ex_em_env: fixture returning an example EmulationEnvConfig
        :return: the mocked function
        """

        def get_emulation(id: int) -> EmulationEnvConfig:
            em_env = get_ex_em_env
            return em_env

        get_emulation_mocker = mocker.MagicMock(side_effect=get_emulation)
        return get_emulation_mocker

    @pytest.fixture
    def emulations_images(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_emulation_images function

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def list_emulation_images() -> List[Tuple[str, bytes]]:  # OBS: kan bli fel
            em_im_list = [("Emulation1", bytes("Emulation1", "utf-8"))]
            return em_im_list

        list_emulation_images_mocker = mocker.MagicMock(side_effect=list_emulation_images)
        return list_emulation_images_mocker

    @pytest.fixture
    def running_emulations(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_all_running_emulations method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def list_all_running_emulations(ip: str, port: int) -> RunningEmulationsDTO:
            return RunningEmulationsDTO(runningEmulations="abcdef")

        list_all_running_emulations_mocker = mocker.MagicMock(side_effect=list_all_running_emulations)
        return list_all_running_emulations_mocker

    @pytest.fixture
    def given_emulation(self, mocker: pytest_mock.MockFixture, get_ex_em_env: EmulationEnvConfig):
        """
        Pytest fixture for mocking the list_emulation_executions_for_a_given_emulation method

        :param mocker: the pytest mocker object
        :param get_ex_em_env: fixture returning an example EmulationEnvConfig
        :return: the mocked function
        """

        def list_emulation_executions_for_a_given_emulation(emulation_name: str) -> List[EmulationExecution]:
            em_env = get_ex_em_env
            em_ex = EmulationExecution(emulation_name="JohbnDoeEmulation", timestamp=1.5, ip_first_octet=-1,
                                       emulation_env_config=em_env, physical_servers=["JohnDoeServer"])
            return [em_ex]

        list_emulation_executions_for_a_given_emulation_mocker = \
            mocker.MagicMock(side_effect=list_emulation_executions_for_a_given_emulation)
        return list_emulation_executions_for_a_given_emulation_mocker

    @pytest.fixture
    def uninstall(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the uninstall_emulation function

        :param mocker: The pytest mocker object
        :return: The mocked function
        """

        def uninstall_emulation(config: EmulationEnvConfig) -> None:
            return None

        uninstall_emulation_mocker = mocker.MagicMock(side_effect=uninstall_emulation)
        return uninstall_emulation_mocker

    @pytest.fixture
    def clean(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the clean_all_executions_of_emulation function

        :param mocker: The pytest mocker object
        :return: The mocked function
        """

        def clean_all_executions_of_emulation(ip: str, port: int, emulation: str) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        clean_all_executions_of_emulation_mocker = mocker.MagicMock(side_effect=clean_all_executions_of_emulation)
        return clean_all_executions_of_emulation_mocker

    @pytest.fixture
    def get_em_im(self, mocker: pytest_mock.MockFixture):
        """
        pytest fixture for mocking the get_emulation_image function

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_emulation_image(emulation_name: str) -> None:
            return None

        get_emulation_image_mocker = mocker.MagicMock(side_effect=get_emulation_image)
        return get_emulation_image_mocker

    @pytest.fixture
    def emulations_ids_in_names(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_emulations_ids function

        :param mocker: the pytest mocker object
        :return: The mocked function
        """

        def list_emulations_ids() -> List[Tuple[int, str]]:
            list_tuple = [(10, "a")]
            return list_tuple

        list_emulations_ids_mocker = mocker.MagicMock(side_effect=list_emulations_ids
                                                      )
        return list_emulations_ids_mocker

    @pytest.fixture
    def host(self, mocker: pytest_mock.MockFixture):
        """
        Pyetst fixutre for mocking the get_host_ip function

        :param mocker: The pytest mocker object
        :return: The mocked function
        """

        def get_host_ip() -> str:
            return "123.456.78.99"

        get_host_ip_mocker = mocker.MagicMock(side_effect=get_host_ip)
        return get_host_ip_mocker

    @pytest.fixture
    def create(self, mocker: pytest_mock.MockFixture, get_ex_em_env: EmulationEnvConfig):
        """
        Pytest fixture for mocking the create_execution function

        :param mocker: the pytest mocker object
        :param get_ex_em_env: fixture returning an example EmulationEnvConfig
        :return: the mocked function
        """

        def create_execution(emulation_env_config: EmulationEnvConfig,
                             physical_servers: List[str], logger: logging.Logger, id: int = -1) -> EmulationExecution:
            em_env = get_ex_em_env
            em_ex = EmulationExecution(emulation_name="JohbnDoeEmulation", timestamp=1.5, ip_first_octet=-1,
                                       emulation_env_config=em_env, physical_servers=["JohnDoeServer"])
            return em_ex

        create_execution_mocker = mocker.MagicMock(side_effect=create_execution)
        return create_execution_mocker

    @pytest.fixture
    def clean_ex(slef, mocker: pytest_mock.MockFixture):
        """
        pytest fixture for mocking the clean_execution function

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def clean_execution(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        clean_execution_mocker = mocker.MagicMock(side_effect=clean_execution)
        return clean_execution_mocker

    @pytest.fixture
    def get_em_ex(self, mocker: pytest_mock.MockFixture, get_ex_em_env: EmulationEnvConfig):
        """
        pytest fixture for mocking the get_emulation_execution function

        :param mocker: the pytest mocker object
        :param get_ex_em_env: fixture returning an example EmulationEnvConfig
        :return: the mocked function
        """

        def get_emulation_execution(ip_first_octet: int, emulation_name: str) -> EmulationExecution:
            em_env = get_ex_em_env
            em_ex = EmulationExecution(emulation_name="JohbnDoeEmulation", timestamp=1.5, ip_first_octet=-1,
                                       emulation_env_config=em_env, physical_servers=["JohnDoeServer"])
            return em_ex

        get_emulation_execution_mocker = mocker.MagicMock(side_effect=get_emulation_execution)
        return get_emulation_execution_mocker

    @pytest.fixture
    def run(self, mocker: pytest_mock.MockFixture):
        """
        pytest fixture for mocking the run_emulation function

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def run_emulation(execution: EmulationExecution, no_traffic: bool,
                          no_clients: bool, physical_servers: List[str]) -> None:
            return None

        run_emulation_mocker = mocker.MagicMock(side_effect=run_emulation)
        return run_emulation_mocker

    @pytest.fixture
    def execution_time(self, mocker: pytest_mock.MockFixture, get_ex_e_m_time: EmulationMetricsTimeSeries):
        """
        pytest fixture for mocking the get_execution_time_series_data function

        :param mocker: the pytest mocker object
        :param get_ex_e_m_time: fixture returning an example EmulationMetricsTimeSeries
        :return: the mocked function
        """

        def get_execution_time_series_data(ip: str, port: int, minutes: int,
                                           ip_first_octet: int, emulation: str) -> EmulationMetricsTimeSeries:
            return get_ex_e_m_time

        get_execution_time_series_data_mocker = mocker.MagicMock(side_effect=get_execution_time_series_data)
        return get_execution_time_series_data_mocker

    @pytest.fixture
    def emulations_ids_not_in_names(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_emulations_ids function

        :param mocker: the pytest mocker object
        :return: The mocked function
        """

        def list_emulations_ids() -> List[Tuple[int, str]]:
            list_tuple = [(10, "q")]
            return list_tuple

        list_emulations_ids_mocker = mocker.MagicMock(side_effect=list_emulations_ids
                                                      )
        return list_emulations_ids_mocker

    @pytest.fixture
    def get_ex_e_m_time(self, get_ex_em_env: EmulationEnvConfig) -> EmulationMetricsTimeSeries:
        """
        Fixture that returns an example EmulationMetricsTimeSeries object

        :param get_ex_em_env: fixture returning an example EmulationEnvConfig
        :return: an example EmulationMetricsTimeSeries object
        """
        c_p_metrics = ClientPopulationMetrics(ip="123.456.78.99", ts=10.5,
                                              num_clients=5, rate=20.5,
                                              service_time=4.5)
        d_stats = DockerStats(pids=1.0, timestamp="null", cpu_percent=1.0, mem_current=2.0,
                              mem_total=2.0, mem_percent=3.0, blk_read=4.0, blk_write=5.0,
                              net_rx=6.0, net_tx=7.0, container_name="JohnDoe",
                              ip="123.456.78.99", ts=8.0)
        h_metrics = HostMetrics(num_logged_in_users=10, num_failed_login_attempts=2,
                                num_open_connections=5, num_login_events=20,
                                num_processes=30, num_users=5,
                                ip="123.456.78.99", ts=1.0)
        e_d_action = EmulationDefenderAction(id=EmulationDefenderActionId.STOP,
                                             name="JohnDoe", cmds=["JohnDoeCommands"],
                                             type=EmulationDefenderActionType.STOP,
                                             descr="null", ips=["123.456.78.99"], index=10,
                                             action_outcome=EmulationDefenderActionOutcome.GAME_END,
                                             alt_cmds=["altCommands"],
                                             execution_time=10.0,
                                             ts=5.0)
        s_ids = SnortIdsAlertCounters()
        e_a_action = EmulationAttackerAction(id=EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST,
                                             name="JohnDoe",
                                             cmds=["JohnDoeCommands"],
                                             type=EmulationAttackerActionType.RECON, descr="null",
                                             ips=["null"], index=10,
                                             action_outcome=EmulationAttackerActionOutcome.INFORMATION_GATHERING,
                                             vulnerability="null", alt_cmds=["null"], backdoor=False,
                                             execution_time=0.0, ts=1.1)
        em_env = get_ex_em_env
        ossec_ids = OSSECIdsAlertCounters()
        flow_stat = FlowStatistic(timestamp=1.0, datapath_id="path_id",
                                  in_port="null", out_port="null", dst_mac_address="null",
                                  num_packets=5, num_bytes=5, duration_nanoseconds=5,
                                  duration_seconds=5, hard_timeout=5,
                                  idle_timeout=5, priority=5, cookie=5)
        port_stat = PortStatistic(timestamp=1.0, datapath_id="null", port=5, num_received_packets=5,
                                  num_received_bytes=5, num_received_errors=5,
                                  num_transmitted_packets=5, num_transmitted_bytes=5,
                                  num_transmitted_errors=5, num_received_dropped=5,
                                  num_transmitted_dropped=5, num_received_frame_errors=5,
                                  num_received_overrun_errors=5, num_received_crc_errors=5,
                                  num_collisions=5, duration_nanoseconds=5, duration_seconds=5)
        avg_flow = AvgFlowStatistic(timestamp=100.0, datapath_id="null",
                                    total_num_packets=10, total_num_bytes=10,
                                    avg_duration_nanoseconds=10, avg_duration_seconds=5,
                                    avg_hard_timeout=10, avg_idle_timeout=10, avg_priority=5, avg_cookie=5)
        avg_port = AvgPortStatistic(timestamp=10.0, datapath_id="null",
                                    total_num_received_packets=10, total_num_received_bytes=4,
                                    total_num_received_errors=4, total_num_transmitted_packets=4,
                                    total_num_transmitted_bytes=4, total_num_transmitted_errors=40,
                                    total_num_received_dropped=40, total_num_transmitted_dropped=40,
                                    total_num_received_frame_errors=10, total_num_received_overrun_errors=15,
                                    total_num_received_crc_errors=14, total_num_collisions=12,
                                    avg_duration_nanoseconds=11, avg_duration_seconds=9)
        agg_flow_stat = AggFlowStatistic(timestamp=10.0, datapath_id="null", total_num_packets=10,
                                         total_num_bytes=5,
                                         total_num_flows=5)
        e_m_time_s = EmulationMetricsTimeSeries(client_metrics=[c_p_metrics],
                                                aggregated_docker_stats=[d_stats],
                                                docker_host_stats={"dockerstats": [d_stats]},
                                                host_metrics={"hostmetrics": [h_metrics]},
                                                aggregated_host_metrics=[h_metrics],
                                                defender_actions=[e_d_action],
                                                attacker_actions=[e_a_action],
                                                agg_snort_ids_metrics=[s_ids],
                                                emulation_env_config=em_env,
                                                ossec_host_alert_counters={"ossec_host": [ossec_ids]},
                                                aggregated_ossec_host_alert_counters=[ossec_ids],
                                                openflow_flow_stats=[flow_stat], openflow_port_stats=[port_stat],
                                                avg_openflow_flow_stats=[avg_flow],
                                                avg_openflow_port_stats=[avg_port],
                                                openflow_flow_metrics_per_switch={"flow_stat": [flow_stat]},
                                                openflow_port_metrics_per_switch={"port_stat": [port_stat]},
                                                openflow_flow_avg_metrics_per_switch={"avg_flow": [avg_flow]},
                                                openflow_port_avg_metrics_per_switch={"avg_port": [avg_port]},
                                                agg_openflow_flow_metrics_per_switch={"agg_flow": [agg_flow_stat]},
                                                agg_openflow_flow_stats=[agg_flow_stat],
                                                snort_ids_ip_metrics={"snort_ips": [SnortIdsIPAlertCounters()]},
                                                agg_snort_ids_rule_metrics=[SnortIdsRuleCounters()],
                                                snort_alert_metrics_per_ids={"snort_ids": [SnortIdsAlertCounters()]},
                                                snort_rule_metrics_per_ids={"snort_ids": [SnortIdsRuleCounters()]})
        return e_m_time_s

    def test_emulations_get(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                            logged_in_as_admin, config, emulations,
                            emulations_images, running_emulations, given_emulation, emulations_ids_not_in_names,
                            emulations_ids_in_names, get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Testing the HTTPS GET method for the /emulations resource
        
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param config: the config fixture
        :param emulations: the emulations fixture
        :param emulations_images: the emulations_images fixture
        :param running_emulations: the running_emulations fixture
        :param given_emulation: the given_emulation fixture
        :param emulations_ids_not_in_names: the emulations_ids_not_in_names fixture
        :param emulations_ids_in_names: the emulations_ids_in_names fixture
        :param get_ex_em_env: the get_ex_em_env fixture
        :return: None
        """
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulations_ids",
                     side_effect=emulations_ids_not_in_names)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config",
                     side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.list_all_running_emulations",
                     side_effect=running_emulations)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulations", side_effect=emulations)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulation_images",
                     side_effect=emulations_images)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "list_emulation_executions_for_a_given_emulation", side_effect=given_emulation)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        repsonse_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == "q"
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] is False
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 10
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulations_ids",
                     side_effect=emulations_ids_in_names)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        repsonse_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == "a"
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] is True
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 10
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        e_e_data = EmulationEnvConfig.from_dict(response_data_dict)
        test_em_env = get_ex_em_env
        test_em_env_dict = test_em_env.to_dict()
        problematic_ipc_type = e_e_data.traffic_config.client_population_config.workflows_config. \
            workflow_services[0].ips_and_commands[0]
        if isinstance(problematic_ipc_type, list):
            e_e_data.traffic_config.client_population_config.workflows_config.workflow_services[0].ips_and_commands[0] \
                = (problematic_ipc_type[0], problematic_ipc_type[1])
        e_e_data_dict = e_e_data.to_dict()
        for k in e_e_data_dict:
            assert e_e_data_dict[k] == test_em_env_dict[k]
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulations_ids",
                     side_effect=emulations_ids_not_in_names)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        repsonse_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == "q"
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] is False
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 10
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulations_ids",
                     side_effect=emulations_ids_in_names)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        repsonse_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == "a"
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] is True
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 10
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        e_e_data = EmulationEnvConfig.from_dict(response_data_dict)
        test_em_env = get_ex_em_env
        test_em_env_dict = test_em_env.to_dict()
        problematic_ipc_type = e_e_data.traffic_config.client_population_config.workflows_config. \
            workflow_services[0].ips_and_commands[0]
        if isinstance(problematic_ipc_type, list):
            e_e_data.traffic_config.client_population_config.workflows_config.workflow_services[0].ips_and_commands[0] \
                = (problematic_ipc_type[0], problematic_ipc_type[1])
        e_e_data_dict = e_e_data.to_dict()
        for k in e_e_data_dict:
            assert e_e_data_dict[k] == test_em_env_dict[k]

    def test_emulations_delete(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                               logged_in_as_admin, config, emulations, emulations_images, running_emulations,
                               given_emulation, uninstall,
                               clean, emulations_ids_not_in_names, emulations_ids_in_names) -> None:
        """
        Testing the HTTPS GET method for the /emulations resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in_fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param config: the config fixture
        :param emulations: the emulations fixture
        :param emulations_images: the emulations_images fixture
        :param running_emulations: the running_emulations fixture
        :param given_emulation: the given_emulation fixture
        :param uninstall: the uninstall fixture
        :param clean: the clean fixture
        :param emulations_ids_not_in_names: the emulations_ids_not_in_names fixture
        :param emulations_ids_in_names: the emulations_ids_in_names fixture
        :return: None
        """
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulations_ids",
                     side_effect=emulations_ids_not_in_names)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.list_all_running_emulations",
                     side_effect=running_emulations)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulations", side_effect=emulations)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulation_images",
                     side_effect=emulations_images)
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController.uninstall_emulation",
                     side_effect=uninstall)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController."
                     "clean_all_executions_of_emulation", side_effect=clean)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "list_emulation_executions_for_a_given_emulation", side_effect=given_emulation)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}"
                                                  f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}"
                                                  f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}"
                                                  f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        repsonse_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == "q"
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] is False
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 10
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulations_ids",
                     side_effect=emulations_ids_in_names)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}"
                                                  f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        repsonse_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == "a"
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] is True
        assert repsonse_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 10
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response_data_list == []
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE

    def test_emulations_ids_get(self, mocker: pytest_mock.MockFixture, emulation_id, flask_app, not_logged_in,
                                logged_in, logged_in_as_admin, config, running_emulations, given_emulation,
                                get_em_im, get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Testing the HTTPS GET method for the /emulations/id resource

        :param mocker: the pytest mocker object
        :param emulation_id: the emulation_id fixture
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param config: the config fixture
        :param running_emulations: the running_emulations fixture
        :param given_emulation: the given_emulation fixture
        :param get_em_im: the get_em_im fixture
        :param get_ex_em_env: the get_ex_em_env fixtuer
        :return: None
        """
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation", side_effect=emulation_id)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.list_all_running_emulations",
                     side_effect=running_emulations)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "list_emulation_executions_for_a_given_emulation", side_effect=given_emulation)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_image",
                     side_effect=get_em_im)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        e_e_data = EmulationEnvConfig.from_dict(response_data_dict)
        test_em_env = get_ex_em_env
        test_em_env_dict = test_em_env.to_dict()
        problematic_ipc_type = e_e_data.traffic_config.client_population_config.workflows_config. \
            workflow_services[0].ips_and_commands[0]
        if isinstance(problematic_ipc_type, list):
            e_e_data.traffic_config.client_population_config.workflows_config. \
                workflow_services[0].ips_and_commands[0] = (problematic_ipc_type[0],
                                                            problematic_ipc_type[1])
        e_e_data_dict = e_e_data.to_dict()
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for k in e_e_data_dict:
            assert e_e_data_dict[k] == test_em_env_dict[k]
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        e_e_data = EmulationEnvConfig.from_dict(response_data_dict)
        test_em_env = get_ex_em_env
        test_em_env_dict = test_em_env.to_dict()
        problematic_ipc_type = e_e_data.traffic_config.client_population_config.workflows_config. \
            workflow_services[0].ips_and_commands[0]
        if isinstance(problematic_ipc_type, list):
            e_e_data.traffic_config.client_population_config.workflows_config.workflow_services[0].ips_and_commands[0] \
                = (problematic_ipc_type[0], problematic_ipc_type[1])
        e_e_data_dict = e_e_data.to_dict()
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for k in e_e_data_dict:
            assert e_e_data_dict[k] == test_em_env_dict[k]

    def test_emulations_ids_delete(self, mocker: pytest_mock.MockFixture, emulation_id, flask_app,
                                   not_logged_in, logged_in, logged_in_as_admin, config, running_emulations,
                                   given_emulation, get_em_im, clean, uninstall) -> None:
        """
        Testing the HTTPS DELETE method for the /emulations/id resource

        :param mocker: the pytest mocker object
        :param emulation_id: the emulation_id fixture
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param config: the config fixture
        :param running_emulations: the running_emulations fixture
        :param given_emulation: the given_emulation fixture
        :param get_em_im: the get_em_im fixture
        :param clean: the clean fixture
        :param uninstall: the uninstall fixture
        :return:
        """
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation", side_effect=emulation_id)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.list_all_running_emulations",
                     side_effect=running_emulations)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "list_emulation_executions_for_a_given_emulation", side_effect=given_emulation)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_image",
                     side_effect=get_em_im)
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController.uninstall_emulation",
                     side_effect=uninstall)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController."
                     "clean_all_executions_of_emulation", side_effect=clean)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE

    def test_emulations_ids_post(self, mocker: pytest_mock.MockFixture, emulation_id, flask_app, not_logged_in,
                                 logged_in, logged_in_as_admin, config, running_emulations, given_emulation,
                                 get_em_im, run, host, clean, create, get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Testing the HTTPS POST method for the /emulations/id resource

        :param mocker: the pytest mocker object
        :param emulation_id: the emulation_id fixture
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param config: the config fixture
        :param running_emulations: the running_emulations fixture
        :param given_emulation: the given_emulation fixture
        :param get_em_im: the get_em_im fixture
        :param run: the run fixture
        :param host: the host fixture
        :param clean: the clean fixture
        :param create: the create fixture
        :param get_ex_em_env: the get_ex_em_env fixture
        :return: None
        """
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation", side_effect=emulation_id)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.list_all_running_emulations",
                     side_effect=running_emulations)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "list_emulation_executions_for_a_given_emulation", side_effect=given_emulation)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_image",
                     side_effect=get_em_im)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController."
                     "clean_all_executions_of_emulation", side_effect=clean)
        mocker.patch("csle_common.util.general_util.GeneralUtil.get_host_ip", side_effect=host)
        mocker.patch("csle_common.controllers.emulation_env_controller.EmulationEnvController.create_execution",
                     side_effect=create)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.run_emulation", side_effect=run)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        e_e_data = EmulationEnvConfig.from_dict(response_data_dict)
        test_em_env = get_ex_em_env
        test_em_env_dict = test_em_env.to_dict()
        problematic_ipc_type = e_e_data.traffic_config.client_population_config.workflows_config. \
            workflow_services[0].ips_and_commands[0]
        if isinstance(problematic_ipc_type, list):
            e_e_data.traffic_config.client_population_config.workflows_config. \
                workflow_services[0].ips_and_commands[0] = (problematic_ipc_type[0], problematic_ipc_type[1])
        e_e_data_dict = e_e_data.to_dict()
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for k in e_e_data_dict:
            if k != api_constants.MGMT_WEBAPP.RUNNING_PROPERTY:
                assert e_e_data_dict[k] == test_em_env_dict[k]

    def test_em_ex_ids_get(self, mocker: pytest_mock.MockFixture, emulation_id, flask_app, not_logged_in, logged_in,
                           logged_in_as_admin, config, given_emulation, get_ex_exec: EmulationExecution) -> None:
        """
        Testing the HTTPS GET method for the /emulations/id/executions resource

        :param mocker: the pytest mocker object
        :param emulation_id: the emulation_id fixture
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param config: the config fixture
        :param given_emulation: the given_emulation fixture
        :param get_ex_exec: the get_ex_exec fixture
        :return: None
        """
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation", side_effect=emulation_id)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "list_emulation_executions_for_a_given_emulation", side_effect=given_emulation)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}/10"
                                               f"{constants.COMMANDS.SLASH_DELIM}"
                                               f"{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}"
                                               f"{constants.COMMANDS.SLASH_DELIM}10"
                                               f"{constants.COMMANDS.SLASH_DELIM}"
                                               f"{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}")
        response_data = response.data.decode("utf-8")
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        response_data_dicts = json.loads(response_data)
        e_e_datas = list(map(lambda x: EmulationExecution.from_dict(x), response_data_dicts))
        for e_e_data in e_e_datas:
            test_exec = get_ex_exec
            test_exec_dict = test_exec.to_dict()
            problematic_ipc_type = e_e_data.emulation_env_config.traffic_config.client_population_config. \
                workflows_config.workflow_services[0].ips_and_commands[0]
            if isinstance(problematic_ipc_type, list):
                e_e_data.emulation_env_config.traffic_config.client_population_config.workflows_config. \
                    workflow_services[0].ips_and_commands[0] = (problematic_ipc_type[0], problematic_ipc_type[1])
            e_e_data_dict = e_e_data.to_dict()
            for k in e_e_data_dict:
                assert e_e_data_dict[k] == test_exec_dict[k]

        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}"
                                               f"{constants.COMMANDS.SLASH_DELIM}10"
                                               f"{constants.COMMANDS.SLASH_DELIM}"
                                               f"{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}")
        response_data = response.data.decode("utf-8")
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        response_data_dicts = json.loads(response_data)
        e_e_datas = list(map(lambda x: EmulationExecution.from_dict(x), response_data_dicts))
        for e_e_data in e_e_datas:
            test_exec = get_ex_exec
            test_exec_dict = test_exec.to_dict()
            problematic_ipc_type = \
                e_e_data.emulation_env_config.traffic_config.client_population_config.workflows_config. \
                workflow_services[0].ips_and_commands[0]
            if isinstance(problematic_ipc_type, list):
                e_e_data.emulation_env_config.traffic_config.client_population_config.workflows_config. \
                    workflow_services[0].ips_and_commands[0] = (problematic_ipc_type[0], problematic_ipc_type[1])
            e_e_data_dict = e_e_data.to_dict()
            for k in e_e_data_dict:
                assert e_e_data_dict[k] == test_exec_dict[k]

    def test_em_ex_ids_id_get(self, mocker: pytest_mock.MockFixture, emulation_id, flask_app, not_logged_in, logged_in,
                              logged_in_as_admin, config, given_emulation, get_em_ex, clean_ex,
                              get_ex_exec: EmulationExecution) -> None:
        """
        Testing the HTTPS GET method for the /emulations/id/executions/id resource

        :param mocker: the pytest mocker object
        :param emulation_id: the emulation_id fixture
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param config: the config fixture
        :param given_emulation: the given_emulation fixture
        :param get_em_ex: the get_em_ex fixture
        :param clean_ex: the clean_ex fixture
        :param get_ex_exec: the get_ex_exec fixture
        :return: None
        """
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation", side_effect=emulation_id)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "list_emulation_executions_for_a_given_emulation", side_effect=given_emulation)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.clean_execution",
                     side_effect=clean_ex)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}/10"
                                               f"{constants.COMMANDS.SLASH_DELIM}"
                                               f"{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}/11")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}/10"
                                               f"{constants.COMMANDS.SLASH_DELIM}"
                                               f"{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}/11")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        e_e_data = EmulationExecution.from_dict(response_data_dict)
        test_exec = get_ex_exec
        test_exec_dict = test_exec.to_dict()
        problematic_ipc_type = e_e_data.emulation_env_config.traffic_config.client_population_config.workflows_config. \
            workflow_services[0].ips_and_commands[0]
        if isinstance(problematic_ipc_type, list):
            e_e_data.emulation_env_config.traffic_config.client_population_config.workflows_config. \
                workflow_services[0].ips_and_commands[0] = (problematic_ipc_type[0], problematic_ipc_type[1])
        e_e_data_dict = e_e_data.to_dict()
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for k in e_e_data_dict:
            assert e_e_data_dict[k] == test_exec_dict[k]

    def test_em_ex_ids_id_delete(self, mocker: pytest_mock.MockFixture, emulation_id, flask_app, not_logged_in,
                                 logged_in, logged_in_as_admin, config, given_emulation, get_em_ex, clean_ex) -> None:
        """
        Testing the HTTPS DELETE method for the /emulations/id/executions/id resource

        :param mocker: the pytest mocker object
        :param emulation_id: the emulation_id fixture
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param config: the config fixtuire
        :param given_emulation: the given_emulation fixture
        :param get_em_ex: the get_em_ex fixture
        :param clean_ex: the clean_ex fixture
        :return: None
        """
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation", side_effect=emulation_id)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "list_emulation_executions_for_a_given_emulation", side_effect=given_emulation)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.clean_execution",
                     side_effect=clean_ex)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}/10"
                                                  f"{constants.COMMANDS.SLASH_DELIM}"
                                                  f"{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}/11")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}/10"
                                                  f"{constants.COMMANDS.SLASH_DELIM}"
                                                  f"{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}/11")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}/10"
                                                  f"{constants.COMMANDS.SLASH_DELIM}"
                                                  f"{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}/11")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict == {}

    def test_em_ex_monitor(self, mocker: pytest_mock.MockFixture, emulation_id, flask_app, not_logged_in, logged_in,
                           logged_in_as_admin, config, given_emulation, get_em_ex, clean_ex, execution_time,
                           get_ex_e_m_time: EmulationMetricsTimeSeries) -> None:
        """
        Testing the HTTPS GET method for the /emulations/id/executions/id/monitor/minutes resource

        :param mocker: the pytest mocker object
        :param emulation_id: the emulation_id fixture
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param config: the config fixture
        :param given_emulation: the given_emulation fixture
        :param get_em_ex: the get_em_ex fixture
        :param clean_ex: the clean_ex fixture
        :param execution_time: the execution_time fixture
        :param get_ex_e_m_time: the get_ex_e_m_time fixture
        :return: None
        """
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation", side_effect=emulation_id)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "list_emulation_executions_for_a_given_emulation", side_effect=given_emulation)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.clean_execution",
                     side_effect=clean_ex)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_execution_time_series_data",
                     side_effect=execution_time)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}/10"
                                               f"{constants.COMMANDS.SLASH_DELIM}"
                                               f"{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}/11"
                                               f"{constants.COMMANDS.SLASH_DELIM}"
                                               f"{api_constants.MGMT_WEBAPP.MONITOR_SUBRESOURCE}/12")

        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}/10"
                                               f"{constants.COMMANDS.SLASH_DELIM}"
                                               f"{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}/11"
                                               f"{constants.COMMANDS.SLASH_DELIM}"
                                               f"{api_constants.MGMT_WEBAPP.MONITOR_SUBRESOURCE}/12")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        data = EmulationMetricsTimeSeries.from_dict(response_data_dict)
        final_data_dict = data.to_dict()
        test_data = get_ex_e_m_time
        test_dict = test_data.to_dict()
        for k in final_data_dict:
            assert final_data_dict[k] == test_dict[k]
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATIONS_RESOURCE}/10"
                                               f"{constants.COMMANDS.SLASH_DELIM}"
                                               f"{api_constants.MGMT_WEBAPP.EXECUTIONS_SUBRESOURCE}/11"
                                               f"{constants.COMMANDS.SLASH_DELIM}"
                                               f"{api_constants.MGMT_WEBAPP.MONITOR_SUBRESOURCE}/12")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        data = EmulationMetricsTimeSeries.from_dict(response_data_dict)
        final_data_dict = data.to_dict()
        test_data = get_ex_e_m_time
        test_dict = test_data.to_dict()
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for k in final_data_dict:
            assert final_data_dict[k] == test_dict[k]
