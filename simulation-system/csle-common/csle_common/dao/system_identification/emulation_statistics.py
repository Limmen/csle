from typing import Dict, Any
import numpy as np
import csle_common.constants.constants as constants
import csle_collector.constants.constants as collector_constants
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId


class EmulationStatistics:
    """
    DTO representing delta-statistics measured from teh emulation
    """

    def __init__(self, emulation_name: str, max_counts : int = 1000, descr: str=""):
        """
        Initializes the statistics DTO

        :param emulation_name: the name of the emulation that the statistics is linked to
        :param descr: a free text description of the statistics
        :param max_counts: the max number a given counter
        """
        self.emulation_name = emulation_name
        self.descr = descr
        self.max_counts = max_counts
        self.ids_counter_labels = collector_constants.LOG_SINK.IDS_ALERTS_LABELS
        self.host_metrics_counter_labels = collector_constants.LOG_SINK.HOST_METRICS_LABELS
        self.docker_stats_counter_labels = collector_constants.LOG_SINK.DOCKER_STATS_COUNTER_LABELS
        self.docker_stats_percent_labels = collector_constants.LOG_SINK.DOCKER_STATS_PERCENT_LABELS
        self.client_metrics_labels = collector_constants.LOG_SINK.CLIENT_POPULATION_METRIC_LABELS
        self.counter_labels = self.ids_counter_labels \
                              + self.host_metrics_counter_labels + self.docker_stats_counter_labels \
                              + self.client_metrics_labels
        self.percent_labels = self.docker_stats_percent_labels
        self.conditionals = {}
        self.conditionals[constants.SYSTEM_IDENTIFICATION.INTRUSION_CONDITIONAL] = self.initialize_counters(d={})
        self.conditionals[constants.SYSTEM_IDENTIFICATION.NO_INTRUSION_CONDITIONAL] = self.initialize_counters(d={})
        self.id = -1

    def initialize_counters(self, d: Dict[str, Dict[int,int]]) -> Dict[str, Dict[int,int]]:
        """
        Initializes counters for a given dict
        :param d: the dict to initialzie
        :return: the initialized dict
        """

        for label in self.counter_labels:
            d[label] = {}
            for val in range(0, self.max_counts+1):
                d[label][val] = 0

        percent_space = np.array(list(range(0,101,1)))/100
        for label in self.percent_labels:
            d[label] = {}
            for val in percent_space:
                d[label][val] = 0

        return d

    def update_counters(self, d: Dict, s: EmulationEnvState, s_prime: EmulationEnvState) -> None:
        """
        Updates the delta counters for a specific dict based on a state transition s->s'

        :param d: the dict to update
        :param s: the current state
        :param s_prime: the new state
        :return: None
        """
        alert_deltas, alert_labels = s.defender_obs_state.ids_alert_counters.get_deltas(
            s_prime.defender_obs_state.ids_alert_counters, max_counter=self.max_counts)
        for i in range(len(alert_deltas)):
            d[alert_labels[i]][alert_deltas[i]] += 1
        docker_stats_deltas, docker_stats_labels = s.defender_obs_state.docker_stats.get_deltas(
            stats_prime=s_prime.defender_obs_state.docker_stats, max_counter=self.max_counts)
        for i in range(len(docker_stats_deltas)):
            d[docker_stats_labels[i]][docker_stats_deltas[i]] += 1

        client_population_metrics_deltas, client_population_metrics_labels = \
            s.defender_obs_state.client_population_metrics.get_deltas(
            stats_prime=s_prime.defender_obs_state.client_population_metrics, max_counter=self.max_counts)
        for i in range(len(client_population_metrics_deltas)):
            d[client_population_metrics_labels[i]][client_population_metrics_deltas[i]] += 1

        aggregated_host_metrics_deltas, aggregated_host_metrics_labels = \
            s.defender_obs_state.aggregated_host_metrics.get_deltas(
                stats_prime=s_prime.defender_obs_state.aggregated_host_metrics, max_counter=self.max_counts)
        for i in range(len(aggregated_host_metrics_deltas)):
            d[aggregated_host_metrics_labels[i]][aggregated_host_metrics_deltas[i]] += 1

    def update_statistics(self, s: EmulationEnvState, s_prime: EmulationEnvState, a1: EmulationDefenderAction,
                        a2: EmulationAttackerAction) -> None:
        """
        Updates the emulation statistics (delta counters) with a given transition (s, a1, a2) -> (s')

        :param s: the previous state
        :param s_prime: the new state
        :param a1: the defender action
        :param a2: the attacker action
        :return: None
        """
        if a2.id == EmulationAttackerActionId.CONTINUE:
            self.update_counters(d=self.conditionals[constants.SYSTEM_IDENTIFICATION.NO_INTRUSION_CONDITIONAL],
                                 s=s, s_prime=s_prime)
        else:
            self.update_counters(d=self.conditionals[constants.SYSTEM_IDENTIFICATION.INTRUSION_CONDITIONAL],
                                 s=s, s_prime=s_prime)

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"conditionals:{self.conditionals}" \
               f"emulation_name: {self.emulation_name}, description: {self.descr}"

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EmulationStatistics":
        """
        Converts a dict representation of the object to a DTO

        :param d: the dict to convert
        :return: the created instance
        """
        obj = EmulationStatistics(
            emulation_name=d["emulation_name"],
            max_counts=d["max_counts"],
            descr=d["descr"]
        )
        obj.conditionals = d["conditionals"]
        if "id" in d:
            obj.id = d["id"]
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["descr"] = self.descr
        d["id"] = self.id
        d["conditionals"] = self.conditionals
        d["max_counts"] = self.max_counts
        d["emulation_name"] = self.emulation_name
        return d

