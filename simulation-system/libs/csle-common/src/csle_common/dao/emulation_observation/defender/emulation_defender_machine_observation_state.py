from typing import Optional, List, Dict, Any
from csle_common.dao.emulation_observation.common.emulation_port_observation_state \
    import EmulationPortObservationState
from csle_common.dao.emulation_observation.common.emulation_connection_observation_state \
    import EmulationConnectionObservationState
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.consumer_threads.host_metrics_consumer_thread import HostMetricsConsumerThread
from csle_common.consumer_threads.docker_host_stats_consumer_thread import DockerHostStatsConsumerThread
from csle_common.consumer_threads.snort_ids_log_consumer_thread import SnortIdsLogConsumerThread
from csle_common.consumer_threads.ossec_ids_log_consumer_thread import OSSECIdsLogConsumerThread
from csle_common.dao.emulation_config.kafka_config import KafkaConfig
from csle_collector.host_manager.dao.host_metrics import HostMetrics
from csle_collector.docker_stats_manager.dao.docker_stats import DockerStats
from csle_collector.snort_ids_manager.dao.snort_ids_ip_alert_counters import SnortIdsIPAlertCounters
from csle_collector.ossec_ids_manager.dao.ossec_ids_alert_counters import OSSECIdsAlertCounters
from csle_base.json_serializable import JSONSerializable


class EmulationDefenderMachineObservationState(JSONSerializable):
    """
    Represents the defender's belief state of a component in the emulation
    """

    def __init__(self, ips: List[str], kafka_config: Optional[KafkaConfig], host_metrics: HostMetrics,
                 docker_stats: DockerStats, snort_ids_ip_alert_counters: SnortIdsIPAlertCounters,
                 ossec_ids_alert_counters: OSSECIdsAlertCounters):
        """
        Initializes the DTO

        :param ips: the ip of the machine
        :param kafka_config: the kafka config
        :param host_metrics: the host metrics object
        :param docker_stats: the docker stats object
        :param snort_ids_ip_alert_counters: the snort ids ip alert counter object
        :param ossec_ids_alert_counters: the ossec ids alert counter object
        """
        self.ips = ips
        self.os = "unknown"
        self.ports: List[EmulationPortObservationState] = []
        self.ssh_connections: List[EmulationConnectionObservationState] = []
        self.kafka_config = kafka_config
        self.host_metrics = host_metrics
        self.docker_stats = docker_stats
        self.snort_ids_ip_alert_counters = snort_ids_ip_alert_counters
        self.ossec_ids_alert_counters = ossec_ids_alert_counters
        self.host_metrics_consumer_thread: Optional[HostMetricsConsumerThread] = None
        self.docker_stats_consumer_thread: Optional[DockerHostStatsConsumerThread] = None
        self.snort_ids_log_consumer_thread: Optional[SnortIdsLogConsumerThread] = None
        self.ossec_ids_log_consumer_thread: Optional[OSSECIdsLogConsumerThread] = None

    def start_monitor_threads(self) -> None:
        """
        Starts the monitoring threads

        :return: None
        """
        if self.kafka_config is None:
            raise ValueError("Cannot start monitoring threads since the kafka config is None.")
        self.host_metrics_consumer_thread = HostMetricsConsumerThread(
            host_ip=self.ips[0], kafka_server_ip=self.kafka_config.container.docker_gw_bridge_ip,
            kafka_port=self.kafka_config.kafka_port_external, host_metrics=self.host_metrics)
        self.docker_stats_consumer_thread = DockerHostStatsConsumerThread(
            host_ip=self.ips[0], kafka_server_ip=self.kafka_config.container.docker_gw_bridge_ip,
            kafka_port=self.kafka_config.kafka_port_external, docker_stats=self.docker_stats)
        self.snort_ids_log_consumer_thread = SnortIdsLogConsumerThread(
            host_ip=self.ips[0], kafka_server_ip=self.kafka_config.container.docker_gw_bridge_ip,
            kafka_port=self.kafka_config.kafka_port_external, snort_ids_alert_counters=self.snort_ids_ip_alert_counters)
        self.ossec_ids_log_consumer_thread = OSSECIdsLogConsumerThread(
            host_ip=self.ips[0], kafka_server_ip=self.kafka_config.container.docker_gw_bridge_ip,
            kafka_port=self.kafka_config.kafka_port_external, ossec_ids_alert_counters=self.ossec_ids_alert_counters)
        self.host_metrics_consumer_thread.start()
        self.docker_stats_consumer_thread.start()
        self.snort_ids_log_consumer_thread.start()
        self.ossec_ids_log_consumer_thread.start()

    @staticmethod
    def from_container(container: NodeContainerConfig, kafka_config: KafkaConfig):
        """
        Creates an instance from a container configuration

        :param container: the container to create the instance from
        :param kafka_config: the kafka config
        :return: the created instance
        """
        obj = EmulationDefenderMachineObservationState(ips=container.get_ips(), kafka_config=kafka_config,
                                                       host_metrics=HostMetrics(), docker_stats=DockerStats(),
                                                       ossec_ids_alert_counters=OSSECIdsAlertCounters(),
                                                       snort_ids_ip_alert_counters=SnortIdsIPAlertCounters())
        obj.os = container.os
        return obj

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EmulationDefenderMachineObservationState":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict representation
        :return: the object instance
        """
        if "kafka_config" in d and d["kafka_config"] is not None:
            kafka_config = KafkaConfig.from_dict(d["kafka_config"])
        else:
            kafka_config = None
        if "snort_ids_ip_alert_counters" in d and d["snort_ids_ip_alert_counters"] is not None:
            ip_alert_counters = SnortIdsIPAlertCounters.from_dict(d["snort_ids_ip_alert_counters"])
        else:
            ip_alert_counters = SnortIdsIPAlertCounters()
        if "ossec_ids_alert_counters" in d and d["ossec_ids_alert_counters"] is not None:
            ossec_alert_counters = OSSECIdsAlertCounters.from_dict(d["ossec_ids_alert_counters"])
        else:
            ossec_alert_counters = OSSECIdsAlertCounters()
        obj = EmulationDefenderMachineObservationState(
            ips=d["ips"], kafka_config=kafka_config,
            host_metrics=HostMetrics.from_dict(d["host_metrics"]),
            docker_stats=DockerStats.from_dict(d["docker_stats"]),
            snort_ids_ip_alert_counters=ip_alert_counters, ossec_ids_alert_counters=ossec_alert_counters)
        obj.os = d["os"]
        obj.ports = list(map(lambda x: EmulationPortObservationState.from_dict(x), d["ports"]))
        obj.ssh_connections = list(map(lambda x: EmulationConnectionObservationState.from_dict(x),
                                       d["ssh_connections"]))
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["ips"] = self.ips
        d["os"] = self.os
        d["ports"] = list(map(lambda x: x.to_dict(), self.ports))
        d["ssh_connections"] = list(map(lambda x: x.to_dict(), self.ssh_connections))
        d["host_metrics"] = self.host_metrics.to_dict() if self.host_metrics is not None else None
        d["docker_stats"] = self.docker_stats.to_dict() if self.docker_stats is not None else None
        d["ossec_ids_alert_counters"] = self.ossec_ids_alert_counters.to_dict() \
            if self.ossec_ids_alert_counters is not None else None
        d["snort_ids_ip_alert_counters"] = self.snort_ids_ip_alert_counters.to_dict() \
            if self.snort_ids_ip_alert_counters is not None else None
        d["kafka_config"] = self.kafka_config.to_dict() if self.kafka_config is not None else None
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ips:{self.ips}, os:{self.os}, ports: {list(map(lambda x: str(x), self.ports))}, " \
               f"ssh_connections: {list(map(lambda x: str(x), self.ssh_connections))}, " \
               f"host_metrics: {self.host_metrics}, docker_stats: {self.docker_stats}, " \
               f"snort_ids_ip_alert_counters: {self.snort_ids_ip_alert_counters}, " \
               f"ossec_ids_alert_counters: {self.ossec_ids_alert_counters}"

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
        if self.host_metrics_consumer_thread is not None:
            self.host_metrics_consumer_thread.running = False
            self.host_metrics_consumer_thread.consumer.close()
        if self.snort_ids_log_consumer_thread is not None:
            self.snort_ids_log_consumer_thread.running = False
            self.snort_ids_log_consumer_thread.consumer.close()
        if self.ossec_ids_log_consumer_thread is not None:
            self.ossec_ids_log_consumer_thread.running = False
            self.ossec_ids_log_consumer_thread.consumer.close()
        for c in self.ssh_connections:
            c.cleanup()

    def copy(self) -> "EmulationDefenderMachineObservationState":
        """
        :return: a copy of the object
        """
        m_copy = EmulationDefenderMachineObservationState(
            ips=self.ips, kafka_config=self.kafka_config,
            host_metrics=self.host_metrics.copy(),
            docker_stats=self.docker_stats.copy(),
            ossec_ids_alert_counters=self.ossec_ids_alert_counters.copy(),
            snort_ids_ip_alert_counters=self.snort_ids_ip_alert_counters.copy())
        m_copy.os = self.os
        if self.ports == []:
            m_copy.ports = self.ports
        else:
            m_copy.ports = list(map(lambda x: x.copy(), self.ports))
        if self.ssh_connections == []:
            m_copy.ssh_connections = self.ssh_connections
        else:
            m_copy.ssh_connections = list(map(lambda x: x.copy(), self.ssh_connections))
        if self.snort_ids_ip_alert_counters is None:
            m_copy.snort_ids_ip_alert_counters = self.snort_ids_ip_alert_counters
        else:
            m_copy.snort_ids_ip_alert_counters = self.snort_ids_ip_alert_counters.copy()
        if self.ossec_ids_alert_counters is None:
            m_copy.ossec_ids_alert_counters = self.ossec_ids_alert_counters
        else:
            m_copy.ossec_ids_alert_counters = self.ossec_ids_alert_counters.copy()
        return m_copy

    @staticmethod
    def from_json_file(json_file_path: str) -> "EmulationDefenderMachineObservationState":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return EmulationDefenderMachineObservationState.from_dict(json.loads(json_str))

    def num_attributes(self) -> int:
        """
        :return: The number of attribute of the DTO
        """
        num_attributes = 2
        if self.host_metrics is not None:
            num_attributes = num_attributes + self.host_metrics.num_attributes()
        if self.docker_stats is not None:
            num_attributes = num_attributes + self.docker_stats.num_attributes()
        if len(self.ports) > 0:
            num_attributes = num_attributes + len(self.ports) * self.ports[0].num_attributes()
        if len(self.ssh_connections) > 0:
            num_attributes = num_attributes + len(self.ports) * self.ssh_connections[0].num_attributes()
        return num_attributes

    @staticmethod
    def schema() -> "EmulationDefenderMachineObservationState":
        """
        :return: get the schema of the DTO
        """
        return EmulationDefenderMachineObservationState(ips=[""], kafka_config=KafkaConfig.schema(),
                                                        host_metrics=HostMetrics.schema(),
                                                        docker_stats=DockerStats.schema(),
                                                        snort_ids_ip_alert_counters=SnortIdsIPAlertCounters.schema(),
                                                        ossec_ids_alert_counters=OSSECIdsAlertCounters.schema())
