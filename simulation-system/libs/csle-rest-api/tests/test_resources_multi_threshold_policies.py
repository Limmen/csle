from typing import List, Tuple
import json
import pytest
import pytest_mock
import csle_common.constants.constants as constants
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.simulation_config.state import State
from csle_common.dao.simulation_config.state_type import StateType
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.multi_threshold_stopping_policy import MultiThresholdStoppingPolicy
from csle_common.dao.training.player_type import PlayerType
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesMultiThresholdPoliciesSuite:
    """
    Test suite for /multi-threshold-policies resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def list_multi_threshold_ids(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_multi_threshold_stopping_policies_ids

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """
        def list_multi_threshold_stopping_policies_ids() -> List[Tuple[int, str]]:
            policy_id = (111, "some_simulation")
            return [policy_id]
        list_multi_threshold_policies_ids_mocker = mocker.MagicMock(
            side_effect=list_multi_threshold_stopping_policies_ids)
        return list_multi_threshold_policies_ids_mocker

    @pytest.fixture
    def list_multi_threshold(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_multi_threshold_stopping_policies function

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """
        def list_multi_threshold_stopping_policies() -> List[MultiThresholdStoppingPolicy]:
            policy = TestResourcesMultiThresholdPoliciesSuite.get_example_policy()
            return [policy]
        list_multi_threshold_stopping_policies_mocker = mocker.MagicMock(
            side_effect=list_multi_threshold_stopping_policies)
        return list_multi_threshold_stopping_policies_mocker

    @pytest.fixture
    def remove(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the remove_multi_threshold_stopping_policy function

        :param mocker: the pytest mocking object
        :return: a mock object with the mocked function
        """
        def remove_multi_threshold_stopping_policy(multi_threshold_stopping_policy: MultiThresholdStoppingPolicy) \
                -> None:
            return None
        remove_multi_threshold_stopping_policy = mocker.MagicMock(
            side_effect=remove_multi_threshold_stopping_policy)
        return remove_multi_threshold_stopping_policy

    @pytest.fixture
    def get_policy(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_multi_threshold_stopping_policy function

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """
        def get_multi_threshold_stopping_policy(id: int) -> MultiThresholdStoppingPolicy:
            policy = TestResourcesMultiThresholdPoliciesSuite.get_example_policy()
            return policy
        get_multi_threshold_stopping_policy_mocker = mocker.MagicMock(side_effect=get_multi_threshold_stopping_policy)
        return get_multi_threshold_stopping_policy_mocker

    @staticmethod
    def get_example_policy() -> MultiThresholdStoppingPolicy:
        """
        Utility function for creating an example instance of a MultiThresholdStoppingPolicy

        :return: an example instance of MultiThresholdStoppingPolicy
        """
        state_list = [State(id=1, name="JohnDoe", descr="description", state_type=StateType(0))]
        e_config_class = ExperimentConfig(output_dir="output_directory", title="title", random_seeds=[1, 2, 3],
                                          agent_type=AgentType(1),
                                          hparams={'element': HParam(10, name="John", descr="Doe")},
                                          log_every=10, player_type=PlayerType(1),
                                          player_idx=10, br_log_every=10)
        obj = MultiThresholdStoppingPolicy(theta=[1, 2, 3], simulation_name="JohnDoeSimulation",
                                           L=20, states=state_list, player_type=PlayerType(1),
                                           actions=[Action(id=10, descr="null")],
                                           experiment_config=e_config_class, avg_R=1.1,
                                           agent_type=AgentType(1),
                                           opponent_strategy=None)
        return obj

    def test_multi_threshold_policies_get(self, flask_app, mocker: pytest_mock.MockFixture, list_multi_threshold,
                                          logged_in, not_logged_in, logged_in_as_admin,
                                          list_multi_threshold_ids) -> None:
        """
        Tests the GET HTTPS method  for the /multi-threshold-policies resource

        :param flask_app: the flask app for making the test requests
        :param mocker: the pytest mocker object for mocking
        :param list_multi_threshold: the list_multi_threshold fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param list_multi_threshold_ids: the list_multi_threhsold_ids fixture
        :return: None
        """
        test_policy = TestResourcesMultiThresholdPoliciesSuite.get_example_policy()
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_multi_threshold_stopping_policies",
                     side_effect=list_multi_threshold)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade."
                     "list_multi_threshold_stopping_policies_ids", side_effect=list_multi_threshold_ids)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.MULTI_THRESHOLD_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.MULTI_THRESHOLD_POLICIES_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        mul_thresh_dict = response_data_list[0]
        assert mul_thresh_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == 111
        assert mul_thresh_dict[api_constants.MGMT_WEBAPP.SIMULATION_PROPERTY] == "some_simulation"
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.MULTI_THRESHOLD_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        mul_thresh = MultiThresholdStoppingPolicy.from_dict(response_data_list[0])
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert mul_thresh.L == test_policy.L
        assert mul_thresh.actions[0].descr == test_policy.actions[0].descr
        assert mul_thresh.actions[0].id == test_policy.actions[0].id
        assert mul_thresh.agent_type == test_policy.agent_type
        assert mul_thresh.avg_R == test_policy.avg_R
        assert mul_thresh.experiment_config.agent_type == test_policy.experiment_config.agent_type
        assert mul_thresh.experiment_config.br_log_every == test_policy.experiment_config.br_log_every
        assert mul_thresh.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].descr == \
            test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].descr
        assert mul_thresh.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].name == \
            test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].name
        assert mul_thresh.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].value == \
            test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].value
        assert mul_thresh.experiment_config.log_every == test_policy.experiment_config.log_every
        assert mul_thresh.experiment_config.output_dir == test_policy.experiment_config.output_dir
        assert mul_thresh.experiment_config.player_idx == test_policy.experiment_config.player_idx
        assert mul_thresh.experiment_config.player_type == test_policy.experiment_config.player_type
        assert mul_thresh.experiment_config.random_seeds == test_policy.experiment_config.random_seeds
        assert mul_thresh.experiment_config.title == test_policy.experiment_config.title
        assert mul_thresh.id == test_policy.id
        assert mul_thresh.player_type == test_policy.player_type
        assert mul_thresh.policy_type == test_policy.policy_type
        assert mul_thresh.simulation_name == mul_thresh.simulation_name
        assert mul_thresh.states[0].descr == test_policy.states[0].descr
        assert mul_thresh.states[0].id == test_policy.states[0].id
        assert mul_thresh.states[0].name == test_policy.states[0].name
        assert mul_thresh.states[0].state_type == test_policy.states[0].state_type
        assert mul_thresh.theta == test_policy.theta
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.MULTI_THRESHOLD_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        mul_thresh = MultiThresholdStoppingPolicy.from_dict(response_data_list[0])
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert mul_thresh.L == test_policy.L
        assert mul_thresh.actions[0].descr == test_policy.actions[0].descr
        assert mul_thresh.actions[0].id == test_policy.actions[0].id
        assert mul_thresh.agent_type == test_policy.agent_type
        assert mul_thresh.avg_R == test_policy.avg_R
        assert mul_thresh.experiment_config.agent_type == test_policy.experiment_config.agent_type
        assert mul_thresh.experiment_config.br_log_every == test_policy.experiment_config.br_log_every
        assert mul_thresh.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].descr == \
            test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].descr
        assert mul_thresh.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].name == \
            test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].name
        assert mul_thresh.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].value == \
            test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].value
        assert mul_thresh.experiment_config.log_every == test_policy.experiment_config.log_every
        assert mul_thresh.experiment_config.output_dir == test_policy.experiment_config.output_dir
        assert mul_thresh.experiment_config.player_idx == test_policy.experiment_config.player_idx
        assert mul_thresh.experiment_config.player_type == test_policy.experiment_config.player_type
        assert mul_thresh.experiment_config.random_seeds == test_policy.experiment_config.random_seeds
        assert mul_thresh.experiment_config.title == test_policy.experiment_config.title
        assert mul_thresh.id == test_policy.id
        assert mul_thresh.player_type == test_policy.player_type
        assert mul_thresh.policy_type == test_policy.policy_type
        assert mul_thresh.simulation_name == mul_thresh.simulation_name
        assert mul_thresh.states[0].descr == test_policy.states[0].descr
        assert mul_thresh.states[0].id == test_policy.states[0].id
        assert mul_thresh.states[0].name == test_policy.states[0].name
        assert mul_thresh.states[0].state_type == test_policy.states[0].state_type
        assert mul_thresh.theta == test_policy.theta

    def test_multi_threshold_policies_delete(self, flask_app, mocker: pytest_mock.MockFixture, list_multi_threshold,
                                             logged_in, not_logged_in, logged_in_as_admin, remove) -> None:
        """
        Tests the DELETE HTTPS method for the /multi-threshold-policies resource

        :param flask_app: the flask app for making the test requests
        :param mocker: the pytest mocker object
        :param list_multi_threshold: the list_multi_threshold_policies
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param remove: the remove fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_multi_threshold_stopping_policy",
                     side_effect=remove)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_multi_threshold_stopping_policies",
                     side_effect=list_multi_threshold)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.MULTI_THRESHOLD_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.MULTI_THRESHOLD_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.MULTI_THRESHOLD_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}

    def test_multi_threshold_policies_id_get(self, flask_app, mocker: pytest_mock.MockFixture, logged_in,
                                             not_logged_in, logged_in_as_admin, get_policy) -> None:
        """
        Testing the HTTPS GET method for the /multi-threshold-policies/id resource

        :param flask_app: the flask app for making the test requests
        :param mocker: the pytest mocker object
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_policy: the get_policy fixture
        :return: None
        """
        test_policy = TestResourcesMultiThresholdPoliciesSuite.get_example_policy()
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_multi_threshold_stopping_policy",
                     side_effect=get_policy)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.MULTI_THRESHOLD_POLICIES_RESOURCE}"f"/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.MULTI_THRESHOLD_POLICIES_RESOURCE}"f"/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        mul_thresh = MultiThresholdStoppingPolicy.from_dict(response_data_list)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert mul_thresh.L == test_policy.L
        assert mul_thresh.actions[0].descr == test_policy.actions[0].descr
        assert mul_thresh.actions[0].id == test_policy.actions[0].id
        assert mul_thresh.agent_type == test_policy.agent_type
        assert mul_thresh.avg_R == test_policy.avg_R
        assert mul_thresh.experiment_config.agent_type == test_policy.experiment_config.agent_type
        assert mul_thresh.experiment_config.br_log_every == test_policy.experiment_config.br_log_every
        assert mul_thresh.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].descr == \
            test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].descr
        assert mul_thresh.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].name == \
            test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].name
        assert mul_thresh.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].value == \
            test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].value
        assert mul_thresh.experiment_config.log_every == test_policy.experiment_config.log_every
        assert mul_thresh.experiment_config.output_dir == test_policy.experiment_config.output_dir
        assert mul_thresh.experiment_config.player_idx == test_policy.experiment_config.player_idx
        assert mul_thresh.experiment_config.player_type == test_policy.experiment_config.player_type
        assert mul_thresh.experiment_config.random_seeds == test_policy.experiment_config.random_seeds
        assert mul_thresh.experiment_config.title == test_policy.experiment_config.title
        assert mul_thresh.id == test_policy.id
        assert mul_thresh.player_type == test_policy.player_type
        assert mul_thresh.policy_type == test_policy.policy_type
        assert mul_thresh.simulation_name == mul_thresh.simulation_name
        assert mul_thresh.states[0].descr == test_policy.states[0].descr
        assert mul_thresh.states[0].id == test_policy.states[0].id
        assert mul_thresh.states[0].name == test_policy.states[0].name
        assert mul_thresh.states[0].state_type == test_policy.states[0].state_type
        assert mul_thresh.theta == test_policy.theta
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin,)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.MULTI_THRESHOLD_POLICIES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        mul_thresh = MultiThresholdStoppingPolicy.from_dict(response_data_list)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert mul_thresh.L == test_policy.L
        assert mul_thresh.actions[0].descr == test_policy.actions[0].descr
        assert mul_thresh.actions[0].id == test_policy.actions[0].id
        assert mul_thresh.agent_type == test_policy.agent_type
        assert mul_thresh.avg_R == test_policy.avg_R
        assert mul_thresh.experiment_config.agent_type == test_policy.experiment_config.agent_type
        assert mul_thresh.experiment_config.br_log_every == test_policy.experiment_config.br_log_every
        assert mul_thresh.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].descr == \
            test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].descr
        assert mul_thresh.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].name == \
            test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].name
        assert mul_thresh.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].value == \
            test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].value
        assert mul_thresh.experiment_config.log_every == test_policy.experiment_config.log_every
        assert mul_thresh.experiment_config.output_dir == test_policy.experiment_config.output_dir
        assert mul_thresh.experiment_config.player_idx == test_policy.experiment_config.player_idx
        assert mul_thresh.experiment_config.player_type == test_policy.experiment_config.player_type
        assert mul_thresh.experiment_config.random_seeds == test_policy.experiment_config.random_seeds
        assert mul_thresh.experiment_config.title == test_policy.experiment_config.title
        assert mul_thresh.id == test_policy.id
        assert mul_thresh.player_type == test_policy.player_type
        assert mul_thresh.policy_type == test_policy.policy_type
        assert mul_thresh.simulation_name == mul_thresh.simulation_name
        assert mul_thresh.states[0].descr == test_policy.states[0].descr
        assert mul_thresh.states[0].id == test_policy.states[0].id
        assert mul_thresh.states[0].name == test_policy.states[0].name
        assert mul_thresh.states[0].state_type == test_policy.states[0].state_type
        assert mul_thresh.theta == test_policy.theta

    def test_multi_threshold_policies_id_delete(self, flask_app, mocker: pytest_mock.MockFixture, logged_in,
                                                not_logged_in, logged_in_as_admin, get_policy, remove) -> None:
        """
        Testing the HTTPS DELETE method for the /multi-threshold-policies/id resource

        :param flask_app: the flask_app for making the test requests
        :param mocker: the pytest mocker object
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_policy: the get_policy fixture
        :param remove: the remove fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_multi_threshold_stopping_policy",
                     side_effect=get_policy)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_multi_threshold_stopping_policy",
                     side_effect=remove)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.MULTI_THRESHOLD_POLICIES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.MULTI_THRESHOLD_POLICIES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.MULTI_THRESHOLD_POLICIES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
