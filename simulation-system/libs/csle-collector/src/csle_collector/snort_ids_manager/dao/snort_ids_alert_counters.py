from typing import List, Dict, Any, Tuple
import time
import numpy as np
from csle_base.json_serializable import JSONSerializable
import csle_collector.constants.constants as constants
from csle_collector.snort_ids_manager.dao.snort_ids_fast_log_alert import SnortIdsFastLogAlert
import csle_collector.snort_ids_manager.snort_ids_manager_pb2


class SnortIdsAlertCounters(JSONSerializable):
    """
    DTO containing statistics from the Snort IDS log
    """

    def __init__(self):
        """
        Initializes the DTO
        """
        self.priority_alerts = [0] * 4
        self.class_alerts = []
        for i in range(len(set(constants.SNORT_IDS_ROUTER.SNORT_ALERT_IDS_ID.values()))):
            self.class_alerts.append(0)
        self.severe_alerts = 0
        self.warning_alerts = 0
        self.total_alerts = 0
        self.alerts_weighted_by_priority = 0
        self.ip = ""
        self.ts = 0.0

    def add(self, alert_counters: "SnortIdsAlertCounters") -> None:
        """
        Adds another alert counters object to this one

        :param alert_counters: the counters to add
        :return: None
        """
        self.severe_alerts = int(self.severe_alerts + alert_counters.severe_alerts)
        self.warning_alerts = int(self.warning_alerts + alert_counters.warning_alerts)
        self.total_alerts = int(self.total_alerts + alert_counters.total_alerts)
        self.alerts_weighted_by_priority = self.alerts_weighted_by_priority + alert_counters.alerts_weighted_by_priority
        for idx in range(len(self.priority_alerts)):
            self.priority_alerts[idx] = int(self.priority_alerts[idx] + alert_counters.priority_alerts[idx])
        for idx in range(len(self.class_alerts)):
            self.class_alerts[idx] = int(self.class_alerts[idx] + alert_counters.class_alerts[idx])

    def count(self, alerts: List[SnortIdsFastLogAlert]) -> None:
        """
        Counts the list of alerts

        :param alerts: list of alerts from the log
        :return: None
        """
        for a in alerts:
            if a.priority - 1 in range(0, len(self.priority_alerts)):
                self.priority_alerts[a.priority] += 1
            if a.class_id in range(0, len(self.class_alerts)):
                self.class_alerts[a.class_id] += 1

        self.total_alerts = len(alerts)
        self.severe_alerts = sum(
            self.priority_alerts[0:constants.SNORT_IDS_ROUTER.SNORT_SEVERE_ALERT_PRIORITY_THRESHOLD])
        self.warning_alerts = sum(
            self.priority_alerts[constants.SNORT_IDS_ROUTER.SNORT_SEVERE_ALERT_PRIORITY_THRESHOLD:])
        self.alerts_weighted_by_priority = 0
        for idx in range(len(self.priority_alerts)):
            priority = (len(self.priority_alerts) - idx + 1)
            self.alerts_weighted_by_priority += priority * self.priority_alerts[idx]

    @staticmethod
    def from_kafka_record(record: str) -> "SnortIdsAlertCounters":
        """
        Converts a kafka record to a DTO

        :param record: the kafka record to convert
        :return: the DTO
        """
        parts = record.split(",")
        obj = SnortIdsAlertCounters()
        obj.ts = float(parts[0])
        obj.ip = parts[1]
        obj.total_alerts = int(round(float(parts[2])))
        obj.warning_alerts = int(round(float(parts[3])))
        obj.severe_alerts = int(round(float(parts[4])))
        obj.alerts_weighted_by_priority = int(round(float(parts[5])))
        obj.class_alerts = []
        obj.priority_alerts = []
        for i in range(6, len(set(constants.SNORT_IDS_ROUTER.SNORT_ALERT_IDS_ID.values())) + 6):
            obj.class_alerts.append(int(round(float(parts[i]))))
        for i in range(len(set(constants.SNORT_IDS_ROUTER.SNORT_ALERT_IDS_ID.values())) + 6,
                       len(set(constants.SNORT_IDS_ROUTER.SNORT_ALERT_IDS_ID.values())) + 10):
            obj.priority_alerts.append(int(round(float(parts[i]))))
        return obj

    def update_with_kafka_record(self, record: str) -> None:
        """
        Updates the DTO with a kafka record

        :param record: the kafka record to use for updating
        :return: None
        """
        parts = record.split(",")
        self.ts = float(parts[0])
        self.ip = parts[1]
        self.total_alerts = int(round(float(parts[2])))
        self.warning_alerts = int(round(float(parts[3])))
        self.severe_alerts = int(round(float(parts[4])))
        self.alerts_weighted_by_priority = int(round(float(parts[5])))

        self.class_alerts = []
        self.priority_alerts = []
        for i in range(6, len(set(constants.SNORT_IDS_ROUTER.SNORT_ALERT_IDS_ID.values())) + 6):
            self.class_alerts.append(int(round(float(parts[i]))))
        for i in range(len(set(constants.SNORT_IDS_ROUTER.SNORT_ALERT_IDS_ID.values())) + 6,
                       len(set(constants.SNORT_IDS_ROUTER.SNORT_ALERT_IDS_ID.values())) + 10):
            self.priority_alerts.append(int(round(float(parts[i]))))

    def to_kafka_record(self, ip: str) -> str:
        """
        Converts the DTO into a kafka record

        :param ip: the ip to add to the record in addition to the IDS statistics
        :return: a comma-separated string representing the kafka record
        """
        ts = time.time()
        total_counters = [ts, ip, self.total_alerts, self.warning_alerts, self.severe_alerts,
                          self.alerts_weighted_by_priority] + self.class_alerts + self.priority_alerts
        record_str = ",".join(list(map(lambda x: str(x), total_counters)))
        return record_str

    def to_dto(self, ip: str) -> csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsLogDTO:
        """
        Converts the object into a gRPC DTO for serialization

        :param ip: the ip to add to the DTO in addition to the statistics
        :return: A csle_collector.snort_ids_manager.snort_ids_manager_pb2.IdsLogDTOb
        """
        ts = time.time()
        return csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsLogDTO(
            timestamp=ts,
            ip=ip,
            attempted_admin_alerts=int(self.class_alerts[33]),
            attempted_user_alerts=int(self.class_alerts[32]),
            inappropriate_content_alerts=int(self.class_alerts[31]),
            policy_violation_alerts=int(self.class_alerts[30]),
            shellcode_detect_alerts=int(self.class_alerts[29]),
            successful_admin_alerts=int(self.class_alerts[28]),
            successful_user_alerts=int(self.class_alerts[27]),
            trojan_activity_alerts=int(self.class_alerts[26]),
            unsuccessful_user_alerts=int(self.class_alerts[25]),
            web_application_attack_alerts=int(self.class_alerts[24]),
            attempted_dos_alerts=int(self.class_alerts[23]),
            attempted_recon_alerts=int(self.class_alerts[22]),
            bad_unknown_alerts=int(self.class_alerts[21]),
            default_login_attempt_alerts=int(self.class_alerts[20]),
            denial_of_service_alerts=int(self.class_alerts[19]),
            misc_attack_alerts=int(self.class_alerts[18]),
            non_standard_protocol_alerts=int(self.class_alerts[17]),
            rpc_portman_decode_alerts=int(self.class_alerts[16]),
            successful_dos_alerts=int(self.class_alerts[15]),
            successful_recon_largescale_alerts=int(self.class_alerts[14]),
            successful_recon_limited_alerts=int(self.class_alerts[13]),
            suspicious_filename_detect_alerts=int(self.class_alerts[12]),
            suspicious_login_alerts=int(self.class_alerts[11]),
            system_call_detect_alerts=int(self.class_alerts[10]),
            unusual_client_port_connection_alerts=int(self.class_alerts[9]),
            web_application_activity_alerts=int(self.class_alerts[8]),
            icmp_event_alerts=int(self.class_alerts[7]),
            misc_activity_alerts=int(self.class_alerts[6]),
            network_scan_alerts=int(self.class_alerts[5]),
            not_suspicious_alerts=int(self.class_alerts[4]),
            protocol_command_decode_alerts=int(self.class_alerts[3]),
            string_detect_alerts=int(self.class_alerts[2]),
            unknown_alerts=int(self.class_alerts[1]),
            tcp_connection_alerts=int(self.class_alerts[0]),
            priority_1_alerts=int(self.priority_alerts[0]),
            priority_2_alerts=int(self.priority_alerts[1]),
            priority_3_alerts=int(self.priority_alerts[2]),
            priority_4_alerts=int(self.priority_alerts[3]),
            total_alerts=self.total_alerts,
            warning_alerts=self.warning_alerts,
            severe_alerts=self.severe_alerts,
            alerts_weighted_by_priority=self.alerts_weighted_by_priority
        )

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"total_alerts: {self.total_alerts}, warning_alerts: {self.warning_alerts}, " \
               f"severe_alerts: {self.severe_alerts}, " \
               f"priority_alerts: {self.priority_alerts}, class_alerts: {self.class_alerts}," \
               f"alerts_weighted_by_priority: {self.alerts_weighted_by_priority}"

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SnortIdsAlertCounters":
        """
        Converts a dict representaion of the object into an instance

        :param d: the dict to convert
        :return: the DTO
        """
        obj = SnortIdsAlertCounters()
        obj.ip = d["ip"]
        obj.ts = d["ts"]
        obj.total_alerts = d["total_alerts"]
        obj.warning_alerts = d["warning_alerts"]
        obj.severe_alerts = d["severe_alerts"]
        obj.priority_alerts = d["priority_alerts"]
        obj.class_alerts = d["class_alerts"]
        obj.alerts_weighted_by_priority = d["alerts_weighted_by_priority"]
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["ip"] = self.ip
        d["ts"] = self.ts
        d["class_alerts"] = list(self.class_alerts)
        d["priority_alerts"] = list(self.priority_alerts)
        d["total_alerts"] = self.total_alerts
        d["warning_alerts"] = self.warning_alerts
        d["severe_alerts"] = self.severe_alerts
        d["alerts_weighted_by_priority"] = self.alerts_weighted_by_priority
        return d

    def copy(self) -> "SnortIdsAlertCounters":
        """
        :return: a copy of the object
        """
        c = SnortIdsAlertCounters()
        c.class_alerts = self.class_alerts.copy()
        c.priority_alerts = self.priority_alerts.copy()
        c.ip = self.ip
        c.ts = self.ts
        c.total_alerts = self.total_alerts
        c.warning_alerts = self.warning_alerts
        c.severe_alerts = self.severe_alerts
        c.alerts_weighted_by_priority = self.alerts_weighted_by_priority
        return c

    def get_deltas(self, counters_prime: "SnortIdsAlertCounters") -> Tuple[List[int], List[str]]:
        """
        Get the deltas between two counters objects

        :param counters_prime: the counters object to compare with
        :return: the deltas and the labels
        """
        deltas_priority = list(np.array(counters_prime.priority_alerts).astype(int).tolist())
        deltas_class = list(np.array(counters_prime.class_alerts).astype(int).tolist())
        deltas = ([int(counters_prime.total_alerts), int(counters_prime.warning_alerts),
                   int(counters_prime.severe_alerts), int(counters_prime.alerts_weighted_by_priority)]
                  + deltas_priority + deltas_class)
        labels = constants.KAFKA_CONFIG.SNORT_IDS_ALERTS_LABELS
        assert len(labels) == len(deltas)
        return list(deltas), labels

    def num_attributes(self) -> int:
        """
        :return: The number of attributes of the DTO
        """
        return 10 + len(set(constants.SNORT_IDS_ROUTER.SNORT_ALERT_IDS_ID.values()))

    @staticmethod
    def schema() -> "SnortIdsAlertCounters":
        """
        :return: get the schema of the DTO
        """
        return SnortIdsAlertCounters()

    @staticmethod
    def from_json_file(json_file_path: str) -> "SnortIdsAlertCounters":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return SnortIdsAlertCounters.from_dict(json.loads(json_str))
