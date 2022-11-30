from typing import List, Dict, Any
from datetime import datetime
import subprocess
from csle_collector.ossec_ids_manager.ossec_ids_alert import OSSECIDSAlert
from csle_collector.ossec_ids_manager.ossec_ids_alert_counters import OSSECIdsAlertCounters
import csle_collector.ossec_ids_manager.ossec_ids_manager_pb2
import csle_collector.constants.constants as constants


class OSSecManagerUtil:
    """
    Class with utility functions related to the OSSEC IDS Manager
    """

    @staticmethod
    def check_ossec_ids_alerts() -> List[OSSECIDSAlert]:
        """
        Reads alerts from the OSSEC IDS alerts log

        :return: a list of alerts
        """
        cmd = constants.OSSEC.TAIL_ALERTS_COMMAND + " " + constants.OSSEC.OSSEC_ALERTS_FILE
        result = subprocess.run(cmd.split(" "), capture_output=True, text=True)
        alerts = []
        timestamp = " "
        groups = []
        host = " "
        ip = " "
        ruleid = " "
        level = 1
        desc = " "
        src = " "
        user = " "
        linesmatched = 0
        for line in result.stdout.split("\n"):
            linematched = 0

            # Test for matches. A line will have more than one matching RE.
            if constants.OSSEC.ALERTLINE_REGEX.match(line):
                linematched = 1
                match = constants.OSSEC.ALERTLINE_REGEX.match(line)
                groupstr = match.group(2).rstrip(',')
                groups = groupstr.split(',')

            if constants.OSSEC.DATELINEREGEX.match(line):
                linematched = 1
                match = constants.OSSEC.DATELINEREGEX.match(line)
                datestr = match.group(0)
                timestamp = datetime.strptime(datestr, "%Y %b %d %H:%M:%S")

            if constants.OSSEC.HOSTLINE_REGEX.match(line):
                linematched += 1
                match = constants.OSSEC.HOSTLINE_REGEX.match(line)
                host = match.group(1)
                ip = match.group(2)

            if constants.OSSEC.SERVHOSTLINE_REGEX.match(line):
                linematched += 1
                match = constants.OSSEC.SERVHOSTLINE_REGEX.match(line)
                host = match.group(1)
                ip = '0.0.0.0'

            if constants.OSSEC.RULELINE_REGEX.match(line):
                linematched += 1
                match = constants.OSSEC.RULELINE_REGEX.match(line)
                ruleid = match.group(1)
                level = match.group(2)
                desc = match.group(3)

            if constants.OSSEC.SRCIPLINE_REGEX.match(line):
                linematched += 1
                match = constants.OSSEC.SRCIPLINE_REGEX.match(line)
                src = match.group(1)

            if constants.OSSEC.USERLINE_REGEX.match(line):
                linematched += 1
                match = constants.OSSEC.USERLINE_REGEX.match(line)
                user = match.group(1)

            linesmatched += linematched

            if linematched == 0 and linesmatched > 0:
                if len(line) <= 1:
                    alert = OSSECIDSAlert(timestamp=datetime.timestamp(timestamp), groups=groups, host=host, ip=ip,
                                          rule_id=ruleid, level=level, descr=desc, src=src, user=user)
                    print(alert)
                    alerts.append(alert)
                    linesmatched = 0
                    timestamp = " "
                    groups = []
                    host = " "
                    ip = " "
                    ruleid = " "
                    level = 1
                    desc = " "
                    src = " "
                    user = " "
        return alerts

    @staticmethod
    def read_ossec_ids_data(episode_last_alert_ts: float) -> OSSECIdsAlertCounters:
        """
        Measures metrics from the OSSEC ids

        :param env_config: environment configuration
        :param episode_last_alert_ts: timestamp when the episode started
        :return: ids statistics
        """

        # Read OSSEC IDS data
        alerts = OSSecManagerUtil.check_ossec_ids_alerts()

        # Filter IDS data from beginning of episode
        alerts = list(filter(lambda x: x.timestamp > episode_last_alert_ts, alerts))

        counters = OSSECIdsAlertCounters()
        counters.count(alerts)

        return counters

    @staticmethod
    def ossec_ids_monitor_dto_to_dict(
            ossec_ids_monitor_dto: csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO) \
            -> Dict[str, Any]:
        """
        Converts a OSSECIdsMonitorDTO to a dict

        :param ossec_ids_monitor_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["monitor_running"] = ossec_ids_monitor_dto.monitor_running
        d["ossec_ids_running"] = ossec_ids_monitor_dto.ossec_ids_running
        return d

    @staticmethod
    def ossec_ids_log_dto_to_dict(
            ossec_ids_log_dto: csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsLogDTO) \
            -> Dict[str, Any]:
        """
        Converts a OSSECIdsLogDTO to a dict

        :param ossec_ids_log_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["timestamp"] = ossec_ids_log_dto.timestamp
        d["ip"] = ossec_ids_log_dto.ip
        d["attempted_admin_alerts"] = ossec_ids_log_dto.attempted_admin_alerts
        d["total_alerts"] = ossec_ids_log_dto.total_alerts
        d["warning_alerts"] = ossec_ids_log_dto.warning_alerts
        d["severe_alerts"] = ossec_ids_log_dto.severe_alerts
        d["alerts_weighted_by_level"] = ossec_ids_log_dto.alerts_weighted_by_level
        d["level_0_alerts"] = ossec_ids_log_dto.level_0_alerts
        d["level_1_alerts"] = ossec_ids_log_dto.level_1_alerts
        d["level_2_alerts"] = ossec_ids_log_dto.level_2_alerts
        d["level_3_alerts"] = ossec_ids_log_dto.level_3_alerts
        d["level_4_alerts"] = ossec_ids_log_dto.level_4_alerts
        d["level_5_alerts"] = ossec_ids_log_dto.level_5_alerts
        d["level_6_alerts"] = ossec_ids_log_dto.level_6_alerts
        d["level_7_alerts"] = ossec_ids_log_dto.level_7_alerts
        d["level_8_alerts"] = ossec_ids_log_dto.level_8_alerts
        d["level_9_alerts"] = ossec_ids_log_dto.level_9_alerts
        d["level_10_alerts"] = ossec_ids_log_dto.level_10_alerts
        d["level_11_alerts"] = ossec_ids_log_dto.level_11_alerts
        d["level_12_alerts"] = ossec_ids_log_dto.level_12_alerts
        d["level_13_alerts"] = ossec_ids_log_dto.level_13_alerts
        d["level_14_alerts"] = ossec_ids_log_dto.level_14_alerts
        d["level_15_alerts"] = ossec_ids_log_dto.level_15_alerts
        d["invalid_login_alerts"] = ossec_ids_log_dto.invalid_login_alerts
        d["authentication_success_alerts"] = ossec_ids_log_dto.authentication_success_alerts
        d["authentication_failed_alerts"] = ossec_ids_log_dto.authentication_failed_alerts
        d["connection_attempt_alerts"] = ossec_ids_log_dto.connection_attempt_alerts
        d["attacks_alerts"] = ossec_ids_log_dto.attacks_alerts
        d["adduser_alerts"] = ossec_ids_log_dto.adduser_alerts
        d["sshd_alerts"] = ossec_ids_log_dto.sshd_alerts
        d["ids_alerts"] = ossec_ids_log_dto.ids_alerts
        d["firewall_alerts"] = ossec_ids_log_dto.firewall_alerts
        d["squid_alerts"] = ossec_ids_log_dto.squid_alerts
        d["apache_alerts"] = ossec_ids_log_dto.apache_alerts
        d["syslog_alerts"] = ossec_ids_log_dto.syslog_alerts
        return d

    @staticmethod
    def ossec_ids_monitor_dto_from_dict(d: Dict[str, Any]) \
            -> csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO:
        """
        Converts a dict representation of a OSSECIDSMonitorDTO to a DTO

        :param d: the dict to convert
        :return: the converted DTO
        """
        ossec_ids_monitor_dto = csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO()
        ossec_ids_monitor_dto.monitor_running = d["monitor_running"]
        ossec_ids_monitor_dto.ossec_ids_running = d["ossec_ids_running"]
        return ossec_ids_monitor_dto

    @staticmethod
    def ossec_ids_log_dto_from_dict(d: Dict[str, Any]) \
            -> csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsLogDTO:
        """
        Converts a dict representation of a OSSECIDSLogDTO to a DTO

        :param d: the dict to convert
        :return: the converted DTO
        """
        ossec_ids_log_dto = csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsLogDTO()
        ossec_ids_log_dto.timestamp = d["timestamp"]
        ossec_ids_log_dto.ip = d["ip"]
        ossec_ids_log_dto.attempted_admin_alerts = d["attempted_admin_alerts"]
        ossec_ids_log_dto.total_alerts = d["total_alerts"]
        ossec_ids_log_dto.warning_alerts = d["warning_alerts"]
        ossec_ids_log_dto.severe_alerts = d["severe_alerts"]
        ossec_ids_log_dto.alerts_weighted_by_level = d["alerts_weighted_by_level"]
        ossec_ids_log_dto.level_0_alerts = d["level_0_alerts"]
        ossec_ids_log_dto.level_1_alerts = d["level_1_alerts"]
        ossec_ids_log_dto.level_2_alerts = d["level_2_alerts"]
        ossec_ids_log_dto.level_3_alerts = d["level_3_alerts"]
        ossec_ids_log_dto.level_4_alerts = d["level_4_alerts"]
        ossec_ids_log_dto.level_5_alerts = d["level_5_alerts"]
        ossec_ids_log_dto.level_6_alerts = d["level_6_alerts"]
        ossec_ids_log_dto.level_7_alerts = d["level_7_alerts"]
        ossec_ids_log_dto.level_8_alerts = d["level_8_alerts"]
        ossec_ids_log_dto.level_9_alerts = d["level_9_alerts"]
        ossec_ids_log_dto.level_10_alerts = d["level_10_alerts"]
        ossec_ids_log_dto.level_11_alerts = d["level_11_alerts"]
        ossec_ids_log_dto.level_12_alerts = d["level_12_alerts"]
        ossec_ids_log_dto.level_13_alerts = d["level_13_alerts"]
        ossec_ids_log_dto.level_14_alerts = d["level_14_alerts"]
        ossec_ids_log_dto.level_15_alerts = d["level_15_alerts"]
        ossec_ids_log_dto.invalid_login_alerts = d["invalid_login_alerts"]
        ossec_ids_log_dto.authentication_success_alerts = d["authentication_success_alerts"]
        ossec_ids_log_dto.authentication_failed_alerts = d["authentication_failed_alerts"]
        ossec_ids_log_dto.connection_attempt_alerts = d["connection_attempt_alerts"]
        ossec_ids_log_dto.attacks_alerts = d["attacks_alerts"]
        ossec_ids_log_dto.adduser_alerts = d["adduser_alerts"]
        ossec_ids_log_dto.sshd_alerts = d["sshd_alerts"]
        ossec_ids_log_dto.ids_alerts = d["ids_alerts"]
        ossec_ids_log_dto.firewall_alerts = d["firewall_alerts"]
        ossec_ids_log_dto.squid_alerts = d["squid_alerts"]
        ossec_ids_log_dto.apache_alerts = d["apache_alerts"]
        ossec_ids_log_dto.syslog_alerts = d["syslog_alerts"]
        return ossec_ids_log_dto

    @staticmethod
    def ossec_ids_log_dto_empty() \
            -> csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsLogDTO:
        """
        :return: an empty OSSECIdsLogDTO
        """
        ossec_ids_log_dto = csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsLogDTO()
        ossec_ids_log_dto.timestamp = 0.0
        ossec_ids_log_dto.ip = ""
        ossec_ids_log_dto.attempted_admin_alerts = 0
        ossec_ids_log_dto.total_alerts = 0
        ossec_ids_log_dto.warning_alerts = 0
        ossec_ids_log_dto.severe_alerts = 0
        ossec_ids_log_dto.alerts_weighted_by_level = 0
        ossec_ids_log_dto.level_0_alerts = 0
        ossec_ids_log_dto.level_1_alerts = 0
        ossec_ids_log_dto.level_2_alerts = 0
        ossec_ids_log_dto.level_3_alerts = 0
        ossec_ids_log_dto.level_4_alerts = 0
        ossec_ids_log_dto.level_5_alerts = 0
        ossec_ids_log_dto.level_6_alerts = 0
        ossec_ids_log_dto.level_7_alerts = 0
        ossec_ids_log_dto.level_8_alerts = 0
        ossec_ids_log_dto.level_9_alerts = 0
        ossec_ids_log_dto.level_10_alerts = 0
        ossec_ids_log_dto.level_11_alerts = 0
        ossec_ids_log_dto.level_12_alerts = 0
        ossec_ids_log_dto.level_13_alerts = 0
        ossec_ids_log_dto.level_14_alerts = 0
        ossec_ids_log_dto.level_15_alerts = 0
        ossec_ids_log_dto.invalid_login_alerts = 0
        ossec_ids_log_dto.authentication_success_alerts = 0
        ossec_ids_log_dto.authentication_failed_alerts = 0
        ossec_ids_log_dto.connection_attempt_alerts = 0
        ossec_ids_log_dto.attacks_alerts = 0
        ossec_ids_log_dto.adduser_alerts = 0
        ossec_ids_log_dto.sshd_alerts = 0
        ossec_ids_log_dto.ids_alerts = 0
        ossec_ids_log_dto.firewall_alerts = 0
        ossec_ids_log_dto.squid_alerts = 0
        ossec_ids_log_dto.apache_alerts = 0
        ossec_ids_log_dto.syslog_alerts = 0
        return ossec_ids_log_dto

    @staticmethod
    def ossec_ids_monitor_dto_empty() -> csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO:
        """
        :return: An empty OSSECIdsMonitorDTO
        """
        ossec_ids_monitor_dto = csle_collector.ossec_ids_manager.ossec_ids_manager_pb2.OSSECIdsMonitorDTO()
        ossec_ids_monitor_dto.monitor_running = False
        ossec_ids_monitor_dto.ossec_ids_running = False
        return ossec_ids_monitor_dto
