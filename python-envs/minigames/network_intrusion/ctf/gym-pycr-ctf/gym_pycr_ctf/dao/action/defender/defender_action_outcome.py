"""
Type of defense action outcomes in the pycr-ctf environment
"""
from enum import Enum


class DefenderActionOutcome(Enum):
    """
    Enum representing the different defense outcomes in the network.
    """
    GAME_END = 0
    CONTINUE = 1
