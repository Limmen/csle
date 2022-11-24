from typing import Dict, Any
from csle_common.dao.simulation_config.simulation_env_input_config import SimulationEnvInputConfig
from csle_common.dao.simulation_config.players_config import PlayersConfig
from csle_common.dao.simulation_config.state_space_config import StateSpaceConfig
from csle_common.dao.simulation_config.joint_action_space_config import JointActionSpaceConfig
from csle_common.dao.simulation_config.joint_observation_space_config import JointObservationSpaceConfig
from csle_common.dao.simulation_config.time_step_type import TimeStepType
from csle_common.dao.simulation_config.reward_function_config import RewardFunctionConfig
from csle_common.dao.simulation_config.transition_operator_config import TransitionOperatorConfig
from csle_common.dao.simulation_config.observation_function_config import ObservationFunctionConfig
from csle_common.dao.simulation_config.initial_state_distribution_config import InitialStateDistributionConfig
from csle_common.dao.simulation_config.env_parameters_config import EnvParametersConfig
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from gym_csle_stopping_game.dao.stopping_game_defender_pomdp_config import StoppingGameDefenderPomdpConfig
from gym_csle_stopping_game.dao.stopping_game_attacker_mdp_config import StoppingGameAttackerMdpConfig


class SimulationEnvConfig:
    """
    A DTO class representing the configuration of a simulation environment
    """

    def __init__(self, name: str, descr: str, version: str,
                 gym_env_name: str,
                 simulation_env_input_config: SimulationEnvInputConfig,
                 players_config: PlayersConfig, state_space_config: StateSpaceConfig,
                 joint_action_space_config: JointActionSpaceConfig,
                 joint_observation_space_config: JointObservationSpaceConfig, time_step_type: TimeStepType,
                 reward_function_config: RewardFunctionConfig, transition_operator_config: TransitionOperatorConfig,
                 observation_function_config: ObservationFunctionConfig,
                 initial_state_distribution_config: InitialStateDistributionConfig,
                 env_parameters_config: EnvParametersConfig, plot_transition_probabilities: bool = False,
                 plot_observation_function: bool = False, plot_reward_function: bool = False
                 ):
        """
        Initializes the DTO

        :param name: the name of the simulation
        :param gym_env_name: the name of the OpenAI gym environment
        :param descr: the description of the simulation
        :param simulation_env_input_config: the input configuration to the simulation
        :param players_config: the players configuration of the simulation
        :param state_space_config: the state space configuration of the simulation
        :param joint_action_space_config: the joint action space configuration of the simulation
        :param joint_observation_space_config: the joint observation space config of the simulation
        :param time_step_type: the time step type of the simulation
        :param reward_function_config: the reward function configuration of the of the simulation
        :param transition_operator_config: the transition operator configuration of the simulation
        :param observation_function_config: the observation function configuration of the simulation
        :param emulation_statistic_id: the id of the emulation statistic
        :param initial_state_distribution_config: the initial state distribution configuration of the simulation
        :param version: the version of the environment
        :param env_parameters_config: parameters that are not part of the state but that the poliy depends on.
        :param plot_transition_probabilities: boolean parameter whether to plot transition probabilities or not
        :param plot_observation_function: boolean parameter whether to plot the observation function or not
        :param plot_reward_function: boolean parameter whether to plot the reward function or not
        """
        self.name = name
        self.descr = descr
        self.simulation_env_input_config = simulation_env_input_config
        self.players_config = players_config
        self.state_space_config = state_space_config
        self.joint_action_space_config = joint_action_space_config
        self.joint_observation_space_config = joint_observation_space_config
        self.time_step_type = time_step_type
        self.reward_function_config = reward_function_config
        self.transition_operator_config = transition_operator_config
        self.observation_function_config = observation_function_config
        self.initial_state_distribution_config = initial_state_distribution_config
        self.version = version
        self.gym_env_name = gym_env_name
        self.image = None
        self.id = -1
        self.env_parameters_config = env_parameters_config
        self.plot_transition_probabilities = plot_transition_probabilities
        self.plot_observation_function = plot_observation_function
        self.plot_reward_function = plot_reward_function

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SimulationEnvConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        input_config = None
        try:
            input_config = StoppingGameConfig.from_dict(d["simulation_env_input_config"])
        except Exception:
            try:
                input_config = StoppingGameAttackerMdpConfig.from_dict(d["simulation_env_input_config"])
            except Exception:
                input_config = StoppingGameDefenderPomdpConfig.from_dict(d["simulation_env_input_config"])
        obj = SimulationEnvConfig(
            name=d["name"], descr=d["descr"],
            simulation_env_input_config=input_config,
            players_config=PlayersConfig.from_dict(d["players_config"]),
            state_space_config=StateSpaceConfig.from_dict(d["state_space_config"]),
            joint_action_space_config=JointActionSpaceConfig.from_dict(d["joint_action_space_config"]),
            joint_observation_space_config=JointObservationSpaceConfig.from_dict(d["joint_observation_space_config"]),
            time_step_type=d["time_step_type"],
            reward_function_config=RewardFunctionConfig.from_dict(d["reward_function_config"]),
            transition_operator_config=TransitionOperatorConfig.from_dict(d["transition_operator_config"]),
            observation_function_config=ObservationFunctionConfig.from_dict(d["observation_function_config"]),
            initial_state_distribution_config=InitialStateDistributionConfig.from_dict(
                d["initial_state_distribution_config"]),
            version=d["version"], gym_env_name=d["gym_env_name"],
            env_parameters_config=EnvParametersConfig.from_dict(d["env_parameters_config"]),
            plot_transition_probabilities=d["plot_transition_probabilities"],
            plot_observation_function=d["plot_observation_function"],
            plot_reward_function=d["plot_reward_function"]
        )
        obj.id = d["id"]
        obj.image = d["image"]
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["name"] = self.name
        d["descr"] = self.descr
        d["simulation_env_input_config"] = self.simulation_env_input_config.to_dict()
        d["players_config"] = self.players_config.to_dict()
        d["state_space_config"] = self.state_space_config.to_dict()
        d["joint_action_space_config"] = self.joint_action_space_config.to_dict()
        d["joint_observation_space_config"] = self.joint_observation_space_config.to_dict()
        d["time_step_type"] = self.time_step_type
        d["reward_function_config"] = self.reward_function_config.to_dict()
        d["transition_operator_config"] = self.transition_operator_config.to_dict()
        d["observation_function_config"] = self.observation_function_config.to_dict()
        d["initial_state_distribution_config"] = self.initial_state_distribution_config.to_dict()
        d["version"] = self.version
        d["gym_env_name"] = self.gym_env_name
        d["id"] = self.id
        d["image"] = self.image
        d["env_parameters_config"] = self.env_parameters_config.to_dict()
        d["plot_transition_probabilities"] = self.plot_transition_probabilities
        d["plot_observation_function"] = self.plot_observation_function
        d["plot_reward_function"] = self.plot_reward_function
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"name: {self.name}, descr: {self.descr}, " \
               f"simulation_env_input_config: {self.simulation_env_input_config}, " \
               f"players_config: {self.players_config}, state_space_config: {self.state_space_config}," \
               f"joint_action_space_config: {self.joint_action_space_config}, " \
               f"joint_observation_space_config: {self.joint_observation_space_config}, " \
               f"time_step_type: {self.time_step_type}, reward_function_config: {self.reward_function_config}, " \
               f"transition_operator_config: {self.transition_operator_config}, " \
               f"observation_function_config: {self.observation_function_config}, " \
               f"initial_state_distribution_config: {self.initial_state_distribution_config}," \
               f"version: {self.version}, gym_env_name: {self.gym_env_name}, id: {self.id}," \
               f"env_parameters_config: {self.env_parameters_config}," \
               f"plot_observation_function: {self.plot_observation_function}," \
               f"plot_transition_probabilities: {self.plot_transition_probabilities}," \
               f"plot_reward_function: {self.plot_reward_function}"

    def copy(self) -> "SimulationEnvConfig":
        """
        :return: a copy of the DTO
        """
        return self.from_dict(self.to_dict())
