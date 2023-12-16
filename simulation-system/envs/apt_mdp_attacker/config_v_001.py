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
from csle_common.dao.training.random_policy import RandomPolicy
from csle_common.dao.training.player_type import PlayerType
from gym_csle_apt_game.util.apt_game_util import AptGameUtil
from gym_csle_apt_game.dao.apt_game_config import AptGameConfig
from gym_csle_apt_game.dao.apt_game_attacker_mdp_config import AptGameAttackerMdpConfig


def default_config(N: int, p_a: float, num_observations: int,
                   name: str, version: str = "0.0.1") -> SimulationEnvConfig:
    """
    The default configuration of the simulation environment

    :param name: the name of the environment
    :param version: the version string
    :param: N: the number of servers
    :param: num_observations: the number of observations
    :param p_a: the intrusion success probability
    :return:the default configuration
    """
    players_config = default_players_config()
    state_space_config = default_state_space_config(N=N)
    joint_action_space_config = default_joint_action_space_config()
    joint_observation_space_config = default_joint_observation_space_config(num_observations=num_observations)
    transition_operator_config = default_transition_operator_config(N=N, p_a=p_a)
    observation_function_config = default_observation_function_config(num_observations=num_observations, N=N)
    reward_function_config = default_reward_function_config(N=N)
    initial_state_distribution_config = default_initial_state_distribution_config(N=N)
    input_config = default_input_config(
        defender_observation_space_config=joint_observation_space_config.observation_spaces[0],
        reward_function_config=reward_function_config,
        transition_tensor_config=transition_operator_config,
        observation_function_config=observation_function_config,
        initial_state_distribution_config=initial_state_distribution_config, N=N, p_a=p_a,
        action_space_config=joint_action_space_config)
    env_parameters_config = default_env_parameters_config()
    descr = "A two-player zero-sum one-sided partially observed stochastic APT game."
    simulation_env_config = SimulationEnvConfig(
        name=name, version=version, descr=descr,
        players_config=players_config, state_space_config=state_space_config,
        joint_action_space_config=joint_action_space_config,
        joint_observation_space_config=joint_observation_space_config,
        transition_operator_config=transition_operator_config,
        observation_function_config=observation_function_config, reward_function_config=reward_function_config,
        initial_state_distribution_config=initial_state_distribution_config, simulation_env_input_config=input_config,
        time_step_type=TimeStepType.DISCRETE,
        gym_env_name="csle-apt-game-v1", env_parameters_config=env_parameters_config,
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
        PlayerConfig(name="attacker", id=2, descr="The attacker which tries to intrude on the infrastructure")
    ]
    players_config = PlayersConfig(
        player_configs=player_configs
    )
    return players_config


def default_state_space_config(N: int) -> StateSpaceConfig:
    """
    :param: N: the number of servers
    :return: the default state space configuration of the simulation
    """
    states = [State(id=0, name="no intrusion state",
                    descr="A Markov state representing the case where the attacker "
                          "has not yet started an intrusion", state_type=StateType.ACTIVE)]
    for i in range(1, N + 1):
        states.append(State(id=i, name=f"state where {i} servers are compromised",
                            descr=f"A Markov state where {i} servers are compromised",
                            state_type=StateType.ACTIVE))
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
                    id=0, descr="Continue action, it means that the attacker is passive"
                ),
                Action(
                    id=1, descr="Stop action, it means that the attacker tries to attack a new server"
                )
            ],
            player_id=2, action_type=ValueType.INTEGER
        )
    ]
    joint_action_sapce_config = JointActionSpaceConfig(
        action_spaces=action_spaces
    )
    return joint_action_sapce_config


def default_joint_observation_space_config(num_observations: int) -> JointObservationSpaceConfig:
    """
    Gets the default joint observation space configuration of the simulation

    :param num_observations: the maximum number of observations
    :return: the default joint observation space configuration
    """
    obs = AptGameUtil.observation_space(num_observations=num_observations)
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
        ),
        ObservationSpaceConfig(
            observations=observations,
            observation_type=ValueType.INTEGER,
            player_id=2,
            descr="The observation space of the attacker. The attacker observes the weighted sum of alerts",
            observation_id_to_observation_id_vector=observation_id_to_observation_id_vector,
            observation_component_name_to_index=observation_component_name_to_index,
            component_observations=component_observations,
            observation_id_to_observation_vector=observation_id_to_observation_vector
        )
    ]
    joint_observation_space_config = JointObservationSpaceConfig(observation_spaces=observation_spaces)
    return joint_observation_space_config


def default_reward_function_config(N: int) -> RewardFunctionConfig:
    """
    :param: N: the number of servers
    :return: the default reward function configuration
    """
    cost_tensor = AptGameUtil.cost_tensor(N=N)
    expanded_cost_tensor = []
    for _ in [1]:
        l_tensor = []
        for a1 in AptGameUtil.defender_actions():
            a1_tensor = []
            for _ in AptGameUtil.attacker_actions():
                a2_tensor = []
                for s in AptGameUtil.state_space(N=N):
                    a2_tensor.append(cost_tensor[a1][s])
                a1_tensor.append(a2_tensor)
            l_tensor.append(a1_tensor)
        expanded_cost_tensor.append(l_tensor)
    reward_function_config = RewardFunctionConfig(
        reward_tensor=list(expanded_cost_tensor)
    )
    return reward_function_config


def default_transition_operator_config(N: int, p_a: float) -> TransitionOperatorConfig:
    """

    :param: N: the number of servers
    :param p_a: the intrusion success probability
    :return: the default transition tensor configuration
    """
    transition_tensor = AptGameUtil.transition_tensor(N=N, p_a=p_a)
    expanded_transition_tensor = []
    for _ in [1]:
        l_tensor = []
        for a1 in AptGameUtil.defender_actions():
            a1_tensor = []
            for a2 in AptGameUtil.attacker_actions():
                a2_tensor = []
                for s in AptGameUtil.state_space(N=N):
                    s_tensor = []
                    for s_prime in AptGameUtil.state_space(N=N):
                        s_tensor.append(transition_tensor[a1][a2][s][s_prime])
                    a2_tensor.append(s_tensor)
                a1_tensor.append(a2_tensor)
            l_tensor.append(a1_tensor)
        expanded_transition_tensor.append(l_tensor)
    transition_operator_config = TransitionOperatorConfig(transition_tensor=list(expanded_transition_tensor))
    return transition_operator_config


def default_observation_function_config(num_observations: int, N: int) -> ObservationFunctionConfig:
    """
    Default observation function config of the POMDP

    :param num_observations: the number of observations
    :return: the default observation function config
    """
    observation_tensor = AptGameUtil.observation_tensor(num_observations=num_observations, N=N)
    expanded_observation_tensor = []
    for _ in AptGameUtil.defender_actions():
        a1_tensor = []
        for _ in AptGameUtil.attacker_actions():
            a2_tensor = []
            for s in AptGameUtil.state_space(N=N):
                s_tensor = []
                for o in AptGameUtil.observation_space(num_observations=num_observations):
                    s_tensor.append(observation_tensor[s][o])
                a2_tensor.append(s_tensor)
            a1_tensor.append(a2_tensor)
        expanded_observation_tensor.append(a1_tensor)
    component_observation_tensors = {}
    component_observation_tensors["weighted_alerts"] = expanded_observation_tensor
    observation_function_config = ObservationFunctionConfig(
        observation_tensor=expanded_observation_tensor, component_observation_tensors=component_observation_tensors)
    return observation_function_config


def default_initial_state_distribution_config(N: int) -> InitialStateDistributionConfig:
    """
    :return: the default initial state distribution configuration
    """
    initial_state_distribution_config = InitialStateDistributionConfig(
        initial_state_distribution=list(AptGameUtil.b1(N=N)))
    return initial_state_distribution_config


def default_input_config(defender_observation_space_config: ObservationSpaceConfig,
                         reward_function_config: RewardFunctionConfig,
                         transition_tensor_config: TransitionOperatorConfig,
                         observation_function_config: ObservationFunctionConfig,
                         initial_state_distribution_config: InitialStateDistributionConfig,
                         action_space_config: JointActionSpaceConfig,
                         N: int, p_a: float) -> SimulationEnvInputConfig:
    """
    Gets the input configuration to the openai gym environment

    :param defender_observation_space_config: the configuration of the defender's observation space
    :param reward_function_config: the reward function configuration
    :param transition_tensor_config: the transition tensor configuration
    :param observation_function_config: the observation function configuration
    :param initial_state_distribution_config: the initial state distribution configuration
    :param action_space_config: the joint action space configuration
    :param: N: the number of servers
    :param p_a: the intrusion success probability
    :return: The default input configuration to the OpenAI gym environment
    """
    game_config = AptGameConfig(
        A1=AptGameUtil.attacker_actions(), A2=AptGameUtil.defender_actions(),
        b1=np.array(initial_state_distribution_config.initial_state_distribution),
        save_dir=ExperimentUtil.default_output_dir() + "/results",
        T=np.array(transition_tensor_config.transition_tensor),
        O=np.array(list(defender_observation_space_config.observation_id_to_observation_vector.keys())),
        Z=np.array(observation_function_config.observation_tensor),
        C=np.array(reward_function_config.reward_tensor),
        S=AptGameUtil.state_space(N=N),
        env_name="csle-apt-game-v1", checkpoint_traces_freq=100000,
        gamma=1, N=N, p_a=p_a)
    defender_strategy = RandomPolicy(actions=action_space_config.action_spaces[0].actions,
                                     player_type=PlayerType.DEFENDER, stage_policy_tensor=None)
    config = AptGameAttackerMdpConfig(
        env_name="csle-stopping-game-mdp-attacker-v1",
        apt_game_config=game_config, apt_game_name="csle-apt-game-v1",
        defender_strategy=defender_strategy
    )
    return config


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--install", help="Boolean parameter, if true, install config",
                        action="store_true")
    parser.add_argument("-u", "--uninstall", help="Boolean parameter, if true, uninstall config",
                        action="store_true")
    args = parser.parse_args()
    config = default_config(name="csle-apt-mdp-attacker-001", version="0.0.1", N=5, p_a=0.1, num_observations=10)

    if args.install:
        SimulationEnvController.install_simulation(config=config)
        img_path = ExperimentUtil.default_simulation_picture_path()
        if os.path.exists(img_path):
            image_data = ExperimentUtil.read_env_picture(img_path)
            SimulationEnvController.save_simulation_image(img=image_data, simulation=config.name)
    if args.uninstall:
        SimulationEnvController.uninstall_simulation(config=config)
