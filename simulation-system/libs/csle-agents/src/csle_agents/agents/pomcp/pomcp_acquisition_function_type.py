from enum import IntEnum


class POMCPAcquisitionFunctionType(IntEnum):
    """
    Enum representing the different types of acquisition functions in POMCP
    """
    UCB = 0
    ALPHA_GO = 1
