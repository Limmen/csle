import argparse
import os
import numpy as np
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
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig


def default_config(name: str, version: str = "0.0.1", min_severe_alerts: int = 0, max_severe_alerts: int = 20,
                   min_warning_alerts: int = 0, max_warning_alerts: int = 20, min_login_attempts: int = 0,
                   max_login_attempts: int = 10) -> SimulationEnvConfig:
    """
    The default configuration of the simulation environment

    :param name: the name of the environment
    :param version: the version string
    :param min_severe_alerts: if using heuristic observation space, this defines the min number of severe alerts
    :param max_severe_alerts: if using heuristic observation space, this defines the max number of severe alerts
    :param min_warning_alerts: if using heuristic observation space, this defines the min number of warning alerts
    :param max_warning_alerts: if using heuristic observation space, this defines the max number of warning alerts
    :param min_login_attempts: if using heuristic observation space, this defines the min number of login attempts
    :param max_login_attempts: if using heuristic observation space, this defines the max number of login attempts
    :return:the default configuration
    """
    players_config = default_players_config()
    state_space_config = default_state_space_config()
    joint_action_space_config = default_joint_action_space_config()
    joint_observation_space_config = default_joint_observation_space_config(
        min_login_attempts=min_login_attempts, max_login_attempts=max_login_attempts,
        min_severe_alerts=min_severe_alerts, max_severe_alerts=max_severe_alerts,
        min_warning_alerts=min_warning_alerts,
        max_warning_alerts=max_warning_alerts)
    transition_operator_config = default_transition_operator_config()
    observation_function_config = default_observation_function_config(
        defender_obs_space=joint_observation_space_config.observation_spaces[0],
        joint_action_space=joint_action_space_config, state_space=state_space_config,
        min_severe_alerts=min_severe_alerts, max_severe_alerts=max_severe_alerts,
        min_warning_alerts=min_warning_alerts,
        max_warning_alerts=max_warning_alerts, min_login_attempts=min_login_attempts,
        max_login_attempts=max_login_attempts
    )
    reward_function_config = default_reward_function_config()
    initial_state_distribution_config = default_initial_state_distribution_config()
    input_config = default_input_config(
        defender_observation_space_config=joint_observation_space_config.observation_spaces[0],
        reward_function_config=reward_function_config,
        transition_tensor_config=transition_operator_config,
        observation_function_config=observation_function_config,
        initial_state_distribution_config=initial_state_distribution_config)
    env_parameters_config = default_env_parameters_config()
    descr = "A two-player zero-sum one-sided partially observed stochastic game. " \
            "The game is based on the optimal stopping formulation of intrusion prevention " \
            "from (Hammar and Stadler 2021, https://ieeexplore.ieee.org/document/9779345)"
    simulation_env_config = SimulationEnvConfig(
        name=name, version=version, descr=descr,
        players_config=players_config, state_space_config=state_space_config,
        joint_action_space_config=joint_action_space_config,
        joint_observation_space_config=joint_observation_space_config,
        transition_operator_config=transition_operator_config,
        observation_function_config=observation_function_config, reward_function_config=reward_function_config,
        initial_state_distribution_config=initial_state_distribution_config, simulation_env_input_config=input_config,
        time_step_type=TimeStepType.DISCRETE,
        gym_env_name="csle-stopping-game-v1", env_parameters_config=env_parameters_config,
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
        PlayerConfig(name="defender", id=1, descr="The defender which tries to detect, prevent, "
                                                  "and interrupt intrusions for the infrastructure"),
        PlayerConfig(name="attacker", id=2, descr="The attacker which tries to intrude on the infrastructure")
    ]
    players_config = PlayersConfig(
        player_configs=player_configs
    )
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
    state_space_config = StateSpaceConfig(
        states=states
    )
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
    joint_action_sapce_config = JointActionSpaceConfig(
        action_spaces=action_spaces
    )
    return joint_action_sapce_config


def default_joint_observation_space_config(
        min_severe_alerts: int = 0, max_severe_alerts: int = 100,
        min_warning_alerts: int = 0, max_warning_alerts: int = 100, min_login_attempts: int = 0,
        max_login_attempts: int = 100) -> JointObservationSpaceConfig:
    """
    Gets the default joint observation space configuration of the simulation

    :param min_severe_alerts: if using heuristic observation space, this defines the min number of severe alerts
    :param max_severe_alerts: if using heuristic observation space, this defines the max number of severe alerts
    :param min_warning_alerts: if using heuristic observation space, this defines the min number of warning alerts
    :param max_warning_alerts: if using heuristic observation space, this defines the max number of warning alerts
    :param min_login_attempts: if using heuristic observation space, this defines the min number of login attempts
    :param max_login_attempts: if using heuristic observation space, this defines the max number of login attempts
    :return: the default joint observation space configuration
    """
    observation_id_to_observation_id_vector = {}
    observation_id_to_observation_vector = {}
    defender_observations = []
    component_observations = {}
    component_observations["severe_alerts"] = []
    for val in range(min_severe_alerts, max_severe_alerts):
        component_observations["severe_alerts"].append(Observation(id=val, val=val,
                                                                   descr=f"{val} severe IDS alerts"))

    component_observations["warning_alerts"] = []
    for val in range(min_warning_alerts, max_warning_alerts):
        component_observations["warning_alerts"].append(Observation(id=val, val=val,
                                                                    descr=f"{val} warning IDS alerts"))

    component_observations["login_attempts"] = []
    for val in range(min_login_attempts, max_login_attempts):
        component_observations["login_attempts"].append(Observation(id=val, val=val,
                                                                    descr=f"{val} login attempts"))

    for i in range(min_severe_alerts, max_severe_alerts):
        for j in range(min_warning_alerts, max_warning_alerts):
            for k in range(min_login_attempts, max_login_attempts):
                id = (i * (len(range(min_warning_alerts, max_warning_alerts)) *
                           len(range(min_login_attempts, max_login_attempts))) + j *
                      len(range(min_login_attempts, max_login_attempts)) + k)
                defender_observations.append(Observation(
                    id=id, val=id,
                    descr=f"{i} severe IDS alerts, {j} warning ids alerts, f{k} login attempts"))
                observation_id_to_observation_vector[id] = [i, j, k]
                observation_id_to_observation_id_vector[id] = [i, j, k]

    observation_component_name_to_index = {
        "severe_alerts": 0,
        "warning_alerts": 1,
        "login_attempts": 2
    }

    observation_spaces = [
        ObservationSpaceConfig(
            observations=defender_observations,
            observation_type=ValueType.INTEGER,
            player_id=1,
            descr="The observation space of the defender. The defender observes three metrics from the infrastructure: "
                  "the number of severe IDS alerts, the number of warning IDS alerts, the number of login attempts",
            observation_id_to_observation_id_vector=observation_id_to_observation_id_vector,
            observation_component_name_to_index=observation_component_name_to_index,
            component_observations=component_observations,
            observation_id_to_observation_vector=observation_id_to_observation_vector
        ),
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
        reward_tensor=list(StoppingGameUtil.reward_tensor(R_INT=-5, R_COST=-5, R_SLA=1, R_ST=5, L=3))
    )
    return reward_function_config


def default_transition_operator_config() -> TransitionOperatorConfig:
    """
    :return: the default transition tensor configuration
    """
    transition_operator_config = TransitionOperatorConfig(
        transition_tensor=list(StoppingGameUtil.transition_tensor(L=3))
    )
    return transition_operator_config


def default_observation_function_config(
        defender_obs_space: ObservationSpaceConfig,
        joint_action_space: JointActionSpaceConfig, state_space: StateSpaceConfig,
        min_severe_alerts: int = 0, max_severe_alerts: int = 100, min_warning_alerts: int = 0,
        max_warning_alerts: int = 100, min_login_attempts: int = 0,
        max_login_attempts: int = 100) -> ObservationFunctionConfig:
    """
    The default observation function configuration

    :param min_severe_alerts: if using heuristic observation space, this defines the min number of severe alerts
    :param max_severe_alerts: if using heuristic observation space, this defines the max number of severe alerts
    :param min_warning_alerts: if using heuristic observation space, this defines the min number of warning alerts
    :param max_warning_alerts: if using heuristic observation space, this defines the max number of warning alerts
    :param min_login_attempts: if using heuristic observation space, this defines the min number of login attempts
    :param max_login_attempts: if using heuristic observation space, this defines the max number of login attempts
    :return: the default configuration of the observation function
    """
    component_observation_tensors = {}
    severe_alerts_tensor = StoppingGameUtil.observation_tensor(len(range(min_severe_alerts, max_severe_alerts)) - 1)
    warning_alerts_tensor = StoppingGameUtil.observation_tensor(len(range(min_warning_alerts, max_warning_alerts)) - 1)
    login_attempts_tensor = StoppingGameUtil.observation_tensor(len(range(min_login_attempts, max_login_attempts)) - 1)
    component_observation_tensors["severe_alerts"] = list(severe_alerts_tensor.tolist())
    component_observation_tensors["warning_alerts"] = list(warning_alerts_tensor.tolist())
    component_observation_tensors["login_attempts"] = list(login_attempts_tensor.tolist())
    observation_tensor = []
    for a1 in range(len(joint_action_space.action_spaces[0].actions)):
        a1_a2_s_o_dist = []
        for a2 in range(len(joint_action_space.action_spaces[1].actions)):
            a2_s_o_dist = []
            for s in range(len(state_space.states)):
                s_o_dist = []
                for o in range(len(defender_obs_space.observations)):
                    obs_vector = defender_obs_space.observation_id_to_observation_vector[o]
                    p = (severe_alerts_tensor[a1][a2][s][obs_vector[0]] *
                         warning_alerts_tensor[a1][a2][s][obs_vector[1]] *
                         login_attempts_tensor[a1][a2][s][obs_vector[2]])
                    s_o_dist.append(p)
                assert round(sum(s_o_dist), 2) == 1.0
                a2_s_o_dist.append(s_o_dist)
            a1_a2_s_o_dist.append(a2_s_o_dist)
        observation_tensor.append(a1_a2_s_o_dist)
    observation_function_config = ObservationFunctionConfig(
        observation_tensor=observation_tensor, component_observation_tensors=component_observation_tensors
    )
    return observation_function_config


def default_initial_state_distribution_config() -> InitialStateDistributionConfig:
    """
    :return: the default initial state distribution configuration
    """
    initial_state_distribution_config = InitialStateDistributionConfig(
        initial_state_distribution=list(StoppingGameUtil.b1())
    )
    return initial_state_distribution_config


def default_input_config(defender_observation_space_config: ObservationSpaceConfig,
                         reward_function_config: RewardFunctionConfig,
                         transition_tensor_config: TransitionOperatorConfig,
                         observation_function_config: ObservationFunctionConfig,
                         initial_state_distribution_config: InitialStateDistributionConfig) -> SimulationEnvInputConfig:
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--install", help="Boolean parameter, if true, install config",
                        action="store_true")
    parser.add_argument("-u", "--uninstall", help="Boolean parameter, if true, uninstall config",
                        action="store_true")
    args = parser.parse_args()
    config = default_config(name="csle-stopping-game-001", version="0.0.1")

    if args.install:
        SimulationEnvController.install_simulation(config=config)
        img_path = ExperimentUtil.default_simulation_picture_path()
        if os.path.exists(img_path):
            image_data = ExperimentUtil.read_env_picture(img_path)
            SimulationEnvController.save_simulation_image(img=image_data, simulation=config.name)
    if args.uninstall:
        SimulationEnvController.uninstall_simulation(config=config)
