
from enum import Enum


class EnvMode(Enum):
    """
    Different modes of running an environment
    """
    SIMULATION = 0
    EMULATION = 1
    GENERATED_SIMULATION = 2