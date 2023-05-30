"""
Type of process that generates new clients for an emulation
"""

from enum import IntEnum


class ClientArrivalType(IntEnum):
    """
    Enum representing the different process types for generating client process in an emulation
    """
    CONSTANT = 0
    SINE_MODULATED = 1
    SPIKING = 2
    PIECE_WISE_CONSTANT = 3
    EPTMP = 4
