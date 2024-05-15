from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType


class TestCSLECyborgConfigSuite:
    """
    Test suite for csle_cyborg_config.py
    """

    def test_creation(self) -> None:
        """
        Tests the creation of a CSLECyborgConfig

        :return: None
        """
        config = CSLECyborgConfig(scenario=2, gym_env_name="mytest", maximum_steps=100,
                                  baseline_red_agents=[RedAgentType.B_LINE_AGENT], red_agent_distribution=[1.0],
                                  reduced_action_space=False, scanned_state=False, decoy_state=False,
                                  decoy_optimization=False)
        assert config.scenario == 2
        assert config.gym_env_name == "mytest"
        assert config.maximum_steps == 100
        assert config.baseline_red_agents == [RedAgentType.B_LINE_AGENT]
        assert config.red_agent_distribution == [1.0]
        assert not config.reduced_action_space
        assert not config.scanned_state
        assert not config.decoy_state
        assert not config.decoy_optimization
