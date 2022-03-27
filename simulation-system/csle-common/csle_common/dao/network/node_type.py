"""
Type of nodes in the csle-ctf environment
"""
from enum import Enum


class NodeType(Enum):
    """
    Enum representing the different node types in the network.
    """
    HACKER = 0
    ROUTER = 1
    SERVER = 2
    CLIENT = 3