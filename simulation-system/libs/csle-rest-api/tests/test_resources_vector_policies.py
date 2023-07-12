from typing import List, Tuple
import json
import pytest
import pytest_mock
import csle_common.constants.constants as constants
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.training.vector_policy import VectorPolicy

import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesVectorPoliciesSuite:
    """
    Test suite for /vector-policies resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def list_vector_ids(self, mocker: pytest_mock.MockFixture):
        """
        Fixture for mocking the list_vector_policies_ids function

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """
        def list_vector_policies_ids() -> List[Tuple[int, str]]:
            policy_id = (111, "some_simulation")
            return [policy_id]
        list_vector_ids_mocker = mocker.MagicMock(side_effect=list_vector_policies_ids)
        return list_vector_ids_mocker

    @pytest.fixture
    def list_vector(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_vector_policies function

        :param mocker: the pytest mock object
        :return: a mock object with the mocked function
        """
        def list_vector_policies() -> List[VectorPolicy]:
            policy = TestResourcesVectorPoliciesSuite.get_example_policy()
            return [policy]
        list_vector_policies_mocker = mocker.MagicMock(side_effect=list_vector_policies)
        return list_vector_policies_mocker

    @pytest.fixture
    def remove(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the remove_vector_policy function

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """
        def remove_vector_policy(vector_policy: VectorPolicy) -> None:
            return None
        remove_vector_policy_mocker = mocker.MagicMock(side_effect=remove_vector_policy)
        return remove_vector_policy_mocker

    @pytest.fixture
    def get_policy(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_vector_policy function

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """
        def get_vector_policy(id: int) -> VectorPolicy:
            policy = TestResourcesVectorPoliciesSuite.get_example_policy()
            return policy
        get_vector_policy_mocker = mocker.MagicMock(side_effect=get_vector_policy)
        return get_vector_policy_mocker

    @staticmethod
    def get_example_policy() -> VectorPolicy:
        """
        Utility function for creating an example istance of the VectorPolicy class

        :return: an example VectorPolicy instance
        """
        obj = VectorPolicy(player_type=PlayerType(1), actions=[1, 2, 3], policy_vector=[1.1, 1.2, 1.3],
                           agent_type=AgentType(1), simulation_name="JohndoeSimulation",
                           avg_R=1.1)
        return obj

    def test_vector_policies_get(self, flask_app, mocker: pytest_mock.MockFixture, list_vector, logged_in,
                                 not_logged_in, logged_in_as_admin, list_vector_ids) -> None:
        """
        Tests the GET HTTP method for the /vector-policies resource

        :param flask_app: the flask app for making the test requests
        :param mocker: the pytest mocker object for mocking
        :param list_vector: the list_vector fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param list_vector_ids: the list_vector_ids_fixture
        :return: None
        """
        test_policy = TestResourcesVectorPoliciesSuite.get_example_policy()
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_vector_policies",
                     side_effect=list_vector)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_vector_policies_ids",
                     side_effect=list_vector_ids)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        vector_dict = response_data_list[0]
        assert vector_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 111
        assert vector_dict[api_constants.MGMT_WEBAPP.SIMULATION_PROPERTY] == "some_simulation"
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        vector = VectorPolicy.from_dict(response_data_list[0])
        assert vector.player_type == test_policy.player_type
        assert vector.policy_vector == test_policy.policy_vector
        assert vector.agent_type == test_policy.agent_type
        assert vector.simulation_name == test_policy.simulation_name
        assert vector.avg_R == test_policy.avg_R
        assert vector.id == test_policy.id
        assert vector.policy_type == test_policy.policy_type
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        vector = VectorPolicy.from_dict(response_data_list[0])
        assert vector.player_type == test_policy.player_type
        assert vector.policy_vector == test_policy.policy_vector
        assert vector.agent_type == test_policy.agent_type
        assert vector.simulation_name == test_policy.simulation_name
        assert vector.avg_R == test_policy.avg_R
        assert vector.id == test_policy.id
        assert vector.policy_type == test_policy.policy_type

    def test_vector_policies_delete(self, flask_app, mocker: pytest_mock.MockFixture, list_vector, logged_in,
                                    not_logged_in, logged_in_as_admin, list_vector_ids, remove) -> None:
        """
        Tests the DELETE HTTP method for the /vector-policies resource

        :param flask_app: the flask app for making the test requests
        :param mocker: the pytest mocker object for mocking
        :param list_vector: the list_vector fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param list_vector_ids: the list_vector_ids fixture
        :param remove: the remove fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_vector_policy", side_effect=remove)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_vector_policies",
                     side_effect=list_vector)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_vector_policies_ids",
                     side_effect=list_vector_ids)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}

    def test_vector_policies_id_get(self, flask_app, mocker: pytest_mock.MockFixture, logged_in, not_logged_in,
                                    logged_in_as_admin, get_policy) -> None:
        """
        Tests the GET HTTP method for /policies?ids=true

        :param flask_app: the flask app for making the test requests
        :param mocker: the pytest mocker object for mocking
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_policy: the get_policy fixture
        :return: None
        """
        test_policy = TestResourcesVectorPoliciesSuite.get_example_policy()
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_vector_policy", side_effect=get_policy)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        vector = VectorPolicy.from_dict(response_data_list)
        assert vector.player_type == test_policy.player_type
        assert vector.policy_vector == test_policy.policy_vector
        assert vector.agent_type == test_policy.agent_type
        assert vector.simulation_name == test_policy.simulation_name
        assert vector.avg_R == test_policy.avg_R
        assert vector.id == test_policy.id
        assert vector.policy_type == test_policy.policy_type
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        vector = VectorPolicy.from_dict(response_data_list)
        assert vector.player_type == test_policy.player_type
        assert vector.policy_vector == test_policy.policy_vector
        assert vector.agent_type == test_policy.agent_type
        assert vector.simulation_name == test_policy.simulation_name
        assert vector.avg_R == test_policy.avg_R
        assert vector.id == test_policy.id
        assert vector.policy_type == test_policy.policy_type

    def test_vector_policies_id_delete(self, flask_app, mocker: pytest_mock.MockFixture, logged_in, not_logged_in,
                                       logged_in_as_admin, get_policy, remove) -> None:
        """
        Tests the HTTP DELETE method for the /vector-policies/id resource

        :param flask_app: the pytest flask App for making requests
        :param mocker:
        :param logged_in:
        :param not_logged_in:
        :param logged_in_as_admin:
        :param get_policy:
        :param remove:
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_vector_policy", side_effect=get_policy)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_vector_policy", side_effect=remove)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.VECTOR_POLICIES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
