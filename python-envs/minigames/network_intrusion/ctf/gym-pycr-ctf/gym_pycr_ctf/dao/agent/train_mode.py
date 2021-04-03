from enum import Enum

class TrainMode(Enum):
    TRAIN_ATTACKER = 0
    TRAIN_DEFENDER = 1
    SELF_PLAY = 2