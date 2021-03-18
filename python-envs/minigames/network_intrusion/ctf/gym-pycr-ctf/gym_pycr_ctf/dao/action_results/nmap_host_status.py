"""
Type of nmap host statuses in the pycr-ctf environment
"""
from enum import Enum

class NmapHostStatus(Enum):
    """
    Enum representing the different host statuses in the network.
    """
    UP = 0
    DOWN = 1