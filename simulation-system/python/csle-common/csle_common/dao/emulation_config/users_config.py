from typing import List, Dict, Any
from csle_common.dao.emulation_config.node_users_config import NodeUsersConfig


class UsersConfig:
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
        root_usernames = []
        for users_config in self.users_configs:
            if users_config.ip in ips:
                root_usernames = root_usernames + users_config.users
        return root_usernames

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
