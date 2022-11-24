from typing import Dict, Any, List
import csle_collector.constants.constants as constants


class OSSECIDSAlert:

    def __init__(self, timestamp: float, groups: List[str] = "", host: str = "", ip: str = "", rule_id: str = "",
                 level: int = 1, descr: str = "",
                 src: str = "", user: str = ""):
        """
        A DTO representing an alert from the OSSEC IDS

        :param timestamp: the timestamp of the alert
        :param groups: the groups of the alert
        :param host: the host of the alert
        :param ip: the ip of the alert
        :param rule_id: the rule id that triggered the alert
        :param level: the level of the alert
        :param descr: the description of the alert
        :param src: the source of the alert
        :param user: the user of the alert
        """
        self.timestamp = timestamp
        self.groups = groups
        self.group_ids = list(map(lambda x: self.get_group_id(x), groups))
        self.host = host
        self.ip = ip
        self.rule_id = rule_id
        self.level = level
        self.descr = descr
        self.src = src
        self.user = user

    def get_group_id(self, group: str) -> int:
        """
        Get the id of a group

        :param group: the group to get the id of
        :return: the id
        """
        if group in constants.OSSEC.OSSEC_IDS_ALERT_GROUP_ID:
            return constants.OSSEC.OSSEC_IDS_ALERT_GROUP_ID[group]
        else:
            return 0

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return f"ts: {self.timestamp}, groups: {self.groups}, host: {self.host}, ip: {self.ip}, " \
               f"rule_id: {self.rule_id}, level: {self.level}, descr: {self.descr}, src: {self.src}, " \
               f"user: {self.user}, group_ids: {self.group_ids}"

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "OSSECIDSAlert":
        """
        Converts a dict representaion of the object into an instance

        :param d: the dict to convert
        :return: the DTO
        """
        obj = OSSECIDSAlert(timestamp=d["timestamp"], groups=d["groups"], host=d["host"], ip=d["ip"],
                            rule_id=d["rule_id"], level=d["level"], descr=d["descr"], src=d["src"], user=d["user"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["timestamp"] = self.timestamp
        d["groups"] = self.groups
        d["host"] = self.host
        d["ip"] = self.ip
        d["rule_id"] = self.rule_id
        d["level"] = self.level
        d["descr"] = self.descr
        d["src"] = self.src
        d["user"] = self.user
        return d

    def copy(self) -> "OSSECIDSAlert":
        """
        :return: a copy of the DTO
        """
        return OSSECIDSAlert.from_dict(self.to_dict())
