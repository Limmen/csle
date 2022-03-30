"""
Type of defense actions
"""
from enum import IntEnum


class EmulationDefenderActionType(IntEnum):
    """
    Enum representing the different defense types in the network.
    """
    STOP = 0
    CONTINUE = 1
    STATE_UPDATE = 2
    ADD_DEFENSIVE_MECHANISM = 3
