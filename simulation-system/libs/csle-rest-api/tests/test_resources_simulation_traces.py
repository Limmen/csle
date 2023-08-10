import json
from typing import List, Tuple

import csle_common.constants.constants as constants
import pytest
import pytest_mock
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace

import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesSimulationTracesSuite:
    """
    Test suite for /emulation-traces resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def list_sim_tr(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_simulation_traces method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def list_simulation_traces() -> List[SimulationTrace]:
            sim_tr = TestResourcesSimulationTracesSuite.get_ex_sim_trace()
            return [sim_tr]
        list_simulation_traces_mocker = mocker.MagicMock(side_effect=list_simulation_traces)
        return list_simulation_traces_mocker

    @pytest.fixture
    def list_sim_tr_ids(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_simulation_traces_ids method
        
        :param mocker the pytest mocker object
        :return: the mocked function
        """
        def list_simulation_traces_ids() -> List[Tuple[int, str]]:
            return [(1, "JDoeSimulation")]
        list_simulation_traces_ids_mocker = mocker.MagicMock(side_effect=list_simulation_traces_ids)
        return list_simulation_traces_ids_mocker

    @pytest.fixture
    def remove(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the remove_simulation_trace method
        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def remove_simulation_trace(simulation_trace: SimulationTrace) -> None:
            return None
        remove_simulation_trace_mocker = mocker.MagicMock(side_effect=remove_simulation_trace)
        return remove_simulation_trace_mocker

    @pytest.fixture
    def get_sim_tr(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_simulation_trace

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def get_simulation_trace(id: int) -> SimulationTrace:
            sim_tr = TestResourcesSimulationTracesSuite.get_ex_sim_trace()
            return sim_tr
        get_simulation_trace_mocker = mocker.MagicMock(side_effect=get_simulation_trace)
        return get_simulation_trace_mocker

    @staticmethod
    def get_ex_sim_trace():
        """
        Static help method for obtainng a SimulationTrace object
        
        :return: A SimulationTrace object
        """
        sim_trace = SimulationTrace(simulation_env="null")
        return sim_trace

    def test_simulation_traces_get(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                                   logged_in_as_admin, list_sim_tr, list_sim_tr_ids) -> None:
        """
        Testing the GET HTTPS for the /simulation-traces resource
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param list_sim_tr: the list_sim_tr fixture
        :param list_sim_tr_ids: the list_sim_tr_ids fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_simulation_traces",
                     side_effect=list_sim_tr)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_simulation_traces_ids",
                     side_effect=list_sim_tr_ids)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 1
        assert response_data_dict[api_constants.MGMT_WEBAPP.SIMULATION_PROPERTY] == "JDoeSimulation"
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        ex_sim_tr = TestResourcesSimulationTracesSuite.get_ex_sim_trace()
        ex_sim_tr_dict = ex_sim_tr.to_dict()
        for k in response_data_dict:
            assert response_data_dict[k] == ex_sim_tr_dict[k]
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 1
        assert response_data_dict[api_constants.MGMT_WEBAPP.SIMULATION_PROPERTY] == "JDoeSimulation"
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        ex_sim_tr = TestResourcesSimulationTracesSuite.get_ex_sim_trace()
        ex_sim_tr_dict = ex_sim_tr.to_dict()
        for k in response_data_dict:
            assert response_data_dict[k] == ex_sim_tr_dict[k]

    def test_simulation_traces_delete(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                                      logged_in_as_admin, list_sim_tr, remove) -> None:
        """
        Testing the DELETE HTTPS for the /simulation-traces resource
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param list_sim_tr: the list_sim_tr fixture
        :param list_sim_tr_ids: the list_sim_tr_ids fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_simulation_traces",
                     side_effect=list_sim_tr)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_simulation_trace",
                     side_effect=remove)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE

    def test_simulation_traces_ids_get(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                                       logged_in_as_admin, get_sim_tr) -> None:
        """
        Testing the GET HTTPS for the /simulation-traces/id resource
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_sim_tr: the get_sim_tr fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_simulation_trace",
                     side_effect=get_sim_tr)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        ex_sim_tr = TestResourcesSimulationTracesSuite.get_ex_sim_trace()
        ex_sim_tr_dict = ex_sim_tr.to_dict()
        for k in response_data_dict:
            assert response_data_dict[k] == ex_sim_tr_dict[k]
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        ex_sim_tr = TestResourcesSimulationTracesSuite.get_ex_sim_trace()
        ex_sim_tr_dict = ex_sim_tr.to_dict()
        for k in response_data_dict:
            assert response_data_dict[k] == ex_sim_tr_dict[k]

    def test_simulation_traces_ids_delete(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                                          logged_in_as_admin, get_sim_tr, remove) -> None:
        """
        Testing the DELETE HTTPS for the /simulation-traces/id resource
        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in: the logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_sim_tr: the get_sim_tr fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_simulation_trace",
                     side_effect=get_sim_tr)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_simulation_trace",
                     side_effect=remove)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.SIMULATION_TRACES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
