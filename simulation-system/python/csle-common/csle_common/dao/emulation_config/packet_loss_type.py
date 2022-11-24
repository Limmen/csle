"""
Type of packet losses on a container's network interface
"""
from enum import IntEnum


class PacketLossType(IntEnum):
    """
    Enum representing the different types of packet losses to emulate on a container
    """
    RANDOM = 0
    STATE = 1
    GEMODEL = 2
