from enum import IntEnum


class SystemModelType(IntEnum):
    """
    Enum representing the different system model types in CSLE
    """
    GAUSSIAN_MIXTURE = 0
    EMPIRICAL_DISTRIBUTION = 1
    GAUSSIAN_PROCESS = 2
