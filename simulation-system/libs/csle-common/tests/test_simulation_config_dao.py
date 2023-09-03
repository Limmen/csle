from typing import Dict
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.simulation_config.action_space_config import ActionSpaceConfig
from csle_common.dao.simulation_config.agent_log import AgentLog
from csle_common.dao.simulation_config.env_parameter import EnvParameter
from csle_common.dao.simulation_config.env_parameters_config import EnvParametersConfig
from csle_common.dao.simulation_config.initial_state_distribution_config import InitialStateDistributionConfig
from csle_common.dao.simulation_config.joint_action_space_config import JointActionSpaceConfig
from csle_common.dao.simulation_config.joint_observation_space_config import JointObservationSpaceConfig
from csle_common.dao.simulation_config.observation_space_config import ObservationSpaceConfig
from csle_common.dao.simulation_config.observation import Observation
from csle_common.dao.simulation_config.observation_function_config import ObservationFunctionConfig
from csle_common.dao.simulation_config.player_config import PlayerConfig
from csle_common.dao.simulation_config.players_config import PlayersConfig
from csle_common.dao.simulation_config.reward_function_config import RewardFunctionConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.simulation_config.state_space_config import StateSpaceConfig
from csle_common.dao.simulation_config.state import State
from csle_common.dao.simulation_config.transition_operator_config import TransitionOperatorConfig
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
from csle_common.dao.simulation_config.simulation_env_input_config import SimulationEnvInputConfig


class ExampleInputConfig(SimulationEnvInputConfig):
    """
    Test instance of the abstract SimulationEnvInputConfig class
    """

    def __init__(self, x: int) -> None:
        """
        Initializes the object

        :param x: the input parameter
        :return: None
        """
        self.x = x

    def to_dict(self) -> Dict[str, int]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, int] = {}
        d["x"] = self.x
        return d

    @staticmethod
    def from_dict(d: Dict[str, int]) -> "ExampleInputConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = ExampleInputConfig(x=d["x"])
        return obj

    @staticmethod
    def from_json_file(json_file_path: str) -> "ExampleInputConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return ExampleInputConfig.from_dict(json.loads(json_str))


class TestSimulationConfigDaoSuite:
    """
    Test suite for simulation config data access objects (DAOs)
    """

    def test_action(self, example_action: Action) -> None:
        """
        Tests creation and dict conversion of the Action DAO

        :param example_action: an example Action
        :return: None
        """
        assert isinstance(example_action.to_dict(), dict)
        assert isinstance(Action.from_dict(example_action.to_dict()), Action)
        assert Action.from_dict(example_action.to_dict()).to_dict() == example_action.to_dict()
        assert Action.from_dict(example_action.to_dict()) == example_action

    def test_action_space_config(self, example_action_space_config: ActionSpaceConfig) -> None:
        """
        Tests creation and dict conversion of the ActionSpaceConfig DAO

        :param example_action_space_config: an example ActionSpaceConfig
        :return: None
        """
        assert isinstance(example_action_space_config.to_dict(), dict)
        assert isinstance(ActionSpaceConfig.from_dict(example_action_space_config.to_dict()),
                          ActionSpaceConfig)
        assert ActionSpaceConfig.from_dict(example_action_space_config.to_dict()).to_dict() == \
               example_action_space_config.to_dict()
        assert ActionSpaceConfig.from_dict(example_action_space_config.to_dict()) == example_action_space_config

    def test_agent_log(self, example_agent_log: AgentLog) -> None:
        """
        Tests creation and dict conversion of the AgentLog DAO

        :param example_agent_log: an example AgentLog
        :return: None
        """
        assert isinstance(example_agent_log.to_dict(), dict)
        assert isinstance(AgentLog.from_dict(example_agent_log.to_dict()), AgentLog)
        assert AgentLog.from_dict(example_agent_log.to_dict()).to_dict() == example_agent_log.to_dict()
        assert AgentLog.from_dict(example_agent_log.to_dict()) == example_agent_log

    def test_observation(self, example_observation: Observation) -> None:
        """
        Tests creation and dict conversion of the Observation DAO

        :param example_observation: an example Observation
        :return: None
        """
        assert isinstance(example_observation.to_dict(), dict)
        assert isinstance(Observation.from_dict(example_observation.to_dict()), Observation)
        assert Observation.from_dict(example_observation.to_dict()).to_dict() == example_observation.to_dict()
        assert Observation.from_dict(example_observation.to_dict()) == example_observation

    def test_env_parameter(self, example_env_parameter: EnvParameter) -> None:
        """
        Tests creation and dict conversion of the EnvParameter DAO

        :param example_env_parameter: an example EnvParameter
        :return: None
        """
        assert isinstance(example_env_parameter.to_dict(), dict)
        assert isinstance(EnvParameter.from_dict(example_env_parameter.to_dict()), EnvParameter)
        assert EnvParameter.from_dict(example_env_parameter.to_dict()).to_dict() == example_env_parameter.to_dict()
        assert EnvParameter.from_dict(example_env_parameter.to_dict()) == example_env_parameter

    def test_env_parameters_config(self, example_env_parameters_config: EnvParametersConfig) -> None:
        """
        Tests creation and dict conversion of the EnvParametersConfig DAO

        :param example_env_parameters_config: an example EnvParametersConfig
        :return: None
        """
        assert isinstance(example_env_parameters_config.to_dict(), dict)
        assert isinstance(EnvParametersConfig.from_dict(example_env_parameters_config.to_dict()), EnvParametersConfig)
        assert (EnvParametersConfig.from_dict(example_env_parameters_config.to_dict()).to_dict() ==
                example_env_parameters_config.to_dict())
        assert EnvParametersConfig.from_dict(example_env_parameters_config.to_dict()) == example_env_parameters_config

    def test_initial_state_distribution_config(
            self, example_initial_state_distribution_config: InitialStateDistributionConfig) -> None:
        """
        Tests creation and dict conversion of the InitialStateDistributionConfig DAO

        :param example_initial_state_distribution_config: an example InitialStateDistributionConfig
        :return: None
        """
        assert isinstance(example_initial_state_distribution_config.to_dict(), dict)
        assert isinstance(InitialStateDistributionConfig.from_dict(example_initial_state_distribution_config.to_dict()),
                          InitialStateDistributionConfig)
        assert (InitialStateDistributionConfig.from_dict(example_initial_state_distribution_config.to_dict()).to_dict()
                == example_initial_state_distribution_config.to_dict())
        assert (InitialStateDistributionConfig.from_dict(example_initial_state_distribution_config.to_dict()) ==
                example_initial_state_distribution_config)

    def test_joint_action_space_config(self, example_joint_action_space_config: JointActionSpaceConfig) -> None:
        """
        Tests creation and dict conversion of the JointActionSpaceConfig DAO

        :param example_joint_action_space_config: an example JointActionSpaceConfig
        :return: None
        """
        assert isinstance(example_joint_action_space_config.to_dict(), dict)
        assert isinstance(JointActionSpaceConfig.from_dict(example_joint_action_space_config.to_dict()),
                          JointActionSpaceConfig)
        assert (JointActionSpaceConfig.from_dict(example_joint_action_space_config.to_dict()).to_dict() ==
                example_joint_action_space_config.to_dict())
        assert (JointActionSpaceConfig.from_dict(example_joint_action_space_config.to_dict()) ==
                example_joint_action_space_config)

    def test_observation_space_config(self, example_observation_space_config: ObservationSpaceConfig) -> None:
        """
        Tests creation and dict conversion of the ObservationSpaceConfig DAO

        :param example_observation_space_config: an example ObservationSpaceConfig
        :return: None
        """
        assert isinstance(example_observation_space_config.to_dict(), dict)
        assert isinstance(ObservationSpaceConfig.from_dict(example_observation_space_config.to_dict()),
                          ObservationSpaceConfig)
        assert (ObservationSpaceConfig.from_dict(example_observation_space_config.to_dict()).to_dict() ==
                example_observation_space_config.to_dict())
        assert (ObservationSpaceConfig.from_dict(example_observation_space_config.to_dict()) ==
                example_observation_space_config)

    def test_joint_observation_space_config(
            self, example_joint_observation_space_config: JointObservationSpaceConfig) -> None:
        """
        Tests creation and dict conversion of the JointObservationSpaceConfig DAO

        :param example_joint_observation_space_config: an example JointObservationSpaceConfig
        :return: None
        """
        assert isinstance(example_joint_observation_space_config.to_dict(), dict)
        assert isinstance(JointObservationSpaceConfig.from_dict(example_joint_observation_space_config.to_dict()),
                          JointObservationSpaceConfig)
        assert (JointObservationSpaceConfig.from_dict(example_joint_observation_space_config.to_dict()).to_dict() ==
                example_joint_observation_space_config.to_dict())
        assert (JointObservationSpaceConfig.from_dict(example_joint_observation_space_config.to_dict()) ==
                example_joint_observation_space_config)

    def test_observation_function_config(self, example_observation_function_config: ObservationFunctionConfig) -> None:
        """
        Tests creation and dict conversion of the ObservationFunctionConfig DAO

        :param example_observation_function_config: an example ObservationFunctionConfig
        :return: None
        """
        assert isinstance(example_observation_function_config.to_dict(), dict)
        assert isinstance(ObservationFunctionConfig.from_dict(example_observation_function_config.to_dict()),
                          ObservationFunctionConfig)
        assert (ObservationFunctionConfig.from_dict(example_observation_function_config.to_dict()).to_dict() ==
                example_observation_function_config.to_dict())
        assert (ObservationFunctionConfig.from_dict(example_observation_function_config.to_dict()) ==
                example_observation_function_config)

    def test_player_config(self, example_player_config: PlayerConfig) -> None:
        """
        Tests creation and dict conversion of the PlayerConfig DAO

        :param example_player_config: an example PlayerConfig
        :return: None
        """
        assert isinstance(example_player_config.to_dict(), dict)
        assert isinstance(PlayerConfig.from_dict(example_player_config.to_dict()), PlayerConfig)
        assert PlayerConfig.from_dict(example_player_config.to_dict()).to_dict() == example_player_config.to_dict()
        assert PlayerConfig.from_dict(example_player_config.to_dict()) == example_player_config

    def test_players_config(self, example_players_config: PlayersConfig) -> None:
        """
        Tests creation and dict conversion of the PlayersConfig DAO

        :param example_players_config: an example PlayersConfig
        :return: None
        """
        assert isinstance(example_players_config.to_dict(), dict)
        assert isinstance(PlayersConfig.from_dict(example_players_config.to_dict()), PlayersConfig)
        assert PlayersConfig.from_dict(example_players_config.to_dict()).to_dict() == example_players_config.to_dict()
        assert PlayersConfig.from_dict(example_players_config.to_dict()) == example_players_config

    def test_reward_function_config(self, example_reward_function_config: RewardFunctionConfig) -> None:
        """
        Tests creation and dict conversion of the RewardFunctionConfig DAO

        :param example_reward_function_config: an example RewardFunctionConfig
        :return: None
        """
        assert isinstance(example_reward_function_config.to_dict(), dict)
        assert isinstance(RewardFunctionConfig.from_dict(example_reward_function_config.to_dict()),
                          RewardFunctionConfig)
        assert (RewardFunctionConfig.from_dict(example_reward_function_config.to_dict()).to_dict() ==
                example_reward_function_config.to_dict())
        assert RewardFunctionConfig.from_dict(example_reward_function_config.to_dict()) == \
               example_reward_function_config

    def test_simulation_env_input_config(self, example_input_config: ExampleInputConfig) -> None:
        """
        Tests creation and dict conversion of the SimulationEnvInputConfig DAO

        :param example_input_config: an example ExampleInputConfig
        :return: None
        """
        assert isinstance(example_input_config.to_dict(), dict)
        assert isinstance(ExampleInputConfig.from_dict(example_input_config.to_dict()),
                          ExampleInputConfig)
        assert (ExampleInputConfig.from_dict(example_input_config.to_dict()).to_dict() ==
                example_input_config.to_dict())
        assert ExampleInputConfig.from_dict(example_input_config.to_dict()) == example_input_config

    def test_simulation_trace(self, example_simulation_trace: SimulationTrace) -> None:
        """
        Tests creation and dict conversion of the SimulationTrace DAO

        :param example_simulation_trace: an example SimulationTrace
        :return: None
        """
        assert isinstance(example_simulation_trace.to_dict(), dict)
        assert isinstance(SimulationTrace.from_dict(example_simulation_trace.to_dict()), SimulationTrace)
        assert SimulationTrace.from_dict(example_simulation_trace.to_dict()).to_dict() == \
               example_simulation_trace.to_dict()
        assert SimulationTrace.from_dict(example_simulation_trace.to_dict()) == example_simulation_trace

    def test_state(self, example_state: State) -> None:
        """
        Tests creation and dict conversion of the State DAO

        :param example_state: an example State
        :return: None
        """
        assert isinstance(example_state.to_dict(), dict)
        assert isinstance(State.from_dict(example_state.to_dict()), State)
        assert State.from_dict(example_state.to_dict()).to_dict() == example_state.to_dict()
        assert State.from_dict(example_state.to_dict()) == example_state

    def test_state_space_config(self, example_state_space_config: StateSpaceConfig) -> None:
        """
        Tests creation and dict conversion of the StateSpaceConfig DAO

        :param example_state_space_config: an example StateSpaceConfig
        :return: None
        """
        assert isinstance(example_state_space_config.to_dict(), dict)
        assert isinstance(StateSpaceConfig.from_dict(example_state_space_config.to_dict()), StateSpaceConfig)
        assert StateSpaceConfig.from_dict(example_state_space_config.to_dict()).to_dict() == \
               example_state_space_config.to_dict()
        assert StateSpaceConfig.from_dict(example_state_space_config.to_dict()) == example_state_space_config

    def test_transition_operator_config(self, example_transition_operator_config: TransitionOperatorConfig) -> None:
        """
        Tests creation and dict conversion of the TransitionOperatorConfig DAO

        :param example_transition_operator_config: an example TransitionOperatorConfig
        :return: None
        """
        assert isinstance(example_transition_operator_config.to_dict(), dict)
        assert isinstance(TransitionOperatorConfig.from_dict(example_transition_operator_config.to_dict()),
                          TransitionOperatorConfig)
        assert (TransitionOperatorConfig.from_dict(example_transition_operator_config.to_dict()).to_dict() ==
                example_transition_operator_config.to_dict())
        assert (TransitionOperatorConfig.from_dict(example_transition_operator_config.to_dict()) ==
                example_transition_operator_config)

    def test_simulation_env_config(self, example_simulation_env_config: SimulationEnvConfig) -> None:
        """
        Tests creation and dict conversion of the SimulationEnvConfig DAO

        :param example_simulation_env_config: an example SimulationEnvConfig
        :return: None
        """
        assert isinstance(example_simulation_env_config.to_dict(), dict)
