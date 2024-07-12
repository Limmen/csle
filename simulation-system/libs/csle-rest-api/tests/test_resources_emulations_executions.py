from typing import List, Tuple, Union
import json
import pytest
import pytest_mock
import csle_common.constants.constants as constants
from csle_cluster.cluster_manager.cluster_manager_pb2 import ExecutionInfoDTO, KibanaTunnelDTO, KibanaTunnelsDTO, \
    OperationOutcomeDTO, RunningEmulationsDTO, RyuTunnelDTO, RyuTunnelsDTO
from csle_collector.client_manager.client_manager_pb2 import ClientsDTO
from csle_collector.docker_stats_manager.docker_stats_manager_pb2 import DockerStatsMonitorDTO
from csle_collector.elk_manager.elk_manager_pb2 import ElkDTO
from csle_collector.host_manager.host_manager_pb2 import HostStatusDTO
from csle_collector.kafka_manager.kafka_manager_pb2 import KafkaDTO
from csle_collector.ossec_ids_manager.ossec_ids_manager_pb2 import OSSECIdsMonitorDTO
from csle_collector.ryu_manager.ryu_manager_pb2 import RyuDTO
from csle_collector.snort_ids_manager.snort_ids_manager_pb2 import SnortIdsMonitorDTO
from csle_collector.traffic_manager.traffic_manager_pb2 import TrafficDTO
from csle_common.dao.emulation_config.client_managers_info import ClientManagersInfo
from csle_common.dao.emulation_config.config import Config
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.dao.emulation_config.docker_stats_managers_info import DockerStatsManagersInfo
from csle_common.dao.emulation_config.elk_managers_info import ELKManagersInfo
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.emulation_execution import EmulationExecution
from csle_common.dao.emulation_config.emulation_execution_info import EmulationExecutionInfo
from csle_common.dao.emulation_config.host_managers_info import HostManagersInfo
from csle_common.dao.emulation_config.kafka_managers_info import KafkaManagersInfo
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.dao.emulation_config.ossec_managers_info import OSSECIDSManagersInfo
from csle_common.dao.emulation_config.ryu_managers_info import RyuManagersInfo
from csle_common.dao.emulation_config.snort_managers_info import SnortIdsManagersInfo
from csle_common.dao.emulation_config.traffic_managers_info import TrafficManagersInfo
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesEmulationExecutionsSuite:
    """
    Test suite for /emulation-executions resource
    """

    class Response:
        """
        Mock class to represent a JSON response
        """

        def __init__(self, content: Union[str, None] = None) -> None:
            """
            Initializes the object

            :param content: the JSON content of the response
            """
            if content is None:
                content_dict = {}
                content_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY] = [
                    {api_constants.MGMT_WEBAPP.ACTIVE_COUNT_PROPERTY: 1,
                     api_constants.MGMT_WEBAPP.TABLE_ID_PROPERTY: 2}]
                self.content = json.dumps(content_dict)
            else:
                self.content = content

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
    def start_client_mng(self, mocker: pytest_mock.MockFixture):
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
    def start_client_pop(self, mocker: pytest_mock.MockFixture):
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
    def stop_client_pop(self, mocker: pytest_mock.MockFixture):
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
    def stop_client_mng(self, mocker: pytest_mock.MockFixture):
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
    def stop_kafka(self, mocker: pytest_mock.MockFixture):
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
    def start_kafka(self, mocker: pytest_mock.MockFixture):
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
    def start_dcm(self, mocker: pytest_mock.MockFixture):
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
    def stop_dcm(self, mocker: pytest_mock.MockFixture):
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
    def start_dcm_thread(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_docker_statsmanager method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_docker_statsmanager_thread(ip: str, port: int, emulation: str, ip_first_octet: int) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_docker_statsmanager_thread_mocker = mocker.MagicMock(side_effect=start_docker_statsmanager_thread)
        return start_docker_statsmanager_thread_mocker

    @pytest.fixture
    def stop_dcm_thread(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_docker_statsmanager method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_docker_statsmanager_thread(ip: str, port: int, emulation: str, ip_first_octet: int) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_docker_statsmanager_thread_mocker = mocker.MagicMock(side_effect=stop_docker_statsmanager_thread)
        return stop_docker_statsmanager_thread_mocker

    @pytest.fixture
    def stop_kafka_mng(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_kafka_manager method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_kafka_manager(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_kafka_manager_mocker = mocker.MagicMock(side_effect=stop_kafka_manager)
        return stop_kafka_manager_mocker

    @pytest.fixture
    def start_kafka_mng(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_kafka_manager method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_kafka_manager(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_kafka_manager_mocker = mocker.MagicMock(side_effect=start_kafka_manager)
        return start_kafka_manager_mocker

    @pytest.fixture
    def start_kafka_srv(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_kafka_server method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_kafka_server(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_kafka_server_mocker = mocker.MagicMock(side_effect=start_kafka_server)
        return start_kafka_server_mocker

    @pytest.fixture
    def stop_kafka_srv(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_kafka_server method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_kafka_server(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_kafka_server_mocker = mocker.MagicMock(side_effect=stop_kafka_server)
        return stop_kafka_server_mocker

    @pytest.fixture
    def stop_snort_ids_mng(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_snort_ids_managers method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_snort_ids_managers(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_snort_ids_managers_mocker = mocker.MagicMock(side_effect=stop_snort_ids_managers)
        return stop_snort_ids_managers_mocker

    @pytest.fixture
    def start_snort_ids_mng(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_snort_ids_managers method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_snort_ids_managers(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_snort_ids_managers_mocker = mocker.MagicMock(side_effect=start_snort_ids_managers)
        return start_snort_ids_managers_mocker

    @pytest.fixture
    def start_snort(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_snort_idses method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_snort_idses(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_snort_idses_mocker = mocker.MagicMock(side_effect=start_snort_idses)
        return start_snort_idses_mocker

    @pytest.fixture
    def stop_snort(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_snort_idses method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_snort_idses(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_snort_idses_mocker = mocker.MagicMock(side_effect=stop_snort_idses)
        return stop_snort_idses_mocker

    @pytest.fixture
    def stop_snort_mon(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_snort_ids_monitor_threads method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_snort_ids_monitor_threads(ip: str, port: int, emulation: str, ip_first_octet: int) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_snort_ids_monitor_threads_mocker = mocker.MagicMock(side_effect=stop_snort_ids_monitor_threads)
        return stop_snort_ids_monitor_threads_mocker

    @pytest.fixture
    def start_snort_mon(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_snort_ids_monitor_threads method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_snort_ids_monitor_threads(ip: str, port: int, emulation: str, ip_first_octet: int) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_snort_ids_monitor_threads_mocker = mocker.MagicMock(side_effect=start_snort_ids_monitor_threads)
        return start_snort_ids_monitor_threads_mocker

    @pytest.fixture
    def start_ossec_mng(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_ossec_ids_managers method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_ossec_ids_manager(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_ossec_ids_manager_mocker = mocker.MagicMock(side_effect=start_ossec_ids_manager)
        return start_ossec_ids_manager_mocker

    @pytest.fixture
    def stop_ossec_mng(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_ossec_ids_managers method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_ossec_ids_manager(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        stop_ossec_ids_manager_mocker = mocker.MagicMock(side_effect=stop_ossec_ids_manager)
        return stop_ossec_ids_manager_mocker

    @pytest.fixture
    def stop_ossec_mng_plural(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_ossec_ids_managers method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_ossec_ids_managers(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        stop_ossec_ids_managers_mocker = mocker.MagicMock(side_effect=stop_ossec_ids_managers)
        return stop_ossec_ids_managers_mocker

    @pytest.fixture
    def start_ossec_mng_plural(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_ossec_ids_managers method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_ossec_ids_managers(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_ossec_ids_managers_mocker = mocker.MagicMock(side_effect=start_ossec_ids_managers)
        return start_ossec_ids_managers_mocker

    @pytest.fixture
    def start_ossec_id_plural(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_ossec_ids_managers method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_ossec_idses(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_ossec_idses_mocker = mocker.MagicMock(side_effect=start_ossec_idses)
        return start_ossec_idses_mocker

    @pytest.fixture
    def start_ossec_id(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_ossec_ids_managers method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_ossec_ids(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_ossec_ids_mocker = mocker.MagicMock(side_effect=start_ossec_ids)
        return start_ossec_ids_mocker

    @pytest.fixture
    def stop_ossec_id_plural(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_ossec_ids_managers method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_ossec_idses(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_ossec_idses_mocker = mocker.MagicMock(side_effect=stop_ossec_idses)
        return stop_ossec_idses_mocker

    @pytest.fixture
    def stop_ossec_id(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_ossec_ids_managers method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_ossec_ids(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_ossec_ids_mocker = mocker.MagicMock(side_effect=stop_ossec_ids)
        return stop_ossec_ids_mocker

    @pytest.fixture
    def stop_ossec_id_mon_plural(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_ossec_ids_managers method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_ossec_ids_monitor_threads(ip: str, port: int, emulation: str, ip_first_octet: int) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_ossec_ids_monitor_threads_mocker = mocker.MagicMock(side_effect=stop_ossec_ids_monitor_threads)
        return stop_ossec_ids_monitor_threads_mocker

    @pytest.fixture
    def stop_ossec_id_mon(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_ossec_ids_managers method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_ossec_ids_monitor_thread(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_ossec_ids_monitor_thread_mocker = mocker.MagicMock(side_effect=stop_ossec_ids_monitor_thread)
        return stop_ossec_ids_monitor_thread_mocker

    @pytest.fixture
    def start_ossec_id_mon_plural(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_ossec_ids_managers method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_ossec_ids_monitor_threads(ip: str, port: int, emulation: str, ip_first_octet: int) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_ossec_ids_monitor_threads_mocker = mocker.MagicMock(side_effect=start_ossec_ids_monitor_threads)
        return start_ossec_ids_monitor_threads_mocker

    @pytest.fixture
    def start_ossec_id_mon(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_ossec_ids_managers method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_ossec_ids_monitor_thread(ip: str, port: int, emulation: str, ip_first_octet: int,
                                           container_ip: str) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        start_ossec_ids_monitor_thread_mocker = mocker.MagicMock(side_effect=start_ossec_ids_monitor_thread)
        return start_ossec_ids_monitor_thread_mocker

    @pytest.fixture
    def start_host_mng_plural(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_host_managers method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_host_managers(ip: str, port: int, emulation: str, ip_first_octet: int, ) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_host_managers_mocker = mocker.MagicMock(side_effect=start_host_managers)
        return start_host_managers_mocker

    @pytest.fixture
    def stop_host_mng_plural(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_host_managers method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_host_managers(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_host_managers_mocker = mocker.MagicMock(side_effect=stop_host_managers)
        return stop_host_managers_mocker

    @pytest.fixture
    def start_host_mng(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_host_manager method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_host_manager(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_host_manager_mocker = mocker.MagicMock(side_effect=start_host_manager)
        return start_host_manager_mocker

    @pytest.fixture
    def stop_host_mng(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_host_manager method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_host_manager(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        stop_host_manager_mocker = mocker.MagicMock(side_effect=stop_host_manager)
        return stop_host_manager_mocker

    @pytest.fixture
    def stop_host_mon_plural(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_host_monitor_threads method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_host_monitor_threads(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_host_monitor_threads_mocker = mocker.MagicMock(side_effect=stop_host_monitor_threads)
        return stop_host_monitor_threads_mocker

    @pytest.fixture
    def start_host_mon_plural(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_host_monitor_threads method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_host_monitor_threads(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_host_monitor_threads_mocker = mocker.MagicMock(side_effect=start_host_monitor_threads)
        return start_host_monitor_threads_mocker

    @pytest.fixture
    def start_host_mon(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_host_monitor_thread method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_host_monitor_thread(ip: str, port: int, emulation: str, ip_first_octet: int,
                                      container_ip: str) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_host_monitor_thread_mocker = mocker.MagicMock(side_effect=start_host_monitor_thread)
        return start_host_monitor_thread_mocker

    @pytest.fixture
    def stop_host_mon(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_host_monitor_thread method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_host_monitor_thread(ip: str, port: int, emulation: str, ip_first_octet: int,
                                     container_ip: str) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_host_monitor_thread_mocker = mocker.MagicMock(side_effect=stop_host_monitor_thread)
        return stop_host_monitor_thread_mocker

    @pytest.fixture
    def start_cont(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_container method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_container(ip: str, port: int, container_name: str) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_container_mocker = mocker.MagicMock(side_effect=start_container)
        return start_container_mocker

    @pytest.fixture
    def stop_cont(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_container method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_container(ip: str, port: int, container_name: str) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_container_mocker = mocker.MagicMock(side_effect=stop_container)
        return stop_container_mocker

    @pytest.fixture
    def start_container_plural(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_containers_of_execution method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_containers_of_execution(ip: str, port: int, emulation: str, ip_first_octet: int) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_containers_of_execution_mocker = mocker.MagicMock(side_effect=start_containers_of_execution)
        return start_containers_of_execution_mocker

    @pytest.fixture
    def stop_container_plural(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_containers_of_execution method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_containers_of_execution(ip: str, port: int, emulation: str, ip_first_octet: int) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_containers_of_execution_mocker = mocker.MagicMock(side_effect=stop_containers_of_execution)
        return stop_containers_of_execution_mocker

    @pytest.fixture
    def start_elk_mng(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mockingthe start_elk_manager method
        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_elk_manager(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_elk_manager_mocker = mocker.MagicMock(side_effect=start_elk_manager)
        return start_elk_manager_mocker

    @pytest.fixture
    def stop_elk_mng(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_elk_manager method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_elk_manager(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_elk_manager_mocker = mocker.MagicMock(side_effect=stop_elk_manager)
        return stop_elk_manager_mocker

    @pytest.fixture
    def stop_elk_stk(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mockingthe stop_elk_stack method
        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_elk_stack(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_elk_stack_mocker = mocker.MagicMock(side_effect=stop_elk_stack)
        return stop_elk_stack_mocker

    @pytest.fixture
    def start_elk_stk(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_elk_stack method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_elk_stack(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_elk_stack_mocker = mocker.MagicMock(side_effect=start_elk_stack)
        return start_elk_stack_mocker

    @pytest.fixture
    def start_els(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_elastic method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_elastic(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_elastic_mocker = mocker.MagicMock(side_effect=start_elastic)
        return start_elastic_mocker

    @pytest.fixture
    def stop_els(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_elastic method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_elastic(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_elastic_mocker = mocker.MagicMock(side_effect=stop_elastic)
        return stop_elastic_mocker

    @pytest.fixture
    def stop_lgst(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_logstash method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_logstash(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_logstash_mocker = mocker.MagicMock(side_effect=stop_logstash)
        return stop_logstash_mocker

    @pytest.fixture
    def start_lgst(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_logstash method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_logstash(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_logstash_mocker = mocker.MagicMock(side_effect=start_logstash)
        return start_logstash_mocker

    @pytest.fixture
    def start_kb(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_kibana method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_kibana(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_kibana_mocker = mocker.MagicMock(side_effect=start_kibana)
        return start_kibana_mocker

    @pytest.fixture
    def stop_kb(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_kibana method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_kibana(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_kibana_mocker = mocker.MagicMock(side_effect=stop_kibana)
        return stop_kibana_mocker

    @pytest.fixture
    def remove_kb(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the remove_kibana_tunnel method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def remove_kibana_tunnel(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        remove_kibana_tunnel_mocker = mocker.MagicMock(side_effect=remove_kibana_tunnel)
        return remove_kibana_tunnel_mocker

    @pytest.fixture
    def stop_tr_mng_plural(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_traffic_managers method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_traffic_managers(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_traffic_managers_mocker = mocker.MagicMock(side_effect=stop_traffic_managers)
        return stop_traffic_managers_mocker

    @pytest.fixture
    def start_tr_mng_plural(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_traffic_managers method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_traffic_managers(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_traffic_managers_mocker = mocker.MagicMock(side_effect=start_traffic_managers)
        return start_traffic_managers_mocker

    @pytest.fixture
    def stop_tr_mng(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_traffic_manager method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_traffic_manager(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_traffic_manager_mocker = mocker.MagicMock(side_effect=stop_traffic_manager)
        return stop_traffic_manager_mocker

    @pytest.fixture
    def start_tr_mng(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_traffic_manager method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_traffic_manager(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        start_traffic_manager_mocker = mocker.MagicMock(side_effect=start_traffic_manager)
        return start_traffic_manager_mocker

    @pytest.fixture
    def stop_tr_gen(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_traffic_generator method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_traffic_generator(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_traffic_generator_mocker = mocker.MagicMock(side_effect=stop_traffic_generator)
        return stop_traffic_generator_mocker

    @pytest.fixture
    def start_tr_gen(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stort_traffic_generator method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_traffic_generator(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_traffic_generator_mocker = mocker.MagicMock(side_effect=start_traffic_generator)
        return start_traffic_generator_mocker

    @pytest.fixture
    def stop_tr_gen_plural(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_traffic_generators method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_traffic_generators(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_traffic_generators_mocker = mocker.MagicMock(side_effect=stop_traffic_generators)
        return stop_traffic_generators_mocker

    @pytest.fixture
    def start_tr_gen_plural(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stort_traffic_generators method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_traffic_generators(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_traffic_generators_mocker = mocker.MagicMock(side_effect=start_traffic_generators)
        return start_traffic_generators_mocker

    @pytest.fixture
    def start_f_beat_plural(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_filebeats method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_filebeats(ip: str, port: int, emulation: str, ip_first_octet: int, initial_start: bool) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_filebeats_mocker = mocker.MagicMock(side_effect=start_filebeats)
        return start_filebeats_mocker

    @pytest.fixture
    def stop_f_beat_plural(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_filebeats method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_filebeats(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_filebeats_mocker = mocker.MagicMock(side_effect=stop_filebeats)
        return stop_filebeats_mocker

    @pytest.fixture
    def start_f_beat(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_filebeat method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_filebeat(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str,
                           initial_start: bool) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_filebeat_mocker = mocker.MagicMock(side_effect=start_filebeat)
        return start_filebeat_mocker

    @pytest.fixture
    def stop_f_beat(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_filebeat method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_filebeat(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_filebeat_mocker = mocker.MagicMock(side_effect=stop_filebeat)
        return stop_filebeat_mocker

    @pytest.fixture
    def start_p_beat_plural(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_packetbeats method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_packetbeats(ip: str, port: int, emulation: str, ip_first_octet: int, initial_start: bool) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_packetbeats_mocker = mocker.MagicMock(side_effect=start_packetbeats)
        return start_packetbeats_mocker

    @pytest.fixture
    def stop_p_beat_plural(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_packetbeats method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_packetbeats(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_packetbeats_mocker = mocker.MagicMock(side_effect=stop_packetbeats)
        return stop_packetbeats_mocker

    @pytest.fixture
    def start_p_beat(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_packetbeat method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_packetbeat(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str,
                             initial_start: bool) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_packetbeat_mocker = mocker.MagicMock(side_effect=start_packetbeat)
        return start_packetbeat_mocker

    @pytest.fixture
    def stop_p_beat(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_packetbeat method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_packetbeat(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_packetbeat_mocker = mocker.MagicMock(side_effect=stop_packetbeat)
        return stop_packetbeat_mocker

    @pytest.fixture
    def start_m_beat_plural(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_metricbeats method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_metricbeats(ip: str, port: int, emulation: str, ip_first_octet: int, initial_start: bool) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_metricbeats_mocker = mocker.MagicMock(side_effect=start_metricbeats)
        return start_metricbeats_mocker

    @pytest.fixture
    def stop_m_beat_plural(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_metricbeats method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_metricbeats(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_metricbeats_mocker = mocker.MagicMock(side_effect=stop_metricbeats)
        return stop_metricbeats_mocker

    @pytest.fixture
    def start_m_beat(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_metricbeat method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_metricbeat(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str,
                             initial_start: bool) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_metricbeat_mocker = mocker.MagicMock(side_effect=start_metricbeat)
        return start_metricbeat_mocker

    @pytest.fixture
    def stop_m_beat(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_metricbeat method
        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_metricbeat(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_metricbeat_mocker = mocker.MagicMock(side_effect=stop_metricbeat)
        return stop_metricbeat_mocker

    @pytest.fixture
    def start_h_beat_plural(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_heartbeats method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_heartbeats(ip: str, port: int, emulation: str, ip_first_octet: int, initial_start: bool) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_heartbeats_mocker = mocker.MagicMock(side_effect=start_heartbeats)
        return start_heartbeats_mocker

    @pytest.fixture
    def stop_h_beat_plural(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_heartbeats method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_heartbeats(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_heartbeats_mocker = mocker.MagicMock(side_effect=stop_heartbeats)
        return stop_heartbeats_mocker

    @pytest.fixture
    def start_h_beat(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_heartbeat method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_heartbeat(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str,
                            initial_start: bool) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_heartbeat_mocker = mocker.MagicMock(side_effect=start_heartbeat)
        return start_heartbeat_mocker

    @pytest.fixture
    def stop_h_beat(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_heartbeat method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_heartbeat(ip: str, port: int, emulation: str, ip_first_octet: int, container_ip: str) \
                -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_heartbeat_mocker = mocker.MagicMock(side_effect=stop_heartbeat)
        return stop_heartbeat_mocker

    @pytest.fixture
    def start_ryu_mng(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_ryu_manager method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_ryu_manager(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_ryu_manager_mocker = mocker.MagicMock(side_effect=start_ryu_manager)
        return start_ryu_manager_mocker

    @pytest.fixture
    def stop_ryu_mng(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_ryu_manager method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_ryu_manager(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_ryu_manager_mocker = mocker.MagicMock(side_effect=stop_ryu_manager)
        return stop_ryu_manager_mocker

    @pytest.fixture
    def stop_ryu_ctr(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_ryu method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_ryu(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_ryu_mocker = mocker.MagicMock(side_effect=stop_ryu)
        return stop_ryu_mocker

    @pytest.fixture
    def start_ryu_ctr(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_ryu method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_ryu(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_ryu_mocker = mocker.MagicMock(side_effect=start_ryu)
        return start_ryu_mocker

    @pytest.fixture
    def start_ryu_mon(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the start_ryu_monitor method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def start_ryu_monitor(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        start_ryu_monitor_mocker = mocker.MagicMock(side_effect=start_ryu_monitor)
        return start_ryu_monitor_mocker

    @pytest.fixture
    def stop_ryu_mon(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the stop_ryu_monitor method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_ryu_monitor(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        stop_ryu_monitor_mocker = mocker.MagicMock(side_effect=stop_ryu_monitor)
        return stop_ryu_monitor_mocker

    @pytest.fixture
    def remove_ryu_ctr(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for the remove_ryu_tunnel method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def remove_ryu_tunnel(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=False)

        remove_ryu_tunnel_mocker = mocker.MagicMock(side_effect=remove_ryu_tunnel)
        return remove_ryu_tunnel_mocker

    @pytest.fixture
    def get_mock(self, mocker: pytest_mock.MockFixture):
        """
        pytest fixture for mocking the request.get() method

        :param mocker: the pytest mokcer object
        :return: the mocked function
        """

        def get(http_adress: str, timeout: str):
            response = TestResourcesEmulationExecutionsSuite.response_returner()
            return response

        get_mocker = mocker.MagicMock(side_effect=get)
        return get_mocker

    @staticmethod
    def response_returner() -> "TestResourcesEmulationExecutionsSuite.Response":
        """
        Static help method for returning a response class

        :return: a Response object
        """
        return TestResourcesEmulationExecutionsSuite.Response()

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
    def kibana(self, mocker: pytest_mock.MockFixture):
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
    def kibana_list(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_kibana_tunnels method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def list_kibana_tunnels(ip: str, port: int):
            kibana_tunnel = KibanaTunnelDTO(port=5, ip="123.456.78.99", emulation="null", ipFirstOctet=-1)
            return KibanaTunnelsDTO(tunnels=[kibana_tunnel])

        list_kibana_tunnels_mocker = mocker.MagicMock(side_effect=list_kibana_tunnels)
        return list_kibana_tunnels_mocker

    @pytest.fixture
    def merged_info(self, mocker: pytest_mock.MockFixture):
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
    def create_ryu(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the create_ryu_tunnel method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def create_ryu_tunnel(ip: str, port: int, emulation: str, ip_first_octet: int) -> OperationOutcomeDTO:
            return OperationOutcomeDTO(outcome=True)

        create_ryu_tunnel_mocker = mocker.MagicMock(side_effect=create_ryu_tunnel)
        return create_ryu_tunnel_mocker

    @pytest.fixture
    def list_ryu(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_ryu_tunnels method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def list_ryu_tunnels(ip: str, port: int) -> RyuTunnelsDTO:
            return RyuTunnelsDTO(tunnels=[RyuTunnelDTO(port=1, ip="123.456.78.99", emulation="null", ipFirstOctet=-1)])

        list_ryu_tunnels_mocker = mocker.MagicMock(side_effect=list_ryu_tunnels)
        return list_ryu_tunnels_mocker

    @pytest.fixture
    def exec_none(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_emulation_execution function

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_emulation_execution(ip_first_octet: int, emulation_name: str) -> None:
            return None

        get_emulation_execution_mocker = mocker.MagicMock(side_effect=get_emulation_execution)
        return get_emulation_execution_mocker

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
    def get_exec_info() -> EmulationExecutionInfo:
        """
        Static help method for returning an ExecutionInfoDTO

        :return: ExecutionInfoDTO
        """
        snort_ids = SnortIdsManagersInfo(ips=["123.456.78.99"],
                                         ports=[10], emulation_name="JDoeEmulation",
                                         execution_id=10,
                                         snort_ids_managers_statuses=[SnortIdsMonitorDTO(monitor_running=True,
                                                                                         snort_ids_running=True)],
                                         snort_ids_managers_running=[True])
        ossec_ids = OSSECIDSManagersInfo(ips=["123.456.78.99"],
                                         ports=[10], emulation_name="JohnDoeEmulation",
                                         execution_id=10,
                                         ossec_ids_managers_statuses=[OSSECIdsMonitorDTO(monitor_running=True,
                                                                                         ossec_ids_running=True)],
                                         ossec_ids_managers_running=[True])
        kafka_mng = KafkaManagersInfo(ips=["123.456.78.99"], ports=[10],
                                      emulation_name="JohnDoeEmulation", execution_id=10,
                                      kafka_managers_statuses=[KafkaDTO(running=True,
                                                                        topics="abcdef")],
                                      kafka_managers_running=[True])
        host_mng = HostManagersInfo(ips=["123.456.78.99"],
                                    ports=[10], emulation_name="JDoeEmulation",
                                    execution_id=10,
                                    host_managers_statuses=[HostStatusDTO(monitor_running=True,
                                                                          filebeat_running=True,
                                                                          packetbeat_running=True,
                                                                          metricbeat_running=True,
                                                                          heartbeat_running=True)],
                                    host_managers_running=[True])
        clinet_mng = ClientManagersInfo(ips=["123.456.78.99"], ports=[10],
                                        emulation_name="JDoeEmulation", execution_id=10,
                                        client_managers_statuses=[ClientsDTO(num_clients=4, client_process_active=True,
                                                                             producer_active=True,
                                                                             clients_time_step_len_seconds=4,
                                                                             producer_time_step_len_seconds=4)],
                                        client_managers_running=[True])
        docker_mng = DockerStatsManagersInfo(ips=["123.456.78.99"], ports=[10],
                                             emulation_name="JDoeEmulation", execution_id=10,
                                             docker_stats_managers_statuses=[
                                                 DockerStatsMonitorDTO(num_monitors=4, emulations="abcdef",
                                                                       emulation_executions=[1, 2, 3, 4, 5]
                                                                       )],
                                             docker_stats_managers_running=[True])
        c_network = ContainerNetwork(name="JohnDoe",
                                     subnet_mask="null",
                                     bitmask="null",
                                     subnet_prefix="null",
                                     interface="eth0")
        node_cc = NodeContainerConfig(name="JohnDoe",
                                      ips_and_networks=[("null", c_network)],
                                      version="null", level="null", restart_policy="null",
                                      suffix="null", os="null", execution_ip_first_octet=-1,
                                      docker_gw_bridge_ip="123.456.78.99",
                                      physical_host_ip="123.456.78.99")
        traffic_mng = TrafficManagersInfo(ips=["123.456.78.99"], ports=[10],
                                          emulation_name="JohnDoeEmulatin", execution_id=10,
                                          traffic_managers_statuses=[TrafficDTO(running=True, script="null")],
                                          traffic_managers_running=[True])

        elk_mng = ELKManagersInfo(ips=["123.456.78.99"], ports=[10],
                                  emulation_name="JDoeEmulation", execution_id=10,
                                  elk_managers_statuses=[ElkDTO(elasticRunning=True,
                                                                kibanaRunning=True,
                                                                logstashRunning=True)],
                                  elk_managers_running=[True], local_kibana_port=5,
                                  physical_server_ip="123.456.78.99")
        ryu_mng = RyuManagersInfo(ips=["123.456.78.99"], ports=[10],
                                  emulation_name="JohnDoeEmulation", execution_id=10,
                                  ryu_managers_statuses=[RyuDTO(ryu_running=True,
                                                                monitor_running=True,
                                                                port=4, web_port=4,
                                                                controller="null",
                                                                kafka_ip="123.456.78.99",
                                                                kafka_port=4, time_step_len=4)],
                                  ryu_managers_running=[True], local_controller_web_port=1,
                                  physical_server_ip="123.456.78.99")
        em_exec_info = EmulationExecutionInfo(emulation_name="JohnDoe", execution_id=10,
                                              snort_ids_managers_info=snort_ids,
                                              ossec_ids_managers_info=ossec_ids,
                                              kafka_managers_info=kafka_mng,
                                              host_managers_info=host_mng,
                                              client_managers_info=clinet_mng,
                                              docker_stats_managers_info=docker_mng,
                                              running_containers=[node_cc],
                                              stopped_containers=[node_cc],
                                              traffic_managers_info=traffic_mng,
                                              active_networks=[c_network],
                                              inactive_networks=[c_network], elk_managers_info=elk_mng,
                                              ryu_managers_info=ryu_mng)
        return em_exec_info

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
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
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
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
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
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
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
                                         logged_in_as_admin, get_em_ex, emulation_exec, get_ex_exec) -> None:
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
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
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
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
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
                                              merged_info, kibana_list, kibana, create_ryu, list_ryu) -> None:
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
        mocker.patch('time.sleep', return_value=None)
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
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                               f"{api_constants.MGMT_WEBAPP.INFO_SUBRESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
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
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                               f"{api_constants.MGMT_WEBAPP.INFO_SUBRESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
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
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                               f"{api_constants.MGMT_WEBAPP.INFO_SUBRESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_cm_post(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                             logged_in, logged_in_as_admin, get_em_ex,
                                             merged_info, get_ex_exec, start_client_mng, stop_client_mng) -> None:
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
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_client_manager",
                     side_effect=stop_client_mng)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_client_manager",
                     side_effect=start_client_mng)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
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
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CLIENT_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
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
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
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
                                             logged_in, logged_in_as_admin, get_em_ex, merged_info, get_ex_exec,
                                             start_client_pop, stop_client_pop) -> None:
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
        mocker.patch('time.sleep', return_value=None)
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
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CLIENT_POPULATION_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CLIENT_POPULATION_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
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
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
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
                                                 logged_in, logged_in_as_admin, get_em_ex, merged_info, start_kafka,
                                                 stop_kafka) -> None:
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
        mocker.patch('time.sleep', return_value=None)
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
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CLIENT_PRODUCER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CLIENT_PRODUCER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
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
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
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
                                              merged_info, start_dcm, stop_dcm, config) -> None:
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
        :param config: the config fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_docker_statsmanager",
                     side_effect=stop_dcm)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_docker_statsmanager",
                     side_effect=start_dcm)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.DOCKER_STATS_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.DOCKER_STATS_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.DOCKER_STATS_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
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
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.DOCKER_STATS_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
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
                                                 logged_in, logged_in_as_admin, get_em_ex, merged_info,
                                                 start_dcm_thread, stop_dcm_thread, config) -> None:
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
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController."
                     "stop_docker_statsmanager_thread", side_effect=stop_dcm_thread)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController."
                     "start_docker_statsmanager_thread", side_effect=start_dcm_thread)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.DOCKER_STATS_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.DOCKER_STATS_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.DOCKER_STATS_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
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
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.DOCKER_STATS_MONITOR_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
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
                                                    logged_in, logged_in_as_admin, get_em_ex, merged_info,
                                                    start_kafka_mng, stop_kafka_mng) -> None:
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
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_kafka_manager",
                     side_effect=stop_kafka_mng)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_kafka_manager",
                     side_effect=start_kafka_mng)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KAFKA_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KAFKA_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KAFKA_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
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
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KAFKA_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
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
                                                logged_in, logged_in_as_admin, get_em_ex, merged_info, start_kafka_srv,
                                                stop_kafka_srv) -> None:
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
        mocker.patch('time.sleep', return_value=None)
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_kafka_server",
                     side_effect=stop_kafka_srv)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_kafka_server",
                     side_effect=start_kafka_srv)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KAFKA_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KAFKA_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KAFKA_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
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
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KAFKA_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
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
                                               logged_in, logged_in_as_admin, get_em_ex, merged_info,
                                               start_snort_ids_mng, stop_snort_ids_mng, config) -> None:
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
        mocker.patch('time.sleep', return_value=None)
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_snort_ids_managers",
                     side_effect=stop_snort_ids_mng)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_snort_ids_managers",
                     side_effect=start_snort_ids_mng)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
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
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
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
                                           logged_in, logged_in_as_admin, get_em_ex, merged_info, start_snort,
                                           stop_snort, config) -> None:
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
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_snort_idses",
                     side_effect=stop_snort)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_snort_idses",
                     side_effect=start_snort)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
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
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
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
                                               logged_in, logged_in_as_admin, get_em_ex, merged_info, start_snort_mon,
                                               stop_snort_mon, config) -> None:
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
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController."
                     "stop_snort_ids_monitor_threads", side_effect=stop_snort_mon)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController."
                     "start_snort_ids_monitor_threads", side_effect=start_snort_mon)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
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
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.SNORT_IDS_MONITOR_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
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
                                               logged_in, logged_in_as_admin, get_em_ex, merged_info, start_ossec_mng,
                                               stop_ossec_mng, stop_ossec_mng_plural, start_ossec_mng_plural, config) \
            -> None:
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
        :param start_ossec_mng: the start_ossec_mng fixture
        :param start_ossec_mng_plural: the start_ossec_mng_plural fixture
        :param stop_ossec_mng: the stop_ossec_mng fixture
        :param stop_ossec_mng_plural: the stop_ossec_mng_plural fixture
        :param config: the config fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_ossec_ids_manager",
                     side_effect=stop_ossec_mng)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_ossec_ids_manager",
                     side_effect=start_ossec_mng)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_ossec_ids_managers",
                     side_effect=start_ossec_mng_plural)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_ossec_ids_managers",
                     side_effect=stop_ossec_mng_plural)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]

        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.START_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_ossec(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                           logged_in, logged_in_as_admin, get_em_ex, merged_info, start_ossec_id,
                                           stop_ossec_id, stop_ossec_id_plural, start_ossec_id_plural, config) -> None:
        """
        Testing the HTTPS GET method for the /emulation-executions/id/ossec-ids resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param start_ossec_mng: the start_ossec_mng fixture
        :param start_ossec_mng_plural: the start_ossec_mng_plural fixture
        :param stop_ossec_mng: the stop_ossec_mng fixture
        :param stop_ossec_mng_plural: the stop_ossec_mng_plural fixture
        :param config: the config fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_ossec_ids",
                     side_effect=stop_ossec_id)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_ossec_ids",
                     side_effect=start_ossec_id)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_ossec_idses",
                     side_effect=start_ossec_id_plural)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_ossec_idses",
                     side_effect=stop_ossec_id_plural)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]

        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.START_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_ossec_mon(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                               logged_in, logged_in_as_admin, get_em_ex, merged_info,
                                               start_ossec_id_mon, stop_ossec_id_mon, stop_ossec_id_mon_plural,
                                               start_ossec_id_mon_plural, config) -> None:
        """
        Testing the HTTPS GET method for the /emulation-executions/id/ossec-ids-monitor resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param stop_ossec_id_mon: the start_ossec_mng fixture
        :param start_ossec_id_mon_plural: the start_ossec_mng_plural fixture
        :param stop_ossec_id_mon: the stop_ossec_mng fixture
        :param stop_ossec_id_mon_plural: the stop_ossec_mng_plural fixture
        :param config: the config fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_ossec_ids_monitor_thread",
                     side_effect=stop_ossec_id_mon)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_ossec_ids_monitor_thread",
                     side_effect=start_ossec_id_mon)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController."
                     "start_ossec_idses_monitor_threads", side_effect=start_ossec_id_mon_plural)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController."
                     "stop_ossec_ids_monitor_threads", side_effect=stop_ossec_id_mon_plural)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_MONITOR_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_MONITOR_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]

        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_MONITOR_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_MONITOR_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.START_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.OSSEC_IDS_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_host_mng(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                              logged_in, logged_in_as_admin, get_em_ex, merged_info, start_host_mng,
                                              stop_host_mng, stop_host_mng_plural, start_host_mng_plural, config) \
            -> None:
        """
        Testing the HTTPS GET method for the /emulation-executions/id/host-manager resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param stop_ossec_id_mon: the start_ossec_mng fixture
        :param start_ossec_id_mon_plural: the start_ossec_mng_plural fixture
        :param stop_ossec_id_mon: the stop_ossec_mng fixture
        :param stop_ossec_id_mon_plural: the stop_ossec_mng_plural fixture
        :param config: the config fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_host_manager",
                     side_effect=stop_host_mng)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_host_manager",
                     side_effect=start_host_mng)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_host_managers",
                     side_effect=start_host_mng_plural)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_host_managers",
                     side_effect=stop_host_mng_plural)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.HOST_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.HOST_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.HOST_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.HOST_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.HOST_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]

        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.HOST_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.HOST_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.START_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.HOST_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_host_mon(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                              logged_in, logged_in_as_admin, get_em_ex, merged_info, start_host_mon,
                                              stop_host_mon, stop_host_mon_plural, start_host_mon_plural, config) \
            -> None:
        """
        Testing the HTTPS GET method for the /emulation-executions/id/host-monitor resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param stop_ossec_id_mon: the start_ossec_mng fixture
        :param start_ossec_id_mon_plural: the start_ossec_mng_plural fixture
        :param stop_ossec_id_mon: the stop_ossec_mng fixture
        :param stop_ossec_id_mon_plural: the stop_ossec_mng_plural fixture
        :param config: the config fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_host_monitor_thread",
                     side_effect=stop_host_mon)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_host_monitor_thread",
                     side_effect=start_host_mon)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_host_monitor_threads",
                     side_effect=start_host_mon_plural)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_host_monitor_threads",
                     side_effect=stop_host_mon_plural)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.HOST_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.HOST_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.HOST_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.HOST_MONITOR_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.HOST_MONITOR_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]

        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.HOST_MONITOR_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.HOST_MONITOR_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.START_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.HOST_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_container(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                               logged_in, logged_in_as_admin, get_em_ex, merged_info, start_cont,
                                               stop_cont, stop_container_plural, start_container_plural, config) \
            -> None:
        """
        Testing the HTTPS GET method for the /emulation-executions/id/container resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param start_cont: the start_cont fixture
        :param stop_container_plural: the stop_container_plural fixture
        :param stop_cont: the stop_cont fixture
        :param start_container_plural: the start_container_plural fixture
        :param config: the config fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_container",
                     side_effect=stop_cont)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_container",
                     side_effect=start_cont)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_containers_of_execution",
                     side_effect=start_container_plural)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_containers_of_execution",
                     side_effect=stop_container_plural)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CONTAINER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CONTAINER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CONTAINER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CONTAINER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.NAME_PROPERTY:
                                                                     "JohnDoe"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CONTAINER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.NAME_PROPERTY: "JohnDoe"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]

        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CONTAINER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.NAME_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CONTAINER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.NAME_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.START_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.CONTAINER_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.NAME_PROPERTY: "JohnDoe"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_elk_mng(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                             logged_in, logged_in_as_admin, get_em_ex, merged_info, start_elk_mng,
                                             stop_elk_mng, config, kibana, kibana_list) -> None:
        """
        Testing the HTTPS GET method for the /emulation-executions/id/elk-manager resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param start_elk_mng: the start_elk_mng fixture
        :param stop_elk_mng: the stop_elk_mng fixture
        :param config: the config fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_elk_manager",
                     side_effect=stop_elk_mng)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.create_kibana_tunnel",
                     side_effect=kibana)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.list_kibana_tunnels",
                     side_effect=kibana_list)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_elk_manager",
                     side_effect=start_elk_mng)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.ELK_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.ELK_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.ELK_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.ELK_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.ELK_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]

        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.ELK_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.ELK_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.START_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.ELK_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_elk_stack(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                               logged_in, logged_in_as_admin, get_em_ex, merged_info, start_elk_stk,
                                               stop_elk_stk, config, kibana, kibana_list) -> None:
        """
        Testing the HTTPS GET method for the /emulation-executions/id/elk-stack resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param start_elk_mng: the start_elk_stk fixture
        :param stop_elk_stk: the stop_elk_stk fixture
        :param config: the config fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_elk_stack",
                     side_effect=stop_elk_stk)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.create_kibana_tunnel",
                     side_effect=kibana)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.list_kibana_tunnels",
                     side_effect=kibana_list)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_elk_stack",
                     side_effect=start_elk_stk)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.ELK_STACK_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.ELK_STACK_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.ELK_STACK_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.ELK_STACK_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.ELK_STACK_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]

        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.ELK_STACK_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.ELK_STACK_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.START_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.ELK_STACK_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_elastic(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                             logged_in, logged_in_as_admin, get_em_ex, merged_info, start_els,
                                             stop_els, config, kibana, kibana_list) -> None:
        """
        Testing the HTTPS GET method for the /emulation-executions/id/elastic resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param start_els: the start_els fixture
        :param stop_els: the stop_els fixture
        :param config: the config fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_elastic",
                     side_effect=stop_els)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.create_kibana_tunnel",
                     side_effect=kibana)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.list_kibana_tunnels",
                     side_effect=kibana_list)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_elastic",
                     side_effect=start_els)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.ELASTIC_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.ELASTIC_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.ELASTIC_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.ELASTIC_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.ELASTIC_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]

        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.ELASTIC_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.ELASTIC_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.START_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.ELASTIC_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_logstash(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                              logged_in, logged_in_as_admin, get_em_ex, merged_info, start_lgst,
                                              stop_lgst, config, kibana, kibana_list) -> None:
        """
        Testing the HTTPS GET method for the /emulation-executions/id/logstash resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param start_els: the start_els fixture
        :param stop_els: the stop_els fixture
        :param config: the config fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_logstash",
                     side_effect=stop_lgst)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.create_kibana_tunnel",
                     side_effect=kibana)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.list_kibana_tunnels",
                     side_effect=kibana_list)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_logstash",
                     side_effect=start_lgst)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.LOGSTASH_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.LOGSTASH_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.LOGSTASH_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.LOGSTASH_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.LOGSTASH_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]

        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.LOGSTASH_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.LOGSTASH_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.START_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.LOGSTASH_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_kibana(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                            logged_in, logged_in_as_admin, get_em_ex, merged_info, start_kb, stop_kb,
                                            config, kibana, kibana_list, remove_kb) -> None:
        """
        Testing the HTTPS GET method for the /emulation-executions/id/kibana resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param start_els: the start_els fixture
        :param stop_els: the stop_els fixture
        :param config: the config fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_kibana",
                     side_effect=stop_kb)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.create_kibana_tunnel",
                     side_effect=kibana)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.list_kibana_tunnels",
                     side_effect=kibana_list)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.remove_kibana_tunnel",
                     side_effect=remove_kb)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_kibana",
                     side_effect=start_kb)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KIBANA_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KIBANA_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KIBANA_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KIBANA_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KIBANA_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]

        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KIBANA_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KIBANA_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.START_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.KIBANA_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_traffic_mng(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                                 logged_in, logged_in_as_admin, get_em_ex, merged_info, start_tr_mng,
                                                 start_tr_mng_plural, stop_tr_mng, stop_tr_mng_plural,
                                                 config, kibana, kibana_list, remove_kb) -> None:
        """
        Testing the HTTPS GET method for the /emulation-executions/id/traffic-manager resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param start_els: the start_els fixture
        :param stop_els: the stop_els fixture
        :param config: the config fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_traffic_manager",
                     side_effect=stop_tr_mng)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_traffic_managers",
                     side_effect=stop_tr_mng_plural)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.create_kibana_tunnel",
                     side_effect=kibana)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.list_kibana_tunnels",
                     side_effect=kibana_list)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.remove_kibana_tunnel",
                     side_effect=remove_kb)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_traffic_manager",
                     side_effect=start_tr_mng)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_traffic_managers",
                     side_effect=start_tr_mng_plural)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.TRAFFIC_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.TRAFFIC_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.TRAFFIC_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.TRAFFIC_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.TRAFFIC_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]

        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.TRAFFIC_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.TRAFFIC_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.START_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.TRAFFIC_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_traffic_gen(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                                 logged_in, logged_in_as_admin, get_em_ex, merged_info, start_tr_gen,
                                                 start_tr_gen_plural, stop_tr_gen, stop_tr_gen_plural, config) -> None:
        """
        Testing the HTTPS GET method for the /emulation-executions/id/traffic-generator resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param start_tr_gen: the start_tr_gen fixture
        :param start_tr_gen_plural: the start_tr_gen_plural fixture
        :param stop_tr_gen_plural: the stop_tr_gen_plural fixture
        :param stop_tr_gen: the stop_tr_gen fixture
        :param config: the config fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_traffic_generator",
                     side_effect=stop_tr_gen)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_traffic_generators",
                     side_effect=stop_tr_gen_plural)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_traffic_generator",
                     side_effect=start_tr_gen)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_traffic_generators",
                     side_effect=start_tr_gen_plural)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.TRAFFIC_GENERATOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.TRAFFIC_GENERATOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.TRAFFIC_GENERATOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.TRAFFIC_GENERATOR_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.TRAFFIC_GENERATOR_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]

        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.TRAFFIC_GENERATOR_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.TRAFFIC_GENERATOR_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.START_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.TRAFFIC_GENERATOR_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_filebeat(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                              logged_in, logged_in_as_admin, get_em_ex, merged_info, start_f_beat,
                                              start_f_beat_plural, stop_f_beat_plural, stop_f_beat, config) -> None:
        """
        Testing the HTTPS GET method for the /emulation-executions/id/filebeat resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param start_tr_gen: the start_tr_gen fixture
        :param start_tr_gen_plural: the start_tr_gen_plural fixture
        :param stop_tr_gen_plural: the stop_tr_gen_plural fixture
        :param stop_tr_gen: the stop_tr_gen fixture
        :param config: the config fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_filebeat",
                     side_effect=stop_f_beat)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_filebeats",
                     side_effect=stop_f_beat_plural)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_filebeat",
                     side_effect=start_f_beat)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_filebeats",
                     side_effect=start_f_beat_plural)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.FILEBEAT_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.FILEBEAT_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.FILEBEAT_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.FILEBEAT_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.FILEBEAT_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]

        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.FILEBEAT_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.FILEBEAT_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.START_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.FILEBEAT_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_packetbeat(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                                logged_in, logged_in_as_admin, get_em_ex, merged_info, start_p_beat,
                                                start_p_beat_plural, stop_p_beat_plural, stop_p_beat, config) -> None:
        """
        Testing the HTTPS GET method for the /emulation-executions/id/packetbeat resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param start_tr_gen: the start_p_beat fixture
        :param start_tr_gen_plural: the start_p_beat_plural fixture
        :param stop_tr_gen_plural: the stop_p_beat_plural fixture
        :param stop_p_beat: the stop_p_beat fixture
        :param config: the config fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_packetbeat",
                     side_effect=stop_p_beat)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_packetbeats",
                     side_effect=stop_p_beat_plural)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_packetbeat",
                     side_effect=start_p_beat)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_packetbeats",
                     side_effect=start_p_beat_plural)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.PACKETBEAT_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.PACKETBEAT_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.PACKETBEAT_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.PACKETBEAT_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.PACKETBEAT_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]

        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.PACKETBEAT_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.PACKETBEAT_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.START_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.PACKETBEAT_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_metricbeat(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                                logged_in, logged_in_as_admin, get_em_ex, merged_info, start_m_beat,
                                                start_m_beat_plural, stop_m_beat_plural, stop_m_beat, config) -> None:
        """
        Testing the HTTPS GET method for the /emulation-executions/id/metricbeat resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param start_m_beat: the start_m_beat fixture
        :param start_m_beat_plural: the start_m_beat_plural fixture
        :param stop_m_breat_plural: the stop_m_beat_plural fixture
        :param stop_m_beat: the stop_m_beat fixture
        :param config: the config fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_metricbeat",
                     side_effect=stop_m_beat)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_metricbeats",
                     side_effect=stop_m_beat_plural)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_metricbeat",
                     side_effect=start_m_beat)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_metricbeats",
                     side_effect=start_m_beat_plural)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.METRICBEAT_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.METRICBEAT_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.METRICBEAT_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.METRICBEAT_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.METRICBEAT_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]

        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.METRICBEAT_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.METRICBEAT_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.START_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.METRICBEAT_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_heartbeat(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                               logged_in, logged_in_as_admin, get_em_ex, merged_info, start_h_beat,
                                               start_h_beat_plural, stop_h_beat_plural, stop_h_beat, config) -> None:
        """
        Testing the HTTPS GET method for the /emulation-executions/id/heartbeat resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param start_h_beat: the start_h_beat fixture
        :param start_h_beat_plural: the start_h_beat_plural fixture
        :param stop_h_breat_plural: the stop_h_beat_plural fixture
        :param stop_h_beat: the stop_h_beat fixture
        :param config: the config fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_heartbeat",
                     side_effect=stop_h_beat)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_heartbeats",
                     side_effect=stop_h_beat_plural)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_heartbeat",
                     side_effect=start_h_beat)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_heartbeats",
                     side_effect=start_h_beat_plural)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.HEARTBEAT_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.HEARTBEAT_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.HEARTBEAT_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.HEARTBEAT_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.HEARTBEAT_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]

        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.HEARTBEAT_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.HEARTBEAT_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.START_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.HEARTBEAT_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_ryu_mng(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                             logged_in, logged_in_as_admin, get_em_ex, merged_info, stop_ryu_mng,
                                             start_ryu_mng, list_ryu, create_ryu, config) -> None:
        """
        Testing the HTTPS GET method for the /emulation-executions/id/ryu-manager resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param list_ryu: the list_ryu fixture
        :param create_ryu: the create_ryu fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param stop_ryu_mng: the stop_ryu_mng fixture
        :param start_ryu_mng: the start_ryu_mng fixture
        :param config: the config fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.create_ryu_tunnel",
                     side_effect=create_ryu)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.list_ryu_tunnels",
                     side_effect=list_ryu)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_ryu_manager",
                     side_effect=stop_ryu_mng)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_ryu_manager",
                     side_effect=start_ryu_mng)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.RYU_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.RYU_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.RYU_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.RYU_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.RYU_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]

        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.RYU_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.RYU_MANAGER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.START_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.RYU_MANAGER_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_ryu_ctr(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                             logged_in, logged_in_as_admin, get_em_ex, merged_info, stop_ryu_ctr,
                                             start_ryu_ctr, list_ryu, create_ryu, remove_ryu_ctr, config) -> None:
        """
        Testing the HTTPS GET method for the /emulation-executions/id/ryu-controller resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param list_ryu: the list_ryu fixture
        :param create_ryu: the create_ryu fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param stop_ryu_ctr: the stop_ryu_ctr fixture
        :param start_ryu_ctr: the start_ryu_ctr fixture
        :param config: the config fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.create_ryu_tunnel",
                     side_effect=create_ryu)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.list_ryu_tunnels",
                     side_effect=list_ryu)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.remove_ryu_tunnel",
                     side_effect=remove_ryu_ctr)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_ryu",
                     side_effect=stop_ryu_ctr)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_ryu",
                     side_effect=start_ryu_ctr)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.RYU_CONTROLLER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.RYU_CONTROLLER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.RYU_CONTROLLER_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.RYU_CONTROLLER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            if k == "ryu_managers_info":
                for i in data_dict[k]:
                    if i == "ryu_managers_statuses":
                        assert data_dict[k][i][0]["monitor_running"] != \
                               exp_exec_info_dict[k][i][0]["monitor_running"]
            else:
                assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.RYU_CONTROLLER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            if k == "ryu_managers_info":
                for i in data_dict[k]:
                    if i == "ryu_managers_statuses":
                        assert data_dict[k][i][0]["monitor_running"] != \
                               exp_exec_info_dict[k][i][0]["monitor_running"]
            else:
                assert data_dict[k] == exp_exec_info_dict[k]

        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.RYU_CONTROLLER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            if k == "ryu_managers_info":
                for i in data_dict[k]:
                    if i == "ryu_managers_statuses":
                        assert data_dict[k][i][0]["monitor_running"] != \
                               exp_exec_info_dict[k][i][0]["monitor_running"]
            else:
                assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.RYU_CONTROLLER_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.START_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            if k == "ryu_managers_info":
                for i in data_dict[k]:
                    if i == "ryu_managers_statuses":
                        assert data_dict[k][i][0]["monitor_running"] != \
                               exp_exec_info_dict[k][i][0]["monitor_running"]
            else:
                assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.RYU_CONTROLLER_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_ryu_mon(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                             logged_in, logged_in_as_admin, get_em_ex,
                                             merged_info, stop_ryu_mon, start_ryu_mon, list_ryu,
                                             create_ryu, config) -> None:
        """
        Testing the HTTPS GET method for the /emulation-executions/id/ryu-monitor resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param list_ryu: the list_ryu fixture
        :param create_ryu: the create_ryu fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param stop_ryu_mon: the stop_ryu_mng fixture
        :param start_ryu_mon: the start_ryu_mng fixture
        :param config: the config fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.create_ryu_tunnel",
                     side_effect=create_ryu)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.list_ryu_tunnels",
                     side_effect=list_ryu)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.stop_ryu_monitor",
                     side_effect=stop_ryu_mon)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.start_ryu_monitor",
                     side_effect=start_ryu_mon)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.RYU_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.RYU_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.RYU_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({"bla": "bla"}))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert api_constants.MGMT_WEBAPP.REASON_PROPERTY in response_data_dict
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.RYU_MONITOR_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.RYU_MONITOR_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]

        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.RYU_MONITOR_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.STOP_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.RYU_MONITOR_SUBRESOURCE}"
                                                f"?{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY:
                                                                     api_constants.MGMT_WEBAPP.START_ALL_PROPERTY
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        format_data = EmulationExecutionInfo.from_dict(response_data_dict)
        data_dict = format_data.to_dict()
        exp_ex_info = TestResourcesEmulationExecutionsSuite.get_exec_info()
        exp_exec_info_dict = exp_ex_info.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == exp_exec_info_dict[k]
        response = flask_app.test_client().post(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                                f"{api_constants.MGMT_WEBAPP.RYU_MONITOR_SUBRESOURCE}",
                                                data=json.dumps({api_constants.MGMT_WEBAPP.START_PROPERTY: True,
                                                                 api_constants.MGMT_WEBAPP.STOP_PROPERTY: False,
                                                                 api_constants.MGMT_WEBAPP.IP_PROPERTY: "123.456.78.99"
                                                                 }))
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.BAD_REQUEST_STATUS_CODE
        assert response_data_dict == {}

    def test_emulation_execution_ids_switches(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                              logged_in, logged_in_as_admin, get_em_ex, get_mock, merged_info, list_ryu,
                                              create_ryu, config, exec_none) -> None:
        """
        Testing the HTTPS GET method for the /emulation-executions/id/switches resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_em_ex: the get_em_ex fixture
        :param list_ryu: the list_ryu fixture
        :param create_ryu: the create_ryu fixture
        :param merged_info: the merged_info fixture
        :param get_ex_exec: the get_ex_exec fixture
        :param stop_ryu_mon: the stop_ryu_mng fixture
        :param start_ryu_mon: the start_ryu_mng fixture
        :param config: the config fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.get_merged_execution_info",
                     side_effect=merged_info)
        mocker.patch("requests.get", side_effect=get_mock)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.create_ryu_tunnel",
                     side_effect=create_ryu)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.list_ryu_tunnels",
                     side_effect=list_ryu)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                               f"{api_constants.MGMT_WEBAPP.SWITCHES_SUBRESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                               f"{api_constants.MGMT_WEBAPP.SWITCHES_SUBRESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        ex_response = TestResourcesEmulationExecutionsSuite.response_returner()
        ex_dict = json.loads(ex_response.content)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict[api_constants.MGMT_WEBAPP.SDN_CONTROLLER_LOCAL_PORT] == 1
        response_switches = response_data_dict[api_constants.MGMT_WEBAPP.SWITCHES_SUBRESOURCE][0]
        assert response_switches[api_constants.MGMT_WEBAPP.AGG_FLOWS_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY][0]
        assert response_switches[api_constants.MGMT_WEBAPP.DESC_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY]
        assert response_switches[api_constants.MGMT_WEBAPP.DPID_PROPERTY] == \
               api_constants.MGMT_WEBAPP.DPID_PROPERTY
        assert response_switches[api_constants.MGMT_WEBAPP.FLOWS_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY]
        assert response_switches[api_constants.MGMT_WEBAPP.GROUP_DESCS_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY]
        assert response_switches[api_constants.MGMT_WEBAPP.GROUP_FEATURES_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY][0]
        assert response_switches[api_constants.MGMT_WEBAPP.GROUPS_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY]
        assert response_switches[api_constants.MGMT_WEBAPP.METER_CONFIGS_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY]
        assert response_switches[api_constants.MGMT_WEBAPP.METER_FEATURES_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY][0]
        assert response_switches[api_constants.MGMT_WEBAPP.METERS_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY]
        assert response_switches[api_constants.MGMT_WEBAPP.PORT_DESCS_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY]
        assert response_switches[api_constants.MGMT_WEBAPP.PORT_STATS_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY]
        assert response_switches[api_constants.MGMT_WEBAPP.QUEUE_CONFIGS_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY][0]
        assert response_switches[api_constants.MGMT_WEBAPP.QUEUES_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY]
        assert response_switches[api_constants.MGMT_WEBAPP.ROLES_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY][0]
        assert response_switches[api_constants.MGMT_WEBAPP.TABLE_FEATURES_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY]
        assert response_switches[api_constants.MGMT_WEBAPP.TABLES_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY]
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=exec_none)

        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                               f"{api_constants.MGMT_WEBAPP.SWITCHES_SUBRESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                               f"{api_constants.MGMT_WEBAPP.SWITCHES_SUBRESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        ex_response = TestResourcesEmulationExecutionsSuite.response_returner()
        ex_dict = json.loads(ex_response.content)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict[api_constants.MGMT_WEBAPP.SDN_CONTROLLER_LOCAL_PORT] == 1
        response_switches = response_data_dict[api_constants.MGMT_WEBAPP.SWITCHES_SUBRESOURCE][0]
        assert response_switches[api_constants.MGMT_WEBAPP.AGG_FLOWS_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY][0]
        assert response_switches[api_constants.MGMT_WEBAPP.DESC_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY]
        assert response_switches[api_constants.MGMT_WEBAPP.DPID_PROPERTY] == \
               api_constants.MGMT_WEBAPP.DPID_PROPERTY
        assert response_switches[api_constants.MGMT_WEBAPP.FLOWS_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY]
        assert response_switches[api_constants.MGMT_WEBAPP.GROUP_DESCS_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY]
        assert response_switches[api_constants.MGMT_WEBAPP.GROUP_FEATURES_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY][0]
        assert response_switches[api_constants.MGMT_WEBAPP.GROUPS_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY]
        assert response_switches[api_constants.MGMT_WEBAPP.METER_CONFIGS_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY]
        assert response_switches[api_constants.MGMT_WEBAPP.METER_FEATURES_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY][0]
        assert response_switches[api_constants.MGMT_WEBAPP.METERS_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY]
        assert response_switches[api_constants.MGMT_WEBAPP.PORT_DESCS_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY]
        assert response_switches[api_constants.MGMT_WEBAPP.PORT_STATS_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY]
        assert response_switches[api_constants.MGMT_WEBAPP.QUEUE_CONFIGS_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY][0]
        assert response_switches[api_constants.MGMT_WEBAPP.QUEUES_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY]
        assert response_switches[api_constants.MGMT_WEBAPP.ROLES_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY][0]
        assert response_switches[api_constants.MGMT_WEBAPP.TABLE_FEATURES_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY]
        assert response_switches[api_constants.MGMT_WEBAPP.TABLES_PROPERTY] == \
               ex_dict[api_constants.MGMT_WEBAPP.DPID_PROPERTY]

        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=exec_none)

        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMULATION_EXECUTIONS_RESOURCE}/-1/"
                                               f"{api_constants.MGMT_WEBAPP.SWITCHES_SUBRESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
