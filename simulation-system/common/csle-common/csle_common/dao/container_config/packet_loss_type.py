"""
Type of packet losses on a container's network interface
"""
from enum import Enum


class PacketLossType(Enum):
    """
    Enum representing the different types of packet losses to emulate on a container
    """
    RANDOM=0
    STATE=1
    GEMODEL=2


    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        if self.value == 0:
            return "random"
        elif self.value == 1:
            return "state"
        else:
            return "gemodel"