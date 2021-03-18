"""
Type of nmap addresses in the pycr-ctf environment
"""
from enum import Enum

class NmapAddrType(Enum):
    """
    Enum representing the different address types in the network.
    """
    IP = 0
    MAC = 1