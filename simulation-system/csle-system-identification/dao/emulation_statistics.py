

class EmulationStatistics:

    def __init__(self, max_counts : int = 100000):
        self.intrusion_counts = {}
        self.no_intrusion_counts = {}
        self.labels = [
            "attempted-user_alerts", "inappropriate-content_alerts", "policy-violation_alerts",
            "shellcode-detect_alerts", "successful-admin_alerts",
            "successful-user_alerts", "trojan-activity_alerts", "unsuccessful-user_alerts",
            "web-application-attack_alerts",
            "attempted-dos_alerts", "attempted-recon_alerts", "bad-unknown_alerts",
            "default-login-attempt_alerts",
            "denial-of-service_alerts", "misc-attack_alerts", "non-standard-protocol_alerts",
            "rpc-portmap-decode_alerts",
            "successful-dos_alerts", "successful-recon-largescale_alerts", "successful-recon-limited_alerts",
            "suspicious-filename-detect_alerts", "suspicious-login_alerts", "system-call-detect_alerts",
            "unusual-client-port-connection_alerts", "web-application-activity_alerts", "icmp-event_alerts",
            "misc-activity_alerts", "network-scan_alerts", "not-suspicious_alerts", "protocol-command-decode_alerts",
            "string-detect_alerts", "unknown_alerts", "tcp-connection_alerts", "priority_1_alerts",
            "priority_2_alerts", "priority_3_alerts", "priority_4_alerts", "num_logged_in_users",
            "severe_alerts", "warning_alerts",
            "num_failed_login_attempts", "num_open_connections", "num_login_events", "num_processes", "num_users",
            "cpu_percent", "mem_percent", "cpu_percent", "mem_current", "mem_total",
            "mem_percent", "blk_read", "blk_write", "net_rc", "net_tx", "pids"
        ]


    def initialize_counters(self):
        self.intrusion_counts = {}
        self.no_intrusion_counts = {}
