from typing import Any, List
import pytest
import pytest_mock
from csle_collector.kafka_manager.kafka_manager_pb2 import KafkaDTO
from csle_collector.kafka_manager.kafka_manager import KafkaManagerServicer
from csle_collector.kafka_manager.kafka_manager_util import KafkaManagerUtil
import csle_collector.kafka_manager.query_kafka_server
import csle_collector.constants.constants as constants


class TestKafkaManagerSuite:
    """
    Test suite for kafka_manager.py
    """

    @pytest.fixture(scope='module')
    def grpc_add_to_server(self) -> Any:
        """
        Necessary fixture for pytest-grpc

        :return: the add_servicer_to_server function
        """
        from csle_collector.kafka_manager.kafka_manager_pb2_grpc import add_KafkaManagerServicer_to_server
        return add_KafkaManagerServicer_to_server

    @pytest.fixture(scope='module')
    def grpc_servicer(self) -> KafkaManagerServicer:
        """
        Necessary fixture for pytest-grpc

        :return: the kafka manager servicer
        """
        return KafkaManagerServicer()

    @pytest.fixture(scope='module')
    def grpc_stub_cls(self, grpc_channel):
        """
        Necessary fixture for pytest-grpc

        :param grpc_channel: the grpc channel for testing
        :return: the stub to the service
        """
        from csle_collector.kafka_manager.kafka_manager_pb2_grpc import KafkaManagerStub
        return KafkaManagerStub

    def test_getKafkaStatus(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the getKafkaStatus grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        running = True
        topics = ["topic1", "topic2"]
        mocker.patch('csle_collector.kafka_manager.kafka_manager.KafkaManagerServicer._get_kafka_status_and_topics',
                     return_value=(running, topics))
        response: KafkaDTO = csle_collector.kafka_manager.query_kafka_server.get_kafka_status(stub=grpc_stub)
        assert response.running == running
        assert response.topics == topics

    def test_stopKafka(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopKafka grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        running = False
        topics: List[str] = []
        mocker.patch('os.system', return_value=True)
        response: KafkaDTO = csle_collector.kafka_manager.query_kafka_server.stop_kafka(stub=grpc_stub)
        assert response.running == running
        assert response.topics == topics

    def test_startKafka(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startKafka grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        running = True
        topics: List[str] = []
        mocker.patch('os.system', return_value=True)
        response: KafkaDTO = csle_collector.kafka_manager.query_kafka_server.start_kafka(stub=grpc_stub)
        assert response.running == running
        assert response.topics == topics

    def test_hours_to_ms(self) -> None:
        """
        Tests the hours_to_ms function

        :return: None
        """
        assert KafkaManagerUtil.hours_to_ms(1 / (60 * 60)) == 1000
        assert KafkaManagerUtil.hours_to_ms(1 / (60)) == 60000
        assert KafkaManagerUtil.hours_to_ms(1) == 3.6e6

    def test_kafka_dto_empty(self) -> None:
        """
        Tests the kafka_dto_empty function

        :return: None
        """
        dto: KafkaDTO = KafkaManagerUtil.kafka_dto_empty()
        assert not dto.running
        assert dto.topics == []

    def test_kafka_dto_from_dict(self) -> None:
        """
        Tests the kafka_dto_from_dict function

        :return: None
        """
        dicts = [{constants.DICT_PROPERTIES.RUNNING: True, constants.DICT_PROPERTIES.TOPICS: ["topic1", "topic2"]},
                 {constants.DICT_PROPERTIES.RUNNING: False, constants.DICT_PROPERTIES.TOPICS: []},
                 {constants.DICT_PROPERTIES.RUNNING: False, constants.DICT_PROPERTIES.TOPICS: ["topic3"]}]
        for d in dicts:
            dto: KafkaDTO = KafkaManagerUtil.kafka_dto_from_dict(d=d)
            assert dto.running == d[constants.DICT_PROPERTIES.RUNNING]
            assert dto.topics == d[constants.DICT_PROPERTIES.TOPICS]

    def test_kafka_dto_to_dict(self) -> None:
        """
        Tests the kafka_dto_to_dict function

        :return: None
        """
        dtos = [KafkaDTO(running=True, topics=["topic1", "topic2"]), KafkaDTO(running=False, topics=[]),
                KafkaDTO(running=True, topics=["topic3"])]
        for dto in dtos:
            d = KafkaManagerUtil.kafka_dto_to_dict(kafka_dto=dto)
            assert dto.running == d[constants.DICT_PROPERTIES.RUNNING]
            assert dto.topics == d[constants.DICT_PROPERTIES.TOPICS]
