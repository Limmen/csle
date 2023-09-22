from enum import IntEnum


class AcquisitionOptimizerType(IntEnum):
    """
    Enum representing different optimizers for acquisition functions
    """
    GRADIENT = 0
    CAUSAL_GRADIENT = 1
