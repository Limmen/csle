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
from csle_common.dao.training.tabular_policy import TabularPolicy
from csle_common.dao.training.agent_type import AgentType
import gym_csle_intrusion_response_game.constants.constants as env_constants
from gym_csle_intrusion_response_game.util.intrusion_response_game_util import IntrusionResponseGameUtil
from gym_csle_intrusion_response_game.dao.workflow_intrusion_response_pomdp_defender_config \
    import WorkflowIntrusionResponsePOMDPDefenderConfig
from gym_csle_intrusion_response_game.dao.workflow_intrusion_response_game_config \
    import WorkflowIntrusionResponseGameConfig


def default_config(name: str, number_of_zones: int, X_max: int, beta: float, reachable: bool,
                   initial_zone: int, attack_success_probability: float, eta: float, defender_action_cost: float,
                   zone_utility: float, detection_probability: float, adjacency_matrix: np.ndarray,
                   num_nodes: int, gamma: float, gw_reachable: np.ndarray,
                   version: str = "0.0.1") -> SimulationEnvConfig:
    """
    The default configuration of the simulation environment

    :param name: the name of the environment
    :param number_of_zones: the number of zones in the network
    :param X_max: the maximum observation
    :param beta: the workflow scaling parameter
    :param reachable: whether the node is reachable or not
    :param initial_zone: the initial zone of the node
    :param attack_success_probability: the attack success probability
    :param eta: the reward scaling parameter
    :param defender_action_cost: the costs of the defender actions
    :param zone_utility: the zone utilities
    :param detection_probability: the detection probability
    :param version: the version string
    :param gamma: the discount factor
    :param adjacency_matrix: the adjacency matrix of the workflow DAG
    :param num_nodes: the number of nodes in the workflow
    :return: the default configuration
    """
    players_config = default_players_config()
    state_space_config = default_state_space_config(number_of_zones=number_of_zones)
    joint_action_space_config = default_joint_action_space_config(number_of_zones=number_of_zones)
    joint_observation_space_config = default_joint_observation_space_config(X_max=X_max)
    transition_operator_config = default_transition_operator_config(
        num_zones=number_of_zones, attack_success_probability=attack_success_probability,
        detection_probability=detection_probability)
    observation_function_config = default_observation_function_config(
        defender_obs_space=joint_observation_space_config.observation_spaces[0],
        number_of_zones=number_of_zones)
    reward_function_config = default_reward_function_config(
        number_of_zones=number_of_zones, eta=eta, beta=beta, reachable=reachable, initial_zone=initial_zone,
        defender_action_cost=defender_action_cost, zone_utility=zone_utility)
    initial_state_distribution_config = default_initial_state_distribution_config(initial_zone=initial_zone,
                                                                                  number_of_zones=number_of_zones)
    input_config = default_input_config(
        local_attacker_action_space_config=joint_action_space_config.action_spaces[1], number_of_zones=number_of_zones,
        attack_success_probability=attack_success_probability, beta=beta, eta=eta,
        defender_action_cost=defender_action_cost, zone_utility=zone_utility,
        detection_probability=detection_probability, num_nodes=num_nodes, adjacency_matrix=adjacency_matrix,
        gamma=gamma, X_max=X_max, gw_reachable=gw_reachable)
    env_parameters_config = default_env_parameters_config()
    descr = "A workflow intrusion response game"
    simulation_env_config = SimulationEnvConfig(
        name=name, version=version, descr=descr,
        players_config=players_config, state_space_config=state_space_config,
        joint_action_space_config=joint_action_space_config,
        joint_observation_space_config=joint_observation_space_config,
        transition_operator_config=transition_operator_config,
        observation_function_config=observation_function_config, reward_function_config=reward_function_config,
        initial_state_distribution_config=initial_state_distribution_config, simulation_env_input_config=input_config,
        time_step_type=TimeStepType.DISCRETE,
        gym_env_name="csle-intrusion-response-game-workflow-pomdp-defender-v1",
        env_parameters_config=env_parameters_config,
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
    states.append(State(
        id=0, name="terminal", descr="Terminal state", state_type=StateType.TERMINAL
    ))
    state_id = 1
    for i in range(number_of_zones):
        states.append(State(
            id=state_id, name=f"{i}_{0}", descr=f"Zone: {i}, no intrusion", state_type=StateType.ACTIVE
        ))
        state_id += 1
        states.append(State(
            id=state_id, name=f"{i}_{1}", descr=f"Zone: {i}, recon", state_type=StateType.ACTIVE
        ))
        state_id += 1
        states.append(State(
            id=state_id, name=f"{i}_{2}", descr=f"Zone: {2}, compromised", state_type=StateType.ACTIVE
        ))
        state_id += 1
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
        id=0, descr="Wait"
    ))
    for i in range(1, number_of_zones + 1):
        defender_actions.append(Action(
            id=i, descr=f"Move node to  zone: {i}"
        ))
    attacker_actions = [
        Action(id=0, descr="Wait"),
        Action(id=1, descr="Recon"),
        Action(id=2, descr="Brute-force"),
        Action(id=3, descr="Exploit")
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
    observation_id_to_observation_id_vector = {}
    observation_id_to_observation_vector = {}
    for i in range(len(obs)):
        observations.append(
            Observation(id=i, val=i, descr=f"{i} weighted alerts")
        )
        observation_id_to_observation_id_vector[i] = [i]
        observation_id_to_observation_vector[i] = [i]
    component_observations = {}
    component_observations["weighted_alerts"] = observations
    observation_component_name_to_index = {"weighted_alerts": 0}
    observation_spaces = [
        ObservationSpaceConfig(
            observations=observations,
            observation_type=ValueType.INTEGER,
            player_id=1,
            descr="The observation space of the defender. The defender observes the weighted sum of alerts",
            observation_id_to_observation_id_vector=observation_id_to_observation_id_vector,
            observation_component_name_to_index=observation_component_name_to_index,
            component_observations=component_observations,
            observation_id_to_observation_vector=observation_id_to_observation_vector
        )
    ]
    joint_observation_space_config = JointObservationSpaceConfig(observation_spaces=observation_spaces)
    return joint_observation_space_config


def default_reward_function_config(reachable: bool, initial_zone: int, beta: float,
                                   number_of_zones: int, defender_action_cost: float, zone_utility: float,
                                   eta: float) -> RewardFunctionConfig:
    """
    :return: the default reward function configuration
    """
    state_space = IntrusionResponseGameUtil.local_state_space(number_of_zones=number_of_zones)
    A1 = IntrusionResponseGameUtil.local_defender_actions(number_of_zones=number_of_zones)
    A2 = IntrusionResponseGameUtil.local_attacker_actions()
    defender_action_costs = IntrusionResponseGameUtil.constant_defender_action_costs(
        A1=A1, constant_cost=defender_action_cost)
    zones = IntrusionResponseGameUtil.zones(num_zones=number_of_zones)
    zone_utilities = IntrusionResponseGameUtil.constant_zone_utilities(zones=zones, constant_utility=zone_utility)
    reward_function_config = RewardFunctionConfig(
        reward_tensor=[list(IntrusionResponseGameUtil.local_reward_tensor(
            eta=eta, reachable=reachable, initial_zone=initial_zone, beta=beta,
            S=state_space, A1=A1, A2=A2,
            C_D=defender_action_costs, Z_U=zone_utilities
        ))])
    return reward_function_config


def default_transition_operator_config(num_zones: int, attack_success_probability: float,
                                       detection_probability: float) -> TransitionOperatorConfig:
    """
    :param num_zones: the number of zones
    :param attack_success_probability: the attack success probability
    :param detection_probability the detection probability
    :return: the default transition tensor configuration
    """
    zones = IntrusionResponseGameUtil.zones(num_zones=num_zones)
    zone_detection_probabilities = IntrusionResponseGameUtil.constant_zone_detection_probabilities(
        zones=zones, constant_detection_prob=detection_probability)
    A2 = IntrusionResponseGameUtil.local_attacker_actions()
    attack_success_probabilities = IntrusionResponseGameUtil.local_attack_success_probabilities_uniform(
        A2=A2, p=attack_success_probability)
    state_space = IntrusionResponseGameUtil.local_state_space(number_of_zones=num_zones)
    defender_actions = IntrusionResponseGameUtil.local_defender_actions(number_of_zones=num_zones)
    attacker_actions = IntrusionResponseGameUtil.local_attacker_actions()
    transition_operator_config = TransitionOperatorConfig(
        transition_tensor=list([IntrusionResponseGameUtil.local_transition_tensor(
            Z_D=zone_detection_probabilities,
            A_P=attack_success_probabilities,
            S=state_space, A1=defender_actions,
            A2=attacker_actions
        )]))
    return transition_operator_config


def default_observation_function_config(defender_obs_space: ObservationSpaceConfig, number_of_zones: int) \
        -> ObservationFunctionConfig:
    """
    The default observation function config of the POMDP

    :param defender_obs_space: the defender's observation space
    :param number_of_zones: the number of zones
    :return: the default observation function config
    """
    state_space = IntrusionResponseGameUtil.local_state_space(number_of_zones=number_of_zones)
    A1 = IntrusionResponseGameUtil.local_defender_actions(number_of_zones=number_of_zones)
    A2 = IntrusionResponseGameUtil.local_attacker_actions()
    O = IntrusionResponseGameUtil.local_observation_space(X_max=len(defender_obs_space.observations))
    Z = IntrusionResponseGameUtil.local_observation_tensor_betabinom(
        S=state_space, A1=A1, A2=A2, O=O)
    component_observation_tensors = {}
    component_observation_tensors["weighted_alerts"] = Z
    observation_function_config = ObservationFunctionConfig(observation_tensor=Z,
                                                            component_observation_tensors=component_observation_tensors)
    return observation_function_config


def default_initial_state_distribution_config(initial_zone: int, number_of_zones: int) \
        -> InitialStateDistributionConfig:
    """
    Gets the default initial state distribution configuration

    :param initial_zone: the initial zone of the node in the local game
    :param number_of_zones: the number of zones
    :return: the default initial state distribution configuration
    """
    S = IntrusionResponseGameUtil.local_state_space(number_of_zones=number_of_zones)
    initial_state_distribution_config = InitialStateDistributionConfig(
        initial_state_distribution=list(IntrusionResponseGameUtil.local_initial_state_distribution(
            S=S, initial_state_idx=IntrusionResponseGameUtil.local_initial_state_idx(
                initial_zone=initial_zone, S=S)
        ))
    )
    return initial_state_distribution_config


def default_input_config(local_attacker_action_space_config: ActionSpaceConfig,
                         number_of_zones: int, attack_success_probability: float,
                         beta: float, eta: float,
                         defender_action_cost: float, zone_utility: float, detection_probability: float,
                         num_nodes: int, adjacency_matrix: np.ndarray, X_max: int,
                         gamma: float, gw_reachable: np.ndarray) -> SimulationEnvInputConfig:
    """
    Gets the input configuration to the openai gym environment

    :param local_attacker_action_space_config: the local action space config
    :param number_of_zones: the number of zones
    :param attack_success_probability: the attack success probabilities
    :param beta: the beta scaling prameter for the utility function
    :param eta: the eta scaling parameter for the utility function
    :param defender_action_cost: the cost of the defender actions
    :param zone_utility: the utilitites of the various zones
    :param detection_probability: the detection probabilities in the various zones
    :param num_nodes: the number of nodes
    :param adjacency_matrix: the adjacency matrix
    :param X_max: the maximum number of observations
    :param gamma: the discount factor
    :param gw_reachable: list of nodes reachable from the public gw
    :return: the default inptut configuration of the environment
    """
    local_A2 = IntrusionResponseGameUtil.local_attacker_actions()
    local_A1 = IntrusionResponseGameUtil.local_defender_actions(number_of_zones=number_of_zones)
    zones = IntrusionResponseGameUtil.zones(num_zones=number_of_zones)
    local_attacker_stage_strategy = np.zeros((len(IntrusionResponseGameUtil.local_attacker_state_space()),
                                              len(local_A2)))
    for i, s_a in enumerate(IntrusionResponseGameUtil.local_attacker_state_space()):
        if s_a == env_constants.ATTACK_STATES.HEALTHY:
            local_attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.WAIT] = 0.8
            local_attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.RECON] = 0.2
        elif s_a == env_constants.ATTACK_STATES.RECON:
            local_attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.WAIT] = 0.7
            local_attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.BRUTE_FORCE] = 0.15
            local_attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.EXPLOIT] = 0.15
        else:
            local_attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.WAIT] = 1
            local_attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.BRUTE_FORCE] = 0.
            local_attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.EXPLOIT] = 0
    attacker_strategy = TabularPolicy(
        player_type=PlayerType.ATTACKER,
        actions=local_attacker_action_space_config.actions,
        simulation_name="csle-intrusion-response-game-workflow-pomdp-defender-001",
        value_function=None, q_table=None,
        lookup_table=list(local_attacker_stage_strategy.tolist()),
        agent_type=AgentType.RANDOM, avg_R=-1)
    Z_D_P = IntrusionResponseGameUtil.constant_zone_detection_probabilities(
        zones=zones, constant_detection_prob=detection_probability)
    C_D = IntrusionResponseGameUtil.constant_defender_action_costs(A1=local_A1, constant_cost=defender_action_cost)
    Z_U = IntrusionResponseGameUtil.constant_zone_utilities(zones=zones, constant_utility=zone_utility)
    A_P = IntrusionResponseGameUtil.local_attack_success_probabilities_uniform(
        p=attack_success_probability, A2=local_A2)
    nodes = np.array(list(range(num_nodes)))
    initial_zones = []
    attacker_strategies = []
    for node in nodes:
        initial_zones.append(np.random.choice(zones))
        attacker_strategies.append(attacker_strategy)
    initial_zones = np.array(initial_zones)
    game_config = WorkflowIntrusionResponseGameConfig(
        env_name="csle-intrusion-response-game-workflow-pomdp-defender-v1",
        nodes=nodes, initial_zones=initial_zones, X_max=X_max, beta=beta, gamma=gamma,
        zones=zones, Z_D_P=Z_D_P, C_D=C_D, A_P=A_P, Z_U=Z_U, adjacency_matrix=adjacency_matrix, eta=eta,
        gw_reachable=gw_reachable)
    input_config = WorkflowIntrusionResponsePOMDPDefenderConfig(
        game_config=game_config, env_name="csle-intrusion-response-game-workflow-pomdp-defender-v1",
        attacker_strategies=attacker_strategies
    )
    return input_config


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--install", help="Boolean parameter, if true, install config",
                        action="store_true")
    parser.add_argument("-u", "--uninstall", help="Boolean parameter, if true, uninstall config",
                        action="store_true")
    args = parser.parse_args()
    gw_reachable = np.array([0, 1, 2])
    adjacency_matrix = [
        [1, 0, 0, 1, 1, 0],
        [0, 1, 0, 1, 0, 1],
        [0, 0, 1, 0, 1, 1],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1]
    ]
    adjacency_matrix = np.array(adjacency_matrix)
    config = default_config(name="csle-intrusion-response-game-workflow-pomdp-defender-001", version="0.0.1",
                            number_of_zones=5, X_max=10, beta=10, reachable=True, initial_zone=3,
                            attack_success_probability=0.3, eta=0.5, defender_action_cost=1, zone_utility=10,
                            detection_probability=0.1, num_nodes=6, adjacency_matrix=adjacency_matrix,
                            gw_reachable=gw_reachable, gamma=0.99)
    if args.install:
        SimulationEnvController.install_simulation(config=config)
        img_path = ExperimentUtil.default_simulation_picture_path()
        if os.path.exists(img_path):
            image_data = ExperimentUtil.read_env_picture(img_path)
            SimulationEnvController.save_simulation_image(img=image_data, simulation=config.name)
    if args.uninstall:
        SimulationEnvController.uninstall_simulation(config=config)
