from unittest.mock import MagicMock
from csle_common.consumer_threads.aggregated_ossec_ids_log_consumer_thread import AggregatedOSSECIdsLogConsumerThread


class TestSuiteAggregatedOSSECIdsLogConsumerThread:
    """
    Test suite for AggregatedOSSECIdsLogConsumerThread
    """

    def test_initialization(self) -> None:
        """
        Initializes the test

        :return: None
        """
        kafka_server_ip = "127.0.0.1"
        kafka_port = 9092
        alert_counters = MagicMock()
        auto_offset_reset = "earliest"

        thread = AggregatedOSSECIdsLogConsumerThread(
            kafka_server_ip=kafka_server_ip,
            kafka_port=kafka_port,
            ossec_ids_alert_counters=alert_counters,
            auto_offset_reset=auto_offset_reset,
        )
        assert thread.running
        assert thread.kafka_server_ip == kafka_server_ip
        assert thread.kafka_port == kafka_port
        assert thread.ossec_ids_alert_counters == alert_counters

    def test_get_aggregated_ids_alert_counters(self) -> None:
        """
        Test the method that returns the aggregated alert counters from the list

        :return: None
        """
        mock_alert_counters_1 = MagicMock()
        mock_alert_counters_2 = MagicMock()
        mock_alert_counters_1.copy.return_value = mock_alert_counters_1
        mock_alert_counters_2.copy.return_value = mock_alert_counters_2
        mock_alert_counters_1.add = MagicMock()
        kafka_server_ip = "127.0.0.1"
        kafka_port = 9092
        alert_counters = MagicMock()
        auto_offset_reset = "earliest"
        thread = AggregatedOSSECIdsLogConsumerThread(
            kafka_server_ip=kafka_server_ip,
            kafka_port=kafka_port,
            ossec_ids_alert_counters=alert_counters,
            auto_offset_reset=auto_offset_reset,
        )
        thread.ossec_ids_alert_counters_list = []
        thread.ossec_ids_alert_counters = mock_alert_counters_1

        result = thread.get_aggregated_ids_alert_counters()
        assert result == mock_alert_counters_1.copy.return_value
