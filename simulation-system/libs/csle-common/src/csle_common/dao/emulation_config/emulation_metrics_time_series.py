from typing import List, Dict, Any
from csle_collector.snort_ids_manager.dao.snort_ids_alert_counters import SnortIdsAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_ip_alert_counters import SnortIdsIPAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_rule_counters import SnortIdsRuleCounters
from csle_collector.ossec_ids_manager.dao.ossec_ids_alert_counters import OSSECIdsAlertCounters
from csle_collector.client_manager.client_population_metrics import ClientPopulationMetrics
from csle_collector.docker_stats_manager.dao.docker_stats import DockerStats
from csle_collector.host_manager.dao.host_metrics import HostMetrics
from csle_ryu.dao.avg_port_statistic import AvgPortStatistic
from csle_ryu.dao.avg_flow_statistic import AvgFlowStatistic
from csle_ryu.dao.flow_statistic import FlowStatistic
from csle_ryu.dao.port_statistic import PortStatistic
from csle_ryu.dao.agg_flow_statistic import AggFlowStatistic
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_base.json_serializable import JSONSerializable


class EmulationMetricsTimeSeries(JSONSerializable):
    """
    DTO containing time series data from the emulation
    """

    def __init__(self, client_metrics: List[ClientPopulationMetrics], aggregated_docker_stats: List[DockerStats],
                 docker_host_stats: Dict[str, List[DockerStats]], host_metrics: Dict[str, List[HostMetrics]],
                 aggregated_host_metrics: List[HostMetrics],
                 defender_actions: List[EmulationDefenderAction], attacker_actions: List[EmulationAttackerAction],
                 agg_snort_ids_metrics: List[SnortIdsAlertCounters], emulation_env_config: EmulationEnvConfig,
                 ossec_host_alert_counters: Dict[str, List[OSSECIdsAlertCounters]],
                 aggregated_ossec_host_alert_counters: List[OSSECIdsAlertCounters],
                 openflow_flow_stats: List[FlowStatistic], openflow_port_stats: List[PortStatistic],
                 avg_openflow_flow_stats: List[AvgFlowStatistic], avg_openflow_port_stats: List[AvgPortStatistic],
                 openflow_flow_metrics_per_switch: Dict[str, List[FlowStatistic]],
                 openflow_port_metrics_per_switch: Dict[str, List[PortStatistic]],
                 openflow_flow_avg_metrics_per_switch: Dict[str, List[AvgFlowStatistic]],
                 openflow_port_avg_metrics_per_switch: Dict[str, List[AvgPortStatistic]],
                 agg_openflow_flow_metrics_per_switch: Dict[str, List[AggFlowStatistic]],
                 agg_openflow_flow_stats: List[AggFlowStatistic],
                 snort_ids_ip_metrics: Dict[str, List[SnortIdsIPAlertCounters]],
                 agg_snort_ids_rule_metrics: List[SnortIdsRuleCounters],
                 snort_alert_metrics_per_ids: Dict[str, List[SnortIdsAlertCounters]],
                 snort_rule_metrics_per_ids: Dict[str, List[SnortIdsRuleCounters]]):
        """
        Initializes the DTO

        :param client_metrics: Time series data with information about the client population
        :param aggregated_docker_stats: Time series data with average docker statistics
        :param docker_host_stats: Time series data with docker statistics per host
        :param host_metrics: Time series data with general host metrics
        :param aggregated_host_metrics: Time series data with aggregated host metrics
        :param defender_actions: Time series data with defender actions
        :param attacker_actions: Time series data with attacker actions
        :param agg_snort_ids_metrics: Time series data with Snort IDS metrics
        :param emulation_env_config: the emulation config
        :param ossec_host_alert_counters: Time series data with ossec alert counters per host
        :param aggregated_ossec_host_alert_counters: Time series data with aggregated ossec alert counters
        :param openflow_flow_stats: openflow flow statistics
        :param openflow_port_stats: openflow port statistics
        :param avg_openflow_flow_stats: average openflow flow statistics per switch
        :param avg_openflow_port_stats: average openflow port statistics per switch
        :param openflow_flow_metrics_per_switch: openflow flow statistics per aggregated per switch
        :param openflow_port_metrics_per_switch: openflow port statistics per aggregated per switch
        :param openflow_flow_avg_metrics_per_switch: average openflow flow statistics per aggregated per switch
        :param openflow_port_avg_metrics_per_switch: average openflow port statistics per aggregated per switch
        :param agg_openflow_flow_stats: aggregated openflow flow statistics
        :param agg_openflow_flow_metrics_per_switch: aggregated openflow flow statistics aggregatd per switch
        :param snort_ids_ip_metrics: Time series data with Snort IDS metrics per IP
        :param agg_snort_ids_rule_metrics: Time series data with Snort IDS metrics per rule
        :param snort_alert_metrics_per_ids: Time series data with Snort IDS alert metrics per IDS
        :param snort_rule_metrics_per_ids: Time series data with Snort IDS rule metrics per IDS
        """
        self.client_metrics = client_metrics
        self.aggregated_docker_stats = aggregated_docker_stats
        self.docker_host_stats = docker_host_stats
        self.host_metrics = host_metrics
        self.defender_actions = defender_actions
        self.attacker_actions = attacker_actions
        self.agg_snort_ids_metrics = agg_snort_ids_metrics
        self.aggregated_host_metrics = aggregated_host_metrics
        self.emulation_env_config = emulation_env_config
        self.ossec_host_alert_counters = ossec_host_alert_counters
        self.aggregated_ossec_host_alert_counters = aggregated_ossec_host_alert_counters
        self.openflow_flow_stats = openflow_flow_stats
        self.openflow_port_stats = openflow_port_stats
        self.avg_openflow_flow_stats = avg_openflow_flow_stats
        self.avg_openflow_port_stats = avg_openflow_port_stats
        self.openflow_flow_metrics_per_switch = openflow_flow_metrics_per_switch
        self.openflow_port_metrics_per_switch = openflow_port_metrics_per_switch
        self.openflow_flow_avg_metrics_per_switch = openflow_flow_avg_metrics_per_switch
        self.openflow_port_avg_metrics_per_switch = openflow_port_avg_metrics_per_switch
        self.agg_openflow_flow_stats = agg_openflow_flow_stats
        self.agg_openflow_flow_metrics_per_switch = agg_openflow_flow_metrics_per_switch
        self.snort_ids_ip_metrics = snort_ids_ip_metrics
        self.agg_snort_ids_rule_metrics = agg_snort_ids_rule_metrics
        self.snort_alert_metrics_per_ids = snort_alert_metrics_per_ids
        self.snort_rule_metrics_per_ids = snort_rule_metrics_per_ids

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EmulationMetricsTimeSeries":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the converted instance
        """
        docker_host_stats = {}
        for k, v in d["docker_host_stats"].items():
            docker_host_stats[k] = list(map(lambda x: DockerStats.from_dict(x), v))
        host_metrics = {}
        for k, v in d["host_metrics"].items():
            host_metrics[k] = list(map(lambda x: HostMetrics.from_dict(x), v))
        ossec_host_alerts = {}
        for k, v in d["ossec_host_alert_counters"].items():
            ossec_host_alerts[k] = list(map(lambda x: OSSECIdsAlertCounters.from_dict(x), v))

        openflow_flow_metrics_per_switch = {}
        for k, v in d["openflow_flow_metrics_per_switch"].items():
            openflow_flow_metrics_per_switch[k] = list(map(lambda x: FlowStatistic.from_dict(x), v))

        openflow_port_metrics_per_switch = {}
        for k, v in d["openflow_port_metrics_per_switch"].items():
            openflow_port_metrics_per_switch[k] = list(map(lambda x: PortStatistic.from_dict(x), v))

        openflow_flow_avg_metrics_per_switch = {}
        for k, v in d["openflow_flow_avg_metrics_per_switch"].items():
            openflow_flow_avg_metrics_per_switch[k] = list(map(lambda x: AvgFlowStatistic.from_dict(x), v))

        openflow_port_avg_metrics_per_switch = {}
        for k, v in d["openflow_port_avg_metrics_per_switch"].items():
            openflow_port_avg_metrics_per_switch[k] = list(map(lambda x: AvgPortStatistic.from_dict(x), v))

        agg_openflow_flow_metrics_per_switch = {}
        for k, v in d["agg_openflow_flow_metrics_per_switch"].items():
            agg_openflow_flow_metrics_per_switch[k] = list(map(lambda x: AggFlowStatistic.from_dict(x), v))

        snort_ids_ip_metrics = {}
        for k, v in d["snort_ids_ip_metrics"].items():
            snort_ids_ip_metrics[k] = list(map(lambda x: SnortIdsIPAlertCounters.from_dict(x), v))

        snort_alert_metrics_per_ids = {}
        for k, v in d["snort_alert_metrics_per_ids"].items():
            snort_alert_metrics_per_ids[k] = list(map(lambda x: SnortIdsAlertCounters.from_dict(x), v))

        snort_rule_metrics_per_ids = {}
        for k, v in d["snort_rule_metrics_per_ids"].items():
            snort_rule_metrics_per_ids[k] = list(map(lambda x: SnortIdsRuleCounters.from_dict(x), v))

        obj = EmulationMetricsTimeSeries(
            client_metrics=list(map(lambda x: ClientPopulationMetrics.from_dict(x), d["client_metrics"])),
            aggregated_docker_stats=list(map(lambda x: DockerStats.from_dict(x), d["aggregated_docker_stats"])),
            docker_host_stats=docker_host_stats,
            host_metrics=host_metrics,
            defender_actions=list(map(lambda x: EmulationDefenderAction.from_dict(x), d["defender_actions"])),
            attacker_actions=list(map(lambda x: EmulationAttackerAction.from_dict(x), d["attacker_actions"])),
            agg_snort_ids_metrics=list(map(lambda x: SnortIdsAlertCounters.from_dict(x), d["agg_snort_ids_metrics"])),
            aggregated_host_metrics=list(map(lambda x: HostMetrics.from_dict(x), d["aggregated_host_metrics"])),
            emulation_env_config=EmulationEnvConfig.from_dict(d["emulation_env_config"]),
            ossec_host_alert_counters=ossec_host_alerts,
            aggregated_ossec_host_alert_counters=list(map(lambda x: OSSECIdsAlertCounters.from_dict(x),
                                                          d["aggregated_ossec_host_alert_counters"])),
            openflow_flow_stats=list(map(lambda x: FlowStatistic.from_dict(x), d["openflow_flow_stats"])),
            openflow_port_stats=list(map(lambda x: PortStatistic.from_dict(x), d["openflow_port_stats"])),
            avg_openflow_flow_stats=list(map(lambda x: AvgFlowStatistic.from_dict(x), d["avg_openflow_flow_stats"])),
            avg_openflow_port_stats=list(map(lambda x: AvgPortStatistic.from_dict(x), d["avg_openflow_port_stats"])),
            openflow_flow_metrics_per_switch=openflow_flow_metrics_per_switch,
            openflow_port_metrics_per_switch=openflow_port_metrics_per_switch,
            openflow_flow_avg_metrics_per_switch=openflow_flow_avg_metrics_per_switch,
            openflow_port_avg_metrics_per_switch=openflow_port_avg_metrics_per_switch,
            agg_openflow_flow_stats=list(map(lambda x: AggFlowStatistic.from_dict(x), d["agg_openflow_flow_stats"])),
            agg_openflow_flow_metrics_per_switch=agg_openflow_flow_metrics_per_switch,
            snort_ids_ip_metrics=snort_ids_ip_metrics,
            agg_snort_ids_rule_metrics=list(map(lambda x: SnortIdsRuleCounters.from_dict(x),
                                                d["agg_snort_ids_rule_metrics"])),
            snort_alert_metrics_per_ids=snort_alert_metrics_per_ids,
            snort_rule_metrics_per_ids=snort_rule_metrics_per_ids)
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["client_metrics"] = list(map(lambda x: x.to_dict(), self.client_metrics))
        d["aggregated_docker_stats"] = list(map(lambda x: x.to_dict(), self.aggregated_docker_stats))
        d["docker_host_stats"] = {}
        for k, v in self.docker_host_stats.items():
            d["docker_host_stats"][k] = list(map(lambda x: x.to_dict(), v))
        d["host_metrics"] = {}
        for k, v in self.host_metrics.items():
            d["host_metrics"][k] = list(map(lambda x: x.to_dict(), v))
        d["defender_actions"] = list(map(lambda x: x.to_dict(), self.defender_actions))
        d["attacker_actions"] = list(map(lambda x: x.to_dict(), self.attacker_actions))
        d["agg_snort_ids_metrics"] = list(map(lambda x: x.to_dict(), self.agg_snort_ids_metrics))
        d["aggregated_host_metrics"] = list(map(lambda x: x.to_dict(), self.aggregated_host_metrics))
        d["emulation_env_config"] = self.emulation_env_config.to_dict()
        d["aggregated_ossec_host_alert_counters"] = list(map(lambda x: x.to_dict(),
                                                             self.aggregated_ossec_host_alert_counters))
        d["ossec_host_alert_counters"] = {}
        for k, v in self.ossec_host_alert_counters.items():
            d["ossec_host_alert_counters"][k] = list(map(lambda x: x.to_dict(), v))
        d["openflow_flow_stats"] = list(map(lambda x: x.to_dict(), self.openflow_flow_stats))
        d["openflow_port_stats"] = list(map(lambda x: x.to_dict(), self.openflow_port_stats))
        d["avg_openflow_flow_stats"] = list(map(lambda x: x.to_dict(), self.avg_openflow_flow_stats))
        d["avg_openflow_port_stats"] = list(map(lambda x: x.to_dict(), self.avg_openflow_port_stats))

        d["openflow_flow_metrics_per_switch"] = {}
        for k, v in self.openflow_flow_metrics_per_switch.items():
            d["openflow_flow_metrics_per_switch"][k] = list(map(lambda x: x.to_dict(), v))

        d["openflow_port_metrics_per_switch"] = {}
        for k, v in self.openflow_port_metrics_per_switch.items():
            d["openflow_port_metrics_per_switch"][k] = list(map(lambda x: x.to_dict(), v))

        d["openflow_flow_avg_metrics_per_switch"] = {}
        for k, v in self.openflow_flow_avg_metrics_per_switch.items():
            d["openflow_flow_avg_metrics_per_switch"][k] = list(map(lambda x: x.to_dict(), v))

        d["openflow_port_avg_metrics_per_switch"] = {}
        for k, v in self.openflow_port_avg_metrics_per_switch.items():
            d["openflow_port_avg_metrics_per_switch"][k] = list(map(lambda x: x.to_dict(), v))

        d["agg_openflow_flow_metrics_per_switch"] = {}
        for k, v in self.agg_openflow_flow_metrics_per_switch.items():
            d["agg_openflow_flow_metrics_per_switch"][k] = list(map(lambda x: x.to_dict(), v))

        d["agg_openflow_flow_stats"] = list(map(lambda x: x.to_dict(), self.agg_openflow_flow_stats))

        d["snort_ids_ip_metrics"] = {}
        for k, v in self.snort_ids_ip_metrics.items():
            d["snort_ids_ip_metrics"][k] = list(map(lambda x: x.to_dict(), v))

        d["agg_snort_ids_rule_metrics"] = list(map(lambda x: x.to_dict(), self.agg_snort_ids_rule_metrics))

        d["snort_alert_metrics_per_ids"] = {}
        for k, v in self.snort_alert_metrics_per_ids.items():
            d["snort_alert_metrics_per_ids"][k] = list(map(lambda x: x.to_dict(), v))

        d["snort_rule_metrics_per_ids"] = {}
        for k, v in self.snort_rule_metrics_per_ids.items():
            d["snort_rule_metrics_per_ids"][k] = list(map(lambda x: x.to_dict(), v))

        return d

    def __str__(self) -> str:
        """
        :return: a string representation
        """
        return f"client_metrics: {list(map(lambda x: str(x), self.client_metrics))}," \
               f"aggregated_docker_stats: {list(map(lambda x: str(x), self.aggregated_docker_stats))}," \
               f"docker_host_stats: {list(map(lambda x: str(x), self.docker_host_stats))}," \
               f"host_metrics: {list(map(lambda x: str(x), self.host_metrics))}," \
               f"defender_actions: {list(map(lambda x: str(x), self.defender_actions))}," \
               f"attacker_actions: {list(map(lambda x: str(x), self.attacker_actions))}," \
               f"agg_snort_ids_metrics: {list(map(lambda x: str(x), self.agg_snort_ids_metrics))}," \
               f"aggregated_host_metrics: {list(map(lambda x: str(x), self.aggregated_host_metrics))}," \
               f"config: {self.emulation_env_config}," \
               f"aggregated_ossec_host_alert_counters: {self.aggregated_ossec_host_alert_counters}," \
               f"ossec_host_alert_counters: {self.ossec_host_alert_counters}," \
               f"openflow_flow_stats: {self.openflow_flow_stats}, openflow_port_stats: {self.openflow_port_stats}," \
               f"avg_openflow_flow_stats: {self.avg_openflow_flow_stats}, " \
               f"avg_openflow_port_stats: {self.avg_openflow_port_stats}," \
               f"openflow_flow_metrics_per_switch: {self.openflow_flow_metrics_per_switch}," \
               f"openflow_port_metrics_per_switch: {self.openflow_port_metrics_per_switch}," \
               f"openflow_flow_avg_metrics_per_switch: {self.openflow_flow_avg_metrics_per_switch}," \
               f"openflow_port_avg_metrics_per_switch: {self.openflow_port_avg_metrics_per_switch}," \
               f"agg_openflow_flow_stats: {self.agg_openflow_flow_stats}," \
               f"agg_openflow_flow_metrics_per_switch: {self.agg_openflow_flow_metrics_per_switch}," \
               f"snort_ids_ip_metrics: {self.snort_ids_ip_metrics}," \
               f"agg_snort_ids_rule_metrics: {self.agg_snort_ids_rule_metrics}," \
               f"snort_alert_metrics_per_ids: {self.snort_alert_metrics_per_ids}," \
               f"snort_rule_metrics_per_ids: {self.snort_rule_metrics_per_ids}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "EmulationMetricsTimeSeries":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return EmulationMetricsTimeSeries.from_dict(json.loads(json_str))
