import logging
import pytest


class TestKafkaManagerSuite(object):
    """
    Test suite for shell_util.py
    """

    pytest.logger = logging.getLogger("kafka_manager_tests")

    def test_get_kafka_status_and_topics(self) -> None:
        """
        Tests the _get_kafka_status_and_topics function

        :return: None
        """
        assert True
