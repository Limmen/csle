from enum import IntEnum


class DecoyType(IntEnum):
    """
    Enum representing the different decoy types in CAGE scenario 2
    """
    APACHE = 1
    FEMITTER = 2
    HARAKA_SMPT = 3
    SMSS = 4
    SSHD = 5
    SVCHOST = 6
    TOMCAT = 7
    VSFTPD = 8
