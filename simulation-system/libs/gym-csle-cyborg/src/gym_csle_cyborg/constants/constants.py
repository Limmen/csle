"""
Constants for gym-csle-cyborg
"""


class COMMON:
    """
    Common string constants
    """
    STATE = "s"
    OBSERVATION = "o"
    REWARD = "r"


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
    REWARD = "r"
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
    CYBORG_SCENARIO_2_DICT = {
        "Agents": {
            "Blue": {
                "AllowedSubnets": [
                    "User",
                    "Enterprise",
                    "Operational"
                ],
                "INT": {
                    "Hosts": {
                        "Defender": {
                            "Interfaces": "All",
                            "System info": "All",
                            "User info": "All"
                        },
                        "Enterprise0": {
                            "Interfaces": "All",
                            "System info": "All",
                            "User info": "All"
                        },
                        "Enterprise1": {
                            "Interfaces": "All",
                            "System info": "All",
                            "User info": "All"
                        },
                        "Enterprise2": {
                            "Interfaces": "All",
                            "System info": "All",
                            "User info": "All"
                        },
                        "Op_Host0": {
                            "Interfaces": "All",
                            "System info": "All",
                            "User info": "All"
                        },
                        "Op_Host1": {
                            "Interfaces": "All",
                            "System info": "All",
                            "User info": "All"
                        },
                        "Op_Host2": {
                            "Interfaces": "All",
                            "System info": "All",
                            "User info": "All"
                        },
                        "Op_Server0": {
                            "Interfaces": "All",
                            "System info": "All",
                            "User info": "All"
                        },
                        "User0": {
                            "Interfaces": "All",
                            "System info": "All",
                            "User info": "All"
                        },
                        "User1": {
                            "Interfaces": "All",
                            "System info": "All",
                            "User info": "All"
                        },
                        "User2": {
                            "Interfaces": "All",
                            "System info": "All",
                            "User info": "All"
                        },
                        "User3": {
                            "Interfaces": "All",
                            "System info": "All",
                            "User info": "All"
                        },
                        "User4": {
                            "Interfaces": "All",
                            "System info": "All",
                            "User info": "All"
                        }
                    }
                },
                "adversary": "Red",
                "actions": [
                    "Sleep",
                    "Monitor",
                    "Analyse",
                    "Remove",
                    "DecoyApache",
                    "DecoyFemitter",
                    "DecoyHarakaSMPT",
                    "DecoySmss",
                    "DecoySSHD",
                    "DecoySvchost",
                    "DecoyTomcat",
                    "DecoyVsftpd",
                    "Restore"
                ],
                "agent_type": "SleepAgent",
                "reward_calculator_type": "HybridAvailabilityConfidentiality",
                "starting_sessions": [
                    {
                        "hostname": "User0",
                        "name": "VeloUser0",
                        "parent": "VeloServer",
                        "type": "VelociraptorClient",
                        "username": "ubuntu"
                    },
                    {
                        "hostname": "User1",
                        "name": "VeloUser1",
                        "parent": "VeloServer",
                        "type": "VelociraptorClient",
                        "username": "ubuntu"
                    },
                    {
                        "hostname": "User2",
                        "name": "VeloUser2",
                        "parent": "VeloServer",
                        "type": "VelociraptorClient",
                        "username": "ubuntu"
                    },
                    {
                        "hostname": "User3",
                        "name": "VeloUser3",
                        "parent": "VeloServer",
                        "type": "VelociraptorClient",
                        "username": "ubuntu"
                    },
                    {
                        "hostname": "User4",
                        "name": "VeloUser4",
                        "parent": "VeloServer",
                        "type": "VelociraptorClient",
                        "username": "ubuntu"
                    },
                    {
                        "hostname": "Enterprise0",
                        "name": "VeloEnterprise0",
                        "parent": "VeloServer",
                        "type": "VelociraptorClient",
                        "username": "ubuntu"
                    },
                    {
                        "hostname": "Enterprise1",
                        "name": "VeloEnterprise1",
                        "parent": "VeloServer",
                        "type": "VelociraptorClient",
                        "username": "SYSTEM"
                    },
                    {
                        "hostname": "Enterprise2",
                        "name": "VeloEnterprise2",
                        "parent": "VeloServer",
                        "type": "VelociraptorClient",
                        "username": "SYSTEM"
                    },
                    {
                        "hostname": "Defender",
                        "name": "VeloDefender",
                        "parent": "VeloServer",
                        "type": "VelociraptorClient",
                        "username": "ubuntu"
                    },
                    {
                        "hostname": "Op_Server0",
                        "name": "VeloOp_Server0",
                        "parent": "VeloServer",
                        "type": "VelociraptorClient",
                        "username": "ubuntu"
                    },
                    {
                        "hostname": "Op_Host0",
                        "name": "VeloOp_Host0",
                        "parent": "VeloServer",
                        "type": "VelociraptorClient",
                        "username": "ubuntu"
                    },
                    {
                        "hostname": "Op_Host1",
                        "name": "VeloOp_Host1",
                        "parent": "VeloServer",
                        "type": "VelociraptorClient",
                        "username": "ubuntu"
                    },
                    {
                        "hostname": "Op_Host2",
                        "name": "VeloOp_Host2",
                        "parent": "VeloServer",
                        "type": "VelociraptorClient",
                        "username": "ubuntu"
                    },
                    {
                        "artifacts": [
                            "NetworkConnections",
                            "ProcessCreation"
                        ],
                        "hostname": "Defender",
                        "name": "VeloServer",
                        "num_children_sessions": 2,
                        "type": "VelociraptorServer",
                        "username": "ubuntu"
                    }
                ],
                "wrappers": [

                ]
            },
            "Green": {
                "AllowedSubnets": [
                    "User",
                    "Enterprise",
                    "Operational"
                ],
                "INT": {
                    "Hosts": {
                        "Defender": {
                            "Interfaces": "All",
                            "System info": "All",
                            "User info": "All"
                        },
                        "Enterprise0": {
                            "Interfaces": "All",
                            "System info": "All",
                            "User info": "All"
                        },
                        "Enterprise1": {
                            "Interfaces": "All",
                            "System info": "All",
                            "User info": "All"
                        },
                        "Enterprise2": {
                            "Interfaces": "All",
                            "System info": "All",
                            "User info": "All"
                        },
                        "Op_Host0": {
                            "Interfaces": "All",
                            "System info": "All",
                            "User info": "All"
                        },
                        "Op_Host1": {
                            "Interfaces": "All",
                            "System info": "All",
                            "User info": "All"
                        },
                        "Op_Host2": {
                            "Interfaces": "All",
                            "System info": "All",
                            "User info": "All"
                        },
                        "Op_Server0": {
                            "Interfaces": "All",
                            "System info": "All",
                            "User info": "All"
                        },
                        "User0": {
                            "Interfaces": "All",
                            "System info": "All",
                            "User info": "All"
                        },
                        "User1": {
                            "Interfaces": "All",
                            "System info": "All",
                            "User info": "All"
                        },
                        "User2": {
                            "Interfaces": "All",
                            "System info": "All",
                            "User info": "All"
                        },
                        "User3": {
                            "Interfaces": "All",
                            "System info": "All",
                            "User info": "All"
                        },
                        "User4": {
                            "Interfaces": "All",
                            "System info": "All",
                            "User info": "All"
                        }
                    }
                },
                "actions": [
                    "Sleep",
                    "GreenPingSweep",
                    "GreenPortScan",
                    "GreenConnection"
                ],
                "agent_type": "SleepAgent",
                "reward_calculator_type": "None",
                "starting_sessions": [
                    {
                        "hostname": "User0",
                        "name": "GreenSession",
                        "type": "green_session",
                        "username": "GreenAgent"
                    },
                    {
                        "hostname": "User1",
                        "name": "GreenSession",
                        "type": "green_session",
                        "username": "GreenAgent"
                    },
                    {
                        "hostname": "User2",
                        "name": "GreenSession",
                        "type": "green_session",
                        "username": "GreenAgent"
                    },
                    {
                        "hostname": "User3",
                        "name": "GreenSession",
                        "type": "green_session",
                        "username": "GreenAgent"
                    },
                    {
                        "hostname": "User4",
                        "name": "GreenSession",
                        "type": "green_session",
                        "username": "GreenAgent"
                    },
                    {
                        "hostname": "Op_Host0",
                        "name": "GreenSession",
                        "type": "green_session",
                        "username": "GreenAgent"
                    },
                    {
                        "hostname": "Op_Host1",
                        "name": "GreenSession",
                        "type": "green_session",
                        "username": "GreenAgent"
                    },
                    {
                        "hostname": "Op_Host2",
                        "name": "GreenSession",
                        "type": "green_session",
                        "username": "GreenAgent"
                    }
                ],
                "wrappers": [

                ]
            },
            "Red": {
                "AllowedSubnets": [
                    "User",
                    "Enterprise",
                    "Operational"
                ],
                "INT": {
                    "Hosts": {
                        "User0": {
                            "Interfaces": "All",
                            "System info": "All"
                        }
                    }
                },
                "actions": [
                    "Sleep",
                    "DiscoverRemoteSystems",
                    "DiscoverNetworkServices",
                    "ExploitRemoteService",
                    "BlueKeep",
                    "EternalBlue",
                    "FTPDirectoryTraversal",
                    "HarakaRCE",
                    "HTTPRFI",
                    "HTTPSRFI",
                    "SQLInjection",
                    "PrivilegeEscalate",
                    "Impact",
                    "SSHBruteForce"
                ],
                "agent_type": "SleepAgent",
                "reward_calculator_type": "HybridImpactPwn",
                "starting_sessions": [
                    {
                        "hostname": "User0",
                        "name": "RedPhish",
                        "type": "RedAbstractSession",
                        "username": "SYSTEM"
                    }
                ],
                "wrappers": [

                ]
            }
        },
        "Hosts": {
            "Defender": {
                "AWS_Info": [

                ],
                "Processes": [
                    {
                        "PID": 1,
                        "PPID": 0,
                        "Path": "/sbin",
                        "Process Name": "init",
                        "Username": "root"
                    },
                    {
                        "PID": 389,
                        "PPID": 1,
                        "Path": "/lib/systemd",
                        "Process Name": "systemd-journald",
                        "Username": "root"
                    },
                    {
                        "PID": 407,
                        "PPID": 1,
                        "Path": "/lib/systemd",
                        "Process Name": "systemd-udevd",
                        "Username": "root"
                    },
                    {
                        "PID": 409,
                        "PPID": 1,
                        "Path": "/sbin",
                        "Process Name": "lvmetad",
                        "Username": "root"
                    },
                    {
                        "PID": 560,
                        "PPID": 1,
                        "Path": "/lib/systemd",
                        "Process Name": "systemd-timesyncd",
                        "Username": "systemd+"
                    },
                    {
                        "PID": 790,
                        "PPID": 1,
                        "Path": "/usr/lib/accountsservice",
                        "Process Name": "accounts-daemon",
                        "Username": "root"
                    },
                    {
                        "PID": 802,
                        "PPID": 1,
                        "Path": "/usr/sbin",
                        "Process Name": "atd",
                        "Username": "daemon"
                    },
                    {
                        "PID": 803,
                        "PPID": 1,
                        "Path": "/bin",
                        "Process Name": "bash",
                        "Username": "velocir+"
                    },
                    {
                        "PID": 807,
                        "PPID": 1,
                        "Path": "/usr/sbin",
                        "Process Name": "rsyslogd",
                        "Username": "syslog"
                    },
                    {
                        "PID": 824,
                        "PPID": 1,
                        "Path": "/usr/sbin",
                        "Process Name": "acpid",
                        "Username": "root"
                    },
                    {
                        "PID": 825,
                        "PPID": 1,
                        "Path": "/usr/lib/snapd",
                        "Process Name": "snapd",
                        "Username": "root"
                    },
                    {
                        "PID": 827,
                        "PPID": 1,
                        "Path": "/usr/bin",
                        "Process Name": "dbus-daemon",
                        "Username": "message+"
                    },
                    {
                        "PID": 832,
                        "PPID": 803,
                        "Path": "/usr/local/bin",
                        "Process Name": "velociraptor.bin",
                        "Username": "velocir+"
                    },
                    {
                        "PID": 844,
                        "PPID": 1,
                        "Path": "/usr/sbin",
                        "Process Name": "cron",
                        "Username": "root"
                    },
                    {
                        "PID": 847,
                        "PPID": 1,
                        "Path": "/lib/systemd",
                        "Process Name": "systemd-logind",
                        "Username": "root"
                    },
                    {
                        "PID": 852,
                        "PPID": 1,
                        "Path": "/usr/bin",
                        "Process Name": "python3",
                        "Username": "root"
                    },
                    {
                        "PID": 853,
                        "PPID": 1,
                        "Path": "/usr/bin",
                        "Process Name": "lxcfs",
                        "Username": "root"
                    },
                    {
                        "PID": 863,
                        "PPID": 1,
                        "Path": "/usr/lib/policykit-1",
                        "Process Name": "polkitd",
                        "Username": "root"
                    },
                    {
                        "PID": 867,
                        "PPID": 1,
                        "Path": "/usr/bin",
                        "Process Name": "python3",
                        "Username": "root"
                    },
                    {
                        "PID": 875,
                        "PPID": 1,
                        "Path": "/sbin",
                        "Process Name": "agetty",
                        "Username": "root"
                    },
                    {
                        "PID": 884,
                        "PPID": 1,
                        "Path": "/sbin",
                        "Process Name": "agetty",
                        "Username": "root"
                    },
                    {
                        "PID": 1370,
                        "PPID": 1,
                        "Path": "/usr/bin",
                        "Process Name": "python3",
                        "Username": "root"
                    },
                    {
                        "PID": 1432,
                        "PPID": 1,
                        "Path": "/lib/systemd",
                        "Process Name": "systemd-hostnamed",
                        "Username": "root"
                    },
                    {
                        "PID": 2288,
                        "PPID": 879,
                        "Process Name": "sshd",
                        "Username": "root"
                    },
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 22,
                                "Transport Protocol": "TCP"
                            }
                        ],
                        "PID": 879,
                        "PPID": 1,
                        "Path": "/usr/sbin",
                        "Process Name": "sshd",
                        "Username": "root"
                    },
                    {
                        "Connections": [
                            {
                                "local_address": "127.0.0.53",
                                "local_port": 53,
                                "Transport Protocol": "TCP"
                            },
                            {
                                "local_address": "127.0.0.53",
                                "local_port": 53,
                                "Transport Protocol": "UDP"
                            }
                        ],
                        "PID": 656,
                        "PPID": 1,
                        "Path": "/lib/systemd",
                        "Process Name": "systemd-resolved",
                        "Username": "systemd+"
                    },
                    {
                        "Connections": [
                            {
                                "local_address": "10.0.11.88",
                                "local_port": 68,
                                "Transport Protocol": "UDP"
                            }
                        ],
                        "PID": 634,
                        "PPID": 1,
                        "Path": "/lib/systemd",
                        "Process Name": "systemd-networkd",
                        "Username": "systemd+"
                    }
                ],
                "System info": {
                    "Architecture": "x64",
                    "OSDistribution": "UBUNTU",
                    "OSType": "LINUX",
                    "OSVersion": "U18_04_3"
                },
                "User Info": [
                    {
                        "Groups": [
                            {
                                "GID": 0,
                                "Group Name": "root"
                            }
                        ],
                        "UID": 0,
                        "Username": "root"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 1000,
                                "Group Name": "ubuntu"
                            }
                        ],
                        "UID": 1000,
                        "Username": "ubuntu"
                    }
                ]
            },
            "Enterprise0": {
                "AWS_Info": [

                ],
                "info": {
                    "Enterprise0": {
                        "Interfaces": "All"
                    }
                },
                "ConfidentialityValue": "Medium",
                "AvailabilityValue": "Medium",
                "Processes": [
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 22,
                                "Transport Protocol": "TCP"
                            }
                        ],
                        "PID": 1091,
                        "PPID": 1,
                        "Path": "/usr/sbin",
                        "Process Name": "sshd",
                        "Username": "root"
                    }
                ],
                "System info": {
                    "Architecture": "x64",
                    "OSDistribution": "UBUNTU",
                    "OSType": "LINUX",
                    "OSVersion": "U18_04_3"
                },
                "User Info": [
                    {
                        "Groups": [
                            {
                                "GID": 0,
                                "Group Name": "root"
                            }
                        ],
                        "UID": 0,
                        "Username": "root"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 33,
                                "Group Name": "www-data"
                            }
                        ],
                        "UID": 33,
                        "Username": "www-data"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 1001,
                                "Group Name": "pi"
                            }
                        ],
                        "UID": 1001,
                        "Username": "pi",
                        "Bruteforceable": True,
                        "Password": "raspberry"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 1000,
                                "Group Name": "ubuntu"
                            }
                        ],
                        "UID": 1000,
                        "Username": "ubuntu"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 1001,
                                "Group Name": "GreenAgent"
                            }
                        ],
                        "UID": 1001,
                        "Username": "GreenAgent"
                    }
                ]
            },
            "Enterprise1": {
                "AWS_Info": [

                ],
                "info": {
                    "Enterprise1": {
                        "Interfaces": "All"
                    }
                },
                "ConfidentialityValue": "Medium",
                "AvailabilityValue": "Medium",
                "Processes": [
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 22
                            }
                        ],
                        "PID": 3368,
                        "PPID": 5956,
                        "Path": "C:\\Program Files\\OpenSSH\\usr\\sbin",
                        "Process Name": "sshd.exe",
                        "Username": "sshd_server"
                    },
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 135
                            }
                        ],
                        "PID": 832,
                        "PPID": 4,
                        "Process Name": "svchost.exe",
                        "Username": "SYSTEM"
                    },
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 3389
                            }
                        ],
                        "PID": 4400,
                        "PPID": 4,
                        "Process Name": "svchost.exe",
                        "Process Type": "rdp",
                        "Username": "SYSTEM"
                    },
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 445
                            },
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 139
                            }
                        ],
                        "PID": 4,
                        "PPID": 372,
                        "Process Name": "smss.exe",
                        "Username": "SYSTEM"
                    },
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 80
                            },
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 443
                            }
                        ],
                        "PID": 3404,
                        "PPID": 4,
                        "Username": "NetworkService",
                        "Process Name": "tomcat8.exe",
                        "Process Type": "webserver",
                        "Properties": [
                            "rfi"
                        ]
                    }
                ],
                "System info": {
                    "Architecture": "x64",
                    "OSDistribution": "WINDOWS_SVR_2008",
                    "OSType": "WINDOWS",
                    "OSVersion": "W6_1_7601"
                },
                "User Info": [
                    {
                        "Groups": [
                            {
                                "GID": 0,
                                "Group Name": "ADMINISTRATORS"
                            }
                        ],
                        "UID": "S-1-5-21-1983491181-1743339912-3520046837-500",
                        "Username": "Administrator"
                    },
                    {
                        "UID": "S-1-5-21-1983491181-1743339912-3520046837-1019",
                        "Username": "GreenAgent"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 0,
                                "Group Name": "ADMINISTRATORS"
                            }
                        ],
                        "UID": "S-1-5-21-1983491181-1743339912-3520046837-1000",
                        "Username": "vagrant",
                        "Password": "vagrant",
                        "Bruteforceable": True
                    },
                    {
                        "Username": "SYSTEM"
                    }
                ]
            },
            "Enterprise2": {
                "AWS_Info": [

                ],
                "info": {
                    "Enterprise2": {
                        "Interfaces": "All"
                    },
                    "Op_Server0": {
                        "Interfaces": "IP Address"
                    }
                },
                "ConfidentialityValue": "Medium",
                "AvailabilityValue": "Medium",
                "Processes": [
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 22
                            }
                        ],
                        "PID": 3368,
                        "PPID": 5956,
                        "Path": "C:\\Program Files\\OpenSSH\\usr\\sbin",
                        "Process Name": "sshd.exe",
                        "Username": "sshd_server"
                    },
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 135
                            }
                        ],
                        "PID": 832,
                        "PPID": 4,
                        "Process Name": "svchost.exe",
                        "Username": "SYSTEM"
                    },
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 3389
                            }
                        ],
                        "PID": 4400,
                        "PPID": 4,
                        "Process Name": "svchost.exe",
                        "Process Type": "rdp",
                        "Username": "SYSTEM"
                    },
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 445
                            },
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 139
                            }
                        ],
                        "PID": 4,
                        "PPID": 372,
                        "Process Name": "smss.exe",
                        "Username": "SYSTEM"
                    },
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 80
                            },
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 443
                            }
                        ],
                        "PID": 3404,
                        "PPID": 4,
                        "Username": "NetworkService",
                        "Process Name": "tomcat8.exe",
                        "Process Type": "webserver",
                        "Properties": [
                            "rfi"
                        ]
                    }
                ],
                "System info": {
                    "Architecture": "x64",
                    "OSDistribution": "WINDOWS_SVR_2008",
                    "OSType": "WINDOWS",
                    "OSVersion": "W6_1_7601"
                },
                "User Info": [
                    {
                        "Groups": [
                            {
                                "GID": 0,
                                "Group Name": "ADMINISTRATORS"
                            }
                        ],
                        "UID": "S-1-5-21-1983491181-1743339912-3520046837-500",
                        "Username": "Administrator"
                    },
                    {
                        "UID": "S-1-5-21-1983491181-1743339912-3520046837-1019",
                        "Username": "GreenAgent"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 0,
                                "Group Name": "ADMINISTRATORS"
                            }
                        ],
                        "UID": "S-1-5-21-1983491181-1743339912-3520046837-1000",
                        "Username": "vagrant",
                        "Password": "vagrant",
                        "Bruteforceable": True
                    },
                    {
                        "Username": "SYSTEM"
                    }
                ]
            },
            "Op_Host0": {
                "AWS_Info": [

                ],
                "info": {
                    "Op_Host0": {
                        "Interfaces": "All"
                    }
                },
                "Processes": [
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 22,
                                "Transport Protocol": "TCP"
                            }
                        ],
                        "PID": 1091,
                        "PPID": 1,
                        "Path": "/usr/sbin",
                        "Process Name": "sshd",
                        "Username": "root"
                    }
                ],
                "System info": {
                    "Architecture": "x64",
                    "OSDistribution": "UBUNTU",
                    "OSType": "LINUX",
                    "OSVersion": "U18_04_3"
                },
                "User Info": [
                    {
                        "Groups": [
                            {
                                "GID": 0,
                                "Group Name": "root"
                            }
                        ],
                        "UID": 0,
                        "Username": "root"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 33,
                                "Group Name": "www-data"
                            }
                        ],
                        "UID": 33,
                        "Username": "www-data"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 1001,
                                "Group Name": "pi"
                            }
                        ],
                        "UID": 1001,
                        "Username": "pi",
                        "Bruteforceable": True,
                        "Password": "raspberry"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 1000,
                                "Group Name": "ubuntu"
                            }
                        ],
                        "UID": 1000,
                        "Username": "ubuntu"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 1001,
                                "Group Name": "GreenAgent"
                            }
                        ],
                        "UID": 1001,
                        "Username": "GreenAgent"
                    }
                ]
            },
            "Op_Host1": {
                "AWS_Info": [

                ],
                "info": {
                    "Op_Host1": {
                        "Interfaces": "All"
                    }
                },
                "Processes": [
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 22,
                                "Transport Protocol": "TCP"
                            }
                        ],
                        "PID": 1091,
                        "PPID": 1,
                        "Path": "/usr/sbin",
                        "Process Name": "sshd",
                        "Username": "root"
                    }
                ],
                "System info": {
                    "Architecture": "x64",
                    "OSDistribution": "UBUNTU",
                    "OSType": "LINUX",
                    "OSVersion": "U18_04_3"
                },
                "User Info": [
                    {
                        "Groups": [
                            {
                                "GID": 0,
                                "Group Name": "root"
                            }
                        ],
                        "UID": 0,
                        "Username": "root"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 33,
                                "Group Name": "www-data"
                            }
                        ],
                        "UID": 33,
                        "Username": "www-data"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 1001,
                                "Group Name": "pi"
                            }
                        ],
                        "UID": 1001,
                        "Username": "pi",
                        "Bruteforceable": True,
                        "Password": "raspberry"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 1000,
                                "Group Name": "ubuntu"
                            }
                        ],
                        "UID": 1000,
                        "Username": "ubuntu"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 1001,
                                "Group Name": "GreenAgent"
                            }
                        ],
                        "UID": 1001,
                        "Username": "GreenAgent"
                    }
                ]
            },
            "Op_Host2": {
                "AWS_Info": [

                ],
                "info": {
                    "Op_Host2": {
                        "Interfaces": "All"
                    }
                },
                "Processes": [
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 22,
                                "Transport Protocol": "TCP"
                            }
                        ],
                        "PID": 1091,
                        "PPID": 1,
                        "Path": "/usr/sbin",
                        "Process Name": "sshd",
                        "Username": "root"
                    }
                ],
                "System info": {
                    "Architecture": "x64",
                    "OSDistribution": "UBUNTU",
                    "OSType": "LINUX",
                    "OSVersion": "U18_04_3"
                },
                "User Info": [
                    {
                        "Groups": [
                            {
                                "GID": 0,
                                "Group Name": "root"
                            }
                        ],
                        "UID": 0,
                        "Username": "root"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 33,
                                "Group Name": "www-data"
                            }
                        ],
                        "UID": 33,
                        "Username": "www-data"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 1001,
                                "Group Name": "pi"
                            }
                        ],
                        "UID": 1001,
                        "Username": "pi",
                        "Bruteforceable": True,
                        "Password": "raspberry"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 1000,
                                "Group Name": "ubuntu"
                            }
                        ],
                        "UID": 1000,
                        "Username": "ubuntu"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 1001,
                                "Group Name": "GreenAgent"
                            }
                        ],
                        "UID": 1001,
                        "Username": "GreenAgent"
                    }
                ]
            },
            "Op_Server0": {
                "AWS_Info": [

                ],
                "info": {
                    "Op_Server0": {
                        "Interfaces": "All",
                        "Services": [
                            "OTService"
                        ]
                    }
                },
                "ConfidentialityValue": "Medium",
                "AvailabilityValue": "High",
                "Processes": [
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 22,
                                "Transport Protocol": "TCP"
                            }
                        ],
                        "PID": 1091,
                        "PPID": 1,
                        "Path": "/usr/sbin",
                        "Process Name": "sshd",
                        "Username": "root"
                    },
                    {
                        "PID": 1043,
                        "PPID": 1,
                        "Path": "/root",
                        "Process Name": "OTService",
                        "Username": "root"
                    }
                ],
                "System info": {
                    "Architecture": "x64",
                    "OSDistribution": "UBUNTU",
                    "OSType": "LINUX",
                    "OSVersion": "U18_04_3"
                },
                "Services": {
                    "OTService": {
                        "active": True,
                        "PID": 1043
                    }
                },
                "User Info": [
                    {
                        "Groups": [
                            {
                                "GID": 0,
                                "Group Name": "root"
                            }
                        ],
                        "UID": 0,
                        "Username": "root"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 33,
                                "Group Name": "www-data"
                            }
                        ],
                        "UID": 33,
                        "Username": "www-data"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 1001,
                                "Group Name": "pi"
                            }
                        ],
                        "UID": 1001,
                        "Username": "pi",
                        "Bruteforceable": True,
                        "Password": "raspberry"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 1000,
                                "Group Name": "ubuntu"
                            }
                        ],
                        "UID": 1000,
                        "Username": "ubuntu"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 1001,
                                "Group Name": "GreenAgent"
                            }
                        ],
                        "UID": 1001,
                        "Username": "GreenAgent"
                    }
                ]
            },
            "User0": {
                "AWS_Info": [

                ],
                "info": {
                    "User0": {
                        "Interfaces": "All"
                    }
                },
                "ConfidentialityValue": "None",
                "AvailabilityValue": "None",
                "Processes": [
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 22
                            }
                        ],
                        "PID": 3368,
                        "PPID": 5956,
                        "Path": "C:\\Program Files\\OpenSSH\\usr\\sbin",
                        "Process Name": "sshd.exe",
                        "Username": "sshd_server"
                    },
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 21
                            }
                        ],
                        "PID": 3344,
                        "PPID": 5566,
                        "Path": "C:\\Program Files\\Femitter",
                        "Process Name": "femitter.exe",
                        "Process Type": "femitter",
                        "Username": "SYSTEM"
                    }
                ],
                "System info": {
                    "Architecture": "x64",
                    "OSDistribution": "WINDOWS_SVR_2008",
                    "OSType": "WINDOWS",
                    "OSVersion": "W6_1_7601"
                },
                "User Info": [
                    {
                        "Groups": [
                            {
                                "GID": 0,
                                "Group Name": "ADMINISTRATORS"
                            }
                        ],
                        "UID": "S-1-5-21-1983491181-1743339912-3520046837-500",
                        "Username": "Administrator"
                    },
                    {
                        "UID": "S-1-5-21-1983491181-1743339912-3520046837-1019",
                        "Username": "GreenAgent"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 0,
                                "Group Name": "ADMINISTRATORS"
                            }
                        ],
                        "UID": "S-1-5-21-1983491181-1743339912-3520046837-1000",
                        "Username": "vagrant",
                        "Password": "vagrant",
                        "Bruteforceable": True
                    },
                    {
                        "Username": "SYSTEM"
                    }
                ]
            },
            "User1": {
                "AWS_Info": [

                ],
                "info": {
                    "Enterprise1": {
                        "Interfaces": "IP Address"
                    },
                    "User1": {
                        "Interfaces": "All"
                    }
                },
                "AvailabilityValue": "None",
                "Processes": [
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 22
                            }
                        ],
                        "PID": 3368,
                        "PPID": 5956,
                        "Path": "C:\\Program Files\\OpenSSH\\usr\\sbin",
                        "Process Name": "sshd.exe",
                        "Username": "sshd_server"
                    },
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 21
                            }
                        ],
                        "PID": 3344,
                        "PPID": 5566,
                        "Path": "C:\\Program Files\\Femitter",
                        "Process Name": "femitter.exe",
                        "Process Type": "femitter",
                        "Username": "SYSTEM"
                    }
                ],
                "System info": {
                    "Architecture": "x64",
                    "OSDistribution": "WINDOWS_SVR_2008",
                    "OSType": "WINDOWS",
                    "OSVersion": "W6_1_7601"
                },
                "User Info": [
                    {
                        "Groups": [
                            {
                                "GID": 0,
                                "Group Name": "ADMINISTRATORS"
                            }
                        ],
                        "UID": "S-1-5-21-1983491181-1743339912-3520046837-500",
                        "Username": "Administrator"
                    },
                    {
                        "UID": "S-1-5-21-1983491181-1743339912-3520046837-1019",
                        "Username": "GreenAgent"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 0,
                                "Group Name": "ADMINISTRATORS"
                            }
                        ],
                        "UID": "S-1-5-21-1983491181-1743339912-3520046837-1000",
                        "Username": "vagrant",
                        "Password": "vagrant",
                        "Bruteforceable": True
                    },
                    {
                        "Username": "SYSTEM"
                    }
                ]
            },
            "User2": {
                "AWS_Info": [

                ],
                "info": {
                    "Enterprise1": {
                        "Interfaces": "IP Address"
                    },
                    "User2": {
                        "Interfaces": "All"
                    }
                },
                "AvailabilityValue": "None",
                "Processes": [
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 445
                            },
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 139
                            }
                        ],
                        "PID": 4,
                        "PPID": 372,
                        "Process Name": "smss.exe",
                        "Username": "SYSTEM",
                        "Process Type": "smb"
                    },
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 135
                            }
                        ],
                        "PID": 832,
                        "PPID": 4,
                        "Process Name": "svchost.exe",
                        "Username": "SYSTEM"
                    },
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 3389
                            }
                        ],
                        "PID": 4400,
                        "PPID": 4,
                        "Process Name": "svchost.exe",
                        "Process Type": "rdp",
                        "Username": "NetworkService"
                    }
                ],
                "System info": {
                    "Architecture": "x64",
                    "OSDistribution": "WINDOWS_SVR_2008",
                    "OSType": "WINDOWS",
                    "OSVersion": "W6_1_7601"
                },
                "User Info": [
                    {
                        "Groups": [
                            {
                                "GID": 0,
                                "Group Name": "ADMINISTRATORS"
                            }
                        ],
                        "UID": "S-1-5-21-1983491181-1743339912-3520046837-500",
                        "Username": "Administrator"
                    },
                    {
                        "UID": "S-1-5-21-1983491181-1743339912-3520046837-1019",
                        "Username": "GreenAgent"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 0,
                                "Group Name": "ADMINISTRATORS"
                            }
                        ],
                        "UID": "S-1-5-21-1983491181-1743339912-3520046837-1000",
                        "Username": "vagrant",
                        "Password": "vagrant",
                        "Bruteforceable": True
                    },
                    {
                        "Username": "SYSTEM"
                    }
                ]
            },
            "User3": {
                "AWS_Info": [

                ],
                "info": {
                    "Enterprise0": {
                        "Interfaces": "IP Address"
                    },
                    "User3": {
                        "Interfaces": "All"
                    }
                },
                "AvailabilityValue": "None",
                "Processes": [
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 80,
                                "Transport Protocol": "TCP"
                            }
                        ],
                        "PID": 1100,
                        "PPID": 1,
                        "Path": "/usr/sbin",
                        "Process Name": "apache2",
                        "Username": "www-data",
                        "Process Type": "webserver",
                        "Properties": "rfi"
                    },
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 3389,
                                "Transport Protocol": "TCP"
                            }
                        ],
                        "PID": 1101,
                        "PPID": 1,
                        "Path": "/etc/init.d",
                        "Process Name": "mysql",
                        "Username": "root"
                    },
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 443,
                                "Transport Protocol": "TCP"
                            }
                        ],
                        "PID": 1100,
                        "PPID": 1,
                        "Path": "/usr/sbin",
                        "Process Name": "apache2",
                        "Username": "www-data",
                        "Process Type": "webserver",
                        "Properties": "rfi"
                    },
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 25,
                                "Transport Protocol": "TCP"
                            }
                        ],
                        "PID": 1102,
                        "PPID": 1,
                        "Path": "/usr/sbin",
                        "Process Name": "smtp",
                        "Username": "root",
                        "Process Type": "smtp",
                        "Process Version": "haraka 2.7.0"
                    }
                ],
                "System info": {
                    "Architecture": "x64",
                    "OSDistribution": "UBUNTU",
                    "OSType": "LINUX",
                    "OSVersion": "U18_04_3"
                },
                "User Info": [
                    {
                        "Groups": [
                            {
                                "GID": 0,
                                "Group Name": "root"
                            }
                        ],
                        "UID": 0,
                        "Username": "root"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 33,
                                "Group Name": "www-data"
                            }
                        ],
                        "UID": 33,
                        "Username": "www-data"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 1001,
                                "Group Name": "pi"
                            }
                        ],
                        "UID": 1001,
                        "Username": "pi",
                        "Bruteforceable": True,
                        "Password": "raspberry"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 1000,
                                "Group Name": "ubuntu"
                            }
                        ],
                        "UID": 1000,
                        "Username": "ubuntu"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 1001,
                                "Group Name": "GreenAgent"
                            }
                        ],
                        "UID": 1001,
                        "Username": "GreenAgent"
                    }
                ]
            },
            "User4": {
                "AWS_Info": [

                ],
                "info": {
                    "Enterprise0": {
                        "Interfaces": "IP Address"
                    },
                    "User4": {
                        "Interfaces": "All"
                    }
                },
                "AvailabilityValue": "None",
                "Processes": [
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 22,
                                "Transport Protocol": "TCP"
                            }
                        ],
                        "PID": 1091,
                        "PPID": 1,
                        "Path": "/usr/sbin",
                        "Process Name": "sshd",
                        "Username": "root"
                    },
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 80,
                                "Transport Protocol": "TCP"
                            }
                        ],
                        "PID": 1100,
                        "PPID": 1,
                        "Path": "/usr/sbin",
                        "Process Name": "apache2",
                        "Username": "www-data",
                        "Process Type": "webserver",
                        "Properties": "rfi"
                    },
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 3390,
                                "Transport Protocol": "TCP"
                            }
                        ],
                        "PID": 1101,
                        "PPID": 1,
                        "Path": "/etc/init.d",
                        "Process Name": "mysql",
                        "Username": "root",
                        "Properties": "None"
                    },
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 443,
                                "Transport Protocol": "TCP"
                            }
                        ],
                        "PID": 1100,
                        "PPID": 1,
                        "Path": "/usr/sbin",
                        "Process Name": "apache2",
                        "Username": "www-data",
                        "Process Type": "webserver",
                        "Properties": "rfi"
                    },
                    {
                        "Connections": [
                            {
                                "local_address": "0.0.0.0",
                                "local_port": 25,
                                "Transport Protocol": "TCP"
                            }
                        ],
                        "PID": 1102,
                        "PPID": 1,
                        "Path": "/usr/sbin",
                        "Process Name": "smtp",
                        "Username": "root",
                        "Process Type": "smtp",
                        "Process Version": "haraka 2.7.0"
                    }
                ],
                "System info": {
                    "Architecture": "x64",
                    "OSDistribution": "UBUNTU",
                    "OSType": "LINUX",
                    "OSVersion": "U18_04_3"
                },
                "User Info": [
                    {
                        "Groups": [
                            {
                                "GID": 0,
                                "Group Name": "root"
                            }
                        ],
                        "UID": 0,
                        "Username": "root"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 33,
                                "Group Name": "www-data"
                            }
                        ],
                        "UID": 33,
                        "Username": "www-data"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 1001,
                                "Group Name": "pi"
                            }
                        ],
                        "UID": 1001,
                        "Username": "pi",
                        "Bruteforceable": True,
                        "Password": "raspberry"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 1000,
                                "Group Name": "ubuntu"
                            }
                        ],
                        "UID": 1000,
                        "Username": "ubuntu"
                    },
                    {
                        "Groups": [
                            {
                                "GID": 1001,
                                "Group Name": "GreenAgent"
                            }
                        ],
                        "UID": 1001,
                        "Username": "GreenAgent"
                    }
                ]
            }
        },
        "Subnets": {
            "Enterprise": {
                "Hosts": [
                    "Enterprise0",
                    "Enterprise1",
                    "Enterprise2",
                    "Defender"
                ],
                "NACLs": {
                    "all": {
                        "in": "all",
                        "out": "all"
                    }
                },
                "Size": 3
            },
            "Operational": {
                "Hosts": [
                    "Op_Server0",
                    "Op_Host0",
                    "Op_Host1",
                    "Op_Host2"
                ],
                "NACLs": {
                    "User": {
                        "in": "None",
                        "out": "all"
                    },
                    "all": {
                        "in": "all",
                        "out": "all"
                    }
                },
                "Size": 4
            },
            "User": {
                "Hosts": [
                    "User0",
                    "User1",
                    "User2",
                    "User3",
                    "User4"
                ],
                "NACLs": {
                    "all": {
                        "in": "all",
                        "out": "all"
                    }
                },
                "Size": 5
            }
        }
    }
