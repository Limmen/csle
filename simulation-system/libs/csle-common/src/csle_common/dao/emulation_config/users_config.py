from typing import List, Dict, Any
from csle_common.dao.emulation_config.node_users_config import NodeUsersConfig
from csle_base.json_serializable import JSONSerializable


class UsersConfig(JSONSerializable):
    """
    A DTO object representing the users configuration of an emulation environment
    """

    def __init__(self, users_configs: List[NodeUsersConfig]):
        """
        Initializes the DTO

        :param users_configs: the list of node users configuration
        """
        self.users_configs = users_configs

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "UsersConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = UsersConfig(
            users_configs=list(map(lambda x: NodeUsersConfig.from_dict(x), d["users_configs"]))
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d = {}
        d["users_configs"] = list(map(lambda x: x.to_dict(), self.users_configs))
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "users:{}".format(",".join(list(map(lambda x: str(x), self.users_configs))))

    def get_root_usernames(self, ips: List[str]) -> List[str]:
        """
        Gets the root usernames for a list of ips

        :param ips: the list of ips to get the root usernames for
        :return: the list of root usernames
        """
        root_usernames: List[str] = []
        for users_config in self.users_configs:
            if users_config.ip in ips:
                for user in users_config.users:
                    if user.root:
                        root_usernames.append(user.username)
        return root_usernames

    @staticmethod
    def from_json_file(json_file_path: str) -> "UsersConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return UsersConfig.from_dict(json.loads(json_str))

    def copy(self) -> "UsersConfig":
        """
        :return: a copy of the DTO
        """
        return UsersConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "UsersConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.users_configs = list(map(lambda x: x.create_execution_config(ip_first_octet=ip_first_octet),
                                        config.users_configs))
        return config
