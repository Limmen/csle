"""
Type of actions in the pycr-pwcrack environment
"""
from enum import Enum

class ActionType(Enum):
    """
    Enum representing the different attack types in the network.
    """
    RECON = 0
    EXPLOIT = 1
    POST_EXPLOIT = 2
    PRIVILEGE_ESCALATION = 3