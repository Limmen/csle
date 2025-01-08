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
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from gym_csle_stopping_game.dao.stopping_game_attacker_mdp_config import StoppingGameAttackerMdpConfig


def default_config(name: str, version: str = "0.0.2", min_alerts_weighted_by_priority: int = 0,
                   max_alerts_weighted_by_priority: int = 100) -> SimulationEnvConfig:
    """
    The default configuration of the simulation environment

    :param name: the name of the environment
    :param version: the version string
    :param min_alerts_weighted_by_priority: if using heuristic observation space, this defines the min number of
                                            alerts weighted by priority
    :param max_alerts_weighted_by_priority: if using heuristic observation space, this defines the max number of
                                            alerts weighted by priority
    :return:the default configuration
    """
    players_config = default_players_config()
    state_space_config = default_state_space_config()
    joint_action_space_config = default_joint_action_space_config()
    joint_observation_space_config = default_joint_observation_space_config(
        min_alerts_weighted_by_priority=min_alerts_weighted_by_priority,
        max_alerts_weighted_by_priority=max_alerts_weighted_by_priority)
    transition_operator_config = default_transition_operator_config()
    observation_function_config = default_observation_function_config(
        defender_obs_space=joint_observation_space_config.observation_spaces[0],
        joint_action_space=joint_action_space_config, state_space=state_space_config,
        min_alerts_weighted_by_priority=min_alerts_weighted_by_priority,
        max_alerts_weighted_by_priority=max_alerts_weighted_by_priority)
    reward_function_config = default_reward_function_config()
    initial_state_distribution_config = default_initial_state_distribution_config()
    input_config = default_input_config(
        defender_observation_space_config=joint_observation_space_config.observation_spaces[0],
        reward_function_config=reward_function_config,
        transition_tensor_config=transition_operator_config,
        observation_function_config=observation_function_config,
        initial_state_distribution_config=initial_state_distribution_config,
        defender_action_space_config=joint_action_space_config.action_spaces[0])
    env_parameters_config = default_env_parameters_config()
    descr = "A MDP based on the optimal stopping formulation of intrusion prevention from " \
            "(Hammar and Stadler 2021, https://arxiv.org/abs/2111.00289)."
    simulation_env_config = SimulationEnvConfig(
        name=name, version=version, descr=descr,
        players_config=players_config, state_space_config=state_space_config,
        joint_action_space_config=joint_action_space_config,
        joint_observation_space_config=joint_observation_space_config,
        transition_operator_config=transition_operator_config,
        observation_function_config=observation_function_config, reward_function_config=reward_function_config,
        initial_state_distribution_config=initial_state_distribution_config, simulation_env_input_config=input_config,
        time_step_type=TimeStepType.DISCRETE,
        gym_env_name="csle-stopping-game-mdp-attacker-v1", env_parameters_config=env_parameters_config,
        plot_transition_probabilities=True, plot_observation_function=True, plot_reward_function=True
    )
    return simulation_env_config


def default_env_parameters_config() -> EnvParametersConfig:
    """
    :return: the default env parameters config
    """
    config = EnvParametersConfig(
        parameters=[
            EnvParameter(id=0, name="l=1", descr="1 stop remaining of the defender"),
            EnvParameter(id=1, name="l=2", descr="2 stops remaining of the defender"),
            EnvParameter(id=2, name="l=3", descr="3 stops remaining of the defender")
        ]
    )
    return config


def default_players_config() -> PlayersConfig:
    """
    :return: the default players configuration of the simulation
    """
    player_configs = [
        PlayerConfig(name="attacker", id=2, descr="The attacker which tries to intrude on the infrastructure")
    ]
    players_config = PlayersConfig(player_configs=player_configs)
    return players_config


def default_state_space_config() -> StateSpaceConfig:
    """
    :return: the default state space configuration of the simulation
    """
    states = [
        State(id=0, name="no intrusion state", descr="A Markov state representing the case where the attacker "
                                                     "has not yet started an intrusion", state_type=StateType.ACTIVE),
        State(id=1, name="intrusion state", descr="A Markov state representing the state of intrusion",
              state_type=StateType.ACTIVE),
        State(id=2, name="terminal state", descr="A terminal state the models the end of a game episode",
              state_type=StateType.TERMINAL)
    ]
    state_space_config = StateSpaceConfig(states=states)
    return state_space_config


def default_joint_action_space_config() -> JointActionSpaceConfig:
    """
    :return: the default joint action space of all players in the simulation
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


def default_joint_observation_space_config(
        min_alerts_weighted_by_priority: int = 0,
        max_alerts_weighted_by_priority: int = 100) -> JointObservationSpaceConfig:
    """
    Gets the default joint observation space configuration of the simulation

    :param min_alerts_weighted_by_priority: if using heuristic observation space, this defines the min number of
                                            alerts weighted by priority
    :param max_alerts_weighted_by_priority: if using heuristic observation space, this defines the max number of
                                            alerts weighted by priority
    :return: the default joint observation space configuration
    """
    observation_id_to_observation_id_vector = {}
    observation_id_to_observation_vector = {}
    defender_observations = []
    component_observations = {}
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
            descr="The observation space of the attacker. The attacker has inside information in the infrastructure "
                  "and observes the same metrics as the defender",
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


def default_reward_function_config() -> RewardFunctionConfig:
    """
    :return: the default reward function configuration
    """
    reward_function_config = RewardFunctionConfig(
        reward_tensor=list(StoppingGameUtil.reward_tensor(R_INT=-1, R_COST=-2, R_SLA=0, R_ST=10, L=3)))
    return reward_function_config


def default_transition_operator_config() -> TransitionOperatorConfig:
    """
    :return: the default transition tensor configuration
    """
    transition_operator_config = TransitionOperatorConfig(
        transition_tensor=list(StoppingGameUtil.transition_tensor(L=3)))
    return transition_operator_config


def default_observation_function_config(
        defender_obs_space: ObservationSpaceConfig,
        joint_action_space: JointActionSpaceConfig, state_space: StateSpaceConfig,
        min_alerts_weighted_by_priority: int = 0, max_alerts_weighted_by_priority: int = 100) \
        -> ObservationFunctionConfig:
    """
    The default observation function configuration

    :param min_alerts_weighted_by_priority: if using heuristic observation space, this defines the min number of
                                            alerts weighted by priority
    :param max_alerts_weighted_by_priority: if using heuristic observation space, this defines the max number of
                                            alerts weighted by priority
    :return: the default configuration of the observation function
    """
    component_observation_tensors = {}
    priority_alerts_tensor = StoppingGameUtil.observation_tensor(
        len(range(min_alerts_weighted_by_priority, max_alerts_weighted_by_priority)) - 1)
    component_observation_tensors["alerts_weighted_by_priority"] = list(priority_alerts_tensor.tolist())
    observation_tensor = priority_alerts_tensor
    observation_function_config = ObservationFunctionConfig(
        observation_tensor=observation_tensor, component_observation_tensors=component_observation_tensors)
    return observation_function_config


def default_initial_state_distribution_config() -> InitialStateDistributionConfig:
    """
    :return: the default initial state distribution configuration
    """
    initial_state_distribution_config = InitialStateDistributionConfig(
        initial_state_distribution=list(StoppingGameUtil.b1()))
    return initial_state_distribution_config


def default_input_config(defender_observation_space_config: ObservationSpaceConfig,
                         reward_function_config: RewardFunctionConfig,
                         transition_tensor_config: TransitionOperatorConfig,
                         observation_function_config: ObservationFunctionConfig,
                         initial_state_distribution_config: InitialStateDistributionConfig,
                         defender_action_space_config: ActionSpaceConfig) -> SimulationEnvInputConfig:
    """
    Gets the input configuration to the openai gym environment

    :param defender_observation_space_config: the configuration of the defender's observation space
    :param reward_function_config: the reward function configuration
    :param transition_tensor_config: the transition tensor configuration
    :param observation_function_config: the observation function configuration
    :param initial_state_distribution_config: the initial state distribution configuration
    :return: The default input configuration to the OpenAI gym environment
    """
    L = 3
    R_INT = -5
    R_COST = -5
    R_SLA = 1
    R_ST = 5

    stopping_game_config = StoppingGameConfig(
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
    config = StoppingGameAttackerMdpConfig(
        stopping_game_config=stopping_game_config, stopping_game_name="csle-stopping-game-v1",
        defender_strategy=RandomPolicy(actions=defender_action_space_config.actions,
                                       player_type=PlayerType.DEFENDER, stage_policy_tensor=None),
        env_name="csle-stopping-game-mdp-attacker-v1")
    return config


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--install", help="Boolean parameter, if true, install config",
                        action="store_true")
    parser.add_argument("-u", "--uninstall", help="Boolean parameter, if true, uninstall config",
                        action="store_true")
    args = parser.parse_args()
    config = default_config(name="csle-stopping-mdp-attacker-002", version="0.0.2")

    if args.install:
        SimulationEnvController.install_simulation(config=config)
        img_path = ExperimentUtil.default_simulation_picture_path()
        if os.path.exists(img_path):
            image_data = ExperimentUtil.read_env_picture(img_path)
            SimulationEnvController.save_simulation_image(img=image_data, simulation=config.name)
    if args.uninstall:
        SimulationEnvController.uninstall_simulation(config=config)
