from typing import Dict, List, Tuple
import json
import pytest
import pytest_mock
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesSystemModelsSuite:
    """
    Test suite for /system-identification-jobs resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def list_g_m_m_ids(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_system_identification_jobs function

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """

        def list_gaussian_mixture_system_models_ids() -> List[Tuple[str, int, int, str]]:
            t = ("csle-level-10", 1, 10, "JDoe_gauss_mix")
            l = [t]
            return l

        list_gaussian_mixture_system_models_ids_mocker = mocker.MagicMock(
            side_effect=list_gaussian_mixture_system_models_ids)
        return list_gaussian_mixture_system_models_ids_mocker

    @pytest.fixture
    def list_e_s_m_ids(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_empirical_system_models_ids function

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """

        def list_empirical_system_models_ids() -> List[Tuple[str, int, int, str]]:
            t = ("csle-level-10", 1, 10, "JDoe_empirical_systems")
            l = [t]
            return l

        list_empirical_system_models_ids_mocker = mocker.MagicMock(side_effect=list_empirical_system_models_ids)
        return list_empirical_system_models_ids_mocker

    @pytest.fixture
    def list_gp_s_m_ids(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_gp_s_m_ids function

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """

        def list_gp_system_models_ids() -> List[Tuple[str, int, int, str]]:
            t = ("csle-level-10", 1, 10, "JDoe_gp_system")
            l = [t]
            return l

        list_gp_system_models_ids_mocker = mocker.MagicMock(side_effect=list_gp_system_models_ids)
        return list_gp_system_models_ids_mocker

    @pytest.fixture
    def list_mcmc_s_m_ids(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_mcmc_s_m_ids function

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """

        def list_mcmc_system_models_ids() -> List[Tuple[str, int, int, str]]:
            t = ("csle-level-10", 1, 10, "JDoe_mcmc")
            l = [t]
            return l

        list_mcmc_system_models_ids_mocker = mocker.MagicMock(side_effect=list_mcmc_system_models_ids)
        return list_mcmc_system_models_ids_mocker

    @staticmethod
    def example_returner() -> List[Dict[str, object]]:
        """
        Utility function that gives an eaxmple of the return value from the system models resource

        :return: the example return
        """
        response_dicts = [{api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM: 1,
                           api_constants.MGMT_WEBAPP.ID_PROPERTY: 'csle-level-10',
                           api_constants.MGMT_WEBAPP.STATISTIC_ID_PROPERTY: 10,
                           api_constants.MGMT_WEBAPP.SYSTEM_MODEL_TYPE:
                               api_constants.MGMT_WEBAPP.GAUSSIAN_MIXTURE_SYSTEM_MODEL_TYPE},
                          {api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM: 1,
                           api_constants.MGMT_WEBAPP.ID_PROPERTY: 'csle-level-10',
                           api_constants.MGMT_WEBAPP.STATISTIC_ID_PROPERTY: 10,
                           api_constants.MGMT_WEBAPP.SYSTEM_MODEL_TYPE:
                               api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODEL_TYPE},
                          {api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM: 1,
                           api_constants.MGMT_WEBAPP.ID_PROPERTY: 'csle-level-10',
                           api_constants.MGMT_WEBAPP.STATISTIC_ID_PROPERTY: 10,
                           api_constants.MGMT_WEBAPP.SYSTEM_MODEL_TYPE:
                               api_constants.MGMT_WEBAPP.GP_SYSTEM_MODEL_TYPE},
                          {api_constants.MGMT_WEBAPP.EMULATION_QUERY_PARAM: 1,
                           api_constants.MGMT_WEBAPP.ID_PROPERTY: 'csle-level-10',
                           api_constants.MGMT_WEBAPP.STATISTIC_ID_PROPERTY: 10,
                           api_constants.MGMT_WEBAPP.SYSTEM_MODEL_TYPE:
                               api_constants.MGMT_WEBAPP.MCMC_SYSTEM_MODEL_TYPE}]
        return response_dicts

    def test_s_m_get(self, flask_app, mocker: pytest_mock.MockFixture,
                     logged_in, not_logged_in, logged_in_as_admin,
                     list_mcmc_s_m_ids, list_gp_s_m_ids, list_e_s_m_ids,
                     list_g_m_m_ids) -> None:
        """
        Testing for the GET HTTPS method in the /system-models resource

        :param flask_app: the flask app for making test requests
        :param mocker: the pytest mocker object
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param list_mcmc_s_m_ids: the list_mcmc_s_m_ids fixture
        :param list_gp_s_m_ids: the list_gp_s_m_ids fixture
        :param list_e_s_m_ids: the list_e_s_m_ids fixture
        :param list_g_m_m_ids: the list_g_m_m_ids fixture
        :return: None
        """
        test_dicts = TestResourcesSystemModelsSuite.example_returner()

        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_gaussian_mixture_system_models_ids",
                     side_effect=list_g_m_m_ids)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_empirical_system_models_ids",
                     side_effect=list_e_s_m_ids)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_gp_system_models_ids",
                     side_effect=list_gp_s_m_ids)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_mcmc_system_models_ids",
                     side_effect=list_mcmc_s_m_ids)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SYSTEM_MODELS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SYSTEM_MODELS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for i in range(len(response_data_list)):
            for j in response_data_list[i]:
                assert response_data_list[i][j] == test_dicts[i][j]
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SYSTEM_MODELS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SYSTEM_MODELS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for i in range(len(response_data_list)):
            for j in response_data_list[i]:
                assert response_data_list[i][j] == test_dicts[i][j]
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SYSTEM_MODELS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}
