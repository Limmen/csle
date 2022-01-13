"""
Type of attack action outcomes in the csle-ctf environment
"""
from enum import Enum


class AttackerActionOutcome(Enum):
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