from unittest.mock import MagicMock, patch
from csle_common.util.read_emulation_statistics_util import ReadEmulationStatisticsUtil
from confluent_kafka import TopicPartition
from csle_collector.host_manager.dao.host_metrics import HostMetrics
from csle_collector.ossec_ids_manager.dao.ossec_ids_alert_counters import OSSECIdsAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_alert_counters import SnortIdsAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_rule_counters import SnortIdsRuleCounters
import csle_collector.constants.constants as constants
import numpy as np


class TestReadEmulationUtilSuite:
    """
    Test suite for read_emulation_util
    """

    @patch("confluent_kafka.Consumer")
    def test_read_all(self, mock_consumer):
        """


        :param mock_consumer: _description_
        :type mock_consumer: _type_
        """

        mock_env_config = MagicMock()

        class MockContainer:
            def __init__(self, name):
                self.name = name

            def get_full_name(self):
                return self.name

            def get_ips(self):
                return ["127.0.0.1"]

        mock_env_config.containers_config.containers = [
            MockContainer("snort"),
            MockContainer("ossec"),
            MockContainer("kafka"),
            MockContainer("elk"),
        ]

        mock_env_config.kafka_config.container.get_full_name.return_value = "kafka"
        mock_env_config.kafka_config.container.docker_gw_bridge_ip = "127.0.0.1"
        mock_env_config.kafka_config.kafka_port_external = 9092
        mock_env_config.elk_config.container.get_full_name.return_value = "elk"
        mock_env_config.sdn_controller_config = None

        instance = mock_consumer.return_value
        mock_topic_partitions = [MagicMock(TopicPartition) for _ in range(3)]
        instance.offsets_for_times.return_value = mock_topic_partitions
        instance.poll.side_effect = [
            MagicMock(value=lambda: b'{"ip": "127.0.0.1"}', topic=lambda: "host_metrics"),
            None,
        ]
        instance.offsets_for_times.return_value = []
        instance.subscribe.side_effect = lambda topics, on_assign: on_assign(instance, [])
        instance.close.return_value = None

        pass
        # result = ReadEmulationStatisticsUtil.read_all(emulation_env_config=mock_env_config,logger=logger)

        # assert instance.subscribe.call_count == 1

    def test_average_host_metrics(self) -> None:
        """
        Test the method that computes the average metrics from a list of host metrics

        :return: None
        """
        metrics1 = HostMetrics(
            num_logged_in_users=5,
            num_failed_login_attempts=2,
            num_open_connections=10,
            num_login_events=3,
            num_processes=50,
            num_users=5,
        )
        metrics2 = HostMetrics(
            num_logged_in_users=7,
            num_failed_login_attempts=4,
            num_open_connections=14,
            num_login_events=5,
            num_processes=60,
            num_users=6,
        )

        metrics3 = HostMetrics(
            num_logged_in_users=6,
            num_failed_login_attempts=3,
            num_open_connections=12,
            num_login_events=4,
            num_processes=55,
            num_users=7,
        )

        average_metrics = ReadEmulationStatisticsUtil.average_host_metrics([metrics1, metrics2, metrics3])

        assert average_metrics.num_logged_in_users == 18
        assert average_metrics.num_failed_login_attempts == 9
        assert average_metrics.num_open_connections == 36
        assert average_metrics.num_login_events == 12
        assert average_metrics.num_processes == 165
        assert average_metrics.num_users == 18

    def test_average_ossec_metrics(self) -> None:
        """
        Test the method that computes the average metrics from a list of OSSEC metrics

        :return: None
        """
        metrics1 = OSSECIdsAlertCounters()
        metrics1.level_alerts = list(np.zeros(16))
        metrics1.group_alerts = list(np.zeros(len(set(constants.OSSEC.OSSEC_IDS_ALERT_GROUP_ID.values()))))
        metrics1.severe_alerts = 5
        metrics1.warning_alerts = 3
        metrics1.total_alerts = 10
        metrics1.alerts_weighted_by_level = 20

        metrics2 = OSSECIdsAlertCounters()
        metrics2.level_alerts = list(np.zeros(16))
        metrics2.group_alerts = list(np.zeros(len(set(constants.OSSEC.OSSEC_IDS_ALERT_GROUP_ID.values()))))
        metrics2.severe_alerts = 10
        metrics2.warning_alerts = 6
        metrics2.total_alerts = 20
        metrics2.alerts_weighted_by_level = 40

        average_metrics = ReadEmulationStatisticsUtil.average_ossec_metrics([metrics1, metrics2])

        assert average_metrics.level_alerts == [0] * 16
        assert average_metrics.group_alerts == [0] * len(set(constants.OSSEC.OSSEC_IDS_ALERT_GROUP_ID.values()))
        assert average_metrics.severe_alerts == 15
        assert average_metrics.warning_alerts == 9
        assert average_metrics.total_alerts == 30
        assert average_metrics.alerts_weighted_by_level == 60

    def test_average_snort_metrics(self) -> None:
        """
        Test the method that computes the average metrics from a list of Snort metrics

        :return: None
        """
        metrics1 = SnortIdsAlertCounters()
        metrics1.priority_alerts = [0] * 4
        metrics1.class_alerts = []
        for i in range(len(set(constants.SNORT_IDS_ROUTER.SNORT_ALERT_IDS_ID.values()))):
            metrics1.class_alerts.append(0)
        metrics1.severe_alerts = 5
        metrics1.warning_alerts = 3
        metrics1.total_alerts = 10
        metrics1.alerts_weighted_by_priority = 20

        metrics2 = SnortIdsAlertCounters()
        metrics2.priority_alerts = [0] * 4
        metrics2.class_alerts = []
        for i in range(len(set(constants.SNORT_IDS_ROUTER.SNORT_ALERT_IDS_ID.values()))):
            metrics2.class_alerts.append(0)
        metrics2.severe_alerts = 10
        metrics2.warning_alerts = 6
        metrics2.total_alerts = 20
        metrics2.alerts_weighted_by_priority = 40

        average_metrics = ReadEmulationStatisticsUtil.average_snort_metrics([metrics1, metrics2])

        assert average_metrics.priority_alerts == [0] * 4
        assert average_metrics.class_alerts == [0] * len(set(constants.SNORT_IDS_ROUTER.SNORT_ALERT_IDS_ID.values()))
        assert average_metrics.severe_alerts == 15
        assert average_metrics.warning_alerts == 9
        assert average_metrics.total_alerts == 30
        assert average_metrics.alerts_weighted_by_priority == 60

    def test_average_snort_rule_metrics(self) -> None:
        """
        Test the method that computes the average metrics from a list of Snort rule metrics

        :return: None
        """
        metrics1 = SnortIdsRuleCounters()
        metrics1.rule_alerts = {}

        metrics2 = SnortIdsAlertCounters()
        metrics2.rule_alerts = {}

        average_metrics = ReadEmulationStatisticsUtil.average_snort_rule_metrics([metrics1, metrics2])

        assert average_metrics.rule_alerts == {}
