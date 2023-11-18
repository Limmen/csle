from typing import List, Dict, Any
import time
from csle_base.json_serializable import JSONSerializable
from csle_collector.snort_ids_manager.dao.snort_ids_fast_log_alert import SnortIdsFastLogAlert


class SnortIdsRuleCounters(JSONSerializable):
    """
    DTO containing rule-statistics from the Snort IDS log
    """

    def __init__(self):
        """
        Initializes the DTO
        """
        self.rule_alerts = {}
        self.ip = ""
        self.ts = 0.0

    def add(self, alert_counters: "SnortIdsRuleCounters") -> None:
        """
        Adds another alert counters object to this one

        :param alert_counters: the counters to add
        :return: None
        """
        for k, v in alert_counters.rule_alerts.items():
            if k not in self.rule_alerts:
                self.rule_alerts[k] = int(alert_counters.rule_alerts[k])
            else:
                self.rule_alerts[k] = int(self.rule_alerts[k]) + int(alert_counters.rule_alerts[k])

    def count(self, alerts: List[SnortIdsFastLogAlert]) -> None:
        """
        Counts the list of alerts

        :param alerts: list of alerts from the log
        :return: None
        """
        for a in alerts:
            if a.rule_id not in self.rule_alerts:
                self.rule_alerts[a.rule_id] = 1
            else:
                self.rule_alerts[a.rule_id] = self.rule_alerts[a.rule_id] + 1

    @staticmethod
    def from_kafka_record(record: str) -> "SnortIdsRuleCounters":
        """
        Converts a kafka record to a DTO

        :param record: the kafka record to convert
        :return: the DTO
        """
        parts = record.split(",")
        obj = SnortIdsRuleCounters()
        obj.ts = float(parts[0])
        obj.ip = parts[1]
        rule_alerts = {}
        for i in range(2, len(parts)):
            k, v = parts[i].split(":")
            if k not in rule_alerts:
                rule_alerts[k] = int(v)
            else:
                rule_alerts[k] = rule_alerts[k] + int(v)
        obj.rule_alerts = rule_alerts
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
        for i in range(2, len(parts)):
            k, v = parts[i].split(":")
            if k not in self.rule_alerts:
                self.rule_alerts[k] = int(v)
            else:
                self.rule_alerts[k] = self.rule_alerts[k] + int(v)

    def to_kafka_record(self, ip: str) -> str:
        """
        Converts the DTO into a kafka record

        :param ip: the ip to add to the record in addition to the IDS statistics
        :return: a comma-separated string representing the kafka record
        """
        ts = time.time()
        record_list = [ts, ip]
        for k, v in self.rule_alerts.items():
            record_list.append(f"{k}:{v}")
        record_str = ",".join(list(map(lambda x: str(x), record_list)))
        return record_str

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ip: {self.ip}, ts: {self.ts}, rule_alerts: {self.rule_alerts}"

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SnortIdsRuleCounters":
        """
        Converts a dict representaion of the object into an instance

        :param d: the dict to convert
        :return: the DTO
        """
        obj = SnortIdsRuleCounters()
        obj.ip = d["ip"]
        obj.ts = d["ts"]
        obj.rule_alerts = d["rule_alerts"]
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["ip"] = self.ip
        d["ts"] = self.ts
        d["rule_alerts"] = self.rule_alerts
        return d

    def copy(self) -> "SnortIdsRuleCounters":
        """
        :return: a copy of the object
        """
        c = SnortIdsRuleCounters()
        c.ip = self.ip
        c.ts = self.ts
        c.rule_alerts = self.rule_alerts.copy()
        return c

    @staticmethod
    def schema() -> "SnortIdsRuleCounters":
        """
        :return: get the schema of the DTO
        """
        return SnortIdsRuleCounters()

    @staticmethod
    def from_json_file(json_file_path: str) -> "SnortIdsRuleCounters":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return SnortIdsRuleCounters.from_dict(json.loads(json_str))
