from enum import IntEnum


class BlueAgentActionType(IntEnum):
    """
    Enum representing the different blue agent action types in CAGE scenario 2
    """
    SLEEP = 0
    MONITOR = 1
    ANALYZE = 2
    REMOVE = 3
    DECOY_APACHE = 4
    DECOY_FEMITTER = 5
    DECOY_HARAKA_SMTP = 6
    DECOY_SMSS = 7
    DECOY_SSHD = 8
    DECOY_SVCHOST = 9
    DECOY_TOMCAT = 10
    DECOY_VSFTPD = 11
    RESTORE = 12

    @staticmethod
    def from_str(action_str: str) -> "BlueAgentActionType":
        """
        Converts an action string to an enum

        :param action_str: the string to convert
        :return: the enum corresponding to the string
        """
        if action_str == "Sleep":
            return BlueAgentActionType.SLEEP
        elif action_str == "Monitor":
            return BlueAgentActionType.MONITOR
        elif action_str == "Analyse":
            return BlueAgentActionType.ANALYZE
        elif action_str == "Remove":
            return BlueAgentActionType.REMOVE
        elif action_str == "DecoyApache":
            return BlueAgentActionType.DECOY_APACHE
        elif action_str == "DecoyFemitter":
            return BlueAgentActionType.DECOY_FEMITTER
        elif action_str == "DecoyHarakaSMPT":
            return BlueAgentActionType.DECOY_HARAKA_SMTP
        elif action_str == "DecoySmss":
            return BlueAgentActionType.DECOY_SMSS
        elif action_str == "DecoySSHD":
            return BlueAgentActionType.DECOY_SSHD
        elif action_str == "DecoySvchost":
            return BlueAgentActionType.DECOY_SVCHOST
        elif action_str == "DecoyTomcat":
            return BlueAgentActionType.DECOY_TOMCAT
        elif action_str == "DecoyVsftpd":
            return BlueAgentActionType.DECOY_VSFTPD
        elif action_str == "Restore":
            return BlueAgentActionType.RESTORE
        else:
            raise ValueError(f"Action name: {action_str} not recognized")
