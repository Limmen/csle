import time
from typing import List
import numpy as np
import csle_collector.constants.constants as constants
from csle_collector.ids_manager.ids_alert import FastLogAlert
import csle_collector.ids_manager.ids_manager_pb2

class AlertCounters:

    def __init__(self):
        self.priority_alerts = list(np.zeros(4))
        self.class_alerts = list(np.zeros(len(constants.IDS_ROUTER.ALERT_IDS_ID)))


    def count(self, alerts: List[FastLogAlert]):
        for a in alerts:
            if a.priority in range(0, len(self.priority_alerts)):
                self.priority_alerts[a.priority] += 1
            if a.class_id in range(0, len(self.class_alerts)):
                self.class_alerts[a.class_id] += 1



    def to_kafka_record(self, ip: str) -> str:
        ts = time.time()
        total_counters = [ts, ip] + self.class_alerts + self.priority_alerts
        record_str = ",".join(list(map(lambda x: str(x), total_counters)))
        return record_str


    def to_dto(self, ip: str):
        ts = time.time()
        csle_collector.ids_manager.ids_manager_pb2.IdsLogDTO(
            timestamp = ts,
            ip = ip,
            attempted_admin_alerts = self.class_alerts[33],
            attempted_user_alerts = self.class_alerts[32],
            inappropriate_content_alerts = self.class_alerts[31],
            policy_violation_alerts = self.class_alerts[30],
            shellcode_detect_alerts = self.class_alerts[29],
            successful_admin_alerts = self.class_alerts[28],
            successful_user_alerts = self.class_alerts[27],
            trojan_activity_alerts = self.class_alerts[26],
            unsuccessful_user_alerts = self.class_alerts[25],
            web_application_attack_alerts = self.class_alerts[24],
            attempted_dos_alerts = self.class_alerts[23],
            attempted_recon_alerts = self.class_alerts[22],
            bad_unknown_alerts = self.class_alerts[21],
            default_login_attempt_alerts = self.class_alerts[20],
            denial_of_service_alerts = self.class_alerts[19],
            misc_attack_alerts = self.class_alerts[18],
            non_standard_protocol_alerts = self.class_alerts[17],
            rpc_portman_decode_alerts = self.class_alerts[16],
            successful_dos_alerts = self.class_alerts[15],
            successful_recon_largescale_alerts = self.class_alerts[14],
            successful_recon_limited_alerts = self.class_alerts[13],
            suspicious_filename_detect_alerts = self.class_alerts[12],
            suspicious_login_alerts = self.class_alerts[11],
            system_call_detect_alerts = self.class_alerts[10],
            unusual_client_port_connection_alerts = self.class_alerts[9],
            web_application_activity_alerts = self.class_alerts[8],
            icmp_event_alerts = self.class_alerts[7],
            misc_activity_alerts = self.class_alerts[6],
            network_scan_alerts = self.class_alerts[5],
            not_suspicious_alerts = self.class_alerts[4],
            protocol_command_decode_alerts = self.class_alerts[3],
            string_detect_alerts = self.class_alerts[2],
            unknown_alerts = self.class_alerts[1],
            tcp_connection_alerts = self.class_alerts[0],
            priority_1_alerts = self.priority_alerts[1],
            priority_2_alerts = self.priority_alerts[2],
            priority_3_alerts = self.priority_alerts[3],
            priority_4_alerts = self.priority_alerts[4]
        )



