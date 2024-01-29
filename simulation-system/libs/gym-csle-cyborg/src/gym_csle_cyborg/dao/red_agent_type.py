from enum import IntEnum


class RedAgentType(IntEnum):
    """
    Enum representing the different red agent types in CyBorg
    """
    B_LINE_AGENT = 1
    MEANDER_AGENT = 2
    SLEEP_AGENT = 3
