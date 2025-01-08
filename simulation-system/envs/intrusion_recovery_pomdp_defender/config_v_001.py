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
from csle_tolerance.util.intrusion_recovery_pomdp_util import IntrusionRecoveryPomdpUtil
from csle_tolerance.dao.intrusion_recovery_pomdp_config import IntrusionRecoveryPomdpConfig


def default_config(name: str, eta: float, p_a: float, p_c_1: float, p_c_2: float, p_u: float,
                   BTR: int, negate_costs: bool, seed: int, discount_factor: float, num_observations: int,
                   version: str = "0.0.1") -> SimulationEnvConfig:
    """
    The default configuration of the simulation environment

    :param name: the name of the simulation environment
    :param eta: the cost scaling parameter
    :param p_a: the intrusion probability
    :param p_c_1: the crash probability in the healthy state
    :param p_c_2: the crash probability in the compromised state
    :param p_u: the software upgrade probability
    :param BTR: the time horizon
    :param negate_costs: boolean flag indicating whether the costs should be negated or not
    :param seed: the random seed
    :param discount_factor: the discount factor
    :param num_observations: the number of observations
    :param version: the version of the environment
    :return: the default configuration
    """
    players_config = default_players_config()
    state_space_config = default_state_space_config()
    joint_action_space_config = default_joint_action_space_config()
    joint_observation_space_config = default_joint_observation_space_config(num_observations=num_observations)
    transition_operator_config = default_transition_operator_config(p_a=p_a, p_c_1=p_c_1, p_c_2=p_c_2, p_u=p_u)
    observation_function_config = default_observation_function_config(num_observations=num_observations)
    reward_function_config = default_reward_function_config(eta=eta, negate_costs=negate_costs)
    initial_state_distribution_config = default_initial_state_distribution_config(p_a=p_a)
    input_config = default_input_config(
        eta=eta, p_a=p_a, p_c_1=p_c_1, p_c_2=p_c_2, p_u=p_u, BTR=BTR, negate_costs=negate_costs, seed=seed,
        discount_factor=discount_factor, simulation_env_name=name, num_observations=num_observations)
    env_parameters_config = default_env_parameters_config()
    descr = "Intrusion recovery POMDP in TOLERANCE"
    simulation_env_config = SimulationEnvConfig(
        name=name, version=version, descr=descr,
        players_config=players_config, state_space_config=state_space_config,
        joint_action_space_config=joint_action_space_config,
        joint_observation_space_config=joint_observation_space_config,
        transition_operator_config=transition_operator_config,
        observation_function_config=observation_function_config, reward_function_config=reward_function_config,
        initial_state_distribution_config=initial_state_distribution_config, simulation_env_input_config=input_config,
        time_step_type=TimeStepType.DISCRETE,
        gym_env_name="csle-tolerance-intrusion-recovery-pomdp-v1",
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
        PlayerConfig(name="defender", id=1, descr="The defender which tries to minimize costs and time-to-recovery")
    ]
    players_config = PlayersConfig(player_configs=player_configs)
    return players_config


def default_state_space_config() -> StateSpaceConfig:
    """
    Gets the default  state space configuration

    :return: the default state space configuration of the simulation
    """
    states = []
    states.append(State(id=0, name="Healthy", descr="Healthy state", state_type=StateType.ACTIVE))
    states.append(State(id=1, name="Compromised", descr="Compromised state", state_type=StateType.ACTIVE))
    states.append(State(id=2, name="Crashed", descr="Crashed state", state_type=StateType.TERMINAL))
    state_space_config = StateSpaceConfig(states=states)
    return state_space_config


def default_joint_action_space_config() -> JointActionSpaceConfig:
    """
    Gets the default action space configuration

    :return: the default joint action space of all players in the simulation
    """
    defender_actions = []
    defender_actions.append(Action(id=0, descr="Wait"))
    defender_actions.append(Action(id=1, descr="Recover"))
    attacker_actions = [Action(id=0, descr="Null")]
    action_spaces = [ActionSpaceConfig(actions=defender_actions, player_id=1, action_type=ValueType.INTEGER),
                     ActionSpaceConfig(actions=attacker_actions, player_id=2, action_type=ValueType.INTEGER)]
    joint_action_space_config = JointActionSpaceConfig(action_spaces=action_spaces)
    return joint_action_space_config


def default_joint_observation_space_config(num_observations: int) -> JointObservationSpaceConfig:
    """
    Gets the default joint observation space configuration of the simulation

    :param num_observations: the maximum number of observations
    :return: the default joint observation space configuration
    """
    obs = IntrusionRecoveryPomdpUtil.observation_space(num_observations=num_observations)
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


def default_reward_function_config(eta: float, negate_costs: bool) -> RewardFunctionConfig:
    """
    Gets the default reward function config

    :param eta: the cost scaling parameter
    :param negate_costs: boolean flag indicating whether the costs should be negated or not
    :return: the default reward function configuration
    """
    cost_tensor = IntrusionRecoveryPomdpUtil.cost_tensor(eta=eta, states=IntrusionRecoveryPomdpUtil.state_space(),
                                                         actions=IntrusionRecoveryPomdpUtil.action_space(),
                                                         negate=negate_costs)
    expanded_cost_tensor = []
    for _ in [1]:
        l_tensor = []
        for a1 in IntrusionRecoveryPomdpUtil.action_space():
            a1_tensor = []
            for _ in [1]:
                a2_tensor = []
                for s in IntrusionRecoveryPomdpUtil.state_space():
                    a2_tensor.append(cost_tensor[a1][s])
                a1_tensor.append(a2_tensor)
            l_tensor.append(a1_tensor)
        expanded_cost_tensor.append(l_tensor)
    reward_function_config = RewardFunctionConfig(reward_tensor=expanded_cost_tensor)
    return reward_function_config


def default_transition_operator_config(p_a: float, p_c_1: float, p_c_2: float, p_u: float) -> TransitionOperatorConfig:
    """
    Gets the default transition tensor configuration

    :param p_a: the intrusion probability
    :param p_c_1: the crash probability in the healthy state
    :param p_c_2: the crash probability in the compromised state
    :param p_u: the software upgrade probability
    :return: the default transition tensor configuration
    """
    transition_tensor = IntrusionRecoveryPomdpUtil.transition_tensor(
        states=IntrusionRecoveryPomdpUtil.state_space(), actions=IntrusionRecoveryPomdpUtil.action_space(),
        p_a=p_a, p_c_1=p_c_1, p_c_2=p_c_2, p_u=p_u)
    expanded_transition_tensor = []
    for _ in [1]:
        l_tensor = []
        for a1 in IntrusionRecoveryPomdpUtil.action_space():
            a1_tensor = []
            for _ in [1]:
                a2_tensor = []
                for s in IntrusionRecoveryPomdpUtil.state_space():
                    s_tensor = []
                    for s_prime in IntrusionRecoveryPomdpUtil.state_space():
                        s_tensor.append(transition_tensor[a1][s][s_prime])
                    a2_tensor.append(s_tensor)
                a1_tensor.append(a2_tensor)
            l_tensor.append(a1_tensor)
        expanded_transition_tensor.append(l_tensor)
    transition_operator_config = TransitionOperatorConfig(
        transition_tensor=expanded_transition_tensor)
    return transition_operator_config


def default_observation_function_config(num_observations: int) -> ObservationFunctionConfig:
    """
    Default observation function config of the POMDP

    :param num_observations: the number of observations
    :return: the default observation function config
    """
    observation_tensor = IntrusionRecoveryPomdpUtil.observation_tensor(
        states=IntrusionRecoveryPomdpUtil.state_space(),
        observations=IntrusionRecoveryPomdpUtil.observation_space(num_observations=num_observations))
    expanded_observation_tensor = []
    for _ in IntrusionRecoveryPomdpUtil.action_space():
        a1_tensor = []
        for _ in [1]:
            a2_tensor = []
            for s in IntrusionRecoveryPomdpUtil.state_space():
                s_tensor = []
                for o in IntrusionRecoveryPomdpUtil.observation_space(num_observations=num_observations):
                    s_tensor.append(observation_tensor[s][o])
                a2_tensor.append(s_tensor)
            a1_tensor.append(a2_tensor)
        expanded_observation_tensor.append(a1_tensor)
    component_observation_tensors = {}
    component_observation_tensors["weighted_alerts"] = expanded_observation_tensor
    observation_function_config = ObservationFunctionConfig(
        observation_tensor=expanded_observation_tensor, component_observation_tensors=component_observation_tensors)
    return observation_function_config


def default_initial_state_distribution_config(p_a: float) -> InitialStateDistributionConfig:
    """
    Gets the default initial state distribution configuration

    :param p_a: the intrusion probability
    :return: the default initial state distribution configuration
    """
    initial_state_distribution_config = InitialStateDistributionConfig(
        initial_state_distribution=IntrusionRecoveryPomdpUtil.initial_belief())
    return initial_state_distribution_config


def default_input_config(eta: float, p_a: float, p_c_1: float, p_c_2: float, p_u: float, BTR: int, negate_costs: bool,
                         seed: int, discount_factor: float, simulation_env_name: str, num_observations: int) \
        -> SimulationEnvInputConfig:
    """
    Gets the default input configuration for the RL environment

    :param eta: the cost scaling factor
    :param p_a: the intrusion probability
    :param p_c_1: the crash probability in the healthy state
    :param p_c_2: the crash probability in the compromised state
    :param p_u: the software upgrade probability
    :param BTR: the time horizon
    :param negate_costs: boolean flag indicating whether costs should be negated or not
    :param seed: the random seed
    :param discount_factor: the discount factor
    :param simulation_env_name: the name of the simulation environment
    :param num_observations: the number of observations
    :return: the default input configuration
    """
    cost_tensor = IntrusionRecoveryPomdpUtil.cost_tensor(eta=eta, states=IntrusionRecoveryPomdpUtil.state_space(),
                                                         actions=IntrusionRecoveryPomdpUtil.action_space(),
                                                         negate=negate_costs)
    observation_tensor = IntrusionRecoveryPomdpUtil.observation_tensor(
        states=IntrusionRecoveryPomdpUtil.state_space(),
        observations=IntrusionRecoveryPomdpUtil.observation_space(num_observations=num_observations))
    transition_tensor = IntrusionRecoveryPomdpUtil.transition_tensor(
        states=IntrusionRecoveryPomdpUtil.state_space(), actions=IntrusionRecoveryPomdpUtil.action_space(), p_a=p_a,
        p_c_1=p_c_1, p_c_2=p_c_2, p_u=p_u)
    config = IntrusionRecoveryPomdpConfig(
        eta=eta, p_a=p_a, p_c_1=p_c_1, p_c_2=p_c_2, p_u=p_u, BTR=BTR, negate_costs=negate_costs, seed=seed,
        discount_factor=discount_factor, states=IntrusionRecoveryPomdpUtil.state_space(),
        actions=IntrusionRecoveryPomdpUtil.action_space(),
        observations=IntrusionRecoveryPomdpUtil.observation_space(num_observations=num_observations),
        cost_tensor=cost_tensor, observation_tensor=observation_tensor, transition_tensor=transition_tensor,
        b1=IntrusionRecoveryPomdpUtil.initial_belief(), T=BTR,
        simulation_env_name=simulation_env_name, gym_env_name="csle-tolerance-intrusion-recovery-pomdp-v1"
    )
    return config


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--install", help="Boolean parameter, if true, install config",
                        action="store_true")
    parser.add_argument("-u", "--uninstall", help="Boolean parameter, if true, uninstall config",
                        action="store_true")
    args = parser.parse_args()
    config = default_config(name="csle-tolerance-intrusion-recovery-pomdp-defender-001", version="0.0.1",
                            eta=1, p_a=0.1, p_c_1=0.00001, p_c_2=0.001, p_u=0.02, BTR=20, negate_costs=False,
                            discount_factor=1, seed=999, num_observations=10)
    if args.install:
        SimulationEnvController.install_simulation(config=config)
        img_path = ExperimentUtil.default_simulation_picture_path()
        if os.path.exists(img_path):
            image_data = ExperimentUtil.read_env_picture(img_path)
            SimulationEnvController.save_simulation_image(img=image_data, simulation=config.name)
    if args.uninstall:
        SimulationEnvController.uninstall_simulation(config=config)
