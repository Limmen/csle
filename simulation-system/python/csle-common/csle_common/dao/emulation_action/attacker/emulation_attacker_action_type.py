"""
Type of attack actions
"""
from enum import IntEnum


class EmulationAttackerActionType(IntEnum):
    """
    Enum representing the different attack types in the emulation.
    """
    RECON = 0
    EXPLOIT = 1
    POST_EXPLOIT = 2
    PRIVILEGE_ESCALATION = 3
    STOP = 4
    CONTINUE = 5
