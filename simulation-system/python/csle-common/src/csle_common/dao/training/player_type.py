from enum import IntEnum


class PlayerType(IntEnum):
    """
    Enum representing the different player types in CSLE
    """
    DEFENDER = 1
    ATTACKER = 2
    SELF_PLAY = 3
