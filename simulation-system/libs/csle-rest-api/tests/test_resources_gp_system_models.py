from typing import Dict, List, Tuple
import json
import csle_common.constants.constants as constants
import pytest
from csle_common.dao.system_identification.gp_conditional import GPConditional
from csle_common.dao.system_identification.gp_system_model import GPSystemModel
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesGPSystemModelsSuite:
    """
    Test suite for /system-identification-jobs resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def list_gp_s_m(self, mocker):
        """
        Pytest fixture for mocking the list_gp_system_models function
        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """

        def list_gp_system_models() -> List[GPSystemModel]:
            g_m_sys_mod = TestResourcesGPSystemModelsSuite.example_returner()
            return [g_m_sys_mod]

        list_gp_system_models_mocker = mocker.MagicMock(
            side_effect=list_gp_system_models)
        return list_gp_system_models_mocker

    @pytest.fixture
    def list_g_m_m_ids(self, mocker):
        """
        Pytest fixture for mocking the list_gaussian_mixture_system_models_ids function
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
    def list_e_s_m_ids(self, mocker):
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
    def get_gp_sys_mod_config(self, mocker):
        """
        pytest fixture for mocking the get_gp_system_model_config function
        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """

        def get_gp_system_model_config(id: int) -> GPSystemModel:
            g_p_sys_mod = TestResourcesGPSystemModelsSuite.example_returner()
            return g_p_sys_mod

        get_gp_system_model_config_mocker = mocker.MagicMock(
            side_effect=get_gp_system_model_config)

        return get_gp_system_model_config_mocker

    @pytest.fixture
    def list_gp_s_m_ids(self, mocker):
        """
        Pytest fixture for mocking the list_gp_system_models_ids function
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
    def list_mcmc_s_m_ids(self, mocker):
        """
        Pytest fixture for mocking the list_mcmc_system_models_ids function
        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """

        def list_mcmc_system_models_ids() -> List[Tuple[str, int, int, str]]:
            t = ("csle-level-10", 1, 10, "JDoe_mcmc")
            l = [t]
            return l

        list_mcmc_system_models_ids_mocker = mocker.MagicMock(side_effect=list_mcmc_system_models_ids)
        return list_mcmc_system_models_ids_mocker

    @pytest.fixture
    def remove(self, mocker):
        """
        pytest fixture for mocking the remove_gp_system_model function
        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """

        def remove_gp_system_model(gp_system_model: GPSystemModel) -> None:
            return None

        remove_gp_system_model_mocker = mocker.MagicMock(
            side_effect=remove_gp_system_model)
        return remove_gp_system_model_mocker

    @staticmethod
    def example_sys_mod() -> List[Dict[str, object]]:
        """
        Static method for returning an example list of response dicts

        :return: An example list of a System model dictionary
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

    @staticmethod
    def example_returner() -> GPSystemModel:
        """
        Static help method for returning an example GP System Model

        :return: an example GPSystemModel
        """
        gp_cond = GPConditional(conditional_name="JohndoeConditional", metric_name="JohnDoeMetric",
                                sample_space=[5], observed_x=[10.0],
                                observed_y=[10], scale_parameter=1.1,
                                noise_parameter=1.1)

        g_m_sys_mod = GPSystemModel(emulation_env_name="JohnDoeEmulation",
                                    emulation_statistic_id=10,
                                    conditional_metric_distributions=[[gp_cond]],
                                    descr="null")
        return g_m_sys_mod

    def test_gp_s_m_get(self, flask_app, mocker,
                        logged_in, not_logged_in, logged_in_as_admin,
                        list_g_m_m_ids, list_e_s_m_ids, list_gp_s_m_ids,
                        list_mcmc_s_m_ids, list_gp_s_m) -> None:
        """
        Testing for the GET HTTPS method in the /gp-system-models resource
        :param flask_app: the pytest flask app for making requests
        :param mocker: the pytest mocker object
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param list_g_m_m_ids: the list_g_m_m_ids fixture
        :param list_e_s_m_ids: the list_e_s_m_ids fixture
        :param list_gp_s_m_ids: the list_gp_s_m_ids fixture
        :param list_mcmc_s_m_ids: the list_mcmc_s_m_ids fixture
        :param list_g_m_m: the list_g_m_m fixture
        :return: None
        """
        test_obj = TestResourcesGPSystemModelsSuite.example_returner()
        test_obj_dict = test_obj.to_dict()
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in, )
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "list_gp_system_models",
                     side_effect=list_gp_s_m)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "list_empirical_system_models_ids",
                     side_effect=list_e_s_m_ids)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "list_gp_system_models_ids",
                     side_effect=list_gp_s_m_ids)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "list_mcmc_system_models_ids",
                     side_effect=list_mcmc_s_m_ids)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "list_gaussian_mixture_system_models_ids",
                     side_effect=list_g_m_m_ids)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.GP_SYSTEM_MODELS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in, )
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.GP_SYSTEM_MODELS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        test_dicts = TestResourcesGPSystemModelsSuite.example_sys_mod()
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for i in range(len(response_data_list)):
            for j in response_data_list[i]:
                assert response_data_list[i][j] == test_dicts[i][j]
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.GP_SYSTEM_MODELS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        gp_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for i in (gp_data_dict):
            assert gp_data_dict[i] == test_obj_dict[i]
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin, )
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.GP_SYSTEM_MODELS_RESOURCE}")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        gp_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for i in (gp_data_dict):
            assert gp_data_dict[i] == test_obj_dict[i]
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.GP_SYSTEM_MODELS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        test_dicts = TestResourcesGPSystemModelsSuite.example_sys_mod()
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for i in range(len(response_data_list)):
            for j in response_data_list[i]:
                assert response_data_list[i][j] == test_dicts[i][j]

    def test_gp_s_m_delete(self, flask_app, mocker,
                           logged_in, not_logged_in, logged_in_as_admin,
                           list_gp_s_m, remove) -> None:
        """
        Testing for the DELETE HTTPS method in the /gp-system-models resource
        :param flask_app: the pytest flask app for making requests
        :param mocker: the pytest mocker object
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param list_gp_s_m: the list_gp_s_m fixture
        :return: None
        """
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in, )
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "list_gp_system_models",
                     side_effect=list_gp_s_m)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "remove_gp_system_model",
                     side_effect=remove)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.GP_SYSTEM_MODELS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in, )
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.GP_SYSTEM_MODELS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE

        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin, )
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.GP_SYSTEM_MODELS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE

    def test_gp_s_m_ids_get(self, flask_app, mocker,
                            logged_in, not_logged_in, logged_in_as_admin,
                            get_gp_sys_mod_config):
        """
        Testing for the GET HTTPS method in the /gp-system-models/id resource
        :param flask_app: the pytest flask app for making requests
        :param mocker: the pytest mocker object
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param get_gp_sys_mod_config: the get_gp_sys_mod_config fixture
        :return: None
        """
        test_obj = TestResourcesGPSystemModelsSuite.example_returner()
        test_obj_dict = test_obj.to_dict()
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in, )
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "get_gp_system_model_config",
                     side_effect=get_gp_sys_mod_config)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.GP_SYSTEM_MODELS_RESOURCE}"
                                               "/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in, )
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.GP_SYSTEM_MODELS_RESOURCE}"
                                               "/10")
        response_data = response.data.decode("utf-8")
        gp_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for i in (gp_data_dict):
            assert gp_data_dict[i] == test_obj_dict[i]
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin, )
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.GP_SYSTEM_MODELS_RESOURCE}"
                                               "/10")
        response_data = response.data.decode("utf-8")
        gp_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for i in (gp_data_dict):
            assert gp_data_dict[i] == test_obj_dict[i]

    def test_gp_s_m_ids_delete(self, flask_app, mocker,
                               logged_in, not_logged_in, logged_in_as_admin,
                               get_gp_sys_mod_config,
                               remove):
        """
        Testing for the DELETE HTTPS method in the /gp-system-models/id resource
        :param flask_app: the pytest flask app for making requests
        :param mocker: the pytest mocker object
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param get_gp_sys_mod_config: the get_gp_sys_mod_config fixture
        :return: None
        """
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in, )
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "get_gp_system_model_config",
                     side_effect=get_gp_sys_mod_config)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "remove_gp_system_model",
                     side_effect=remove)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.GP_SYSTEM_MODELS_RESOURCE}"
                                                  "/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in, )
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.GP_SYSTEM_MODELS_RESOURCE}"
                                                  "/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin, )
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.GP_SYSTEM_MODELS_RESOURCE}"
                                                  "/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
