from typing import List, Dict, Any
from csle_common.dao.emulation_config.user import User


class NodeUsersConfig:
    """
    A DTO object representing the users of a container in an emulation environment
    """

    def __init__(self, ip: str, users: List[User]):
        """
        Initializes the DTO

        :param ip: the ip of the node
        :param users: the list of users
        """
        self.ip = ip
        self.users = users

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NodeUsersConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = NodeUsersConfig(
            ip=d["ip"], users=list(map(lambda x: User.from_dict(x), d["users"]))
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["ip"] = self.ip
        d["users"] = list(map(lambda x: x.to_dict(), self.users))
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "ip:{}, users:{}".format(self.ip, ",".join(list(map(lambda x: str(x), self.users))))