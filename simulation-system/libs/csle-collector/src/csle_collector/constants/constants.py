"""
Constants for csle collector
"""
import re

LATEST_VERSION = "latest"
INSTALL = "sudo /root/miniconda3/bin/pip install -U --no-cache-dir csle-collector "


class BEATS:
    """
    Constants related to beats
    """
    RELOAD_ENABLED_PROPERTY = "reload.enabled"
    SETUP_TEMPLATE_SETTINGS_PROPERTY = "setup.template.settings"
    INDEX_NUM_SHARDS_PROPERTY = "index.number_of_shards"
    SETUP_KIBANA_PROPERTY = "setup.kibana"
    HOST_PROPERTY = "host"
    HOSTS_PROPERTY = "hosts"
    ELASTIC_OUTPUT_PROPERTY = "output.elasticsearch"
    PROCESSORS_PROPERTY = "processors"
    ADD_HOST_METADATA_PROPERTY = "add_host_metadata"
    WHEN_NOT_CONTAIN_TAGS_PROPERTY = "when.not.contains.tags"
    FORWARDED_PROPERTY = "forwarded"
    MODULE_PROPERTY = "module"
    LOG_PROPERTY = "log"
    SYSLOG_PROPERTY = "syslog"
    AUTH_PROPERTY = "auth"
    SLOWLOG_PROPERTY = "slowlog"
    AUDIT_PROPERTY = "audit"
    SERVER_PROPERTY = "server"
    VAR_INPUT_PROPERTY = "var.input"
    VAR_PATHS_PROPERTY = "var.paths"
    FILE_PROPERTY = "file"
    TYPE_PROPERTY = "type"
    FILESTREAM_PROPERTY = "filestream"
    KAFKA_PROPERTY = "kafka"
    TOPICS_PROPERTY = "topics"
    GROUP_ID_PROPERTY = "group_id"
    ID_PROPERTY = "id"
    NAME_PROPERTY = "name"
    ENABLED_PROPERTY = "enabled"
    PATHS_PROPERTY = "paths"
    PATH_PROPERTY = "path"
    PERIOD_PROPERTY = "period"
    METRICSETS_PROPERTY = "metricsets"


class FILEBEAT:
    """
    Constants related to Filebeat
    """
    FILEBEAT_GROUP_ID = "filebeat"
    CONFIG_DIR = "/etc/filebeat/"
    CONFIG_FILE = "/etc/filebeat/filebeat.yml"
    SETUP_CMD = "filebeat setup -e"
    SNORT_MODULE = "snort"
    ELASTICSEARCH_MODULE = "elasticsearch"
    KIBANA_MODULE = "kibana"
    SYSTEM_MODULE = "system"
    KAFKA_MODULE = "kafka"
    LOGSTASH_MODULE = "logstash"
    ENABLE_MODULE_CMD = "filebeat modules enable {}"
    MODULES_CONFIG_DIR = "/etc/filebeat/modules.d/"
    SNORT_MODULE_CONFIG_FILE = "snort.yml"
    LOGSTASH_MODULE_CONFIG_FILE = "logstash.yml"
    KIBANA_MODULE_CONFIG_FILE = "kibana.yml"
    SYSTEM_MODULE_CONFIG_FILE = "system.yml"
    KAFKA_MODULE_CONFIG_FILE = "kafka.yml"
    ELASTICSEARCH_MODULE_CONFIG_FILE = "elasticsearch.yml"
    INPUTS_PROPERTY = "filebeat.inputs"
    MODULES_PROPERTY = "filebeat.config.modules"
    FILEBEAT_STATUS = "sudo service filebeat status"
    FILEBEAT_START = "sudo service filebeat start"
    FILEBEAT_STOP = "sudo service filebeat stop"


class PACKETBEAT:
    """
    Constants related to Packetbeat
    """
    FILEBEAT_GROUP_ID = "packetbeat"
    CONFIG_DIR = "/etc/packetbeat/"
    CONFIG_FILE = "/etc/packetbeat/packetbeat.yml"
    SETUP_CMD = "packetbeat setup -e"
    PACKETBEAT_STATUS = "sudo service packetbeat status"
    PACKETBEAT_START = "sudo service packetbeat start"
    PACKETBEAT_STOP = "sudo service packetbeat stop"
    INTERFACES_TYPE_PROPERTY = "packetbeat.interfaces.type"
    AF_PACKET_PROPERTY = "af_packet"
    ANY_DEVICE_PROPERTY = "any"
    INTERFACES_DEVICE_PROPERTY = "packetbeat.interfaces.device"
    FLOWS = "packetbeat.flows"
    TIMEOUT_PROPERTY = "timeout"
    PROTOCOLS = "packetbeat.protocols"
    ICMP_PROTOCOL = "icmp"
    AMQP_PROTOCOL = "amqp"
    PORTS_PROPERTY = "ports"
    AMQP_PORTS = [5672]
    CASSANDRA_PROTOCOL = "cassandra"
    CASSANDRA_PORTS = [9042]
    DHCPV4_PROTOCOL = "dhcpv4"
    DHCPV4_PORTS = [67, 68]
    DNS_PROTOCOL = "dns"
    DNS_PORTS = [53]
    HTTP_PROTOCOL = "http"
    HTTP_PORTS = [80, 8080, 8000, 5000, 8002]
    MEMCACHE_PROTOCOL = "memcache"
    MEMCACHE_PORTS = [11211]
    MYSQL_PROTOCOL = "mysql"
    MYSQL_PORTS = [3306, 3307]
    PGSQL_PROTOCOL = "pgsql"
    PGSQL_PORTS = [5432]
    REDIS_PROTOCOL = "redis"
    REDIS_PORTS = [6379]
    THRIFT_PROTOCOL = "thrift"
    THRIFT_PORTS = [9090]
    MONGODB_PROTOCOL = "mongodb"
    MONGODB_PORTS = [27017]
    NFS_PROTOCOL = "nfs"
    NFS_PORTS = [2049]
    TLS_PROTOCOL = "tls"
    TLS_PORTS = [443, 993, 995, 5223, 8443, 8883, 9243]
    SIP_PROTOCOL = "sip"
    SIP_PORTS = [9243]


class METRICBEAT:
    """
    Constants related to Metricbeat
    """
    CONFIG_DIR = "/etc/metricbeat/"
    CONFIG_FILE = "/etc/metricbeat/metricbeat.yml"
    SETUP_CMD = "metricbeat setup -e"
    ELASTICSEARCH_MODULE = "elasticsearch"
    KIBANA_MODULE = "kibana"
    SYSTEM_MODULE = "system"
    LINUX_MODULE = "linux"
    KAFKA_MODULE = "kafka"
    LOGSTASH_MODULE = "logstash"
    ENABLE_MODULE_CMD = "metricbeat modules enable {}"
    MODULES_CONFIG_DIR = "/etc/metricbeat/modules.d/"
    SNORT_MODULE_CONFIG_FILE = "snort.yml"
    LOGSTASH_MODULE_CONFIG_FILE = "logstash.yml"
    KIBANA_MODULE_CONFIG_FILE = "kibana.yml"
    SYSTEM_MODULE_CONFIG_FILE = "system.yml"
    LINUX_MODULE_CONFIG_FILE = "linux.yml"
    KAFKA_MODULE_CONFIG_FILE = "kafka.yml"
    ELASTICSEARCH_MODULE_CONFIG_FILE = "elasticsearch.yml"
    MODULES_PROPERTY = "metricbeat.config.modules"
    METRICBEAT_STATUS = "sudo service metricbeat status"
    METRICBEAT_START = "sudo service metricbeat start"
    METRICBEAT_STOP = "sudo service metricbeat stop"
    PROCESSES_PROPERTY = "processes"
    CPU_METRICS_PROPERTY = "cpu.metrics"
    CORE_METRICS_PROPERTY = "core.metrics"
    PERCENTAGES_PROPERTY = "percentages"
    NORMALIZED_PERCENTAGES_PROPERTY = "normalized_percentages"
    CPU_METRIC = "cpu"
    LOAD_METRIC = "load"
    MEMORY_METRIC = "memory"
    NETWORK_METRIC = "network"
    PROCESS_METRIC = "process"
    PROCESS_SUMMARY_METRIC = "process_summary"
    SOCKET_SUMMARY_METRIC = "socket_summary"
    PAGEINFO_METRIC = "pageinfo"
    SUMMARY_METRIC = "memory"


class HEARTBEAT:
    """
    Constants related to heartbeat
    """
    CONFIG_DIR = "/etc/heartbeat/"
    CONFIG_FILE = "/etc/heartbeat/heartbeat.yml"
    SETUP_CMD = "heartbeat setup -e"
    HEARTBEAT_STATUS = "sudo service heartbeat-elastic status"
    HEARTBEAT_START = "sudo service heartbeat-elastic start"
    HEARTBEAT_STOP = "sudo service heartbeat-elastic stop"
    SCHEDULE_PROPERTY = "schedule"
    ICMP_MONITOR_TYPE = "icmp"
    HEARTBEAT_MONITORS_PROPERTY = "heartbeat.monitors"
    CSLE_MONITOR_SERVICE_NAME = "csle-topology-connection-service"
    CSLE_MONITOR_SERVICE_ID = "csle-topology-connection-service-id"


class GRPC:
    """
    Constants related to GRPC
    """
    TIMEOUT_SECONDS = 30
    CONFIG_TIMEOUT_SECONDS = 300


class SYSTEM:
    """
    Constants related to system
    """
    AUTH_LOG = "/var/log/auth.log"
    SYSLOG = "/var/log/syslog"


class LOG_FILES:
    """
    Constants related to the log files
    """
    KAFKA_MANAGER_LOG_FILE = "kafka_manager.log"
    KAFKA_MANAGER_LOG_DIR = "/"
    OSSEC_IDS_MANAGER_LOG_FILE = "ossec_ids_manager.log"
    OSSEC_IDS_MANAGER_LOG_DIR = "/"
    SNORT_IDS_MANAGER_LOG_FILE = "snort_ids_manager.log"
    SNORT_IDS_MANAGER_LOG_DIR = "/"
    ELK_MANAGER_LOG_FILE = "elk_manager.log"
    ELK_MANAGER_LOG_DIR = "/"
    DOCKER_STATS_MANAGER_LOG_FILE = "docker_stats_manager.log"
    DOCKER_STATS_MANAGER_LOG_DIR = "/var/log/csle/"
    HOST_MANAGER_LOG_FILE = "host_manager.log"
    HOST_MANAGER_LOG_DIR = "/"
    CLIENT_MANAGER_LOG_FILE = "client_manager.log"
    CLIENT_MANAGER_LOG_DIR = "/"
    TRAFFIC_MANAGER_LOG_FILE = "traffic_manager.log"
    TRAFFIC_MANAGER_LOG_DIR = "/"
    KAFKA_LOG_FILE = "/usr/local/kafka/logs/server.log"


class TRAFFIC_GENERATOR:
    """
    Constants related to the traffic generator
    """
    START_TRAFFIC_GENERATOR_CMD = "sudo nohup /traffic_generator.sh &"
    CHECK_IF_TRAFFIC_GENERATOR_IS_RUNNING = "ps -aux | grep traffic_generator"
    TRAFFIC_GENERATOR_FILE_NAME = "traffic_generator.sh"
    CREATE_TRAFFIC_GENERATOR_FILE = "sudo touch /traffic_generator.sh"
    MAKE_TRAFFIC_GENERATOR_FILE_EXECUTABLE = "sudo chmod 777 /traffic_generator.sh"
    REMOVE_OLD_TRAFFIC_GENERATOR_FILE = "sudo rm -f /traffic_generator.sh"


class DOCKER_STATS:
    """
    Constants related to Docker stats
    """
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


class OSSEC:
    """
    Constants related to the OSSEC HIDS
    """
    MAX_ALERTS = 10000
    OSSEC_ALERTS_FILE = "/var/ossec/alerts/alerts.log"
    OSSEC_LOG_FILE = "/var/ossec/logs/ossec.log"
    TAIL_ALERTS_COMMAND = "sudo tail -" + str(MAX_ALERTS)
    ALERTLINE_REGEX = re.compile(r"\*\* Alert (\d+.\d+)*: - (\w+.+)")
    HOSTLINE_REGEX = re.compile(r"\d+ \w+ \d+ \d+:\d+:\d+ \((\w+.+)\) (\d+.\d+.\d+.\d+)")
    SERVHOSTLINE_REGEX = re.compile(r"\d+ \w+ \d+ \d+:\d+:\d+ (\w+)")
    RULELINE_REGEX = re.compile(r"Rule: (\d+)* \(level (\d+)\) -> '(\w+.+)'")
    SRCIPLINE_REGEX = re.compile(r"Src IP: (\d+.\d+.\d+.\d+)")
    USERLINE_REGEX = re.compile(r"User: (\w+)")
    DATELINEREGEX = re.compile(r"\d+ \w+ \d+ \d+:\d+:\d+")
    OSSEC_ALERT_RULE_ID_TO_DESCR = {}
    OSSEC_ALERT_RULE_ID_TO_DESCR[0] = "Ignored - No action taken. Used to avoid false positives. " \
                                      "These rules are scanned before all the others. " \
                                      "They include events with no security relevance."
    OSSEC_ALERT_RULE_ID_TO_DESCR[1] = "None"
    OSSEC_ALERT_RULE_ID_TO_DESCR[2] = "System low priority notification - System notification or status messages. " \
                                      "They have no security relevance."
    OSSEC_ALERT_RULE_ID_TO_DESCR[3] = "Successful/Authorized events - They include successful login attempts, " \
                                      "firewall allow events, etc."
    OSSEC_ALERT_RULE_ID_TO_DESCR[4] = "System low priority error - Errors related to bad configurations or " \
                                      "unused devices/applications. They have no security relevance and are usually " \
                                      "caused by default installations or software testing."
    OSSEC_ALERT_RULE_ID_TO_DESCR[5] = "User generated error - They include missed passwords, denied actions, etc. " \
                                      "By itself they have no security relevance."
    OSSEC_ALERT_RULE_ID_TO_DESCR[6] = "Low relevance attack - They indicate a worm or a virus that have no affect to " \
                                      "the system (like code red for apache servers, etc). " \
                                      "They also include frequently IDS events and frequently errors."
    OSSEC_ALERT_RULE_ID_TO_DESCR[7] = "'Bad word' matching. They include words like 'bad', " \
                                      "'error', etc. These events " \
                                      "are most of the time unclassified and may have some security relevance."
    OSSEC_ALERT_RULE_ID_TO_DESCR[8] = "First time seen - Include first time seen events. First time an IDS event is " \
                                      "fired or the first time an user logged in. If you just started using OSSEC " \
                                      "HIDS these messages will probably be frequently. After a while they should " \
                                      "go away, It also includes security relevant actions " \
                                      "(like the starting of a sniffer or something like that)."
    OSSEC_ALERT_RULE_ID_TO_DESCR[9] = "Error from invalid source - Include attempts to login as an unknown user or " \
                                      "from an invalid source. May have security relevance (specially if repeated). " \
                                      "They also include errors regarding the “admin” (root) account."
    OSSEC_ALERT_RULE_ID_TO_DESCR[10] = "Multiple user generated errors - They include multiple bad passwords, " \
                                       "multiple failed logins, etc. " \
                                       "They may indicate an attack or may just be that a user " \
                                       "just forgot his credentials."
    OSSEC_ALERT_RULE_ID_TO_DESCR[11] = "Integrity checking warning - They include messages regarding the " \
                                       "modification of binaries or the presence of rootkits (by rootcheck). " \
                                       "If you just modified your system configuration you should be fine " \
                                       "regarding the “syscheck” messages. " \
                                       "They may indicate a successful attack. Also included IDS events that " \
                                       "will be ignored (high number of repetitions)."
    OSSEC_ALERT_RULE_ID_TO_DESCR[12] = "High importancy event - They include error or warning messages from the " \
                                       "system, kernel, etc. They may indicate an attack against a " \
                                       "specific application."
    OSSEC_ALERT_RULE_ID_TO_DESCR[13] = "Unusual error (high importance) - Most of the times it matches a " \
                                       "common attack pattern."
    OSSEC_ALERT_RULE_ID_TO_DESCR[14] = "High importance security event. Most of the times done with correlation and " \
                                       "it indicates an attack."
    OSSEC_ALERT_RULE_ID_TO_DESCR[15] = "Severe attack - No chances of false positives. Immediate attention " \
                                       "is necessary."
    OSSEC_IDS_ALERT_GROUP_ID = {}
    OSSEC_IDS_ALERT_GROUP_ID["invalid_login"] = 0
    OSSEC_IDS_ALERT_GROUP_ID["authentication_success"] = 1
    OSSEC_IDS_ALERT_GROUP_ID["authentication_failed"] = 2
    OSSEC_IDS_ALERT_GROUP_ID["connection_attempt"] = 3
    OSSEC_IDS_ALERT_GROUP_ID["attacks"] = 4
    OSSEC_IDS_ALERT_GROUP_ID["adduser"] = 5
    OSSEC_IDS_ALERT_GROUP_ID["sshd"] = 6
    OSSEC_IDS_ALERT_GROUP_ID["ids"] = 7
    OSSEC_IDS_ALERT_GROUP_ID["firewall"] = 8
    OSSEC_IDS_ALERT_GROUP_ID["squid"] = 9
    OSSEC_IDS_ALERT_GROUP_ID["apache"] = 10
    OSSEC_IDS_ALERT_GROUP_ID["syslog"] = 11
    OSSEC_SEVERE_ALERT_LEVEL_THRESHOLD = 10
    STOP_OSSEC_IDS = "/var/ossec/bin/ossec-control stop"
    START_OSSEC_IDS = "/var/ossec/bin/ossec-control start"
    CHECK_IF_OSSEC_IS_RUNNING_CMD = "ps -aux | grep ossec"
    OSSEC_RUNNING_SEARCH = "/var/ossec/bin/ossec-execd"


class SNORT_IDS_ROUTER:
    """
    Constants related to the Snort IDS
    """
    MAX_ALERTS = 10000
    UPDATE_RULESET = "/pulledpork/pulledpork.pl -c /pulledpork/etc/pulledpork.conf -l -P -E -H SIGHUP"
    SNORT_FAST_LOG_FILE = "/var/snort/fast.log"
    SNORT_ALERTS_FILE = "/var/snort/alert.csv"
    SNORT_STATS_FILE = "/var/snort/snort.stats"
    TAIL_ALERTS_COMMAND = "sudo tail -" + str(MAX_ALERTS)
    TAIL_FAST_LOG_COMMAND = "sudo tail -" + str(str(MAX_ALERTS))
    TAIL_ALERTS_LATEST_COMMAND = "sudo tail -1"
    PRIORITY_REGEX = re.compile(r"Priority: \d")
    CLASSIFICATION_REGEX = re.compile(r"(?<=Classification: )(.*?)(?=])")
    SNORT_SEVERE_ALERT_PRIORITY_THRESHOLD = 2
    SNORT_ALERT_IDS_ID = {}
    SNORT_ALERT_IDS_ID["tcp-connection"] = 0
    SNORT_ALERT_IDS_ID["A TCP connection was detected"] = 0
    SNORT_ALERT_IDS_ID["unknown"] = 1
    SNORT_ALERT_IDS_ID["Unknown Traffic"] = 1
    SNORT_ALERT_IDS_ID["string-detect"] = 2
    SNORT_ALERT_IDS_ID["A suspicious string was detected"] = 2
    SNORT_ALERT_IDS_ID["protocol-command-decode"] = 3
    SNORT_ALERT_IDS_ID["Generic Protocol Command Decode"] = 3
    SNORT_ALERT_IDS_ID["not-suspicious"] = 4
    SNORT_ALERT_IDS_ID["Not Suspicious Traffic"] = 4
    SNORT_ALERT_IDS_ID["network-scan"] = 5
    SNORT_ALERT_IDS_ID["Detection of a Network Scan"] = 5
    SNORT_ALERT_IDS_ID["misc-activity"] = 6
    SNORT_ALERT_IDS_ID["Misc activity"] = 6
    SNORT_ALERT_IDS_ID["icmp-event"] = 7
    SNORT_ALERT_IDS_ID["Generic ICMP event"] = 7
    SNORT_ALERT_IDS_ID["web-application-activity"] = 8
    SNORT_ALERT_IDS_ID["Access to a potentially vulnerable web application"] = 8
    SNORT_ALERT_IDS_ID["unusual-client-port-connection"] = 9
    SNORT_ALERT_IDS_ID["A client was using an unusual port"] = 9
    SNORT_ALERT_IDS_ID["system-call-detect"] = 10
    SNORT_ALERT_IDS_ID["A system call was detected"] = 10
    SNORT_ALERT_IDS_ID["suspicious-login"] = 11
    SNORT_ALERT_IDS_ID["An attempted login using a suspicious username was detected"] = 11
    SNORT_ALERT_IDS_ID["suspicious-filename-detect"] = 12
    SNORT_ALERT_IDS_ID["A suspicious filename was detected"] = 12
    SNORT_ALERT_IDS_ID["successful-recon-limited"] = 13
    SNORT_ALERT_IDS_ID["Information Leak"] = 13
    SNORT_ALERT_IDS_ID["successful-recon-largescale"] = 14
    SNORT_ALERT_IDS_ID["Large Scale Information Leak"] = 14
    SNORT_ALERT_IDS_ID["successful-dos"] = 15
    SNORT_ALERT_IDS_ID["Denial of Service"] = 15
    SNORT_ALERT_IDS_ID["rpc-portmap-decode"] = 16
    SNORT_ALERT_IDS_ID["Decode of an RPC Query"] = 16
    SNORT_ALERT_IDS_ID["non-standard-protocol"] = 17
    SNORT_ALERT_IDS_ID["Detection of a non-standard protocol or event"] = 17
    SNORT_ALERT_IDS_ID["misc-attack"] = 18
    SNORT_ALERT_IDS_ID["Misc Attack"] = 18
    SNORT_ALERT_IDS_ID["denial-of-service"] = 19
    SNORT_ALERT_IDS_ID["Detection of a Denial of Service Attack"] = 19
    SNORT_ALERT_IDS_ID["default-login-attempt"] = 20
    SNORT_ALERT_IDS_ID["Attempt to login by a default username and password"] = 20
    SNORT_ALERT_IDS_ID["bad-unknown"] = 21
    SNORT_ALERT_IDS_ID["Potentially Bad Traffic"] = 21
    SNORT_ALERT_IDS_ID["attempted-recon"] = 22
    SNORT_ALERT_IDS_ID["Attempted Information Leak"] = 22
    SNORT_ALERT_IDS_ID["attempted-dos"] = 23
    SNORT_ALERT_IDS_ID["Attempted Denial of Service"] = 23
    SNORT_ALERT_IDS_ID["web-application-attack"] = 24
    SNORT_ALERT_IDS_ID["Web Application Attack"] = 24
    SNORT_ALERT_IDS_ID["unsuccessful-user"] = 25
    SNORT_ALERT_IDS_ID["Unsuccessful User Privilege Gain"] = 25
    SNORT_ALERT_IDS_ID["trojan-activity"] = 26
    SNORT_ALERT_IDS_ID["A Network Trojan was detected"] = 26
    SNORT_ALERT_IDS_ID["successful-user"] = 27
    SNORT_ALERT_IDS_ID["Successful User Privilege Gain"] = 27
    SNORT_ALERT_IDS_ID["successful-admin"] = 28
    SNORT_ALERT_IDS_ID["Successful Administrator Privilege Gain"] = 28
    SNORT_ALERT_IDS_ID["shellcode-detect"] = 29
    SNORT_ALERT_IDS_ID["Executable code was detected"] = 29
    SNORT_ALERT_IDS_ID["policy-violation"] = 30
    SNORT_ALERT_IDS_ID["Potential Corporate Privacy Violation"] = 30
    SNORT_ALERT_IDS_ID["inappropriate-content"] = 31
    SNORT_ALERT_IDS_ID["Inappropriate Content was Detected"] = 31
    SNORT_ALERT_IDS_ID["attempted-user"] = 32
    SNORT_ALERT_IDS_ID["Attempted User Privilege Gain"] = 32
    SNORT_ALERT_IDS_ID["attempted-admin"] = 33
    SNORT_ALERT_IDS_ID["Attempted Administrator Privilege Gain"] = 33
    STOP_SNORT_IDS = "kill -9 $(pgrep snort)"
    START_SNORT_IDS = "sudo snort -D -q -u snort -g snort -c /etc/snort/snort.conf -i eth1:eth0 -l " \
                      "/var/snort/ -h 55.0.0.0/8 -Q -I --create-pidfile"
    CHECK_IF_SNORT_IS_RUNNING_CMD = "ps -aux | grep snort.conf"
    SEARCH_SNORT_RUNNING = "/etc/snort/snort.conf"


class HOST_METRICS:
    """
    Constants related to the defender's sensor commands
    """
    LIST_LOGGED_IN_USERS_CMD = "users"
    LIST_OPEN_CONNECTIONS_CMD = "netstat -n"
    LIST_USER_ACCOUNTS = "cat /etc/passwd"
    LIST_FAILED_LOGIN_ATTEMPTS = "sudo tail -10000 /var/log/auth.log"
    LIST_SUCCESSFUL_LOGIN_ATTEMPTS = "last"
    LIST_NUMBER_OF_PROCESSES = "ps -e | wc -l"


class EXTERNAL_NETWORK:
    """
    Constants related to the external network
    """
    NETWORK_ID_THIRD_OCTET = 1


class ELK_CONFIG:
    """
    Constants related to the ELK container configuration
    """
    NETWORK_ID_THIRD_OCTET = 253
    NETWORK_ID_FOURTH_OCTET = 252
    SUFFIX = "_1"


class KAFKA_CONFIG:
    """
    Constants related to the kafka container configuration
    """
    NETWORK_ID_THIRD_OCTET = 253
    NETWORK_ID_FOURTH_OCTET = 253
    SUFFIX = "_1"
    CLIENT_POPULATION_TOPIC_NAME = "client_population"
    SNORT_IDS_LOG_TOPIC_NAME = "snort_ids_log"
    OSSEC_IDS_LOG_TOPIC_NAME = "ossec_ids_log"
    HOST_METRICS_TOPIC_NAME = "host_metrics"
    DOCKER_STATS_TOPIC_NAME = "docker_stats"
    DOCKER_HOST_STATS_TOPIC_NAME = "docker_host_stats"
    OPENFLOW_FLOW_STATS_TOPIC_NAME = "openflow_flow_stats_topic"
    OPENFLOW_PORT_STATS_TOPIC_NAME = "openflow_port_stats_topic"
    OPENFLOW_AGG_FLOW_STATS_TOPIC_NAME = "openflow_flow_agg_stats_topic"
    AVERAGE_OPENFLOW_FLOW_STATS_PER_SWITCH_TOPIC_NAME = "avg_openflow_flow_stats_per_switch_topic"
    AVERAGE_OPENFLOW_PORT_STATS_PER_SWITCH_TOPIC_NAME = "avg_openflow_port_stats_per_switch_topic"
    ATTACKER_ACTIONS_TOPIC_NAME = "attacker_actions"
    DEFENDER_ACTIONS_TOPIC_NAME = "defender_actions"
    CLIENT_POPULATION_TOPIC_ATTRIBUTES = ["timestamp", "ip", "num_clients", "rate"]
    SNORT_IDS_LOG_TOPIC_ATTRIBUTES = ["timestamp", "ip", "attempted-admin", "attempted-user",
                                      "inappropriate-content", "policy-violation", "shellcode-detect",
                                      "successful-admin", "successful-user", "trojan-activity", "unsuccessful-user",
                                      "web-application-attack", "attempted-dos", "attempted-recon", "bad-unknown",
                                      "default-login-attempt", "denial-of-service", "misc-attack",
                                      "non-standard-protocol", "rpc-portmap-decode", "successful-dos",
                                      "successful-recon-largescale", "successful-recon-limited",
                                      "suspicious-filename-detect", "suspicious-login", "system-call-detect",
                                      "unusual-client-port-connection", "web-application-activity", "icmp-event",
                                      "misc-activity", "network-scan", "not-suspicious", "protocol-command-decode",
                                      "string-detect", "unknown", "tcp-connection", "priority_1", "priority_2",
                                      "priority_3", "priority_4", "alerts_weighted_by_priority", "total_alerts",
                                      "severe_alerts", "warning_alerts"]
    OSSEC_IDS_LOG_TOPIC_ATTRIBUTES = ["timestamp", "ip", "total_alerts", "warning_alerts", "severe_alerts",
                                      "alerts_weighted_by_level", "level_0_alerts", "level_1_alerts",
                                      "level_2_alerts", "level_3_alerts", "level_4_alerts", "level_5_alerts",
                                      "level_6_alerts", "level_7_alerts", "level_8_alerts", "level_9_alerts",
                                      "level_10_alerts", "level_11_alerts", "level_12_alerts", "level_13_alerts",
                                      "level_14_alerts", "level_15_alerts", "invalid_login_alerts",
                                      "authentication_success_alerts", "authentication_failed_alerts",
                                      "connection_attempt_alerts", "attacks_alerts", "adduser_alerts", "sshd_alerts",
                                      "ids_alerts", "firewall_alerts", "squid_alerts",
                                      "apache_alerts", "syslog_alerts"]
    HOST_METRICS_TOPIC_ATTRIBUTES = ["timestamp", "ip", "num_logged_in_users", "num_failed_login_attempts",
                                     "num_open_connections", "num_login_events", "num_processes", "num_users"]
    DOCKER_STATS_TOPIC_ATTRIBUTES = ["timestamp", "ip", "cpu_percent", "mem_current", "mem_total",
                                     "mem_percent", "blk_read", "blk_write", "net_rc", "net_tx", "pids"]
    ATTACKER_ACTIONS_ATTRIBUTES = ["timestamp", "id", "description", "index", "name", "time", "ip", "cmd"]
    DEFENDER_ACTIONS_ATTRIBUTES = ["timestamp", "id", "description", "index", "name", "time", "ip", "cmd"]
    OPENFLOW_FLOW_STATS_TOPIC_ATTRIBUTES = ["timestamp", "datapath_id", "in_port", "out_port", "dst_mac_address",
                                            "num_packets", "num_bytes", "duration_nanoseconds",
                                            "duration_seconds", "hard_timeout", "idle_timeout", "priority",
                                            "cookie"]
    OPENFLOW_PORT_STATS_TOPIC_ATTRIBUTES = ["timestamp", "datapath_id", "port", "num_received_packets",
                                            "num_received_bytes", "num_received_errors", "num_transmitted_packets",
                                            "num_transmitted_bytes", "num_transmitted_errors", "num_received_dropped",
                                            "num_transmitted_dropped", "num_received_frame_errors",
                                            "num_received_overrun_errors", "num_received_crc_errors", "num_collisions",
                                            "duration_nanoseconds", "duration_seconds"]
    OPENFLOW_AGG_FLOW_STATS_TOPIC_ATTRIBUTES = ["timestamp", "datapath_id", "total_num_packets", "total_num_bytes",
                                                "total_num_flows"]
    AVERAGE_OPENFLOW_FLOW_STATS_PER_SWITCH_TOPIC_ATTRIBUTES = [
        "timestamp", "datapath_id", "total_num_packets", "total_num_bytes", "avg_duration_nanoseconds",
        "avg_duration_seconds", "avg_hard_timeout", "avg_idle_timeout", "avg_priority", "avg_cookie"]
    AVERAGE_OPENFLOW_PORT_STATS_PER_SWITCH_TOPIC_ATTRIBUTES = [
        "timestamp", "datapath_id", "total_num_received_packets", "total_num_received_bytes",
        "total_num_received_errors", "total_num_transmitted_packets", "total_num_transmitted_bytes",
        "total_num_transmitted_errors", "total_num_received_dropped", "total_num_transmitted_dropped",
        "total_num_received_frame_errors", "total_num_received_overrun_errors",
        "total_num_received_crc_errors", "total_num_collisions", "avg_duration_nanoseconds", "avg_duration_seconds"]

    SNORT_IDS_ALERTS_LABELS = [
        "total_alerts", "warning_alerts", "severe_alerts", "alerts_weighted_by_priority",
        "priority_1_alerts", "priority_2_alerts",
        "priority_3_alerts", "priority_4_alerts", "attempted-admin_alerts",
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
        "string-detect_alerts", "unknown_alerts", "tcp-connection_alerts"
    ]
    OSSEC_IDS_ALERTS_LABELS = [
        "total_alerts", "warning_alerts", "severe_alerts", "alerts_weighted_by_level",
        "level_0_alerts", "level_1_alerts",
        "level_2_alerts", "level_3_alerts", "level_4_alerts", "level_5_alerts", "level_6_alerts", "level_7_alerts",
        "level_8_alerts", "level_9_alerts", "level_10_alerts", "level_11_alerts", "level_12_alerts",
        "level_13_alerts", "level_14_alerts", "level_15_alerts",
        "invalid_login_alerts", "authentication_success_alerts", "authentication_failed_alerts",
        "connection_attempt_alerts", "attacks_alerts", "adduser_alerts", "sshd_alerts", "ids_alerts",
        "firewall_alerts", "squid_alerts", "apache_alerts", "syslog_alerts"
    ]
    HOST_METRICS_LABELS = [
        "num_logged_in_users", "severe_alerts", "warning_alerts",
        "num_failed_login_attempts", "num_open_connections", "num_login_events",
        "num_processes", "num_users"
    ]
    DOCKER_STATS_COUNTER_LABELS = [
        "pids", "cpu_percent", "mem_current", "mem_total",
        "mem_percent", "blk_read", "blk_write", "net_rx", "net_tx"
    ]
    DOCKER_STATS_PERCENT_LABELS = [
        "cpu_percent", "cpu_percent"
    ]
    CLIENT_POPULATION_METRIC_LABELS = ["num_clients", "rate"]
    ALL_DELTA_LABELS = (SNORT_IDS_ALERTS_LABELS + HOST_METRICS_LABELS + DOCKER_STATS_COUNTER_LABELS +
                        DOCKER_STATS_PERCENT_LABELS + CLIENT_POPULATION_METRIC_LABELS + OSSEC_IDS_ALERTS_LABELS)
    ALL_INITIAL_LABELS = (HOST_METRICS_LABELS + DOCKER_STATS_COUNTER_LABELS + DOCKER_STATS_PERCENT_LABELS +
                          CLIENT_POPULATION_METRIC_LABELS + SNORT_IDS_ALERTS_LABELS + OSSEC_IDS_ALERTS_LABELS)


class KAFKA:
    """
    String constants for managing Kafka
    """
    KAFKA_STATUS = "service kafka status"
    KAFKA_STOP = "service kafka stop"
    KAFKA_START = "service kafka start"
    RETENTION_MS_CONFIG_PROPERTY = "retention.ms"
    BOOTSTRAP_SERVERS_PROPERTY = "bootstrap.servers"
    CLIENT_ID_PROPERTY = "client.id"
    GROUP_ID_PROPERTY = "group.id"
    AUTO_OFFSET_RESET_PROPERTY = "auto.offset.reset"
    EARLIEST_OFFSET = "earliest"
    PORT = 9092
    DIR = "/usr/local/kafka/logs/"


class ELK:
    """
    String constants for managing the ELK stack
    """
    ELK_START = "nohup /usr/local/bin/start.sh > /elk_server.log &"
    ELK_LOG = "/elk_server.log"
    ELASTICSEARCH_STOP = "service elasticsearch stop"
    KIBANA_STOP = "service kibana stop"
    LOGSTASH_STOP = "service logstash stop"
    ELASTICSEARCH_START = "service elasticsearch start"
    KIBANA_START = "service kibana start"
    LOGSTASH_START = "service logstash start"
    ELASTICSEARCH_STATUS = "service elasticsearch status"
    KIBANA_STATUS = "service kibana status"
    LOGSTASH_STATUS = "service logstash status"
    ELASTICSEARCH_LOG_DIR = "/var/log/elasticsearch/"
    LOGSTASH_LOG_DIR = "/var/log/logstash/"
    KIBANA_LOG_DIR = "/var/log/kibana/"
