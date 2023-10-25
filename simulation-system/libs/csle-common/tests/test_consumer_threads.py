import numpy as np
import random
import csle_collector.constants.constants as constants
from csle_collector.host_manager.dao.host_metrics import HostMetrics
from csle_common.consumer_threads.host_metrics_consumer_thread import HostMetricsConsumerThread
from csle_common.consumer_threads.aggregated_host_metrics_thread import AggregatedHostMetricsThread
from csle_collector.ossec_ids_manager.dao.ossec_ids_alert_counters import OSSECIdsAlertCounters
from csle_common.consumer_threads.aggregated_ossec_ids_log_consumer_thread import AggregatedOSSECIdsLogConsumerThread


class TestConsumerThreadsSuiteSuite:
    """
    Test suite for consumer threads
    """

    def test_host_metrics_consumer_thread(self) -> None:
        """
        Tests creation of a host metrics consumer thread and its methods

        :return: None
        """
        example_host_metrics = HostMetrics(num_logged_in_users=1, num_failed_login_attempts=10,
                                           num_open_connections=1, num_login_events=2,
                                           num_processes=5, num_users=1, ip="1.1.1.1", ts=0.5)
        thread = HostMetricsConsumerThread(host_ip="8.8.8.8", kafka_server_ip="8.8.8.8", kafka_port=3030,
                                           host_metrics=example_host_metrics)
        assert thread.host_metrics == example_host_metrics

    def test_aggregated_host_metrics_consumer_thread(self) -> None:
        """
        Tests creation of the aggregated host metrics consumer thread and its methods

        :return: None
        """
        example_host_metrics = HostMetrics(num_logged_in_users=1, num_failed_login_attempts=10,
                                           num_open_connections=1, num_login_events=2,
                                           num_processes=5, num_users=1, ip="1.1.1.1", ts=0.5)
        thread = AggregatedHostMetricsThread(host_metrics=example_host_metrics, machines=[], sleep_time=10)
        assert thread.host_metrics == example_host_metrics
        assert thread.sleep_time == 10
        assert len(thread.machines) == 0

        # Test empty list
        thread.host_metrics_list = []
        averaged_host_metrics = thread.get_average_aggregated_host_metrics()
        assert averaged_host_metrics == example_host_metrics

        # Test singleton list
        thread.host_metrics_list = [example_host_metrics]
        averaged_host_metrics = thread.get_average_aggregated_host_metrics()
        assert averaged_host_metrics == example_host_metrics

        # Test list with 10 identical objects
        thread.host_metrics_list = [example_host_metrics] * 10
        averaged_host_metrics = thread.get_average_aggregated_host_metrics()
        assert averaged_host_metrics.num_logged_in_users == example_host_metrics.num_logged_in_users
        assert averaged_host_metrics.num_failed_login_attempts == example_host_metrics.num_failed_login_attempts
        assert averaged_host_metrics.num_open_connections == example_host_metrics.num_open_connections
        assert averaged_host_metrics.num_login_events == example_host_metrics.num_login_events
        assert averaged_host_metrics.num_processes == example_host_metrics.num_processes
        assert averaged_host_metrics.num_users == example_host_metrics.num_users

        # Test list with two different objects
        example_host_metrics_2 = HostMetrics(num_logged_in_users=2, num_failed_login_attempts=5,
                                             num_open_connections=7, num_login_events=9,
                                             num_processes=11, num_users=3, ip="1.1.1.1", ts=0.5)
        thread.host_metrics_list = [example_host_metrics, example_host_metrics_2]
        averaged_host_metrics = thread.get_average_aggregated_host_metrics()
        assert (averaged_host_metrics.num_logged_in_users ==
                int(round((example_host_metrics.num_logged_in_users + example_host_metrics_2.num_logged_in_users) / 2)))
        assert (averaged_host_metrics.num_failed_login_attempts ==
                int(round((example_host_metrics.num_failed_login_attempts +
                           example_host_metrics_2.num_failed_login_attempts) / 2)))
        assert (averaged_host_metrics.num_open_connections ==
                int(round(
                    (example_host_metrics.num_open_connections + example_host_metrics_2.num_open_connections) / 2)))
        assert (averaged_host_metrics.num_login_events ==
                int(round((example_host_metrics.num_login_events + example_host_metrics_2.num_login_events) / 2)))
        assert (averaged_host_metrics.num_processes ==
                int(round((example_host_metrics.num_processes + example_host_metrics_2.num_processes) / 2)))
        assert (averaged_host_metrics.num_users ==
                int(round((example_host_metrics.num_users + example_host_metrics_2.num_users) / 2)))

    def test_aggregated_ossec_ids_log_consumer_thread(self) -> None:
        """
        Tests creation of a ossec ids log consumer thread and its methods

        :param example_ossec_ids_alert_counters: an object of OSSECIdsAlertCounters
        :return: None
        """
        example_ossec_ids_alert_counters = OSSECIdsAlertCounters()
        example_ossec_ids_alert_counters.level_alerts = list(np.zeros(16))
        for idx in range(16):
            example_ossec_ids_alert_counters.level_alerts[idx] = random.randint(0, 10)

        example_ossec_ids_alert_counters.group_alerts = list(
            np.zeros(len(set(constants.OSSEC.OSSEC_IDS_ALERT_GROUP_ID.values()))))
        for idx in range(len(example_ossec_ids_alert_counters.group_alerts)):
            example_ossec_ids_alert_counters.group_alerts[idx] = random.randint(0, 10)

        example_ossec_ids_alert_counters.severe_alerts = 10
        example_ossec_ids_alert_counters.warning_alerts = 4
        example_ossec_ids_alert_counters.total_alerts = 21
        example_ossec_ids_alert_counters.alerts_weighted_by_level = 0.3

        thread = AggregatedOSSECIdsLogConsumerThread(
            kafka_server_ip="1.2.3.4", kafka_port=1234, ossec_ids_alert_counters=example_ossec_ids_alert_counters.copy()
        )
        assert thread.ossec_ids_alert_counters == example_ossec_ids_alert_counters
        assert thread.kafka_port == 1234
        assert thread.kafka_server_ip == "1.2.3.4"

        # Test empty list
        thread.ossec_ids_alert_counters_list = []
        aggregated_ossec_ids_alert_counters = thread.get_aggregated_ids_alert_counters()
        assert aggregated_ossec_ids_alert_counters == example_ossec_ids_alert_counters

        # Test singleton list
        thread.ossec_ids_alert_counters_list = [example_ossec_ids_alert_counters.copy()]
        aggregated_ossec_ids_alert_counters = thread.get_aggregated_ids_alert_counters()
        assert aggregated_ossec_ids_alert_counters == example_ossec_ids_alert_counters

        # Test list with 10 identical objects
        thread.ossec_ids_alert_counters_list = []
        for i in range(10):
            thread.ossec_ids_alert_counters_list.append(example_ossec_ids_alert_counters.copy())
        aggregated_ossec_ids_alert_counters = thread.get_aggregated_ids_alert_counters()
        assert (aggregated_ossec_ids_alert_counters.severe_alerts ==
                10 * example_ossec_ids_alert_counters.severe_alerts)
        assert (aggregated_ossec_ids_alert_counters.warning_alerts ==
                10 * example_ossec_ids_alert_counters.warning_alerts)
        assert (aggregated_ossec_ids_alert_counters.total_alerts == 10 * example_ossec_ids_alert_counters.total_alerts)
        assert (round(aggregated_ossec_ids_alert_counters.alerts_weighted_by_level, 3) ==
                round(10 * example_ossec_ids_alert_counters.alerts_weighted_by_level, 3))
        for idx in range(len(aggregated_ossec_ids_alert_counters.level_alerts)):
            assert (aggregated_ossec_ids_alert_counters.level_alerts[idx] ==
                    10 * example_ossec_ids_alert_counters.level_alerts[idx])
        for idx in range(len(aggregated_ossec_ids_alert_counters.group_alerts)):
            assert (aggregated_ossec_ids_alert_counters.group_alerts[idx] ==
                    10 * example_ossec_ids_alert_counters.group_alerts[idx])

        # Test list with two different objects
        example_ossec_ids_alert_counters_2 = OSSECIdsAlertCounters()
        example_ossec_ids_alert_counters_2.level_alerts = list(np.zeros(16))
        for idx in range(16):
            example_ossec_ids_alert_counters_2.level_alerts[idx] = random.randint(0, 10)

        example_ossec_ids_alert_counters_2.group_alerts = list(
            np.zeros(len(set(constants.OSSEC.OSSEC_IDS_ALERT_GROUP_ID.values()))))
        for idx in range(len(example_ossec_ids_alert_counters_2.group_alerts)):
            example_ossec_ids_alert_counters_2.group_alerts[idx] = random.randint(0, 10)

        example_ossec_ids_alert_counters_2.severe_alerts = 15
        example_ossec_ids_alert_counters_2.warning_alerts = 1
        example_ossec_ids_alert_counters_2.total_alerts = 18
        example_ossec_ids_alert_counters_2.alerts_weighted_by_level = 0.7

        thread.ossec_ids_alert_counters_list = [example_ossec_ids_alert_counters, example_ossec_ids_alert_counters_2]
        aggregated_ossec_ids_alert_counters = thread.get_aggregated_ids_alert_counters()

        assert (aggregated_ossec_ids_alert_counters.severe_alerts ==
                example_ossec_ids_alert_counters.severe_alerts + example_ossec_ids_alert_counters_2.severe_alerts)
        assert (aggregated_ossec_ids_alert_counters.warning_alerts ==
                example_ossec_ids_alert_counters.warning_alerts + example_ossec_ids_alert_counters_2.warning_alerts)
        assert (aggregated_ossec_ids_alert_counters.total_alerts ==
                example_ossec_ids_alert_counters.total_alerts + example_ossec_ids_alert_counters_2.total_alerts)
        assert (round(aggregated_ossec_ids_alert_counters.alerts_weighted_by_level, 3) ==
                round(example_ossec_ids_alert_counters.alerts_weighted_by_level +
                      example_ossec_ids_alert_counters_2.alerts_weighted_by_level, 3))
        for idx in range(len(aggregated_ossec_ids_alert_counters.level_alerts)):
            assert (aggregated_ossec_ids_alert_counters.level_alerts[idx] ==
                    example_ossec_ids_alert_counters.level_alerts[idx] +
                    example_ossec_ids_alert_counters_2.level_alerts[idx])
        for idx in range(len(aggregated_ossec_ids_alert_counters.group_alerts)):
            assert (aggregated_ossec_ids_alert_counters.group_alerts[idx] ==
                    example_ossec_ids_alert_counters.group_alerts[idx] +
                    example_ossec_ids_alert_counters_2.group_alerts[idx])
