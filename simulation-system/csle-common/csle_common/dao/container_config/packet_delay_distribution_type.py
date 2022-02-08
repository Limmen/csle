"""
Type of delay distributions on a container's network interface
"""
from enum import Enum


class PacketDelayDistributionType(Enum):
    """
    Enum representing the different types of delay distributions to emulate on a container
    """
    UNIFORM=0
    NORMAL=1
    PARETO=2
    PARETONORMAL=2

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        if self.value == 0:
            return "uniform"
        elif self.value == 1:
            return "normal"
        elif self.value == 2:
            return "pareto"
        else:
            return "paretonormal"