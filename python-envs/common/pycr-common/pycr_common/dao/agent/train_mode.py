from enum import Enum


class TrainMode(Enum):
    """
    Enum representing the different training modes
    """
    TRAIN_ATTACKER = 0
    TRAIN_DEFENDER = 1
    SELF_PLAY = 2