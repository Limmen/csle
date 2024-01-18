from enum import IntEnum


class ActivityType(IntEnum):
    """
    Enum representing the different activity types in CAGE scenario 2
    """
    NONE = 0
    SCAN = 1
    EXPLOIT = 2

    @staticmethod
    def from_str(activity_type_str: str) -> "ActivityType":
        """
        Converts an activity type string to an enum

        :param activity_type_str: the string to convert
        :return: the enum corresponding to the string
        """
        if activity_type_str == "None":
            return ActivityType.NONE
        elif activity_type_str == "Scan":
            return ActivityType.SCAN
        elif activity_type_str == "Exploit":
            return ActivityType.EXPLOIT
        else:
            raise ValueError(f"Activity type: {activity_type_str} not recognized")
