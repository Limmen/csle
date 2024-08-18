from unittest.mock import MagicMock, patch
from csle_common.consumer_threads.aggregated_host_metrics_thread import AggregatedHostMetricsThread
from csle_collector.host_manager.dao.host_metrics import HostMetrics


class TestSuiteAggregatedHostMetricsThread:
    """
    Test suite for AggregatedHostMetricsThread
    """
    def test_initialization(self) -> None:
        """
        Test the initialization function

        :return: None
        """
        host_metrics = HostMetrics
        mock_machine = MagicMock(spec='EmulationDefenderMachineObservationState')
        mock_machines = [mock_machine, mock_machine]
        sleep_time = 3
        thread = AggregatedHostMetricsThread(host_metrics=host_metrics, machines=mock_machines, sleep_time=sleep_time)
        assert thread.host_metrics == host_metrics
        assert thread.machines == mock_machines
        assert thread.sleep_time == sleep_time

    @patch("time.sleep", return_value=None)
    def test_run(self, mock_sleep) -> None:
        """
        Test the method that runs the thread

        :param mock_sleep: mock_sleep
        :return: None
        """
        mock_host_metrics_1 = MagicMock(spec="HostMetrics")
        mock_host_metrics_1.num_logged_in_users = 5
        mock_host_metrics_1.num_failed_login_attempts = 2
        mock_host_metrics_1.num_open_connections = 10
        mock_host_metrics_1.num_login_events = 7
        mock_host_metrics_1.num_processes = 50
        mock_host_metrics_1.num_users = 3

        mock_host_metrics_2 = MagicMock(spec="HostMetrics")
        mock_host_metrics_2.num_logged_in_users = 3
        mock_host_metrics_2.num_failed_login_attempts = 1
        mock_host_metrics_2.num_open_connections = 5
        mock_host_metrics_2.num_login_events = 4
        mock_host_metrics_2.num_processes = 30
        mock_host_metrics_2.num_users = 2

        mock_machine_1 = MagicMock(spec="EmulationDefenderMachineObservationState")
        mock_machine_1.host_metrics = mock_host_metrics_1

        mock_machine_2 = MagicMock(spec="EmulationDefenderMachineObservationState")
        mock_machine_2.host_metrics = mock_host_metrics_2

        mock_machines = [mock_machine_1, mock_machine_2]

        mock_aggregated_host_metrics = MagicMock(spec="HostMetrics")
        mock_aggregated_host_metrics.copy = MagicMock(spec="HostMetrics")
        mock_aggregated_host_metrics.copy.return_value = MagicMock(spec="HostMetrics")

        sleep_time = 1

        thread = AggregatedHostMetricsThread(
            host_metrics=mock_aggregated_host_metrics, machines=mock_machines, sleep_time=sleep_time
        )

        def stop_running(*args, **kwargs):
            thread.running = False

        mock_sleep.side_effect = stop_running
        thread.run()
        assert thread.host_metrics.num_logged_in_users == 8
        assert thread.host_metrics.num_failed_login_attempts == 3
        assert thread.host_metrics.num_open_connections == 15
        assert thread.host_metrics.num_login_events == 11
        assert thread.host_metrics.num_processes == 80
        assert thread.host_metrics.num_users == 5

    def test_get_average_aggregated_host_metrics(self) -> None:
        """
        Test the method that returns the average of the list of aggregated host metrics

        :return: None
        """
        mock_host_metrics_1 = MagicMock(spec="HostMetrics")
        mock_host_metrics_1.num_logged_in_users = 10
        mock_host_metrics_1.num_failed_login_attempts = 5
        mock_host_metrics_1.num_open_connections = 15
        mock_host_metrics_1.num_login_events = 20
        mock_host_metrics_1.num_processes = 25
        mock_host_metrics_1.num_users = 30

        mock_host_metrics_2 = MagicMock(spec="HostMetrics")
        mock_host_metrics_2.num_logged_in_users = 20
        mock_host_metrics_2.num_failed_login_attempts = 10
        mock_host_metrics_2.num_open_connections = 25
        mock_host_metrics_2.num_login_events = 30
        mock_host_metrics_2.num_processes = 35
        mock_host_metrics_2.num_users = 40

        thread = AggregatedHostMetricsThread(
            host_metrics=MagicMock(spec="HostMetrics"), machines=[], sleep_time=1
        )
        thread.host_metrics_list = [mock_host_metrics_1, mock_host_metrics_2]
        avg_metrics = thread.get_average_aggregated_host_metrics()
        assert avg_metrics.num_logged_in_users == 15
        assert avg_metrics.num_failed_login_attempts == 8
        assert avg_metrics.num_open_connections == 20
        assert avg_metrics.num_login_events == 25
        assert avg_metrics.num_processes == 30
        assert avg_metrics.num_users == 35
