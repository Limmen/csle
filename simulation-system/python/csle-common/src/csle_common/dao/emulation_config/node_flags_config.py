from typing import List, Dict, Any
from csle_common.dao.emulation_config.flag import Flag
from csle_common.util.general_util import GeneralUtil


class NodeFlagsConfig:
    """
    A DTO object representing the set of flags at a specific container in an emulation environment
    """

    def __init__(self, ip: str, flags: List[Flag]):
        """
        Initializes the DTO

        :param ip: the ip of the node
        :param flags: the list of flags
        """
        self.ip = ip
        self.flags = flags

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["ip"] = self.ip
        d["flags"] = list(map(lambda x: x.to_dict(), self.flags))
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NodeFlagsConfig":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        return NodeFlagsConfig(ip=d["ip"], flags=list(map(lambda x: Flag.from_dict(x), d["flags"])))

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "ip:{}, flags:{}".format(self.ip, ",".join(list(map(lambda x: str(x), self.flags))))

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

    def copy(self) -> "NodeFlagsConfig":
        """
        :return: a copy of the DTO
        """
        return NodeFlagsConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "NodeFlagsConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.ip = GeneralUtil.replace_first_octet_of_ip(ip=config.ip, ip_first_octet=ip_first_octet)
        return config
