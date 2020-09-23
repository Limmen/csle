"""
Type of action outcomes in the pycr-pwcrack environment
"""
from enum import Enum

class ActionOutcome(Enum):
    """
    Enum representing the different attack outcomes in the network.
    """
    SHELL_ACCESS = 0
    INFORMATION_GATHERING = 1
    LOGIN = 2
    FLAG = 3