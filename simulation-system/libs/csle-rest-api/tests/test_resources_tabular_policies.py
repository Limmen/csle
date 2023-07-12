from typing import List, Tuple
import json
import pytest
import pytest_mock
import csle_common.constants.constants as constants
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.training.tabular_policy import TabularPolicy
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestRecourcesTabularSuite:
    """
    Test suite for /muti-threshold-policies resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def list_tabular_ids(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list of tabular policies ids function on the database

        :param mocker: The pytest mocker object
        :return: Fixture for mocking list_tabular_policies_ids
        """
        def list_tabular_policies_ids() -> List[Tuple[int, str]]:
            policy_id = (111, "some_simulation")
            return [policy_id]
        list_tabular_policies_ids_mocker = mocker.MagicMock(side_effect=list_tabular_policies_ids)
        return list_tabular_policies_ids_mocker

    @pytest.fixture
    def list_tabular(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list of tabular policies function on the database

        :param mocker: The pytest mocker object
        :return: Fixture for mocking list_tabular_policies
        """
        def list_tabular_policies() -> List[TabularPolicy]:
            policy = TestRecourcesTabularSuite.get_example_policy()
            return [policy]
        list_tabular_policies_mocker = mocker.MagicMock(side_effect=list_tabular_policies)
        return list_tabular_policies_mocker

    @pytest.fixture
    def remove(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking remove tabular policy function on the database

        :param mocker: The pytest mocker object
        :return: Fixture for mocking function remove_tabular_policy
        """
        def remove_tabular_policy(tabular_policy: TabularPolicy) -> None:
            return None
        remove_tabular_policy = mocker.MagicMock(side_effect=remove_tabular_policy)
        return remove_tabular_policy

    @pytest.fixture
    def get_policy(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for the get multi_threshold policy function on the database

        :param mocker: The pytest mocker object
        :return: Fixture for mocking function get_multi_threshold_stopping_policy
        """
        def get_multi_threshold_stopping_policy(id: int) -> TabularPolicy:
            policy = TestRecourcesTabularSuite.get_example_policy()
            return policy
        get_multi_threshold_stopping_policy_mocker = mocker.MagicMock(side_effect=get_multi_threshold_stopping_policy)
        return get_multi_threshold_stopping_policy_mocker

    @staticmethod
    def get_example_policy() -> TabularPolicy:
        """
        :return: An example TabularPolicy class containing dummy values for mocked testing
        """
        obj = TabularPolicy(player_type=PlayerType(1), actions=[Action(id=10, descr="null")],
                            lookup_table=[1, 2, 3], agent_type=AgentType(1), simulation_name="JohnDoeSimulation",
                            avg_R=1.1, value_function=None, q_table=None)
        return obj

    def test_tabular_policies_get(self, flask_app, mocker: pytest_mock.MockFixture, list_tabular, logged_in,
                                  not_logged_in, logged_in_as_admin, list_tabular_ids) -> None:
        """
        Testing the GET HTTPS method  for the /tabular-policies resource

        :param flask_app: The flaskk app representing te web server
        :param mocker: The pytest mocker object
        :param list_tabular: The list_tabular fixture
        :param logged_in: The logged_in fixture
        :param not_logged_in: The not_logged_in fixture
        :param logged_in_as_admin: The logged_in_as_admin fixture
        :param list_tabular_ids: The list_tabular_ids fixture
        """
        test_policy = TestRecourcesTabularSuite.get_example_policy()
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_tabular_policies",
                     side_effect=list_tabular)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_tabular_policies_ids",
                     side_effect=list_tabular_ids)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        tab_dict = response_data_list[0]
        assert tab_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 111
        assert tab_dict[api_constants.MGMT_WEBAPP.SIMULATION_PROPERTY] == "some_simulation"
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        tabular = TabularPolicy.from_dict(response_data_list[0])
        assert tabular.actions[0].descr == test_policy.actions[0].descr
        assert tabular.actions[0].id == test_policy.actions[0].id
        assert tabular.agent_type == test_policy.agent_type
        assert tabular.avg_R == test_policy.avg_R
        assert tabular.id == test_policy.id
        assert tabular.lookup_table == test_policy.lookup_table
        assert tabular.player_type == test_policy.player_type
        assert tabular.policy_type == test_policy.policy_type
        assert tabular.q_table == test_policy.q_table
        assert tabular.simulation_name == test_policy.simulation_name
        assert tabular.value_function == test_policy.value_function
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        tabular = TabularPolicy.from_dict(response_data_list[0])
        assert tabular.actions[0].descr == test_policy.actions[0].descr
        assert tabular.actions[0].id == test_policy.actions[0].id
        assert tabular.agent_type == test_policy.agent_type
        assert tabular.avg_R == test_policy.avg_R
        assert tabular.id == test_policy.id
        assert tabular.lookup_table == test_policy.lookup_table
        assert tabular.player_type == test_policy.player_type
        assert tabular.policy_type == test_policy.policy_type
        assert tabular.q_table == test_policy.q_table
        assert tabular.simulation_name == test_policy.simulation_name
        assert tabular.value_function == test_policy.value_function

    def test_tabular_policies_delete(self, flask_app, mocker: pytest_mock.MockFixture, list_tabular, logged_in,
                                     not_logged_in, logged_in_as_admin, remove) -> None:
        """
        Testing  the DELETE HTTPS method for the /tabular-policies resource

        :param flask_app: The flaskk app representing te web server
        :param mocker: The pytest mocker object
        :param list_tabular: The list_tabular fixture
        :param logged_in: The logged_in fixture
        :param not_logged_in: The not_logged_in fixture
        :param logged_in_as_admin: The logged_in_as_admin fixture
        :param remove: The remove fixture
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_tabular_policy", side_effect=remove)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_tabular_policies",
                     side_effect=list_tabular)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}

    def test_tabular_policies_id_get(self, flask_app, mocker: pytest_mock.MockFixture, logged_in,
                                     not_logged_in, logged_in_as_admin, get_policy) -> None:
        """
        Testing the HTTPS GET method for the /tabular-policies/id resource

        :param flask_app: The flaskk app representing te web server
        :param mocker: The pytest mocker object
        :param logged_in: The logged_in fixture
        :param not_logged_in: The not_logged_in fixture
        :param logged_in_as_admin: The logged_in_as_admin fixture
        :param get_policy: The get_policy fixture
        """
        test_policy = TestRecourcesTabularSuite.get_example_policy()
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_tabular_policy",
                     side_effect=get_policy)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        tabular = TabularPolicy.from_dict(response_data_list)
        assert tabular.actions[0].descr == test_policy.actions[0].descr
        assert tabular.actions[0].id == test_policy.actions[0].id
        assert tabular.agent_type == test_policy.agent_type
        assert tabular.avg_R == test_policy.avg_R
        assert tabular.id == test_policy.id
        assert tabular.lookup_table == test_policy.lookup_table
        assert tabular.player_type == test_policy.player_type
        assert tabular.policy_type == test_policy.policy_type
        assert tabular.q_table == test_policy.q_table
        assert tabular.simulation_name == test_policy.simulation_name
        assert tabular.value_function == test_policy.value_function
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        tabular = TabularPolicy.from_dict(response_data_list)
        assert tabular.actions[0].descr == test_policy.actions[0].descr
        assert tabular.actions[0].id == test_policy.actions[0].id
        assert tabular.agent_type == test_policy.agent_type
        assert tabular.avg_R == test_policy.avg_R
        assert tabular.id == test_policy.id
        assert tabular.lookup_table == test_policy.lookup_table
        assert tabular.player_type == test_policy.player_type
        assert tabular.policy_type == test_policy.policy_type
        assert tabular.q_table == test_policy.q_table
        assert tabular.simulation_name == test_policy.simulation_name
        assert tabular.value_function == test_policy.value_function

    def test_tabular_policies_id_delete(self, flask_app, mocker: pytest_mock.MockFixture, logged_in,
                                        not_logged_in, logged_in_as_admin, get_policy, remove) -> None:
        """
        Testing the HTTPS DELETE method for the /tabular-policies/id resource

        :param flask_app: The flaskk app representing te web server
        :param mocker: The pytest mocker object
        :param logged_in: The logged_in fixture
        :param not_logged_in: The not_logged_in fixture
        :param logged_in_as_admin: The logged_in_as_admin fixture
        :param get_policy: The list_tabular_ids fixture
        :param remove: The remove policy
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_tabular_policy",
                     side_effect=get_policy)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_tabular_policy", side_effect=remove)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in,)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.TABULAR_POLICIES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
