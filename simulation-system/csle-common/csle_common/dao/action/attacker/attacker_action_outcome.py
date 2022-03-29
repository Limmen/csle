"""
Type of attack action outcomes
"""
from enum import IntEnum


class AttackerActionOutcome(IntEnum):
    """
    Enum representing the different attack outcomes in the network.
    """
    SHELL_ACCESS = 0
    INFORMATION_GATHERING = 1
    LOGIN = 2
    FLAG = 3
    PIVOTING = 4
    PRIVILEGE_ESCALATION_ROOT = 5
    GAME_END = 6
    CONTINUE = 7