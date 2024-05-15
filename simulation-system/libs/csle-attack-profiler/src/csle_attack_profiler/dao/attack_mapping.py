from typing import Dict, Set, Union
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id \
    import EmulationAttackerActionId
from csle_attack_profiler.dao.techniques import Techniques, SubTechniques


class EmulationAttackerMapping:
    """
    Maps EmulationAttackerActionId's to tactics and techniques
    """

    @staticmethod
    def get_attack_info(id: EmulationAttackerActionId) \
            -> Union[Dict[str, Union[Set[Techniques], Set[SubTechniques]]], None]:
        """
        Maps id's to tactics and techniques

        :param id: the id of the attack
        :return: the attack info for the id
        """

        mapping: Dict[EmulationAttackerActionId, Union[Dict[str, Union[Set[Techniques], Set[SubTechniques]]], None]] = {
            EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_HOST_INFORMATION,
                               Techniques.NETWORK_SERVICE_DISCOVERY}
            },
            EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_ALL: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_HOST_INFORMATION,
                               Techniques.NETWORK_SERVICE_DISCOVERY}
            },
            EmulationAttackerActionId.PING_SCAN_HOST: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_HOST_INFORMATION,
                               Techniques.NETWORK_SERVICE_DISCOVERY}
            },
            EmulationAttackerActionId.PING_SCAN_ALL: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_HOST_INFORMATION,
                               Techniques.NETWORK_SERVICE_DISCOVERY}
            },
            EmulationAttackerActionId.UDP_PORT_SCAN_HOST: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_HOST_INFORMATION,
                               Techniques.NETWORK_SERVICE_DISCOVERY}
            },
            EmulationAttackerActionId.UDP_PORT_SCAN_ALL: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_HOST_INFORMATION,
                               Techniques.NETWORK_SERVICE_DISCOVERY}
            },
            EmulationAttackerActionId.TCP_CON_NON_STEALTH_SCAN_HOST: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_HOST_INFORMATION,
                               Techniques.NETWORK_SERVICE_DISCOVERY}
            },
            EmulationAttackerActionId.TCP_CON_NON_STEALTH_SCAN_ALL: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_HOST_INFORMATION,
                               Techniques.NETWORK_SERVICE_DISCOVERY}
            },
            EmulationAttackerActionId.TCP_FIN_SCAN_HOST: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_HOST_INFORMATION,
                               Techniques.NETWORK_SERVICE_DISCOVERY}
            },
            EmulationAttackerActionId.TCP_FIN_SCAN_ALL: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_HOST_INFORMATION,
                               Techniques.NETWORK_SERVICE_DISCOVERY}
            },
            EmulationAttackerActionId.TCP_NULL_SCAN_HOST: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_HOST_INFORMATION,
                               Techniques.NETWORK_SERVICE_DISCOVERY}
            },
            EmulationAttackerActionId.TCP_NULL_SCAN_ALL: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_HOST_INFORMATION,
                               Techniques.NETWORK_SERVICE_DISCOVERY}
            },
            EmulationAttackerActionId.TCP_XMAS_TREE_SCAN_HOST: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_HOST_INFORMATION,
                               Techniques.NETWORK_SERVICE_DISCOVERY}
            },
            EmulationAttackerActionId.TCP_XMAS_TREE_SCAN_ALL: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_HOST_INFORMATION,
                               Techniques.NETWORK_SERVICE_DISCOVERY}
            },
            EmulationAttackerActionId.OS_DETECTION_SCAN_HOST: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_HOST_INFORMATION,
                               Techniques.NETWORK_SERVICE_DISCOVERY}
            },
            EmulationAttackerActionId.OS_DETECTION_SCAN_ALL: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_HOST_INFORMATION,
                               Techniques.NETWORK_SERVICE_DISCOVERY}
            },

            EmulationAttackerActionId.VULSCAN_HOST: {
                "techniques": {Techniques.GATHER_VICTIM_HOST_INFORMATION,
                               Techniques.SOFTWARE_DISCOVERY},
                "subtechniques": {SubTechniques.SOFTWARE}
            },
            EmulationAttackerActionId.VULSCAN_ALL: {
                "techniques": {Techniques.GATHER_VICTIM_HOST_INFORMATION,
                               Techniques.SOFTWARE_DISCOVERY},
                "subtechniques": {SubTechniques.SOFTWARE}
            },
            EmulationAttackerActionId.NMAP_VULNERS_HOST: {
                "techniques": {Techniques.GATHER_VICTIM_HOST_INFORMATION,
                               Techniques.SOFTWARE_DISCOVERY},
                "subtechniques": {SubTechniques.SOFTWARE}
            },
            EmulationAttackerActionId.NMAP_VULNERS_ALL: {
                "techniques": {Techniques.GATHER_VICTIM_HOST_INFORMATION,
                               Techniques.SOFTWARE_DISCOVERY},
                "subtechniques": {SubTechniques.SOFTWARE}
            },

            EmulationAttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST: {
                "techniques": {Techniques.BRUTE_FORCE,
                               Techniques.VALID_ACCOUNTS},
                "subtechniques": {SubTechniques.CREDENTIAL_STUFFING,
                                  SubTechniques.DEFAULT_ACCOUNTS}
            },
            EmulationAttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_ALL: {
                "techniques": {Techniques.BRUTE_FORCE,
                               Techniques.VALID_ACCOUNTS},
                "subtechniques": {SubTechniques.CREDENTIAL_STUFFING,
                                  SubTechniques.DEFAULT_ACCOUNTS}
            },
            EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST: {
                "techniques": {Techniques.BRUTE_FORCE,
                               Techniques.VALID_ACCOUNTS},
                "subtechniques": {SubTechniques.CREDENTIAL_STUFFING,
                                  SubTechniques.DEFAULT_ACCOUNTS}
            },
            EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_ALL: {
                "techniques": {Techniques.BRUTE_FORCE,
                               Techniques.VALID_ACCOUNTS},
                "subtechniques": {SubTechniques.CREDENTIAL_STUFFING,
                                  SubTechniques.DEFAULT_ACCOUNTS}
            },
            EmulationAttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST: {
                "techniques": {Techniques.BRUTE_FORCE,
                               Techniques.VALID_ACCOUNTS},
                "subtechniques": {SubTechniques.CREDENTIAL_STUFFING,
                                  SubTechniques.DEFAULT_ACCOUNTS}
            },
            EmulationAttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_ALL: {
                "techniques": {Techniques.BRUTE_FORCE,
                               Techniques.VALID_ACCOUNTS},
                "subtechniques": {SubTechniques.CREDENTIAL_STUFFING,
                                  SubTechniques.DEFAULT_ACCOUNTS}
            },
            EmulationAttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST: {
                "techniques": {Techniques.BRUTE_FORCE,
                               Techniques.VALID_ACCOUNTS},
                "subtechniques": {SubTechniques.CREDENTIAL_STUFFING,
                                  SubTechniques.DEFAULT_ACCOUNTS}
            },
            EmulationAttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_ALL: {
                "techniques": {Techniques.BRUTE_FORCE,
                               Techniques.VALID_ACCOUNTS},
                "subtechniques": {SubTechniques.CREDENTIAL_STUFFING,
                                  SubTechniques.DEFAULT_ACCOUNTS}
            },
            EmulationAttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST: {
                "techniques": {Techniques.BRUTE_FORCE,
                               Techniques.VALID_ACCOUNTS},
                "subtechniques": {SubTechniques.CREDENTIAL_STUFFING,
                                  SubTechniques.DEFAULT_ACCOUNTS}
            },
            EmulationAttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_ALL: {
                "techniques": {Techniques.BRUTE_FORCE,
                               Techniques.VALID_ACCOUNTS},
                "subtechniques": {SubTechniques.CREDENTIAL_STUFFING,
                                  SubTechniques.DEFAULT_ACCOUNTS}
            },
            EmulationAttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST: {
                "techniques": {Techniques.BRUTE_FORCE,
                               Techniques.VALID_ACCOUNTS},
                "subtechniques": {SubTechniques.CREDENTIAL_STUFFING,
                                  SubTechniques.DEFAULT_ACCOUNTS},
            },
            EmulationAttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_ALL: {
                "techniques": {Techniques.BRUTE_FORCE,
                               Techniques.VALID_ACCOUNTS},
                "subtechniques": {SubTechniques.CREDENTIAL_STUFFING,
                                  SubTechniques.DEFAULT_ACCOUNTS},
            },
            EmulationAttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST: {
                "techniques": {Techniques.BRUTE_FORCE,
                               Techniques.VALID_ACCOUNTS},
                "subtechniques": {SubTechniques.CREDENTIAL_STUFFING,
                                  SubTechniques.DEFAULT_ACCOUNTS}
            },
            EmulationAttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_ALL: {
                "techniques": {Techniques.BRUTE_FORCE,
                               Techniques.VALID_ACCOUNTS},
                "subtechniques": {SubTechniques.CREDENTIAL_STUFFING,
                                  SubTechniques.DEFAULT_ACCOUNTS}
            },
            EmulationAttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST: {
                "techniques": {Techniques.BRUTE_FORCE,
                               Techniques.VALID_ACCOUNTS},
                "subtechniques": {SubTechniques.CREDENTIAL_STUFFING,
                                  SubTechniques.DEFAULT_ACCOUNTS}
            },
            EmulationAttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_ALL: {
                "techniques": {Techniques.BRUTE_FORCE,
                               Techniques.VALID_ACCOUNTS},
                "subtechniques": {SubTechniques.CREDENTIAL_STUFFING,
                                  SubTechniques.DEFAULT_ACCOUNTS}
            },
            EmulationAttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST: {
                "techniques": {Techniques.BRUTE_FORCE,
                               Techniques.VALID_ACCOUNTS},
                "subtechniques": {SubTechniques.CREDENTIAL_STUFFING,
                                  SubTechniques.DEFAULT_ACCOUNTS}
            },
            EmulationAttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_ALL: {
                "techniques": {Techniques.BRUTE_FORCE,
                               Techniques.VALID_ACCOUNTS},
                "subtechniques": {SubTechniques.CREDENTIAL_STUFFING,
                                  SubTechniques.DEFAULT_ACCOUNTS}
            },

            EmulationAttackerActionId.NETWORK_SERVICE_LOGIN: {
                "techniques": {Techniques.VALID_ACCOUNTS,
                               Techniques.REMOTE_SERVICES,
                               Techniques.EXTERNAL_REMOTE_SERVICES}
            },
            EmulationAttackerActionId.FIND_FLAG: {
                "techniques": {Techniques.DATA_FROM_LOCAL_SYSTEM}
            },
            EmulationAttackerActionId.NIKTO_WEB_HOST_SCAN: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_HOST_INFORMATION}
            },
            EmulationAttackerActionId.MASSCAN_HOST_SCAN: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_HOST_INFORMATION,
                               Techniques.NETWORK_SERVICE_DISCOVERY}
            },
            EmulationAttackerActionId.MASSCAN_ALL_SCAN: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_HOST_INFORMATION,
                               Techniques.NETWORK_SERVICE_DISCOVERY}
            },
            EmulationAttackerActionId.FIREWALK_HOST: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_NETWORK_INFORMATION}
            },
            EmulationAttackerActionId.FIREWALK_ALL: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_NETWORK_INFORMATION}
            },
            EmulationAttackerActionId.HTTP_ENUM_HOST: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_NETWORK_INFORMATION}
            },
            EmulationAttackerActionId.HTTP_ENUM_ALL: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_NETWORK_INFORMATION}
            },
            EmulationAttackerActionId.HTTP_GREP_HOST: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_IDENTITY_INFORMATION}
            },
            EmulationAttackerActionId.HTTP_GREP_ALL: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_IDENTITY_INFORMATION}
            },
            EmulationAttackerActionId.FINGER_HOST: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_HOST_INFORMATION}
            },
            EmulationAttackerActionId.FINGER_ALL: {
                "techniques": {Techniques.ACTIVE_SCANNING,
                               Techniques.GATHER_VICTIM_HOST_INFORMATION}
            },
            EmulationAttackerActionId.INSTALL_TOOLS: {
                "techniques": {Techniques.INGRESS_TOOL_TRANSFER}
            },
            EmulationAttackerActionId.SSH_BACKDOOR: {
                "techniques": {Techniques.COMPROMISE_CLIENT_SOFTWARE_BINARY,
                               Techniques.CREATE_ACCOUNT}
            },
            EmulationAttackerActionId.SAMBACRY_EXPLOIT: {
                "techniques": {Techniques.EXPLOIT_PUBLIC_FACING_APPLICATION,
                               Techniques.REMOTE_SERVICES,
                               Techniques.EXPLOITATION_OF_REMOTE_SERVICES,
                               Techniques.NATIVE_API}
            },
            EmulationAttackerActionId.SHELLSHOCK_EXPLOIT: {
                "techniques": {Techniques.EXPLOIT_PUBLIC_FACING_APPLICATION,
                               Techniques.EXPLOITATION_OF_REMOTE_SERVICES,
                               Techniques.COMMAND_AND_SCRIPTING_INTERPRETER}
            },
            EmulationAttackerActionId.DVWA_SQL_INJECTION: {
                "techniques": {Techniques.EXPLOIT_PUBLIC_FACING_APPLICATION,
                               Techniques.EXPLOITATION_FOR_CREDENTIAL_ACCESS,
                               Techniques.CREDENTIALS_FROM_PASSWORD_STORES}
            },
            EmulationAttackerActionId.CVE_2015_3306_EXPLOIT: {
                "techniques": {Techniques.EXPLOIT_PUBLIC_FACING_APPLICATION,
                               Techniques.VALID_ACCOUNTS,
                               Techniques.FALLBACK_CHANNELS,
                               Techniques.REMOTE_SERVICES},
            },
            EmulationAttackerActionId.CVE_2015_1427_EXPLOIT: {
                "techniques": {Techniques.EXPLOIT_PUBLIC_FACING_APPLICATION,
                               Techniques.EXPLOITATION_OF_REMOTE_SERVICES,
                               Techniques.COMMAND_AND_SCRIPTING_INTERPRETER,
                               Techniques.FALLBACK_CHANNELS}
            },
            EmulationAttackerActionId.CVE_2016_10033_EXPLOIT: {
                "techniques": {Techniques.EXPLOIT_PUBLIC_FACING_APPLICATION,
                               Techniques.COMMAND_AND_SCRIPTING_INTERPRETER,
                               Techniques.ABUSE_ELEVATION_CONTROL_MECHANISM,
                               Techniques.VALID_ACCOUNTS,
                               Techniques.FALLBACK_CHANNELS}
            },
            EmulationAttackerActionId.CVE_2010_0426_PRIV_ESC: {
                "techniques": {Techniques.ABUSE_ELEVATION_CONTROL_MECHANISM,
                               Techniques.COMMAND_AND_SCRIPTING_INTERPRETER,
                               Techniques.EXPLOITATION_FOR_PRIVILEGE_ESCALATION},
                "subtechniques": {SubTechniques.UNIX_SHELL}
            },
            EmulationAttackerActionId.CVE_2015_5602_PRIV_ESC: {
                "techniques": {Techniques.ABUSE_ELEVATION_CONTROL_MECHANISM,
                               Techniques.EXPLOITATION_FOR_PRIVILEGE_ESCALATION},
                "subtechniques": {SubTechniques.SUDO_AND_SUDO_CACHING}
            },
            EmulationAttackerActionId.CONTINUE: None,
            EmulationAttackerActionId.STOP: None

        }
        if id in mapping:
            return mapping[id]
        return None
