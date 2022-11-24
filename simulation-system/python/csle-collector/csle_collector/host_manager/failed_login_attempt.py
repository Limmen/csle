import datetime


class FailedLoginAttempt:
    """
    Class representing a failed login event on some server in the emulation
    """

    def __init__(self):
        """
        Initializes the object
        """
        self.timestamp = None

    @staticmethod
    def parse_from_str(login_attempt_str: str):
        """
        Parses a failed login event DTO from a string

        :param login_attempt_str: the string to parse
        :return: the parsed DTO
        """
        failed_login_attempt_dto = FailedLoginAttempt()
        failed_login_attempt_dto.timestamp = \
            datetime.datetime.strptime(login_attempt_str, '%Y %b %d %H:%M:%S').timestamp()
        return failed_login_attempt_dto

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "timestamp:{}".format(self.timestamp)
