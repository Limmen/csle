from csle_collector.client_manager.dao.constant_arrival_config import ConstantArrivalConfig
from csle_collector.client_manager.dao.sine_arrival_config import SineArrivalConfig


class TestClientManagerDaoSuite:
    """
    Test suite for datasets data access objects (DAOs) in client_manager
    """

    def test_constant_arrival_config(self, example_constant_arrival_config: ConstantArrivalConfig) -> None:
        """
        Tests creation and dict conversion of the ConstantArrivalConfig DAO

        :param example_constant_arrival_config: an example ConstantArrivalConfig
        :return: None
        """
        assert isinstance(example_constant_arrival_config.to_dict(), dict)
        assert isinstance(ConstantArrivalConfig.from_dict(example_constant_arrival_config.to_dict()),
                          ConstantArrivalConfig)
        assert (ConstantArrivalConfig.from_dict(example_constant_arrival_config.to_dict()).to_dict()
                == example_constant_arrival_config.to_dict())
        assert (ConstantArrivalConfig.from_dict(example_constant_arrival_config.to_dict())
                == example_constant_arrival_config)


    def test_since_arrival_config(self, example_sine_arrival_config: SineArrivalConfig) -> None:
        """
        Tests creation and dict conversion of the SineArrivalConfig DAO

        :param example_constant_arrival_config: an example SineArrivalConfig
        :return: None
        """
        assert isinstance(example_sine_arrival_config.to_dict(), dict)
        assert isinstance(SineArrivalConfig.from_dict(example_sine_arrival_config.to_dict()),
                          SineArrivalConfig)
        assert (SineArrivalConfig.from_dict(example_sine_arrival_config.to_dict()).to_dict()
                == example_sine_arrival_config.to_dict())
        assert (SineArrivalConfig.from_dict(example_sine_arrival_config.to_dict())
                == example_sine_arrival_config)
