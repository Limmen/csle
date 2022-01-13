from typing import List
from csle_common.dao.container_config.node_users_config import NodeUsersConfig


class UsersConfig:
    """
    A DTO object representing the users configuration of an emulation environment
    """
    def __init__(self, users : List[NodeUsersConfig]):
        """
        Initializes the DTO

        :param users: the list of node users configuration
        """
        self.users = users

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "users:{}".format(",".join(list(map(lambda x: str(x), self.users))))