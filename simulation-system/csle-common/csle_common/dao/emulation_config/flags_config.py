from typing import List
from csle_common.dao.emulation_config.node_flags_config import NodeFlagsConfig
from csle_common.dao.emulation_config.flag import Flag


class FlagsConfig:
    """
    A DTO representing the set of flags in an emulation environment
    """

    def __init__(self, node_flag_configs : List[NodeFlagsConfig]):
        """
        Initializes the DTO

        :param node_flag_configs: the list of flags
        """
        self.node_flag_configs = node_flag_configs

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["flags"] = list(map(lambda x: x.to_dict(), self.node_flag_configs))
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return ",".join(list(map(lambda x: str(x), self.node_flag_configs)))

    def get_flags_for_ips(self, ips: List[str]) -> List[Flag]:
        """
        Get all flags for a list of ip addresses

        :param ips: the list of ip addresses to get flags for
        :return: the list of flags
        """
        flags = []
        for node_flag_config in self.node_flag_configs:
            if node_flag_config.ip in ips:
                flags = flags + node_flag_config.flags
        return flags