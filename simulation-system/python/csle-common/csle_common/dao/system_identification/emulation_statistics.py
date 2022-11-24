import math
from typing import Dict, Any, List
import numpy as np
from scipy.special import rel_entr
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

    def __init__(self, emulation_name: str, descr: str = ""):
        """
        Initializes the statistics DTO

        :param emulation_name: the name of the emulation that the statistics is linked to
        :param descr: a free text description of the statistics
        """
        self.emulation_name = emulation_name
        self.descr = descr
        self.initial_distributions_counts = self.initialize_counters(
            d={}, labels=collector_constants.KAFKA_CONFIG.ALL_INITIAL_LABELS)
        self.conditionals_counts = {}
        self.conditionals_counts[constants.SYSTEM_IDENTIFICATION.INTRUSION_CONDITIONAL] = \
            EmulationStatistics.initialize_counters(d={}, labels=collector_constants.KAFKA_CONFIG.ALL_DELTA_LABELS)
        self.conditionals_counts[constants.SYSTEM_IDENTIFICATION.NO_INTRUSION_CONDITIONAL] = \
            EmulationStatistics.initialize_counters(d={}, labels=collector_constants.KAFKA_CONFIG.ALL_DELTA_LABELS)
        self.id = -1
        self.means = {}
        self.stds = {}
        self.mins = {}
        self.maxs = {}
        self.conditionals_probs = {}
        self.initial_distributions_probs = {}
        self.initial_means = {}
        self.initial_stds = {}
        self.initial_mins = {}
        self.initial_maxs = {}
        self.conditionals_kl_divergences = {}
        self.num_metrics = 0
        self.num_measurements = 0
        self.num_conditions = 0
        self.conditions = []
        self.metrics = []

    @staticmethod
    def initialize_counters(d: Dict[str, Dict[int, int]], labels: List[str]) -> Dict[str, Dict[int, int]]:
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

        # Snort alerts
        snort_alert_deltas, snort_alert_labels = s.defender_obs_state.avg_snort_ids_alert_counters.get_deltas(
            s_prime.defender_obs_state.avg_snort_ids_alert_counters)
        for i in range(len(snort_alert_deltas)):
            if snort_alert_deltas[i] in d[snort_alert_labels[i]]:
                d[snort_alert_labels[i]][snort_alert_deltas[i]] += 1
            else:
                d[snort_alert_labels[i]][snort_alert_deltas[i]] = 1

        # OSSEC alerts
        ossec_alert_deltas, ossec_alert_labels = s.defender_obs_state.avg_ossec_ids_alert_counters.get_deltas(
            s_prime.defender_obs_state.avg_ossec_ids_alert_counters)
        for i in range(len(ossec_alert_deltas)):
            if ossec_alert_deltas[i] in d[ossec_alert_labels[i]]:
                d[ossec_alert_labels[i]][ossec_alert_deltas[i]] += 1
            else:
                d[ossec_alert_labels[i]][ossec_alert_deltas[i]] = 1

        # Docker stats
        docker_stats_deltas, docker_stats_labels = s.defender_obs_state.avg_docker_stats.get_deltas(
            stats_prime=s_prime.defender_obs_state.avg_docker_stats)
        for i in range(len(docker_stats_deltas)):
            if docker_stats_deltas[i] in d[docker_stats_labels[i]]:
                d[docker_stats_labels[i]][docker_stats_deltas[i]] += 1
            else:
                d[docker_stats_labels[i]][docker_stats_deltas[i]] = 1

        # Client metrics
        client_population_metrics_deltas, client_population_metrics_labels = (
            s.defender_obs_state.avg_client_population_metrics.get_deltas(
                stats_prime=s_prime.defender_obs_state.avg_client_population_metrics))
        for i in range(len(client_population_metrics_deltas)):
            if client_population_metrics_deltas[i] in d[client_population_metrics_labels[i]]:
                d[client_population_metrics_labels[i]][client_population_metrics_deltas[i]] += 1
            else:
                d[client_population_metrics_labels[i]][client_population_metrics_deltas[i]] = 1

        # Host metrics
        aggregated_host_metrics_deltas, aggregated_host_metrics_labels = \
            s.defender_obs_state.avg_aggregated_host_metrics.get_deltas(
                stats_prime=s_prime.defender_obs_state.avg_aggregated_host_metrics)
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

        # Intrusion vs No Intrusion Conditionals
        if a2.id == EmulationAttackerActionId.CONTINUE:
            self.update_counters(d=self.conditionals_counts[constants.SYSTEM_IDENTIFICATION.NO_INTRUSION_CONDITIONAL],
                                 s=s, s_prime=s_prime)
        else:
            self.update_counters(d=self.conditionals_counts[constants.SYSTEM_IDENTIFICATION.INTRUSION_CONDITIONAL],
                                 s=s, s_prime=s_prime)

        logged_in_ips = list(map(lambda x: "_".join(x.ips), filter(
            lambda x: x.logged_in and x.tools_installed and x.backdoor_installed and x.root,
            s.attacker_obs_state.machines)))
        # Action conditionals
        if f"A:{a2.name}_D:{a1.name}_M:{logged_in_ips}" not in self.conditionals_counts:
            self.conditionals_counts[f"A:{a2.name}_D:{a1.name}_M:{logged_in_ips}"] = \
                EmulationStatistics.initialize_counters(d={}, labels=collector_constants.KAFKA_CONFIG.ALL_DELTA_LABELS)
        self.update_counters(
            d=self.conditionals_counts[f"A:{a2.name}_D:{a1.name}_M:{logged_in_ips}"], s=s, s_prime=s_prime)

    def update_initial_statistics(self, s: EmulationEnvState) -> None:
        """
        Updates the emulation statistics for the initial state

        :param s: the initial state
        :return: None
        """
        snort_alert_labels = collector_constants.KAFKA_CONFIG.SNORT_IDS_ALERTS_LABELS
        for i in range(len(snort_alert_labels)):
            if 0 in self.initial_distributions_counts[snort_alert_labels[i]]:
                self.initial_distributions_counts[snort_alert_labels[i]][0] += 1
            else:
                self.initial_distributions_counts[snort_alert_labels[i]][0] = 1

        ossec_alert_labels = collector_constants.KAFKA_CONFIG.OSSEC_IDS_ALERTS_LABELS
        for i in range(len(ossec_alert_labels)):
            if 0 in self.initial_distributions_counts[ossec_alert_labels[i]]:
                self.initial_distributions_counts[ossec_alert_labels[i]][0] += 1
            else:
                self.initial_distributions_counts[ossec_alert_labels[i]][0] = 1

        docker_stats_values, docker_stats_labels = s.defender_obs_state.docker_stats.get_values()
        for i in range(len(docker_stats_values)):
            if docker_stats_values[i] in self.initial_distributions_counts[docker_stats_labels[i]]:
                self.initial_distributions_counts[docker_stats_labels[i]][docker_stats_values[i]] += 1
            else:
                self.initial_distributions_counts[docker_stats_labels[i]][docker_stats_values[i]] = 1

        client_population_metrics_values, client_population_metrics_labels = \
            s.defender_obs_state.client_population_metrics.get_values()
        for i in range(len(client_population_metrics_values)):
            if (client_population_metrics_values[i] in
                    self.initial_distributions_counts[client_population_metrics_labels[i]]):
                self.initial_distributions_counts[
                    client_population_metrics_labels[i]][client_population_metrics_values[i]] += 1
            else:
                self.initial_distributions_counts[
                    client_population_metrics_labels[i]][client_population_metrics_values[i]] = 1
        aggregated_host_metrics_values, aggregated_host_metrics_labels = \
            s.defender_obs_state.aggregated_host_metrics.get_values()
        for i in range(len(aggregated_host_metrics_values)):
            if (aggregated_host_metrics_values[i] in
                    self.initial_distributions_counts[aggregated_host_metrics_labels[i]]):
                self.initial_distributions_counts[
                    aggregated_host_metrics_labels[i]][aggregated_host_metrics_values[i]] += 1
            else:
                self.initial_distributions_counts[aggregated_host_metrics_labels[i]][
                    aggregated_host_metrics_values[i]] = 1

    def compute_descriptive_statistics_and_distributions(self) -> None:
        """
        Computes descriptive statistics and empirical probability distributions based on the counters.

        :return: None
        """
        self.num_measurements = 0
        self.conditions = list(self.conditionals_counts.keys())
        self.num_conditions = len(self.conditions)
        for condition in self.conditionals_counts.keys():
            self.means[condition] = {}
            self.stds[condition] = {}
            self.mins[condition] = {}
            self.maxs[condition] = {}
            self.conditionals_probs[condition] = {}
            for metric in self.conditionals_counts[condition].keys():
                self.conditionals_probs[condition][metric] = {}
                observations = []
                total_counts = sum(self.conditionals_counts[condition][metric].values())
                self.num_measurements = self.num_measurements + total_counts
                for value in self.conditionals_counts[condition][metric].keys():
                    tmp = self.conditionals_counts[condition][metric][value] / total_counts
                    self.conditionals_probs[condition][metric][value] = tmp
                    observations = observations + [int(round(float(value)))] * int(
                        round(float(self.conditionals_counts[condition][metric][value])))
                if len(observations) == 0:
                    self.means[condition][metric] = -1
                    self.stds[condition][metric] = -1
                    self.mins[condition][metric] = -1
                    self.maxs[condition][metric] = -1
                else:
                    self.means[condition][metric] = round(float(np.mean(observations)), 2)
                    self.stds[condition][metric] = round(float(np.std(observations)), 2)
                    self.mins[condition][metric] = round(float(np.min(observations)), 2)
                    self.maxs[condition][metric] = round(float(np.max(observations)), 2)
        self.num_metrics = len(self.initial_distributions_counts.keys())
        self.metrics = list(self.initial_distributions_counts.keys())
        for metric in self.initial_distributions_counts.keys():
            self.initial_distributions_probs[metric] = {}
            total_counts = sum(self.initial_distributions_counts[metric].values())
            observations = []
            for value in self.initial_distributions_counts[metric].keys():
                self.initial_distributions_probs[metric][value] = (self.initial_distributions_counts[metric][value] /
                                                                   total_counts)
                observations = (observations + [int(round(float(value)))] * int(round(
                    float(self.initial_distributions_counts[metric][value]))))
            if len(observations) == 0:
                self.initial_means[metric] = -1
                self.initial_stds[metric] = -1
                self.initial_mins[metric] = -1
                self.initial_maxs[metric] = -1
            else:
                self.initial_means[metric] = round(float(np.mean(observations)), 2)
                self.initial_stds[metric] = round(float(np.std(observations)), 2)
                self.initial_mins[metric] = round(float(np.min(observations)), 2)
                self.initial_maxs[metric] = round(float(np.max(observations)), 2)

        for condition1 in list(self.conditionals_counts.keys()):
            self.conditionals_kl_divergences[condition1] = {}
            for condition2 in list(self.conditionals_counts.keys()):
                self.conditionals_kl_divergences[condition1][condition2] = {}
                for metric in self.conditionals_counts[condition1].keys():
                    if (len(list(self.conditionals_probs[condition1][metric].keys())) > 0
                            and len(list(self.conditionals_probs[condition2][metric].keys())) > 0):
                        normalized_p_1 = []
                        normalized_p_2 = []
                        for val in set((list(self.conditionals_probs[condition1][metric].keys()) +
                                        list(self.conditionals_probs[condition2][metric].keys()))):
                            if val in self.conditionals_probs[condition1][metric]:
                                normalized_p_1.append(self.conditionals_probs[condition1][metric][val])
                            else:
                                normalized_p_1.append(0.0)
                            if val in self.conditionals_probs[condition2][metric]:
                                normalized_p_2.append(self.conditionals_probs[condition2][metric][val])
                            else:
                                normalized_p_2.append(0.0)
                        self.conditionals_kl_divergences[condition1][condition2][metric] = \
                            float(round(sum(rel_entr(normalized_p_1, normalized_p_2)), 3))
                        if math.isinf(self.conditionals_kl_divergences[condition1][condition2][metric]):
                            self.conditionals_kl_divergences[condition1][condition2][metric] = "inf"
                    else:
                        self.conditionals_kl_divergences[condition1][condition2][metric] = -1

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"conditionals:{self.conditionals_counts}, initial distributions: {self.initial_distributions_counts}" \
               f"emulation_name: {self.emulation_name}, description: {self.descr}, means: {self.means}, " \
               f"maxs: {self.maxs}, mins: {self.mins}, stds: {self.stds}, " \
               f"conditionals_kl_divergences: {self.conditionals_kl_divergences}, " \
               f"num_measurements: {self.num_measurements}, num_metrics: {self.num_metrics}, metrics: {self.metrics}," \
               f"conditions: {self.conditions}, num_conditions: {self.num_conditions}"

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
        obj.conditionals_counts = d["conditionals_counts"]
        obj.initial_distributions_counts = d["initial_distributions_counts"]
        if "id" in d:
            obj.id = d["id"]
        if "means" in d:
            obj.means = d["means"]
        if "stds" in d:
            obj.stds = d["stds"]
        if "mins" in d:
            obj.mins = d["mins"]
        if "maxs" in d:
            obj.maxs = d["maxs"]
        if "initial_distributions_probs" in d:
            obj.initial_distributions_probs = d["initial_distributions_probs"]
        if "conditionals_probs" in d:
            obj.conditionals_probs = d["conditionals_probs"]
        if "initial_means" in d:
            obj.initial_means = d["initial_means"]
        if "initial_stds" in d:
            obj.initial_stds = d["initial_stds"]
        if "initial_mins" in d:
            obj.initial_mins = d["initial_mins"]
        if "initial_maxs" in d:
            obj.initial_maxs = d["initial_maxs"]
        if "num_metrics" in d:
            obj.num_metrics = d["num_metrics"]
        if "num_measurements" in d:
            obj.num_measurements = d["num_measurements"]
        if "metrics" in d:
            obj.metrics = d["metrics"]
        if "conditions" in d:
            obj.conditions = d["conditions"]
        if "num_conditions" in d:
            obj.num_conditions = d["num_conditions"]
        obj.conditionals_kl_divergences = d["conditionals_kl_divergences"]
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["descr"] = self.descr
        d["id"] = self.id
        d["conditionals_counts"] = self.conditionals_counts
        d["initial_distributions_counts"] = self.initial_distributions_counts
        d["emulation_name"] = self.emulation_name
        d["means"] = self.means
        d["stds"] = self.stds
        d["maxs"] = self.maxs
        d["mins"] = self.mins
        d["conditionals_probs"] = self.conditionals_probs
        d["initial_distributions_probs"] = self.initial_distributions_probs
        d["initial_means"] = self.initial_means
        d["initial_stds"] = self.initial_stds
        d["initial_maxs"] = self.initial_maxs
        d["initial_mins"] = self.initial_mins
        d["conditionals_kl_divergences"] = self.conditionals_kl_divergences
        d["num_metrics"] = self.num_metrics
        d["num_conditions"] = self.num_conditions
        d["num_measurements"] = self.num_measurements
        d["metrics"] = self.metrics
        d["conditions"] = self.conditions
        return d

    @staticmethod
    def from_json_file(json_file_path: str) -> "EmulationStatistics":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return EmulationStatistics.from_dict(json.loads(json_str))

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

    def get_number_of_samples(self) -> int:
        num_samples = 0
        for k, v in self.conditionals_counts.items():
            for k, v in v.items():
                num_samples += v
        return num_samples

    def merge(self, second_statistic: "EmulationStatistics") -> None:
        """
        Merges the statistic with another statistic by adding the counts

        :param second_statistic: the statistic to merge with
        :return: None
        """
        for condition in self.conditionals_counts.keys():
            for metric in self.conditionals_counts[condition].keys():
                for value in self.conditionals_counts[condition][metric].keys():
                    if (condition in second_statistic.conditionals_counts
                            and metric in second_statistic.conditionals_counts[condition]
                            and value in second_statistic.conditionals_counts[condition][metric]):
                        self.conditionals_counts[condition][metric][value] = \
                            self.conditionals_counts[condition][metric][value] + \
                            second_statistic.conditionals_counts[condition][metric][value]

        for condition in second_statistic.conditionals_counts.keys():
            if condition not in self.conditionals_counts:
                self.conditionals_counts[condition] = {}
            for metric in second_statistic.conditionals_counts[condition].keys():
                if metric not in self.conditionals_counts[condition]:
                    self.conditionals_counts[condition][metric] = {}
                for value in second_statistic.conditionals_counts[condition][metric].keys():
                    if value not in self.conditionals_counts[condition][metric]:
                        self.conditionals_counts[condition][metric][value] = \
                            second_statistic.conditionals_counts[condition][metric][value]

        for metric in self.initial_distributions_counts.keys():
            for value in self.initial_distributions_counts[metric].keys():
                if (metric in second_statistic.initial_distributions_counts
                        and value in second_statistic.initial_distributions_counts[metric]):
                    self.initial_distributions_counts[metric][value] = \
                        self.initial_distributions_counts[metric][value] + \
                        second_statistic.initial_distributions_counts[metric][value]

        for metric in second_statistic.initial_distributions_counts.keys():
            if metric not in self.initial_distributions_counts:
                self.initial_distributions_counts[metric] = {}
            for value in second_statistic.initial_distributions_counts[metric].keys():
                if value not in self.initial_distributions_counts[metric]:
                    self.initial_distributions_counts[metric][value] = \
                        second_statistic.initial_distributions_counts[metric][value]
