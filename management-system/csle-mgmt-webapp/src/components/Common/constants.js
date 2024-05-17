/**
 * File with constants
 */

export const HTTP_PREFIX = "http://"
export const ACCESS_CONTROL_ALLOW_ORIGIN_HEADER = "Access-Control-Allow-Origin"
export const IDS_QUERY_PARAM = "ids"
export const DOWNLOAD_QUERY_PARAM = "download"
export const TOKEN_QUERY_PARAM = "token"
export const STOP_QUERY_PARAM = "stop"
export const EMULATION_QUERY_PARAM = "emulation"
export const EXECUTION_ID_QUERY_PARAM = "executionid"
export const IP_QUERY_PARAM = "ip"
export const CONTAINER_NAME_PROPERTY = "container_name"
export const STATIC_RESOURCE_INDEX = "index.html"
export const HTTP_REST_GET = "GET"
export const HTTP_REST_POST = "POST"
export const HTTP_REST_DELETE = "DELETE"
export const HTTP_REST_PUT = "PUT"
export const STATIC = "static"
export const ABOUT_PAGE_RESOURCE = "about-page"
export const LOGIN_PAGE_RESOURCE = "login-page"
export const SDN_CONTROLLER_LOCAL_PORT = "sdn-controller-local-port"
export const REGISTER_PAGE_RESOURCE = "register-page"
export const EMULATION_STATISTICS_PAGE_RESOURCE = "emulation-statistics-page"
export const CREATE_EMULATION_PAGE_RESOURCE = "create-emulation-page"
export const EMULATIONS_PAGE_RESOURCE = "emulations-page"
export const IMAGES_PAGE_RESOURCE = "images-page"
export const DOWNLOADS_PAGE_RESOURCE = "downloads-page"
export const JOBS_PAGE_RESOURCE = "jobs-page"
export const MONITORING_PAGE_RESOURCE = "monitoring-page"
export const POLICIES_PAGE_RESOURCE = "policies-page"
export const POLICY_EXAMINATION_PAGE_RESOURCE = "policy-examination-page"
export const SDN_CONTROLLERS_PAGE_RESOURCE = "sdn-controllers-page"
export const CONTROL_PLANE_PAGE_RESOURCE = "control-plane-page"
export const SERVER_CLUSTER_PAGE_RESOURCE = "server-cluster-page"
export const USER_ADMIN_PAGE_RESOURCE = "user-admin-page"
export const CONTAINER_TERMINAL_PAGE_RESOURCE = "container-terminal-page"
export const SYSTEM_ADMIN_PAGE_RESOURCE = "system-admin-page"
export const LOGS_ADMIN_PAGE_RESOURCE = "logs-admin-page"
export const SIMULATIONS_PAGE_RESOURCE = "simulations-page"
export const SYSTEM_MODELS_PAGE_RESOURCE = "system-models-page"
export const TRACES_PAGE_RESOURCE = "traces-page"
export const TRAINING_PAGE_RESOURCE = "training-page"
export const CREATE_EMULATION_PAGE = "create-emulation-page"
export const CADVISOR_RESOURCE = "cadvisor"
export const GRAFANA_RESOURCE = "grafana"
export const PGADMIN_RESOURCE = "pgadmin"
export const POSTGRESQL_RESOURCE = "postgresql"
export const NGINX_RESOURCE = "nginx"
export const DOCKER_RESOURCE = "docker"
export const FLASK_RESOURCE = "flask"
export const CLUSTER_MANAGER_RESOURCE = "clustermanager"
export const CLUSTER_STATUS_RESOURCE = "clusterstatus"
export const NODE_EXPORTER_RESOURCE = "node-exporter"
export const PROMETHEUS_RESOURCE = "prometheus"
export const EMULATIONS_RESOURCE = "emulations"
export const EXECUTIONS_SUBRESOURCE = "executions"
export const INFO_SUBRESOURCE = "info"
export const CLIENT_MANAGER_SUBRESOURCE = "client-manager"
export const RYU_MANAGER_SUBRESOURCE = "ryu-manager"
export const RYU_CONTROLLER_SUBRESOURCE = "ryu-controller"
export const RYU_MONITOR_SUBRESOURCE = "ryu-monitor"
export const CLIENT_POPULATION_SUBRESOURCE = "client-population"
export const CLIENT_PRODUCER_SUBRESOURCE = "client-producer"
export const KAFKA_MANAGER_SUBRESOURCE = "kafka-manager"
export const KAFKA_SUBRESOURCE = "kafka"
export const ELK_MANAGER_SUBRESOURCE = "elk-manager"
export const ELK_STACK_SUBRESOURCE = "elk-stack"
export const ELASTIC_SUBRESOURCE = "elastic"
export const KIBANA_SUBRESOURCE = "kibana"
export const LOGSTASH_SUBRESOURCE = "logstash"
export const OSSEC_IDS_MANAGER_SUBRESOURCE = "ossec-ids-manager"
export const OSSEC_IDS_SUBRESOURCE = "ossec-ids"
export const OSSEC_IDS_MONITOR_SUBRESOURCE = "ossec-ids-monitor"
export const SNORT_IDS_MANAGER_SUBRESOURCE = "snort-ids-manager"
export const SNORT_IDS_SUBRESOURCE = "snort-ids"
export const SNORT_IDS_MONITOR_SUBRESOURCE = "snort-ids-monitor"
export const HOST_MANAGER_SUBRESOURCE = "host-manager"
export const HOST_MONITOR_SUBRESOURCE = "host-monitor"
export const FILEBEAT_SUBRESOURCE = "filebeat"
export const PACKETBEAT_SUBRESOURCE = "packetbeat"
export const METRICBEAT_SUBRESOURCE = "metricbeat"
export const HEARTBEAT_SUBRESOURCE = "heartbeat"
export const TRAFFIC_MANAGER_SUBRESOURCE = "traffic-manager"
export const TRAFFIC_GENERATOR_SUBRESOURCE = "traffic-generator"
export const DOCKER_STATS_MANAGER_SUBRESOURCE = "docker-stats-manager"
export const DOCKER_STATS_MONITOR_SUBRESOURCE = "docker-stats-monitor"
export const CREATE_SUBRESOURCE = "create"
export const CONTAINER_SUBRESOURCE = "container"
export const SWITCHES_SUBRESOURCE = "switches"
export const MONITOR_SUBRESOURCE = "monitor"
export const EMULATION_EXECUTIONS_RESOURCE = "emulation-executions"
export const EMULATION_TRACES_RESOURCE = "emulation-traces"
export const VERSION_RESOURCE = "version"
export const EMULATION_SIMULATION_TRACES_RESOURCE = "emulation-simulation-traces"
export const SIMULATION_TRACES_RESOURCE = "simulation-traces"
export const TRACES_DATASETS_RESOURCE = "traces-datasets"
export const STATISTICS_DATASETS_RESOURCE = "statistics-datasets"
export const SIMULATIONS_RESOURCE = "simulations"
export const EMULATION_STATISTICS_RESOURCE = "emulation-statistics"
export const IMAGES_RESOURCE = "images"
export const FILE_RESOURCE = "file"
export const LOGIN_RESOURCE = "login"
export const REGISTRATION_ALLOWED_SUBRESOURCE = "registration-allowed"
export const JOBS_RESOURCE = "jobs"
export const MONITORING_RESOURCE = "monitoring"
export const POLICIES_RESOURCE = "policies"
export const SDN_CONTROLLERS_RESOURCE = "sdn-controllers"
export const SYSTEM_MODELS_RESOURCE = "system-models"
export const GAUSSIAN_MIXTURE_SYSTEM_MODELS_RESOURCE = "gaussian-mixture-system-models"
export const EMPIRICAL_SYSTEM_MODELS_RESOURCE = "empirical-system-models"
export const MCMC_SYSTEM_MODELS_RESOURCE = "mcmc-system-models"
export const GP_SYSTEM_MODELS_RESOURCE = "gp-system-models"
export const EXPERIMENTS_RESOURCE = "experiments"
export const MULTI_THRESHOLD_POLICIES_RESOURCE = "multi-threshold-policies"
export const LINEAR_THRESHOLD_POLICIES_RESOURCE = "linear-threshold-policies"
export const PPO_POLICIES_RESOURCE = "ppo-policies"
export const ALPHA_VEC_POLICIES_RESOURCE = "alpha-vec-policies"
export const VECTOR_POLICIES_RESOURCE = "vector-policies"
export const TABULAR_POLICIES_RESOURCE = "tabular-policies"
export const CREATE_EMULATION_RESOURCE = "create-emulation"
export const USERS_RESOURCE = "users"
export const LOGS_RESOURCE = "logs"
export const CONFIG_RESOURCE = "config"
export const SERVER_CLUSTER_RESOURCE = "server-cluster"
export const DQN_POLICIES_RESOURCE = "dqn-policies"
export const FNN_W_SOFTMAX_POLICIES_RESOURCE = "fnn-w-softmax-policies"
export const TRACES_RESOURCE = "traces"
export const TRAINING_RESOURCE = "training"
export const RUNNING_PROPERTY = "running"
export const OUTPUT_PROPERTY = "output"
export const INPUT_PROPERTY = "input"
export const ROWS_PROPERTY = "rows"
export const COLS_PROPERTY = "cols"
export const WS_CONNECT_MSG = "connect"
export const WS_CONNECT_ERROR = "connect_error"
export const WS_DISCONNECT_MSG = "disconnect"
export const WS_CONTAINER_TERMINAL_OUTPUT_MSG = "container-terminal-output"
export const WS_CONTAINER_TERMINAL_INPUT_MSG = "container-terminal-input"
export const WS_RESIZE_MSG = "resize"
export const IP_PROPERTY = "ip"
export const EXEC_ID_PROPERTY = "exec_id"
export const EMULATION_PROPERTY = "emulation"
export const STATISTIC_ID_PROPERTY = "statistic_id"
export const SYSTEM_MODEL_TYPE = "system_model_type"
export const SIMULATION_PROPERTY = "simulation"
export const TRACES_DATASET_PROPERTY = "traces_dataset"
export const STATISTICS_DATASET_PROPERTY = "statistics_dataset"
export const ID_PROPERTY = "id"
export const NAME_PROPERTY = "name"
export const SIZE_PROPERTY = "size"
export const TRAINING_JOBS_RESOURCE = "training-jobs"
export const DATA_COLLECTION_JOBS_RESOURCE = "data-collection-jobs"
export const SYSTEM_IDENTIFICATION_JOBS_RESOURCE = "system-identification-jobs"
export const LOGS_PROPERTY = "logs"
export const PATH_PROPERTY = "path"
export const USER_PROPERTY = "user"
export const PORT_PROPERTY = "port"
export const THREAD_PROPERTY = "thread"
export const START_PROPERTY = "start"
export const CONFIG_PROPERTY = "config"
export const STOP_PROPERTY = "stop"
export const STOP_ALL_PROPERTY = "stop-all"
export const START_ALL_PROPERTY = "start-all"
export const USERNAME_PROPERTY = "username"
export const PASSWORD_PROPERTY = "password"
export const SALT_PROPERTY = ""
export const FIRST_NAME_PROPERTY = "first_name"
export const LAST_NAME_PROPERTY = "last_name"
export const EMAIL_PROPERTY = "email"
export const ORGANIZATION_PROPERTY = "organization"
export const TOKEN_PROPERTY = "token"
export const ADMIN_PROPERTY = "admin"
export const GAUSSIAN_MIXTURE_SYSTEM_MODEL_TYPE = "gaussian_mixture"
export const EMPIRICAL_SYSTEM_MODEL_TYPE = "empirical"
export const MCMC_SYSTEM_MODEL_TYPE = "mcmc"
export const GP_SYSTEM_MODEL_TYPE = "gp"
export const WS_CONTAINER_TERMINAL_NAMESPACE = "container-terminal"
export const REGISTRATION_ALLOWED_PROPERTY = "registration_allowed"
export const GAUSSIAN_MIXTURE_SYSTEM_MODEL_TYPE_INT = 0
export const EMPIRICAL_SYSTEM_MODEL_TYPE_INT = 1
export const MCMC_SYSTEM_MODEL_TYPE_INT = 3
export const GP_SYSTEM_MODEL_TYPE_INT = 2
export const CONTAINERS_OS = {
    csle_ssh_1: [{
        name: 'csle_ssh_1',
        os: 'ubuntu'
    }],
    csle_router_2: [{
        name: 'csle_router_2',
        os: 'ubuntu'
    }],
    csle_samba_2: [{
        name: 'csle_samba_2',
        os: 'debian'
    }],
    csle_honeypot_1: [{
        name: 'csle_honeypot_1',
        os: 'ubuntu'
    }],
    csle_ftp_1: [{
        name: 'csle_ftp_1',
        os: 'ubuntu'
    }],
    csle_hacker_kali_1: [{
        name: 'csle_hacker_kali_1',
        os: 'kali'
    }],
    csle_shellshock_1: [{
        name: 'csle_shellshock_1',
        os: 'debian'
    }],
    csle_sql_injection_1: [{
        name: 'csle_sql_injection_1',
        os: 'debian'
    }],
    csle_cve_2010_0426_1: [{
        name: 'csle_cve_2010_0426_1',
        os: 'debian'
    }],
    csle_cve_2015_1427_1: [{
        name: 'csle_cve_2015_1427_1',
        os: 'debian'
    }],
    csle_honeypot_2: [{
        name: 'csle_honeypot_2',
        os: 'ubuntu'
    }],
    csle_cve_2015_3306_1: [{
        name: 'csle_cve_2015_3306_1',
        os: 'debian'
    }],
    csle_cve_2015_5602_1: [{
        name: 'csle_cve_2015_5602_1',
        os: 'debian'
    }],
    csle_cve_2016_10033_1: [{
        name: 'csle_cve_2016_10033_1',
        os: 'debian'
    }],
    csle_client_1: [{
        name: 'csle_client_1',
        os: 'ubuntu'
    }],
    csle_kafka_1: [{
        name: 'csle_kafka_1',
        os: 'ubuntu'
    }],
    csle_elk_1: [{
        name: 'csle_elk_1',
        os: 'ubuntu'
    }],
    csle_router_1: [{
        name: 'csle_router_1',
        os: 'ubuntu'
    }],
    csle_telnet_1: [{
        name: 'csle_telnet_1',
        os: 'ubuntu'
    }],
    csle_ssh_2: [{
        name: 'csle_ssh_2',
        os: 'ubuntu'
    }],
    csle_ssh_3: [{
        name: 'csle_ssh_3',
        os: 'ubuntu'
    }],
    csle_telnet_2: [{
        name: 'csle_telnet_2',
        os: 'ubuntu'
    }],
    csle_telnet_3: [{
        name: 'csle_telnet_3',
        os: 'ubuntu'
    }],
    csle_ftp_2: [{
        name: 'csle_ftp_2',
        os: 'ubuntu'
    }],
    csle_ovs_1: [{
        name: 'csle_ovs_1',
        os: 'ubuntu'
    }],
    csle_ryu_1: [{
        name: 'csle_ryu_1',
        os: 'ubuntu'
    }],
    csle_pengine_exploit_1: [{
        name: 'csle_pengine_exploit_1',
        os: 'ubuntu'
    }],
    csle_cve_2014_0160_1: [{
        name: 'csle_cve_2014_0160_1',
        os: 'debian'
    }],
    csle_spark_1: [{
        name: 'csle_spark_1',
        os: 'spark'
    }]
}
export const DEFAULT_INTERFACE_CONFIG = {
    name: '',
    ip: '',
    subnetMask: '',
    subnetPrefix: '',
    physicalInterface: '',
    bitmask: '',
    limitPacketsQueue: 30000,
    packetDelayMs: 2,
    packetDelayJitterMs: 0.5,
    packetDelayCorrelationPercentage: 25,
    packetDelayDistribution: '0',
    packetLossType: '0',
    lossGemodelp: 0.02,
    lossGemodelr: 0.97,
    lossGemodelk: 0.98,
    lossGemodelh: 0.0001,
    packetCorruptPercentage: 0.00001,
    packetCorruptCorrelationPercentage: 25,
    packetDuplicatePercentage: 0.00001,
    packetDuplicateCorrelationPercentage: 25,
    packetReorderPercentage: 0.0025,
    packetReorderCorrelationPercentage: 25,
    packetReorderGap: 5,
    rateLimitMbit: 1000,
    packetOverheadBytes: 0,
    cellOverheadBytes: 0,
    defaultGateway: "0.0.0.0",
    defaultInput: "accept",
    defaultOutput: "accept",
    defaultForward: "Drop",
    trafficManagerPort: "50043",
    trafficManagerLogFile: "traffic_manager.log",
    trafficManagerLogDir: "/",
    trafficManagerMaxWorkers: "10"
}