"""
Type of state representations in the pycr-pwcrack environment
"""
from enum import Enum

class StateType(Enum):
    """
    Enum representing the different state types
    """
    BASE = 0
    COMPACT = 1
    ESSENTIAL = 2