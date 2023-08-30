import numpy

from csle_common.dao.simulation_config.action import Action
from csle_common.dao.simulation_config.action_space_config import ActionSpaceConfig
from csle_common.dao.simulation_config.value_type import ValueType
from csle_common.dao.simulation_config.agent_log import AgentLog
from csle_common.dao.simulation_config.env_parameter import EnvParameter
from csle_common.dao.simulation_config.env_parameters_config import EnvParametersConfig
from csle_common.dao.simulation_config.initial_state_distribution_config import InitialStateDistributionConfig
from csle_common.dao.simulation_config.joint_action_space_config import JointActionSpaceConfig
from csle_common.dao.simulation_config.joint_observation_space_config import JointObservationSpaceConfig
from csle_common.dao.simulation_config.observation_space_config import ObservationSpaceConfig
from csle_common.dao.simulation_config.observation import Observation
from csle_common.dao.simulation_config.observation_function_config import ObservationFunctionConfig


class TestSimulationConfigDaoSuite:
    """
    Test suite for simulation config data access objects (DAOs)
    """

    def test_action(self) -> None:
        """
        Tests creation and dict conversion of the Action DAO

        :return: None
        """

        action = Action(id=1, descr="test")

        assert isinstance(action.to_dict(), dict)
        assert isinstance(Action.from_dict(action.to_dict()),
                          Action)
        assert (Action.from_dict(action.to_dict()).to_dict() ==
                action.to_dict())
        assert (Action.from_dict(action.to_dict()) ==
                action)

    def test_action_space_config(self) -> None:
        """
        Tests creation and dict conversion of the ActionSpaceConfig DAO

        :return: None
        """

        action_space_config = ActionSpaceConfig(actions=[Action(id=1, descr="test")],
                                                player_id=1, action_type=ValueType.INTEGER)

        assert isinstance(action_space_config.to_dict(), dict)
        assert isinstance(ActionSpaceConfig.from_dict(action_space_config.to_dict()),
                          ActionSpaceConfig)
        assert (ActionSpaceConfig.from_dict(action_space_config.to_dict()).to_dict() ==
                action_space_config.to_dict())
        assert (ActionSpaceConfig.from_dict(action_space_config.to_dict()) ==
                action_space_config)

    def test_agent_log(self) -> None:
        """
        Tests creation and dict conversion of the AgentLog DAO

        :return: None
        """

        agent_log = AgentLog()

        assert isinstance(agent_log.to_dict(), dict)
        assert isinstance(AgentLog.from_dict(agent_log.to_dict()),
                          AgentLog)
        assert (AgentLog.from_dict(agent_log.to_dict()).to_dict() ==
                agent_log.to_dict())
        assert (AgentLog.from_dict(agent_log.to_dict()) ==
                agent_log)

    def test_env_parameter(self) -> None:
        """
        Tests creation and dict conversion of the EnvParameter DAO

        :return: None
        """

        env_parameter = EnvParameter(id=1, name="test", descr="test1")

        assert isinstance(env_parameter.to_dict(), dict)
        assert isinstance(EnvParameter.from_dict(env_parameter.to_dict()),
                          EnvParameter)
        assert (EnvParameter.from_dict(env_parameter.to_dict()).to_dict() ==
                env_parameter.to_dict())
        assert (EnvParameter.from_dict(env_parameter.to_dict()) ==
                env_parameter)

    def test_env_parameters_config(self) -> None:
        """
        Tests creation and dict conversion of the EnvParametersConfig DAO

        :return: None
        """

        env_parameters_config = EnvParametersConfig(parameters=[EnvParameter(id=1, name="test", descr="test1")])

        assert isinstance(env_parameters_config.to_dict(), dict)
        assert isinstance(EnvParametersConfig.from_dict(env_parameters_config.to_dict()),
                          EnvParametersConfig)
        assert (EnvParametersConfig.from_dict(env_parameters_config.to_dict()).to_dict() ==
                env_parameters_config.to_dict())
        assert (EnvParametersConfig.from_dict(env_parameters_config.to_dict()) ==
                env_parameters_config)

    def test_initial_state_distribution_config(self) -> None:
        """
        Tests creation and dict conversion of the InitialStateDistributionConfig DAO

        :return: None
        """

        initial_state_distribution_config = InitialStateDistributionConfig(initial_state_distribution=[0.1, 0.9])

        assert isinstance(initial_state_distribution_config.to_dict(), dict)
        assert isinstance(InitialStateDistributionConfig.from_dict(initial_state_distribution_config.to_dict()),
                          InitialStateDistributionConfig)
        assert (InitialStateDistributionConfig.from_dict(initial_state_distribution_config.to_dict()).to_dict() ==
                initial_state_distribution_config.to_dict())
        assert (InitialStateDistributionConfig.from_dict(initial_state_distribution_config.to_dict()) ==
                initial_state_distribution_config)

    def test_joint_action_space_config(self) -> None:
        """
        Tests creation and dict conversion of the JointActionSpaceConfig DAO

        :return: None
        """
        
        joint_action_space_config = JointActionSpaceConfig(
            action_spaces=[ActionSpaceConfig(actions=[Action(id=1, descr="test")], player_id=1,
                                             action_type=ValueType.INTEGER)])

        assert isinstance(joint_action_space_config.to_dict(), dict)
        assert isinstance(JointActionSpaceConfig.from_dict(joint_action_space_config.to_dict()),
                          JointActionSpaceConfig)
        assert (JointActionSpaceConfig.from_dict(joint_action_space_config.to_dict()).to_dict() ==
                joint_action_space_config.to_dict())
        assert (JointActionSpaceConfig.from_dict(joint_action_space_config.to_dict()) ==
                joint_action_space_config)

    def test_joint_observation_space_config(self) -> None:
        """
        Tests creation and dict conversion of the JointObservationSpaceConfig DAO

        :return: None
        """

        observation = Observation(id=1, val=2, descr="test")
        observation_component_name_to_index = dict()
        observation_component_name_to_index["test"] = 1
        observation_id_to_observation_id_vector = dict()
        observation_id_to_observation_id_vector[0] = [1, 2, 3]
        observation_id_to_observation_vector = dict()
        observation_id_to_observation_vector[4] = [4, 5, 6]
        component_observations = dict()
        component_observations["test1"] = [observation]
        observation_space_config = ObservationSpaceConfig(
            observations=[observation], observation_type=ValueType.INTEGER, descr="test", player_id=2,
            observation_component_name_to_index=observation_component_name_to_index,
            observation_id_to_observation_id_vector=observation_id_to_observation_id_vector,
            observation_id_to_observation_vector=observation_id_to_observation_vector,
            component_observations=component_observations)

        joint_observation_space_config = JointObservationSpaceConfig(observation_spaces=[observation_space_config])

        assert isinstance(joint_observation_space_config.to_dict(), dict)
        assert isinstance(JointObservationSpaceConfig.from_dict(joint_observation_space_config.to_dict()),
                          JointObservationSpaceConfig)
        assert (JointObservationSpaceConfig.from_dict(joint_observation_space_config.to_dict()).to_dict() ==
                joint_observation_space_config.to_dict())
        assert (JointObservationSpaceConfig.from_dict(joint_observation_space_config.to_dict()) ==
                joint_observation_space_config)

    def test_observation(self) -> None:
        """
        Tests creation and dict conversion of the Observation DAO

        :return: None
        """

        observation = Observation(id=1, val=2, descr="test")

        assert isinstance(observation.to_dict(), dict)
        assert isinstance(Observation.from_dict(observation.to_dict()),
                          Observation)
        assert (Observation.from_dict(observation.to_dict()).to_dict() ==
                observation.to_dict())
        assert (Observation.from_dict(observation.to_dict()) ==
                observation)

    def test_observation_function_config(self) -> None:
        """
        Tests creation and dict conversion of the ObservationFunctionConfig DAO

        :return: None
        """

        observation_tensor = numpy.array([1, 2, 3])
        component_observation_tensors = dict()
        component_observation_tensors["test"] = numpy.array([1, 2, 3])
        observation_function_config = ObservationFunctionConfig(
            observation_tensor=observation_tensor, component_observation_tensors=component_observation_tensors)

        assert isinstance(observation_function_config.to_dict(), dict)
        assert isinstance(ObservationFunctionConfig.from_dict(observation_function_config.to_dict()),
                          ObservationFunctionConfig)
        assert (ObservationFunctionConfig.from_dict(observation_function_config.to_dict()).to_dict() ==
                observation_function_config.to_dict())
        assert (ObservationFunctionConfig.from_dict(observation_function_config.to_dict()) ==
                observation_function_config)

    def test_observation_space_config(self) -> None:
        """
        Tests creation and dict conversion of the ObservationSpaceConfig DAO

        :return: None
        """

        observation = Observation(id=1, val=2, descr="test")
        observation_component_name_to_index = dict()
        observation_component_name_to_index["test"] = 1
        observation_id_to_observation_id_vector = dict()
        observation_id_to_observation_id_vector[0] = [1, 2, 3]
        observation_id_to_observation_vector = dict()
        observation_id_to_observation_vector[4] = [4, 5, 6]
        component_observations = dict()
        component_observations["test1"] = [observation]
        observation_space_config = ObservationSpaceConfig(
            observations=[observation], observation_type=ValueType.INTEGER, descr="test", player_id=2,
            observation_component_name_to_index=observation_component_name_to_index,
            observation_id_to_observation_id_vector=observation_id_to_observation_id_vector,
            observation_id_to_observation_vector=observation_id_to_observation_vector,
            component_observations=component_observations
        )

        assert isinstance(observation_space_config.to_dict(), dict)
        assert isinstance(ObservationSpaceConfig.from_dict(observation_space_config.to_dict()),
                          ObservationSpaceConfig)
        assert (ObservationSpaceConfig.from_dict(observation_space_config.to_dict()).to_dict() ==
                observation_space_config.to_dict())
        assert (ObservationSpaceConfig.from_dict(observation_space_config.to_dict()) ==
                observation_space_config)
