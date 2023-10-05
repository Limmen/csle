import pytest
from csle_collector.client_manager.dao.constant_arrival_config import ConstantArrivalConfig
from csle_collector.client_manager.dao.sine_arrival_config import SineArrivalConfig


@pytest.fixture
def example_constant_arrival_config() -> ConstantArrivalConfig:
    """
    Fixture that returns an example ConstantArrivalConfig object

    :return: an example ConstantArrivalConfig object
    """
    return ConstantArrivalConfig(lamb=10)


@pytest.fixture
def example_sine_arrival_config() -> SineArrivalConfig:
    """
    Fixture that returns an example SineArrivalConfig object

    :return: an example SineArrival object
    """
    return SineArrivalConfig(lamb = 0.5, time_scaling_factor=1.0, period_scaling_factor=5.0)