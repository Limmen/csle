from typing import List
from csle_common.dao.emulation_config.flag import Flag


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
        # flags= [(name, path, id, root, score)]
        self.flags = flags

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["ip"] = self.ip
        d["flags"] = list(map(lambda x: x.to_dict(), self.flags))
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "ip:{}, flags:{}".format(self.ip, ",".join(list(map(lambda x: str(x), self.flags))))
