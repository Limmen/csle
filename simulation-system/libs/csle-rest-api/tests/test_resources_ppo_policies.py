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
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.training.ppo_policy import PPOPolicy
import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesPPOPoliciesSuite:
    """
    Test suite for /users resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def list_ppo_ids(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_ppo_policies_ids function

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """
        def list_ppo_policies_ids() -> List[Tuple[int, str]]:
            policy_id = (111, "some_simulation")
            return [policy_id]
        list_ppo_plicies_ids_mocker = mocker.MagicMock(side_effect=list_ppo_policies_ids)
        return list_ppo_plicies_ids_mocker

    @pytest.fixture
    def list_ppo(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_ppo_policies function

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """
        def list_ppo_policies() -> List[PPOPolicy]:
            policy = TestResourcesPPOPoliciesSuite.get_example_policy()
            return [policy]
        list_ppo_policies_mocker = mocker.MagicMock(side_effect=list_ppo_policies)
        return list_ppo_policies_mocker

    @pytest.fixture
    def remove(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the remove_ppo_policy function

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """
        def remove_ppo_policy(ppo_policy: PPOPolicy) -> None:
            return None
        remove_ppo_policy_mocker = mocker.MagicMock(side_effect=remove_ppo_policy)
        return remove_ppo_policy_mocker

    @pytest.fixture
    def get_policy(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_ppo_policy function

        :param mocker: the pytest mocker object
        :return: a mock object with the mocked function
        """
        def get_ppo_policy(id: int) -> PPOPolicy:
            policy = TestResourcesPPOPoliciesSuite.get_example_policy()
            return policy
        get_ppo_policy_mocker = mocker.MagicMock(side_effect=get_ppo_policy)
        return get_ppo_policy_mocker

    @staticmethod
    def get_example_policy() -> PPOPolicy:
        """
        Utility function for getting an example instance of a PPOPolicy

        :return: an example isntance of a PPOPOlicy
        """
        state_list = [State(id=1, name="JohnDoe", descr="description", state_type=StateType(0))]
        e_config_class = ExperimentConfig(output_dir="output_directory", title="title", random_seeds=[1, 2, 3],
                                          agent_type=AgentType(1),
                                          hparams={'element': HParam(10, name="John", descr="Doe")},
                                          log_every=10, player_type=PlayerType(1),
                                          player_idx=10, br_log_every=10)

        obj = PPOPolicy(model=None, simulation_name="JohnDoeSimulation", save_path="",
                        states=state_list, player_type=PlayerType(1),
                        actions=[Action(id=10, descr="null")],
                        experiment_config=e_config_class, avg_R=1.1)
        return obj

    def test_ppo_policies_get(self, flask_app, mocker: pytest_mock.MockFixture, list_ppo, logged_in, not_logged_in,
                              logged_in_as_admin, list_ppo_ids) -> None:
        """
        Testing for the GET HTTPS method in the /ppo-policies resource

        :param flask_app: the flask app for making the test requests
        :param mocker: the pytest mocker object
        :param list_ppo: the list_ppo fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param list_ppo_ids: the list_ppo_ids fixture
        :return: None
        """
        test_policy = TestResourcesPPOPoliciesSuite.get_example_policy()
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in,)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_ppo_policies",
                     side_effect=list_ppo)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_ppo_policies_ids",
                     side_effect=list_ppo_ids)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        ppo_data = PPOPolicy.from_dict(response_data_list[0])
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert ppo_data.actions[0].id == test_policy.actions[0].id
        assert ppo_data.actions[0].descr == test_policy.actions[0].descr
        assert ppo_data.model == test_policy.model
        assert ppo_data.id == test_policy.id
        assert ppo_data.simulation_name == test_policy.simulation_name
        assert ppo_data.save_path == test_policy.save_path
        assert ppo_data.states[0].id == test_policy.states[0].id
        assert ppo_data.states[0].name == test_policy.states[0].name
        assert ppo_data.states[0].descr == test_policy.states[0].descr
        assert ppo_data.states[0].state_type == test_policy.states[0].state_type
        assert ppo_data.experiment_config.output_dir == test_policy.experiment_config.output_dir
        assert ppo_data.experiment_config.title == test_policy.experiment_config.title
        assert ppo_data.experiment_config.random_seeds == test_policy.experiment_config.random_seeds
        assert ppo_data.experiment_config.agent_type == test_policy.experiment_config.agent_type
        assert ppo_data.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].value == \
            test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].value
        assert ppo_data.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].name ==\
            test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].name
        assert ppo_data.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].descr ==\
            test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].descr
        assert ppo_data.experiment_config.log_every == test_policy.experiment_config.log_every
        assert ppo_data.experiment_config.player_type == test_policy.experiment_config.player_type
        assert ppo_data.experiment_config.player_idx == test_policy.experiment_config.player_idx
        assert ppo_data.experiment_config.br_log_every == test_policy.experiment_config.br_log_every
        assert ppo_data.policy_type == test_policy.policy_type
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list[0][api_constants.MGMT_WEBAPP.ID_PROPERTY] == 111
        assert response_data_list[0][api_constants.MGMT_WEBAPP.SIMULATION_PROPERTY] == "some_simulation"
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        ppo_data = PPOPolicy.from_dict(response_data_list[0])
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert ppo_data.actions[0].id == test_policy.actions[0].id
        assert ppo_data.actions[0].descr == test_policy.actions[0].descr
        assert ppo_data.model == test_policy.model
        assert ppo_data.id == test_policy.id
        assert ppo_data.simulation_name == test_policy.simulation_name
        assert ppo_data.save_path == test_policy.save_path
        assert ppo_data.states[0].id == test_policy.states[0].id
        assert ppo_data.states[0].name == test_policy.states[0].name
        assert ppo_data.states[0].descr == test_policy.states[0].descr
        assert ppo_data.states[0].state_type == test_policy.states[0].state_type
        assert ppo_data.experiment_config.output_dir == test_policy.experiment_config.output_dir
        assert ppo_data.experiment_config.title == test_policy.experiment_config.title
        assert ppo_data.experiment_config.random_seeds == test_policy.experiment_config.random_seeds
        assert ppo_data.experiment_config.agent_type == test_policy.experiment_config.agent_type
        assert ppo_data.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].value == \
            test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].value
        assert ppo_data.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].name ==\
            test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].name
        assert ppo_data.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].descr ==\
            test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].descr
        assert ppo_data.experiment_config.log_every == test_policy.experiment_config.log_every
        assert ppo_data.experiment_config.player_type == test_policy.experiment_config.player_type
        assert ppo_data.experiment_config.player_idx == test_policy.experiment_config.player_idx
        assert ppo_data.experiment_config.br_log_every == test_policy.experiment_config.br_log_every
        assert ppo_data.policy_type == test_policy.policy_type
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}

    def test_ppo_policies_delete(self, flask_app, mocker: pytest_mock.MockFixture, list_ppo, logged_in, not_logged_in,
                                 logged_in_as_admin, remove) -> None:
        """
        Tests the HTTP DELETE method on the /ppo-policies resource

        :param flask_app: the flask app for making the test requests
        :param mocker: the pytest mocker object
        :param list_ppo: the list_ppo fixture
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param remove: the remove fixture
        :return: None
        """
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_ppo_policies", side_effect=list_ppo)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_ppo_policy", side_effect=remove)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}

    def test_ppo_policies_id_get(self, flask_app, mocker: pytest_mock.MockFixture, logged_in, not_logged_in,
                                 logged_in_as_admin, get_policy,) -> None:
        """
        Tests the HTTPS GET method for the /ppo-policies-id resource

        :param flask_app: the flask app for making the test requests
        :param mocker: the pytest mocker object
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param logged_in_as_admin: the logged_in_as_admin fixture
        :param get_policy: the get_policy fixture
        :return: None
        """
        test_policy = TestResourcesPPOPoliciesSuite.get_example_policy()
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_ppo_policy", side_effect=get_policy)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        ppo_data = PPOPolicy.from_dict(response_data_list)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert ppo_data.actions[0].id == test_policy.actions[0].id
        assert ppo_data.actions[0].descr == test_policy.actions[0].descr
        assert ppo_data.model == test_policy.model
        assert ppo_data.id == test_policy.id
        assert ppo_data.simulation_name == test_policy.simulation_name
        assert ppo_data.save_path == test_policy.save_path
        assert ppo_data.states[0].id == test_policy.states[0].id
        assert ppo_data.states[0].name == test_policy.states[0].name
        assert ppo_data.states[0].descr == test_policy.states[0].descr
        assert ppo_data.states[0].state_type == test_policy.states[0].state_type
        assert ppo_data.experiment_config.output_dir == test_policy.experiment_config.output_dir
        assert ppo_data.experiment_config.title == test_policy.experiment_config.title
        assert ppo_data.experiment_config.random_seeds == test_policy.experiment_config.random_seeds
        assert ppo_data.experiment_config.agent_type == test_policy.experiment_config.agent_type
        assert ppo_data.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].value == \
            test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].value
        assert ppo_data.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].name ==\
            test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].name
        assert ppo_data.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].descr ==\
            test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].descr
        assert ppo_data.experiment_config.log_every == test_policy.experiment_config.log_every
        assert ppo_data.experiment_config.player_type == test_policy.experiment_config.player_type
        assert ppo_data.experiment_config.player_idx == test_policy.experiment_config.player_idx
        assert ppo_data.experiment_config.br_log_every == test_policy.experiment_config.br_log_every
        assert ppo_data.policy_type == test_policy.policy_type
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        ppo_data = PPOPolicy.from_dict(response_data_list)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert ppo_data.actions[0].id == test_policy.actions[0].id
        assert ppo_data.actions[0].descr == test_policy.actions[0].descr
        assert ppo_data.model == test_policy.model
        assert ppo_data.id == test_policy.id
        assert ppo_data.simulation_name == test_policy.simulation_name
        assert ppo_data.save_path == test_policy.save_path
        assert ppo_data.states[0].id == test_policy.states[0].id
        assert ppo_data.states[0].name == test_policy.states[0].name
        assert ppo_data.states[0].descr == test_policy.states[0].descr
        assert ppo_data.states[0].state_type == test_policy.states[0].state_type
        assert ppo_data.experiment_config.output_dir == test_policy.experiment_config.output_dir
        assert ppo_data.experiment_config.title == test_policy.experiment_config.title
        assert ppo_data.experiment_config.random_seeds == test_policy.experiment_config.random_seeds
        assert ppo_data.experiment_config.agent_type == test_policy.experiment_config.agent_type
        assert ppo_data.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].value == \
            test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].value
        assert ppo_data.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].name ==\
            test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].name
        assert ppo_data.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].descr ==\
            test_policy.experiment_config.hparams[api_constants.MGMT_WEBAPP.ELEMENT_PROPERTY].descr
        assert ppo_data.experiment_config.log_every == test_policy.experiment_config.log_every
        assert ppo_data.experiment_config.player_type == test_policy.experiment_config.player_type
        assert ppo_data.experiment_config.player_idx == test_policy.experiment_config.player_idx
        assert ppo_data.experiment_config.br_log_every == test_policy.experiment_config.br_log_every
        assert ppo_data.policy_type == test_policy.policy_type

    def test_ppo_policies_id_delete(self, flask_app, mocker: pytest_mock.MockFixture, logged_in, not_logged_in,
                                    get_policy) -> None:
        """
        Tests the HTTPS DELETE method for the /ppo-policies-id resource

        :param flask_app: the flask app for making the tests requests
        :param mocker: the pytest mocker object
        :param logged_in: the logged_in fixture
        :param not_logged_in: the not_logged_in fixture
        :param get_policy: the get_policy fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_ppo_policy", side_effect=get_policy)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE}"f"/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE}"f"/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
