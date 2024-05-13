from config_v_001 import default_config


class TestSimulationConfigSuite:
    """
    Test suite for the simulation configuration for 'apt_game'
    """

    def test_create_config(self) -> None:
        """
        Tests creation of the simulation configuration

        :return: None
        """
        config = default_config(name="csle-apt-game-001", version="0.0.1", N=5, p_a=0.1, num_observations=10)
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
