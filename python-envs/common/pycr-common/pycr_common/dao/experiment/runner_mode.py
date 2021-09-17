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
    MANUAL_ATTACKER = 2
    TRAIN_DEFENDER = 3
    SELF_PLAY = 4
