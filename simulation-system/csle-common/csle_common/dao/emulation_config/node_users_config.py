from typing import List, Tuple


class NodeUsersConfig:
    """
    A DTO object representing the users of a container in an emulation environment
    """

    def __init__(self, ip: str, users: List[Tuple[str, str, bool]]):
        """
        Initializes the DTO

        :param ip: the ip of the node
        :param users: the list of users
        """
        self.ip = ip
        self.users = users


    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["ip"] = self.ip
        d["users"] = self.users
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "ip:{}, users:{}".format(self.ip, ",".join(list(map(lambda x: str(x), self.users))))