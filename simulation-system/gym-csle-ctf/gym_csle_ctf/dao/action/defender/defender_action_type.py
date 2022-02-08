"""
Type of defense actions in the csle-ctf environment
"""
from enum import Enum


class DefenderActionType(Enum):
    """
    Enum representing the different defense types in the network.
    """
    STOP = 0
    CONTINUE = 1
    STATE_UPDATE = 2
    ADD_DEFENSIVE_MECHANISM = 3
