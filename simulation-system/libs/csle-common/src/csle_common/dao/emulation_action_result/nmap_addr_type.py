"""
Type of nmap addresses
"""
from enum import IntEnum


class NmapAddrType(IntEnum):
    """
    Enum representing the different address types in the network.
    """
    IP = 0
    MAC = 1
