from enum import IntEnum


class AcquisitionFunctionType(IntEnum):
    """
    Enum representing different acquisition functions
    """
    EXPECTED_IMPROVEMENT = 0
    CAUSAL_EXPECTED_IMPROVEMENT = 1
    NEGATIVE_LOWER_CONFIDENCE_BOUND = 2
    PROBABILITY_OF_IMPROVEMENT = 3
    PROBABILITY_OF_FEASIBILITY = 4
    ENTROPY_SEARCH = 5
    MAX_VALUE_ENTROPY_SEARCH = 6
    MUMBO = 7
