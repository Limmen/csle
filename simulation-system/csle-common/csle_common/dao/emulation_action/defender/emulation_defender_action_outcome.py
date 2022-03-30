"""
Type of defense action outcomes
"""
from enum import IntEnum


class EmulationDefenderActionOutcome(IntEnum):
    """
    Enum representing the different defense outcomes in the network.
    """
    GAME_END = 0
    CONTINUE = 1
    STATE_UPDATE = 2
    ADD_DEFENSIVE_MECHANISM = 3
