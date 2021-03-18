"""
Type of nodes in the pycr-ctf environment
"""
from enum import Enum

class NodeType(Enum):
    """
    Enum representing the different node types in the network.
    """
    HACKER = 0
    ROUTER = 1
    SERVER = 2