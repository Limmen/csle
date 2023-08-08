import base64
import json
from typing import List, Tuple

import csle_common.constants.constants as constants
import pytest
import pytest_mock
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.simulation_config.action_space_config import ActionSpaceConfig
from csle_common.dao.simulation_config.env_parameter import EnvParameter
from csle_common.dao.simulation_config.env_parameters_config import EnvParametersConfig
from csle_common.dao.simulation_config.initial_state_distribution_config import (
    InitialStateDistributionConfig,
)
from csle_common.dao.simulation_config.joint_action_space_config import (
    JointActionSpaceConfig,
)
from csle_common.dao.simulation_config.joint_observation_space_config import (
    JointObservationSpaceConfig,
)
from csle_common.dao.simulation_config.observation import Observation
from csle_common.dao.simulation_config.observation_function_config import (
    ObservationFunctionConfig,
)
from csle_common.dao.simulation_config.observation_space_config import (
    ObservationSpaceConfig,
)
from csle_common.dao.simulation_config.player_config import PlayerConfig
from csle_common.dao.simulation_config.players_config import PlayersConfig
from csle_common.dao.simulation_config.reward_function_config import (
    RewardFunctionConfig,
)
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_input_config import (
    SimulationEnvInputConfig,
)
from csle_common.dao.simulation_config.state import State
from csle_common.dao.simulation_config.state_space_config import StateSpaceConfig
from csle_common.dao.simulation_config.state_type import StateType
from csle_common.dao.simulation_config.time_step_type import TimeStepType
from csle_common.dao.simulation_config.transition_operator_config import (
    TransitionOperatorConfig,
)
from csle_common.dao.simulation_config.value_type import ValueType

import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestResourcesSimulationsSuite:
    """
    Test suite for /simulations resource
    """

    @pytest.fixture
    def flask_app(self):
        """
        Gets the Flask app

        :return: the flask app fixture representing the webserver
        """
        return create_app(static_folder="../../../../../management-system/csle-mgmt-webapp/build")

    @pytest.fixture
    def list_sim(self, mocker: pytest_mock.MockFixture):
        """
        Pytst dixture for mocking the list_simulations method
        
        :param mocker: the pytest mocker object
        """
        def list_simulations() -> List[SimulationEnvConfig]:
            list_obj = TestResourcesSimulationsSuite.get_ex_sim_env()
            return [list_obj]
        list_simulations_mocker = mocker.MagicMock(side_effect=list_simulations)
        return list_simulations_mocker

    @pytest.fixture
    def list_sim_im(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the list_simulations_images method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def list_simulation_images() -> List[Tuple[str, bytes]]:
            return [("null", b'null')]
        list_simulation_images_mocker = mocker.MagicMock(side_effect=list_simulation_images)
        return list_simulation_images_mocker

    @pytest.fixture
    def uninstall(self, mocker):
        """
        Pytest fixture for mocking the uninstall_simulation method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def uninstall_simulation(sim: SimulationEnvConfig) -> None:
            return None
        uninstall_simulation_mocker = mocker.MagicMock(side_effect=uninstall_simulation)
        return uninstall_simulation_mocker

    @pytest.fixture
    def list_sim_id(self, mocker):
        """
        Pytest fixture for mocking the list_simulation_ids method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def list_simulation_ids() -> List[Tuple[str, int]]:
            return [("null", 1)]
        list_simulation_ids_mocker = mocker.MagicMock(side_effect=list_simulation_ids)
        return list_simulation_ids_mocker

    @pytest.fixture
    def get_sim(self, mocker):
        """
        Pytest fixture for mocking the get_simulation method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def get_simulation(name: str) -> SimulationEnvConfig:
            sim_env = TestResourcesSimulationsSuite.get_ex_sim_env()
            return sim_env
        get_simulation_mocker = mocker.MagicMock(side_effect=get_simulation)
        return get_simulation_mocker

    @staticmethod
    def get_ex_sim_env() -> SimulationEnvConfig:
        """Static help method for obtaining an example SimulationsEnvConfig object"""
        os_config = ObservationSpaceConfig(observations=[Observation(id=1, val=10, descr="null")],
                                           observation_type=ValueType.INTEGER.value, descr="null",
                                           player_id=1, observation_component_name_to_index={"JohnDoe": 1},
                                           observation_id_to_observation_id_vector={1: ["null"]},
                                           observation_id_to_observation_vector={1: ["null"]},
                                           component_observations={"JohnDoe": [Observation(id=1, val=10, descr="null")
                                                                               ]})
        of_config = ObservationFunctionConfig(observation_tensor=[], component_observation_tensors={"null": []})
        isd_config = InitialStateDistributionConfig(initial_state_distribution=[1.0])
        sim_env = SimulationEnvConfig(name="JohnDoe", descr="null", version="null",
                                      gym_env_name="null",
                                      simulation_env_input_config=SimulationEnvInputConfig,
                                      players_config=PlayersConfig(player_configs=[PlayerConfig(name="JohnDoe", id=1,
                                                                                                descr="null")]),
                                      state_space_config=StateSpaceConfig(states=[State(id=1, name="JohnDoe",
                                                                                        descr="null",
                                                                                        state_type=StateType.ACTIVE.
                                                                                        value)]),
                                      joint_action_space_config=JointActionSpaceConfig(action_spaces=[
                                          ActionSpaceConfig(actions=[Action(id=1, descr="null")], player_id=1,
                                                            action_type=ValueType.INTEGER.value, descr="null")]),
                                      joint_observation_space_config=JointObservationSpaceConfig(observation_spaces=[
                                          os_config]),
                                      time_step_type=TimeStepType.DISCRETE.value,
                                      reward_function_config=RewardFunctionConfig(reward_tensor=[]),
                                      transition_operator_config=TransitionOperatorConfig(transition_tensor=[]),
                                      observation_function_config=of_config,
                                      initial_state_distribution_config=isd_config,
                                      env_parameters_config=EnvParametersConfig(parameters=[EnvParameter(id=1,
                                                                                                         name="JohnDoe",
                                                                                                         descr="null")
                                                                                            ]),
                                      plot_transition_probabilities=False,
                                      plot_observation_function=False, plot_reward_function=False)
        return sim_env

    @pytest.fixture
    def get_sim_im(self, mocker):
        """
        Pytest fixture for mocking the get_simulation_image method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """
        def get_simulation_image(simulation_name: str) -> Tuple[str, bytes]:
            return ("null", b'null')
        get_simulation_image_mocker = mocker.MagicMock(side_effect=get_simulation_image)
        return get_simulation_image_mocker

    def test_simulations_get(self, mocker, flask_app, list_sim, list_sim_im,
                             uninstall, list_sim_id, get_sim, get_sim_im,
                             not_logged_in, logged_in, logged_in_as_admin) -> None:
        """
        Testing the GET HTTPS method of the /simulations resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param list_sim: the list_sim fixture
        :param list_sim_im: the list_sim_im fixture
        :param uninstall: the uninstall fixture
        :param list_sim_id: the list_sim_id fixture
        :param get_sim: the get_sim fixture
        :param get_sim_sim: the get_sim_im fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_simulations",
                     side_effect=list_sim)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_simulation_images",
                     side_effect=list_sim_im)

        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}

        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        ex_data = TestResourcesSimulationsSuite.get_ex_sim_env()
        ex_data_dict = ex_data.to_dict()

        response_data_dict["joint_observation_space_config"]["observation_spaces"][0][
            'observation_id_to_observation_id_vector'][1] = \
            response_data_dict["joint_observation_space_config"]["observation_spaces"][0][
                'observation_id_to_observation_id_vector']['1']
        del response_data_dict["joint_observation_space_config"]["observation_spaces"][0][
            'observation_id_to_observation_id_vector']['1']

        response_data_dict["joint_observation_space_config"]["observation_spaces"][0][
            'observation_id_to_observation_vector'][1] = \
            response_data_dict["joint_observation_space_config"]["observation_spaces"][0][
                'observation_id_to_observation_vector']['1']
        del response_data_dict["joint_observation_space_config"]["observation_spaces"][0][
            'observation_id_to_observation_vector']['1']
        for k in response_data_dict:
            assert response_data_dict[k] == ex_data_dict[k]
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_simulation_ids",
                     side_effect=list_sim_id)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == "null"
        assert response_data_dict[api_constants.MGMT_WEBAPP.SIMULATION_PROPERTY] == 1
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        response_data_dict["joint_observation_space_config"]["observation_spaces"][0][
            'observation_id_to_observation_id_vector'][1] = \
            response_data_dict["joint_observation_space_config"]["observation_spaces"][0][
                'observation_id_to_observation_id_vector']['1']
        del response_data_dict["joint_observation_space_config"]["observation_spaces"][0][
            'observation_id_to_observation_id_vector']['1']

        response_data_dict["joint_observation_space_config"]["observation_spaces"][0][
            'observation_id_to_observation_vector'][1] = \
            response_data_dict["joint_observation_space_config"]["observation_spaces"][0][
                'observation_id_to_observation_vector']['1']
        del response_data_dict["joint_observation_space_config"]["observation_spaces"][0][
            'observation_id_to_observation_vector']['1']
        for k in response_data_dict:
            assert response_data_dict[k] == ex_data_dict[k]
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == "null"
        assert response_data_dict[api_constants.MGMT_WEBAPP.SIMULATION_PROPERTY] == 1

    def test_simulations_delete(self, mocker, flask_app, list_sim, list_sim_im,
                                uninstall, list_sim_id, get_sim, get_sim_im,
                                not_logged_in, logged_in, logged_in_as_admin) -> None:
        """
        Testing the DELETE HTTPS method of the /simulations resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param list_sim: the list_sim fixture
        :param list_sim_im: the list_sim_im fixture
        :param uninstall: the uninstall fixture
        :param list_sim_id: the list_sim_id fixture
        :param get_sim: the get_sim fixture
        :param get_sim_sim: the get_sim_im fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_simulations",
                     side_effect=list_sim)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_simulation_images",
                     side_effect=list_sim_im)
        mocker.patch("csle_common.controllers.simulation_env_controller.SimulationEnvController.uninstall_simulation",
                     side_effect=uninstall)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_simulation_ids",
                     side_effect=list_sim_id)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}

        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict == []
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}"
                                                  f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict[api_constants.MGMT_WEBAPP.ID_PROPERTY] == "null"
        assert response_data_dict[api_constants.MGMT_WEBAPP.SIMULATION_PROPERTY] == 1

    def test_simulations_get_id(self, mocker, flask_app, list_sim, list_sim_im,
                                uninstall, list_sim_id, get_sim, get_sim_im,
                                not_logged_in, logged_in, logged_in_as_admin):
        """
        Testing the GET HTTPS method of the /simulations/id resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param list_sim: the list_sim fixture
        :param list_sim_im: the list_sim_im fixture
        :param uninstall: the uninstall fixture
        :param list_sim_id: the list_sim_id fixture
        :param get_sim: the get_sim fixture
        :param get_sim_sim: the get_sim_im fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_simulation",
                     side_effect=get_sim)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_simulation_image",
                     side_effect=get_sim_im)
        mocker.patch("csle_common.controllers.simulation_env_controller.SimulationEnvController.uninstall_simulation",
                     side_effect=uninstall)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_simulation_ids",
                     side_effect=list_sim_id)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}/-1)")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        ex_data = TestResourcesSimulationsSuite.get_ex_sim_env()
        ex_data.image = base64.b64encode(b'null').decode()
        ex_data_dict = ex_data.to_dict()
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        response_data_dict["joint_observation_space_config"]["observation_spaces"][0][
            'observation_id_to_observation_id_vector'][1] = \
            response_data_dict["joint_observation_space_config"]["observation_spaces"][0][
                'observation_id_to_observation_id_vector']['1']
        del response_data_dict["joint_observation_space_config"]["observation_spaces"][0][
            'observation_id_to_observation_id_vector']['1']

        response_data_dict["joint_observation_space_config"]["observation_spaces"][0][
            'observation_id_to_observation_vector'][1] = \
            response_data_dict["joint_observation_space_config"]["observation_spaces"][0][
                'observation_id_to_observation_vector']['1']
        del response_data_dict["joint_observation_space_config"]["observation_spaces"][0][
            'observation_id_to_observation_vector']['1']
        for k in response_data_dict:
            assert response_data_dict[k] == ex_data_dict[k]
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        ex_data = TestResourcesSimulationsSuite.get_ex_sim_env()
        ex_data.image = base64.b64encode(b'null').decode()
        ex_data_dict = ex_data.to_dict()
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        response_data_dict["joint_observation_space_config"]["observation_spaces"][0][
            'observation_id_to_observation_id_vector'][1] = \
            response_data_dict["joint_observation_space_config"]["observation_spaces"][0][
                'observation_id_to_observation_id_vector']['1']
        del response_data_dict["joint_observation_space_config"]["observation_spaces"][0][
            'observation_id_to_observation_id_vector']['1']

        response_data_dict["joint_observation_space_config"]["observation_spaces"][0][
            'observation_id_to_observation_vector'][1] = \
            response_data_dict["joint_observation_space_config"]["observation_spaces"][0][
                'observation_id_to_observation_vector']['1']
        del response_data_dict["joint_observation_space_config"]["observation_spaces"][0][
            'observation_id_to_observation_vector']['1']
        for k in response_data_dict:
            assert response_data_dict[k] == ex_data_dict[k]

    def test_simulations_delete_id(self, mocker, flask_app, list_sim, list_sim_im,
                                   uninstall, list_sim_id, get_sim, get_sim_im,
                                   not_logged_in, logged_in, logged_in_as_admin):
        """
        Testing the DELETE HTTPS method of the /simulations/id resource

        :param mocker: the pytest mocker object
        :param flask_app: the flask_app fixture
        :param list_sim: the list_sim fixture
        :param list_sim_im: the list_sim_im fixture
        :param uninstall: the uninstall fixture
        :param list_sim_id: the list_sim_id fixture
        :param get_sim: the get_sim fixture
        :param get_sim_sim: the get_sim_im fixture
        :return: None
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_simulation",
                     side_effect=get_sim)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_simulation_image",
                     side_effect=get_sim_im)
        mocker.patch("csle_common.controllers.simulation_env_controller.SimulationEnvController.uninstall_simulation",
                     side_effect=uninstall)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_simulation_ids",
                     side_effect=list_sim_id)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}/-1)")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}/-1)")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}/-1)")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict == {}
