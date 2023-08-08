from typing import List, Tuple, Dict
import base64
import json
import pytest
import pytest_mock
import numpy as np
import csle_common.constants.constants as constants
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.simulation_config.action_space_config import ActionSpaceConfig
from csle_common.dao.simulation_config.env_parameter import EnvParameter
from csle_common.dao.simulation_config.env_parameters_config import EnvParametersConfig
from csle_common.dao.simulation_config.initial_state_distribution_config import InitialStateDistributionConfig
from csle_common.dao.simulation_config.joint_action_space_config import JointActionSpaceConfig
from csle_common.dao.simulation_config.joint_observation_space_config import JointObservationSpaceConfig
from csle_common.dao.simulation_config.observation import Observation
from csle_common.dao.simulation_config.observation_function_config import ObservationFunctionConfig
from csle_common.dao.simulation_config.observation_space_config import ObservationSpaceConfig
from csle_common.dao.simulation_config.player_config import PlayerConfig
from csle_common.dao.simulation_config.players_config import PlayersConfig
from csle_common.dao.simulation_config.reward_function_config import RewardFunctionConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_input_config import SimulationEnvInputConfig
from csle_common.dao.simulation_config.state import State
from csle_common.dao.simulation_config.state_space_config import StateSpaceConfig
from csle_common.dao.simulation_config.state_type import StateType
from csle_common.dao.simulation_config.time_step_type import TimeStepType
from csle_common.dao.simulation_config.transition_operator_config import TransitionOperatorConfig
from csle_common.dao.simulation_config.value_type import ValueType
from gym_csle_stopping_game.dao.stopping_game_attacker_mdp_config import StoppingGameAttackerMdpConfig
from gym_csle_stopping_game.dao.stopping_game_defender_pomdp_config import StoppingGameDefenderPomdpConfig
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from csle_common.dao.training.random_policy import RandomPolicy
from csle_common.dao.training.player_type import PlayerType
import csle_rest_api.constants.constants as api_constants
from csle_common.util.experiment_util import ExperimentUtil
from csle_rest_api.rest_api import create_app
from csle_common.dao.encoding.np_encoder import NpEncoder


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
            list_obj = TestResourcesSimulationsSuite.example_simulation_config()
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
    def uninstall(self, mocker: pytest_mock.MockFixture):
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
    def list_sim_id(self, mocker: pytest_mock.MockFixture):
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
    def get_sim(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_simulation method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_simulation(name: str) -> SimulationEnvConfig:
            sim_env = TestResourcesSimulationsSuite.example_simulation_config()
            return sim_env

        get_simulation_mocker = mocker.MagicMock(side_effect=get_simulation)
        return get_simulation_mocker

    @staticmethod
    def default_config(name: str, version: str = "0.0.2", min_alerts_weighted_by_priority: int = 0,
                       max_alers_weighted_by_priority: int = 100) -> SimulationEnvConfig:
        """
        Help function that returns an example transition SimulationEnvConfig

        :param name: the name of the environment
        :param version: the version string
        :param min_alerts_weighted_by_priority: if using heuristic observation space, this defines the min number of
                                                alerts weighted by priority
        :param max_alers_weighted_by_priority: if using heuristic observation space, this defines the max number of
                                               alerts weighted by priority
        :return:the example configuration
        """
        players_config = TestResourcesSimulationsSuite.default_players_config()
        state_space_config = TestResourcesSimulationsSuite.default_state_space_config()
        joint_action_space_config = TestResourcesSimulationsSuite.default_joint_action_space_config()
        joint_observation_space_config = TestResourcesSimulationsSuite.default_joint_observation_space_config(
            min_alerts_weighted_by_priority=min_alerts_weighted_by_priority,
            max_alerts_weighted_by_priority=max_alers_weighted_by_priority)
        transition_operator_config = TestResourcesSimulationsSuite.default_transition_operator_config()
        observation_function_config = TestResourcesSimulationsSuite.default_observation_function_config(
            defender_obs_space=joint_observation_space_config.observation_spaces[0],
            joint_action_space=joint_action_space_config, state_space=state_space_config,
            min_alerts_weighted_by_priority=min_alerts_weighted_by_priority,
            max_alerts_weighted_by_priority=max_alers_weighted_by_priority)
        reward_function_config = TestResourcesSimulationsSuite.default_reward_function_config()
        initial_state_distribution_config = TestResourcesSimulationsSuite.default_initial_state_distribution_config()
        input_config = TestResourcesSimulationsSuite.default_input_config(
            defender_observation_space_config=joint_observation_space_config.observation_spaces[0],
            reward_function_config=reward_function_config,
            transition_tensor_config=transition_operator_config,
            observation_function_config=observation_function_config,
            initial_state_distribution_config=initial_state_distribution_config)
        env_parameters_config = TestResourcesSimulationsSuite.default_env_parameters_config()
        descr = "A two-player zero-sum one-sided partially observed stochastic game. " \
                "The game is based on the optimal stopping formulation of intrusion prevention " \
                "from (Hammar and Stadler 2021, https://arxiv.org/abs/2111.00289)"
        simulation_env_config = SimulationEnvConfig(
            name=name, version=version, descr=descr,
            players_config=players_config, state_space_config=state_space_config,
            joint_action_space_config=joint_action_space_config,
            joint_observation_space_config=joint_observation_space_config,
            transition_operator_config=transition_operator_config,
            observation_function_config=observation_function_config, reward_function_config=reward_function_config,
            initial_state_distribution_config=initial_state_distribution_config,
            simulation_env_input_config=input_config,
            time_step_type=TimeStepType.DISCRETE,
            gym_env_name="csle-stopping-game-v1", env_parameters_config=env_parameters_config,
            plot_transition_probabilities=True, plot_observation_function=True, plot_reward_function=True
        )
        return simulation_env_config

    @staticmethod
    def default_env_parameters_config() -> EnvParametersConfig:
        """
        Help function that returns an example envParametersConfig

        :return: the example env parameters config
        """
        config = EnvParametersConfig(
            parameters=[
                EnvParameter(id=0, name="l=1", descr="1 stop remaining of the defender"),
                EnvParameter(id=1, name="l=2", descr="2 stops remaining of the defender"),
                EnvParameter(id=2, name="l=3", descr="3 stops remaining of the defender")
            ]
        )
        return config

    @staticmethod
    def default_players_config() -> PlayersConfig:
        """
        Help function that returns an example players config

        :return: the example players configuration of the simulation
        """
        player_configs = [
            PlayerConfig(name="defender", id=1, descr="The defender which tries to detect, prevent, "
                                                      "and interrupt intrusions for the infrastructure"),
            PlayerConfig(name="attacker", id=2, descr="The attacker which tries to intrude on the infrastructure")
        ]
        players_config = PlayersConfig(player_configs=player_configs)
        return players_config

    @staticmethod
    def default_state_space_config() -> StateSpaceConfig:
        """
        Help function that returns an example state space config

        :return: the example state space configuration of the simulation
        """
        states = [
            State(id=0, name="no intrusion state", descr="A Markov state representing the case where the attacker "
                                                         "has not yet started an intrusion",
                  state_type=StateType.ACTIVE),
            State(id=1, name="intrusion state", descr="A Markov state representing the state of intrusion",
                  state_type=StateType.ACTIVE),
            State(id=2, name="terminal state", descr="A terminal state the models the end of a game episode",
                  state_type=StateType.TERMINAL)
        ]
        state_space_config = StateSpaceConfig(states=states)
        return state_space_config

    @staticmethod
    def default_joint_action_space_config() -> JointActionSpaceConfig:
        """
        Help function that returns an example joint action space config

        :return: the example joint action space of all players in the simulation
        """
        action_spaces = [
            ActionSpaceConfig(
                actions=[
                    Action(
                        id=0, descr="Continue action, it means that the defender continues to monitor the system "
                                    "but does not take an active action"
                    ),
                    Action(
                        id=1, descr="Stop action, it means that the defender takes an active defensive action"
                    )
                ],
                player_id=1, action_type=ValueType.INTEGER
            ),
            ActionSpaceConfig(
                actions=[
                    Action(
                        id=0, descr="Continue action, it means that the attacker continues the intrusion if it "
                                    "is in progress or that it continues to wait if it has not started the intrusion "
                    ),
                    Action(
                        id=1, descr="Stop action, it means that the attacker stops the intrusion if it is in "
                                    "progress and otherwise it starts the intrusion"
                    )
                ],
                player_id=2, action_type=ValueType.INTEGER
            )
        ]
        joint_action_sapce_config = JointActionSpaceConfig(action_spaces=action_spaces)
        return joint_action_sapce_config

    @staticmethod
    def default_joint_observation_space_config(min_alerts_weighted_by_priority: int = 0,
                                               max_alerts_weighted_by_priority: int = 100) \
            -> JointObservationSpaceConfig:
        """
        Help function that returns an example join observation space config

        :param min_alerts_weighted_by_priority: if using heuristic observation space, this defines the min number of
                                                alerts weighted by priority
        :param max_alerts_weighted_by_priority: if using heuristic observation space, this defines the max number of
                                                alerts weighted by priority
        :return: the example joint observation space configuration
        """
        observation_id_to_observation_id_vector = {}
        observation_id_to_observation_vector = {}
        defender_observations = []
        component_observations: Dict[str, List[Observation]] = {}
        component_observations["alerts_weighted_by_priority"] = []
        for val in range(min_alerts_weighted_by_priority, max_alerts_weighted_by_priority):
            component_observations["alerts_weighted_by_priority"].append(Observation(
                id=val, val=val, descr=f"{val} IDS alerts weighted by priority"))

        for i in range(min_alerts_weighted_by_priority, max_alerts_weighted_by_priority):
            id = i
            defender_observations.append(Observation(
                id=id, val=id,
                descr=f"{i} IDS alerts weighted by priority"))
            observation_id_to_observation_vector[id] = [i]
            observation_id_to_observation_id_vector[id] = [i]

        observation_component_name_to_index = {"alerts_weighted_by_priority": 0}

        observation_spaces = [
            ObservationSpaceConfig(
                observations=defender_observations,
                observation_type=ValueType.INTEGER,
                player_id=2,
                descr="The observation space of the attacker. The attacker has inside information in "
                      "the infrastructure and observes the same metrics as the defender",
                observation_id_to_observation_id_vector=observation_id_to_observation_id_vector,
                observation_component_name_to_index=observation_component_name_to_index,
                component_observations=component_observations,
                observation_id_to_observation_vector=observation_id_to_observation_vector
            )
        ]
        joint_observation_space_config = JointObservationSpaceConfig(
            observation_spaces=observation_spaces
        )
        return joint_observation_space_config

    @staticmethod
    def default_reward_function_config() -> RewardFunctionConfig:
        """
        Help function that returns an example reward function configuration

        :return: the example reward function configuration
        """
        reward_function_config = RewardFunctionConfig(
            reward_tensor=list(StoppingGameUtil.reward_tensor(R_INT=-1, R_COST=-2, R_SLA=0, R_ST=10, L=3)))
        return reward_function_config

    @staticmethod
    def default_transition_operator_config() -> TransitionOperatorConfig:
        """
        Help function that returns an example transition tensor configuration

        :return: the default transition tensor configuration
        """
        transition_operator_config = TransitionOperatorConfig(
            transition_tensor=list(StoppingGameUtil.transition_tensor(L=3, p=0.01)))
        return transition_operator_config

    @staticmethod
    def default_observation_function_config(
            defender_obs_space: ObservationSpaceConfig, joint_action_space: JointActionSpaceConfig,
            state_space: StateSpaceConfig,
            min_alerts_weighted_by_priority: int = 0, max_alerts_weighted_by_priority: int = 100) \
            -> ObservationFunctionConfig:
        """
        Help function that returns an example observation function config

        :param min_alerts_weighted_by_priority: if using heuristic observation space, this defines the min number of
                                                alerts weighted by priority
        :param max_alerts_weighted_by_priority: if using heuristic observation space, this defines the max number of
                                                alerts weighted by priority
        :return: the example configuration of the observation function
        """
        component_observation_tensors = {}
        priority_alerts_tensor = StoppingGameUtil.observation_tensor(
            len(range(min_alerts_weighted_by_priority, max_alerts_weighted_by_priority)) - 1)
        component_observation_tensors["alerts_weighted_by_priority"] = list(priority_alerts_tensor.tolist())
        observation_tensor = priority_alerts_tensor
        observation_function_config = ObservationFunctionConfig(
            observation_tensor=observation_tensor, component_observation_tensors=component_observation_tensors)
        return observation_function_config

    @staticmethod
    def default_initial_state_distribution_config() -> InitialStateDistributionConfig:
        """
        Help function that returns an example initial state distribution config

        :return: the example initial state distribution configuration
        """
        initial_state_distribution_config = InitialStateDistributionConfig(
            initial_state_distribution=list(StoppingGameUtil.b1()))
        return initial_state_distribution_config

    @staticmethod
    def default_input_config(defender_observation_space_config: ObservationSpaceConfig,
                             reward_function_config: RewardFunctionConfig,
                             transition_tensor_config: TransitionOperatorConfig,
                             observation_function_config: ObservationFunctionConfig,
                             initial_state_distribution_config: InitialStateDistributionConfig) \
            -> SimulationEnvInputConfig:
        """
        Help function that returns an example environment input configuration

        :param defender_observation_space_config: the configuration of the defender's observation space
        :param reward_function_config: the reward function configuration
        :param transition_tensor_config: the transition tensor configuration
        :param observation_function_config: the observation function configuration
        :param initial_state_distribution_config: the initial state distribution configuration
        :return: The example input configuration to the OpenAI gym environment
        """
        L = 3
        R_INT = -5
        R_COST = -5
        R_SLA = 1
        R_ST = 5

        config = StoppingGameConfig(
            A1=StoppingGameUtil.attacker_actions(), A2=StoppingGameUtil.defender_actions(), L=L, R_INT=R_INT,
            R_COST=R_COST,
            R_SLA=R_SLA, R_ST=R_ST, b1=np.array(initial_state_distribution_config.initial_state_distribution),
            save_dir=ExperimentUtil.default_output_dir() + "/results",
            T=np.array(transition_tensor_config.transition_tensor),
            O=np.array(list(defender_observation_space_config.observation_id_to_observation_vector.keys())),
            Z=np.array(observation_function_config.observation_tensor),
            R=np.array(reward_function_config.reward_tensor),
            S=StoppingGameUtil.state_space(), env_name="csle-stopping-game-v1", checkpoint_traces_freq=100000,
            gamma=1)
        return config

    @staticmethod
    def example_simulation_config() -> SimulationEnvConfig:
        """
        Help function that returns an example simulation environment configuration

        :return: the example configuration
        """
        config = TestResourcesSimulationsSuite.default_config(name="csle-stopping-game-002", version="0.0.2")
        return config

    @staticmethod
    def example_attacker_simulation_config() -> SimulationEnvConfig:
        """
        Help function that returns an example attacker simulation environment configuration

        :return: the example configuration
        """
        config = TestResourcesSimulationsSuite.default_config(name="csle-stopping-mdp-attacker-002", version="0.0.2")
        config.gym_env_name = "csle-stopping-game-mdp-attacker-v1"
        config.players_config = PlayersConfig(player_configs=[config.players_config.player_configs[1]])
        config.simulation_env_input_config = StoppingGameAttackerMdpConfig(
            stopping_game_config=config.simulation_env_input_config, stopping_game_name="csle-stopping-game-v1",
            defender_strategy=RandomPolicy(actions=[config.joint_action_space_config.action_spaces[0].actions],
                                           player_type=PlayerType.DEFENDER, stage_policy_tensor=None),
            env_name="csle-stopping-game-mdp-attacker-v1")
        return config

    @staticmethod
    def example_defender_simulation_config() -> SimulationEnvConfig:
        """
        Help function that returns an example defender simulation environment configuration

        :return: the example configuration
        """
        config = TestResourcesSimulationsSuite.default_config(name="csle-stopping-pomdp-defender-002", version="0.0.2")
        config.gym_env_name = "csle-stopping-game-pomdp-defender-v1"
        config.players_config = PlayersConfig(player_configs=[config.players_config.player_configs[0]])
        attacker_stage_strategy = np.zeros((3, 2))
        attacker_stage_strategy[0][0] = 0.9
        attacker_stage_strategy[0][1] = 0.1
        attacker_stage_strategy[1][0] = 0.9
        attacker_stage_strategy[1][1] = 0.1
        attacker_stage_strategy[2] = attacker_stage_strategy[1]
        config.simulation_env_input_config = StoppingGameDefenderPomdpConfig(
            stopping_game_config=config.simulation_env_input_config, stopping_game_name="csle-stopping-game-v1",
            attacker_strategy=RandomPolicy(actions=config.joint_action_space_config.action_spaces[1].actions,
                                           player_type=PlayerType.ATTACKER,
                                           stage_policy_tensor=list(attacker_stage_strategy)),
            env_name="csle-stopping-game-pomdp-defender-v1")
        return config

    @pytest.fixture
    def get_sim_im(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the get_simulation_image method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_simulation_image(simulation_name: str) -> Tuple[str, bytes]:
            return ("null", b'null')

        get_simulation_image_mocker = mocker.MagicMock(side_effect=get_simulation_image)
        return get_simulation_image_mocker

    def test_simulations_get(self, mocker: pytest_mock.MockFixture, flask_app, list_sim, list_sim_im,
                             uninstall, list_sim_id, get_sim, get_sim_im, not_logged_in, logged_in,
                             logged_in_as_admin) -> None:
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
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_simulations", side_effect=list_sim)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_simulation_images",
                     side_effect=list_sim_im)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        response_data_dict = response_data_list[0]
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        ex_data = TestResourcesSimulationsSuite.example_simulation_config()
        ex_data_dict = json.loads(json.dumps(ex_data.to_dict(), indent=4, sort_keys=True, cls=NpEncoder))
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

    def test_simulations_delete(self, mocker: pytest_mock.MockFixture, flask_app, list_sim, list_sim_im,
                                uninstall, list_sim_id, get_sim, get_sim_im, not_logged_in, logged_in,
                                logged_in_as_admin) -> None:
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
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_simulations", side_effect=list_sim)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_simulation_images",
                     side_effect=list_sim_im)
        mocker.patch("csle_common.controllers.simulation_env_controller.SimulationEnvController.uninstall_simulation",
                     side_effect=uninstall)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_simulation_ids",
                     side_effect=list_sim_id)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
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

    def test_simulations_get_id(self, mocker: pytest_mock.MockFixture, flask_app, list_sim, list_sim_im, uninstall,
                                list_sim_id, get_sim, get_sim_im, not_logged_in, logged_in, logged_in_as_admin) -> None:
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
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_simulation", side_effect=get_sim)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_simulation_image",
                     side_effect=get_sim_im)
        mocker.patch("csle_common.controllers.simulation_env_controller.SimulationEnvController.uninstall_simulation",
                     side_effect=uninstall)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_simulation_ids",
                     side_effect=list_sim_id)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}/-1)")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        ex_data = TestResourcesSimulationsSuite.example_simulation_config()
        ex_data.image = base64.b64encode(b'null').decode()
        ex_data_dict = json.loads(json.dumps(ex_data.to_dict(), indent=4, sort_keys=True, cls=NpEncoder))
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for k in response_data_dict:
            assert response_data_dict[k] == ex_data_dict[k]
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}/10")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        ex_data = TestResourcesSimulationsSuite.example_simulation_config()
        ex_data.image = base64.b64encode(b'null').decode()
        ex_data_dict = json.loads(json.dumps(ex_data.to_dict(), indent=4, sort_keys=True, cls=NpEncoder))
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        for k in response_data_dict:
            assert response_data_dict[k] == ex_data_dict[k]

    def test_simulations_delete_id(self, mocker: pytest_mock.MockFixture, flask_app, list_sim, list_sim_im, uninstall,
                                   list_sim_id, get_sim, get_sim_im, not_logged_in, logged_in, logged_in_as_admin) \
            -> None:
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
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_simulation", side_effect=get_sim)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_simulation_image",
                     side_effect=get_sim_im)
        mocker.patch("csle_common.controllers.simulation_env_controller.SimulationEnvController.uninstall_simulation",
                     side_effect=uninstall)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade.list_simulation_ids",
                     side_effect=list_sim_id)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=not_logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}/-1)")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}/-1)")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_dict == {}
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized", side_effect=logged_in_as_admin)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.SIMULATIONS_RESOURCE}/-1)")
        response_data = response.data.decode("utf-8")
        response_data_dict = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_dict == {}
