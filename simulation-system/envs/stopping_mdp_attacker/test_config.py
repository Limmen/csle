from config_v_001 import default_config as default_config_v_001
from config_v_002 import default_config as default_config_v_002
from config_v_003 import default_config as default_config_v_003


class TestSimulationConfigSuite:
    """
    Test suite for the simulation configuration for 'stopping-mdp-attacker'
    """

    def test_create_config_v001(self) -> None:
        """
        Tests creation of the simulation configuration

        :return: None
        """
        config = default_config_v_001(name="csle-stopping-mdp-attacker-001", version="0.0.1")
        assert config.players_config is not None
        assert config.state_space_config is not None
        assert config.joint_action_space_config is not None
        assert config.joint_observation_space_config is not None
        assert config.transition_operator_config is not None
        assert config.observation_function_config is not None
        assert config.reward_function_config is not None
        assert config.initial_state_distribution_config is not None
        assert config.env_parameters_config is not None
        assert config.simulation_env_input_config is not None
        assert config.gym_env_name is not None
        assert config.plot_transition_probabilities is not None
        assert config.plot_observation_function is not None
        assert config.plot_reward_function is not None

    def test_create_config_v002(self) -> None:
        """
        Tests creation of the simulation configuration

        :return: None
        """
        config = default_config_v_002(name="csle-stopping-mdp-attacker-002", version="0.0.2")
        assert config.players_config is not None
        assert config.state_space_config is not None
        assert config.joint_action_space_config is not None
        assert config.joint_observation_space_config is not None
        assert config.transition_operator_config is not None
        assert config.observation_function_config is not None
        assert config.reward_function_config is not None
        assert config.initial_state_distribution_config is not None
        assert config.env_parameters_config is not None
        assert config.simulation_env_input_config is not None
        assert config.gym_env_name is not None
        assert config.plot_transition_probabilities is not None
        assert config.plot_observation_function is not None
        assert config.plot_reward_function is not None

    def test_create_config_v003(self) -> None:
        """
        Tests creation of the simulation configuration

        :return: None
        """
        config = default_config_v_003(name="csle-stopping-mdp-attacker-003", version="0.0.3")
        assert config.players_config is not None
        assert config.state_space_config is not None
        assert config.joint_action_space_config is not None
        assert config.joint_observation_space_config is not None
        assert config.transition_operator_config is not None
        assert config.observation_function_config is not None
        assert config.reward_function_config is not None
        assert config.initial_state_distribution_config is not None
        assert config.env_parameters_config is not None
        assert config.simulation_env_input_config is not None
        assert config.gym_env_name is not None
        assert config.plot_transition_probabilities is not None
        assert config.plot_observation_function is not None
        assert config.plot_reward_function is not None
