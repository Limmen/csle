INSTALL = "sudo /root/miniconda3/bin/pip install -U --no-cache-dir csle-ryu "
LATEST_VERSION = "latest"


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
    LOG_FILE = "csle_sdn_controller.log"
    WEB_APP_PORT_ARG = "--wsapi-port"
    RYU_MANAGER = "/root/miniconda3/bin/ryu-manager"
    PACKET_BUFFER_MAX_LEN = 512
    NORTHBOUND_API_APP_NAME = "csle_api_app"
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
    WSGI = "wsgi"
    CONTROLLER_APP = "controller_app"
    NETWORK_ID_THIRD_OCTET = 252
    NETWORK_ID_FOURTH_OCTET = 251
    SUFFIX = "_1"
    DEFAULT_PORT = 6633
    DEFAULT_TRANSPORT_PROTOCOL = "tcp"
    SUBNETMASK_SUFFIX = "/29"
    FULL_SUBNETMASK_SUFFIX = ".0/24"
    BITMASK = "255.255.255.248"
    FULL_BITMASK = "255.255.255.0"
    STPLIB = "stplib"
    BYTE_COUNT = "byte_count"
    PACKET_COUNT = "packet_count"
    FLOW_COUNT = "flow_count"
    IN_PORT = "in_port"
    ETH_DST = "eth_dst"
    PRODUCER_RUNNING = "producer_running"
    KAFKA_CONF = "kafka_conf"
    TIMEOUT = 5


class CONTROLLERS:
    """
    RYU Controllers in CSLE
    """
    LEARNING_SWITCH_CONTROLLER = "learning_switch_controller"
    LEARNING_SWITCH_STP_CONTROLLER = "learning_switch_stp_controller"
