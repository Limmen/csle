import json
import logging
from typing import List, Tuple

import csle_common.constants.constants as constants
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
from csle_common.dao.emulation_config.packet_delay_distribution_type import (
    PacketDelayDistributionType,
)

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
            snort_ids = SnortIdsManagersInfoDTO(ips="abcdef", ports=2, emulationName="abcdef",
                                                executionId=[2], snortIdsManagersRunning=False,
                                                snortIdsManagersStatuses=[SnortIdsStatusDTO(monitor_running=False,
                                                                                            snort_ids_running=True)])
            ossec_ids = OSSECIdsManagersInfoDTO(ips="123.456.78.99", ports=5,
                                                emulationName="JohnDoe", executionId=4,
                                                ossecIdsManagersRunning=True,
                                                ossecIdsManagersStatuses=OSSECIdsStatusDTO(monitor_running=True,
                                                                                           ossec_ids_running=False))
            kafka_mng = KafkaManagersInfoDTO(ips="123.456.78.99", ports=5,
                                             emulationName="JohnDoe",
                                             executionId=1, kafkaManagersRunning=True,
                                             kafkaManagersStatuses=KafkaStatusDTO(running=True, topics="abcdef"))
            host_mng = HostManagersInfoDTO(ips="123.456.78.99", ports=5,
                                           emulationName="JohnDoe",
                                           executionId=5,
                                           hostManagersRunning=True,
                                           hostManagersStatuses=HostManagerStatusDTO(monitor_running=True,
                                                                                     filebeat_running=True,
                                                                                     packetbeat_running=True,
                                                                                     metricbeat_running=True,
                                                                                     heartbeat_running=True,
                                                                                     ip="123.456.78.99"))
            client_mng = ClientManagersInfoDTO(ips="123.456.78.99",
                                               ports=5,
                                               emulationName="JohnDoe",
                                               executionId=5,
                                               clientManagersRunning=True,
                                               clientManagersStatuses=GetNumClientsDTO(num_clients=1,
                                                                                       client_process_active=True,
                                                                                       producer_active=True,
                                                                                       clients_time_step_len_seconds=15,
                                                                                       producer_time_step_len_seconds=10))
            docker_mng = DockerStatsManagersInfoDTO(ips="123.456.78.99", ports=5,
                                                    emulationName="JohnDoe",
                                                    executionId=5,
                                                    dockerStatsManagersRunning=True,
                                                    dockerStatsManagersStatuses=DockerStatsMonitorStatusDTO(num_monitors=1,
                                                                                                            emulations="null",
                                                                                                            emulation_executions=15))
            running_cont = RunningContainersDTO(DockerContainerDTO(name="JohnDoe",
                                                                   image="null",
                                                                   ip="123.456.78.99"))
            stopped_cont = StoppedContainersDTO(stoppedContainers=DockerContainerDTO(name="JohnDoe",
                                                                                   image="null",
                                                                                   ip="123.456.78.99"))
            traffic_info = TrafficManagersInfoDTO(ips="123..456.78.99",
                                                  ports=5,
                                                  emulationName="JohnDoe",
                                                  executionId=5,
                                                  trafficManagersRunning=True,
                                                  trafficManagersStatuses=TrafficManagerInfoDTO(runnning=True,
                                                                                                script="null"))
            docker_net = DockerNetworksDTO(networks="abcdef", network_ids=5)
            elk_mng = ElkManagersInfoDTO(ips="123.456.78.99", ports=5,
                                         emulationName="JohnDoe", executionId=5,
                                         elkManagersRunning=True,
                                         elkManagersStatuses=ElkStatusDTO(elasticRunning=True,
                                                                          kibanaRunning=True,
                                                                          logstashRunning=True))
            ryu_mng = RyuManagersInfoDTO(ips="123.456.78.99", ports=5,
                                         emulationName="JohnDoe", executionId=5,
                                         ryuManagersRunning=True,
                                         ryuManagersStatuses=RyuManagerStatusDTO(ryu_running=True,
                                                                                 monitor_running=True,
                                                                                 port=5,
                                                                                 web_port=4,
                                                                                 controller="null",
                                                                                 kafka_ip="123.456.78.99",
                                                                                 kafka_port=5,
                                                                                 time_step_len=10))
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
            return RyuTunnelsDTO(tunnels=RyuTunnelDTO(port=1,
                                                      ip="123.456.78.99",
                                                      emulation="null",
                                                      ipFirstOctet=-1))
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

    def test_emulation_execution_ids_info_get(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                                              logged_in_as_admin, get_em_ex, emulation_exec, get_ex_exec, merged_info,
                                              kibana_list, kibana, create_ryu, list_ryu, ):
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
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in)
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
        response_data_list = json.loads(response_data)
        logger.info(response.status_code)
        logger.info(response_data_list)
