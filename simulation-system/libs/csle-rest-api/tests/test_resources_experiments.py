from typing import List, Tuple
import json

import pytest_mock

import csle_common.constants.constants as constants
import pytest
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType

import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesExperimentsSuite:
    """
    Test suite for /experiments url
    """

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def executions(self, mocker):
        """
        pytest fixture for mocking the list_experiment_executions function
        :param mocker: the pytest mocker object
        :return: mocked version of the function
        """

        def list_experiment_executions() -> List[ExperimentExecution]:
            exp_ex = TestResourcesExperimentsSuite.get_example_exp()
            list_e_e = [exp_ex]
            return list_e_e

        list_experiment_executions_mocker = mocker.MagicMock(
            side_effect=list_experiment_executions)
        return list_experiment_executions_mocker

    @pytest.fixture
    def get_execution(self, mocker):
        """
        pytest fixture for mocking the get_experiment_execution function
        :param mocker: the pytest mocker object
        :return: the mocked bersion ofthe function
        """

        def get_experiment_execution(id: int) -> ExperimentExecution:
            exp_ex = TestResourcesExperimentsSuite.get_example_exp()
            return exp_ex

        get_experiment_execution_mocker = mocker.MagicMock(
            side_effect=get_experiment_execution)
        return get_experiment_execution_mocker

    @staticmethod
    def get_example_exp() -> ExperimentExecution:
        """
        Static help method the returns an example experiment execution
        :return: ExperimentExecution class
        """
        h_param = HParam(value=1.5, name="JohnDoe", descr="null")
        exp_res = ExperimentResult()
        exp_conf = ExperimentConfig(output_dir="null",
                                    title="JDoeTitle",
                                    random_seeds=[1],
                                    agent_type=AgentType(0),
                                    hparams={"param": h_param},
                                    log_every=10,
                                    player_type=PlayerType(1),
                                    player_idx=5,
                                    br_log_every=10)
        exp_ex = ExperimentExecution(config=exp_conf,
                                     result=exp_res,
                                     timestamp=5.5,
                                     emulation_name="JDoeEmulation",
                                     simulation_name="JDoeSimulation",
                                     descr="null",
                                     log_file_path="null")
        return exp_ex

    @pytest.fixture
    def executions_ids(self, mocker):
        """
        pytest fixture for mocking the list_experiment_executions_ids function
        :param mocker: the pytest mocker object
        :return: mocked version of the function
        """

        def list_experiment_executions_ids() -> List[Tuple[int, str, str]]:
            lustle = [(4242, 'csle-level0-000', "csle-JDoe-Defender")]
            return lustle

        list_experiment_executions_ids_mocker = mocker.MagicMock(
            side_effect=list_experiment_executions_ids)
        return list_experiment_executions_ids_mocker

    @pytest.fixture
    def remove(self, mocker):
        """
        pytest fixture for mocking the remove_experiment_execution function
        :param mocker: the pytest mocker object
        :return: Mocked function
        """

        def remove_experiment_execution(experiment_execution: ExperimentExecution) -> None:
            return None

        remove_experiment_execution_mocker = mocker.MagicMock(side_effect=remove_experiment_execution)
        return remove_experiment_execution_mocker

    def test_exp_get(self, mocker, flask_app,
                     executions, executions_ids,
                     logged_in, not_logged_in,
                     logged_in_as_admin) -> None:
        """
        test function for the /experiments resource
        :param flask_app: the pytest flask app for making requests
        :param mocker: the pytest mocker object
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        """
        test_e_e = TestResourcesExperimentsSuite.get_example_exp()
        test_e_e_dict = test_e_e.to_dict()
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "list_experiment_executions", side_effect=executions)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "list_experiment_executions_ids", side_effect=executions_ids)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response_data_list[0][api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == 'csle-JDoe-Defender'
        assert response_data_list[0][api_constants.MGMT_WEBAPP.ID_PROPERTY] == 4242
        assert response_data_list[0][api_constants.MGMT_WEBAPP.SIMULATION_PROPERTY] == 'csle-level0-000'
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        for k in response_data_dict:
            assert response_data_dict[k] == test_e_e_dict[k]
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response_data_list[0][api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == 'csle-JDoe-Defender'
        assert response_data_list[0][api_constants.MGMT_WEBAPP.ID_PROPERTY] == 4242
        assert response_data_list[0][api_constants.MGMT_WEBAPP.SIMULATION_PROPERTY] == 'csle-level0-000'
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        for k in response_data_dict:
            assert response_data_dict[k] == test_e_e_dict[k]

    def test_exp_delete(self, mocker: pytest_mock.MockerFixture, flask_app, executions, executions_ids, logged_in,
                        not_logged_in, logged_in_as_admin, remove) -> None:
        """
        test function for the /experiments resource
        :param flask_app: the pytest flask app for making requests
        :param mocker: the pytest mocker object
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_experiment_executions",
                     side_effect=executions)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_experiment_execution",
                     side_effect=remove)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}

    def test_exp_ids_get(self, mocker: pytest_mock.MockerFixture, flask_app, get_execution, logged_in, not_logged_in,
                         logged_in_as_admin) -> None:
        """
        test function for the /experiments resource
        :param flask_app: the pytest flask app for making requests
        :param mocker: the pytest mocker object
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        """
        test_e_e = TestResourcesExperimentsSuite.get_example_exp()
        test_e_e_dict = test_e_e.to_dict()
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_experiment_execution",
                     side_effect=get_execution)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for k in response_data_dict:
            assert response_data_dict[k] == test_e_e_dict[k]
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for k in response_data_dict:
            assert response_data_dict[k] == test_e_e_dict[k]

    def test_exp_ids_delete(self, mocker: pytest_mock.MockerFixture, flask_app, get_execution, logged_in, not_logged_in,
                            logged_in_as_admin, remove) -> None:
        """
        test function for the /experiments resource
        :param flask_app: the pytest flask app for making requests
        :param mocker: the pytest mocker object
        :param get_execution: the get_execution fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_experiment_execution",
                     side_effect=get_execution)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_experiment_execution",
                     side_effect=remove)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EXPERIMENTS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict == {}
