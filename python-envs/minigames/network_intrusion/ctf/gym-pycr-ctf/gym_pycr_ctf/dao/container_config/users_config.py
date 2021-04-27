from typing import List
from gym_pycr_ctf.dao.container_config.node_users_config import NodeUsersConfig


class UsersConfig:
    """
    A DTO object representing the users configuration of an emulation environment
    """
    def __init__(self, users : List[NodeUsersConfig]):
        self.users = users

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "users:{}".format(",".join(list(map(lambda x: str(x), self.users))))