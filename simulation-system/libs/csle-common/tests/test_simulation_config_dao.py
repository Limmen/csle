from csle_common.dao.simulation_config.action import Action
from csle_common.dao.simulation_config.action_space_config import ActionSpaceConfig
from csle_common.dao.simulation_config.value_type import ValueType
from csle_common.dao.simulation_config.agent_log import AgentLog
from csle_common.dao.simulation_config.env_parameter import EnvParameter
from csle_common.dao.simulation_config.env_parameters_config import EnvParametersConfig
from csle_common.dao.simulation_config.initial_state_distribution_config import InitialStateDistributionConfig
from csle_common.dao.simulation_config.joint_action_space_config import JointActionSpaceConfig


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
