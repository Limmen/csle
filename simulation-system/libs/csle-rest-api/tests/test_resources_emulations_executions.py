import json
import logging
from typing import List, Tuple

import csle_common.constants.constants as constants
import google
import pytest
import pytest_mock
from csle_cluster.cluster_manager.cluster_manager_pb2 import (
    ClientManagersInfoDTO,
    DockerContainerDTO,
    DockerNetworksDTO,
    DockerStatsManagersInfoDTO,
    DockerStatsMonitorStatusDTO,
    ElkManagersInfoDTO,
    ElkStatusDTO,
    ExecutionInfoDTO,
    GetNumClientsDTO,
    HostManagersInfoDTO,
    HostManagerStatusDTO,
    KafkaManagersInfoDTO,
    KafkaStatusDTO,
    KibanaTunnelDTO,
    KibanaTunnelsDTO,
    OperationOutcomeDTO,
    OSSECIdsManagersInfoDTO,
    OSSECIdsStatusDTO,
    RunningContainersDTO,
    RunningEmulationsDTO,
    RyuManagersInfoDTO,
    RyuManagerStatusDTO,
    RyuTunnelDTO,
    RyuTunnelsDTO,
    SnortIdsManagersInfoDTO,
    SnortIdsStatusDTO,
    StoppedContainersDTO,
    TrafficManagerInfoDTO,
    TrafficManagersInfoDTO,
)
from csle_common.dao.emulation_config.config import Config
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.emulation_execution import EmulationExecution

import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app

logger = logging.getLogger()


class TestResourcesEmulationExecutionsSuite:
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
    def emulation_exec(self, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution):
        """
        Pytest fixture for mocking the list_emulation_executions function

        :param mocker: the pytest mocker object
        :param get_ex_em_env: fixture returning an example EmulationEnvConfig
        :return: the mocked function
        """

        def list_emulation_executions() -> List[EmulationExecution]:
            em_ex = get_ex_exec
            return [em_ex]

        list_emulation_executions_mocker = mocker.MagicMock(side_effect=list_emulation_executions)
        return list_emulation_executions_mocker

    @pytest.fixture
    def start_client_mng(self, mocker):
        """
        Pytest fixture for mocking the start_client_manager method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def start_client_manager(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)
        start_client_manager_mocker = mocker.MagicMock(side_effect=start_client_manager)
        return start_client_manager_mocker

    @pytest.fixture
    def start_client_pop(self, mocker):
        """
        Pytest fixture for mocking the start_client_population method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def start_client_population(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)
        start_client_population_mocker = mocker.MagicMock(side_effect=start_client_population)
        return start_client_population_mocker

    @pytest.fixture
    def stop_client_pop(self, mocker):
        """
        Pytest fixture for mocking the stop_client_population method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def stop_client_population(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)
        stop_client_population_mocker = mocker.MagicMock(side_effect=stop_client_population)
        return stop_client_population_mocker

    @pytest.fixture
    def stop_client_mng(self, mocker):
        """
        Pytest fixture for mocking the stop_client_manager method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def stop_client_manager(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)
        stop_client_manager_mocker = mocker.MagicMock(side_effect=stop_client_manager)
        return stop_client_manager_mocker

    @pytest.fixture
    def stop_kafka(self, mocker):
        """
        Pytest fixture for mocking the stop_kafka_client_producer method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def stop_kafka_client_producer(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)
        stop_kafka_client_producer_mocker = mocker.MagicMock(side_effect=stop_kafka_client_producer)
        return stop_kafka_client_producer_mocker
    
    @pytest.fixture
    def start_kafka(self, mocker):
        """
        Pytest fixture for mocking the start_kafka_client_producer method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def start_kafka_client_producer(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)
        start_kafka_client_producer_mocker = mocker.MagicMock(side_effect=start_kafka_client_producer)
        return start_kafka_client_producer_mocker

    @pytest.fixture
    def start_dcm(self, mocker):
        """
        Pytest fixture for mocking the start_docker_statsmanager method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def start_docker_statsmanager(ip: str, port: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)
        start_docker_statsmanager_mocker = mocker.MagicMock(side_effect=start_docker_statsmanager)
        return start_docker_statsmanager_mocker

    @pytest.fixture
    def stop_dcm(self, mocker):
        """
        Pytest fixture for mocking the stop_docker_statsmanager method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def stop_docker_statsmanager(ip: str, port: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)
        stop_docker_statsmanager_mocker = mocker.MagicMock(side_effect=stop_docker_statsmanager)
        return stop_docker_statsmanager_mocker

    @pytest.fixture
    def start_dcm_thread(self, mocker):
        """
        Pytest fixture for mocking the start_docker_statsmanager method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def start_docker_statsmanager_thread(ip: str, port: int, 
                                             emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)
        start_docker_statsmanager_thread_mocker = mocker.MagicMock(side_effect=start_docker_statsmanager_thread)
        return start_docker_statsmanager_thread_mocker

    @pytest.fixture
    def stop_dcm_thread(self, mocker):
        """
        Pytest fixture for mocking the start_docker_statsmanager method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def stop_docker_statsmanager_thread(ip: str, port: int,
                                            emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)
        stop_docker_statsmanager_thread_mocker = mocker.MagicMock(side_effect=stop_docker_statsmanager_thread)
        return stop_docker_statsmanager_thread_mocker

    @pytest.fixture
    def stop_kafka_mng(self, mocker):
        """
        Pytest fixture for mocking the stop_kafka_manager method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def stop_kafka_manager(ip: str, port: int,
                               emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)
        stop_kafka_manager_mocker = mocker.MagicMock(side_effect=stop_kafka_manager)
        return stop_kafka_manager_mocker

    @pytest.fixture
    def start_kafka_mng(self, mocker):
        """
        Pytest fixture for mocking the start_kafka_manager method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def start_kafka_manager(ip: str, port: int,
                                emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)
        start_kafka_manager_mocker = mocker.MagicMock(side_effect=start_kafka_manager)
        return start_kafka_manager_mocker

    @pytest.fixture
    def start_kafka_srv(self, mocker):
        """
        Pytest fixture for mocking the start_kafka_server method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def start_kafka_server(ip: str, port: int,
                               emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)
        start_kafka_server_mocker = mocker.MagicMock(side_effect=start_kafka_server)
        return start_kafka_server_mocker

    @pytest.fixture
    def stop_kafka_srv(self, mocker):
        """
        Pytest fixture for mocking the stop_kafka_server method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def stop_kafka_server(ip: str, port: int,
                              emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)
        stop_kafka_server_mocker = mocker.MagicMock(side_effect=stop_kafka_server)
        return stop_kafka_server_mocker

    @pytest.fixture
    def stop_snort_ids_mng(self, mocker):
        """
        Pytest fixture for mocking the stop_snort_ids_managers method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def stop_snort_ids_managers(ip: str, port: int,
                                    emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)
        stop_snort_ids_managers_mocker = mocker.MagicMock(side_effect=stop_snort_ids_managers)
        return stop_snort_ids_managers_mocker

    @pytest.fixture
    def start_snort_ids_mng(self, mocker):
        """
        Pytest fixture for mocking the start_snort_ids_managers method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def start_snort_ids_managers(ip: str, port: int,
                                     emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)
        start_snort_ids_managers_mocker = mocker.MagicMock(side_effect=start_snort_ids_managers)
        return start_snort_ids_managers_mocker

    @pytest.fixture
    def start_snort(self, mocker):
        """
        Pytest fixture for mocking the start_snort_idses method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def start_snort_idses(ip: str, port: int,
                              emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)
        start_snort_idses_mocker = mocker.MagicMock(side_effect=start_snort_idses)
        return start_snort_idses_mocker

    @pytest.fixture
    def stop_snort(self, mocker):
        """
        Pytest fixture for mocking the start_snort_idses method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def stop_snort_idses(ip: str, port: int,
                             emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)
        stop_snort_idses_mocker = mocker.MagicMock(side_effect=stop_snort_idses)
        return stop_snort_idses_mocker

    @pytest.fixture
    def stop_snort_mon(self, mocker):
        """
        Pytest fixture for mocking the stop_snort_ids_monitor_threads method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def stop_snort_ids_monitor_threads(ip: str, port: int,
                                           emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)
        stop_snort_ids_monitor_threads_mocker = mocker.MagicMock(side_effect=stop_snort_ids_monitor_threads)
        return stop_snort_ids_monitor_threads_mocker

    @pytest.fixture
    def start_snort_mon(self, mocker):
        """
        Pytest fixture for mocking the start_snort_ids_monitor_threads method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def start_snort_ids_monitor_threads(ip: str, port: int,
                                            emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)
        start_snort_ids_monitor_threads_mocker = mocker.MagicMock(side_effect=start_snort_ids_monitor_threads)
        return start_snort_ids_monitor_threads_mocker

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
    def kibana(self, mocker):
        """
        Pytest fixture for mocking the create_kibana_tunnel method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def create_kibana_tunnel(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)
        create_kibana_tunnel_mocker = mocker.MagicMock(side_effect=create_kibana_tunnel)
        return create_kibana_tunnel_mocker

    @pytest.fixture
    def kibana_list(self, mocker):
        """
        Pytest fixture for mocking the list_kibana_tunnels method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def list_kibana_tunnels(ip: str, port: int):
            kibana_tunnel = KibanaTunnelDTO(port=5, ip="123.456.78.99",
                                            emulation="null",
                                            ipFirstOctet=-1)
            return KibanaTunnelsDTO(tunnels=[kibana_tunnel])

        list_kibana_tunnels_mocker = mocker.MagicMock(side_effect=list_kibana_tunnels)
        return list_kibana_tunnels_mocker

    @pytest.fixture
    def merged_info(self, mocker):
        """
        Pytest fixture for mocking the get_merged_execution_info method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def get_merged_execution_info(execution: EmulationExecution) -> ExecutionInfoDTO:
            merged_exec_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
            return merged_exec_info

        get_merged_execution_info_mocker = mocker.MagicMock(side_effect=get_merged_execution_info)
        return get_merged_execution_info_mocker

    @pytest.fixture
    def create_ryu(self, mocker):
        """
        Pytest fixture for mocking the create_ryu_tunnel method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def create_ryu_tunnel(ip: str, port: int, emulation: str, ip_first_octet: int) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)
        create_ryu_tunnel_mocker = mocker.MagicMock(side_effect=create_ryu_tunnel)
        return create_ryu_tunnel_mocker

    @pytest.fixture
    def list_ryu(self, mocker):
        """
        Pytest fixture for mocking the list_ryu_tunnels method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def list_ryu_tunnels(ip: str, port: int) -> RyuTunnelsDTO:
            return RyuTunnelsDTO(tunnels=[RyuTunnelDTO(port=1,
                                                       ip="123.456.78.99",
                                                       emulation="null", ipFirstOctet=-1)])
        list_ryu_tunnels_mocker = mocker.MagicMock(side_effect=list_ryu_tunnels)
        return list_ryu_tunnels_mocker

    @pytest.fixture
    def emulation_exec_ids(self, mocker: pytest_mock.MockFixture, get_ex_exec: EmulationExecution):
        """
        Pytest fixture for mocking the list_emulation_execution_ids function

        :param mocker: the pytest mocker object
        :param get_ex_em_env: fixture returning an example EmulationEnvConfig
        :return: the mocked function
        """
        def list_emulation_execution_ids() -> List[Tuple[int, str]]:
            list_tuple = [(10, "a")]
            return list_tuple

        list_emulation_execution_ids_mocker = mocker.MagicMock(side_effect=list_emulation_execution_ids)
        return list_emulation_execution_ids_mocker

    @staticmethod
    def get_exec_info():
        """
        Static help method for returning an ExecutionInfoDTO
        :return: ExecutionInfoDTO
        """
        snort_ids = SnortIdsManagersInfoDTO(ips="abcdef", ports=[1, 2, 3, 4, 5], emulationName="abcdef",
                                            executionId=1,
                                            snortIdsManagersRunning=[False, True, False, True, False],
                                            snortIdsManagersStatuses=[SnortIdsStatusDTO(monitor_running=False,
                                                                                        snort_ids_running=True)])
        ossec_ids = OSSECIdsManagersInfoDTO(ips="123.456.78.99", ports=[1, 2, 3, 4, 5],
                                            emulationName="JohnDoe", executionId=4,
                                            ossecIdsManagersRunning=[True, False, True, False, True],
                                            ossecIdsManagersStatuses=[OSSECIdsStatusDTO(monitor_running=True,
                                                                                        ossec_ids_running=False)])
        kafka_mng = KafkaManagersInfoDTO(ips="123.456.78.99", ports=[1, 2, 3, 4, 5],
                                         emulationName="JohnDoe",
                                         executionId=1, kafkaManagersRunning=[True, False, True, False, True],
                                         kafkaManagersStatuses=[KafkaStatusDTO(running=True, topics="abcdef")])
        host_mng = HostManagersInfoDTO(ips="123.456.78.99", ports=[1, 2, 3, 4, 5],
                                       emulationName="JohnDoe",
                                       executionId=5,
                                       hostManagersRunning=[True, False, True, False, True],
                                       hostManagersStatuses=[HostManagerStatusDTO(monitor_running=True,
                                                                                  filebeat_running=True,
                                                                                  packetbeat_running=True,
                                                                                  metricbeat_running=True,
                                                                                  heartbeat_running=True,
                                                                                  ip="123.456.78.99")])
        client_mng = ClientManagersInfoDTO(ips="123.456.78.99",
                                           ports=[1, 2, 3, 4, 5],
                                           emulationName="JohnDoe",
                                           executionId=5,
                                           clientManagersRunning=[True, False, True, False, True],
                                           clientManagersStatuses=[
                                               GetNumClientsDTO(num_clients=1,
                                                                client_process_active=True,
                                                                producer_active=True,
                                                                clients_time_step_len_seconds=15,
                                                                producer_time_step_len_seconds=10)])
        docker_mng = DockerStatsManagersInfoDTO(ips="123.456.78.99", ports=[1, 2, 3, 4, 5],
                                                emulationName="JohnDoe",
                                                executionId=5,
                                                dockerStatsManagersRunning=[True, False, True, False, True],
                                                dockerStatsManagersStatuses=[
                                                    DockerStatsMonitorStatusDTO(num_monitors=1,
                                                                                emulations="null",
                                                                                emulation_executions=[1, 2, 3, 4, 5])])
        running_cont = RunningContainersDTO(runningContainers=[DockerContainerDTO(name="JohnDoe",
                                                                                  image="null",
                                                                                  ip="123.456.78.99")])
        stopped_cont = StoppedContainersDTO(stoppedContainers=[DockerContainerDTO(name="JohnDoe",
                                                                                  image="null",
                                                                                  ip="123.456.78.99")])
        traffic_info = TrafficManagersInfoDTO(ips="123..456.78.99",
                                              ports=[1, 2, 3, 4, 5],
                                              emulationName="JohnDoe",
                                              executionId=5,
                                              trafficManagersRunning=[True, False, True, False, True],
                                              trafficManagersStatuses=[TrafficManagerInfoDTO(running=True,
                                                                                             script="null")])
        docker_net = DockerNetworksDTO(networks="abcdef", network_ids=[1, 2, 3, 4, 5])
        elk_mng = ElkManagersInfoDTO(ips="123.456.78.99", ports=[1, 2, 3, 4, 5],
                                     emulationName="JohnDoe", executionId=5,
                                     elkManagersRunning=[True, False, True, False, True],
                                     elkManagersStatuses=[ElkStatusDTO(elasticRunning=True, kibanaRunning=True,
                                                                       logstashRunning=True)],
                                     localKibanaPort=5,
                                     physicalServerIp="123.456.78.99")
        ryu_mng = RyuManagersInfoDTO(ips="123.456.78.99", ports=[1, 2, 3, 4, 5],
                                     emulationName="JohnDoe", executionId=5,
                                     ryuManagersRunning=[True, False, True, False, True],
                                     ryuManagersStatuses=[RyuManagerStatusDTO(ryu_running=True,
                                                                              monitor_running=True,
                                                                              port=5, web_port=4,
                                                                              controller="null",
                                                                              kafka_ip="123.456.78.99",
                                                                              kafka_port=5, time_step_len=10)],
                                     localControllerWebPort=1, physicalServerIp="123.456.78.99")
        return ExecutionInfoDTO(emulationName="JohnDoe", executionId=-1,
                                snortIdsManagersInfo=snort_ids,
                                ossecIdsManagersInfo=ossec_ids,
                                kafkaManagersInfo=kafka_mng,
                                hostManagersInfo=host_mng, clientManagersInfo=client_mng,
                                dockerStatsManagersInfo=docker_mng,
                                runningContainers=running_cont,
                                stoppedContainers=stopped_cont,
                                trafficManagersInfoDTO=traffic_info,
                                activeNetworks=docker_net, elkManagersInfoDTO=elk_mng,
                                ryuManagersInfoDTO=ryu_mng)

    def test_emulation_executions_get(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                                      logged_in_as_admin, config, emulation_exec, emulation_exec_ids,
                                      running_emulations, get_ex_exec) -> None:
        """
        Testing the HTTPS GET method for the /emulation/executions resource
        
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
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config",
                     side_effect=config)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulation_executions",
                     side_effect=emulation_exec)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulation_execution_ids",
                     side_effect=emulation_exec_ids)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.list_all_running_emulations",
                     side_effect=running_emulations)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict[api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == "a"
        assert response_data_dict[api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] is True
        assert response_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 10
        ex_exec = get_ex_exec
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        e_e_data = EmulationExecution.from_dict(response_data_dict)
        e_e_data_dict = e_e_data.to_dict()
        ex_exec_dict = ex_exec.to_dict()
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for k in response_data_dict:
            assert e_e_data_dict[k] == ex_exec_dict[k]
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict[api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == "a"
        assert response_data_dict[api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] is True
        assert response_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 10
        ex_exec = get_ex_exec
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        e_e_data = EmulationExecution.from_dict(response_data_dict)
        e_e_data_dict = e_e_data.to_dict()
        ex_exec_dict = ex_exec.to_dict()
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for k in response_data_dict:
            assert e_e_data_dict[k] == ex_exec_dict[k]

    def test_emulation_execution_ids_get(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                                         logged_in_as_admin, get_em_ex, emulation_exec, get_ex_exec):
        """
        Testing the HTTPS GET method for the /emulation_executions/id resource
        
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
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulation_executions",
                     side_effect=emulation_exec)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1"
                                               f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        ex_exec = get_ex_exec
        ex_exec_dict = ex_exec.to_dict()
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)[0]
        e_e_data = EmulationExecution.from_dict(response_data_dict)
        e_e_data_dict = e_e_data.to_dict()
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for k in e_e_data_dict:
            assert e_e_data_dict[k] == ex_exec_dict[k]

        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1"
                                               f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        e_e_data = EmulationExecution.from_dict(response_data_dict)
        e_e_data_dict = e_e_data.to_dict()
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for k in e_e_data_dict:
            assert e_e_data_dict[k] == ex_exec_dict[k]
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)[0]
        e_e_data = EmulationExecution.from_dict(response_data_dict)
        e_e_data_dict = e_e_data.to_dict()
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for k in e_e_data_dict:
            assert e_e_data_dict[k] == ex_exec_dict[k]

        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1"
                                               f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        e_e_data = EmulationExecution.from_dict(response_data_dict)
        e_e_data_dict = e_e_data.to_dict()
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for k in e_e_data_dict:
            assert e_e_data_dict[k] == ex_exec_dict[k]

    def test_emulation_execution_ids_info_get(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                              logged_in, logged_in_as_admin, get_em_ex, emulation_exec, get_ex_exec,
                                              merged_info, kibana_list, kibana, create_ryu, list_ryu):
        """
        Testing the HTTPS GET method for the /emulation_executions/id/info resource
        
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
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.list_kibana_tunnels",
                     side_effect=kibana_list)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.create_kibana_tunnel",
                     side_effect=kibana)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.create_ryu_tunnel",
                     side_effect=create_ryu)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.list_ryu_tunnels",
                     side_effect=list_ryu)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                               f"{api_constants.MGMT_WEBAPP.INFO_SUBRESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                               f"{api_constants.MGMT_WEBAPP.INFO_SUBRESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                               f"{api_constants.MGMT_WEBAPP.INFO_SUBRESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = google.protobuf.json_format.MessageToDict(exp_ex_info,
                                                                       including_default_value_fields=False,
                                                                       preserving_proto_field_name=False,
                                                                       use_integers_for_enums=False,
                                                                       descriptor_pool=None, float_precision=None)
        for k in response_data_dict:
            assert response_data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                               f"{api_constants.MGMT_WEBAPP.INFO_SUBRESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                               f"{api_constants.MGMT_WEBAPP.INFO_SUBRESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                               f"{api_constants.MGMT_WEBAPP.INFO_SUBRESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = google.protobuf.json_format.MessageToDict(exp_ex_info,
                                                                       including_default_value_fields=False,
                                                                       preserving_proto_field_name=False,
                                                                       use_integers_for_enums=False,
                                                                       descriptor_pool=None, float_precision=None)
        for k in response_data_dict:
            assert response_data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                               f"{api_constants.MGMT_WEBAPP.INFO_SUBRESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_cm_post(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                             logged_in, logged_in_as_admin, get_em_ex,
                                             merged_info, get_ex_exec,
                                             start_client_mng, stop_client_mng):
        """
        Testing the HTTPS GET method for the /emulation-executions/id/client-manager resource
        
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param start_client: the start_client fixture
        :param stop_client: the stop_client fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_client_manager",
                     side_effect=stop_client_mng)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_client_manager",
                     side_effect=start_client_mng)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CLIENT_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CLIENT_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CLIENT_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {api_constants.MGMT_WEBAPP.REASON_PROPERTY:
                                      f"{api_constants.MGMT_WEBAPP.IP_PROPERTY} or "
                                      f"{api_constants.MGMT_WEBAPP.START_PROPERTY} or "
                                      f"{api_constants.MGMT_WEBAPP.STOP_PROPERTY} not provided"}
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CLIENT_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = google.protobuf.json_format.MessageToDict(exp_ex_info,
                                                                       including_default_value_fields=False,
                                                                       preserving_proto_field_name=False,
                                                                       use_integers_for_enums=False,
                                                                       descriptor_pool=None, float_precision=None)
        for k in response_data_dict:
            assert response_data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CLIENT_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE

    def test_emulation_execution_ids_cp_post(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                             logged_in, logged_in_as_admin, get_em_ex,
                                             merged_info, get_ex_exec,
                                             start_client_pop, stop_client_pop):
        """
        Testing the HTTPS GET method for the /emulation-executions/id/client-population resource
        
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param start_client_pop: the start_client_pop fixture
        :param stop_client_pop: the stop_client_pop fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_client_population",
                     side_effect=stop_client_pop)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_client_population",
                     side_effect=start_client_pop)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CLIENT_POPULATION_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CLIENT_POPULATION_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CLIENT_POPULATION_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {api_constants.MGMT_WEBAPP.REASON_PROPERTY:
                                      f"{api_constants.MGMT_WEBAPP.IP_PROPERTY} or "
                                      f"{api_constants.MGMT_WEBAPP.START_PROPERTY} or "
                                      f"{api_constants.MGMT_WEBAPP.STOP_PROPERTY} not provided"}
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CLIENT_POPULATION_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = google.protobuf.json_format.MessageToDict(exp_ex_info,
                                                                       including_default_value_fields=False,
                                                                       preserving_proto_field_name=False,
                                                                       use_integers_for_enums=False,
                                                                       descriptor_pool=None, float_precision=None)
        for k in response_data_dict:
            assert response_data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CLIENT_POPULATION_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_c_prod_post(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                                 logged_in, logged_in_as_admin, get_em_ex,
                                                 merged_info, start_kafka, stop_kafka):
        """
        Testing the HTTPS GET method for the /emulation-executions/id/client-producer resource
        
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param start_client_pop: the start_kafka fixture
        :param stop_client_pop: the stop_kafka fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_kafka_client_producer",
                     side_effect=stop_kafka)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_kafka_client_producer",
                     side_effect=start_kafka)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CLIENT_PRODUCER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CLIENT_PRODUCER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CLIENT_PRODUCER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {api_constants.MGMT_WEBAPP.REASON_PROPERTY:
                                      f"{api_constants.MGMT_WEBAPP.IP_PROPERTY} or "
                                      f"{api_constants.MGMT_WEBAPP.START_PROPERTY} or "
                                      f"{api_constants.MGMT_WEBAPP.STOP_PROPERTY} not provided"}
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CLIENT_PRODUCER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = google.protobuf.json_format.MessageToDict(exp_ex_info,
                                                                       including_default_value_fields=False,
                                                                       preserving_proto_field_name=False,
                                                                       use_integers_for_enums=False,
                                                                       descriptor_pool=None, float_precision=None)
        for k in response_data_dict:
            assert response_data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CLIENT_PRODUCER_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_dcm_post(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                              logged_in, logged_in_as_admin, get_em_ex,
                                              merged_info, start_dcm, stop_dcm):
        """
        Testing the HTTPS GET method for the /emulation-executions/id/docker-stats-manager resource
        
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param start_dcm: the start_dcm fixture
        :param stop_dcm: the stop_dcm fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_docker_statsmanager",
                     side_effect=stop_dcm)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_docker_statsmanager",
                     side_effect=start_dcm)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.DOCKER_STATS_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.DOCKER_STATS_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.DOCKER_STATS_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {api_constants.MGMT_WEBAPP.REASON_PROPERTY:
                                      f"{api_constants.MGMT_WEBAPP.IP_PROPERTY} or "
                                      f"{api_constants.MGMT_WEBAPP.START_PROPERTY} or "
                                      f"{api_constants.MGMT_WEBAPP.STOP_PROPERTY} not provided"}
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.DOCKER_STATS_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = google.protobuf.json_format.MessageToDict(exp_ex_info,
                                                                       including_default_value_fields=False,
                                                                       preserving_proto_field_name=False,
                                                                       use_integers_for_enums=False,
                                                                       descriptor_pool=None, float_precision=None)
        for k in response_data_dict:
            assert response_data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.DOCKER_STATS_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = google.protobuf.json_format.MessageToDict(exp_ex_info,
                                                                       including_default_value_fields=False,
                                                                       preserving_proto_field_name=False,
                                                                       use_integers_for_enums=False,
                                                                       descriptor_pool=None, float_precision=None)
        for k in response_data_dict:
            assert response_data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.DOCKER_STATS_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_dc_mon_post(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                                 logged_in, logged_in_as_admin, get_em_ex,
                                                 merged_info, start_dcm_thread, stop_dcm_thread, config):
        """
        Testing the HTTPS GET method for the /emulation-executions/id/docker-stats-monitor resource
        
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param start_cdm_thread: the start_dcm_thread fixture
        :param stop_dcm_thread: the stop_dcm_thread fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config",
                     side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController."
                     "stop_docker_statsmanager_thread",
                     side_effect=stop_dcm_thread)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController."
                     "start_docker_statsmanager_thread",
                     side_effect=start_dcm_thread)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.DOCKER_STATS_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.DOCKER_STATS_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.DOCKER_STATS_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {api_constants.MGMT_WEBAPP.REASON_PROPERTY:
                                      f"{api_constants.MGMT_WEBAPP.IP_PROPERTY} or "
                                      f"{api_constants.MGMT_WEBAPP.START_PROPERTY} or "
                                      f"{api_constants.MGMT_WEBAPP.STOP_PROPERTY} not provided"}
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.DOCKER_STATS_MONITOR_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = google.protobuf.json_format.MessageToDict(exp_ex_info,
                                                                       including_default_value_fields=False,
                                                                       preserving_proto_field_name=False,
                                                                       use_integers_for_enums=False,
                                                                       descriptor_pool=None, float_precision=None)
        for k in response_data_dict:
            assert response_data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.DOCKER_STATS_MONITOR_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = google.protobuf.json_format.MessageToDict(exp_ex_info,
                                                                       including_default_value_fields=False,
                                                                       preserving_proto_field_name=False,
                                                                       use_integers_for_enums=False,
                                                                       descriptor_pool=None, float_precision=None)
        for k in response_data_dict:
            assert response_data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.DOCKER_STATS_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_kafka_mng_post(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                                    logged_in, logged_in_as_admin, get_em_ex,
                                                    merged_info, start_kafka_mng, stop_kafka_mng):
        """
        Testing the HTTPS GET method for the /emulation-executions/id/kafka-manager resource
        
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param start_kafka_mng: the start_kafka_mng fixture
        :param stop_kafka_mng: the stop_kafka_mng fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController."
                     "stop_kafka_manager",
                     side_effect=stop_kafka_mng)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController."
                     "start_kafka_manager",
                     side_effect=start_kafka_mng)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KAFKA_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KAFKA_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KAFKA_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {api_constants.MGMT_WEBAPP.REASON_PROPERTY:
                                      f"{api_constants.MGMT_WEBAPP.IP_PROPERTY} or "
                                      f"{api_constants.MGMT_WEBAPP.START_PROPERTY} or "
                                      f"{api_constants.MGMT_WEBAPP.STOP_PROPERTY} not provided"}
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KAFKA_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = google.protobuf.json_format.MessageToDict(exp_ex_info,
                                                                       including_default_value_fields=False,
                                                                       preserving_proto_field_name=False,
                                                                       use_integers_for_enums=False,
                                                                       descriptor_pool=None, float_precision=None)
        for k in response_data_dict:
            assert response_data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KAFKA_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = google.protobuf.json_format.MessageToDict(exp_ex_info,
                                                                       including_default_value_fields=False,
                                                                       preserving_proto_field_name=False,
                                                                       use_integers_for_enums=False,
                                                                       descriptor_pool=None, float_precision=None)
        for k in response_data_dict:
            assert response_data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KAFKA_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_kafka_post(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                                logged_in, logged_in_as_admin, get_em_ex,
                                                merged_info, start_kafka_srv, stop_kafka_srv):
        """
        Testing the HTTPS GET method for the /emulation-executions/id/kafka resource
        
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param start_kafka_mng: the start_kafka_mng fixture
        :param stop_kafka_mng: the stop_kafka_mng fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController."
                     "stop_kafka_server",
                     side_effect=stop_kafka_srv)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController."
                     "start_kafka_server",
                     side_effect=start_kafka_srv)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KAFKA_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KAFKA_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KAFKA_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {api_constants.MGMT_WEBAPP.REASON_PROPERTY:
                                      f"{api_constants.MGMT_WEBAPP.IP_PROPERTY} or "
                                      f"{api_constants.MGMT_WEBAPP.START_PROPERTY} or "
                                      f"{api_constants.MGMT_WEBAPP.STOP_PROPERTY} not provided"}
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KAFKA_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = google.protobuf.json_format.MessageToDict(exp_ex_info,
                                                                       including_default_value_fields=False,
                                                                       preserving_proto_field_name=False,
                                                                       use_integers_for_enums=False,
                                                                       descriptor_pool=None, float_precision=None)
        for k in response_data_dict:
            assert response_data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KAFKA_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = google.protobuf.json_format.MessageToDict(exp_ex_info,
                                                                       including_default_value_fields=False,
                                                                       preserving_proto_field_name=False,
                                                                       use_integers_for_enums=False,
                                                                       descriptor_pool=None, float_precision=None)
        for k in response_data_dict:
            assert response_data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KAFKA_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_snort_mng(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                               logged_in, logged_in_as_admin, get_em_ex,
                                               merged_info, start_snort_ids_mng,
                                               stop_snort_ids_mng, config):
        """
        Testing the HTTPS GET method for the /emulation-executions/id/snort-ids-manager resource
        
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param start_snort_ids_mng: the start_snort_ids_mng fixture
        :param stop_snort_ids_mng: the stop_snort_ids_mng fixture
        :param config: the config fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config",
                     side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController."
                     "stop_snort_ids_managers",
                     side_effect=stop_snort_ids_mng)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController."
                     "start_snort_ids_managers",
                     side_effect=start_snort_ids_mng)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {api_constants.MGMT_WEBAPP.REASON_PROPERTY:
                                      f"{api_constants.MGMT_WEBAPP.IP_PROPERTY} or "
                                      f"{api_constants.MGMT_WEBAPP.START_PROPERTY} or "
                                      f"{api_constants.MGMT_WEBAPP.STOP_PROPERTY} not provided"}
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = google.protobuf.json_format.MessageToDict(exp_ex_info,
                                                                       including_default_value_fields=False,
                                                                       preserving_proto_field_name=False,
                                                                       use_integers_for_enums=False,
                                                                       descriptor_pool=None, float_precision=None)
        for k in response_data_dict:
            assert response_data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = google.protobuf.json_format.MessageToDict(exp_ex_info,
                                                                       including_default_value_fields=False,
                                                                       preserving_proto_field_name=False,
                                                                       use_integers_for_enums=False,
                                                                       descriptor_pool=None, float_precision=None)
        for k in response_data_dict:
            assert response_data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_snort(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                           logged_in, logged_in_as_admin, get_em_ex,
                                           merged_info, start_snort,
                                           stop_snort, config):
        """
        Testing the HTTPS GET method for the /emulation-executions/id/snort-ids resource
        
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param start_snort: the start_snort fixture
        :param stop_snort: the stop_snort fixture
        :param config: the config fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config",
                     side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController."
                     "stop_snort_idses",
                     side_effect=stop_snort)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController."
                     "start_snort_idses",
                     side_effect=start_snort)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {api_constants.MGMT_WEBAPP.REASON_PROPERTY:
                                      f"{api_constants.MGMT_WEBAPP.IP_PROPERTY} or "
                                      f"{api_constants.MGMT_WEBAPP.START_PROPERTY} or "
                                      f"{api_constants.MGMT_WEBAPP.STOP_PROPERTY} not provided"}
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = google.protobuf.json_format.MessageToDict(exp_ex_info,
                                                                       including_default_value_fields=False,
                                                                       preserving_proto_field_name=False,
                                                                       use_integers_for_enums=False,
                                                                       descriptor_pool=None, float_precision=None)
        for k in response_data_dict:
            assert response_data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = google.protobuf.json_format.MessageToDict(exp_ex_info,
                                                                       including_default_value_fields=False,
                                                                       preserving_proto_field_name=False,
                                                                       use_integers_for_enums=False,
                                                                       descriptor_pool=None, float_precision=None)
        for k in response_data_dict:
            assert response_data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_snort_mon(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                               logged_in, logged_in_as_admin, get_em_ex,
                                               merged_info, start_snort_mon,
                                               stop_snort_mon, config):
        """
        Testing the HTTPS GET method for the /emulation-executions/id/snort-ids-monitor resource
        
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param start_snort_mon: the start_snort_mon fixture
        :param stop_snort_mon: the stop_snort_mon fixture
        :param config: the config fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config",
                     side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController."
                     "stop_snort_ids_monitor_threads",
                     side_effect=stop_snort_mon)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController."
                     "start_snort_ids_monitor_threads",
                     side_effect=start_snort_mon)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {api_constants.MGMT_WEBAPP.REASON_PROPERTY:
                                      f"{api_constants.MGMT_WEBAPP.IP_PROPERTY} or "
                                      f"{api_constants.MGMT_WEBAPP.START_PROPERTY} or "
                                      f"{api_constants.MGMT_WEBAPP.STOP_PROPERTY} not provided"}
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MONITOR_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = google.protobuf.json_format.MessageToDict(exp_ex_info,
                                                                       including_default_value_fields=False,
                                                                       preserving_proto_field_name=False,
                                                                       use_integers_for_enums=False,
                                                                       descriptor_pool=None, float_precision=None)
        for k in response_data_dict:
            assert response_data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MONITOR_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = google.protobuf.json_format.MessageToDict(exp_ex_info,
                                                                       including_default_value_fields=False,
                                                                       preserving_proto_field_name=False,
                                                                       use_integers_for_enums=False,
                                                                       descriptor_pool=None, float_precision=None)
        for k in response_data_dict:
            assert response_data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_ossec_mng(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                               logged_in, logged_in_as_admin, get_em_ex,
                                               merged_info, start_snort_mon,
                                               stop_snort_mon, config):
        """
        Testing the HTTPS GET method for the /emulation-executions/id/ossec-ids-manager resource
        
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param start_snort: the start_snort fixture
        :param stop_snort: the stop_snort fixture
        :param config: the config fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config",
                     side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController."
                     "stop_snort_ids_monitor_threads",
                     side_effect=stop_snort_mon)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController."
                     "start_snort_ids_monitor_threads",
                     side_effect=start_snort_mon)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {api_constants.MGMT_WEBAPP.REASON_PROPERTY:
                                      f"{api_constants.MGMT_WEBAPP.IP_PROPERTY} or "
                                      f"{api_constants.MGMT_WEBAPP.START_PROPERTY} or "
                                      f"{api_constants.MGMT_WEBAPP.STOP_PROPERTY} not provided"}
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MONITOR_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = google.protobuf.json_format.MessageToDict(exp_ex_info,
                                                                       including_default_value_fields=False,
                                                                       preserving_proto_field_name=False,
                                                                       use_integers_for_enums=False,
                                                                       descriptor_pool=None, float_precision=None)
        for k in response_data_dict:
            assert response_data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MONITOR_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = google.protobuf.json_format.MessageToDict(exp_ex_info,
                                                                       including_default_value_fields=False,
                                                                       preserving_proto_field_name=False,
                                                                       use_integers_for_enums=False,
                                                                       descriptor_pool=None, float_precision=None)
        for k in response_data_dict:
            assert response_data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}