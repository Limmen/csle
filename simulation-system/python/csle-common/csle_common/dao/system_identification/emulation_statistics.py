from typing import Dict, Any, List
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

    def __init__(self, emulation_name: str, descr: str=""):
        """
        Initializes the statistics DTO

        :param emulation_name: the name of the emulation that the statistics is linked to
        :param descr: a free text description of the statistics
        """
        self.emulation_name = emulation_name
        self.descr = descr
        self.initial_distributions = self.initialize_counters(
            d={}, labels=collector_constants.LOG_SINK.ALL_INITIAL_LABELS)
        self.conditionals = {}
        self.conditionals[constants.SYSTEM_IDENTIFICATION.INTRUSION_CONDITIONAL] = \
            EmulationStatistics.initialize_counters(d={}, labels=collector_constants.LOG_SINK.ALL_DELTA_LABELS)
        self.conditionals[constants.SYSTEM_IDENTIFICATION.NO_INTRUSION_CONDITIONAL] = \
            EmulationStatistics.initialize_counters(d={}, labels=collector_constants.LOG_SINK.ALL_DELTA_LABELS)
        self.id = -1

    @staticmethod
    def initialize_counters(d: Dict[str, Dict[int,int]], labels: List[str]) -> Dict[str, Dict[int,int]]:
        """
        Initializes counters for a given dict
        :param d: the dict to initialzie
        :return: the initialized dict
        """

        for label in labels:
            d[label] = {}

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
            s_prime.defender_obs_state.ids_alert_counters)
        for i in range(len(alert_deltas)):
            if alert_deltas[i] in d[alert_labels[i]]:
                d[alert_labels[i]][alert_deltas[i]] += 1
            else:
                d[alert_labels[i]][alert_deltas[i]] = 1
        docker_stats_deltas, docker_stats_labels = s.defender_obs_state.docker_stats.get_deltas(
            stats_prime=s_prime.defender_obs_state.docker_stats)
        for i in range(len(docker_stats_deltas)):
            if docker_stats_deltas[i] in d[docker_stats_labels[i]]:
                d[docker_stats_labels[i]][docker_stats_deltas[i]] += 1
            else:
                d[docker_stats_labels[i]][docker_stats_deltas[i]] = 1

        client_population_metrics_deltas, client_population_metrics_labels = \
            s.defender_obs_state.client_population_metrics.get_deltas(
            stats_prime=s_prime.defender_obs_state.client_population_metrics)
        for i in range(len(client_population_metrics_deltas)):
            if client_population_metrics_deltas[i] in d[client_population_metrics_labels[i]]:
                d[client_population_metrics_labels[i]][client_population_metrics_deltas[i]] += 1
            else:
                d[client_population_metrics_labels[i]][client_population_metrics_deltas[i]] = 1
        aggregated_host_metrics_deltas, aggregated_host_metrics_labels = \
            s.defender_obs_state.aggregated_host_metrics.get_deltas(
                stats_prime=s_prime.defender_obs_state.aggregated_host_metrics)
        for i in range(len(aggregated_host_metrics_deltas)):
            if aggregated_host_metrics_deltas[i] in d[aggregated_host_metrics_labels[i]]:
                d[aggregated_host_metrics_labels[i]][aggregated_host_metrics_deltas[i]] += 1
            else:
                d[aggregated_host_metrics_labels[i]][aggregated_host_metrics_deltas[i]] = 1

    def update_delta_statistics(self, s: EmulationEnvState, s_prime: EmulationEnvState, a1: EmulationDefenderAction,
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

    def update_initial_statistics(self, s: EmulationEnvState) -> None:
        """
        Updates the emulation statistics for the initial state

        :param s: the initial state
        :return: None
        """
        docker_stats_values, docker_stats_labels = s.defender_obs_state.docker_stats.get_values()
        for i in range(len(docker_stats_values)):
            if docker_stats_values[i] in self.initial_distributions[docker_stats_labels[i]]:
                self.initial_distributions[docker_stats_labels[i]][docker_stats_values[i]] += 1
            else:
                self.initial_distributions[docker_stats_labels[i]][docker_stats_values[i]] = 1

        client_population_metrics_values, client_population_metrics_labels = \
            s.defender_obs_state.client_population_metrics.get_values()
        for i in range(len(client_population_metrics_values)):
            if client_population_metrics_values[i] in self.initial_distributions[client_population_metrics_labels[i]]:
                self.initial_distributions[client_population_metrics_labels[i]][client_population_metrics_values[i]] += 1
            else:
                self.initial_distributions[client_population_metrics_labels[i]][client_population_metrics_values[i]] = 1
        aggregated_host_metrics_values, aggregated_host_metrics_labels = \
            s.defender_obs_state.aggregated_host_metrics.get_values()
        for i in range(len(aggregated_host_metrics_values)):
            if aggregated_host_metrics_values[i] in self.initial_distributions[aggregated_host_metrics_labels[i]]:
                self.initial_distributions[aggregated_host_metrics_labels[i]][aggregated_host_metrics_values[i]] += 1
            else:
                self.initial_distributions[aggregated_host_metrics_labels[i]][aggregated_host_metrics_values[i]] = 1

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"conditionals:{self.conditionals}, initial distributions: {self.initial_distributions}" \
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
            descr=d["descr"]
        )
        obj.conditionals = d["conditionals"]
        obj.initial_distributions = d["initial_distributions"]
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
        d["initial_distributions"] = self.initial_distributions
        d["emulation_name"] = self.emulation_name
        return d

