from typing import List
import threading
import time
from csle_collector.host_manager.host_metrics import HostMetrics
from csle_common.dao.emulation_observation.defender.emulation_defender_machine_observation_state import \
    EmulationDefenderMachineObservationState


class AggregatedHostMetricsThread(threading.Thread):
    """
    Thread that polls the Kafka log to get the latest status of the docker statistics for a specific host
    """

    def __init__(self, host_metrics: HostMetrics,
                 machines: List[EmulationDefenderMachineObservationState], sleep_time: int) -> None:
        """
        Initializes the thread

        :param host_metrics: the host metrics to update
        :param machines: the list of machiens to update the host metrics with
        """
        threading.Thread.__init__(self)
        self.machines = machines
        self.running = True
        self.host_metrics = host_metrics
        self.host_metrics_list = []
        self.sleep_time = sleep_time

    def run(self) -> None:
        """
        Runs the thread

        :return: None
        """
        while self.running:
            time.sleep(self.sleep_time)
            total_num_logged_in_users = 0
            total_num_failed_login_attempts = 0
            total_num_open_connections = 0
            total_num_login_events = 0
            total_num_processes = 0
            total_num_users = 0
            for m in self.machines:
                total_num_logged_in_users += m.host_metrics.num_logged_in_users
                total_num_failed_login_attempts += m.host_metrics.num_failed_login_attempts
                total_num_open_connections += m.host_metrics.num_open_connections
                total_num_login_events += m.host_metrics.num_login_events
                total_num_processes += m.host_metrics.num_processes
                total_num_users += m.host_metrics.num_users
            self.host_metrics.num_logged_in_users = total_num_logged_in_users
            self.host_metrics.num_failed_login_attempts = total_num_failed_login_attempts
            self.host_metrics.num_open_connections = total_num_open_connections
            self.host_metrics.num_login_events = total_num_login_events
            self.host_metrics.num_processes = total_num_processes
            self.host_metrics.num_users = total_num_users
            self.host_metrics_list.append(self.host_metrics.copy())

    def get_average_aggregated_host_metrics(self) -> HostMetrics:
        """
        :return: average of the list of aggregated host metrics
        """
        if len(self.host_metrics_list) == 0:
            return self.host_metrics.copy()
        if len(self.host_metrics_list) == 1:
            return self.host_metrics_list[0].copy()
        avg_host_metrics = HostMetrics()
        for i in range(0, len(self.host_metrics_list)):
            avg_host_metrics.num_logged_in_users = (avg_host_metrics.num_logged_in_users +
                                                    self.host_metrics_list[i].num_logged_in_users)
            avg_host_metrics.num_failed_login_attempts = (avg_host_metrics.num_failed_login_attempts +
                                                          self.host_metrics_list[i].num_failed_login_attempts)
            avg_host_metrics.num_open_connections = (avg_host_metrics.num_open_connections
                                                     + self.host_metrics_list[i].num_open_connections)
            avg_host_metrics.num_login_events = (avg_host_metrics.num_login_events +
                                                 self.host_metrics_list[i].num_login_events)
            avg_host_metrics.num_processes = avg_host_metrics.num_processes + self.host_metrics_list[i].num_processes
            avg_host_metrics.num_users = avg_host_metrics.num_users + self.host_metrics_list[i].num_users

        avg_host_metrics.num_logged_in_users = int(round(avg_host_metrics.num_logged_in_users /
                                                         len(self.host_metrics_list)))
        avg_host_metrics.num_failed_login_attempts = int(round(avg_host_metrics.num_failed_login_attempts /
                                                               len(self.host_metrics_list)))
        avg_host_metrics.num_open_connections = int(round(avg_host_metrics.num_open_connections /
                                                          len(self.host_metrics_list)))
        avg_host_metrics.num_login_events = int(round(avg_host_metrics.num_login_events / len(self.host_metrics_list)))
        avg_host_metrics.num_processes = int(round(avg_host_metrics.num_processes / len(self.host_metrics_list)))
        avg_host_metrics.num_users = int(round(avg_host_metrics.num_users / len(self.host_metrics_list)))
        return avg_host_metrics
