from typing import Optional, List, Dict, Any, Union, Set, Tuple
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_observation.defender.emulation_defender_machine_observation_state \
    import EmulationDefenderMachineObservationState
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_config.kafka_config import KafkaConfig
from csle_common.consumer_threads.docker_stats_consumer_thread import DockerStatsConsumerThread
from csle_common.consumer_threads.aggregated_snort_ids_log_consumer_thread import AggregatedSnortIdsLogConsumerThread
from csle_common.consumer_threads.aggregated_ossec_ids_log_consumer_thread import AggregatedOSSECIdsLogConsumerThread
from csle_common.consumer_threads.aggregated_snort_ids_rule_log_consumer_thread \
    import AggregatedSnortIdsRuleLogConsumerThread
from csle_common.consumer_threads.client_population_consumer_thread import ClientPopulationConsumerThread
from csle_common.consumer_threads.attacker_actions_consumer_thread import AttackerActionsConsumerThread
from csle_common.consumer_threads.defender_actions_consumer_thread import DefenderActionsConsumerThread
from csle_common.consumer_threads.aggregated_host_metrics_thread import AggregatedHostMetricsThread
from csle_collector.client_manager.client_population_metrics import ClientPopulationMetrics
from csle_collector.docker_stats_manager.dao.docker_stats import DockerStats
from csle_collector.snort_ids_manager.dao.snort_ids_alert_counters import SnortIdsAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_rule_counters import SnortIdsRuleCounters
from csle_collector.ossec_ids_manager.dao.ossec_ids_alert_counters import OSSECIdsAlertCounters
from csle_collector.host_manager.dao.host_metrics import HostMetrics
from csle_base.json_serializable import JSONSerializable


class EmulationDefenderObservationState(JSONSerializable):
    """
    Represents the defender's agent's current belief state of the emulation
    """

    def __init__(self, kafka_config: Union[KafkaConfig, None], client_population_metrics: ClientPopulationMetrics,
                 docker_stats: DockerStats, snort_ids_alert_counters: SnortIdsAlertCounters,
                 ossec_ids_alert_counters: OSSECIdsAlertCounters, aggregated_host_metrics: HostMetrics,
                 defender_actions: List[EmulationDefenderAction], attacker_actions: List[EmulationAttackerAction],
                 snort_ids_rule_counters: SnortIdsRuleCounters):
        """
        Initializes the DTO

        :param kafka_config: the kafka config
        :param client_population_metrics: the client population metrics
        :param docker_stats: the docker stats
        :param snort_ids_alert_counters: the snort ids alert counters
        :param ossec_ids_alert_counters: the ossec ids alert counters
        :param defender_actions: the list of defender actions
        :param attacker_actions: the list of attacker actions
        :param aggregated_host_metrics: the aggregated host metrics
        :param snort_ids_rule_counters: the aggregated snort IDS rule counters
        """
        self.kafka_config = kafka_config
        self.machines: List[EmulationDefenderMachineObservationState] = []
        self.actions_tried: Set[Tuple[int, int, str]] = set()
        self.client_population_metrics = client_population_metrics
        self.avg_client_population_metrics = self.client_population_metrics.copy()
        self.docker_stats = docker_stats
        self.avg_docker_stats = self.docker_stats.copy()
        self.snort_ids_alert_counters = snort_ids_alert_counters
        self.avg_snort_ids_alert_counters = self.snort_ids_alert_counters.copy()
        self.snort_ids_rule_counters = snort_ids_rule_counters
        self.avg_snort_ids_rule_counters = self.snort_ids_rule_counters.copy()
        self.ossec_ids_alert_counters = ossec_ids_alert_counters
        self.avg_ossec_ids_alert_counters = self.ossec_ids_alert_counters.copy()
        self.attacker_actions = attacker_actions
        self.defender_actions = defender_actions
        self.aggregated_host_metrics = aggregated_host_metrics
        self.avg_aggregated_host_metrics: HostMetrics = self.aggregated_host_metrics.copy()
        self.docker_stats_consumer_thread: Optional[DockerStatsConsumerThread] = None
        self.client_population_consumer_thread: Optional[ClientPopulationConsumerThread] = None
        self.aggregated_snort_ids_log_consumer_thread: Optional[AggregatedSnortIdsLogConsumerThread] = None
        self.aggregated_snort_ids_rule_log_consumer_thread: Optional[AggregatedSnortIdsRuleLogConsumerThread] = None
        self.aggregated_ossec_ids_log_consumer_thread: Optional[AggregatedOSSECIdsLogConsumerThread] = None
        self.attacker_actions_consumer_thread: Optional[AttackerActionsConsumerThread] = None
        self.defender_actions_consumer_thread: Optional[DefenderActionsConsumerThread] = None
        self.aggregated_host_metrics_thread: Optional[AggregatedHostMetricsThread] = None

    def start_monitoring_threads(self) -> None:
        """
        Starts the avg host metrics thread

        :return: None
        """
        if self.kafka_config is None:
            raise ValueError("KafkaConfig is None")
        if self.attacker_actions is None:
            raise ValueError("EmulationAttackerAction is None")
        if self.defender_actions is None:
            raise ValueError("EmulationDefenderAction is None")
        self.aggregated_host_metrics_thread = AggregatedHostMetricsThread(
            host_metrics=self.aggregated_host_metrics,
            sleep_time=self.kafka_config.time_step_len_seconds,
            machines=self.machines
        )
        self.docker_stats_consumer_thread = DockerStatsConsumerThread(
            kafka_server_ip=self.kafka_config.container.docker_gw_bridge_ip,
            kafka_port=self.kafka_config.kafka_port_external,
            docker_stats=self.docker_stats)
        self.client_population_consumer_thread = ClientPopulationConsumerThread(
            kafka_server_ip=self.kafka_config.container.docker_gw_bridge_ip,
            kafka_port=self.kafka_config.kafka_port_external,
            client_population_metrics=self.client_population_metrics
        )
        self.aggregated_snort_ids_log_consumer_thread = AggregatedSnortIdsLogConsumerThread(
            kafka_server_ip=self.kafka_config.container.docker_gw_bridge_ip,
            kafka_port=self.kafka_config.kafka_port_external,
            snort_ids_alert_counters=self.snort_ids_alert_counters
        )
        self.aggregated_snort_ids_rule_log_consumer_thread = AggregatedSnortIdsRuleLogConsumerThread(
            kafka_server_ip=self.kafka_config.container.docker_gw_bridge_ip,
            kafka_port=self.kafka_config.kafka_port_external,
            snort_ids_rule_counters=self.snort_ids_rule_counters
        )
        self.aggregated_ossec_ids_log_consumer_thread = AggregatedOSSECIdsLogConsumerThread(
            kafka_server_ip=self.kafka_config.container.docker_gw_bridge_ip,
            kafka_port=self.kafka_config.kafka_port_external,
            ossec_ids_alert_counters=self.ossec_ids_alert_counters
        )
        self.attacker_actions_consumer_thread = AttackerActionsConsumerThread(
            kafka_server_ip=self.kafka_config.container.docker_gw_bridge_ip,
            kafka_port=self.kafka_config.kafka_port_external,
            attacker_actions=self.attacker_actions
        )
        self.defender_actions_consumer_thread = DefenderActionsConsumerThread(
            kafka_server_ip=self.kafka_config.container.docker_gw_bridge_ip,
            kafka_port=self.kafka_config.kafka_port_external,
            defender_actions=self.defender_actions
        )
        self.aggregated_host_metrics_thread.start()
        self.docker_stats_consumer_thread.start()
        self.client_population_consumer_thread.start()
        self.aggregated_snort_ids_log_consumer_thread.start()
        self.aggregated_snort_ids_rule_log_consumer_thread.start()
        self.aggregated_ossec_ids_log_consumer_thread.start()
        self.attacker_actions_consumer_thread.start()
        self.defender_actions_consumer_thread.start()
        for m in self.machines:
            m.start_monitor_threads()

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EmulationDefenderObservationState":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        kafka_config: Union[None, KafkaConfig] = None
        try:
            kafka_config = KafkaConfig.from_dict(d["kafka_config"])
        except Exception:
            pass
        if "snort_ids_rule_counters" not in d:
            snort_ids_rule_counters = SnortIdsRuleCounters()
        else:
            snort_ids_rule_counters = SnortIdsRuleCounters.from_dict(d["snort_ids_rule_counters"])
        if "avg_snort_ids_rule_counters" not in d:
            avg_snort_ids_rule_counters = SnortIdsRuleCounters()
        else:
            avg_snort_ids_rule_counters = SnortIdsRuleCounters.from_dict(d["avg_snort_ids_rule_counters"])
        obj = EmulationDefenderObservationState(
            kafka_config=kafka_config,
            client_population_metrics=ClientPopulationMetrics.from_dict(d["client_population_metrics"]),
            docker_stats=DockerStats.from_dict(d["docker_stats"]),
            ossec_ids_alert_counters=OSSECIdsAlertCounters.from_dict(d["ossec_ids_alert_counters"]),
            aggregated_host_metrics=HostMetrics.from_dict(d["aggregated_host_metrics"]),
            defender_actions=list(map(lambda x: EmulationDefenderAction.from_dict(x), d["defender_actions"])),
            attacker_actions=list(map(lambda x: EmulationAttackerAction.from_dict(x), d["attacker_actions"])),
            snort_ids_rule_counters=snort_ids_rule_counters,
            snort_ids_alert_counters=SnortIdsAlertCounters.from_dict(d["snort_ids_alert_counters"]))
        obj.machines = list(map(lambda x: EmulationDefenderMachineObservationState.from_dict(d=x), d["machines"]))
        obj.actions_tried = set(list(map(lambda x: (int(x[0]), int(x[1]), str(x[2])), d["actions_tried"])))
        obj.avg_aggregated_host_metrics = HostMetrics.from_dict(d["avg_aggregated_host_metrics"])
        obj.avg_docker_stats = DockerStats.from_dict(d["avg_docker_stats"])
        obj.avg_client_population_metrics = ClientPopulationMetrics.from_dict(d["avg_client_population_metrics"])
        obj.avg_snort_ids_alert_counters = SnortIdsAlertCounters.from_dict(d["avg_snort_ids_alert_counters"])
        obj.avg_snort_ids_rule_counters = avg_snort_ids_rule_counters
        obj.avg_ossec_ids_alert_counters = OSSECIdsAlertCounters.from_dict(d["avg_ossec_ids_alert_counters"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["machines"] = list(map(lambda x: x.to_dict(), self.machines))
        d["actions_tried"] = list(self.actions_tried)
        if self.client_population_metrics is None or self.docker_stats is None \
                or self.snort_ids_alert_counters is None or self.snort_ids_rule_counters is None or \
                self.ossec_ids_alert_counters is None:
            raise ValueError("ClientPopulationMetrics is None")
        d["client_population_metrics"] = self.client_population_metrics.to_dict()
        d["docker_stats"] = self.docker_stats.to_dict()
        d["snort_ids_alert_counters"] = self.snort_ids_alert_counters.to_dict()
        d["snort_ids_rule_counters"] = self.snort_ids_rule_counters.to_dict()
        d["ossec_ids_alert_counters"] = self.ossec_ids_alert_counters.to_dict()
        if self.kafka_config is not None:
            d["kafka_config"] = self.kafka_config.to_dict()
        else:
            d["kafka_config"] = None
        if self.attacker_actions is None:
            raise ValueError("attacker_actions is None and thus has no to_dict attribute")
        if self.defender_actions is None:
            raise ValueError("attacker_actions is None and thus has no to_dict attribute")
        if self.aggregated_host_metrics is None or self.avg_aggregated_host_metrics is None:
            raise ValueError("aggregated_host_metrics is None and thus has no to_dict attribute")
        d["attacker_actions"] = list(map(lambda x: x.to_dict(), self.attacker_actions))
        d["defender_actions"] = list(map(lambda x: x.to_dict(), self.defender_actions))
        d["aggregated_host_metrics"] = self.aggregated_host_metrics.to_dict()
        d["avg_aggregated_host_metrics"] = self.avg_aggregated_host_metrics.to_dict()
        d["avg_client_population_metrics"] = self.avg_client_population_metrics.to_dict()
        d["avg_docker_stats"] = self.avg_docker_stats.to_dict()
        d["avg_snort_ids_alert_counters"] = self.avg_snort_ids_alert_counters.to_dict()
        d["avg_snort_ids_rule_counters"] = self.avg_snort_ids_rule_counters.to_dict()
        d["avg_ossec_ids_alert_counters"] = self.avg_ossec_ids_alert_counters.to_dict()
        return d

    def sort_machines(self) -> None:
        """
        Sorts the machines in the observation

        :return: None
        """
        self.machines = sorted(self.machines, key=lambda x: int(x.ips[0].rsplit(".", 1)[-1]), reverse=False)

    def cleanup(self) -> None:
        """
        Cleans up the machines in the observation

        :return: None
        """
        if self.docker_stats_consumer_thread is not None:
            self.docker_stats_consumer_thread.running = False
            self.docker_stats_consumer_thread.consumer.close()
        if self.client_population_consumer_thread is not None:
            self.client_population_consumer_thread.running = False
            self.client_population_consumer_thread.consumer.close()
        if self.aggregated_snort_ids_log_consumer_thread is not None:
            self.aggregated_snort_ids_log_consumer_thread.running = False
            self.aggregated_snort_ids_log_consumer_thread.consumer.close()
        if self.aggregated_snort_ids_rule_log_consumer_thread is not None:
            self.aggregated_snort_ids_rule_log_consumer_thread.running = False
            self.aggregated_snort_ids_rule_log_consumer_thread.consumer.close()
        if self.aggregated_ossec_ids_log_consumer_thread is not None:
            self.aggregated_ossec_ids_log_consumer_thread.running = False
            self.aggregated_ossec_ids_log_consumer_thread.consumer.close()
        if self.attacker_actions_consumer_thread is not None:
            self.attacker_actions_consumer_thread.running = False
            self.attacker_actions_consumer_thread.consumer.close()
        if self.defender_actions_consumer_thread is not None:
            self.defender_actions_consumer_thread.running = False
            self.defender_actions_consumer_thread.consumer.close()
        if self.aggregated_host_metrics_thread is not None:
            self.aggregated_host_metrics_thread.running = False
        for m in self.machines:
            m.cleanup()

    def reset_metric_lists(self) -> None:
        """
        Resets the metric lists

        :return: None
        """
        if self.aggregated_snort_ids_log_consumer_thread is None or \
                self.aggregated_snort_ids_rule_log_consumer_thread is None or \
                self.aggregated_ossec_ids_log_consumer_thread is None or \
                self.docker_stats_consumer_thread is None or \
                self.client_population_consumer_thread is None or \
                self.aggregated_host_metrics_thread is None:
            raise ValueError("At least one of the objects is None")

        self.aggregated_snort_ids_log_consumer_thread.snort_ids_alert_counters_list = []
        self.aggregated_snort_ids_rule_log_consumer_thread.snort_ids_rule_counters_list = []
        self.aggregated_ossec_ids_log_consumer_thread.ossec_ids_alert_counters_list = []
        self.docker_stats_consumer_thread.docker_stats_list = []
        self.client_population_consumer_thread.client_population_metrics_list = []
        self.aggregated_host_metrics_thread.host_metrics_list = []

    def average_metric_lists(self):
        """
        :return: computes the averages of the metric lists
        """
        if self.aggregated_snort_ids_log_consumer_thread is None or \
                self.aggregated_snort_ids_rule_log_consumer_thread is None or \
                self.aggregated_ossec_ids_log_consumer_thread is None or \
                self.docker_stats_consumer_thread is None or \
                self.client_population_consumer_thread is None or \
                self.aggregated_host_metrics_thread is None:
            raise ValueError("At least one of the objects is None")
        self.avg_snort_ids_alert_counters = \
            self.aggregated_snort_ids_log_consumer_thread.get_aggregated_ids_alert_counters()
        self.avg_snort_ids_rule_counters = \
            self.aggregated_snort_ids_rule_log_consumer_thread.get_aggregated_ids_rule_counters()
        self.avg_ossec_ids_alert_counters = \
            self.aggregated_ossec_ids_log_consumer_thread.get_aggregated_ids_alert_counters()
        self.avg_docker_stats = self.docker_stats_consumer_thread.get_average_docker_stats()
        self.avg_aggregated_host_metrics = self.aggregated_host_metrics_thread.get_average_aggregated_host_metrics()
        self.avg_client_population_metrics = \
            self.client_population_consumer_thread.get_average_client_population_metrics()

    def get_action_ips(self, a: EmulationDefenderAction, emulation_env_config: EmulationEnvConfig) -> List[str]:
        """
        Gets the ips of the node that a defender action is targeted for

        :param a: the action
        :param emulation_env_config: the emulation env config
        :return: the ip of the target node
        """
        if a.index == -1:
            return emulation_env_config.topology_config.subnetwork_masks
        if a.index < len(self.machines):
            return self.machines[a.index].ips
        return a.ips

    def copy(self) -> "EmulationDefenderObservationState":
        """
        :return: a copy of the object
        """
        if self.client_population_metrics is None or self.docker_stats is None or \
                self.snort_ids_alert_counters is None or self.ossec_ids_alert_counters is None or \
                self.attacker_actions is None or self.defender_actions is None or \
                self.aggregated_host_metrics is None or \
                self.snort_ids_rule_counters is None or \
                self.avg_aggregated_host_metrics is None:
            raise ValueError("At least of the objects is None")
        c = EmulationDefenderObservationState(
            kafka_config=self.kafka_config,
            client_population_metrics=self.client_population_metrics.copy(), docker_stats=self.docker_stats.copy(),
            snort_ids_alert_counters=self.snort_ids_alert_counters.copy(),
            ossec_ids_alert_counters=self.ossec_ids_alert_counters.copy(),
            attacker_actions=self.attacker_actions.copy(),
            defender_actions=self.defender_actions.copy(), aggregated_host_metrics=self.aggregated_host_metrics.copy(),
            snort_ids_rule_counters=self.snort_ids_rule_counters.copy(),
        )
        c.actions_tried = self.actions_tried.copy()
        c.avg_snort_ids_alert_counters = self.avg_snort_ids_alert_counters.copy()
        c.avg_snort_ids_rule_counters = self.avg_snort_ids_rule_counters.copy()
        c.avg_ossec_ids_alert_counters = self.avg_ossec_ids_alert_counters.copy()
        c.avg_docker_stats = self.avg_docker_stats.copy()
        c.avg_aggregated_host_metrics = self.avg_aggregated_host_metrics.copy()
        c.avg_client_population_metrics = self.avg_client_population_metrics.copy()

        for m in self.machines:
            c.machines.append(m.copy())
        return c

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        if self.attacker_actions is None:
            raise ValueError("attacker_Actions is not iterable")
        if self.defender_actions is None:
            raise ValueError("defender_actions is not iterable")
        return f"client_population_metrics: {self.client_population_metrics}," \
               f"docker_stats: {self.docker_stats}," \
               f"snort_ids_alert_counters: {self.snort_ids_alert_counters}," \
               f"snort_ids_rule_counters: {self.snort_ids_rule_counters}," \
               f"ossec_ids_alert_counters: {self.ossec_ids_alert_counters}," \
               f"aggregated_host_metrics: {self.aggregated_host_metrics}" \
               f"attacker_actions: {list(map(lambda x: str(x), self.attacker_actions))}," \
               f"defender_actions: {list(map(lambda x: str(x), self.defender_actions))}\n," \
               f"avg_snort_ids_alert_counters: {self.avg_snort_ids_alert_counters}," \
               f"avg_snort_ids_rule_counters: {self.avg_snort_ids_rule_counters}," \
               f"avg_ossec_ids_alert_counters: {self.avg_ossec_ids_alert_counters}," \
               f"avg_docker_stats: {self.avg_docker_stats}," \
               f"avg_aggregated_host_metrics: {self.avg_aggregated_host_metrics}," \
               f"avg_client_population_metrics: {self.avg_client_population_metrics}" \
            + "\n".join([str(i) + ":" + str(self.machines[i]) for i in range(len(self.machines))])

    @staticmethod
    def from_json_file(json_file_path: str) -> "EmulationDefenderObservationState":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return EmulationDefenderObservationState.from_dict(json.loads(json_str))

    def num_attributes(self) -> int:
        """
        :return: The number of attribute of the DTO
        """
        if self.defender_actions is None:
            raise ValueError("defender_action is None and thus has no size")
        if self.attacker_actions is None:
            raise ValueError("attacker_action is None and thus has no size")
        num_attributes = 0
        if self.client_population_metrics is not None:
            num_attributes = num_attributes + self.client_population_metrics.num_attributes()
        if self.docker_stats is not None:
            num_attributes = num_attributes + self.docker_stats.num_attributes()
        if self.snort_ids_alert_counters is not None:
            num_attributes = num_attributes + self.snort_ids_alert_counters.num_attributes()
        if self.snort_ids_rule_counters is not None:
            num_attributes = num_attributes + 1
        if self.ossec_ids_alert_counters is not None:
            num_attributes = num_attributes + self.ossec_ids_alert_counters.num_attributes()
        if self.aggregated_host_metrics is not None:
            num_attributes = num_attributes + self.aggregated_host_metrics.num_attributes()
        if len(self.defender_actions) > 0:
            num_attributes = num_attributes + len(self.defender_actions) * self.defender_actions[0].num_attributes()
        if len(self.attacker_actions) > 0:
            num_attributes = num_attributes + len(self.attacker_actions) * self.attacker_actions[0].num_attributes()
        return num_attributes

    @staticmethod
    def schema() -> "EmulationDefenderObservationState":
        """
        :return: get the schema of the DTO
        """
        return EmulationDefenderObservationState(kafka_config=KafkaConfig.schema(),
                                                 client_population_metrics=ClientPopulationMetrics.schema(),
                                                 docker_stats=DockerStats.schema(),
                                                 snort_ids_alert_counters=SnortIdsAlertCounters.schema(),
                                                 ossec_ids_alert_counters=OSSECIdsAlertCounters.schema(),
                                                 aggregated_host_metrics=HostMetrics.schema(),
                                                 defender_actions=[EmulationDefenderAction.schema()],
                                                 attacker_actions=[EmulationAttackerAction.schema()],
                                                 snort_ids_rule_counters=SnortIdsRuleCounters.schema())
