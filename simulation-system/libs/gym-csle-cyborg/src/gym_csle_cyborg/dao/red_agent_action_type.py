from enum import IntEnum


class RedAgentActionType(IntEnum):
    """
    Enum representing the different red agent action types in CyBorg
    """
    DISCOVER_REMOTE_SYSTEMS = 0
    DISCOVER_NETWORK_SERVICES = 1
    EXPLOIT_REMOTE_SERVICE = 2
    PRIVILEGE_ESCALATE = 3
    IMPACT = 4

    @staticmethod
    def from_str(action_str: str) -> "RedAgentActionType":
        """
        Converts an action string to an enum

        :param action_str: the string to convert
        :return: the enum corresponding to the string
        """
        if action_str == "DiscoverRemoteSystems":
            return RedAgentActionType.DISCOVER_REMOTE_SYSTEMS
        elif action_str == "DiscoverNetworkServices":
            return RedAgentActionType.DISCOVER_NETWORK_SERVICES
        elif action_str == "ExploitRemoteService":
            return RedAgentActionType.EXPLOIT_REMOTE_SERVICE
        elif action_str == "PrivilegeEscalate":
            return RedAgentActionType.PRIVILEGE_ESCALATE
        elif action_str == "Impact":
            return RedAgentActionType.IMPACT
        else:
            raise ValueError(f"Action name: {action_str} not recognized")
