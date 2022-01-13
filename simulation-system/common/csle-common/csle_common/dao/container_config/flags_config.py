from typing import List
from csle_common.dao.container_config.node_flags_config import NodeFlagsConfig


class FlagsConfig:
    """
    A DTO representing the set of flags in an emulation environment
    """

    def __init__(self, flags : List[NodeFlagsConfig]):
        """
        Initializes the DTO

        :param flags: the list of flags
        """
        self.flags = flags

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return ",".join(list(map(lambda x: str(x), self.flags)))