"""
Type of nmap host statuses
"""
from enum import IntEnum


class NmapHostStatus(IntEnum):
    """
    Enum representing the different host statuses in the network.
    """
    UP = 0
    DOWN = 1
