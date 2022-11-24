import datetime


class SuccessfulLogin:
    """
    DTO Class representing a parsed successful login event from a server in the emulation
    """

    def __init__(self):
        """
        Initializes the DTO
        """
        self.timestamp = None
        self.ip = ""
        self.user = ""

    @staticmethod
    def parse_from_str(login_attempt_str: str, year: int):
        """
        Parses a login event from a string

        :param login_attempt_str: the string to parse
        :param year: the current year
        :return: the parsed login event
        """
        successful_login_attempt_dto = SuccessfulLogin()
        parts = login_attempt_str.split()
        if len(parts) > 6:
            successful_login_attempt_dto.user = parts[0]
            successful_login_attempt_dto.ip = parts[2]
            date_str = " ".join(parts[3:7])
            date_str = str(year) + " " + date_str
            successful_login_attempt_dto.timestamp = \
                datetime.datetime.strptime(date_str, '%Y %a %b %d %H:%M').timestamp()
        return successful_login_attempt_dto

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "ip:{}, user:{}, timestamp:{}".format(self.ip, self.user, self.timestamp)
