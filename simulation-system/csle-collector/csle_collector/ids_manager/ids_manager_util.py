from typing import List, Tuple
import datetime
import subprocess
from csle_collector.ids_manager.ids_alert import IdsAlert
import csle_collector.constants.constants as constants


class IdsManagerUtil:

    @staticmethod
    def check_ids_alerts() -> List[IdsAlert]:
        """
        Reads alerts from the IDS alerts log

        :return: a list of alerts
        """
        cmd = constants.IDS_ROUTER.TAIL_ALERTS_COMMAND + " " + constants.IDS_ROUTER.ALERTS_FILE
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p.wait()
        alerts = []
        year = datetime.datetime.now().year
        for line in output.decode().split("\n"):
            a_str = line.replace("\n", "")
            alerts.append(IdsAlert.parse_from_str(a_str, year=year))
        return alerts

    @staticmethod
    def check_ids_fast_log() -> List[Tuple[int, float]]:
        """
        Reads alerts from the IDS fast-log

        :param env_config: the environment config
        :return: a list of alerts
        """
        cmd = constants.IDS_ROUTER.TAIL_FAST_LOG_COMMAND + " " + constants.IDS_ROUTER.FAST_LOG_FILE
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p.wait()
        fast_logs = []
        year = datetime.datetime.now().year
        for line in output.decode().split("\n"):
            if line != None and line != "" and line != " ":
                a_str = line.replace("\n", "")
                priority, ts = IdsAlert.fast_log_parse(a_str, year=year)
                fast_logs.append((priority, ts))
        return fast_logs


    @staticmethod
    def get_latest_alert_ts() -> float:
        """
        Gets the latest timestamp in the snort alerts log

        :param env_config: the environment config
        :return: the latest timestamp
        """
        cmd = constants.IDS_ROUTER.TAIL_ALERTS_LATEST_COMMAND + " " + constants.IDS_ROUTER.ALERTS_FILE
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p.wait()
        year = datetime.datetime.now().year
        alerts = []
        year = datetime.datetime.now().year
        for line in output.decode().split("\n"):
            if line != "" and line != None and line != " ":
                a_str = line.replace("\n", "")
                alerts.append(IdsAlert.parse_from_str(a_str, year=year))
        if len(alerts) == 0:
            # retry once
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            p.wait()
            alerts = []
            for line in output.decode().split("\n"):
                if line != "" and line != None and line != " ":
                    a_str = line.replace("\n", "")
                    alerts.append(IdsAlert.parse_from_str(a_str, year=year))
            if len(alerts) == 0:
                return datetime.datetime.now().timestamp()
            else:
                return alerts[0].timestamp
        else:
            return alerts[0].timestamp

    @staticmethod
    def read_ids_data(episode_last_alert_ts : datetime, defender_ids_severity_threshold : int = 3) -> Tuple[int, int, int, int]:
        """
        Measures metrics from the ids

        :param env_config: environment configuration
        :param episode_last_alert_ts: timestamp when the episode started
        :param defender_ids_severity_threshold: the priority threshold to classify an alert as severe
        :return: ids statistics
        """

        # Read IDS data
        alerts = IdsManagerUtil.check_ids_alerts()
        fast_logs = IdsManagerUtil.check_ids_fast_log()

        # Filter IDS data from beginning of episode
        alerts = list(filter(lambda x: x.timestamp > episode_last_alert_ts, alerts))
        fast_logs = list(filter(lambda x: x[1] > episode_last_alert_ts, fast_logs))

        # Measure total alerts
        num_alerts = len(alerts)
        num_severe_alerts = len(list(filter(lambda x: x[0] >= defender_ids_severity_threshold, fast_logs)))
        num_warning_alerts = len(
            list(filter(lambda x: x[0] < defender_ids_severity_threshold, fast_logs)))
        sum_priority_alerts = sum(list(map(lambda x: x[0], fast_logs)))

        if num_alerts < num_severe_alerts + num_warning_alerts:
            num_alerts = num_severe_alerts + num_warning_alerts

        return num_alerts, num_severe_alerts, num_warning_alerts, sum_priority_alerts