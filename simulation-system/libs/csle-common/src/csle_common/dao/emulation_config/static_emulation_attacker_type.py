"""
Type of vulnerabilities in an emulation
"""

from enum import IntEnum


class StaticEmulationAttackerType(IntEnum):
    """
    Enum representing the different static emulation attacker types
    """
    NOVICE = 0
    EXPERIENCED = 1
    EXPERT = 2
