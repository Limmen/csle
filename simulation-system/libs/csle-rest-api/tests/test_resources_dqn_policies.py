import json
import pytest
import pytest_mock
import csle_common.constants.constants as constants
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.simulation_config.state import State
from csle_common.dao.simulation_config.state_type import StateType
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.dqn_policy import DQNPolicy
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestRecourcesDQNPoliciesSuite:
    """
    Test suite for /dqn-policies resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def list_dqn_ids(self, mocker: pytest_mock.MockFixture):
        """
        pytest fixture for mocking list_dqn_policies_ids

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """

        def list_dqn_policies_ids():
            policy_id = (111, "some_simulation")
            return [policy_id]

        list_ppo_plicies_ids_mocker = mocker.MagicMock(side_effect=list_dqn_policies_ids)
        return list_ppo_plicies_ids_mocker

    @pytest.fixture
    def list_dqn(self, mocker: pytest_mock.MockFixture):
        """
        pytest fixture for mocking the list_dqn_policies

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """

        def list_dqn_policies():
            policy = TestRecourcesDQNPoliciesSuite.get_example_policy()
            return [policy]

        list_dqn_policies_mocker = mocker.MagicMock(
            side_effect=list_dqn_policies)
        return list_dqn_policies_mocker

    @pytest.fixture
    def remove(self, mocker: pytest_mock.MockFixture):
        """
        pytest fixture for mocking the remove_dqn_policy

        :param mocker: the pytest mocker object for mocking
        :return: a mock object with the mocked function
        """

        def remove_dqn_policy(dqn_policy: DQNPolicy):
            return None

        remove_dqn_policy_mocker = mocker.MagicMock(
            side_effect=remove_dqn_policy)
        return remove_dqn_policy_mocker

    @pytest.fixture
    def get_policy(self, mocker: pytest_mock.MockFixture):
        """
        pytest fixture for the get mocking the get_dqn_policy

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """

        def get_dqn_policy(id: int):
            policy = TestRecourcesDQNPoliciesSuite.get_example_policy()
            return policy

        get_dqn_policy_mocker = mocker.MagicMock(side_effect=get_dqn_policy)
        return get_dqn_policy_mocker

    @staticmethod
    def get_example_policy() -> DQNPolicy:
        """
        :return: an example DQNPolicy object
        """
        state_list = [State(id=1, name="JohnDoe", descr="description", state_type=StateType(0))]
        e_config_class = ExperimentConfig(output_dir="output_directory", title="title", random_seeds=[1, 2, 3],
                                          agent_type=AgentType(1),
                                          hparams={'element': HParam(10, name="John", descr="Doe")},
                                          log_every=10, player_type=PlayerType(1),
                                          player_idx=10, br_log_every=10)
        obj = DQNPolicy(model=None, simulation_name="JohnDoeSimulation", save_path="", player_type=PlayerType(1),
                        states=state_list, actions=[Action(id=10, descr="null")],
                        experiment_config=e_config_class, avg_R=1.1)
        return obj

    def test_dqn_policies_get(self, flask_app, mocker: pytest_mock.MockFixture, list_dqn, logged_in,
                              not_logged_in, logged_in_as_admin, list_dqn_ids) -> None:
        """
        testing the GET HTTPS method  for the /dqn-policies resource

        :param flask_app: the Flask app for making test HTTP requests
        :param mocker: pytest mocker object for mocking
        :param list_dqn: the list_dqn fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param list_dqn_ids: the list_dqn_ids fixture
        :return: None
        """
        test_policy = TestRecourcesDQNPoliciesSuite.get_example_policy()
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_dqn_policies", side_effect=list_dqn)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_dqn_policies_ids",
                     side_effect=list_dqn_ids)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.DQN_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.DQN_POLICIES_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        dqn_dict = response_data_list[0]
        assert dqn_dict["id"] == 111
        assert dqn_dict["simulation"] == "some_simulation"
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.DQN_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        dqn = DQNPolicy.from_dict(response_data_list[0])
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert dqn.actions[0].descr == test_policy.actions[0].descr
        assert dqn.actions[0].id == test_policy.actions[0].id
        assert dqn.agent_type == test_policy.agent_type
        assert dqn.avg_R == test_policy.avg_R
        assert dqn.experiment_config.agent_type == test_policy.experiment_config.agent_type
        assert dqn.experiment_config.br_log_every == test_policy.experiment_config.br_log_every
        assert dqn.experiment_config.hparams["element"].descr == \
            test_policy.experiment_config.hparams["element"].descr
        assert dqn.experiment_config.hparams["element"].name == \
            test_policy.experiment_config.hparams["element"].name
        assert dqn.experiment_config.hparams["element"].value == \
            test_policy.experiment_config.hparams["element"].value
        assert dqn.experiment_config.log_every == test_policy.experiment_config.log_every
        assert dqn.experiment_config.output_dir == test_policy.experiment_config.output_dir
        assert dqn.experiment_config.player_idx == test_policy.experiment_config.player_idx
        assert dqn.experiment_config.player_type == test_policy.experiment_config.player_type
        assert dqn.experiment_config.random_seeds == test_policy.experiment_config.random_seeds
        assert dqn.experiment_config.title == test_policy.experiment_config.title
        assert dqn.id == test_policy.id
        assert dqn.player_type == dqn.player_type
        assert dqn.policy_type == test_policy.policy_type
        assert dqn.save_path == test_policy.save_path
        assert dqn.simulation_name == test_policy.simulation_name
        assert dqn.states[0].descr == test_policy.states[0].descr
        assert dqn.states[0].id == test_policy.states[0].id
        assert dqn.states[0].name == test_policy.states[0].name
        assert dqn.states[0].state_type == test_policy.states[0].state_type
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin, )
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.DQN_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        dqn = DQNPolicy.from_dict(response_data_list[0])
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert dqn.actions[0].descr == test_policy.actions[0].descr
        assert dqn.actions[0].id == test_policy.actions[0].id
        assert dqn.agent_type == test_policy.agent_type
        assert dqn.avg_R == test_policy.avg_R
        assert dqn.experiment_config.agent_type == test_policy.experiment_config.agent_type
        assert dqn.experiment_config.br_log_every == test_policy.experiment_config.br_log_every
        assert dqn.experiment_config.hparams["element"].descr == \
            test_policy.experiment_config.hparams["element"].descr
        assert dqn.experiment_config.hparams["element"].name == \
            test_policy.experiment_config.hparams["element"].name
        assert dqn.experiment_config.hparams["element"].value == \
            test_policy.experiment_config.hparams["element"].value
        assert dqn.experiment_config.log_every == test_policy.experiment_config.log_every
        assert dqn.experiment_config.output_dir == test_policy.experiment_config.output_dir
        assert dqn.experiment_config.player_idx == test_policy.experiment_config.player_idx
        assert dqn.experiment_config.player_type == test_policy.experiment_config.player_type
        assert dqn.experiment_config.random_seeds == test_policy.experiment_config.random_seeds
        assert dqn.experiment_config.title == test_policy.experiment_config.title
        assert dqn.id == test_policy.id
        assert dqn.player_type == dqn.player_type
        assert dqn.policy_type == test_policy.policy_type
        assert dqn.save_path == test_policy.save_path
        assert dqn.simulation_name == test_policy.simulation_name
        assert dqn.states[0].descr == test_policy.states[0].descr
        assert dqn.states[0].id == test_policy.states[0].id
        assert dqn.states[0].name == test_policy.states[0].name
        assert dqn.states[0].state_type == test_policy.states[0].state_type

    def test_dqn_policies_delete(self, flask_app, mocker: pytest_mock.MockFixture, list_dqn, logged_in, not_logged_in,
                                 logged_in_as_admin, remove) -> None:
        """
        testing  the DELETE HTTPS method for the /dqn-policies resource

        :param flask_app: the flask app for making the test requests
        :param mocker: the pytest mocker object for mocking
        :param list_dqn: the list_dqn fixture
        :param logged_in: logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param remove: the remove fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_dqn_policy", side_effect=remove)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_dqn_policies", side_effect=list_dqn)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.DQN_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.DQN_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.DQN_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}

    def test_dqn_policies_id_get(self, flask_app, mocker: pytest_mock.MockFixture, logged_in,
                                 not_logged_in, logged_in_as_admin, get_policy) -> None:
        """
        testing the HTTPS GET method for the /dqn-policies/id resource

        :param flask_app: the flask app for making tests requests
        :param mocker: the pytest mocker object for making mocks
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_policy: the get_policy fixture
        :return: None
        """
        test_policy = TestRecourcesDQNPoliciesSuite.get_example_policy()
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_dqn_policy", side_effect=get_policy)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.DQN_POLICIES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.DQN_POLICIES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        dqn = DQNPolicy.from_dict(response_data_list)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert dqn.actions[0].descr == test_policy.actions[0].descr
        assert dqn.actions[0].id == test_policy.actions[0].id
        assert dqn.agent_type == test_policy.agent_type
        assert dqn.avg_R == test_policy.avg_R
        assert dqn.experiment_config.agent_type == test_policy.experiment_config.agent_type
        assert dqn.experiment_config.br_log_every == test_policy.experiment_config.br_log_every
        assert dqn.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].descr == \
               test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].descr
        assert dqn.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].name == \
               test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].name
        assert dqn.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].value == \
               test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].value
        assert dqn.experiment_config.log_every == test_policy.experiment_config.log_every
        assert dqn.experiment_config.output_dir == test_policy.experiment_config.output_dir
        assert dqn.experiment_config.player_idx == test_policy.experiment_config.player_idx
        assert dqn.experiment_config.player_type == test_policy.experiment_config.player_type
        assert dqn.experiment_config.random_seeds == test_policy.experiment_config.random_seeds
        assert dqn.experiment_config.title == test_policy.experiment_config.title
        assert dqn.id == test_policy.id
        assert dqn.player_type == dqn.player_type
        assert dqn.policy_type == test_policy.policy_type
        assert dqn.save_path == test_policy.save_path
        assert dqn.simulation_name == test_policy.simulation_name
        assert dqn.states[0].descr == test_policy.states[0].descr
        assert dqn.states[0].id == test_policy.states[0].id
        assert dqn.states[0].name == test_policy.states[0].name
        assert dqn.states[0].state_type == test_policy.states[0].state_type
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.DQN_POLICIES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        dqn = DQNPolicy.from_dict(response_data_list)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert dqn.actions[0].descr == test_policy.actions[0].descr
        assert dqn.actions[0].id == test_policy.actions[0].id
        assert dqn.agent_type == test_policy.agent_type
        assert dqn.avg_R == test_policy.avg_R
        assert dqn.experiment_config.agent_type == test_policy.experiment_config.agent_type
        assert dqn.experiment_config.br_log_every == test_policy.experiment_config.br_log_every
        assert dqn.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].descr == \
               test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].descr
        assert dqn.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].name == \
               test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].name
        assert dqn.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].value == \
               test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].value
        assert dqn.experiment_config.log_every == test_policy.experiment_config.log_every
        assert dqn.experiment_config.output_dir == test_policy.experiment_config.output_dir
        assert dqn.experiment_config.player_idx == test_policy.experiment_config.player_idx
        assert dqn.experiment_config.player_type == test_policy.experiment_config.player_type
        assert dqn.experiment_config.random_seeds == test_policy.experiment_config.random_seeds
        assert dqn.experiment_config.title == test_policy.experiment_config.title
        assert dqn.id == test_policy.id
        assert dqn.player_type == dqn.player_type
        assert dqn.policy_type == test_policy.policy_type
        assert dqn.save_path == test_policy.save_path
        assert dqn.simulation_name == test_policy.simulation_name
        assert dqn.states[0].descr == test_policy.states[0].descr
        assert dqn.states[0].id == test_policy.states[0].id
        assert dqn.states[0].name == test_policy.states[0].name
        assert dqn.states[0].state_type == test_policy.states[0].state_type

    def test_dqn_policies_id_delete(self, flask_app, mocker: pytest_mock.MockFixture, logged_in, not_logged_in,
                                    logged_in_as_admin, get_policy, remove) -> None:
        """
        testing the HTTPS DELETE method for the /dqn-policies/id resource

        :param flask_app: the flask app for making the test requests
        :param mocker: the pytest mocker object for mocking
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_policy: the get_policy fixture
        :param remove: the remove fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_dqn_policy", side_effect=get_policy)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_dqn_policy", side_effect=remove)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.DQN_POLICIES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.DQN_POLICIES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.DQN_POLICIES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
