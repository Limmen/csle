from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig


class TestCSLECyborgConfigSuite(object):
    """
    Test suite for csle_cyborg_config.py
    """

    def test_creation(self) -> None:
        """
        Tests the creation of a CSLECyborgConfig

        :return: None
        """
        config = CSLECyborgConfig(scenario=2, env_name="mytest")
        assert config.scenario == 2
        assert config.env_name == "mytest"
