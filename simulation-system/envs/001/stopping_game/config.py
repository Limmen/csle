import argparse
import os
import numpy as np
import csle_common.constants.constants as constants
from csle_common.controllers.simulation_env_manager import SimulationEnvManager
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
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
from csle_common.metastore.metastore_facade import MetastoreFacade
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig


def default_config(name: str, version: str = "0.0.1") -> SimulationEnvConfig:
    emulation_statistic = default_emulation_statistic()
    players_config = default_players_config()
    state_space_config = default_state_space_config()
    joint_action_space_config = default_joint_action_space_config()
    joint_observation_space_config = default_joint_observation_space_config(emulation_statistic=emulation_statistic)
    transition_operator_config = default_transition_operator_config()
    observation_function_config = default_observation_function_config(emulation_statistic=emulation_statistic)
    reward_function_config = default_reward_function_config()
    initial_state_distribution_config = default_initial_state_distribution_config()
    input_config = default_input_config(
        defender_observation_space_config=joint_observation_space_config.observation_spaces[0],
        reward_function_config=reward_function_config,
        transition_tensor_config=transition_operator_config,
        observation_function_config=observation_function_config,
        initial_state_distribution_config=initial_state_distribution_config)
    descr="An two-player zero-sum one-sided partially observed stochastic game. " \
          "The game is based on the optimal stopping formulation of intrusion prevention from " \
          "(Hammar and Stadler 2021, https://arxiv.org/abs/2111.00289)"
    simulation_env_config = SimulationEnvConfig(
        name=name, version=version, descr=descr,
        players_config=players_config, state_space_config=state_space_config,
        joint_action_space_config=joint_action_space_config,
        joint_observation_space_config=joint_observation_space_config,
        transition_operator_config=transition_operator_config,
        observation_function_config=observation_function_config, reward_function_config=reward_function_config,
        initial_state_distribution_config=initial_state_distribution_config, simulation_env_input_config=input_config,
        emulation_statistic=emulation_statistic, time_step_type=TimeStepType.DISCRETE
    )
    return simulation_env_config


def default_emulation_statistic() -> EmulationStatistics:
    emulation_statistic_id = 1
    emulation_statistic = MetastoreFacade.get_emulation_statistic(id=emulation_statistic_id)
    if emulation_statistic is None:
        raise ValueError(f"Emulation statistic with id: {emulation_statistic_id} does not exist in the metastore")
    return emulation_statistic


def default_players_config() -> PlayersConfig:
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
    states = [
        State(id=0, name="no intrusion state", descr="A Markov state representing the case where the attacker "
                                                     "has not yet started an intrusion"),
        State(id=1, name="intrusion state", descr="A Markov state representing the state of intrusion"),
        State(id=2, name="terminal state", descr="A terminal state the models the end of a game episode")
    ]
    state_space_config = StateSpaceConfig(
        states=states
    )
    return state_space_config


def default_joint_action_space_config() -> JointActionSpaceConfig:
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
            player_id = 1,
            action_type=ValueType.INTEGER
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
            player_id = 2,
            action_type=ValueType.INTEGER
        )
    ]
    joint_action_sapce_config = JointActionSpaceConfig(
        action_spaces=action_spaces
    )
    return joint_action_sapce_config


def default_joint_observation_space_config(emulation_statistic: EmulationStatistics) -> JointObservationSpaceConfig:
    defender_observations = []
    min_severe_alerts = min(
        min(emulation_statistic.conditionals[constants.SYSTEM_IDENTIFICATION.NO_INTRUSION_CONDITIONAL][
                "severe_alerts"].keys()),
        min(emulation_statistic.conditionals[constants.SYSTEM_IDENTIFICATION.INTRUSION_CONDITIONAL][
                "severe_alerts"].keys()))
    max_severe_alerts = max(
        max(emulation_statistic.conditionals[constants.SYSTEM_IDENTIFICATION.NO_INTRUSION_CONDITIONAL][
                "severe_alerts"].keys()),
        max(emulation_statistic.conditionals[constants.SYSTEM_IDENTIFICATION.INTRUSION_CONDITIONAL][
                "severe_alerts"].keys()))

    min_warning_alerts = min(
        min(emulation_statistic.conditionals[constants.SYSTEM_IDENTIFICATION.NO_INTRUSION_CONDITIONAL][
                "warning_alerts"].keys()),
        min(emulation_statistic.conditionals[constants.SYSTEM_IDENTIFICATION.INTRUSION_CONDITIONAL][
                "warning_alerts"].keys()))
    max_warning_alerts = max(
        max(emulation_statistic.conditionals[constants.SYSTEM_IDENTIFICATION.NO_INTRUSION_CONDITIONAL][
                "warning_alerts"].keys()),
        max(emulation_statistic.conditionals[constants.SYSTEM_IDENTIFICATION.INTRUSION_CONDITIONAL][
                "warning_alerts"].keys()))

    min_login_attempts = min(
        min(emulation_statistic.conditionals[constants.SYSTEM_IDENTIFICATION.NO_INTRUSION_CONDITIONAL][
                "severe_alerts"].keys()),
        min(emulation_statistic.conditionals[constants.SYSTEM_IDENTIFICATION.INTRUSION_CONDITIONAL][
                "severe_alerts"].keys()))
    max_login_attempts = max(
        max(emulation_statistic.conditionals[constants.SYSTEM_IDENTIFICATION.NO_INTRUSION_CONDITIONAL][
                "num_failed_login_attempts"].keys()),
        max(emulation_statistic.conditionals[constants.SYSTEM_IDENTIFICATION.INTRUSION_CONDITIONAL][
                "num_failed_login_attempts"].keys()))

    observation_id_to_observation_vector = {}

    for i in range(min_severe_alerts, max_severe_alerts+1):
        for j in range(min_warning_alerts+max_warning_alerts):
            for k in range(min_login_attempts, max_login_attempts):
                id = i*(len(range(min_warning_alerts+max_warning_alerts)))
                +j*len(range(min_login_attempts, max_login_attempts)) + k
                defender_observations.append(Observation(
                    id=id,
                    descr=f"{i} severe IDS alerts, {j} warning ids alerts, f{k} login attempts"))
                observation_id_to_observation_vector[id] = [i, j, k]

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
            observation_id_to_observation_vector = observation_id_to_observation_vector,
            observation_component_name_to_index = observation_component_name_to_index
        ),
        ObservationSpaceConfig(
            observations=defender_observations,
            observation_type=ValueType.INTEGER,
            player_id=0,
            descr="The observation space of the attacker. The attacker has inside information in the infrastructure "
                  "and observes the same metrics as the defender",
            observation_id_to_observation_vector = observation_id_to_observation_vector,
            observation_component_name_to_index = observation_component_name_to_index
        )
    ]
    joint_observation_space_config = JointObservationSpaceConfig(
        observation_spaces=observation_spaces
    )
    return joint_observation_space_config


def default_reward_function_config() -> RewardFunctionConfig:
    reward_function_config = RewardFunctionConfig(
        reward_tensor=list(StoppingGameUtil.reward_tensor(R_INT=-5, R_COST=-5, R_SLA=1, R_ST=5, L=3))
    )
    return reward_function_config


def default_transition_operator_config() -> TransitionOperatorConfig:
    transition_operator_config = TransitionOperatorConfig(
        transition_tensor=list(StoppingGameUtil.transition_tensor(L=3, p=0.01))
    )
    return transition_operator_config


def default_observation_function_config(emulation_statistic: EmulationStatistics) -> ObservationFunctionConfig:
    observation_function_config = ObservationFunctionConfig(
        observation_tensor=list(StoppingGameUtil.observation_tensor_from_emulation_statistics(
            emulation_statistic=emulation_statistic))
    )
    return observation_function_config


def default_initial_state_distribution_config() -> InitialStateDistributionConfig:
    initial_state_distribution_config = InitialStateDistributionConfig(
        initial_state_distribution=list(StoppingGameUtil.b1())
    )
    return initial_state_distribution_config


def default_input_config(defender_observation_space_config: ObservationSpaceConfig,
                         reward_function_config: RewardFunctionConfig,
                         transition_tensor_config: TransitionOperatorConfig,
                         observation_function_config: ObservationFunctionConfig,
                         initial_state_distribution_config: InitialStateDistributionConfig) -> SimulationEnvInputConfig:
    L=3
    R_INT = -5
    R_COST = -5
    R_SLA = 1
    R_ST = 5

    config = StoppingGameConfig(
        A1 = StoppingGameUtil.attacker_actions(), A2= StoppingGameUtil.defender_actions(), L=L, R_INT=R_INT,
        R_COST=R_COST,
        R_SLA=R_SLA, R_ST =R_ST,b1=np.array(initial_state_distribution_config.initial_state_distribution),
        save_dir=ExperimentUtil.default_output_dir() + "/results",
        T=np.array(transition_tensor_config.transition_tensor),
        O=np.array(defender_observation_space_config.observation_id_to_observation_vector.keys()),
        Z=np.array(observation_function_config.observation_tensor),
        R=np.array(reward_function_config.reward_tensor),
        S=StoppingGameUtil.state_space())
    return config


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--install", help="Boolean parameter, if true, install config",
                        action="store_true")
    parser.add_argument("-u", "--uninstall", help="Boolean parameter, if true, uninstall config",
                        action="store_true")
    args = parser.parse_args()
    if not os.path.exists(ExperimentUtil.default_simulation_config_path()):
        config = default_config(name="csle-stopping-game-001", version="0.0.1")
        ExperimentUtil.write_simulation_config_file(config, ExperimentUtil.default_simulation_config_path())
    config = ExperimentUtil.read_simulation_env_config(ExperimentUtil.default_simulation_config_path())

    if args.install:
        SimulationEnvManager.install_simulation(config=config)
    if args.uninstall:
        SimulationEnvManager.uninstall_simulation(config=config)