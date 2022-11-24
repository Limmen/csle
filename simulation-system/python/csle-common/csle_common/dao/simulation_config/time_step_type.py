from enum import IntEnum


class TimeStepType(IntEnum):
    """
    Enum representing the time-step types of a simulation
    """
    DISCRETE = 0
    CONTINUOUS = 1
