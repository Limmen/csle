from typing import Tuple
import datetime
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.envs.logic.emulation.util.common.emulation_util import EmulationUtil
import gym_pycr_ctf.constants.constants as constants
from gym_pycr_ctf.dao.action_results.failed_login_attempt import FailedLoginAttempt


class ReadLogsUtil:
    """
    Class containing utility functions for the defender reading logs of nodes in the emulation
    """

    @staticmethod
    def read_latest_ts_auth(emulation_config: EmulationConfig) -> int:
        """
        Measures the latest failed login attempt

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
            return FailedLoginAttempt.parse_from_str(login_attempts[-1][0:15]).timestamp
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
        login_attempts = list(map(lambda x: FailedLoginAttempt.parse_from_str(x[0:15]), login_attempts))
        login_attempts = list(filter(lambda x: x.timestamp > failed_auth_last_ts, login_attempts))
        return len(login_attempts)


    @staticmethod
    def read_successful_login_events(emulation_config: EmulationConfig) -> int:
        """
        Measures the number of recent sucessful login attempts

        :param emulation_config: configuration to connect to the node in the emulation
        :return: the number of recently failed login attempts
        """
        pass

    @staticmethod
    def read_ids_data(env_config: EnvConfig, episode_last_alert_ts : datetime) \
            -> Tuple[int, int, int, int, int, int, int, int]:
        """
        Measures metrics from the ids

        :param env_config: environment configuration
        :param episode_last_alert_ts: timestamp when the episode started
        :return: ids statistics
        """

        # Read IDS data
        alerts = EmulationUtil.check_ids_alerts(env_config=env_config)
        fast_logs = EmulationUtil.check_ids_fast_log(env_config=env_config)

        # Filter IDS data from beginning of episode
        alerts = list(filter(lambda x: x.timestamp > episode_last_alert_ts, alerts))
        fast_logs = list(filter(lambda x: x[1] > episode_last_alert_ts, fast_logs))

        # Measure total alerts
        num_alerts = len(alerts)
        num_severe_alerts = len(list(filter(lambda x: x[0] >= env_config.defender_ids_severity_threshold, fast_logs)))
        num_warning_alerts = len(
            list(filter(lambda x: x[0] < env_config.defender_ids_severity_threshold, fast_logs)))
        sum_priority_alerts = sum(list(map(lambda x: x[0], fast_logs)))

        # Compute threshold for recent
        last_alert_ts = EmulationUtil.get_latest_alert_ts(env_config=env_config)
        recent_threshold = (datetime.datetime.fromtimestamp(last_alert_ts) - datetime.timedelta(
            seconds=env_config.defender_ids_recent_threshold_seconds)).timestamp()

        # Measure recent alerts
        recent_alerts = list(filter(lambda x: x.timestamp > recent_threshold, alerts))
        recent_fast_logs = list(filter(lambda x: x[1] > recent_threshold, fast_logs))
        num_recent_alerts = len(recent_alerts)
        num_recent_severe_alerts = len(
            list(filter(lambda x: x[0] >= env_config.defender_ids_severity_threshold, recent_fast_logs)))
        num_recent_warning_alerts = len(
            list(filter(lambda x: x[0] < env_config.defender_ids_severity_threshold, recent_fast_logs)))
        sum_recent_priority_alerts = sum(list(map(lambda x: x[0], recent_fast_logs)))

        print("num alerts:{}, num_severe_alerts:{}, num_warning_alerts:{}, sum_priority_alerts:{},"
              "num_recent_alerts:{}, num_recent_severe_alerts:{}, num_recent_warning_alerts:{},"
              "sum_recent_priority_alerts:{}".format(num_alerts, num_severe_alerts, num_warning_alerts,
                                                     sum_priority_alerts, num_recent_alerts, num_recent_severe_alerts,
                                                     num_recent_warning_alerts, sum_recent_priority_alerts))

        return num_alerts, num_severe_alerts, num_warning_alerts, sum_priority_alerts, num_recent_alerts, \
               num_recent_severe_alerts, num_recent_warning_alerts, sum_recent_priority_alerts
