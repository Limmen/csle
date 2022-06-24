

class RYU:
    """
    String constants related to RYU
    """
    CONTROLLERS_PREFIX = "csle_ryu.controllers."
    OFCTL_REST_APP = "ryu.app.ofctl_rest"
    OFCTL_REST_QOS_APP = "ryu.app.rest_qos"
    OFCTL_REST_TOPOLOGY = "ryu.app.rest_topology"
    OFCTL_WS_TOPOLOGY = "ryu.app.ws_topology"
    OFCTL_GUI_TOPOLOGY = "ryu.app.gui_topology.gui_topology"
    OBSERVE_LINKS = "--observe-links"
    APP_LISTS_ARG = "--app-lists"
    LOG_FILE_ARG = "--log-file"
    CONTROLLER_PORT_ARG = "--ofp-tcp-listen-port"
    WEB_APP_PORT_ARG = "--wsapi-port"
    RYU_MANAGER = "/root/miniconda3/bin/ryu-manager"
    PACKET_BUFFER_MAX_LEN = 512
    NORTHBOUND_API_APP_NAME = "csle_api_app"
    START_PRODUCER_HTTP_RESOURCE = "/cslenorthboundapi/producer/start"
    STOP_PRODUCER_HTTP_RESOURCE = "/cslenorthboundapi/producer/stop"
    STATUS_PRODUCER_HTTP_RESOURCE = "/cslenorthboundapi/producer/status"


class CONTROLLERS:
    """
    RYU Controllers in CSLE
    """
    LEARNING_SWITCH_CONTROLLER = "learning_switch_controller"
    LEARNING_SWITCH_STP_CONTROLLER = "learning_switch_stp_controller"


class TOPIC_NAMES:
    """
    Topic names for SDN statistics
    """
    OPENFLOW_FLOW_STATS_TOPIC_NAME = "openflow_flow_stats_topic"
    OPENFLOW_PORT_STATS_TOPIC_NAME = "openflow_port_stats_topic"
    AVERAGE_OPENFLOW_FLOW_STATS_PER_SWITCH_TOPIC_NAME = "avg_openflow_flow_stats_per_switch_topic"
    AVERAGE_OPENFLOW_PORT_STATS_PER_SWITCH_TOPIC_NAME = "avg_openflow_port_stats_per_switch_topic"

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
    TIME_STEP_LEN_SECONDS = "time_step_len_seconds"

