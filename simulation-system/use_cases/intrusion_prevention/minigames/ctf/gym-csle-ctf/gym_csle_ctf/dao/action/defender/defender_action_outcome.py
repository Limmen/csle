"""
Type of defense action outcomes in the csle-ctf environment
"""
from enum import Enum


class DefenderActionOutcome(Enum):
    """
    Enum representing the different defense outcomes in the network.
    """
    GAME_END = 0
    CONTINUE = 1
    STATE_UPDATE = 2
    ADD_DEFENSIVE_MECHANISM = 3
