import json
import logging

import csle_common.constants.constants as constants
import pytest
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.simulation_config.state import State
from csle_common.dao.simulation_config.state_type import StateType
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.fnn_with_softmax_policy import FNNWithSoftmaxPolicy
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType

import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesFnnWSoftmaxSuite(object):
    """
    Test suite for /fnn-w-softmax resource
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
    def list_fnn_w_softmax_ids(self, mocker):
        """
        pytest fixture for fnn_w_softmax ids policies
        """
        def list_fnn_w_softmax_policies_ids():
            policy_id = (111, "some_simulation")
            return [policy_id]
        list_ppo_plicies_ids_mocker = mocker.MagicMock(side_effect=list_fnn_w_softmax_policies_ids)
        return list_ppo_plicies_ids_mocker

    @pytest.fixture
    def list_fnn_w_softmax(self, mocker):
        """
        pytest fixture for listing fnn_w_softmax policies
        """
        def list_fnn_w_softmax_policies():
            policy = TestResourcesFnnWSoftmaxSuite.get_example_policy()
            return [policy]
        list_fnn_w_softmax_policies_mocker = mocker.MagicMock(side_effect=list_fnn_w_softmax_policies)
        return list_fnn_w_softmax_policies_mocker

    @pytest.fixture
    def remove(self, mocker):
        """
        pytest fixture for removal of fnn_w_softmax policies
        """
        def remove_fnn_w_softmax_policy(fnn_w_softmax_policy):
            return None
        remove_fnn_w_softmax_policy_mocker = mocker.MagicMock(side_effect=remove_fnn_w_softmax_policy)
        return remove_fnn_w_softmax_policy_mocker

    @pytest.fixture
    def get_policy(self, mocker):
        """
        pytest fixture for the get fnn_w_softmax policy
        """
        def get_fnn_w_softmax_policy(id):
            policy = TestResourcesFnnWSoftmaxSuite.get_example_policy()
            return policy
        get_fnn_w_softmax_policy_mocker = mocker.MagicMock(side_effect=get_fnn_w_softmax_policy)
        return get_fnn_w_softmax_policy_mocker

    @staticmethod
    def get_example_policy():
        """
        :return: an example fnn_w_softmax plicy class full of dummy values
        """
        state_list = [State(id=1, name="JohnDoe", descr="description", state_type=StateType(0))]
        e_config_class = ExperimentConfig(output_dir="output_directory", title="title", random_seeds=[1, 2, 3],
                                          agent_type=AgentType(1),
                                          hparams={'element': HParam(10, name="John", descr="Doe")},
                                          log_every=10, player_type=PlayerType(1),
                                          player_idx=10, br_log_every=10)
        obj = FNNWithSoftmaxPolicy(policy_network=None,
                                   simulation_name="JohnDoeSimulation1", save_path="", player_type=PlayerType(1),
                                   states=state_list, actions=[Action(id=10, descr="null")],
                                   experiment_config=e_config_class, avg_R=1.1,
                                   input_dim=15, output_dim=30)
        return obj

    def test_fnnwsm_policies_get(
            self,
            flask_app,
            mocker,
            list_fnn_w_softmax,
            logged_in,
            not_logged_in,
            logged_in_as_admin,
            list_fnn_w_softmax_ids,
    ) -> None:
        """
        testing the GET HTTPS method  for the /fnn-w-softmax-policies resource
        """
        test_policy = TestResourcesFnnWSoftmaxSuite.get_example_policy()
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_fnn_w_softmax_policies",
                     side_effect=list_fnn_w_softmax)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_fnn_w_softmax_policies_ids",
                     side_effect=list_fnn_w_softmax_ids)
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.FNN_W_SOFTMAX_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.FNN_W_SOFTMAX_POLICIES_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        fnnwsm_vec_dict = response_data_list[0]
        assert fnnwsm_vec_dict["id"] == 111
        assert fnnwsm_vec_dict["simulation"] == "some_simulation"
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.FNN_W_SOFTMAX_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        fnnwsm_vec = FNNWithSoftmaxPolicy.from_dict(response_data_list[0])
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert fnnwsm_vec.actions[0].descr == test_policy.actions[0].descr
        assert fnnwsm_vec.actions[0].id == test_policy.actions[0].id
        assert fnnwsm_vec.agent_type == test_policy.agent_type
        assert fnnwsm_vec.avg_R == test_policy.avg_R
        assert fnnwsm_vec.experiment_config.agent_type == test_policy.experiment_config.agent_type
        assert fnnwsm_vec.experiment_config.br_log_every == test_policy.experiment_config.br_log_every
        assert fnnwsm_vec.experiment_config.hparams["element"].descr == \
            test_policy.experiment_config.hparams["element"].descr
        assert fnnwsm_vec.experiment_config.hparams["element"].name == \
            test_policy.experiment_config.hparams["element"].name
        assert fnnwsm_vec.experiment_config.hparams["element"].value == \
            test_policy.experiment_config.hparams["element"].value
        assert fnnwsm_vec.experiment_config.log_every == \
            test_policy.experiment_config.log_every
        assert fnnwsm_vec.experiment_config.output_dir == \
            test_policy.experiment_config.output_dir
        assert fnnwsm_vec.experiment_config.player_idx == \
            test_policy.experiment_config.player_idx
        assert fnnwsm_vec.experiment_config.player_type == \
            test_policy.experiment_config.player_type
        assert fnnwsm_vec.experiment_config.random_seeds == \
            test_policy.experiment_config.random_seeds
        assert fnnwsm_vec.experiment_config.title == \
            test_policy.experiment_config.title
        assert fnnwsm_vec.id == test_policy.id
        assert fnnwsm_vec.input_dim == test_policy.input_dim
        assert fnnwsm_vec.output_dim == test_policy.output_dim
        assert fnnwsm_vec.player_type == test_policy.player_type
        assert fnnwsm_vec.policy_type == test_policy.policy_type
        assert fnnwsm_vec.simulation_name == test_policy.simulation_name
        assert fnnwsm_vec.save_path == test_policy.save_path
        assert fnnwsm_vec.states[0].descr == test_policy.states[0].descr
        assert fnnwsm_vec.states[0].id == test_policy.states[0].id
        assert fnnwsm_vec.states[0].name == test_policy.states[0].name
        assert fnnwsm_vec.states[0].state_type == test_policy.states[0].state_type
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.FNN_W_SOFTMAX_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        fnnwsm_vec = FNNWithSoftmaxPolicy.from_dict(response_data_list[0])
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert fnnwsm_vec.policy_network == test_policy.policy_network
        assert fnnwsm_vec.actions[0].descr == test_policy.actions[0].descr
        assert fnnwsm_vec.actions[0].id == test_policy.actions[0].id
        assert fnnwsm_vec.agent_type == test_policy.agent_type
        assert fnnwsm_vec.avg_R == test_policy.avg_R
        assert fnnwsm_vec.experiment_config.agent_type == test_policy.experiment_config.agent_type
        assert fnnwsm_vec.experiment_config.br_log_every == test_policy.experiment_config.br_log_every
        assert fnnwsm_vec.experiment_config.hparams["element"].descr == \
            test_policy.experiment_config.hparams["element"].descr
        assert fnnwsm_vec.experiment_config.hparams["element"].name == \
            test_policy.experiment_config.hparams["element"].name
        assert fnnwsm_vec.experiment_config.hparams["element"].value == \
            test_policy.experiment_config.hparams["element"].value
        assert fnnwsm_vec.experiment_config.log_every == \
            test_policy.experiment_config.log_every
        assert fnnwsm_vec.experiment_config.output_dir == \
            test_policy.experiment_config.output_dir
        assert fnnwsm_vec.experiment_config.player_idx == \
            test_policy.experiment_config.player_idx
        assert fnnwsm_vec.experiment_config.player_type == \
            test_policy.experiment_config.player_type
        assert fnnwsm_vec.experiment_config.random_seeds == \
            test_policy.experiment_config.random_seeds
        assert fnnwsm_vec.experiment_config.title == \
            test_policy.experiment_config.title
        assert fnnwsm_vec.id == test_policy.id
        assert fnnwsm_vec.input_dim == test_policy.input_dim
        assert fnnwsm_vec.output_dim == test_policy.output_dim
        assert fnnwsm_vec.player_type == test_policy.player_type
        assert fnnwsm_vec.simulation_name == test_policy.simulation_name
        assert fnnwsm_vec.save_path == test_policy.save_path
        assert fnnwsm_vec.states[0].descr == test_policy.states[0].descr
        assert fnnwsm_vec.states[0].id == test_policy.states[0].id
        assert fnnwsm_vec.states[0].name == test_policy.states[0].name
        assert fnnwsm_vec.states[0].state_type == test_policy.states[0].state_type

    def test_fnnwsm_policies_delete(
            self,
            flask_app,
            mocker,
            list_fnn_w_softmax,
            logged_in,
            not_logged_in,
            logged_in_as_admin,
            remove,
    ) -> None:
        """
        testing  the DELETE HTTPS method for the /fnn-w-softmax-policies resource
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_fnn_w_softmax_policy",
                     side_effect=remove)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_fnn_w_softmax_policies",
                     side_effect=list_fnn_w_softmax)
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.FNN_W_SOFTMAX_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.FNN_W_SOFTMAX_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,
        )
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.FNN_W_SOFTMAX_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}

    def test_fnnwsm_policies_id_get(self, flask_app, mocker, logged_in,
                                    not_logged_in, logged_in_as_admin,
                                    get_policy,) -> None:
        """
        testing the HTTPS GET method for the /fnn-w-softmax-policies/id resource
        """
        test_policy = TestResourcesFnnWSoftmaxSuite.get_example_policy()
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_fnn_w_softmax_policy",
                     side_effect=get_policy)
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.FNN_W_SOFTMAX_POLICIES_RESOURCE}"f"/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.FNN_W_SOFTMAX_POLICIES_RESOURCE}"f"/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        fnnwsm_vec = FNNWithSoftmaxPolicy.from_dict(response_data_list)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert fnnwsm_vec.policy_network == test_policy.policy_network
        assert fnnwsm_vec.actions[0].descr == test_policy.actions[0].descr
        assert fnnwsm_vec.actions[0].id == test_policy.actions[0].id
        assert fnnwsm_vec.agent_type == test_policy.agent_type
        assert fnnwsm_vec.avg_R == test_policy.avg_R
        assert fnnwsm_vec.experiment_config.agent_type == test_policy.experiment_config.agent_type
        assert fnnwsm_vec.experiment_config.br_log_every == test_policy.experiment_config.br_log_every
        assert fnnwsm_vec.experiment_config.hparams["element"].descr == \
            test_policy.experiment_config.hparams["element"].descr
        assert fnnwsm_vec.experiment_config.hparams["element"].name == \
            test_policy.experiment_config.hparams["element"].name
        assert fnnwsm_vec.experiment_config.hparams["element"].value == \
            test_policy.experiment_config.hparams["element"].value
        assert fnnwsm_vec.experiment_config.log_every == \
            test_policy.experiment_config.log_every
        assert fnnwsm_vec.experiment_config.output_dir == \
            test_policy.experiment_config.output_dir
        assert fnnwsm_vec.experiment_config.player_idx == \
            test_policy.experiment_config.player_idx
        assert fnnwsm_vec.experiment_config.player_type == \
            test_policy.experiment_config.player_type
        assert fnnwsm_vec.experiment_config.random_seeds == \
            test_policy.experiment_config.random_seeds
        assert fnnwsm_vec.experiment_config.title == \
            test_policy.experiment_config.title
        assert fnnwsm_vec.id == test_policy.id
        assert fnnwsm_vec.input_dim == test_policy.input_dim
        assert fnnwsm_vec.output_dim == test_policy.output_dim
        assert fnnwsm_vec.player_type == test_policy.player_type
        assert fnnwsm_vec.simulation_name == test_policy.simulation_name
        assert fnnwsm_vec.save_path == test_policy.save_path
        assert fnnwsm_vec.states[0].descr == test_policy.states[0].descr
        assert fnnwsm_vec.states[0].id == test_policy.states[0].id
        assert fnnwsm_vec.states[0].name == test_policy.states[0].name
        assert fnnwsm_vec.states[0].state_type == test_policy.states[0].state_type
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.FNN_W_SOFTMAX_POLICIES_RESOURCE}"f"/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        fnnwsm_vec = FNNWithSoftmaxPolicy.from_dict(response_data_list)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert fnnwsm_vec.policy_network == test_policy.policy_network
        assert fnnwsm_vec.actions[0].descr == test_policy.actions[0].descr
        assert fnnwsm_vec.actions[0].id == test_policy.actions[0].id
        assert fnnwsm_vec.agent_type == test_policy.agent_type
        assert fnnwsm_vec.avg_R == test_policy.avg_R
        assert fnnwsm_vec.experiment_config.agent_type == test_policy.experiment_config.agent_type
        assert fnnwsm_vec.experiment_config.br_log_every == test_policy.experiment_config.br_log_every
        assert fnnwsm_vec.experiment_config.hparams["element"].descr == \
            test_policy.experiment_config.hparams["element"].descr
        assert fnnwsm_vec.experiment_config.hparams["element"].name == \
            test_policy.experiment_config.hparams["element"].name
        assert fnnwsm_vec.experiment_config.hparams["element"].value == \
            test_policy.experiment_config.hparams["element"].value
        assert fnnwsm_vec.experiment_config.log_every == \
            test_policy.experiment_config.log_every
        assert fnnwsm_vec.experiment_config.output_dir == \
            test_policy.experiment_config.output_dir
        assert fnnwsm_vec.experiment_config.player_idx == \
            test_policy.experiment_config.player_idx
        assert fnnwsm_vec.experiment_config.player_type == \
            test_policy.experiment_config.player_type
        assert fnnwsm_vec.experiment_config.random_seeds == \
            test_policy.experiment_config.random_seeds
        assert fnnwsm_vec.experiment_config.title == \
            test_policy.experiment_config.title
        assert fnnwsm_vec.id == test_policy.id
        assert fnnwsm_vec.input_dim == test_policy.input_dim
        assert fnnwsm_vec.output_dim == test_policy.output_dim
        assert fnnwsm_vec.player_type == test_policy.player_type
        assert fnnwsm_vec.simulation_name == test_policy.simulation_name
        assert fnnwsm_vec.save_path == test_policy.save_path
        assert fnnwsm_vec.states[0].descr == test_policy.states[0].descr
        assert fnnwsm_vec.states[0].id == test_policy.states[0].id
        assert fnnwsm_vec.states[0].name == test_policy.states[0].name
        assert fnnwsm_vec.states[0].state_type == test_policy.states[0].state_type

    def test_fnnwsm_policies_id_delete(self, flask_app, mocker, logged_in,
                                       not_logged_in, logged_in_as_admin,
                                       get_policy, remove) -> None:

        """
        testing the HTTPS DELETE method for the /dnn-w-softmax-policies/id resource
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_fnn_w_softmax_policy",
                     side_effect=get_policy)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.remove_fnn_w_softmax_policy",
                     side_effect=remove)
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.FNN_W_SOFTMAX_POLICIES_RESOURCE}"f"/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.FNN_W_SOFTMAX_POLICIES_RESOURCE}"f"/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,
        )
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.FNN_W_SOFTMAX_POLICIES_RESOURCE}"f"/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
