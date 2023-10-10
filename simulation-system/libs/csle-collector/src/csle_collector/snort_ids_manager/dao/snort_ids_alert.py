from typing import Dict, Any
import re
import datetime
from csle_base.json_serializable import JSONSerializable
from csle_collector.snort_ids_manager.dao.snort_ids_fast_log_alert import SnortIdsFastLogAlert
import csle_collector.constants.constants as constants


class SnortIdsAlert(JSONSerializable):
    """
    Object representing an IDS Alert
    """

    def __init__(self):
        """
        Initializes the IDS Alert Fields
        """
        self.timestamp = None
        self.sig_generator = None
        self.sig_id = None
        self.sig_rev = None
        self.msg = None
        self.proto = None
        self.src_ip = None
        self.src_port = None
        self.dst_ip = None
        self.dst_port = None
        self.eth_src = None
        self.eth_dst = None
        self.eth_len = None
        self.tcp_flags = None
        self.tcp_seq = None
        self.tcp_ack = None
        self.tcp_len = None
        self.tcp_window = None
        self.ttl = None
        self.tos = None
        self.id = None
        self.dgm_len = None
        self.ip_len = None
        self.icmp_type = None
        self.icmp_code = None
        self.icmp_id = None
        self.icmp_seq = None
        self.priority = None

    @staticmethod
    def parse_from_str(csv_str_record: str, year: int) -> "SnortIdsAlert":
        """
        Parses the IDS alert from a string

        :param csv_str_record: the string to parse
        :param year: the year of the entry
        :return: the parsed IDS Alert
        """
        a_fields = csv_str_record.split(",")
        alert_dao = SnortIdsAlert()
        if len(a_fields) > 1:
            alert_dao.timestamp = a_fields[0]
            if alert_dao.timestamp is not None and alert_dao.timestamp != "" and alert_dao.timestamp != "0":
                alert_dao.timestamp = str(year) + " " + alert_dao.timestamp
                try:
                    alert_dao.timestamp = datetime.datetime.strptime(alert_dao.timestamp.strip(),
                                                                     '%Y %m/%d-%H:%M:%S.%f').timestamp()
                except Exception:
                    alert_dao.timestamp = datetime.datetime.strptime("2010 04/20-08:46:14.094913",
                                                                     '%Y %m/%d-%H:%M:%S.%f').timestamp()
            else:
                alert_dao.timestamp = datetime.datetime.strptime("2010 04/20-08:46:14.094913",
                                                                 '%Y %m/%d-%H:%M:%S.%f').timestamp()
        else:
            alert_dao.timestamp = datetime.datetime.strptime("2010 04/20-08:46:14.094913",
                                                             '%Y %m/%d-%H:%M:%S.%f').timestamp()
        if len(a_fields) > 1:
            alert_dao.sig_generator = a_fields[1]
        if len(a_fields) > 2:
            alert_dao.sig_id = a_fields[2]
        if len(a_fields) > 3:
            alert_dao.sig_rev = a_fields[3]
        if len(a_fields) > 4:
            alert_dao.msg = a_fields[4]
        if len(a_fields) > 5:
            alert_dao.proto = a_fields[5]
        if len(a_fields) > 6:
            alert_dao.src_ip = a_fields[6]
        if len(a_fields) > 7:
            alert_dao.src_port = a_fields[7]
        if len(a_fields) > 8:
            alert_dao.dst_ip = a_fields[8]
        if len(a_fields) > 9:
            alert_dao.dst_port = a_fields[9]
        if len(a_fields) > 10:
            alert_dao.eth_src = a_fields[10]
        if len(a_fields) > 11:
            alert_dao.eth_dst = a_fields[11]
        if len(a_fields) > 12:
            alert_dao.eth_len = a_fields[12]
        if len(a_fields) > 13:
            alert_dao.tcp_flags = a_fields[13]
        if len(a_fields) > 14:
            alert_dao.tcp_seq = a_fields[14]
        if len(a_fields) > 15:
            alert_dao.tcp_ack = a_fields[15]
        if len(a_fields) > 16:
            alert_dao.tcp_len = a_fields[16]
        if len(a_fields) > 17:
            alert_dao.tcp_window = a_fields[17]
        if len(a_fields) > 18:
            alert_dao.ttl = a_fields[18]
        if len(a_fields) > 19:
            alert_dao.tos = a_fields[19]
        if len(a_fields) > 20:
            alert_dao.id = a_fields[20]
        if len(a_fields) > 21:
            alert_dao.dgm_len = a_fields[21]
        if len(a_fields) > 22:
            alert_dao.ip_len = a_fields[22]
        if len(a_fields) > 23:
            alert_dao.icmp_type = a_fields[23]
        if len(a_fields) > 24:
            alert_dao.icmp_code = a_fields[24]
        if len(a_fields) > 25:
            alert_dao.icmp_id = a_fields[25]
        if len(a_fields) > 26:
            alert_dao.icmp_seq = a_fields[26]
        alert_dao.priority = 1
        return alert_dao

    def set_priority(self, priority: int) -> None:
        """
        Sets the priority of the alert DTO

        :param priority: the priority to set
        :return: None
        """
        self.priority = priority

    @staticmethod
    def fast_log_parse(fast_log_str: str, year: int) -> SnortIdsFastLogAlert:
        """
        Parses the IDS Alert from a given string from the fast-log of Snort

        :param fast_log_str: the fast log string to parse
        :param year: the year
        :return: the priority, the class, and the time-stamp
        """
        priorities = re.findall(constants.SNORT_IDS_ROUTER.PRIORITY_REGEX, fast_log_str)
        if len(priorities) > 0:
            temp = priorities[0].replace("Priority: ", "")
            priority = int(temp)
        else:
            priority = 1
        alert_classes = re.findall(constants.SNORT_IDS_ROUTER.CLASSIFICATION_REGEX, fast_log_str)
        alert_class = "unknown"
        alert_class_id = 1
        if len(alert_classes) > 0:
            alert_class = alert_classes[0]
        if alert_class in constants.SNORT_IDS_ROUTER.SNORT_ALERT_IDS_ID:
            alert_class_id = constants.SNORT_IDS_ROUTER.SNORT_ALERT_IDS_ID[alert_class]

        ts_str = fast_log_str.split(" ")[0]
        if ts_str is not None and ts_str != "":
            ts_str = ts_str.strip()
            if ts_str != "":
                ts_str = str(year) + " " + ts_str
                try:
                    ts = datetime.datetime.strptime(ts_str.strip(), '%Y %m/%d-%H:%M:%S.%f').timestamp()
                except Exception:
                    ts = datetime.datetime.strptime("2010 04/20-08:46:14.094913", '%Y %m/%d-%H:%M:%S.%f').timestamp()
            else:
                ts = datetime.datetime.strptime("2010 04/20-08:46:14.094913", '%Y %m/%d-%H:%M:%S.%f').timestamp()

        source_ip = ""
        target_ip = ""
        ips_match = re.findall(constants.SNORT_IDS_ROUTER.IPS_REGEX, fast_log_str)
        if len(ips_match) > 0:
            ips = ips_match[0].replace(" ", "").split("->")
            source_ip = ips[0]
            target_ip = ips[1]

        rule_id = ""
        rule_match = re.findall(constants.SNORT_IDS_ROUTER.RULE_ID_REGEX, fast_log_str)
        if len(rule_match) > 0:
            rule_id = rule_match[0].replace("[", "").replace(":", "-")

        fast_log_alert = SnortIdsFastLogAlert(timestamp=ts, priority=priority, class_id=alert_class_id,
                                              source_ip=source_ip, target_ip=target_ip, rule_id=rule_id)
        return fast_log_alert

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["timestamp"] = self.timestamp
        d["sig_generator"] = self.sig_generator
        d["sig_id"] = self.sig_id
        d["sig_rev"] = self.sig_rev
        d["msg"] = self.msg
        d["proto"] = self.proto
        d["src_ip"] = self.src_ip
        d["src_port"] = self.src_port
        d["dst_ip"] = self.dst_ip
        d["dst_port"] = self.dst_port
        d["eth_src"] = self.eth_src
        d["eth_dst"] = self.eth_dst
        d["eth_len"] = self.eth_len
        d["tcp_flags"] = self.tcp_flags
        d["tcp_seq"] = self.tcp_seq
        d["tcp_ack"] = self.tcp_ack
        d["tcp_len"] = self.tcp_len
        d["tcp_window"] = self.tcp_window
        d["ttl"] = self.ttl
        d["tos"] = self.tos
        d["id"] = self.id
        d["dgm_len"] = self.dgm_len
        d["ip_len"] = self.ip_len
        d["icmp_type"] = self.icmp_type
        d["icmp_code"] = self.icmp_code
        d["icmp_id"] = self.icmp_id
        d["icmp_seq"] = self.icmp_seq
        d["priority"] = self.priority
        return d

    @staticmethod
    def from_dict(parsed_stats_dict: Dict[str, Any]) -> "SnortIdsAlert":
        """
        Parses a SnortIdsAlert object from a dict

        :param parsed_stats_dict: the dict to parse
        :return: the parsed SnortIdsAlert object
        """
        snort_ids_alert = SnortIdsAlert()
        snort_ids_alert.timestamp = parsed_stats_dict["timestamp"]
        snort_ids_alert.sig_generator = parsed_stats_dict["sig_generator"]
        snort_ids_alert.sig_id = parsed_stats_dict["sig_id"]
        snort_ids_alert.sig_rev = parsed_stats_dict["sig_rev"]
        snort_ids_alert.msg = parsed_stats_dict["msg"]
        snort_ids_alert.proto = parsed_stats_dict["proto"]
        snort_ids_alert.src_ip = parsed_stats_dict["src_ip"]
        snort_ids_alert.src_port = parsed_stats_dict["src_port"]
        snort_ids_alert.dst_ip = parsed_stats_dict["dst_ip"]
        snort_ids_alert.dst_port = parsed_stats_dict["dst_port"]
        snort_ids_alert.eth_src = parsed_stats_dict["eth_src"]
        snort_ids_alert.eth_dst = parsed_stats_dict["eth_dst"]
        snort_ids_alert.eth_len = parsed_stats_dict["eth_len"]
        snort_ids_alert.tcp_flags = parsed_stats_dict["tcp_flags"]
        snort_ids_alert.tcp_seq = parsed_stats_dict["tcp_seq"]
        snort_ids_alert.tcp_ack = parsed_stats_dict["tcp_ack"]
        snort_ids_alert.tcp_len = parsed_stats_dict["tcp_len"]
        snort_ids_alert.tcp_window = parsed_stats_dict["tcp_window"]
        snort_ids_alert.ttl = parsed_stats_dict["ttl"]
        snort_ids_alert.tos = parsed_stats_dict["tos"]
        snort_ids_alert.id = parsed_stats_dict["id"]
        snort_ids_alert.dgm_len = parsed_stats_dict["dgm_len"]
        snort_ids_alert.ip_len = parsed_stats_dict["ip_len"]
        snort_ids_alert.icmp_type = parsed_stats_dict["icmp_type"]
        snort_ids_alert.icmp_code = parsed_stats_dict["icmp_code"]
        snort_ids_alert.icmp_id = parsed_stats_dict["icmp_id"]
        snort_ids_alert.icmp_seq = parsed_stats_dict["icmp_seq"]
        snort_ids_alert.priority = parsed_stats_dict["priority"]
        return snort_ids_alert

    @staticmethod
    def from_json_file(json_file_path: str) -> "SnortIdsAlert":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return SnortIdsAlert.from_dict(json.loads(json_str))
