from csle_collector.client_manager.dao.constant_arrival_config import ConstantArrivalConfig
from csle_collector.client_manager.dao.sine_arrival_config import SineArrivalConfig
from csle_collector.client_manager.dao.client import Client
from csle_collector.client_manager.dao.eptmp_arrival_config import EPTMPArrivalConfig
from csle_collector.client_manager.dao.piece_wise_constant_arrival_config import PieceWiseConstantArrivalConfig
from csle_collector.client_manager.dao.spiking_arrival_config import SpikingArrivalConfig
from csle_collector.client_manager.dao.workflow_markov_chain import WorkflowMarkovChain
from csle_collector.client_manager.dao.workflow_service import WorkflowService
from csle_collector.client_manager.dao.workflows_config import WorkflowsConfig


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

    def test_client(self, example_client: Client) -> None:
        """
        Tests creation and dict conversion of the Client DAO

        :param example_client: an example Client
        :return: None
        """
        assert isinstance(example_client.to_dict(), dict)
        assert isinstance(Client.from_dict(example_client.to_dict()), Client)
        assert (Client.from_dict(example_client.to_dict()).to_dict() == example_client.to_dict())
        assert (Client.from_dict(example_client.to_dict()) == example_client)

    def test_eptmp(self, example_eptmp_arrival_config: EPTMPArrivalConfig) -> None:
        """
        Tests creation and dict conversion of the EPTMPArrivalConfig DAO

        :param example_eptmp_arrival_config: an example EPTMPArrivalConfig
        :return: None
        """
        assert isinstance(example_eptmp_arrival_config.to_dict(), dict)
        assert isinstance(EPTMPArrivalConfig.from_dict(example_eptmp_arrival_config.to_dict()), EPTMPArrivalConfig)
        assert (EPTMPArrivalConfig.from_dict(example_eptmp_arrival_config.to_dict()).to_dict() ==
                example_eptmp_arrival_config.to_dict())
        assert (EPTMPArrivalConfig.from_dict(example_eptmp_arrival_config.to_dict()) == example_eptmp_arrival_config)

    def test_piece_wise_constant_arrival_config(
            self, example_piece_wise_constant_arrival_config: PieceWiseConstantArrivalConfig) -> None:
        """
        Tests creation and dict conversion of the PieceWiseConstantArrivalConfig DAO

        :param example_piece_wise_constant_arrival_config: an example PieceWiseConstantArrivalConfig
        :return: None
        """
        assert isinstance(example_piece_wise_constant_arrival_config.to_dict(), dict)
        assert isinstance(PieceWiseConstantArrivalConfig.from_dict(
            example_piece_wise_constant_arrival_config.to_dict()), PieceWiseConstantArrivalConfig)
        assert (PieceWiseConstantArrivalConfig.from_dict(
            example_piece_wise_constant_arrival_config.to_dict()).to_dict()
            == example_piece_wise_constant_arrival_config.to_dict())
        assert (PieceWiseConstantArrivalConfig.from_dict(example_piece_wise_constant_arrival_config.to_dict())
                == example_piece_wise_constant_arrival_config)

    def test_example_spiking_arrival_config(
            self, example_spiking_arrival_config: SpikingArrivalConfig) -> None:
        """
        Tests creation and dict conversion of the SpikingArrivalConfig DAO

        :param example_spiking_arrival_config: an example SpikingArrivalConfig
        :return: None
        """
        assert isinstance(example_spiking_arrival_config.to_dict(), dict)
        assert isinstance(SpikingArrivalConfig.from_dict(example_spiking_arrival_config.to_dict()),
                          SpikingArrivalConfig)
        assert (SpikingArrivalConfig.from_dict(example_spiking_arrival_config.to_dict()).to_dict()
                == example_spiking_arrival_config.to_dict())
        assert (SpikingArrivalConfig.from_dict(example_spiking_arrival_config.to_dict())
                == example_spiking_arrival_config)

    def test_example_workflow_markov_chain(
            self, example_workflow_markov_chain: WorkflowMarkovChain) -> None:
        """
        Tests creation and dict conversion of the WorkflowMarkovChain DAO

        :param example_workflow_markov_chain: an example WorkflowMarkovChain
        :return: None
        """
        assert isinstance(example_workflow_markov_chain.to_dict(), dict)
        assert isinstance(WorkflowMarkovChain.from_dict(example_workflow_markov_chain.to_dict()),
                          WorkflowMarkovChain)
        assert (WorkflowMarkovChain.from_dict(example_workflow_markov_chain.to_dict()).to_dict()
                == example_workflow_markov_chain.to_dict())
        assert (WorkflowMarkovChain.from_dict(example_workflow_markov_chain.to_dict())
                == example_workflow_markov_chain)

    def test_example_workflow_service(self, example_workflow_service: WorkflowService) -> None:
        """
        Tests creation and dict conversion of the WorkflowService DAO

        :param example_workflow_service: an example WorkflowService
        :return: None
        """
        assert isinstance(example_workflow_service.to_dict(), dict)
        assert isinstance(WorkflowService.from_dict(example_workflow_service.to_dict()), WorkflowService)
        assert (WorkflowService.from_dict(example_workflow_service.to_dict()).to_dict()
                == example_workflow_service.to_dict())
        assert (WorkflowService.from_dict(example_workflow_service.to_dict()) == example_workflow_service)

    def test_example_workflow_config(self, example_workflow_config: WorkflowsConfig) -> None:
        """
        Tests creation and dict conversion of the WorkflowsConfig DAO

        :param example_workflow_config: an example WorkflowsConfig
        :return: None
        """
        assert isinstance(example_workflow_config.to_dict(), dict)
        assert isinstance(WorkflowsConfig.from_dict(example_workflow_config.to_dict()), WorkflowsConfig)
        assert (WorkflowsConfig.from_dict(example_workflow_config.to_dict()).to_dict()
                == example_workflow_config.to_dict())
        assert (WorkflowsConfig.from_dict(example_workflow_config.to_dict()) == example_workflow_config)
