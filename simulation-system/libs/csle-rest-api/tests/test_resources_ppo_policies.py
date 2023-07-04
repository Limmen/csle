import json
import logging

import csle_common.constants.constants as constants
import pytest
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.simulation_config.state import State
from csle_common.dao.simulation_config.state_type import StateType
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.training.policy_type import PolicyType
from csle_common.dao.training.ppo_policy import PPOPolicy

import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesPPOPoliciesSuite(object):
    """
    Test suite for /users resource
    """

    pytest.logger = logging.getLogger("resources_users_tests")

    @pytest.fixture
    def flask_app(self):
        """
        :return: the flask app fixture representing the webserver
        """
        return create_app(
            static_folder="../../../../../management-system/csle-mgmt-webapp/build"
        )

    @pytest.fixture
    def list_ppo_ids(self, mocker):
        """
        pytest fixture for listing alpha vec policy ids
        """
        def list_ppo_policies_ids():
            policy_id = (111, "some_simulation")
            return [policy_id]
        list_ppo_plicies_ids_mocker = mocker.MagicMock(side_effect=list_ppo_policies_ids)
        return list_ppo_plicies_ids_mocker

    @pytest.fixture
    def list_ppo(self, mocker):
        """
        pytest fixture for listing alpha vec policies
        """
        def list_ppo_policies():
            policy = TestResourcesPPOPoliciesSuite.get_example_policy()
            return [policy]
        list_ppo_policies_mocker = mocker.MagicMock(side_effect=list_ppo_policies)
        return list_ppo_policies_mocker

    @pytest.fixture
    def remove(self, mocker):
        """
        pytest fixture for removal of alpha vec policies
        """
        def remove_ppo_policy(ppo_policy):
            return None
        remove_ppo_policy_mocker = mocker.MagicMock(side_effect=remove_ppo_policy)
        return remove_ppo_policy_mocker

    @pytest.fixture
    def get_policy(self, mocker):
        """
        pytest fixture for the get ppo policy
        """
        def get_ppo_policy(id):
            policy = TestResourcesPPOPoliciesSuite.get_example_policy()
            return policy
        get_ppo_policy_mocker = mocker.MagicMock(side_effect=get_ppo_policy)
        return get_ppo_policy_mocker

    @staticmethod
    def get_example_policy():
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

    def test_ppo_policies_get(
            self,
            flask_app,
            mocker,
            list_ppo,
            logged_in,
            not_logged_in,
            logged_in_as_admin,
            list_ppo_ids,
    ) -> None:
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_ppo_policies",
                     side_effect=list_ppo)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_ppo_policies_ids",
                     side_effect=list_ppo_ids)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        pytest.logger.info(response_data_list)
        ppo_data = PPOPolicy.from_dict(response_data_list[0])
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert ppo_data.actions[0].id == 10
        assert ppo_data.actions[0].descr == "null"
        assert ppo_data.model is None
        assert ppo_data.id == -1
        assert ppo_data.simulation_name == "JohnDoeSimulation"
        assert ppo_data.save_path == ""
        assert ppo_data.states[0].id == 1
        assert ppo_data.states[0].name == "JohnDoe"
        assert ppo_data.states[0].descr == "description"
        assert ppo_data.states[0].state_type == 0
        assert ppo_data.experiment_config.output_dir == "output_directory"
        assert ppo_data.experiment_config.title == "title"
        assert ppo_data.experiment_config.random_seeds == [1, 2, 3]
        assert ppo_data.experiment_config.agent_type == AgentType(1)
        assert ppo_data.experiment_config.hparams["element"].value == 10
        assert ppo_data.experiment_config.hparams["element"].name == "John"
        assert ppo_data.experiment_config.hparams["element"].descr == "Doe"
        assert ppo_data.experiment_config.log_every == 10
        assert ppo_data.experiment_config.player_type == PlayerType(1)
        assert ppo_data.experiment_config.player_idx == 10
        assert ppo_data.experiment_config.br_log_every == 10
        assert ppo_data.avg_R == 1.1
        assert ppo_data.policy_type == PolicyType.PPO
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list[0][api_constants.MGMT_WEBAPP.ID_PROPERTY] == 111
        assert response_data_list[0][api_constants.MGMT_WEBAPP.SIMULATION_PROPERTY] == "some_simulation"
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,
        )
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        ppo_data = PPOPolicy.from_dict(response_data_list[0])
        assert ppo_data.actions[0].id == 10
        assert ppo_data.actions[0].descr == "null"
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert ppo_data.model is None
        assert ppo_data.id == -1
        assert ppo_data.simulation_name == "JohnDoeSimulation"
        assert ppo_data.save_path == ""
        assert ppo_data.states[0].id == 1
        assert ppo_data.states[0].name == "JohnDoe"
        assert ppo_data.states[0].descr == "description"
        assert ppo_data.states[0].state_type == 0
        assert ppo_data.experiment_config.output_dir == "output_directory"
        assert ppo_data.experiment_config.title == "title"
        assert ppo_data.experiment_config.random_seeds == [1, 2, 3]
        assert ppo_data.experiment_config.agent_type == AgentType(1)
        assert ppo_data.experiment_config.hparams["element"].value == 10
        assert ppo_data.experiment_config.hparams["element"].name == "John"
        assert ppo_data.experiment_config.hparams["element"].descr == "Doe"
        assert ppo_data.experiment_config.log_every == 10
        assert ppo_data.experiment_config.player_type == PlayerType(1)
        assert ppo_data.experiment_config.player_idx == 10
        assert ppo_data.experiment_config.br_log_every == 10
        assert ppo_data.avg_R == 1.1
        assert ppo_data.policy_type == PolicyType.PPO
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}

    def test_ppo_policies_delete(self, flask_app, mocker,
                                 list_ppo, logged_in, not_logged_in,
                                 logged_in_as_admin, remove) -> None:
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_ppo_policies",
                     side_effect=list_ppo)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_ppo_policy",
                     side_effect=remove)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,
        )
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}

    def test_ppo_policies_id_get(self, flask_app, mocker, logged_in,
                                 not_logged_in, logged_in_as_admin,
                                 get_policy,) -> None:
        """
        testing the /ppo-policies-id resource
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_ppo_policy",
                     side_effect=get_policy)
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE}"f"/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE}"f"/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        ppo_data = PPOPolicy.from_dict(response_data_list)
        assert ppo_data.actions[0].id == 10
        assert ppo_data.actions[0].descr == "null"
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert ppo_data.model is None
        assert ppo_data.id == -1
        assert ppo_data.simulation_name == "JohnDoeSimulation"
        assert ppo_data.save_path == ""
        assert ppo_data.states[0].id == 1
        assert ppo_data.states[0].name == "JohnDoe"
        assert ppo_data.states[0].descr == "description"
        assert ppo_data.states[0].state_type == 0
        assert ppo_data.experiment_config.output_dir == "output_directory"
        assert ppo_data.experiment_config.title == "title"
        assert ppo_data.experiment_config.random_seeds == [1, 2, 3]
        assert ppo_data.experiment_config.agent_type == AgentType(1)
        assert ppo_data.experiment_config.hparams["element"].value == 10
        assert ppo_data.experiment_config.hparams["element"].name == "John"
        assert ppo_data.experiment_config.hparams["element"].descr == "Doe"
        assert ppo_data.experiment_config.log_every == 10
        assert ppo_data.experiment_config.player_type == PlayerType(1)
        assert ppo_data.experiment_config.player_idx == 10
        assert ppo_data.experiment_config.br_log_every == 10
        assert ppo_data.avg_R == 1.1
        assert ppo_data.policy_type == PolicyType.PPO
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,
        )
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE}"f"/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        ppo_data = PPOPolicy.from_dict(response_data_list)
        assert ppo_data.actions[0].id == 10
        assert ppo_data.actions[0].descr == "null"
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert ppo_data.model is None
        assert ppo_data.id == -1
        assert ppo_data.simulation_name == "JohnDoeSimulation"
        assert ppo_data.save_path == ""
        assert ppo_data.states[0].id == 1
        assert ppo_data.states[0].name == "JohnDoe"
        assert ppo_data.states[0].descr == "description"
        assert ppo_data.states[0].state_type == 0
        assert ppo_data.experiment_config.output_dir == "output_directory"
        assert ppo_data.experiment_config.title == "title"
        assert ppo_data.experiment_config.random_seeds == [1, 2, 3]
        assert ppo_data.experiment_config.agent_type == AgentType(1)
        assert ppo_data.experiment_config.hparams["element"].value == 10
        assert ppo_data.experiment_config.hparams["element"].name == "John"
        assert ppo_data.experiment_config.hparams["element"].descr == "Doe"
        assert ppo_data.experiment_config.log_every == 10
        assert ppo_data.experiment_config.player_type == PlayerType(1)
        assert ppo_data.experiment_config.player_idx == 10
        assert ppo_data.experiment_config.br_log_every == 10
        assert ppo_data.avg_R == 1.1
        assert ppo_data.policy_type == PolicyType.PPO

    def test_ppo_policies_id_delete(self, flask_app, mocker,
                                    logged_in, not_logged_in,
                                    get_policy,) -> None:
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_ppo_policy",
                     side_effect=get_policy)
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE}"f"/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.PPO_POLICIES_RESOURCE}"f"/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
