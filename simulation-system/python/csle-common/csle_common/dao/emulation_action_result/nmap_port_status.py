"""
Type of nmap port statuses
"""
from enum import IntEnum


class NmapPortStatus(IntEnum):
    """
    Enum representing the different port statuses in the network.
    """
    UP = 0
    DOWN = 1
