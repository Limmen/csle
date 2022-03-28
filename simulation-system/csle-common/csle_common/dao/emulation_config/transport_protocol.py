"""
Transport protocols in the csle-ctf environment
"""
from enum import IntEnum


class TransportProtocol(IntEnum):
    """
    Enum representing the different transport protocols in the network.
    """
    TCP = 0
    UDP = 1
