import argparse
import os
from csle_common.controllers.simulation_env_controller import SimulationEnvController
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.dao.simulation_config.players_config import PlayersConfig
from csle_common.dao.simulation_config.player_config import PlayerConfig
from csle_common.dao.simulation_config.state import State
from csle_common.dao.simulation_config.state_space_config import StateSpaceConfig
from csle_common.dao.simulation_config.joint_action_space_config import JointActionSpaceConfig
from csle_common.dao.simulation_config.action_space_config import ActionSpaceConfig
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.simulation_config.value_type import ValueType
from csle_common.dao.simulation_config.joint_observation_space_config import JointObservationSpaceConfig
from csle_common.dao.simulation_config.observation_space_config import ObservationSpaceConfig
from csle_common.dao.simulation_config.observation import Observation
from csle_common.dao.simulation_config.time_step_type import TimeStepType
from csle_common.dao.simulation_config.reward_function_config import RewardFunctionConfig
from csle_common.dao.simulation_config.transition_operator_config import TransitionOperatorConfig
from csle_common.dao.simulation_config.observation_function_config import ObservationFunctionConfig
from csle_common.dao.simulation_config.simulation_env_input_config import SimulationEnvInputConfig
from csle_common.dao.simulation_config.initial_state_distribution_config import InitialStateDistributionConfig
from csle_common.dao.simulation_config.env_parameters_config import EnvParametersConfig
from csle_common.dao.simulation_config.env_parameter import EnvParameter
from csle_common.dao.simulation_config.state_type import StateType
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType


def default_config(name: str, version: str = "0.0.1") -> SimulationEnvConfig:
    """
    The default configuration of the simulation environment

    :param name: the name of the simulation environment
    :param version: the version of the environment
    :return: The default configuration of the simulation environment
    """
    players_config = default_players_config()
    state_space_config = default_state_space_config()
    joint_action_space_config = default_joint_action_space_config()
    joint_observation_space_config = default_joint_observation_space_config()
    transition_operator_config = default_transition_operator_config()
    observation_function_config = default_observation_function_config()
    reward_function_config = default_reward_function_config()
    initial_state_distribution_config = default_initial_state_distribution_config()
    input_config = default_input_config()
    env_parameters_config = default_env_parameters_config()
    descr = "A wrapper for CybORG."
    simulation_env_config = SimulationEnvConfig(
        name=name, version=version, descr=descr,
        players_config=players_config, state_space_config=state_space_config,
        joint_action_space_config=joint_action_space_config,
        joint_observation_space_config=joint_observation_space_config,
        transition_operator_config=transition_operator_config,
        observation_function_config=observation_function_config, reward_function_config=reward_function_config,
        initial_state_distribution_config=initial_state_distribution_config, simulation_env_input_config=input_config,
        time_step_type=TimeStepType.DISCRETE,
        gym_env_name="csle-cyborg-scenario-two-v1", env_parameters_config=env_parameters_config,
        plot_transition_probabilities=True, plot_observation_function=True, plot_reward_function=True
    )
    return simulation_env_config


def default_env_parameters_config() -> EnvParametersConfig:
    """
    :return: the default env parameters config
    """
    config = EnvParametersConfig(
        parameters=[
            EnvParameter(id=0, name="default", descr="default"),
        ]
    )
    return config


def default_players_config() -> PlayersConfig:
    """
    :return: the default players configuration of the simulation
    """
    player_configs = [
        PlayerConfig(name="defender", id=1, descr="The defender which tries to solve the challenge")
    ]
    players_config = PlayersConfig(player_configs=player_configs)
    return players_config


def default_state_space_config() -> StateSpaceConfig:
    """
    Gets the default state space configuration

    :return: the default state space configuration of the simulation
    """
    states = []
    for i in range(5):
        states.append(
            State(id=i, name=f"{i} nodes", descr=f"State {i}",
                  state_type=StateType.ACTIVE),
        )
    state_space_config = StateSpaceConfig(states=states)
    return state_space_config


def default_joint_action_space_config() -> JointActionSpaceConfig:
    """
    :return: the default joint action space of all players in the simulation
    """
    action_spaces = [
        ActionSpaceConfig(
            actions=[Action(id=0, descr="action 0"), Action(id=1, descr="Add 1 node")],
            player_id=1, action_type=ValueType.INTEGER
        ),
        ActionSpaceConfig(actions=[Action(id=0, descr="null")],
                          player_id=2, action_type=ValueType.INTEGER)
    ]
    joint_action_space_config = JointActionSpaceConfig(action_spaces=action_spaces)
    return joint_action_space_config


def default_joint_observation_space_config() -> JointObservationSpaceConfig:
    """
    Gets the default joint observation space configuration of the simulation

    :return: the default joint observation space configuration
    """
    observations = []
    observation_id_to_observation_id_vector = {}
    observation_id_to_observation_vector = {}
    for i in range(10):
        observations.append(Observation(id=i, val=i, descr=f"{i}"))
        observation_id_to_observation_id_vector[i] = [i]
        observation_id_to_observation_vector[i] = [i]
    component_observations = {}
    component_observations["data"] = observations
    observation_component_name_to_index = {"data": 0}
    observation_spaces = [
        ObservationSpaceConfig(
            observations=observations,
            observation_type=ValueType.INTEGER,
            player_id=1,
            descr="The observation space of the defender.",
            observation_id_to_observation_id_vector=observation_id_to_observation_id_vector,
            observation_component_name_to_index=observation_component_name_to_index,
            component_observations=component_observations,
            observation_id_to_observation_vector=observation_id_to_observation_vector
        )
    ]
    joint_observation_space_config = JointObservationSpaceConfig(observation_spaces=observation_spaces)
    return joint_observation_space_config


def default_reward_function_config() -> RewardFunctionConfig:
    """
    Gets the default reward function configuration

    :return: the default reward function configuration
    """
    expanded_cost_tensor = []
    for _ in [1]:
        l_tensor = []
        for _ in [0, 1]:
            a1_tensor = []
            for _ in [1]:
                a2_tensor = []
                for s in range(5):
                    a2_tensor.append(1)
                a1_tensor.append(a2_tensor)
            l_tensor.append(a1_tensor)
        expanded_cost_tensor.append(l_tensor)
    reward_function_config = RewardFunctionConfig(reward_tensor=expanded_cost_tensor)
    return reward_function_config


def default_transition_operator_config() -> TransitionOperatorConfig:
    """
    Gets the default transition tensor configuration

    :return: the default transition tensor configuration
    """
    expanded_transition_tensor = []
    for _ in [1]:
        l_tensor = []
        for _ in [0, 1]:
            a1_tensor = []
            for _ in [1]:
                a2_tensor = []
                for s in range(5):
                    s_tensor = []
                    for s_prime in range(5):
                        s_tensor.append(1 / 5)
                    a2_tensor.append(s_tensor)
                a1_tensor.append(a2_tensor)
            l_tensor.append(a1_tensor)
        expanded_transition_tensor.append(l_tensor)
    transition_operator_config = TransitionOperatorConfig(transition_tensor=expanded_transition_tensor)
    return transition_operator_config


def default_observation_function_config() -> ObservationFunctionConfig:
    """
    Gets the default observation tensor configuration

    :return: the default observation tensor configuration
    """
    expanded_observation_tensor = []
    for _ in [0, 1]:
        a1_tensor = []
        for _ in [1]:
            a2_tensor = []
            for s in range(5):
                s_tensor = []
                for o in range(10):
                    s_tensor.append(1 / 10)
                a2_tensor.append(s_tensor)
            a1_tensor.append(a2_tensor)
        expanded_observation_tensor.append(a1_tensor)
    component_observation_tensors = {}
    component_observation_tensors["data"] = expanded_observation_tensor
    observation_function_config = ObservationFunctionConfig(
        observation_tensor=expanded_observation_tensor, component_observation_tensors=component_observation_tensors)
    return observation_function_config


def default_initial_state_distribution_config() -> InitialStateDistributionConfig:
    """
    Gets the default initial state distribution configuration
    :param s_max: the maximum number of nodes
    :param initial_state: the initial number of nodes
    :return: the default initial state distribution configuration
    """
    initial_state_distribution = [0] * 5
    initial_state_distribution[0] = 1
    initial_state_distribution_config = InitialStateDistributionConfig(
        initial_state_distribution=initial_state_distribution)
    return initial_state_distribution_config


def default_input_config() -> SimulationEnvInputConfig:
    """
    Gets the input configuration to the openai gym environment

    :return: The default input configuration to the OpenAI gym environment
    """
    config = CSLECyborgConfig(gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, maximum_steps=100,
                              baseline_red_agents=[RedAgentType.B_LINE_AGENT], red_agent_distribution=[1.0],
                              reduced_action_space=False, scanned_state=False, decoy_state=False,
                              decoy_optimization=False, cache_visited_states=False)
    return config


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--install", help="Boolean parameter, if true, install config",
                        action="store_true")
    parser.add_argument("-u", "--uninstall", help="Boolean parameter, if true, uninstall config",
                        action="store_true")
    args = parser.parse_args()
    config = default_config(name="csle-cyborg-001", version="0.0.1")
    if args.install:
        SimulationEnvController.install_simulation(config=config)
        img_path = ExperimentUtil.default_simulation_picture_path()
        if os.path.exists(img_path):
            image_data = ExperimentUtil.read_env_picture(img_path)
            SimulationEnvController.save_simulation_image(img=image_data, simulation=config.name)
    if args.uninstall:
        SimulationEnvController.uninstall_simulation(config=config)
