from typing import List, Tuple
import json
import pytest
import pytest_mock
import csle_common.constants.constants as constants
from csle_cluster.cluster_manager.cluster_manager_pb2 import RunningEmulationsDTO
from csle_common.dao.emulation_config.config import Config
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.emulation_execution import EmulationExecution
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesSDNControllersSuite:
    """
    Test suite for /dsn-controllers resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

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

    def test_sdn_controllers_get(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                 logged_in, emulation_exec, emulation_exec_ids, running_emulations, config, get_em_ex,
                                 get_ex_exec) -> None:
        """
        Testing the GET HTTPS method for the /sdn-controllers resource
        
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param emulation_exec: the emulation_exec fixture
        :param emulation_exec_ids: the emulation_exec_ids fixture
        :param running_emulations: the running_emulations fixture
        :param config: the config fixture
        :param get_em_ex: the get_em_ex fixture
        """
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_config", side_effect=config)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulation_executions",
                     side_effect=emulation_exec)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_emulation_execution_ids",
                     side_effect=emulation_exec_ids)
        mocker.patch("csle_cluster.cluster_manager.cluster_controller.ClusterController.list_all_running_emulations",
                     side_effect=running_emulations)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_execution",
                     side_effect=get_em_ex)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.SDN_CONTROLLERS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.SDN_CONTROLLERS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        data = EmulationExecution.from_dict(response_data_dict)
        data_dict = data.to_dict()
        ex_exec = get_ex_exec
        ex_exec_dict = ex_exec.to_dict()
        for k in response_data_dict:
            assert data_dict[k] == ex_exec_dict[k]
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SDN_CONTROLLERS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        assert response_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 10
        assert response_data_dict[api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == 'a'
        assert response_data_dict[api_constants.MGMT_WEBAPP.RUNNING_PROPERTY] is True
