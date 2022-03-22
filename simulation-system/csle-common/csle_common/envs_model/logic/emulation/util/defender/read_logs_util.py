from typing import Tuple
import datetime
from gym_csle_ctf.dao.network.env_config import CSLEEnvConfig
import csle_common.constants.constants as constants
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.logic.emulation.util.common.emulation_util import EmulationUtil
from csle_common.dao.action_results.failed_login_attempt import FailedLoginAttempt
from csle_common.dao.action_results.successful_login import SuccessfulLogin


class ReadLogsUtil:
    """
    Class containing utility functions for the defender reading logs of nodes in the emulation
    """

    @staticmethod
    def read_latest_ts_auth(emulation_config: EmulationConfig) -> int:
        """
        Measures the timestamp of the latest failed login attempt

        :param emulation_config: configuration to connect to the node in the emulation
        :return: the number of recently failed login attempts
        """
        try:
            outdata, errdata, total_time = \
                EmulationUtil.execute_ssh_cmd(cmd=constants.DEFENDER.LIST_FAILED_LOGIN_ATTEMPTS,
                                              conn=emulation_config.agent_conn)
            login_attempts_str = outdata.decode()
            login_attempts = login_attempts_str.split("\n")
            login_attempts = list(filter(lambda x: x != "" and len(x) > 14, login_attempts))
            year = datetime.datetime.now().year
            parsed_ts = FailedLoginAttempt.parse_from_str(str(year) + " "+ " ".join(login_attempts[-1][0:15].split())).timestamp
            return parsed_ts
        except:
            return datetime.datetime.now().timestamp()

    @staticmethod
    def read_failed_login_attempts(emulation_config: EmulationConfig, failed_auth_last_ts: float) -> int:
        """
        Measures the number of recent failed login attempts

        :param emulation_config: configuration to connect to the node in the emulation
        :return: the number of recently failed login attempts
        """
        outdata, errdata, total_time = \
            EmulationUtil.execute_ssh_cmd(cmd=constants.DEFENDER.LIST_FAILED_LOGIN_ATTEMPTS,
                                          conn=emulation_config.agent_conn)
        login_attempts_str = outdata.decode()
        login_attempts = login_attempts_str.split("\n")
        login_attempts = list(filter(lambda x: x != "" and len(x) > 14, login_attempts))
        year = datetime.datetime.now().year
        login_attempts = list(map(lambda x: FailedLoginAttempt.parse_from_str(
            str(year) + " "+ " ".join(x[0:15].split())), login_attempts))
        login_attempts = list(filter(lambda x: x.timestamp > failed_auth_last_ts, login_attempts))
        return len(login_attempts)

    @staticmethod
    def read_latest_ts_login(emulation_config: EmulationConfig) -> int:
        """
        Measures the timestamp of the latest successful login attempt

        :param emulation_config: configuration to connect to the node in the emulation
        :return: the number of recently failed login attempts
        """
        try:
            outdata, errdata, total_time = \
                EmulationUtil.execute_ssh_cmd(cmd=constants.DEFENDER.LIST_SUCCESSFUL_LOGIN_ATTEMPTS,
                                              conn=emulation_config.agent_conn)
            logins = outdata.decode()
            logins = logins.split("\n")
            logins = list(filter(lambda x: x != "" and len(x) > 0 and "wtmp begins" not in x, logins))
            year = datetime.datetime.now().year
            return SuccessfulLogin.parse_from_str(" ".join(logins[0].split()), year=year).timestamp
        except:
            return datetime.datetime.now().timestamp()


    @staticmethod
    def read_successful_login_events(emulation_config: EmulationConfig, login_last_ts: float) -> int:
        """
        Measures the number of recent successful login attempts

        :param emulation_config: configuration to connect to the node in the emulation
        :param login_last_ts: the timestamp to use when filtering logins
        :return: the number of recently failed login attempts
        """
        outdata, errdata, total_time = \
            EmulationUtil.execute_ssh_cmd(cmd=constants.DEFENDER.LIST_SUCCESSFUL_LOGIN_ATTEMPTS,
                                          conn=emulation_config.agent_conn)
        logins = outdata.decode()
        logins = logins.split("\n")
        logins = list(filter(lambda x: x != "" and len(x) > 0 and "wtmp begins" not in x, logins))
        year = datetime.datetime.now().year
        successful_logins = list(map(lambda x: SuccessfulLogin.parse_from_str(" ".join(x.split()), year=year),
                                     logins))
        successful_logins = list(filter(lambda x: x.timestamp != None, successful_logins))
        successful_logins = list(filter(lambda x: x.timestamp > login_last_ts, successful_logins))
        return len(successful_logins)
