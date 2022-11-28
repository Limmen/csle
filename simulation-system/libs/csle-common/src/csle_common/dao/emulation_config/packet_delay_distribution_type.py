"""
Type of delay distributions on a container's network interface
"""
from enum import IntEnum


class PacketDelayDistributionType(IntEnum):
    """
    Enum representing the different types of delay distributions to emulate on a container
    """
    UNIFORM = 0
    NORMAL = 1
    PARETO = 2
    PARETONORMAL = 2
