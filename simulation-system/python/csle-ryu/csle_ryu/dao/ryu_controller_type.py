"""
Type of RYU SDN controllers in CSLE
"""

from enum import IntEnum


class RYUControllerType(IntEnum):
    """
    Enum representing the different RYU SDN controller types supported in CSLE
    """
    LEARNING_SWITCH = 0
    LEARNING_SWITCH_STP = 1
