from typing import Dict, Any
from csle_base.json_serializable import JSONSerializable


class SnortIdsFastLogAlert(JSONSerializable):
    """
    DTO representing an alert entry in the fast log of Snort
    """

    def __init__(self, timestamp: float, priority: int, class_id: int, source_ip: str, target_ip: str, rule_id: str) \
            -> None:
        """
        Initializes the DTO

        :param timestamp: the timestamp of the record
        :param priority: the priority of the record
        :param class_id: the class id of the record
        :param source_ip: the source ip of the record
        :param target_ip: the target ip of the record
        :param rule_id: the id of the Snort rule relating to the record
        """
        self.timestamp = timestamp
        self.priority = priority
        self.class_id = class_id
        self.source_ip = source_ip
        self.target_ip = target_ip
        self.rule_id = rule_id

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["timestamp"] = self.timestamp
        d["priority"] = self.priority
        d["class_id"] = self.class_id
        d["source_ip"] = self.source_ip
        d["target_ip"] = self.target_ip
        d["rule_id"] = self.rule_id
        return d

    @staticmethod
    def from_dict(parsed_stats_dict: Dict[str, Any]) -> "SnortIdsFastLogAlert":
        """
        Parses a SnortIdsFastLogAlert object from a dict

        :param parsed_stats_dict: the dict to parse
        :return: the parsed SnortIdsFastLogAlert object
        """
        snort_ids_fast_log_alert = SnortIdsFastLogAlert(parsed_stats_dict["timestamp"], parsed_stats_dict["priority"],
                                                        parsed_stats_dict["class_id"], parsed_stats_dict["source_ip"],
                                                        parsed_stats_dict["target_ip"], parsed_stats_dict["rule_id"])
        return snort_ids_fast_log_alert

    @staticmethod
    def from_json_file(json_file_path: str) -> "SnortIdsFastLogAlert":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return SnortIdsFastLogAlert.from_dict(json.loads(json_str))
