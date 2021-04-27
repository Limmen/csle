from typing import List, Tuple


class NodeUsersConfig:
    """
    A DTO object representing the users of a container in an emulation environment
    """

    def __init__(self, ip: str, users: List[Tuple[str, str, bool]]):
        self.ip = ip
        self.users = users

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "ip:{}, users:{}".format(self.ip, ",".join(list(map(lambda x: str(x), self.users))))