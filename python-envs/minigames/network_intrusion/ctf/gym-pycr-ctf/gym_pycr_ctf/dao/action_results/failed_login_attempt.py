import datetime
import re
import gym_pycr_ctf.constants.constants as constants

class FailedLoginAttempt:

    def __init__(self):
        self.timestamp = None


    @staticmethod
    def parse_from_str(login_attempt_str : str):
        failed_login_attempt_dto = FailedLoginAttempt
        failed_login_attempt_dto.timestamp = datetime.datetime.strptime(login_attempt_str, '%b %d %H:%M:%S').timestamp()
        return failed_login_attempt_dto
