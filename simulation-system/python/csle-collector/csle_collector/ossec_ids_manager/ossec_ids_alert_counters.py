from typing import List, Dict, Any, Tuple
import time
import numpy as np
import csle_collector.constants.constants as constants
from csle_collector.ossec_ids_manager.ossec_ids_alert import OSSECIDSAlert
import csle_collector.ossec_ids_manager.ossec_ids_manager_pb2


class OSSECIdsAlertCounters:
    """
    DTO containing statistics from the OSSEC log
    """
    def __init__(self):
        """
        Initializes the DTO
        """
        self.level_alerts = list(np.zeros(16))
        self.group_alerts = list(np.zeros(len(set(constants.OSSEC.OSSEC_IDS_ALERT_GROUP_ID.values()))))
        self.severe_alerts = 0
        self.warning_alerts = 0
        self.total_alerts = 0
        self.alerts_weighted_by_level = 0
        self.ip = None
        self.ts = None

    def add(self, alert_counters: "OSSECIdsAlertCounters") -> None:
        """
        Adds another alert counters object to this one

        :param alert_counters: the counters to add
        :return: None
        """
        self.severe_alerts = self.severe_alerts + alert_counters.severe_alerts
        self.warning_alerts = self.warning_alerts + alert_counters.warning_alerts
        self.total_alerts = self.total_alerts + alert_counters.total_alerts
        self.alerts_weighted_by_level = self.alerts_weighted_by_level + alert_counters.alerts_weighted_by_level
        for idx in range(len(self.level_alerts)):
            self.level_alerts[idx] = self.level_alerts[idx] + alert_counters.level_alerts[idx]
        for idx in range(len(self.group_alerts)):
            self.group_alerts[idx] = self.group_alerts[idx] + alert_counters.group_alerts[idx]

    def count(self, alerts: List[OSSECIDSAlert]) -> None:
        """
        Counts the list of alerts

        :param alerts: list of alerts from the log
        :return: None
        """
        for a in alerts:
            if a.level in range(0, len(self.level_alerts)):
                self.level_alerts[a.level] += 1
            for group_id in a.group_ids:
                if group_id in range(0, len(self.group_alerts)):
                    self.group_alerts[group_id] += 1

        self.total_alerts = len(alerts)
        self.severe_alerts = sum(self.level_alerts[0:constants.OSSEC.OSSEC_SEVERE_ALERT_LEVEL_THRESHOLD])
        self.warning_alerts = sum(self.level_alerts[constants.OSSEC.OSSEC_SEVERE_ALERT_LEVEL_THRESHOLD:])
        self.alerts_weighted_by_level = 0
        for idx in range(len(self.level_alerts)):
            level = idx
            self.alerts_weighted_by_level += level * self.level_alerts[idx]

    @staticmethod
    def from_kafka_record(record: str) -> "OSSECIdsAlertCounters":
        """
        Converts a kafka record to a DTO

        :param record: the kafka record to convert
        :return: the DTO
        """
        parts = record.split(",")
        obj = OSSECIdsAlertCounters()
        obj.ts = float(parts[0])
        obj.ip = parts[1]
        obj.total_alerts = int(round(float(parts[2])))
        obj.warning_alerts = int(round(float(parts[3])))
        obj.severe_alerts = int(round(float(parts[4])))
        obj.alerts_weighted_by_level = int(round(float(parts[5])))
        obj.group_alerts = []
        obj.level_alerts = []
        for i in range(6, len(set(constants.OSSEC.OSSEC_ALERT_RULE_ID_TO_DESCR.keys())) + 6):
            obj.level_alerts.append(int(round(float(parts[i]))))
        for i in range(len(set(constants.OSSEC.OSSEC_ALERT_RULE_ID_TO_DESCR.keys())) + 6,
                       len(set(constants.OSSEC.OSSEC_IDS_ALERT_GROUP_ID.values())) +
                       len(set(constants.OSSEC.OSSEC_ALERT_RULE_ID_TO_DESCR.keys())) + 6):
            obj.group_alerts.append(int(round(float(parts[i]))))
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
        self.alerts_weighted_by_level = int(round(float(parts[5])))

        self.group_alerts = []
        self.level_alerts = []
        for i in range(6, len(set(constants.OSSEC.OSSEC_ALERT_RULE_ID_TO_DESCR.keys())) + 6):
            self.level_alerts.append(int(round(float(parts[i]))))
        for i in range(len(set(constants.OSSEC.OSSEC_ALERT_RULE_ID_TO_DESCR.keys())) + 6,
                       len(set(constants.OSSEC.OSSEC_IDS_ALERT_GROUP_ID.values()))
                       + len(set(constants.OSSEC.OSSEC_ALERT_RULE_ID_TO_DESCR.keys())) + 6):
            self.group_alerts.append(int(round(float(parts[i]))))

    def to_kafka_record(self, ip: str) -> str:
        """
        Converts the DTO into a kafka record

        :param ip: the ip to add to the record in addition to the IDS statistics
        :return: a comma-separated string representing the kafka record
        """
        ts = time.time()
        total_counters = [ts, ip, self.total_alerts, self.warning_alerts, self.severe_alerts,
                          self.alerts_weighted_by_level] + self.group_alerts + self.level_alerts
        record_str = ",".join(list(map(lambda x: str(x), total_counters)))
        return record_str

    def to_dto(self, ip: str) -> csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsLogDTO:
        """
        Converts the object into a gRPC DTO for serialization

        :param ip: the ip to add to the DTO in addition to the statistics
        :return: A csle_collector.snort_ids_manager.snort_ids_manager_pb2.IdsLogDTOb
        """
        ts = time.time()
        csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsLogDTO(
            timestamp=ts,
            ip=ip,
            total_alerts=self.total_alerts,
            warning_alerts=self.warning_alerts,
            severe_alerts=self.severe_alerts,
            alerts_weighted_by_level=self.alerts_weighted_by_level,
            level_0_alerts=self.level_alerts[0],
            level_1_alerts=self.level_alerts[1],
            level_2_alerts=self.level_alerts[2],
            level_3_alerts=self.level_alerts[3],
            level_4_alerts=self.level_alerts[4],
            level_5_alerts=self.level_alerts[5],
            level_6_alerts=self.level_alerts[6],
            level_7_alerts=self.level_alerts[7],
            level_8_alerts=self.level_alerts[8],
            level_9_alerts=self.level_alerts[9],
            level_10_alerts=self.level_alerts[10],
            level_11_alerts=self.level_alerts[11],
            level_12_alerts=self.level_alerts[12],
            level_13_alerts=self.level_alerts[13],
            level_14_alerts=self.level_alerts[14],
            level_15_alerts=self.level_alerts[15],
            invalid_login_alerts=self.group_alerts[0],
            authentication_success_alerts=self.group_alerts[1],
            authentication_failed_alerts=self.group_alerts[2],
            connection_attempt_alerts=self.group_alerts[3],
            attacks_alerts=self.group_alerts[4],
            adduser_alerts=self.group_alerts[5],
            sshd_alerts=self.group_alerts[6],
            ids_alerts=self.group_alerts[7],
            firewall_alerts=self.group_alerts[8],
            squid_alerts=self.group_alerts[9],
            apache_alerts=self.group_alerts[10],
            syslog_alerts=self.group_alerts[11]
        )

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"total_alerts: {self.total_alerts}, warning_alerts: {self.warning_alerts}, " \
               f"severe_alerts: {self.severe_alerts}, " \
               f"group_alerts: {self.level_alerts}, group_alerts: {self.group_alerts}," \
               f"alerts_weighted_by_level: {self.alerts_weighted_by_level}"

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "OSSECIdsAlertCounters":
        """
        Converts a dict representation of the object into an instance

        :param d: the dict to convert
        :return: the DTO
        """
        obj = OSSECIdsAlertCounters()
        obj.ip = d["ip"]
        obj.ts = d["ts"]
        obj.total_alerts = d["total_alerts"]
        obj.warning_alerts = d["warning_alerts"]
        obj.severe_alerts = d["severe_alerts"]
        obj.level_alerts = d["level_alerts"]
        obj.group_alerts = d["group_alerts"]
        obj.alerts_weighted_by_level = d["alerts_weighted_by_level"]
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["ip"] = self.ip
        d["ts"] = self.ts
        d["group_alerts"] = self.group_alerts
        d["level_alerts"] = self.level_alerts
        d["total_alerts"] = self.total_alerts
        d["warning_alerts"] = self.warning_alerts
        d["severe_alerts"] = self.severe_alerts
        d["alerts_weighted_by_level"] = self.alerts_weighted_by_level
        return d

    def copy(self) -> "OSSECIdsAlertCounters":
        """
        :return: a copy of the object
        """
        c = OSSECIdsAlertCounters()
        c.group_alerts = self.group_alerts
        c.level_alerts = self.level_alerts
        c.ip = self.ip
        c.ts = self.ts
        c.total_alerts = self.total_alerts
        c.warning_alerts = self.warning_alerts
        c.severe_alerts = self.severe_alerts
        c.alerts_weighted_by_level = self.alerts_weighted_by_level
        return c

    def get_deltas(self, counters_prime: "OSSECIdsAlertCounters") -> Tuple[List[int], List[str]]:
        """
        Get the deltas between two counters objects

        :param counters_prime: the counters object to compare with
        :return: the deltas and the labels
        """
        deltas_level = list(np.array(counters_prime.level_alerts).astype(int).tolist())
        deltas_group = list(np.array(counters_prime.group_alerts).astype(int).tolist())
        deltas = ([int(counters_prime.total_alerts), int(counters_prime.warning_alerts),
                  int(counters_prime.severe_alerts), int(counters_prime.alerts_weighted_by_level)] +
                  deltas_level + deltas_group)
        labels = constants.KAFKA_CONFIG.OSSEC_IDS_ALERTS_LABELS
        assert len(labels) == len(deltas)
        return list(deltas), labels

    def num_attributes(self) -> int:
        """
        :return: The number of attributes of the DTO
        """
        return 22 + len(set(constants.OSSEC.OSSEC_IDS_ALERT_GROUP_ID.values()))

    @staticmethod
    def schema() -> "OSSECIdsAlertCounters":
        """
        :return: get the schema of the DTO
        """
        return OSSECIdsAlertCounters()
