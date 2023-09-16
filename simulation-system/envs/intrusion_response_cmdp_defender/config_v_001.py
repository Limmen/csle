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
from csle_tolerance.util.intrusion_response_cmdp_util import IntrusionResponseCmdpUtil
from csle_tolerance.dao.intrusion_response_cmdp_config import IntrusionResponseCmdpConfig


def default_config(name: str, p_a: float, p_c: float, p_u: float, s_max: int, negate_costs: bool, seed: int,
                   initial_state: int, f: int, epsilon_a: float,
                   discount_factor: float, version: str = "0.0.1") -> SimulationEnvConfig:
    """
    The default configuration of the simulation environment

    :param name: the name of the simulation environment
    :param p_a: the intrusion probability
    :param p_c: the crash probability
    :param p_u: the software upgrade probability
    :param s_max: the maximum number of nodes
    :param negate_costs: boolean flag indiciating whether the costs should be negated or not
    :param seed: the random seed
    :param initial_state: the initial state
    :param f: the tolerance threshold
    :param epsilon_a: the availability threshold
    :param discount_factor: the discount factor
    :param version: the version of the environment
    :return: The default configuration of the simulation environment
    """
    players_config = default_players_config()
    state_space_config = default_state_space_config(s_max=s_max)
    joint_action_space_config = default_joint_action_space_config()
    joint_observation_space_config = default_joint_observation_space_config(s_max=s_max)
    transition_operator_config = default_transition_operator_config(s_max=s_max, p_a=p_a, p_c=p_c, p_u=p_u)
    observation_function_config = default_observation_function_config(s_max=s_max, p_a=p_a, p_c=p_c, p_u=p_u)
    reward_function_config = default_reward_function_config(s_max=s_max, negate_costs=negate_costs)
    initial_state_distribution_config = default_initial_state_distribution_config(s_max=s_max,
                                                                                  initial_state=initial_state)
    input_config = default_input_config(
        p_a=p_a, p_c=p_c, s_max=s_max, negate_costs=negate_costs, seed=seed, initial_state=initial_state, f=f,
        epsilon_a=epsilon_a, simulation_env_name=name, discount_factor=discount_factor, p_u=p_u)
    env_parameters_config = default_env_parameters_config()
    descr = "A CMDP for intrusion response."
    simulation_env_config = SimulationEnvConfig(
        name=name, version=version, descr=descr,
        players_config=players_config, state_space_config=state_space_config,
        joint_action_space_config=joint_action_space_config,
        joint_observation_space_config=joint_observation_space_config,
        transition_operator_config=transition_operator_config,
        observation_function_config=observation_function_config, reward_function_config=reward_function_config,
        initial_state_distribution_config=initial_state_distribution_config, simulation_env_input_config=input_config,
        time_step_type=TimeStepType.DISCRETE,
        gym_env_name="csle-tolerance-intrusion-response-cmdp-v1", env_parameters_config=env_parameters_config,
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
        PlayerConfig(name="defender", id=1, descr="The defender which tries to minimize nodes "
                                                  "and meet availability constraints")
    ]
    players_config = PlayersConfig(player_configs=player_configs)
    return players_config


def default_state_space_config(s_max: int) -> StateSpaceConfig:
    """
    Gets the default state space configuration

    :param s_max: the maximum number of nodes
    :return: the default state space configuration of the simulation
    """
    states = []
    for i in range(s_max + 1):
        states.append(
            State(id=i, name=f"{i} nodes", descr=f"State where the replicated system has {i} nodes",
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
            actions=[Action(id=0, descr="Add 0 nodes"), Action(id=1, descr="Add 1 node")],
            player_id=1, action_type=ValueType.INTEGER
        ),
        ActionSpaceConfig(actions=[Action(id=0, descr="null")],
                          player_id=2, action_type=ValueType.INTEGER)
    ]
    joint_action_space_config = JointActionSpaceConfig(action_spaces=action_spaces)
    return joint_action_space_config


def default_joint_observation_space_config(s_max: int) -> JointObservationSpaceConfig:
    """
    Gets the default joint observation space configuration of the simulation

    :param s_max: the maximum number of nodes
    :return: the default joint observation space configuration
    """
    obs = IntrusionResponseCmdpUtil.state_space(s_max=s_max)
    observations = []
    observation_id_to_observation_id_vector = {}
    observation_id_to_observation_vector = {}
    for i in range(len(obs)):
        observations.append(Observation(id=i, val=i, descr=f"{i} nodes"))
        observation_id_to_observation_id_vector[i] = [i]
        observation_id_to_observation_vector[i] = [i]
    component_observations = {}
    component_observations["nodes"] = observations
    observation_component_name_to_index = {"nodes": 0}
    observation_spaces = [
        ObservationSpaceConfig(
            observations=observations,
            observation_type=ValueType.INTEGER,
            player_id=1,
            descr="The observation space of the defender. The defender observes the number of nodes",
            observation_id_to_observation_id_vector=observation_id_to_observation_id_vector,
            observation_component_name_to_index=observation_component_name_to_index,
            component_observations=component_observations,
            observation_id_to_observation_vector=observation_id_to_observation_vector
        )
    ]
    joint_observation_space_config = JointObservationSpaceConfig(observation_spaces=observation_spaces)
    return joint_observation_space_config


def default_reward_function_config(s_max: int, negate_costs: bool) -> RewardFunctionConfig:
    """
    Gets the default reward function configuration

    :param s_max: the maximum number of nodes
    :param negate_costs: boolean flag indicating whether costs should be negated or not
    :return: the default reward function configuration
    """
    cost_tensor = IntrusionResponseCmdpUtil.cost_tensor(states=IntrusionResponseCmdpUtil.state_space(s_max=s_max),
                                                        negate=negate_costs)
    expanded_cost_tensor = []
    for _ in [1]:
        l_tensor = []
        for _ in IntrusionResponseCmdpUtil.action_space():
            a1_tensor = []
            for _ in [1]:
                a2_tensor = []
                for s in IntrusionResponseCmdpUtil.state_space(s_max=s_max):
                    a2_tensor.append(cost_tensor[s])
                a1_tensor.append(a2_tensor)
            l_tensor.append(a1_tensor)
        expanded_cost_tensor.append(l_tensor)
    reward_function_config = RewardFunctionConfig(reward_tensor=expanded_cost_tensor)
    return reward_function_config


def default_transition_operator_config(s_max: int, p_a: float, p_c: float, p_u: float) -> TransitionOperatorConfig:
    """
    Gets the default transition tensor configuration

    :param s_max: the maximum number of nodes
    :param p_a: the intrusion probability
    :param p_c: the crash probability
    :param p_u: the software upgrade probability
    :return: the default transition tensor configuration
    """
    transition_tensor = IntrusionResponseCmdpUtil.transition_tensor(
        states=IntrusionResponseCmdpUtil.state_space(s_max=s_max), actions=IntrusionResponseCmdpUtil.action_space(),
        p_a=p_a, p_c=p_c, p_u=p_u, s_max=s_max)
    expanded_transition_tensor = []
    for _ in [1]:
        l_tensor = []
        for a1 in IntrusionResponseCmdpUtil.action_space():
            a1_tensor = []
            for _ in [1]:
                a2_tensor = []
                for s in IntrusionResponseCmdpUtil.state_space(s_max=s_max):
                    s_tensor = []
                    for s_prime in IntrusionResponseCmdpUtil.state_space(s_max=s_max):
                        s_tensor.append(transition_tensor[a1][s][s_prime])
                    a2_tensor.append(s_tensor)
                a1_tensor.append(a2_tensor)
            l_tensor.append(a1_tensor)
        expanded_transition_tensor.append(l_tensor)
    transition_operator_config = TransitionOperatorConfig(transition_tensor=expanded_transition_tensor)
    return transition_operator_config


def default_observation_function_config(s_max: int, p_a: float, p_c: float, p_u: float) -> ObservationFunctionConfig:
    """
    Gets the default observation tensor configuration

    :param s_max: the maximum number of nodes
    :param p_a: the intrusion probability
    :param p_c: the crash probability
    :param p_u: the software upgrade probability
    :return: the default observation tensor configuration
    """
    observation_tensor = IntrusionResponseCmdpUtil.transition_tensor(
        states=IntrusionResponseCmdpUtil.state_space(s_max=s_max), actions=IntrusionResponseCmdpUtil.action_space(),
        p_a=p_a, p_c=p_c, p_u=p_u, s_max=s_max)
    expanded_observation_tensor = []
    for a1 in IntrusionResponseCmdpUtil.action_space():
        a1_tensor = []
        for _ in [1]:
            a2_tensor = []
            for s in IntrusionResponseCmdpUtil.state_space(s_max=s_max):
                s_tensor = []
                for s_prime in IntrusionResponseCmdpUtil.state_space(s_max=s_max):
                    s_tensor.append(observation_tensor[a1][s][s_prime])
                a2_tensor.append(s_tensor)
            a1_tensor.append(a2_tensor)
        expanded_observation_tensor.append(a1_tensor)
    component_observation_tensors = {}
    component_observation_tensors["number of nodes"] = expanded_observation_tensor
    observation_function_config = ObservationFunctionConfig(
        observation_tensor=expanded_observation_tensor, component_observation_tensors=component_observation_tensors)
    return observation_function_config


def default_initial_state_distribution_config(s_max: int, initial_state: int) -> InitialStateDistributionConfig:
    """
    Gets the default initial state distribution configuration
    :param s_max: the maximum number of nodes
    :param initial_state: the initial number of nodes
    :return: the default initial state distribution configuration
    """
    initial_state_distribution = [0] * (s_max + 1)
    initial_state_distribution[initial_state] = 1
    initial_state_distribution_config = InitialStateDistributionConfig(
        initial_state_distribution=initial_state_distribution)
    return initial_state_distribution_config


def default_input_config(p_a: float, p_c: float, p_u: float, s_max: int, negate_costs: bool, seed: int,
                         initial_state: int, f: int, epsilon_a: float, simulation_env_name: str,
                         discount_factor: float) -> SimulationEnvInputConfig:
    """
    Gets the input configuration to the openai gym environment

    :param p_a: the intrusion probability
    :param p_c: the crash probability
    :param p_u: the software upgrade probability
    :param s_max: the maximum number of nodes
    :param negate_costs: boolean flag indicating whether the costs should be negated or not
    :param seed: the random seed
    :param initial_state: the initial number of nodes
    :param f: the tolerance threshold
    :param epsilon_a: the availability threshold
    :param simulation_env_name: the simulation environment name
    :param discount_factor: the discount factor
    :return: The default input configuration to the OpenAI gym environment
    """
    transition_tensor = IntrusionResponseCmdpUtil.transition_tensor(
        states=IntrusionResponseCmdpUtil.state_space(s_max=s_max),
        actions=IntrusionResponseCmdpUtil.action_space(), p_a=p_a, p_c=p_c, p_u=p_u, s_max=s_max)
    cost_tensor = IntrusionResponseCmdpUtil.cost_tensor(
        states=IntrusionResponseCmdpUtil.state_space(s_max=s_max), negate=negate_costs)
    constraint_cost_tensor = IntrusionResponseCmdpUtil.constraint_cost_tensor(
        states=IntrusionResponseCmdpUtil.state_space(s_max=s_max), f=f)
    config = IntrusionResponseCmdpConfig(
        p_a=p_a, p_c=p_c, p_u=p_u, s_max=s_max, transition_tensor=transition_tensor, cost_tensor=cost_tensor,
        negate_costs=negate_costs, seed=seed, states=IntrusionResponseCmdpUtil.state_space(s_max=s_max),
        actions=IntrusionResponseCmdpUtil.action_space(), initial_state=initial_state,
        constraint_cost_tensor=constraint_cost_tensor, f=f, epsilon_a=epsilon_a,
        simulation_env_name=simulation_env_name,
        gym_env_name="csle-tolerance-intrusion-response-cmdp-v1", discount_factor=discount_factor
    )
    return config


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--install", help="Boolean parameter, if true, install config",
                        action="store_true")
    parser.add_argument("-u", "--uninstall", help="Boolean parameter, if true, uninstall config",
                        action="store_true")
    args = parser.parse_args()
    config = default_config(
        name="csle-tolerance-intrusion-response-cmdp-defender-001", version="0.0.1",
        p_u=0.4, p_a=0.4, p_c=0.01, s_max=20,
        initial_state=10, seed=999, discount_factor=1, negate_costs=False, f=3, epsilon_a=0.2)
    if args.install:
        SimulationEnvController.install_simulation(config=config)
        img_path = ExperimentUtil.default_simulation_picture_path()
        if os.path.exists(img_path):
            image_data = ExperimentUtil.read_env_picture(img_path)
            SimulationEnvController.save_simulation_image(img=image_data, simulation=config.name)
    if args.uninstall:
        SimulationEnvController.uninstall_simulation(config=config)
