from enum import IntEnum


class CompromisedType(IntEnum):
    """
    Enum representing the different compromised types in CAGE scenario 2
    """
    NO = 0
    USER = 1
    PRIVILEGED = 2
    UNKNOWN = 3

    @staticmethod
    def from_str(compromised_type_str: str) -> "CompromisedType":
        """
        Converts a compromised type string to an enum

        :param compromised_type_str: the string to convert
        :return: the enum corresponding to the string
        """
        if compromised_type_str == "No":
            return CompromisedType.NO
        elif compromised_type_str == "Unknown":
            return CompromisedType.UNKNOWN
        elif compromised_type_str == "User":
            return CompromisedType.USER
        elif compromised_type_str == "Privileged":
            return CompromisedType.PRIVILEGED
        else:
            raise ValueError(f"Compromised type: {compromised_type_str} not recognized")
