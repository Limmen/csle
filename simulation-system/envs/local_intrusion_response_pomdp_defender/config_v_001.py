import argparse
import os
import numpy as np
from csle_common.controllers.simulation_env_controller import SimulationEnvController
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.dao.simulation_config.players_config import PlayersConfig
from csle_common.dao.simulation_config.player_config import PlayerConfig
from csle_common.dao.training.player_type import PlayerType
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
from csle_common.dao.training.random_policy import RandomPolicy
from gym_csle_intrusion_response_game.util.intrusion_response_game_util import IntrusionResponseGameUtil
from gym_csle_intrusion_response_game.dao.intrusion_response_game_config import IntrusionResponseGameConfig
from gym_csle_intrusion_response_game.dao.intrusion_response_game_local_pomdp_defender_config \
    import IntrusionResponseGameLocalPOMDPDefenderConfig


def default_config(name: str, number_of_zones: int,
                   X_max :int, lamb: float, beta: float, mu: float, reachable: bool,
                   initial_zone: int, version: str = "0.0.1") -> SimulationEnvConfig:
    """
    The default configuration of the simulation environment

    :param name: the name of the environment
    :param version: the version string
    :return:the default configuration
    """
    players_config = default_players_config()
    state_space_config = default_state_space_config(number_of_zones=number_of_zones)
    joint_action_space_config = default_joint_action_space_config(number_of_zones=number_of_zones)
    joint_observation_space_config = default_joint_observation_space_config(X_max=X_max)
    transition_operator_config = default_transition_operator_config(num_zones=number_of_zones)
    observation_function_config = default_observation_function_config(
        defender_obs_space=joint_observation_space_config.observation_spaces[0],
        number_of_zones=number_of_zones)
    reward_function_config = default_reward_function_config(
        number_of_zones=number_of_zones, lamb=lamb, beta=beta, mu=mu, reachable=reachable,
        initial_zone=initial_zone)
    initial_state_distribution_config = default_initial_state_distribution_config(initial_zone=initial_zone,
                                                                                  number_of_zones=number_of_zones)
    input_config = default_input_config(
        defender_observation_space_config=joint_observation_space_config.observation_spaces[0],
        reward_function_config=reward_function_config,
        transition_tensor_config=transition_operator_config,
        observation_function_config=observation_function_config,
        initial_state_distribution_config=initial_state_distribution_config,
        attacker_action_space_config=joint_action_space_config.action_spaces[1], number_of_zones=number_of_zones)
    env_parameters_config = default_env_parameters_config()
    descr = "TODO"
    simulation_env_config = SimulationEnvConfig(
        name=name, version=version, descr=descr,
        players_config=players_config, state_space_config=state_space_config,
        joint_action_space_config=joint_action_space_config,
        joint_observation_space_config=joint_observation_space_config,
        transition_operator_config=transition_operator_config,
        observation_function_config=observation_function_config, reward_function_config=reward_function_config,
        initial_state_distribution_config=initial_state_distribution_config, simulation_env_input_config=input_config,
        time_step_type=TimeStepType.DISCRETE,
        gym_env_name="csle-intrusion-response-game-pomdp-defender-v1", env_parameters_config=env_parameters_config,
        plot_transition_probabilities=True, plot_observation_function=True, plot_reward_function=True
    )
    return simulation_env_config


def default_env_parameters_config() -> EnvParametersConfig:
    """
    :return: the default env parameters config
    """
    config = EnvParametersConfig(parameters=[])
    return config


def default_players_config() -> PlayersConfig:
    """
    :return: the default players configuration of the simulation
    """
    player_configs = [
        PlayerConfig(name="defender", id=1, descr="The defender which tries to detect, prevent, "
                                                  "and interrupt intrusions for the infrastructure")
    ]
    players_config = PlayersConfig(player_configs=player_configs)
    return players_config


def default_state_space_config(number_of_zones: int) -> StateSpaceConfig:
    """
    Gets the default  state space configuration

    :param number_of_zones: the number of zones in the network
    :return: the default state space configuration of the simulation
    """
    states = []
    state_id = 0
    for i in range(number_of_zones):
        states.append(State(
            id=state_id, name=f"{i}_{0}", descr=f"Zone: {i}, no intrusion", state_type=StateType.ACTIVE
        ))
        states.append(State(
            id=state_id, name=f"{i}_{1}", descr=f"Zone: {i}, recon", state_type=StateType.ACTIVE
        ))
        states.append(State(
            id=state_id, name=f"{i}_{2}", descr=f"Zone: {2}, compromised", state_type=StateType.ACTIVE
        ))
    state_space_config = StateSpaceConfig(states=states)
    return state_space_config


def default_joint_action_space_config(number_of_zones: int) -> JointActionSpaceConfig:
    """
    Gets the default action space configuration

    :param number_of_zones: the number of zones in the network
    :return: the default joint action space of all players in the simulation
    """
    defender_actions = []
    defender_actions.append(Action(
        id=0, descr=f"Wait"
    ))
    for i in range(1, number_of_zones+1):
        defender_actions.append(Action(
            id=i, descr=f"Move node to  zone: {i}"
        ))
    attacker_actions = [
        Action(id=0, descr=f"Wait"),
        Action(id=1, descr=f"Recon"),
        Action(id=2, descr=f"Brute-force"),
        Action(id=3, descr=f"Exploit")
    ]
    action_spaces = [ActionSpaceConfig(actions=defender_actions, player_id=1, action_type=ValueType.INTEGER),
                     ActionSpaceConfig(actions=attacker_actions, player_id=2, action_type=ValueType.INTEGER)]
    joint_action_space_config = JointActionSpaceConfig(action_spaces=action_spaces)
    return joint_action_space_config


def default_joint_observation_space_config(X_max: int) -> JointObservationSpaceConfig:
    """
    Gets the default joint observation space configuration of the simulation

    :param X_max: the maximum number of alerts
    :return: the default joint observation space configuration
    """
    obs = IntrusionResponseGameUtil.local_observation_space(X_max=X_max)
    observations = []
    for i in range(len(obs)):
        observations.append(
            Observation(id=i, val=i, descr=f"{i} weighted alerts")
        )
    observation_spaces = [
        ObservationSpaceConfig(
            observations=observations,
            observation_type=ValueType.INTEGER,
            player_id=1,
            descr="The observation space of the defender. The defender observes the weighted sum of alerts",
            observation_id_to_observation_id_vector={},
            observation_component_name_to_index={},
            component_observations={},
            observation_id_to_observation_vector={}
        )
    ]
    joint_observation_space_config = JointObservationSpaceConfig(observation_spaces=observation_spaces)
    return joint_observation_space_config


def default_reward_function_config(lamb: float, mu: float, reachable: bool, initial_zone: int, beta: float,
                                   number_of_zones: int) -> RewardFunctionConfig:
    """
    :return: the default reward function configuration
    """
    state_space = IntrusionResponseGameUtil.local_state_space(number_of_zones=number_of_zones)
    defender_actions = IntrusionResponseGameUtil.local_defender_actions(number_of_zones=number_of_zones)
    attacker_actions = IntrusionResponseGameUtil.local_attacker_actions()
    defender_action_costs = IntrusionResponseGameUtil.costant_defender_action_costs(defender_actions=defender_actions)
    zones = IntrusionResponseGameUtil.zones(num_zones=number_of_zones)
    zone_utilities = IntrusionResponseGameUtil.constant_zone_utilities(zones=zones)
    reward_function_config = RewardFunctionConfig(
        reward_tensor=list(IntrusionResponseGameUtil.local_reward_tensor(
            lamb=lamb, mu=mu, reachable=reachable, initial_zone=initial_zone, beta=beta,
            S=state_space, A1=defender_actions, A2=attacker_actions,
            D_C=defender_action_costs, Z_U=zone_utilities
        )))
    return reward_function_config


def default_transition_operator_config(num_zones: int) -> TransitionOperatorConfig:
    """
    :return: the default transition tensor configuration
    """
    zones = IntrusionResponseGameUtil.zones(num_zones=num_zones)
    zone_detection_probabilities = IntrusionResponseGameUtil.uniform_zone_detection_probabilities(zones=zones)
    attack_success_probabilities = IntrusionResponseGameUtil.local_attack_success_probabilities_uniform()
    state_space = IntrusionResponseGameUtil.local_state_space(number_of_zones=num_zones)
    defender_actions = IntrusionResponseGameUtil.local_defender_actions(number_of_zones=num_zones)
    attacker_actions = IntrusionResponseGameUtil.local_attacker_actions()
    transition_operator_config = TransitionOperatorConfig(
        transition_tensor=list(IntrusionResponseGameUtil.local_transition_tensor(
            Z_D=zone_detection_probabilities,
            A_P=attack_success_probabilities,
            S=state_space, A1=defender_actions,
            A2=attacker_actions
        )))
    return transition_operator_config


def default_observation_function_config(
        defender_obs_space: ObservationSpaceConfig,
        number_of_zones: int) -> ObservationFunctionConfig:
    state_space = IntrusionResponseGameUtil.local_state_space(number_of_zones=number_of_zones)
    defender_actions = IntrusionResponseGameUtil.local_defender_actions(number_of_zones=number_of_zones)
    attacker_actions = IntrusionResponseGameUtil.local_attacker_actions()
    observation_space = IntrusionResponseGameUtil.local_observation_space(X_max=len(defender_obs_space.observations))
    observation_tensor = IntrusionResponseGameUtil.local_observation_tensor_betabinom(
        X_max=len(defender_obs_space.observations), S=state_space, A1=defender_actions,
        A2=attacker_actions, O=observation_space
    )
    observation_function_config = ObservationFunctionConfig(observation_tensor=observation_tensor,
                                                            component_observation_tensors={})
    return observation_function_config


def default_initial_state_distribution_config(initial_zone: int, number_of_zones: int) -> InitialStateDistributionConfig:
    """
    :return: the default initial state distribution configuration
    """
    state_space = IntrusionResponseGameUtil.local_state_space(number_of_zones=number_of_zones)
    initial_state_distribution_config = InitialStateDistributionConfig(
        initial_state_distribution=list(IntrusionResponseGameUtil.local_initial_defender_belief(
            S=state_space, initial_zone=initial_zone
        ))
    )
    return initial_state_distribution_config


def default_input_config(defender_observation_space_config: ObservationSpaceConfig,
                         reward_function_config: RewardFunctionConfig,
                         transition_tensor_config: TransitionOperatorConfig,
                         observation_function_config: ObservationFunctionConfig,
                         initial_state_distribution_config: InitialStateDistributionConfig,
                         attacker_action_space_config: ActionSpaceConfig, number_of_zones: int) -> SimulationEnvInputConfig:
    """
    Gets the input configuration to the openai gym environment

    :param defender_observation_space_config: the configuration of the defender's observation space
    :param reward_function_config: the reward function configuration
    :param transition_tensor_config: the transition tensor configuration
    :param observation_function_config: the observation function configuration
    :param initial_state_distribution_config: the initial state distribution configuration
    :param attacker_action_space_config: the attacker's action space config
    :return: The default input configuration to the OpenAI gym environment
    """

    attacker_stage_strategy = np.zeros((3, 2))
    attacker_stage_strategy[0][0] = 0.9
    attacker_stage_strategy[0][1] = 0.1
    attacker_stage_strategy[1][0] = 0.9
    attacker_stage_strategy[1][1] = 0.1
    attacker_stage_strategy[2] = attacker_stage_strategy[1]

    game_config = IntrusionResponseGameConfig(
        A1=IntrusionResponseGameUtil.local_attacker_actions(),
        A2=IntrusionResponseGameUtil.local_defender_actions(number_of_zones=number_of_zones),
        d_b1=np.array(initial_state_distribution_config.initial_state_distribution),
        a_b1=np.array(initial_state_distribution_config.initial_state_distribution),
        T=np.array(transition_tensor_config.transition_tensor),
        O=np.array(list(map(lambda x: x.val, defender_observation_space_config.observations))),
        Z=np.array(observation_function_config.observation_tensor),
        R=np.array(reward_function_config.reward_tensor),
        S=IntrusionResponseGameUtil.local_state_space(number_of_zones=number_of_zones),
        env_name="csle-stopping-game-pomdp-defender-v1",
        gamma=1)
    config = IntrusionResponseGameLocalPOMDPDefenderConfig(
        intrusion_response_game_config=game_config,
        attacker_strategy=RandomPolicy(actions=attacker_action_space_config.actions,
                                       player_type=PlayerType.ATTACKER,
                                       stage_policy_tensor=list(attacker_stage_strategy)),
        env_name="csle-stopping-game-pomdp-defender-v1")
    return config


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--install", help="Boolean parameter, if true, install config",
                        action="store_true")
    parser.add_argument("-u", "--uninstall", help="Boolean parameter, if true, uninstall config",
                        action="store_true")
    args = parser.parse_args()
    config = default_config(name="csle-intrusion-response-game-pomdp-defender-001", version="0.0.1",
                            number_of_zones=5, X_max=10, lamb=1, beta=1, mu=1, reachable=True, initial_zone=3)
    if args.install:
        SimulationEnvController.install_simulation(config=config)
        img_path = ExperimentUtil.default_simulation_picture_path()
        if os.path.exists(img_path):
            image_data = ExperimentUtil.read_env_picture(img_path)
            SimulationEnvController.save_simulation_image(img=image_data, simulation=config.name)
    if args.uninstall:
        SimulationEnvController.uninstall_simulation(config=config)
