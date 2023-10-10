from csle_collector.host_manager.dao.host_metrics import HostMetrics
from csle_common.consumer_threads.host_metrics_consumer_thread import HostMetricsConsumerThread
from csle_common.consumer_threads.aggregated_host_metrics_thread import AggregatedHostMetricsThread


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
