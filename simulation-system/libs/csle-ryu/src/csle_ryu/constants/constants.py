

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
    STATS_SWITCHES_RESOURCE = "/stats/switches"
    STATS_DESC_RESOURCE = "/stats/desc"
    STATS_FLOW_RESOURCE = "/stats/flow"
    STATS_AGGREGATE_FLOW_RESOURCE = "/stats/aggregateflow"
    STATS_TABLE_RESOURCE = "/stats/table"
    STATS_TABLE_FEATURES_RESOURCE = "/stats/tablefeatures"
    STATS_PORT_RESOURCE = "/stats/port"
    STATS_PORT_DESC_RESOURCE = "/stats/portdesc"
    STATS_QUEUE_RESOURCE = "/stats/queue"
    STATS_QUEUE_CONFIG_RESOURCE = "/stats/queueconfig"
    STATS_QUEUE_DESC_RESOURCE = "/stats/queuedesc"
    STATS_GROUP_RESOURCE = "/stats/group"
    STATS_GROUP_DESC_RESOURCE = "/stats/groupdesc"
    STATS_GROUP_FEATURES_RESOURCE = "/stats/groupfeatures"
    STATS_METER_RESOURCE = "/stats/meter"
    STATS_METER_CONFIG_RESOURCE = "/stats/meterconfig"
    STATS_METER_FEATURES_RESOURCE = "/stats/meterfeatures"
    STATS_ROLE_RESOURCE = "/stats/role"


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
    OPENFLOW_AGG_FLOW_STATS_TOPIC_NAME = "openflow_flow_agg_stats_topic"
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
