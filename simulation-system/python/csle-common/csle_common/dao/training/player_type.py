from enum import IntEnum


class PlayerType(IntEnum):
    """
    Enum representing the different player types in CSLE
    """
    ATTACKER=0
    DEFENDER=1
    SELF_PLAY=2