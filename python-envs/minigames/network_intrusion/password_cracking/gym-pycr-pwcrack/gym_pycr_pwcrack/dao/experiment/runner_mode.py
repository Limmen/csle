"""
Different types of experiments for the runner
"""
from enum import Enum

class RunnerMode(Enum):
    """
    Mode for the experiments runner
    """
    TRAIN_ATTACKER = 0
    SIMULATE = 1
