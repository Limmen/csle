from enum import Enum


class Techniques(Enum):
    """
    Techniques from MITRE ATT&CK, used to profile the attack
    """
    ACTIVE_SCANNING = "Active Scanning"
    GATHER_VICTIM_HOST_INFORMATION = "Gather Victim Host Information"
    GATHER_VICTIM_NETWORK_INFORMATION = "Gather Victim Network Information"
    GATHER_VICTIM_IDENTITY_INFORMATION = "Gather Victim Identity Information"
    NETWORK_SERVICE_DISCOVERY = "Network Service Discovery"
    SOFTWARE_DISCOVERY = "Software Discovery"
    BRUTE_FORCE = "Brute Force"
    VALID_ACCOUNTS = "Valid Accounts"
    DATA_FROM_LOCAL_SYSTEM = "Data from Local System"
    COMMAND_AND_SCRIPTING_INTERPRETER = "Command and Scripting Interpreter"
    LATERAL_TOOL_TRANSFER = "Lateral Tool Transfer"
    REMOTE_SERVICES = "Remote Services"
    CREATE_ACCOUNT = "Create Account"
    EXPLOIT_PUBLIC_FACING_APPLICATION = "Exploit Public-Facing Application"
    EXPLOITATION_FOR_PRIVILEGE_ESCALATION = "Exploitation for Privilege Escalation"
    EXPLOITATION_OF_REMOTE_SERVICES = "Exploitation of Remote Services"
    EXPLOITATION_FOR_CLIENT_EXECUTION = "Exploitation for Client Execution"
    CREDENTIALS_FROM_PASSWORD_STORES = "Credentials from Password Stores"
    FALLBACK_CHANNELS = "Fallback Channels"
    ABUSE_ELEVATION_CONTROL_MECHANISM = "Abuse Elevation Control Mechanism"
    INGRESS_TOOL_TRANSFER = "Ingress Tool Transfer"
    EXPLOITATION_FOR_CREDENTIAL_ACCESS = "Exploitation for Credential Access"
    COMPROMISE_CLIENT_SOFTWARE_BINARY = "Compromise Client Software Binary"
    EXTERNAL_REMOTE_SERVICES = "External Remote Services"
    NATIVE_API = "Native API"


class SubTechniques(Enum):
    """
    Sub-techniques from MITRE ATT&CK, used to profile the attack
    """
    SOFTWARE = "Software"
    CREDENTIAL_STUFFING = "Credential Stuffing"
    DEFAULT_ACCOUNTS = "Default Accounts"
    SSH = "SSH"
    UNIX_SHELL = "Unix Shell"
    SUDO_AND_SUDO_CACHING = "Sudo and Sudo Caching"
