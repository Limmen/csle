from typing import List, Dict, Any
import datetime
import subprocess
from csle_collector.snort_ids_manager.snort_ids_alert import SnortIdsAlert, SnortIdsFastLogAlert
from csle_collector.snort_ids_manager.snort_ids_alert_counters import SnortIdsAlertCounters
import csle_collector.snort_ids_manager.snort_ids_manager_pb2
import csle_collector.constants.constants as constants


class SnortIdsManagerUtil:
    """
    Class with utility functions related to the Snort IDS Manager
    """

    @staticmethod
    def check_snort_ids_alerts() -> List[SnortIdsAlert]:
        """
        Reads alerts from the Snort IDS alerts log

        :return: a list of alerts
        """
        cmd = constants.SNORT_IDS_ROUTER.TAIL_ALERTS_COMMAND + " " + constants.SNORT_IDS_ROUTER.SNORT_ALERTS_FILE
        result = subprocess.run(cmd.split(" "), capture_output=True, text=True)
        alerts = []
        year = datetime.datetime.now().year
        for line in result.stdout.split("\n"):
            a_str = line.replace("\n", "")
            alerts.append(SnortIdsAlert.parse_from_str(a_str, year=year))
        return alerts

    @staticmethod
    def check_snort_ids_fast_log() -> List[SnortIdsFastLogAlert]:
        """
        Reads alerts from the Snort IDS fast-log

        :param env_config: the environment config
        :return: a list of alerts
        """
        cmd = constants.SNORT_IDS_ROUTER.TAIL_FAST_LOG_COMMAND + " " + constants.SNORT_IDS_ROUTER.SNORT_FAST_LOG_FILE
        result = subprocess.run(cmd.split(" "), capture_output=True, text=True)
        fast_logs = []
        year = datetime.datetime.now().year
        for line in result.stdout.split("\n"):
            if line is not None and line != "" and line != " ":
                a_str = line.replace("\n", "")
                fast_logs.append(SnortIdsAlert.fast_log_parse(a_str, year=year))
        return fast_logs

    @staticmethod
    def get_latest_snort_alert_ts() -> float:
        """
        Gets the latest timestamp in the snort alerts log

        :param env_config: the environment config
        :return: the latest timestamp
        """
        cmd = constants.SNORT_IDS_ROUTER.TAIL_ALERTS_LATEST_COMMAND + " " + constants.SNORT_IDS_ROUTER.SNORT_ALERTS_FILE
        result = subprocess.run(cmd.split(" "), capture_output=True, text=True)
        year = datetime.datetime.now().year
        alerts = []
        year = datetime.datetime.now().year
        for line in result.stdout.split("\n"):
            if line != "" and line is not None and line != " ":
                a_str = line.replace("\n", "")
                alerts.append(SnortIdsAlert.parse_from_str(a_str, year=year))
        if len(alerts) == 0:
            # retry once
            result = subprocess.run(cmd.split(" "), capture_output=True, text=True)
            alerts = []
            for line in result.stdout.split("\n"):
                if line != "" and line is not None and line != " ":
                    a_str = line.replace("\n", "")
                    alerts.append(SnortIdsAlert.parse_from_str(a_str, year=year))
            if len(alerts) == 0:
                return datetime.datetime.now().timestamp()
            else:
                return alerts[0].timestamp
        else:
            return alerts[0].timestamp

    @staticmethod
    def read_snort_ids_data(episode_last_alert_ts: datetime) -> SnortIdsAlertCounters:
        """
        Measures metrics from the Snort ids

        :param env_config: environment configuration
        :param episode_last_alert_ts: timestamp when the episode started
        :return: ids statistics
        """

        # Read Snort IDS data
        # alerts = IdsManagerUtil.check_ids_alerts()
        fast_logs = SnortIdsManagerUtil.check_snort_ids_fast_log()

        # Filter IDS data from beginning of episode
        # alerts = list(filter(lambda x: x.timestamp > episode_last_alert_ts, alerts))
        fast_logs = list(filter(lambda x: x.timestamp > episode_last_alert_ts, fast_logs))

        counters = SnortIdsAlertCounters()
        counters.count(fast_logs)

        return counters

    @staticmethod
    def snort_ids_monitor_dto_to_dict(
            snort_ids_monitor_dto: csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO) \
            -> Dict[str, Any]:
        """
        Converts a SnortIDSMonitorDTO to a dict

        :param snort_ids_monitor_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["monitor_running"] = snort_ids_monitor_dto.monitor_running
        d["snort_ids_running"] = snort_ids_monitor_dto.snort_ids_running
        return d

    @staticmethod
    def snort_ids_monitor_dto_from_dict(d: Dict[str, Any]) \
            -> csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO:
        """
        Converts a dict representation of a SnortIDSMonitorDTO to a DTO

        :param d: the dict to convert
        :return: the converted DTO
        """
        snort_ids_monitor_dto = csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO()
        snort_ids_monitor_dto.monitor_running = d["monitor_running"]
        snort_ids_monitor_dto.snort_ids_running = d["snort_ids_running"]
        return snort_ids_monitor_dto

    @staticmethod
    def snort_ids_log_dto_to_dict(
            snort_ids_log_dto: csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsLogDTO) \
            -> Dict[str, Any]:
        """
        Converts a SnortIdsLogDTO to a dict

        :param snort_ids_log_dto: the DTO to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["timestamp"] = snort_ids_log_dto.timestamp
        d["ip"] = snort_ids_log_dto.ip
        d["attempted_admin_alerts"] = snort_ids_log_dto.attempted_admin_alerts
        d["attempted_user_alerts"] = snort_ids_log_dto.attempted_user_alerts
        d["inappropriate_content_alerts"] = snort_ids_log_dto.inappropriate_content_alerts
        d["policy_violation_alerts"] = snort_ids_log_dto.policy_violation_alerts
        d["shellcode_detect_alerts"] = snort_ids_log_dto.shellcode_detect_alerts
        d["successful_admin_alerts"] = snort_ids_log_dto.successful_admin_alerts
        d["successful_user_alerts"] = snort_ids_log_dto.successful_user_alerts
        d["trojan_activity_alerts"] = snort_ids_log_dto.trojan_activity_alerts
        d["unsuccessful_user_alerts"] = snort_ids_log_dto.unsuccessful_user_alerts
        d["web_application_attack_alerts"] = snort_ids_log_dto.web_application_attack_alerts
        d["attempted_dos_alerts"] = snort_ids_log_dto.attempted_dos_alerts
        d["attempted_recon_alerts"] = snort_ids_log_dto.attempted_recon_alerts
        d["bad_unknown_alerts"] = snort_ids_log_dto.bad_unknown_alerts
        d["default_login_attempt_alerts"] = snort_ids_log_dto.default_login_attempt_alerts
        d["denial_of_service_alerts"] = snort_ids_log_dto.denial_of_service_alerts
        d["misc_attack_alerts"] = snort_ids_log_dto.misc_attack_alerts
        d["non_standard_protocol_alerts"] = snort_ids_log_dto.non_standard_protocol_alerts
        d["rpc_portman_decode_alerts"] = snort_ids_log_dto.rpc_portman_decode_alerts
        d["successful_dos_alerts"] = snort_ids_log_dto.successful_dos_alerts
        d["successful_recon_largescale_alerts"] = snort_ids_log_dto.successful_recon_largescale_alerts
        d["successful_recon_limited_alerts"] = snort_ids_log_dto.successful_recon_limited_alerts
        d["suspicious_filename_detect_alerts"] = snort_ids_log_dto.suspicious_filename_detect_alerts
        d["suspicious_login_alerts"] = snort_ids_log_dto.suspicious_login_alerts
        d["system_call_detect_alerts"] = snort_ids_log_dto.system_call_detect_alerts
        d["unusual_client_port_connection_alerts"] = snort_ids_log_dto.unusual_client_port_connection_alerts
        d["web_application_activity_alerts"] = snort_ids_log_dto.web_application_activity_alerts
        d["icmp_event_alerts"] = snort_ids_log_dto.icmp_event_alerts
        d["misc_activity_alerts"] = snort_ids_log_dto.misc_activity_alerts
        d["network_scan_alerts"] = snort_ids_log_dto.network_scan_alerts
        d["not_suspicious_alerts"] = snort_ids_log_dto.not_suspicious_alerts
        d["protocol_command_decode_alerts"] = snort_ids_log_dto.protocol_command_decode_alerts
        d["unknown_alerts"] = snort_ids_log_dto.unknown_alerts
        d["tcp_connection_alerts"] = snort_ids_log_dto.tcp_connection_alerts
        d["priority_1_alerts"] = snort_ids_log_dto.priority_1_alerts
        d["priority_2_alerts"] = snort_ids_log_dto.priority_2_alerts
        d["priority_3_alerts"] = snort_ids_log_dto.priority_3_alerts
        d["priority_4_alerts"] = snort_ids_log_dto.priority_4_alerts
        d["total_alerts"] = snort_ids_log_dto.total_alerts
        d["warning_alerts"] = snort_ids_log_dto.warning_alerts
        d["severe_alerts"] = snort_ids_log_dto.severe_alerts
        d["alerts_weighted_by_priority"] = snort_ids_log_dto.alerts_weighted_by_priority
        return d

    @staticmethod
    def snort_ids_log_dto_from_dict(d: Dict[str, Any]) \
            -> csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsLogDTO:
        """
        Converts a dict representation of a SnortIdsLogDTO to a DTO

        :param d: the dict to convert
        :return: the converted DTO
        """
        snort_ids_log_dto = csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsLogDTO()
        snort_ids_log_dto.timestamp = d["timestamp"]
        snort_ids_log_dto.ip = d["ip"]
        snort_ids_log_dto.attempted_admin_alerts = d["attempted_admin_alerts"]
        snort_ids_log_dto.attempted_user_alerts = d["attempted_user_alerts"]
        snort_ids_log_dto.inappropriate_content_alerts = d["inappropriate_content_alerts"]
        snort_ids_log_dto.policy_violation_alerts = d["policy_violation_alerts"]
        snort_ids_log_dto.shellcode_detect_alerts = d["shellcode_detect_alerts"]
        snort_ids_log_dto.successful_admin_alerts = d["successful_admin_alerts"]
        snort_ids_log_dto.successful_user_alerts = d["successful_user_alerts"]
        snort_ids_log_dto.trojan_activity_alerts = d["trojan_activity_alerts"]
        snort_ids_log_dto.unsuccessful_user_alerts = d["unsuccessful_user_alerts"]
        snort_ids_log_dto.web_application_attack_alerts = d["web_application_attack_alerts"]
        snort_ids_log_dto.attempted_dos_alerts = d["attempted_dos_alerts"]
        snort_ids_log_dto.attempted_recon_alerts = d["attempted_recon_alerts"]
        snort_ids_log_dto.bad_unknown_alerts = d["bad_unknown_alerts"]
        snort_ids_log_dto.default_login_attempt_alerts = d["default_login_attempt_alerts"]
        snort_ids_log_dto.denial_of_service_alerts = d["denial_of_service_alerts"]
        snort_ids_log_dto.misc_attack_alerts = d["misc_attack_alerts"]
        snort_ids_log_dto.non_standard_protocol_alerts = d["non_standard_protocol_alerts"]
        snort_ids_log_dto.rpc_portman_decode_alerts = d["rpc_portman_decode_alerts"]
        snort_ids_log_dto.successful_dos_alerts = d["successful_dos_alerts"]
        snort_ids_log_dto.successful_recon_largescale_alerts = d["successful_recon_largescale_alerts"]
        snort_ids_log_dto.successful_recon_limited_alerts = d["successful_recon_limited_alerts"]
        snort_ids_log_dto.suspicious_filename_detect_alerts = d["suspicious_filename_detect_alerts"]
        snort_ids_log_dto.suspicious_login_alerts = d["suspicious_login_alerts"]
        snort_ids_log_dto.system_call_detect_alerts = d["system_call_detect_alerts"]
        snort_ids_log_dto.unusual_client_port_connection_alerts = d["unusual_client_port_connection_alerts"]
        snort_ids_log_dto.web_application_activity_alerts = d["web_application_activity_alerts"]
        snort_ids_log_dto.icmp_event_alerts = d["icmp_event_alerts"]
        snort_ids_log_dto.misc_activity_alerts = d["misc_activity_alerts"]
        snort_ids_log_dto.network_scan_alerts = d["network_scan_alerts"]
        snort_ids_log_dto.not_suspicious_alerts = d["not_suspicious_alerts"]
        snort_ids_log_dto.protocol_command_decode_alerts = d["protocol_command_decode_alerts"]
        snort_ids_log_dto.unknown_alerts = d["unknown_alerts"]
        snort_ids_log_dto.tcp_connection_alerts = d["tcp_connection_alerts"]
        snort_ids_log_dto.priority_1_alerts = d["priority_1_alerts"]
        snort_ids_log_dto.priority_2_alerts = d["priority_2_alerts"]
        snort_ids_log_dto.priority_3_alerts = d["priority_3_alerts"]
        snort_ids_log_dto.priority_4_alerts = d["priority_4_alerts"]
        snort_ids_log_dto.total_alerts = d["total_alerts"]
        snort_ids_log_dto.warning_alerts = d["warning_alerts"]
        snort_ids_log_dto.severe_alerts = d["severe_alerts"]
        snort_ids_log_dto.alerts_weighted_by_priority = d["alerts_weighted_by_priority"]
        return snort_ids_log_dto

    @staticmethod
    def snort_ids_log_dto_empty() \
            -> csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsLogDTO:
        """
        :return: an empty SnortIdsLogDTO
        """
        snort_ids_log_dto = csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsLogDTO()
        snort_ids_log_dto.timestamp = 0.0
        snort_ids_log_dto.ip = ""
        snort_ids_log_dto.attempted_admin_alerts = 0
        snort_ids_log_dto.attempted_user_alerts = 0
        snort_ids_log_dto.inappropriate_content_alerts = 0
        snort_ids_log_dto.policy_violation_alerts = 0
        snort_ids_log_dto.shellcode_detect_alerts = 0
        snort_ids_log_dto.successful_admin_alerts = 0
        snort_ids_log_dto.successful_user_alerts = 0
        snort_ids_log_dto.trojan_activity_alerts = 0
        snort_ids_log_dto.unsuccessful_user_alerts = 0
        snort_ids_log_dto.web_application_attack_alerts = 0
        snort_ids_log_dto.attempted_dos_alerts = 0
        snort_ids_log_dto.attempted_recon_alerts = 0
        snort_ids_log_dto.bad_unknown_alerts = 0
        snort_ids_log_dto.default_login_attempt_alerts = 0
        snort_ids_log_dto.denial_of_service_alerts = 0
        snort_ids_log_dto.misc_attack_alerts = 0
        snort_ids_log_dto.non_standard_protocol_alerts = 0
        snort_ids_log_dto.rpc_portman_decode_alerts = 0
        snort_ids_log_dto.successful_dos_alerts = 0
        snort_ids_log_dto.successful_recon_largescale_alerts = 0
        snort_ids_log_dto.successful_recon_limited_alerts = 0
        snort_ids_log_dto.suspicious_filename_detect_alerts = 0
        snort_ids_log_dto.suspicious_login_alerts = 0
        snort_ids_log_dto.system_call_detect_alerts = 0
        snort_ids_log_dto.unusual_client_port_connection_alerts = 0
        snort_ids_log_dto.web_application_activity_alerts = 0
        snort_ids_log_dto.icmp_event_alerts = 0
        snort_ids_log_dto.misc_activity_alerts = 0
        snort_ids_log_dto.network_scan_alerts = 0
        snort_ids_log_dto.not_suspicious_alerts = 0
        snort_ids_log_dto.protocol_command_decode_alerts = 0
        snort_ids_log_dto.unknown_alerts = 0
        snort_ids_log_dto.tcp_connection_alerts = 0
        snort_ids_log_dto.priority_1_alerts = 0
        snort_ids_log_dto.priority_2_alerts = 0
        snort_ids_log_dto.priority_3_alerts = 0
        snort_ids_log_dto.priority_4_alerts = 0
        snort_ids_log_dto.total_alerts = 0
        snort_ids_log_dto.warning_alerts = 0
        snort_ids_log_dto.severe_alerts = 0
        snort_ids_log_dto.alerts_weighted_by_priority = 0
        return snort_ids_log_dto

    @staticmethod
    def snort_ids_monitor_dto_empty() -> csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO:
        """
        :return: An empty SnortIdsMonitorDTO
        """
        snort_ids_monitor_dto = csle_collector.snort_ids_manager.snort_ids_manager_pb2.SnortIdsMonitorDTO()
        snort_ids_monitor_dto.monitor_running = False
        snort_ids_monitor_dto.snort_ids_running = False
        return snort_ids_monitor_dto
