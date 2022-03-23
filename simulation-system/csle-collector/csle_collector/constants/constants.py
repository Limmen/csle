"""
Constants for csle collector
"""
import re

class DOCKER_STATS:
    CPU_STATS = "cpu_stats"
    CPU_USAGE = "cpu_usage"
    PERCPU_USAGE = "percpu_usage"
    PRECPU_STATS = "precpu_stats"
    TOTAL_USAGE = "total_usage"
    SYSTEM_CPU_USAGE = "system_cpu_usage"
    ONLINE_CPUS = "online_cpus"
    BLKIO_STATS = "blkio_stats"
    IO_SERVICE_BYTES_RECURSIVE = "io_service_bytes_recursive"
    OP = "op"
    READ = "Read"
    VALUE = "value"
    WRITE = "Write"
    NETWORKS = "networks"
    RX_BYTES = "rx_bytes"
    TX_BYTES = "tx_bytes"
    MEMORY_STATS = "memory_stats"
    USAGE = "usage"
    LIMIT = "limit"
    PIDS = "pids"
    TIMESTAMP = "timestamp"
    CPU_PERCENT = "cpu_percent"
    MEM_CURRENT = "mem_current"
    MEM_TOTAL = "mem_total"
    MEM_PERCENT = "mem_percent"
    BLK_READ = "blk_read"
    BLK_WRITE = "blk_write"
    NET_RX = "net_rx"
    NET_TX = "net_tx"
    PIDS_STATS = "pids_stats"
    CURRENT = "current"
    CONTAINER_NAME = "container_name"
    CONTAINER_ID = "container_id"
    CONTAINER_IP = "container_ip"
    UNIX_DOCKER_SOCK_URL = "unix://var/run/docker.sock"

class IDS_ROUTER:
    """
    Constants related to the IDS
    """
    MAX_ALERTS = 1000
    UPDATE_RULESET = "/pulledpork/pulledpork.pl -c /pulledpork/etc/pulledpork.conf -l -P -E -H SIGHUP"
    FAST_LOG_FILE = "/var/snort/fast.log"
    ALERTS_FILE = "/var/snort/alert.csv"
    STATS_FILE = "/var/snort/snort.stats"
    TAIL_ALERTS_COMMAND = "sudo tail -" + str(MAX_ALERTS)
    TAIL_FAST_LOG_COMMAND = "sudo tail -" + str(str(MAX_ALERTS))
    TAIL_ALERTS_LATEST_COMMAND = "sudo tail -1"
    PRIORITY_REGEX = re.compile(r"Priority: \d")
    CLASSIFICATION_REGEX = re.compile(r"(?<=Classification: )(.*?)(?=])")
    SEVERE_ALERT_PRIORITY_THRESHOLD = 3
    ALERT_IDS_ID = {}
    ALERT_IDS_ID["tcp-connection"] = 0
    ALERT_IDS_ID["A TCP connection was detected"] = 0
    ALERT_IDS_ID["unknown"] = 1
    ALERT_IDS_ID["Unknown Traffic"] = 1
    ALERT_IDS_ID["string-detect"] = 2
    ALERT_IDS_ID["A suspicious string was detected"] = 2
    ALERT_IDS_ID["protocol-command-decode"] = 3
    ALERT_IDS_ID["Generic Protocol Command Decode"] = 3
    ALERT_IDS_ID["not-suspicious"] = 4
    ALERT_IDS_ID["Not Suspicious Traffic"] = 4
    ALERT_IDS_ID["network-scan"] = 5
    ALERT_IDS_ID["Detection of a Network Scan"] = 5
    ALERT_IDS_ID["misc-activity"] = 6
    ALERT_IDS_ID["Misc activity"] = 6
    ALERT_IDS_ID["icmp-event"] = 7
    ALERT_IDS_ID["Generic ICMP event"] = 7
    ALERT_IDS_ID["web-application-activity"] = 8
    ALERT_IDS_ID["Access to a potentially vulnerable web application"] = 8
    ALERT_IDS_ID["unusual-client-port-connection"] = 9
    ALERT_IDS_ID["A client was using an unusual port"] = 9
    ALERT_IDS_ID["system-call-detect"] = 10
    ALERT_IDS_ID["A system call was detected"] = 10
    ALERT_IDS_ID["suspicious-login"] = 11
    ALERT_IDS_ID["An attempted login using a suspicious username was detected"] = 11
    ALERT_IDS_ID["suspicious-filename-detect"] = 12
    ALERT_IDS_ID["A suspicious filename was detected"] = 12
    ALERT_IDS_ID["successful-recon-limited"] = 13
    ALERT_IDS_ID["Information Leak"] = 13
    ALERT_IDS_ID["successful-recon-largescale"] = 14
    ALERT_IDS_ID["Large Scale Information Leak"] = 14
    ALERT_IDS_ID["successful-dos"] = 15
    ALERT_IDS_ID["Denial of Service"] = 15
    ALERT_IDS_ID["rpc-portmap-decode"] = 16
    ALERT_IDS_ID["Decode of an RPC Query"] = 16
    ALERT_IDS_ID["non-standard-protocol"] = 17
    ALERT_IDS_ID["Detection of a non-standard protocol or event"] = 17
    ALERT_IDS_ID["misc-attack"] = 18
    ALERT_IDS_ID["Misc Attack"] = 18
    ALERT_IDS_ID["denial-of-service"] = 19
    ALERT_IDS_ID["Detection of a Denial of Service Attack"] = 19
    ALERT_IDS_ID["default-login-attempt"] = 20
    ALERT_IDS_ID["Attempt to login by a default username and password"] = 20
    ALERT_IDS_ID["bad-unknown"] = 21
    ALERT_IDS_ID["Potentially Bad Traffic"] = 21
    ALERT_IDS_ID["attempted-recon"] = 22
    ALERT_IDS_ID["Attempted Information Leak"] = 22
    ALERT_IDS_ID["attempted-dos"] = 23
    ALERT_IDS_ID["Attempted Denial of Service"] = 23
    ALERT_IDS_ID["web-application-attack"] = 24
    ALERT_IDS_ID["Web Application Attack"] = 24
    ALERT_IDS_ID["unsuccessful-user"] = 25
    ALERT_IDS_ID["Unsuccessful User Privilege Gain"] = 25
    ALERT_IDS_ID["trojan-activity"] = 26
    ALERT_IDS_ID["A Network Trojan was detected"] = 26
    ALERT_IDS_ID["successful-user"] = 27
    ALERT_IDS_ID["Successful User Privilege Gain"] = 27
    ALERT_IDS_ID["successful-admin"] = 28
    ALERT_IDS_ID["Successful Administrator Privilege Gain"] = 28
    ALERT_IDS_ID["shellcode-detect"] = 29
    ALERT_IDS_ID["Executable code was detected"] = 29
    ALERT_IDS_ID["policy-violation"] = 30
    ALERT_IDS_ID["Potential Corporate Privacy Violation"] = 30
    ALERT_IDS_ID["inappropriate-content"] = 31
    ALERT_IDS_ID["Inappropriate Content was Detected"] = 31
    ALERT_IDS_ID["attempted-user"] = 32
    ALERT_IDS_ID["Attempted User Privilege Gain"] = 32
    ALERT_IDS_ID["attempted-admin"] = 33
    ALERT_IDS_ID["Attempted Administrator Privilege Gain"] = 33


class HOST_METRICS:
    """
    Constants related to the defender's sensor commands
    """
    LIST_LOGGED_IN_USERS_CMD = "users"
    LIST_OPEN_CONNECTIONS_CMD = "netstat -n"
    LIST_USER_ACCOUNTS = "cat /etc/passwd"
    LIST_FAILED_LOGIN_ATTEMPTS = "sudo tail -50 /var/log/auth.log"
    LIST_SUCCESSFUL_LOGIN_ATTEMPTS = "last"
    LIST_NUMBER_OF_PROCESSES = "ps -e | wc -l"


class LOG_SINK:
    NETWORK_ID_THIRD_OCTET=253
    NETWORK_ID_FOURTH_OCTET=253
    SUFFIX="_1"
    CLIENT_POPULATION_TOPIC_NAME = "client_population"
    IDS_LOG_TOPIC_NAME = "ids_log"
    HOST_METRICS_TOPIC_NAME = "host_metrics"
    DOCKER_STATS_TOPIC_NAME = "docker_stats"
    CLIENT_POPULATION_TOPIC_ATTRIBUTES = ["timestamp", "ip", "num_clients"]
    IDS_LOG_TOPIC_ATTRIBUTES = ["timestamp", "ip", "attempted-admin", "attempted-user",
                                "inappropriate-content", "policy-violation", "shellcode-detect", "successful-admin",
                                "successful-user", "trojan-activity", "unsuccessful-user", "web-application-attack",
                                "attempted-dos", "attempted-recon", "bad-unknown", "default-login-attempt",
                                "denial-of-service", "misc-attack", "non-standard-protocol", "rpc-portmap-decode",
                                "successful-dos", "successful-recon-largescale", "successful-recon-limited",
                                "suspicious-filename-detect", "suspicious-login", "system-call-detect",
                                "unusual-client-port-connection", "web-application-activity", "icmp-event",
                                "misc-activity", "network-scan", "not-suspicious", "protocol-command-decode",
                                "string-detect",
                                "unknown", "tcp-connection", "priority_1", "priority_2", "priority_3", "priority_4"]
    HOST_METRICS_TOPIC_ATTRIBUTES = ["timestamp", "ip", "num_logged_in_users", "num_failed_login_attempts",
                                     "num_open_connections", "num_login_events", "num_processes", "num_users"]
    DOCKER_STATS_TOPIC_ATTRIBUTES = ["timestamp", "ip", "cpu_percent", "mem_current", "mem_total",
                                     "mem_percent", "blk_read", "blk_write", "net_rc", "net_tx"]


class KAFKA_COMMANDS:
    """
    String constants for managing Kafka
    """
    KAFKA_STATUS = "service kafka status"
    KAFKA_STOP = "service kafka stop"
    KAFKA_START = "service kafka start"
