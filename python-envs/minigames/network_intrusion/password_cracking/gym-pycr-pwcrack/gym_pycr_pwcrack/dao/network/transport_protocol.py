"""
Transport protocols in the pycr-pwcrack environment
"""
from enum import Enum

class TransportProtocol(Enum):
    """
    Enum representing the different transport protocols in the network.
    """
    TCP = 0
    UDP = 1