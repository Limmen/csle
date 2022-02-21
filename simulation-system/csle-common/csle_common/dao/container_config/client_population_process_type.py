"""
Type of process that generates new clients for an emulation
"""

from enum import Enum


class ClientPopulationProcessType(Enum):
    """
    Enum representing the different process types for generating client process in an emulation
    """
    POISSON = 0
    SINUS_MODULATED_POISSON = 1