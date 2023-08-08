from typing import List, Tuple
import json
import pytest
import pytest_mock
import csle_common.constants.constants as constants
from csle_common.dao.system_identification.empirical_conditional import EmpiricalConditional
from csle_common.dao.system_identification.empirical_system_model import EmpiricalSystemModel
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesESMModelsSuite:
    """
    Test suite for /empirical-system-models resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")
    
    @pytest.fixture
    def list_esm_ids(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_empirical_system_models_ids method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def list_empirical_system_models_ids() -> List[Tuple[int, int, int]]:
            return [(1, 1, 1)]
        list_empirical_system_models_ids_mocker = mocker.MagicMock(
            side_effect=list_empirical_system_models_ids)
        return list_empirical_system_models_ids_mocker

    @pytest.fixture
    def list_esm(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_empirical_system_models method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def list_empirical_system_models() -> List[EmpiricalSystemModel]:
            esm_model = TestResourcesESMModelsSuite.get_example_esm()
            return [esm_model]
        list_empirical_system_models_mocker = mocker.MagicMock(side_effect=list_empirical_system_models)
        return list_empirical_system_models_mocker

    @pytest.fixture
    def remove(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for the remove_empirical_system_model method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def remove_empirical_system_model(empirical_system_model: EmpiricalSystemModel) -> None:
            return None
        remove_empirical_system_model_mocker = mocker.MagicMock(side_effect=remove_empirical_system_model)
        return remove_empirical_system_model_mocker

    @pytest.fixture
    def get_esm_config(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for the get_empirical_system_model_config method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def get_empirical_system_model_config(id: int) -> EmpiricalSystemModel:
            esm_model = TestResourcesESMModelsSuite.get_example_esm()
            return esm_model
        get_empirical_system_model_config_mocker = mocker.MagicMock(side_effect=get_empirical_system_model_config)
        return get_empirical_system_model_config_mocker

    @pytest.fixture
    def get_esm_config_none(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for the get_empirical_system_model_config method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def get_empirical_system_model_config(id: int) -> None:
            return None
        get_empirical_system_model_config_mocker = mocker.MagicMock(side_effect=get_empirical_system_model_config)
        return get_empirical_system_model_config_mocker

    @staticmethod
    def get_example_esm() -> EmpiricalSystemModel:
        """
        Helper function that creates an example empirical system model for mocking

        :return: the example empirical system model
        """
        e_cond = EmpiricalConditional(conditional_name="JohnDoe",
                                      metric_name="JDoeMetric",
                                      sample_space=[10],
                                      probabilities=[1.0])
        esm_model = EmpiricalSystemModel(emulation_env_name="JohnDoe",
                                         emulation_statistic_id=1,
                                         conditional_metric_distributions=[[e_cond]],
                                         descr="null")
        return esm_model

    def test_empirical_system_models_get(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                                         logged_in_as_admin, list_esm_ids, list_esm) -> None:
        """
        Tests the GET HTTPS method for the /empirical-system-models resource

        :param flask_app: the pytest flask app for making requests
        :param mocker: the pytest mocker object
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param list_esm: the list_esm fixture
        :param list_esm_ids: the list_esm_ids fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_empirical_system_models_ids",
                     side_effect=list_esm_ids)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_empirical_system_models",
                     side_effect=list_esm)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODELS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode('utf-8')
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODELS_RESOURCE}")
        response_data = response.data.decode('utf-8')
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODELS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 1
        assert response_data_dict[api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == 1
        assert response_data_dict[api_constants.MGMT_WEBAPP.STATISTIC_ID_PROPERTY] == 1
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODELS_RESOURCE}")
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        ex_esm_data = TestResourcesESMModelsSuite.get_example_esm()
        ex_esm_data_dict = ex_esm_data.to_dict()
        for k in response_data_dict:
            assert response_data_dict[k] == ex_esm_data_dict[k]
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODELS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 1
        assert response_data_dict[api_constants.MGMT_WEBAPP.EMULATION_PROPERTY] == 1
        assert response_data_dict[api_constants.MGMT_WEBAPP.STATISTIC_ID_PROPERTY] == 1
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODELS_RESOURCE}")
        response_data = response.data.decode('utf-8')
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        ex_esm_data = TestResourcesESMModelsSuite.get_example_esm()
        ex_esm_data_dict = ex_esm_data.to_dict()
        for k in response_data_dict:
            assert response_data_dict[k] == ex_esm_data_dict[k]

    def test_empirical_system_models_delete(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                                            logged_in_as_admin, remove, list_esm) -> None:
        """
        Tests the DELETE HTTPS method for the /empirical-system-models resource

        :param flask_app: the pytest flask app for making requests
        :param mocker: the pytest mocker object
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param list_esm: the list_esm fixture
        :param remove: the remove fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_empirical_system_models",
                     side_effect=list_esm)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_empirical_system_model",
                     side_effect=remove)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODELS_RESOURCE}")
        response_data = response.data.decode('utf-8')
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODELS_RESOURCE}")
        response_data = response.data.decode('utf-8')
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODELS_RESOURCE}")
        response_data = response.data.decode('utf-8')
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE

    def test_empirical_system_models_ids_get(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in, logged_in,
                                             logged_in_as_admin, get_esm_config, get_esm_config_none) -> None:
        """
        Tests the GET HTTPS method for the /empirical-system-models/id resource

        :param flask_app: the pytest flask app for making requests
        :param mocker: the pytest mocker object
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param list_esm: the list_esm fixture
        :param list_esm_ids: the list_esm_ids fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_empirical_system_model_config",
                     side_effect=get_esm_config)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODELS_RESOURCE}/10")
        response_data = response.data.decode('utf-8')
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODELS_RESOURCE}/10")
        response_data = response.data.decode('utf-8')
        response_data_dict = json.loads(response_data)
        ex_esm_data = TestResourcesESMModelsSuite.get_example_esm()
        ex_esm_data_dict = ex_esm_data.to_dict()
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for k in response_data_dict:
            assert response_data_dict[k] == ex_esm_data_dict[k]
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_empirical_system_model_config",
                     side_effect=get_esm_config_none)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODELS_RESOURCE}/10")
        response_data = response.data.decode('utf-8')
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_empirical_system_model_config",
                     side_effect=get_esm_config)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODELS_RESOURCE}/10")
        response_data = response.data.decode('utf-8')
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for k in response_data_dict:
            assert response_data_dict[k] == ex_esm_data_dict[k]
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_empirical_system_model_config",
                     side_effect=get_esm_config_none)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODELS_RESOURCE}/10")
        response_data = response.data.decode('utf-8')
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict == {}

    def test_empirical_system_models_ids_delete(self, mocker: pytest_mock.MockFixture, flask_app, not_logged_in,
                                                logged_in, logged_in_as_admin, get_esm_config, remove,
                                                get_esm_config_none):
        """
        Tests the DELETE HTTPS method for the /empirical-system-models/id resource

        :param flask_app: the pytest flask app for making requests
        :param mocker: the pytest mocker object
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param list_esm: the list_esm fixture
        :param list_esm_ids: the list_esm_ids fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_empirical_system_model_config",
                     side_effect=get_esm_config)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_empirical_system_model",
                     side_effect=remove)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODELS_RESOURCE}/10")
        response_data = response.data.decode('utf-8')
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODELS_RESOURCE}/10")
        response_data = response.data.decode('utf-8')
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODELS_RESOURCE}/10")
        response_data = response.data.decode('utf-8')
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_empirical_system_model_config",
                     side_effect=get_esm_config_none)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.EMPIRICAL_SYSTEM_MODELS_RESOURCE}/10")
        response_data = response.data.decode('utf-8')
        response_data_dict = json.loads(response_data)
        assert response_data_dict == {}
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
