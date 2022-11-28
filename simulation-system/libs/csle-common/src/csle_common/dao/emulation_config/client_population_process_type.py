"""
Type of process that generates new clients for an emulation
"""

from enum import IntEnum


class ClientPopulationProcessType(IntEnum):
    """
    Enum representing the different process types for generating client process in an emulation
    """
    POISSON = 0
    SINE_MODULATED_POISSON = 1
