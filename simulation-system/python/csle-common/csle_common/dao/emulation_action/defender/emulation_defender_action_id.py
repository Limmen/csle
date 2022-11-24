from enum import IntEnum


class EmulationDefenderActionId(IntEnum):
    """
    Enum representing the different defenses
    """
    STOP = 0
    CONTINUE = 1
    RESET_USERS = 2
    ENABLE_DPI = 3
    BLACKLIST_IPS = 4
