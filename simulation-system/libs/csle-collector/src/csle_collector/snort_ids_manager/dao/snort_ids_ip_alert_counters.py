from typing import List, Dict, Any, Tuple
import time
import numpy as np
from csle_base.json_serializable import JSONSerializable
import csle_collector.constants.constants as constants
from csle_collector.snort_ids_manager.dao.snort_ids_fast_log_alert import SnortIdsFastLogAlert


class SnortIdsIPAlertCounters(JSONSerializable):
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
        self.alert_ip = ""
        self.ts = 0.0

    def add(self, alert_counters: "SnortIdsIPAlertCounters") -> None:
        """
        Adds another alert counters object to this one

        :param alert_counters: the counters to add
        :return: None
        """
        self.severe_alerts = self.severe_alerts + alert_counters.severe_alerts
        self.warning_alerts = self.warning_alerts + alert_counters.warning_alerts
        self.total_alerts = self.total_alerts + alert_counters.total_alerts
        self.alerts_weighted_by_priority = self.alerts_weighted_by_priority + alert_counters.alerts_weighted_by_priority
        for idx in range(len(self.priority_alerts)):
            self.priority_alerts[idx] = self.priority_alerts[idx] + alert_counters.priority_alerts[idx]
        for idx in range(len(self.class_alerts)):
            self.class_alerts[idx] = self.class_alerts[idx] + alert_counters.class_alerts[idx]

    def count(self, alerts: List[SnortIdsFastLogAlert]) -> None:
        """
        Counts the list of alerts

        :param alerts: list of alerts from the log
        :return: None
        """
        alerts = list(filter(lambda x: x.target_ip == self.alert_ip, alerts))
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
    def from_kafka_record(record: str) -> "SnortIdsIPAlertCounters":
        """
        Converts a kafka record to a DTO

        :param record: the kafka record to convert
        :return: the DTO
        """
        parts = record.split(",")
        obj = SnortIdsIPAlertCounters()
        obj.ts = float(parts[0])
        obj.ip = parts[1]
        obj.alert_ip = parts[2]
        obj.total_alerts = int(round(float(parts[3])))
        obj.warning_alerts = int(round(float(parts[4])))
        obj.severe_alerts = int(round(float(parts[5])))
        obj.alerts_weighted_by_priority = int(round(float(parts[6])))
        obj.class_alerts = []
        obj.priority_alerts = []
        for i in range(7, len(set(constants.SNORT_IDS_ROUTER.SNORT_ALERT_IDS_ID.values())) + 7):
            obj.class_alerts.append(int(round(float(parts[i]))))
        for i in range(len(set(constants.SNORT_IDS_ROUTER.SNORT_ALERT_IDS_ID.values())) + 7,
                       len(set(constants.SNORT_IDS_ROUTER.SNORT_ALERT_IDS_ID.values())) + 11):
            obj.priority_alerts.append(int(round(float(parts[i]))))
        return obj

    def update_with_kafka_record(self, record: str, ip: str) -> None:
        """
        Updates the DTO with a kafka record

        :param record: the kafka record to use for updating
        :return: None
        """
        parts = record.split(",")
        if parts[2] == ip:
            self.ts = float(parts[0])
            self.ip = parts[1]
            self.alert_ip = parts[2]
            self.total_alerts = int(round(float(parts[3])))
            self.warning_alerts = int(round(float(parts[4])))
            self.severe_alerts = int(round(float(parts[5])))
            self.alerts_weighted_by_priority = int(round(float(parts[6])))
            self.class_alerts = []
            self.priority_alerts = []
            for i in range(7, len(set(constants.SNORT_IDS_ROUTER.SNORT_ALERT_IDS_ID.values())) + 7):
                self.class_alerts.append(int(round(float(parts[i]))))
            for i in range(len(set(constants.SNORT_IDS_ROUTER.SNORT_ALERT_IDS_ID.values())) + 7,
                           len(set(constants.SNORT_IDS_ROUTER.SNORT_ALERT_IDS_ID.values())) + 11):
                self.priority_alerts.append(int(round(float(parts[i]))))

    def to_kafka_record(self, ip: str) -> str:
        """
        Converts the DTO into a kafka record

        :param ip: the ip to add to the record in addition to the IDS statistics
        :return: a comma-separated string representing the kafka record
        """
        ts = time.time()
        total_counters = [ts, ip, self.alert_ip, self.total_alerts, self.warning_alerts, self.severe_alerts,
                          self.alerts_weighted_by_priority] + self.class_alerts + self.priority_alerts
        record_str = ",".join(list(map(lambda x: str(x), total_counters)))
        return record_str

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"alert_ip: {self.alert_ip}, total_alerts: {self.total_alerts}, " \
               f"warning_alerts: {self.warning_alerts}, " \
               f"severe_alerts: {self.severe_alerts}, " \
               f"priority_alerts: {self.priority_alerts}, class_alerts: {self.class_alerts}," \
               f"alerts_weighted_by_priority: {self.alerts_weighted_by_priority}"

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SnortIdsIPAlertCounters":
        """
        Converts a dict representaion of the object into an instance

        :param d: the dict to convert
        :return: the DTO
        """
        obj = SnortIdsIPAlertCounters()
        obj.ip = d["ip"]
        obj.ts = d["ts"]
        obj.alert_ip = d["alert_ip"]
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
        d["alert_ip"] = self.alert_ip
        d["ts"] = self.ts
        d["class_alerts"] = list(self.class_alerts)
        d["priority_alerts"] = list(self.priority_alerts)
        d["total_alerts"] = self.total_alerts
        d["warning_alerts"] = self.warning_alerts
        d["severe_alerts"] = self.severe_alerts
        d["alerts_weighted_by_priority"] = self.alerts_weighted_by_priority
        return d

    def copy(self) -> "SnortIdsIPAlertCounters":
        """
        :return: a copy of the object
        """
        c = SnortIdsIPAlertCounters()
        c.alert_ip = self.alert_ip
        c.class_alerts = self.class_alerts
        c.priority_alerts = self.priority_alerts
        c.ip = self.ip
        c.ts = self.ts
        c.total_alerts = self.total_alerts
        c.warning_alerts = self.warning_alerts
        c.severe_alerts = self.severe_alerts
        c.alerts_weighted_by_priority = self.alerts_weighted_by_priority
        return c

    def get_deltas(self, counters_prime: "SnortIdsIPAlertCounters") -> Tuple[List[int], List[str]]:
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
        return 11 + len(set(constants.SNORT_IDS_ROUTER.SNORT_ALERT_IDS_ID.values()))

    @staticmethod
    def schema() -> "SnortIdsIPAlertCounters":
        """
        :return: get the schema of the DTO
        """
        return SnortIdsIPAlertCounters()

    @staticmethod
    def from_json_file(json_file_path: str) -> "SnortIdsIPAlertCounters":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return SnortIdsIPAlertCounters.from_dict(json.loads(json_str))
