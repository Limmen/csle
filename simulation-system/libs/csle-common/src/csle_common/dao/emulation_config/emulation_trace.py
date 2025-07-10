from typing import Optional, List, Dict, Any, Tuple, Union
import json
import os
from csle_common.logging.log import Logger
import csle_common.constants.constants as constants
import csle_collector.constants.constants as collector_constants
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.encoding.np_encoder import NpEncoder
from csle_common.dao.emulation_observation.attacker.emulation_attacker_observation_state \
    import EmulationAttackerObservationState
from csle_common.dao.emulation_observation.defender.emulation_defender_observation_state \
    import EmulationDefenderObservationState
from csle_base.json_serializable import JSONSerializable


class EmulationTrace(JSONSerializable):
    """
    DTO class representing a trace in the emulation system
    """

    def __init__(self, initial_attacker_observation_state: EmulationAttackerObservationState,
                 initial_defender_observation_state: EmulationDefenderObservationState, emulation_name: str):
        """
        Initializes the DTO

        :param initial_attacker_observation_state: the initial state of the attacker
        :param initial_defender_observation_state: the intial state of the defender
        :param emulation_name: the name of the emulation
        """
        self.initial_attacker_observation_state = initial_attacker_observation_state
        self.initial_defender_observation_state = initial_defender_observation_state
        self.attacker_observation_states: List[EmulationAttackerObservationState] = []
        self.defender_observation_states: List[EmulationDefenderObservationState] = []
        self.attacker_actions: List[EmulationAttackerAction] = []
        self.defender_actions: List[EmulationDefenderAction] = []
        self.emulation_name = emulation_name
        self.id = -1

    def __str__(self):
        """
        :return: a string representation of the object
        """
        return f"initial_attacker_observation_state:{self.initial_attacker_observation_state}" \
               f"initial_defender_observation_state:{self.initial_defender_observation_state}" \
               f"attacker_observation_states:{self.attacker_observation_states}\n" \
               f"defender_observation_states:{self.defender_observation_states}\n" \
               f"attacker_actions:{self.attacker_actions}\n" \
               f"defender_actions:{self.defender_actions}\n" \
               f"emulation_name: {self.emulation_name}," \
               f"id:{self.id}"

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EmulationTrace":
        """
        Converts a dict representation into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = EmulationTrace(
            initial_attacker_observation_state=EmulationAttackerObservationState.from_dict(
                d["initial_attacker_observation_state"]),
            initial_defender_observation_state=EmulationDefenderObservationState.from_dict(
                d["initial_defender_observation_state"]),
            emulation_name=d["emulation_name"]
        )
        obj.attacker_observation_states = list(map(lambda x: EmulationAttackerObservationState.from_dict(x),
                                                   d["attacker_observation_states"]))
        obj.defender_observation_states = list(map(lambda x: EmulationDefenderObservationState.from_dict(x),
                                                   d["defender_observation_states"]))
        obj.attacker_actions = list(map(lambda x: EmulationAttackerAction.from_dict(x), d["attacker_actions"]))
        obj.defender_actions = list(map(lambda x: EmulationDefenderAction.from_dict(x),
                                        d["defender_actions"]))
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["initial_attacker_observation_state"] = self.initial_attacker_observation_state.to_dict()
        d["initial_defender_observation_state"] = self.initial_defender_observation_state.to_dict()
        d["attacker_observation_states"] = list(map(lambda x: x.to_dict(), self.attacker_observation_states))
        d["defender_observation_states"] = list(map(lambda x: x.to_dict(), self.defender_observation_states))
        d["attacker_actions"] = list(map(lambda x: x.to_dict(), self.attacker_actions))
        d["defender_actions"] = list(map(lambda x: x.to_dict(), self.defender_actions))
        d["emulation_name"] = self.emulation_name
        d["id"] = self.id
        return d

    @staticmethod
    def save_traces_to_disk(traces_save_dir, traces: List["EmulationTrace"], traces_file: Optional[str] = None) -> None:
        """
        Utility function for saving a list of traces to a json file

        :param traces_save_dir: the directory where to save the traces
        :param traces: the traces to save
        :param traces_file: the filename of the traces file
        :return: None
        """
        traces_1 = list(map(lambda x: x.to_dict(), traces))
        if traces_file is None:
            traces_file = constants.SYSTEM_IDENTIFICATION.EMULATION_TRACES_FILE
        if not os.path.exists(traces_save_dir):
            os.makedirs(traces_save_dir)
        with open(traces_save_dir + "/" + traces_file, 'w') as fp:
            json.dump({"traces": traces_1}, fp, cls=NpEncoder)

    @staticmethod
    def load_traces_from_disk(traces_file: str) -> List["EmulationTrace"]:
        """
        Utility function for loading and parsing a list of traces from a json file

        :param traces_file: (optional) a custom name of the traces file
        :return: a list of the loaded traces
        """
        if os.path.exists(traces_file):
            with open(traces_file, 'r') as fp:
                d = json.load(fp)
                if constants.METADATA_STORE.TRACES_PROPERTY in d:
                    traces = d[constants.METADATA_STORE.TRACES_PROPERTY]
                else:
                    traces = d["emulations"]
                traces_1 = list(map(lambda x: EmulationTrace.from_dict(x), traces))
                return traces_1
        else:
            Logger.__call__().get_logger().info("Warning: Could not "
                                                f"read traces file, path does not exist:{traces_file}")
            return []

    @staticmethod
    def from_json_str(json_str: str) -> "EmulationTrace":
        """
        Converts json string into a DTO

        :param json_str: the json string representation
        :return: the DTO instance
        """
        import json
        dto: EmulationTrace = EmulationTrace.from_dict(json.loads(json_str))
        return dto

    @staticmethod
    def from_json_file(json_file_path: str) -> "EmulationTrace":
        """
        Reads a json file and converts it into a dto

        :param json_file_path: the json file path to save  the DTO to
        :return: None
        """
        import io
        with io.open(json_file_path, 'r', encoding='utf-8') as f:
            json_str = f.read()
            dto = EmulationTrace.from_json_str(json_str=json_str)
            return dto

    def num_attributes_per_time_step(self) -> int:
        """
        :return: approximately the number of attributes recorded per time-step of the trace
        """
        num_attributes: int = 2
        num_attributes = (num_attributes + (1 + len(self.attacker_observation_states))
                          * self.initial_attacker_observation_state.num_attributes())
        num_attributes = (num_attributes + (1 + len(self.defender_observation_states))
                          * self.initial_defender_observation_state.num_attributes())
        if len(self.defender_actions) > 0:
            num_attributes = num_attributes + len(self.defender_actions) * self.defender_actions[0].num_attributes()
        if len(self.attacker_actions) > 0:
            num_attributes = num_attributes + len(self.attacker_actions) * self.attacker_actions[0].num_attributes()
        return num_attributes

    @staticmethod
    def schema():
        """
        :return: the schema of the DTO
        """
        dto = EmulationTrace(initial_attacker_observation_state=EmulationAttackerObservationState.schema(),
                             initial_defender_observation_state=EmulationDefenderObservationState.schema(),
                             emulation_name="")
        dto.attacker_observation_states = [EmulationAttackerObservationState.schema()]
        dto.defender_observation_states = [EmulationDefenderObservationState.schema()]
        dto.attacker_actions = [EmulationAttackerAction.schema()]
        dto.defender_actions = [EmulationDefenderAction.schema()]
        return dto

    def to_csv_record(self, max_time_steps: int, max_nodes: int, max_ports: int, max_vulns: int,
                      null_value: int = -1) -> Tuple[List[Union[str, int, float]], List[str]]:
        """
        Converts the trace into a csv row

        :param max_time_steps: the maximum number of time-steps to include in the row
        :param max_nodes: the maximum number of nodes to include metrics from
        :param max_ports: the maximum number of ports to include metrics from
        :param max_vulns: the maximum number of vulnerabilities to include metrics from
        :param null_value: the default null value if a metric is missing
        :return: the list of labels and values of the csv row
        """
        # lookup tables for vuln names, service names, protocol names
        labels = []
        values: List[Union[str, float]] = []
        intrusion_started = False
        attacker_observations = [self.initial_attacker_observation_state] + self.attacker_observation_states
        defender_observations = [self.initial_defender_observation_state] + self.defender_observation_states
        for t in range(max_time_steps):
            labels.append(f"{t}_intrusion")
            if len(attacker_observations) > t:
                if not intrusion_started and self.attacker_actions[t].id != EmulationAttackerActionId.CONTINUE:
                    intrusion_started = True
                values.append(int(intrusion_started))
            else:
                values.append(null_value)

            labels.append(f"{t}_attacker_action_id")
            if (len(self.attacker_actions) + 1) > t:
                if t > 0:
                    values.append(self.attacker_actions[t - 1].id)
                else:
                    values.append(null_value)
            else:
                values.append(null_value)
            labels.append(f"{t}_attacker_action_name")
            if (len(self.attacker_actions) + 1) > t:
                if t > 0:
                    values.append(self.attacker_actions[t - 1].name)
                else:
                    values.append(null_value)
            else:
                values.append(null_value)
            labels.append(f"{t}_attacker_action_type")
            if (len(self.attacker_actions) + 1) > t:
                if t > 0:
                    values.append(self.attacker_actions[t - 1].type)
                else:
                    values.append(null_value)
            else:
                values.append(null_value)
            labels.append(f"{t}_attacker_action_ips")
            if (len(self.attacker_actions) + 1) > t:
                if t > 0:
                    values.append("-".join(self.attacker_actions[t - 1].ips))
                else:
                    values.append(null_value)
            else:
                values.append(null_value)
            labels.append(f"{t}_attacker_action_index")
            if (len(self.attacker_actions) + 1) > t:
                if t > 0:
                    values.append(self.attacker_actions[t - 1].index)
                else:
                    values.append(null_value)
            else:
                values.append(null_value)
            labels.append(f"{t}_attacker_action_outcome")
            if (len(self.attacker_actions) + 1) > t:
                if t > 0:
                    values.append(self.attacker_actions[t - 1].action_outcome)
                else:
                    values.append(null_value)
            else:
                values.append(null_value)
            labels.append(f"{t}_attacker_action_execution_time")
            if (len(self.attacker_actions) + 1) > t:
                if t > 0:
                    values.append(self.attacker_actions[t - 1].execution_time)
                else:
                    values.append(null_value)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_action_id")
            if (len(self.defender_actions) + 1) > t:
                if t > 0:
                    values.append(self.defender_actions[t - 1].id)
                else:
                    values.append(null_value)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_action_name")
            if (len(self.defender_actions) + 1) > t:
                if t > 0:
                    values.append(self.defender_actions[t - 1].name)
                else:
                    values.append(null_value)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_action_type")
            if (len(self.defender_actions) + 1) > t:
                if t > 0:
                    values.append(self.defender_actions[t - 1].type)
                else:
                    values.append(null_value)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_action_ips")
            if (len(self.defender_actions) + 1) > t:
                if t > 0:
                    values.append("-".join(self.defender_actions[t - 1].ips))
                else:
                    values.append(null_value)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_action_index")
            if (len(self.defender_actions) + 1) > t:
                if t > 0:
                    values.append(self.defender_actions[t - 1].index)
                else:
                    values.append(null_value)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_action_outcome")
            if (len(self.defender_actions) + 1) > t:
                if t > 0:
                    values.append(self.defender_actions[t - 1].action_outcome)
                else:
                    values.append(null_value)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_action_execution_time")
            if (len(self.defender_actions) + 1) > t:
                if t > 0:
                    values.append(self.defender_actions[t - 1].execution_time)
                else:
                    values.append(null_value)
            else:
                values.append(null_value)
            labels.append(f"{t}_attacker_num_catched_flags")
            if len(attacker_observations) > t:
                values.append(attacker_observations[t].catched_flags)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_num_clients")
            if len(defender_observations) > t:
                values.append(defender_observations[t].avg_client_population_metrics.num_clients)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_clients_arrival_rate")
            if len(defender_observations) > t:
                values.append(defender_observations[t].avg_client_population_metrics.rate)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_num_pids")
            if len(defender_observations) > t:
                values.append(defender_observations[t].avg_docker_stats.pids)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_cpu_percent")
            if len(defender_observations) > t:
                values.append(defender_observations[t].avg_docker_stats.cpu_percent)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_mem_current")
            if len(defender_observations) > t:
                values.append(defender_observations[t].avg_docker_stats.mem_current)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_mem_total")
            if len(defender_observations) > t:
                values.append(defender_observations[t].avg_docker_stats.mem_total)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_mem_percent")
            if len(defender_observations) > t:
                values.append(defender_observations[t].avg_docker_stats.mem_percent)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_blk_read")
            if len(defender_observations) > t:
                values.append(defender_observations[t].avg_docker_stats.blk_read)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_blk_write")
            if len(defender_observations) > t:
                values.append(defender_observations[t].avg_docker_stats.blk_write)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_net_rx")
            if len(defender_observations) > t:
                values.append(defender_observations[t].avg_docker_stats.net_rx)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_net_tx")
            if len(defender_observations) > t:
                values.append(defender_observations[t].avg_docker_stats.net_tx)
            else:
                values.append(null_value)
            for i in range(4):
                labels.append(f"{t}_defender_num_snort_priority_{i}_alerts")
                if len(defender_observations) > t:
                    values.append(defender_observations[t].avg_snort_ids_alert_counters.priority_alerts[i])
                else:
                    values.append(null_value)
            for i in range(len(set(collector_constants.SNORT_IDS_ROUTER.SNORT_ALERT_IDS_ID.values()))):
                labels.append(f"{t}_defender_num_snort_class_{i}_alerts")
                if len(defender_observations) > t:
                    values.append(defender_observations[t].avg_snort_ids_alert_counters.class_alerts[i])
                else:
                    values.append(null_value)
            labels.append(f"{t}_defender_num_snort_severe_alerts")
            if len(defender_observations) > t:
                values.append(defender_observations[t].avg_snort_ids_alert_counters.severe_alerts)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_num_snort_warning_alerts")
            if len(defender_observations) > t:
                values.append(defender_observations[t].avg_snort_ids_alert_counters.warning_alerts)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_num_snort_total_alerts")
            if len(defender_observations) > t:
                values.append(defender_observations[t].avg_snort_ids_alert_counters.total_alerts)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_num_snort_alerts_weighted_by_priority")
            if len(defender_observations) > t:
                values.append(defender_observations[t].avg_snort_ids_alert_counters.alerts_weighted_by_priority)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_num_ossec_severe_alerts")
            if len(defender_observations) > t:
                values.append(defender_observations[t].avg_ossec_ids_alert_counters.severe_alerts)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_num_ossec_warning_alerts")
            if len(defender_observations) > t:
                values.append(defender_observations[t].avg_ossec_ids_alert_counters.warning_alerts)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_num_ossec_total_alerts")
            if len(defender_observations) > t:
                values.append(defender_observations[t].avg_ossec_ids_alert_counters.total_alerts)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_num_ossec_alerts_weighted_by_level")
            if len(defender_observations) > t:
                values.append(defender_observations[t].avg_ossec_ids_alert_counters.alerts_weighted_by_level)
            else:
                values.append(null_value)
            for i in range(16):
                labels.append(f"{t}_defender_num_ossec_level_{i}_alerts")
                if len(defender_observations) > t:
                    values.append(defender_observations[t].avg_ossec_ids_alert_counters.level_alerts[i])
                else:
                    values.append(null_value)
            for i in range(len(set(collector_constants.OSSEC.OSSEC_IDS_ALERT_GROUP_ID.values()))):
                labels.append(f"{t}_defender_num_ossec_group_{i}_alerts")
                if len(defender_observations) > t:
                    values.append(defender_observations[t].avg_ossec_ids_alert_counters.group_alerts[i])
                else:
                    values.append(null_value)
            labels.append(f"{t}_defender_num_logged_in_users")
            if len(defender_observations) > t:
                values.append(defender_observations[t].avg_aggregated_host_metrics.num_logged_in_users)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_num_failed_login_attempts")
            if len(defender_observations) > t and defender_observations[t].avg_aggregated_host_metrics is not None:
                values.append(defender_observations[t].avg_aggregated_host_metrics.num_failed_login_attempts)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_num_open_connections")
            if len(defender_observations) > t and defender_observations[t].avg_aggregated_host_metrics is not None:
                values.append(defender_observations[t].avg_aggregated_host_metrics.num_open_connections)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_num_login_events")
            if len(defender_observations) > t and defender_observations[t].avg_aggregated_host_metrics is not None:
                values.append(defender_observations[t].avg_aggregated_host_metrics.num_login_events)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_num_processes")
            if len(defender_observations) > t and defender_observations[t].avg_aggregated_host_metrics is not None:
                values.append(defender_observations[t].avg_aggregated_host_metrics.num_processes)
            else:
                values.append(null_value)
            labels.append(f"{t}_defender_num_users")
            if len(defender_observations) > t and defender_observations[t].avg_aggregated_host_metrics is not None:
                values.append(defender_observations[t].avg_aggregated_host_metrics.num_users)
            else:
                values.append(null_value)

            for i in range(max_nodes):
                labels.append(f"{t}_node_{i}_ip")
                if len(defender_observations) > t and len(defender_observations[t].machines) > i:
                    values.append(defender_observations[t].machines[i].ips[0])
                else:
                    values.append(null_value)
                labels.append(f"{t}_node_{i}_os")
                if len(defender_observations) > t and len(defender_observations[t].machines) > i:
                    values.append(defender_observations[t].machines[i].os)
                else:
                    values.append(null_value)
                labels.append(f"{t}_attacker_node_{i}_discovered")
                if len(attacker_observations) > t and len(attacker_observations[t].machines) > i:
                    values.append(1)
                else:
                    values.append(null_value)
                for j in range(max_ports):
                    labels.append(f"{t}_attacker_node_{i}_port_{j}_port_number")
                    if len(attacker_observations) > t and len(attacker_observations[t].machines) > i \
                            and len(attacker_observations[t].machines[i].ports) > j:
                        values.append(int(attacker_observations[t].machines[i].ports[j].port))
                    else:
                        values.append(null_value)
                    labels.append(f"{t}_attacker_node_{i}_port_{j}_open")
                    if len(attacker_observations) > t and len(attacker_observations[t].machines) > i \
                            and len(attacker_observations[t].machines[i].ports) > j:
                        values.append(int(attacker_observations[t].machines[i].ports[j].open))
                    else:
                        values.append(null_value)
                    labels.append(f"{t}_attacker_node_{i}_port_{j}_service")
                    if len(attacker_observations) > t and len(attacker_observations[t].machines) > i \
                            and len(attacker_observations[t].machines[i].ports) > j:
                        values.append(int(attacker_observations[t].machines[i].ports[j].service))
                    else:
                        values.append(null_value)
                    labels.append(f"{t}_attacker_node_{i}_port_{j}_protocol")
                    if len(attacker_observations) > t and len(attacker_observations[t].machines) > i \
                            and len(attacker_observations[t].machines[i].ports) > j:
                        values.append(int(attacker_observations[t].machines[i].ports[j].protocol))
                    else:
                        values.append(null_value)
                for k in range(max_vulns):
                    labels.append(f"{t}_attacker_node_{i}_vuln_{k}_name")
                    if len(attacker_observations) > t and len(attacker_observations[t].machines) > i \
                            and len(attacker_observations[t].machines[i].cve_vulns) > k:
                        values.append(attacker_observations[t].machines[i].cve_vulns[k].name)
                    else:
                        values.append(null_value)
                    labels.append(f"{t}_attacker_node_{i}_vuln_{k}_port_number")
                    if len(attacker_observations) > t and len(attacker_observations[t].machines) > i \
                            and len(attacker_observations[t].machines[i].cve_vulns) > k:
                        values.append(int(attacker_observations[t].machines[i].cve_vulns[k].port))
                    else:
                        values.append(null_value)
                    labels.append(f"{t}_attacker_node_{i}_vuln_{k}_protocol")
                    if len(attacker_observations) > t and len(attacker_observations[t].machines) > i \
                            and len(attacker_observations[t].machines[i].cve_vulns) > k:
                        values.append(int(attacker_observations[t].machines[i].cve_vulns[k].protocol))
                    else:
                        values.append(null_value)
                    labels.append(f"{t}_attacker_node_{i}_vuln_{k}_cvss")
                    if len(attacker_observations) > t and len(attacker_observations[t].machines) > i \
                            and len(attacker_observations[t].machines[i].cve_vulns) > k:
                        values.append(attacker_observations[t].machines[i].cve_vulns[k].cvss)
                    else:
                        values.append(null_value)
                    labels.append(f"{t}_attacker_node_{i}_vuln_{k}_osvdbid")
                    if len(attacker_observations) > t and len(attacker_observations[t].machines) > i \
                            and len(attacker_observations[t].machines[i].cve_vulns) > k \
                            and attacker_observations[t].machines[i].cve_vulns[k].osvdb_id is not None:
                        values.append(int(attacker_observations[t].machines[i].cve_vulns[k].osvdb_id))
                    else:
                        values.append(null_value)
                labels.append(f"{t}_attacker_node_{i}_shell_access")
                if len(attacker_observations) > t and len(attacker_observations[t].machines) > i:
                    values.append(int(attacker_observations[t].machines[i].shell_access))
                else:
                    values.append(null_value)
                labels.append(f"{t}_attacker_node_{i}_logged_in")
                if len(attacker_observations) > t and len(attacker_observations[t].machines) > i:
                    values.append(int(attacker_observations[t].machines[i].logged_in))
                else:
                    values.append(null_value)
                labels.append(f"{t}_attacker_node_{i}_root")
                if len(attacker_observations) > t and len(attacker_observations[t].machines) > i:
                    values.append(int(attacker_observations[t].machines[i].root))
                else:
                    values.append(null_value)
                labels.append(f"{t}_attacker_node_{i}_num_flags_found")
                if len(attacker_observations) > t and len(attacker_observations[t].machines) > i:
                    values.append(len(attacker_observations[t].machines[i].flags_found))
                else:
                    values.append(null_value)
                labels.append(f"{t}_attacker_node_{i}_file_system_searched")
                if len(attacker_observations) > t and len(attacker_observations[t].machines) > i:
                    values.append(int(attacker_observations[t].machines[i].filesystem_searched))
                else:
                    values.append(null_value)
                labels.append(f"{t}_attacker_node_{i}_untried_credentials")
                if len(attacker_observations) > t and len(attacker_observations[t].machines) > i:
                    values.append(int(attacker_observations[t].machines[i].untried_credentials))
                else:
                    values.append(null_value)
                labels.append(f"{t}_attacker_node_{i}_telnet_brute_tried")
                if len(attacker_observations) > t and len(attacker_observations[t].machines) > i:
                    values.append(int(attacker_observations[t].machines[i].telnet_brute_tried))
                else:
                    values.append(null_value)
                labels.append(f"{t}_attacker_node_{i}_ssh_brute_tried")
                if len(attacker_observations) > t and len(attacker_observations[t].machines) > i:
                    values.append(int(attacker_observations[t].machines[i].ssh_brute_tried))
                else:
                    values.append(null_value)
                labels.append(f"{t}_attacker_node_{i}_ftp_brute_tried")
                if len(attacker_observations) > t and len(attacker_observations[t].machines) > i:
                    values.append(int(attacker_observations[t].machines[i].ftp_brute_tried))
                else:
                    values.append(null_value)
                labels.append(f"{t}_attacker_node_{i}_cassandra_brute_tried")
                if len(attacker_observations) > t and len(attacker_observations[t].machines) > i:
                    values.append(int(attacker_observations[t].machines[i].cassandra_brute_tried))
                else:
                    values.append(null_value)
                labels.append(f"{t}_attacker_node_{i}_irc_brute_tried")
                if len(attacker_observations) > t and len(attacker_observations[t].machines) > i:
                    values.append(int(attacker_observations[t].machines[i].irc_brute_tried))
                else:
                    values.append(null_value)
                labels.append(f"{t}_attacker_node_{i}_mongo_brute_tried")
                if len(attacker_observations) > t and len(attacker_observations[t].machines) > i:
                    values.append(int(attacker_observations[t].machines[i].mongo_brute_tried))
                else:
                    values.append(null_value)
                labels.append(f"{t}_attacker_node_{i}_mysql_brute_tried")
                if len(attacker_observations) > t and len(attacker_observations[t].machines) > i:
                    values.append(int(attacker_observations[t].machines[i].mysql_brute_tried))
                else:
                    values.append(null_value)
                labels.append(f"{t}_attacker_node_{i}_smtp_brute_tried")
                if len(attacker_observations) > t and len(attacker_observations[t].machines) > i:
                    values.append(int(attacker_observations[t].machines[i].smtp_brute_tried))
                else:
                    values.append(null_value)
                labels.append(f"{t}_attacker_node_{i}_postgres_brute_tried")
                if len(attacker_observations) > t and len(attacker_observations[t].machines) > i:
                    values.append(int(attacker_observations[t].machines[i].postgres_brute_tried))
                else:
                    values.append(null_value)
                labels.append(f"{t}_attacker_node_{i}_tools_installed")
                if len(attacker_observations) > t and len(attacker_observations[t].machines) > i:
                    values.append(int(attacker_observations[t].machines[i].tools_installed))
                else:
                    values.append(null_value)
                labels.append(f"{t}_attacker_node_{i}_backdoor_installed")
                if len(attacker_observations) > t and len(attacker_observations[t].machines) > i:
                    values.append(int(attacker_observations[t].machines[i].backdoor_installed))
                else:
                    values.append(null_value)
                labels.append(f"{t}_attacker_node_{i}_backdoor_tried")
                if len(attacker_observations) > t and len(attacker_observations[t].machines) > i:
                    values.append(int(attacker_observations[t].machines[i].backdoor_tried))
                else:
                    values.append(null_value)
                labels.append(f"{t}_attacker_node_{i}_dvwa_sql_injection_tried")
                if len(attacker_observations) > t and len(attacker_observations[t].machines) > i:
                    values.append(int(attacker_observations[t].machines[i].dvwa_sql_injection_tried))
                else:
                    values.append(null_value)
                labels.append(f"{t}_attacker_node_{i}_cve_2015_3306_tried")
                if len(attacker_observations) > t and len(attacker_observations[t].machines) > i:
                    values.append(int(attacker_observations[t].machines[i].cve_2015_3306_tried))
                else:
                    values.append(null_value)
                labels.append(f"{t}_attacker_node_{i}_cve_2015_1427_tried")
                if len(attacker_observations) > t and len(attacker_observations[t].machines) > i:
                    values.append(int(attacker_observations[t].machines[i].cve_2015_1427_tried))
                else:
                    values.append(null_value)
                labels.append(f"{t}_attacker_node_{i}_cve_2016_10033_tried")
                if len(attacker_observations) > t and len(attacker_observations[t].machines) > i:
                    values.append(int(attacker_observations[t].machines[i].cve_2016_10033_tried))
                else:
                    values.append(null_value)
                labels.append(f"{t}_attacker_node_{i}_cve_2010_0426_tried")
                if len(attacker_observations) > t and len(attacker_observations[t].machines) > i:
                    values.append(int(attacker_observations[t].machines[i].cve_2010_0426_tried))
                else:
                    values.append(null_value)
                labels.append(f"{t}_attacker_node_{i}_cve_2015_5602_tried")
                if len(attacker_observations) > t and len(attacker_observations[t].machines) > i:
                    values.append(int(attacker_observations[t].machines[i].cve_2015_5602_tried))
                else:
                    values.append(null_value)
                labels.append(f"{t}_node_{i}_defender_num_pids")
                if len(defender_observations) > t and len(defender_observations[t].machines) > i:
                    values.append(defender_observations[t].machines[i].docker_stats.pids)
                else:
                    values.append(null_value)
                labels.append(f"{t}_node_{i}_defender_cpu_percent")
                if len(defender_observations) > t and len(defender_observations[t].machines) > i:
                    values.append(defender_observations[t].machines[i].docker_stats.cpu_percent)
                else:
                    values.append(null_value)
                labels.append(f"{t}_node_{i}_defender_mem_current")
                if len(defender_observations) > t and len(defender_observations[t].machines) > i:
                    values.append(defender_observations[t].machines[i].docker_stats.mem_current)
                else:
                    values.append(null_value)
                labels.append(f"{t}_node_{i}_defender_mem_total")
                if len(defender_observations) > t and len(defender_observations[t].machines) > i:
                    values.append(defender_observations[t].machines[i].docker_stats.mem_total)
                else:
                    values.append(null_value)
                labels.append(f"{t}_node_{i}_defender_mem_percent")
                if len(defender_observations) > t and len(defender_observations[t].machines) > i:
                    values.append(defender_observations[t].machines[i].docker_stats.mem_percent)
                else:
                    values.append(null_value)
                labels.append(f"{t}_node_{i}_defender_blk_read")
                if len(defender_observations) > t and len(defender_observations[t].machines) > i:
                    values.append(defender_observations[t].machines[i].docker_stats.blk_read)
                else:
                    values.append(null_value)
                labels.append(f"{t}_node_{i}_defender_blk_write")
                if len(defender_observations) > t and len(defender_observations[t].machines) > i:
                    values.append(defender_observations[t].machines[i].docker_stats.blk_write)
                else:
                    values.append(null_value)
                labels.append(f"{t}_node_{i}_defender_net_rx")
                if len(defender_observations) > t and len(defender_observations[t].machines) > i:
                    values.append(defender_observations[t].machines[i].docker_stats.net_rx)
                else:
                    values.append(null_value)
                labels.append(f"{t}_node_{i}_defender_net_tx")
                if len(defender_observations) > t and len(defender_observations[t].machines) > i:
                    values.append(defender_observations[t].machines[i].docker_stats.net_tx)
                else:
                    values.append(null_value)
                labels.append(f"{t}_node_{i}_defender_num_logged_in_users")
                if len(defender_observations) > t and len(defender_observations[t].machines) > i:
                    values.append(defender_observations[t].machines[i].host_metrics.num_logged_in_users)
                else:
                    values.append(null_value)
                labels.append(f"{t}_node_{i}_defender_num_failed_login_attempts")
                if len(defender_observations) > t and len(defender_observations[t].machines) > i:
                    values.append(defender_observations[t].machines[i].host_metrics.num_failed_login_attempts)
                else:
                    values.append(null_value)
                labels.append(f"{t}_node_{i}_defender_num_open_connections")
                if len(defender_observations) > t and len(defender_observations[t].machines) > i:
                    values.append(defender_observations[t].machines[i].host_metrics.num_open_connections)
                else:
                    values.append(null_value)
                labels.append(f"{t}_node_{i}_defender_num_login_events")
                if len(defender_observations) > t and len(defender_observations[t].machines) > i:
                    values.append(defender_observations[t].machines[i].host_metrics.num_login_events)
                else:
                    values.append(null_value)
                labels.append(f"{t}_node_{i}_defender_num_processes")
                if len(defender_observations) > t and len(defender_observations[t].machines) > i:
                    values.append(defender_observations[t].machines[i].host_metrics.num_processes)
                else:
                    values.append(null_value)
                labels.append(f"{t}_node_{i}_defender_num_users")
                if len(defender_observations) > t and len(defender_observations[t].machines) > i:
                    values.append(defender_observations[t].machines[i].host_metrics.num_users)
                else:
                    values.append(null_value)
        assert len(values) == len(labels)
        return values, labels
