from typing import List
from csle_common.dao.emulation_config.node_users_config import NodeUsersConfig


class UsersConfig:
    """
    A DTO object representing the users configuration of an emulation environment
    """
    def __init__(self, users_configs : List[NodeUsersConfig]):
        """
        Initializes the DTO

        :param users_configs: the list of node users configuration
        """
        self.users_configs = users_configs


    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["users"] = list(map(lambda x: x.to_dict(), self.users_configs))
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
