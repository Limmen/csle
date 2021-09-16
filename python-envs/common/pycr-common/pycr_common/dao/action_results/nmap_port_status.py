"""
Type of nmap port statuses in the pycr-ctf environment
"""
from enum import Enum


class NmapPortStatus(Enum):
    """
    Enum representing the different port statuses in the network.
    """
    UP = 0
    DOWN = 1
