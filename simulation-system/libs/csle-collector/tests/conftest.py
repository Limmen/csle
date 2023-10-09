import pytest
from csle_collector.client_manager.dao.constant_arrival_config import ConstantArrivalConfig
from csle_collector.client_manager.dao.sine_arrival_config import SineArrivalConfig
from csle_collector.client_manager.dao.client import Client
from csle_collector.client_manager.dao.eptmp_arrival_config import EPTMPArrivalConfig
from csle_collector.client_manager.dao.piece_wise_constant_arrival_config import PieceWiseConstantArrivalConfig
from csle_collector.client_manager.dao.spiking_arrival_config import SpikingArrivalConfig
from csle_collector.client_manager.dao.workflow_markov_chain import WorkflowMarkovChain
from csle_collector.client_manager.dao.workflow_service import WorkflowService
from csle_collector.client_manager.dao.workflows_config import WorkflowsConfig


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
    return SineArrivalConfig(lamb=0.5, time_scaling_factor=1.0, period_scaling_factor=5.0)


@pytest.fixture
def example_client(example_constant_arrival_config: ConstantArrivalConfig) -> Client:
    """
    Fixture that returns an example Client object

    :return: an example Client object
    """
    return Client(id=1, workflow_distribution=[0.8, 0.2], arrival_config=example_constant_arrival_config)


@pytest.fixture
def example_eptmp_arrival_config() -> EPTMPArrivalConfig:
    """
    Fixture that returns an example EPTMPArrivalConfig object

    :return: an example EPTMPArrivalConfig object
    """
    return EPTMPArrivalConfig(thetas=[0.1, 0.4], gammas=[0.3, 0.6], phis=[0.7], omegas=[0.4, 0.2])


@pytest.fixture
def example_piece_wise_constant_arrival_config() -> PieceWiseConstantArrivalConfig:
    """
    Fixture that returns an example PieceWiseConstantArrivalConfig object

    :return: an example PieceWiseConstantArrivalConfig object
    """
    return PieceWiseConstantArrivalConfig(breakvalues=[1.4, 0.2], breakpoints=[2, 5])


@pytest.fixture
def example_spiking_arrival_config() -> SpikingArrivalConfig:
    """
    Fixture that returns an example SpikingArrivalConfig object

    :return: an example SpikingArrivalConfig object
    """
    return SpikingArrivalConfig(exponents=[0.3, 0.2], factors=[0.4, 0.2])


@pytest.fixture
def example_workflow_markov_chain() -> WorkflowMarkovChain:
    """
    Fixture that returns an example WorkflowMarkovChain object

    :return: an example WorkflowMarkovChain object
    """
    return WorkflowMarkovChain(transition_matrix=[[0.1, 0.9], [0.4, 0.6]], initial_state=5, id=2)


@pytest.fixture
def example_workflow_service() -> WorkflowService:
    """
    Fixture that returns an example WorkflowService object

    :return: an example WorkflowService object
    """
    return WorkflowService(ips_and_commands=[("1.2.2.1", ["command1", "command2"])], id=2)


@pytest.fixture
def example_workflow_config(example_workflow_markov_chain: WorkflowMarkovChain,
                            example_workflow_service: WorkflowService) -> WorkflowsConfig:
    """
    Fixture that returns an example WorkflowsConfig object

    :return: an example WorkflowsConfig object
    """
    return WorkflowsConfig(workflow_markov_chains=[example_workflow_markov_chain],
                           workflow_services=[example_workflow_service])
