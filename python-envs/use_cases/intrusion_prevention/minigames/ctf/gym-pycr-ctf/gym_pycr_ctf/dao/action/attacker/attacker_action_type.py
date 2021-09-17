"""
Type of attack actions in the pycr-ctf environment
"""
from enum import Enum


class AttackerActionType(Enum):
    """
    Enum representing the different attack types in the network.
    """
    RECON = 0
    EXPLOIT = 1
    POST_EXPLOIT = 2
    PRIVILEGE_ESCALATION = 3
    STOP = 4
    CONTINUE = 5