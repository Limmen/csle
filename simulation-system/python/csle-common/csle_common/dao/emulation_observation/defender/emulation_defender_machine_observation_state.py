from typing import List, Dict, Any
from csle_common.dao.emulation_observation.common.emulation_port_observation_state \
    import EmulationPortObservationState
from csle_common.dao.emulation_observation.common.emulation_connection_observation_state \
    import EmulationConnectionObservationState
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.consumer_threads.host_metrics_consumer_thread import HostMetricsConsumerThread
from csle_common.consumer_threads.docker_host_stats_consumer_thread import DockerHostStatsConsumerThread
from csle_common.dao.emulation_config.log_sink_config import LogSinkConfig
from csle_collector.host_manager.host_metrics import HostMetrics
from csle_collector.docker_stats_manager.docker_stats import DockerStats


class EmulationDefenderMachineObservationState:
    """
    Represents the defender's belief state of a component in the emulation
    """

    def __init__(self, ips : List[str], log_sink_config: LogSinkConfig,
                 host_metrics : HostMetrics = None, docker_stats: DockerStats = None):
        """
        Initializes the DTO

        :param ips: the ip of the machine
        :param log_sink_config: the log sink config
        :param host_metrics: the host metrics object
        :param docker_stats: the docker stats objecty
        """
        self.ips = ips
        self.os="unknown"
        self.ports : List[EmulationPortObservationState] = []
        self.ssh_connections :List[EmulationConnectionObservationState] = []
        self.log_sink_config = log_sink_config
        self.host_metrics = host_metrics
        if self.host_metrics is None:
            self.host_metrics = HostMetrics()
        self.docker_stats = docker_stats
        if self.docker_stats is None:
            self.docker_stats = DockerStats()
        self.host_metrics_consumer_thread = None
        self.docker_stats_consumer_thread = None

    def start_monitor_threads(self) -> None:
        """
        Starts the monitoring threads

        :return: None
        """
        self.host_metrics_consumer_thread = HostMetricsConsumerThread(
            host_ip=self.ips[0],  kafka_server_ip=self.log_sink_config.container.get_ips()[0],
            kafka_port=self.log_sink_config.kafka_port, host_metrics=self.host_metrics)
        self.docker_stats_consumer_thread = DockerHostStatsConsumerThread(
            host_ip=self.ips[0],  kafka_server_ip=self.log_sink_config.container.get_ips()[0],
            kafka_port=self.log_sink_config.kafka_port, docker_stats=self.docker_stats
        )
        self.host_metrics_consumer_thread.start()
        self.docker_stats_consumer_thread.start()

    @staticmethod
    def from_container(container: NodeContainerConfig, log_sink_config: LogSinkConfig):
        """
        Creates an instance from a container configuration

        :param container: the container to create the instance from
        :param log_sink_config: the log sink config
        :return: the c reated instance
        """
        obj = EmulationDefenderMachineObservationState(ips=container.get_ips(), log_sink_config=log_sink_config,
                                                       host_metrics=None, docker_stats=None)
        obj.os = container.os
        return obj

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EmulationDefenderMachineObservationState":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict representation
        :return: the object instance
        """
        obj = EmulationDefenderMachineObservationState(
            ips=d["ips"], log_sink_config=LogSinkConfig.from_dict(d["log_sink_config"]),
            host_metrics=HostMetrics.from_dict(d["host_metrics"]),
            docker_stats=DockerStats.from_dict(d["docker_stats"]))
        obj.os = d["os"]
        obj.ports=list(map(lambda x: EmulationPortObservationState.from_dict(x), d["ports"]))
        obj.ssh_connections=list(map(lambda x: EmulationConnectionObservationState.from_dict(x), d["ssh_connections"]))
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["ips"] = self.ips
        d["os"] = self.os
        d["ports"] = list(map(lambda x: x.to_dict(), self.ports))
        d["ssh_connections"] = list(map(lambda x: x.to_dict(), self.ssh_connections))
        d["host_metrics"] = self.host_metrics.to_dict()
        d["docker_stats"] = self.docker_stats.to_dict()
        d["log_sink_config"] = self.log_sink_config.to_dict()
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ips:{self.ips}, os:{self.os}, ports: {list(map(lambda x: str(x), self.ports))}, " \
               f"ssh_connections: {list(map(lambda x: str(x), self.ssh_connections))}, " \
               f"host_metrics: {self.host_metrics}, docker_stats: {self.docker_stats}"

    def sort_ports(self) -> None:
        """
        Sorts the list of ports

        :return: None
        """
        for p in self.ports:
            p.port = int(p.port)
        self.ports = sorted(self.ports, key=lambda x: x.kafka_port, reverse=False)

    def cleanup(self) -> None:
        """
        Cleans up environment state. This method is particularly useful in emulation mode where there are
        SSH/Telnet/FTP... connections that should be cleaned up, as well as background threads.

        :return: None
        """
        if self.docker_stats_consumer_thread is not None:
            self.docker_stats_consumer_thread.running = False
            self.docker_stats_consumer_thread.consumer.close()
        for c in self.ssh_connections:
            c.cleanup()

    def copy(self) -> "EmulationDefenderMachineObservationState":
        """
        :return: a copy of the object
        """
        m_copy = EmulationDefenderMachineObservationState(
            ips=self.ips, log_sink_config=self.log_sink_config, host_metrics=self.host_metrics.copy(),
            docker_stats=self.docker_stats.copy())
        m_copy.os = self.os
        m_copy.ports = list(map(lambda x: x.copy(), self.ports))
        m_copy.ssh_connections = self.ssh_connections
        m_copy.host_metrics = self.host_metrics.copy()
        m_copy.docker_stats = self.docker_stats.copy()
        return m_copy

    def to_json_str(self) -> str:
        """
        Converts the DTO into a json string

        :return: the json string representation of the DTO
        """
        import json
        json_str = json.dumps(self.to_dict(), indent=4, sort_keys=True)
        return json_str

    def to_json_file(self, json_file_path: str) -> None:
        """
        Saves the DTO to a json file

        :param json_file_path: the json file path to save  the DTO to
        :return: None
        """
        import io
        json_str = self.to_json_str()
        with io.open(json_file_path, 'w', encoding='utf-8') as f:
            f.write(json_str)