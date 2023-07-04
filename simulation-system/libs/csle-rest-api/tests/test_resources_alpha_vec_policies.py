import json
import logging

import csle_common.constants.constants as constants
import pytest
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.simulation_config.state import State
from csle_common.dao.simulation_config.state_type import StateType
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.alpha_vectors_policy import AlphaVectorsPolicy
from csle_common.dao.training.player_type import PlayerType

import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesAlphaVecsSuite(object):
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
    def list_alpha_vec_ids(self, mocker):
        """
        pytest fixture for listing alpha vec policy ids
        """
        def list_alpha_vec_policies_ids():
            policy_id = (111, "some_simulation")
            return [policy_id]
        list_ppo_plicies_ids_mocker = mocker.MagicMock(side_effect=list_alpha_vec_policies_ids)
        return list_ppo_plicies_ids_mocker

    @pytest.fixture
    def list_alpha_vec(self, mocker):
        """
        pytest fixture for listing alpha vec policies
        """
        def list_alpha_vec_policies():
            policy = TestResourcesAlphaVecsSuite.get_example_policy()
            return [policy]
        list_alpha_vec_policies_mocker = mocker.MagicMock(side_effect=list_alpha_vec_policies)
        return list_alpha_vec_policies_mocker

    @pytest.fixture
    def remove(self, mocker):
        """
        pytest fixture for removal of alpha vec policies
        """
        def remove_alpha_vec_policy(alpha_vec_policy):
            return None
        remove_alpha_vec_policy_mocker = mocker.MagicMock(side_effect=remove_alpha_vec_policy)
        return remove_alpha_vec_policy_mocker

    @pytest.fixture
    def get_policy(self, mocker):
        """
        pytest fixture for the get ppo policy
        """
        def get_ppo_policy(id):
            policy = TestResourcesAlphaVecsSuite.get_example_policy()
            return policy
        get_ppo_policy_mocker = mocker.MagicMock(side_effect=get_ppo_policy)
        return get_ppo_policy_mocker

    @staticmethod
    def get_example_policy():

        obj = AlphaVectorsPolicy(player_type=PlayerType(1),
                                 actions=[Action(id=10, descr="null")],
                                 alpha_vectors=[1, 2, 3],
                                 transition_tensor=[1, 2, 3],
                                 reward_tensor=[1, 2, 3],
                                 states=[State(id=10, name="JohnDoe", descr="null", state_type=StateType(0))],
                                 agent_type=AgentType(1),
                                 simulation_name="JohnDoeSimulation",
                                 avg_R=1.1)
        return obj

    def test_alpha_vec_policies_get(
            self,
            flask_app,
            mocker,
            list_alpha_vec,
            logged_in,
            not_logged_in,
            logged_in_as_admin,
            list_alpha_vec_ids,
    ) -> None:
        """
        testing the GET HTTPS method  for the /alpha-vec-policies resource
        """
        test_policy = TestResourcesAlphaVecsSuite.get_example_policy()
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.ALPHA_VEC_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_alpha_vec_policies",
                     side_effect=list_alpha_vec)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_alpha_vec_policies_ids",
                     side_effect=list_alpha_vec_ids)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.ALPHA_VEC_POLICIES_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        alpha_vec_dict = response_data_list[0]
        assert alpha_vec_dict["id"] == 111
        assert alpha_vec_dict["simulation"] == "some_simulation"
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.ALPHA_VEC_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        alpha_vec = AlphaVectorsPolicy.from_dict(response_data_list[0])
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert alpha_vec.actions[0].descr == test_policy.actions[0].descr
        assert alpha_vec.actions[0].id == test_policy.actions[0].id
        assert alpha_vec.agent_type == test_policy.agent_type
        assert alpha_vec.alpha_vectors == test_policy.alpha_vectors
        assert alpha_vec.avg_R == test_policy.avg_R
        assert alpha_vec.player_type == test_policy.player_type
        assert alpha_vec.policy_type == test_policy.policy_type
        assert alpha_vec.reward_tensor == test_policy.reward_tensor
        assert alpha_vec.simulation_name == test_policy.simulation_name
        assert alpha_vec.states[0].descr == test_policy.states[0].descr
        assert alpha_vec.states[0].id == test_policy.states[0].id
        assert alpha_vec.states[0].name == test_policy.states[0].name
        assert alpha_vec.states[0].state_type == test_policy.states[0].state_type
        assert alpha_vec.transition_tensor == test_policy.transition_tensor
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,
        )
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.ALPHA_VEC_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert alpha_vec.actions[0].descr == test_policy.actions[0].descr
        assert alpha_vec.actions[0].id == test_policy.actions[0].id
        assert alpha_vec.agent_type == test_policy.agent_type
        assert alpha_vec.alpha_vectors == test_policy.alpha_vectors
        assert alpha_vec.avg_R == test_policy.avg_R
        assert alpha_vec.player_type == test_policy.player_type
        assert alpha_vec.policy_type == test_policy.policy_type
        assert alpha_vec.reward_tensor == test_policy.reward_tensor
        assert alpha_vec.simulation_name == test_policy.simulation_name
        assert alpha_vec.states[0].descr == test_policy.states[0].descr
        assert alpha_vec.states[0].id == test_policy.states[0].id
        assert alpha_vec.states[0].name == test_policy.states[0].name
        assert alpha_vec.states[0].state_type == test_policy.states[0].state_type
        assert alpha_vec.transition_tensor == test_policy.transition_tensor

    def test_alpha_vec_policies_delete(
            self,
            flask_app,
            mocker,
            list_alpha_vec,
            logged_in,
            not_logged_in,
            logged_in_as_admin,
            list_alpha_vec_ids,
            remove,
    ) -> None:
        """
        testing  the DELETE HTTPS method for the /alpha-vec-policies resource
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_alpha_vec_policy",
                     side_effect=remove)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_alpha_vec_policies",
                     side_effect=list_alpha_vec)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_alpha_vec_policies_ids",
                     side_effect=list_alpha_vec_ids)
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )

        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.ALPHA_VEC_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_alpha_vec_policies",
                     side_effect=list_alpha_vec)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_alpha_vec_policies_ids",
                     side_effect=list_alpha_vec_ids)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.ALPHA_VEC_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,
        )
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.ALPHA_VEC_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}
