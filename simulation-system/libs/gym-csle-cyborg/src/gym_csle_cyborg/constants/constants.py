"""
Constants for gym-csle-cyborg
"""


class STATIC_DEFENDER_STRATEGIES:
    """
    String constants representing static defender strategies
    """
    RANDOM = "random"


class STATIC_ATTACKER_STRATEGIES:
    """
    String constants representing static attacker strategies
    """
    RANDOM = "random"


class ENV_METRICS:
    """
    String constants representing environment metrics
    """
    RETURN = "R"
    TIME_HORIZON = "T"
    STOP = "stop"
    STATE = "s"
    STATE_ID = "s_id"
    STATE_VECTOR = "state_vector"
    DEFENDER_ACTION = "a1"
    ATTACKER_ACTION = "a2"
    OBSERVATION = "o"
    OBSERVATION_VECTOR = "obs_vec"
    OBSERVATION_ID = "obs_id"
    TIME_STEP = "t"
    AVERAGE_UPPER_BOUND_RETURN = "average_upper_bound_return"


class CYBORG:
    """
    String constants related to Cyborg
    """
    SCENARIO_CONFIGS_DIR = "/shared/scenarios/"
    SCENARIO_CONFIG_PREFIX = "Scenario"
    SCENARIO_CONFIG_SUFFIX = ".yaml"
    SCENARIO_2_CONFIG_PATH = '/shared/scenarios/Scenario2.yaml'
    SIMULATION = "sim"
    RED = "Red"
    BLUE = "Blue"
    Green = "Green"
    ALL_HOSTNAME = "ALL"
    HOSTNAME = "hostname"
    SUBNET = "subnet"
    IP_ADDRESS = "ip_address"
    SUBNET_BLUE_TABLE_IDX = 0
    IP_BLUE_TABLE_IDX = 1
    HOSTNAME_BLUE_TABLE_IDX = 2
    ACTIVITY_BLUE_TABLE_IDX = 3
    COMPROMISED_BLUE_TABLE_IDX = 4
    BLUE_TABLE = "blue_table"
    VECTOR_OBS_PER_HOST = "vector_obs_per_host"
    OBS_PER_HOST = "obs_per_host"
    ACTIVITY = "activity"
    SCANNED_STATE = "scanned_state"
    DECOY_STATE = "decoy_state"
    COMPROMISED = "compromised"
    NOT_SCANNED = 0
    SCANNED = 1
    MOST_RECENTLY_SCANNED = 2
    NO = "No"
    NONE = "None"
    USER = "User"
    PRIVILEGED = "Privileged"
    UNKNOWN = "Unknown"
    DEFENDER = "Defender"
    ENTERPRISE0 = "Enterprise0"
    ENTERPRISE1 = "Enterprise1"
    ENTERPRISE2 = "Enterprise2"
    OP_HOST0 = "Op_Host0"
    OP_HOST1 = "Op_Host1"
    OP_HOST2 = "Op_Host2"
    OP_SERVER0 = "Op_Server0"
    USER0 = "User0"
    USER1 = "User1"
    USER2 = "User2"
    USER3 = "User3"
    USER4 = "User4"
    DEFENDER_IDX = 0
    ENTERPRISE0_IDX = 1
    ENTERPRISE1_IDX = 2
    ENTERPRISE2_IDX = 3
    OP_HOST0_IDX = 4
    OP_HOST1_IDX = 5
    OP_HOST2_IDX = 6
    OP_SERVER0_IDX = 7
    USER0_IDX = 8
    USER1_IDX = 9
    USER2_IDX = 10
    USER3_IDX = 11
    USER4_IDX = 12
    NUM_HOSTS = 13
    NUM_SUBNETS = 3
    USER_HOST_IDS = [8, 9, 10, 11, 12]
    ENTERPRISE_HOST_IDS = [0, 1, 2, 3]
    OPERATIONAL_HOST_IDS = [4, 5, 6, 7]
    USER_SUBNET_ID = 0
    ENTERPRISE_SUBNET_ID = 1
    OPERATIONAL_SUBNET_ID = 2
    HOST_STATE_KNOWN_IDX = 0
    HOST_STATE_SCANNED_IDX = 1
    HOST_STATE_ACCESS_IDX = 2
    HOST_STATE_DECOY_IDX = 3
    SSH_PORT = 22
    B_LINE_AGENT_JUMPS = [0, 1, 2, 2, 2, 2, 5, 5, 5, 5, 9, 9, 9, 12, 13]
