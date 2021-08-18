"""
Constants for the pycr-ctf environment
"""

import re


class RENDERING:
    """
    Rendering constants
    """
    RECT_SIZE = 200
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    RED = (205, 55, 35)
    RED_ALPHA = (255, 0, 0, 255)
    GREEN = (0, 128, 0)
    GREEN_ALPHA = (0, 128, 0, 255)
    LIME = (0, 255, 0)
    BLUE_PURPLE = (102, 102, 153)
    #LIME = (0, 255, 0)
    BLACK_ALPHA = (0, 0, 0, 255)
    WHITE_ALPHA = (255, 255, 255, 255)
    RED_ALPHA = (128, 0, 0, 255)
    WHITE = (255, 255, 255)
    GREY = (220, 220, 220)
    RESOURCES_DIR = "resources"
    LINE_WIDTH = 1
    CAPTION = "PyCr-ctf"
    DEFAULT_WIDTH = 950
    DEFAULT_HEIGHT = 900
    TITLE = "PyCr-ctf"
    FIREWALL_SPRITE_NAME = "firewall.png"
    HACKER_SPRITE_NAME = "hacker.png"
    FLAG_SPRITE_NAME = "flag_1.png"
    LINK_COLORS = [(132,87,87), (153,0,153), (153,0,0), (204,204,255), (0,102,0), (102, 0, 102), (153,153,0),
                   (128,128,128), (51,153,255), (0, 153, 153), (204,255,153), (255, 204, 153), (255, 153, 153),
                   (51,51,255), (255, 229, 204)]


class SERVICES:
    """
    Services constants
    """
    service_lookup = {}
    service_lookup["none"] = 0
    service_lookup["finger"] = 1
    service_lookup["mongo"] = 2
    service_lookup["mongod"] = 2
    service_lookup["tomcat"] = 3
    service_lookup["teamspeak"] = 4
    service_lookup["ts3"] = 4
    service_lookup["snmp"] = 5
    service_lookup["irc"] = 6
    service_lookup["ntp"] = 7
    service_lookup["postgres"] = 8
    service_lookup["postgresql"] = 8
    service_lookup["kafka"] = 9
    service_lookup["smtp"] = 10
    service_lookup["ssh"] = 11
    service_lookup["pengine"] = 12
    service_lookup["cassandra"] = 13
    service_lookup["telnet"] = 14
    service_lookup["http"] = 15
    service_lookup["http-proxy"] = 15
    service_lookup["gopher"] = 16
    service_lookup["kerberos"] = 17
    service_lookup["netbios"] = 18
    service_lookup["imap"] = 19
    service_lookup["dhcp"] = 20
    service_lookup["hdfs"] = 21
    service_lookup["netconf"] = 22
    service_lookup["dns"] = 23
    service_lookup["domain"] = 23
    service_lookup["mysql"] = 24
    service_lookup["docker"] = 25
    service_lookup["ventrilo"] = 26
    service_lookup["bittorrent"] = 27
    service_lookup["bitcoin"] = 28
    service_lookup["ftp"] = 29
    service_lookup["unknown"] = 30
    service_lookup["apani1"] = 31
    service_lookup["eforward"] = 32
    service_lookup["XmlIpcRegSvc"] = 33
    service_lookup["xmlipcregsvc"] = 33
    service_lookup["ajp13"] = 34
    service_lookup["wiegand"] = 35
    service_lookup["netiq-voipa"] = 36
    service_lookup["fmpro-v6"] = 37
    service_lookup["piccolo"] = 38
    service_lookup["dbdb"] = 39
    service_lookup["clariion-evr01"] = 40
    service_lookup["worldfusion2"] = 41
    service_lookup["esimport"] = 42
    service_lookup["ncdmirroring"] = 43
    service_lookup["abb-escp"] = 44
    service_lookup["directnet"] = 45
    service_lookup["fln - spx"] = 46
    service_lookup["netspeak-is"] = 47
    service_lookup["sec-pc2fax-srv"] = 48
    service_lookup["ridgeway2"] = 49
    service_lookup["fjicl-tep-b"] = 50
    service_lookup["ddt"] = 51
    service_lookup["informer"] = 52
    service_lookup["3m-image-lm"] = 53
    service_lookup["corelccam"] = 54
    service_lookup["plysrv-http"] = 56
    service_lookup["jdmn-port"] = 57
    service_lookup["evtp-data"] = 58
    service_lookup["can-ferret-ssl"] = 59
    service_lookup["efi-lm"] = 60
    service_lookup["landmarks"] = 61
    service_lookup["saris"] = 62
    service_lookup["powerguardian"] = 63
    service_lookup["sstp-1"] = 64
    service_lookup["escvpnet"] = 65
    service_lookup["mentaserver"] = 66
    service_lookup["nokia-ann-ch2"] = 67
    service_lookup["sip"] = 68
    service_lookup["mccwebsvr-port"] = 69
    service_lookup["newheights"] = 70
    service_lookup["lmp"] = 71
    service_lookup["vrml-multi-use"] = 71
    service_lookup["lotusnotes"] = 72
    service_lookup["dsmipv6"] = 73
    service_lookup["can-dch"] = 74
    service_lookup["hacl-monitor"] = 75
    service_lookup["spiral-admin"] = 76
    service_lookup["rapidmq-reg"] = 77
    service_lookup["neto-wol-server"] = 78
    service_lookup["pdb"] = 79
    service_lookup["directplay8"] = 80
    service_lookup["bis-web"] = 81
    service_lookup["senomix06"] = 82
    service_lookup["rsmtp"] = 83
    service_lookup["apc-9951"] = 84
    service_lookup["faxportwinport"] = 85
    service_lookup["mac-srvr-admin"] = 86
    service_lookup["vrts-at-port"] = 87
    service_lookup["vrtstrapserver"] = 88
    service_lookup["mtrgtrans"] = 89
    service_lookup["e-builder"] = 90
    service_lookup["ansoft-lm-1"] = 91
    service_lookup["ktelnet"] = 92
    service_lookup["pxc-ntfy"] = 93
    service_lookup["sybasesrvmon"] = 94
    service_lookup["opsmgr"] = 95
    service_lookup["fcp-srvr-inst2"] = 96
    service_lookup["itm-lm"] = 97
    service_lookup["ncconfig"] = 98
    service_lookup["client-ctrl"] = 99
    service_lookup["aairnet-2"] = 100
    service_lookup["servistaitsm"] = 101
    service_lookup["nfsrdma"] = 102
    service_lookup["cockroachdb"] = 103
    service_lookup["glassfish"] = 104
    service_lookup["samba"] = 105
    service_lookup["netbios-ssn"] = 106
    service_lookup["microsoft-ds"] = 107
    service_lookup["vrace"] = 108
    service_lookup["wap-wsp"] = 109
    service_lookup["elasticsearch"] = 110

    #
    service_lookup_inv = {v: k for k, v in service_lookup.items()}


class VULNERABILITIES:
    """
    Vulnerabilities constants
    """
    vuln_lookup = {}
    vuln_lookup["none"] = 0
    vuln_lookup["heartbleed"] = 1
    vuln_lookup["ghostcat"] = 2
    vuln_lookup["sql_injection"] = 3
    vuln_lookup["weak_password"] = 4
    vuln_lookup["drown"] = 5
    vuln_lookup["eternal_blue"] = 6
    vuln_lookup["shellshock"] = 7
    vuln_lookup["poodle"] = 8
    vuln_lookup["timthumb"] = 9
    vuln_lookup["CVE-2020-8620"] = 10
    vuln_lookup["CVE-2020-8617"] = 11
    vuln_lookup["CVE-2020-8616"] = 12
    vuln_lookup["CVE-2019-6470"] = 13
    vuln_lookup["CVE-2020-8623"] = 14
    vuln_lookup["CVE-2020-8621"] = 15
    vuln_lookup["CVE-2020-8624"] = 16
    vuln_lookup["CVE-2020-8622"] = 17
    vuln_lookup["CVE-2020-8619"] = 18
    vuln_lookup["CVE-2020-8618"] = 19
    vuln_lookup["CVE-2014-9278"] = 20
    vuln_lookup["ssh-weak-password"] = 21
    vuln_lookup["telnet-weak-password"] = 22
    vuln_lookup["ftp-weak-password"] = 23
    vuln_lookup["CVE-2020-15523"] = 24
    vuln_lookup["CVE-2020-14422"] = 25
    vuln_lookup["PACKETSTORM:157836"] = 26
    vuln_lookup["unknown"] = 27
    vuln_lookup_inv = {v: k for k, v in vuln_lookup.items()}
    default_cvss = 2.0

    
class OS:
    """
    Operating systems constants
    """
    os_lookup = {}
    os_lookup["unknown"] = 0
    os_lookup["windows"] = 1
    os_lookup["ubuntu"] = 2
    os_lookup["kali"] = 3
    os_lookup["suse"] = 4
    os_lookup["centos"] = 5
    os_lookup["fedora"] = 6
    os_lookup["debian"] = 7
    os_lookup["redhat"] = 8
    os_lookup["linux"] = 9
    os_lookup_inv = {v: k for k, v in os_lookup.items()}


class SECLISTS:
    """
    Constants related to seclists
    """
    TOP_USERNAMES_SHORTLIST = "/SecLists/Usernames/top-usernames-shortlist.txt"


class NMAP:
    """
    Constants related to nmap commands
    """
    SPEED_ARGS = "--min-rate 100000 --max-retries 1 -T5 -n"
    FILE_ARGS = "-oX"
    TELNET_BRUTE_SUBNET = "-p 23 --script telnet-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST \
                          + ",passdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",telnet-brute.timeout=8s,brute.firstonly=true"
    TELNET_BRUTE_HOST = "-p 23 --script telnet-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST \
                        + ",passdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",telnet-brute.timeout=8s,brute.firstonly=true"
    SSH_BRUTE_SUBNET = "-p 22 --script ssh-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                       + SECLISTS.TOP_USERNAMES_SHORTLIST + ",ssh-brute.timeout=8s,brute.firstonly=true"
    SSH_BRUTE_HOST = "-p 22 --script ssh-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                     + SECLISTS.TOP_USERNAMES_SHORTLIST + ",ssh-brute.timeout=8s,brute.firstonly=true"
    FTP_BRUTE_SUBNET = "-p 21 --script ftp-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                       + SECLISTS.TOP_USERNAMES_SHORTLIST+",ftp-brute.timeout=8s,brute.firstonly=true"
    FTP_BRUTE_HOST = "-p 21 --script ftp-brute --script-args userdb="+SECLISTS.TOP_USERNAMES_SHORTLIST+",passdb="\
                     +SECLISTS.TOP_USERNAMES_SHORTLIST+",ftp-brute.timeout=8s,brute.firstonly=true"
    CASSANDRA_BRUTE_SUBNET = "-p 9160 --script cassandra-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                       + SECLISTS.TOP_USERNAMES_SHORTLIST + ",cassandra-brute.timeout=8s,brute.firstonly=true"
    CASSANDRA_BRUTE_HOST = "-p 9160 --script cassandra-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                     + SECLISTS.TOP_USERNAMES_SHORTLIST + ",cassandra-brute.timeout=8s,brute.firstonly=true"
    IRC_BRUTE_SUBNET = "-p 6667 --script irc-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                             + SECLISTS.TOP_USERNAMES_SHORTLIST + ",irc-brute.timeout=8s,brute.firstonly=true"
    IRC_BRUTE_HOST = "-p 6667 --script irc-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                           + SECLISTS.TOP_USERNAMES_SHORTLIST + ",irc-brute.timeout=8s,brute.firstonly=true"
    MONGO_BRUTE_SUBNET = "-p 27017 --script mongo-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                       + SECLISTS.TOP_USERNAMES_SHORTLIST + ",mongo-brute.timeout=8s,brute.firstonly=true"
    MONGO_BRUTE_HOST = "-p 27017 --script mongo-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                     + SECLISTS.TOP_USERNAMES_SHORTLIST + ",mongo-brute.timeout=8s,brute.firstonly=true"
    MYSQL_BRUTE_SUBNET = "-p 27017 --script mysql-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                         + SECLISTS.TOP_USERNAMES_SHORTLIST + ",mysql-brute.timeout=8s,brute.firstonly=true"
    MYSQL_BRUTE_HOST = "-p 27017 --script mysql-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                       + SECLISTS.TOP_USERNAMES_SHORTLIST + ",mysql-brute.timeout=8s,brute.firstonly=true"
    SMTP_BRUTE_SUBNET = "-p 25 --script smtp-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                         + SECLISTS.TOP_USERNAMES_SHORTLIST + ",smtp-brute.timeout=8s,brute.firstonly=true"
    SMTP_BRUTE_HOST = "-p 25 --script smtp-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                       + SECLISTS.TOP_USERNAMES_SHORTLIST + ",smtp-brute.timeout=8s,brute.firstonly=true"
    POSTGRES_BRUTE_SUBNET = "-p 5432 --script pgsql-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                        + SECLISTS.TOP_USERNAMES_SHORTLIST + ",pgsql-brute.timeout=8s,brute.firstonly=true"
    POSTGRES_BRUTE_HOST = "-p 5432 --script pgsql-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                      + SECLISTS.TOP_USERNAMES_SHORTLIST + ",pgsql-brute.timeout=8s,brute.firstonly=true"
    SAMBA_CVE_2017_7494_SCAN = "--script smb-vuln-cve-2017-7494 --script-args smb-vuln-cve-2017-7494.check-version -p445"
    FIREWALK_HOST = "--script=firewalk --traceroute --script-args=firewalk.max-retries=1,firewalk.probe-timeout=800ms"
    HTTP_ENUM = "--script=http-enum"
    HTTP_GREP = "--script=http-grep"
    FINGER = "--script=finger"


class AUXILLARY:
    """
    Auxillary constants
    """
    USER_PLACEHOLDER = "USER_PLACEHOLDER"
    PW_PLACEHOLDER = "USER_PLACEHOLDER"


class NMAP_XML:
    """
    Constants related to nmap XML output
    """
    HOST = "host"
    STATUS = "status"
    ADDRESS = "address"
    HOSTNAMES = "hostnames"
    PORTS = "ports"
    TRACE = "trace"
    HOP = "hop"
    OS = "os"
    STATE = "state"
    REASON = "reason"
    ARP_RESPONSE = "arp-response"
    STATUS_UP = "up"
    ADDR = "addr"
    ADDR_TYPE = "addrtype"
    HOSTNAME = "hostname"
    NAME = "name"
    PORT = "port"
    PORT_ID = "portid"
    UNKNOWN = "unknown"
    SERVICE = "service"
    SCRIPT = "script"
    OPEN_STATE = "open"
    OS_MATCH = "osmatch"
    ACCURACY = "accuracy"
    OS_CLASS = "osclass"
    VENDOR = "vendor"
    OS_FAMILY = "osfamily"
    ELEM = "elem"
    KEY = "key"
    CVSS = "cvss"
    ID = "id"
    TABLE = "table"
    IP = "ip"
    IPADDR = "ipaddr"
    TTL = "ttl"
    RTT = "rtt"
    HOST = "host"
    MAC = "mac"
    VULNERS_SCRIPT_ID = "vulners"
    TELNET_BRUTE_SCRIPT_ID = "telnet-brute"
    SSH_BRUTE_SCRIPT_ID = "ssh-brute"
    FTP_BRUTE_SCRIPT_ID = "ftp-brute"
    CASSANDRA_BRUTE_SCRIPT_ID = "cassandra-brute"
    IRC_BRUTE_SCRIPT_ID = "irc-brute"
    MONGO_BRUTE_SCRIPT_ID = "mongo-brute"
    MYSQL_BRUTE_SCRIPT_ID = "mysql-brute"
    SMTP_BRUTE_SCRIPT_ID = "smtp-brute"
    POSTGRES_BRUTE_SCRIPT_ID = "postgres-brute"
    BRUTE_SCRIPTS = [TELNET_BRUTE_SCRIPT_ID, SSH_BRUTE_SCRIPT_ID, FTP_BRUTE_SCRIPT_ID, CASSANDRA_BRUTE_SCRIPT_ID,
                     IRC_BRUTE_SCRIPT_ID, MONGO_BRUTE_SCRIPT_ID, MYSQL_BRUTE_SCRIPT_ID, SMTP_BRUTE_SCRIPT_ID,
                     POSTGRES_BRUTE_SCRIPT_ID]
    USERNAME = "username"
    PASSWORD = "password"
    ACCOUNTS = "Accounts"
    HTTP_ENUM_SCRIPT = "http-enum"
    OUTPUT = "output"
    HTTP_GREP_SCRIPT = "http-grep"
    VULSCAN_SCRIPT = "vulscan"
    VERSION = "version"
    SERVICEFP = "servicefp"


class SSH:
    """
    Constants related to the SSH service
    """
    SERVICE_NAME ="ssh"
    DEFAULT_PORT = 22
    DIRECT_CHANNEL = "direct-tcpip"


class TELNET:
    """
    Constants related to the Telnet service
    """
    PROMPT = b':~$'
    LOCALHOST = "127.0.0.1"
    LOGIN_PROMPT = b"login: "
    PASSWORD_PROMPT = b"Password: "
    INCORRECT_LOGIN = "Login incorrect"
    SERVICE_NAME="telnet"
    DEFAULT_PORT = 23


class FTP:
    """
    Constants related to the FTP service
    """
    INCORRECT_LOGIN = "Login incorrect"
    SERVICE_NAME = "ftp"
    DEFAULT_PORT = 21
    LOCALHOST = "127.0.0.1"
    LFTP_PROMPT = ":~>"
    LFTP_PROMPT_2 = ":/>"
    LFTP_PREFIX = "lftp ftp://"
    ACCESS_FAILED = "Access failed"


class IRC:
    """
    Constants related to the IRC service
    """
    SERVICE_NAME = "irc"


class POSTGRES:
    """
    Constants related to the Postgres service
    """
    SERVICE_NAME = "postgres"


class SMTP:
    """
    Constants related to the SMTP service
    """
    SERVICE_NAME = "smtp"


class MYSQL:
    """
    Constants related to the MySQL service
    """
    SERVICE_NAME = "mysql"


class MONGO:
    """
    Constants related to the MongoDB service
    """
    SERVICE_NAME = "mongo"


class CASSANDRA:
    """
    Constants related to the Cassandra service
    """
    SERVICE_NAME = "cassandra"


class SAMBA:
    """
    Constants related to the Samba service
    """
    SERVICE_NAME = "samba"
    USER="sambacry"
    PW="nosambanocry"
    BACKDOOR_USER="ssh_backdoor_sambapwned"
    BACKDOOR_PW="sambapwnedpw"
    PORT=445
    ALREADY_EXISTS = "already exists"
    ERROR = "Error"
    AUTH_OK = "Authentication ok"
    VERIFYING = "Veryfying"
    VULNERABILITY_NAME = "cve-2017-7494"


class CVE_2010_0426:
    """
    Constants related to CVE-2010-0426
    """
    SERVICE_NAME = "sudoedit"
    BACKDOOR_USER="ssh_backdoor_cve10_0426pwn"
    BACKDOOR_PW="cve_2010_0426_pwnedpw"
    EXPLOIT_FILE = "/etc/fstab"
    VULNERABILITY_NAME="cve-2010-0426"


class CVE_2015_5602:
    """
    Constants related to CVE-2015-5602
    """
    SERVICE_NAME = "sudoedit"
    BACKDOOR_USER="ssh_backdoor_cve15_5602pwn"
    BACKDOOR_PW="cve_2015_5602_pwnedpw"
    ROOT_PW="cve_2015_5602_temp_root_pw"
    VULNERABILITY_NAME = "cve-2015-5602"


class CVE_2015_3306:
    """
    Constants related to CVE-2015-3306
    """
    SERVICE_NAME = "proftpd"
    BACKDOOR_USER="ssh_backdoor_cve2015_3306_pwned"
    BACKDOOR_PW="cve2015_3306_pwnedpw"
    PORT=21
    VULNERABILITY_NAME="cve-2015-3306"


class CVE_2016_10033:
    """
    Constants related to CVE-2016-10033
    """
    SERVICE_NAME = "http"
    BACKDOOR_USER="ssh_backdoor_2016_10033_pwn"
    BACKDOOR_PW="cve_2016_10033_pwnedpw"
    PORT=80
    VULNERABILITY_NAME = "cve-2016-10033"


class CVE_2015_1427:
    """
    Constants related to CVE-2015-1427
    """
    SERVICE_NAME = "elasticsearch"
    BACKDOOR_USER="ssh_backdoor_cve_2015_1427_pwned"
    BACKDOOR_PW="cve_2015_1427_pwnedpw"
    PORT=9200
    VULNERABILITY_NAME = "cve-2015-1427"


class SHELLSHOCK:
    """
    Constants related to ShellShock
    """
    SERVICE_NAME = "http"
    BACKDOOR_USER="ssh_backdoor_shellshocked"
    BACKDOOR_PW="shellshockedpw"
    PORT=80
    VULNERABILITY_NAME = "cve-2014-6271"


class DVWA_SQL_INJECTION:
    """
    Constants related to DVWA SQL Injection Vulnerabilities
    """
    SERVICE_NAME = "http"
    EXPLOIT_USER="pablo"
    EXPLOIT_OUTPUT_FILENAME = "dvwa_sql_injection_result.txt"
    PORT=80
    VULNERABILITY_NAME="dvwa_sql_injection"


class PENGINE_EXPLOIT:
    """
    Constants related to Pengine Exploit
    """
    SERVICE_NAME = "http"
    PORT=4000
    VULNERABILITY_NAME="pengine-exploit"
    BACKDOOR_USER = "ssh_backdoor_pengine_exploitpwn"
    BACKDOOR_PW = "ssh_backdoor_pengine_exploitpwnpw"


class COMMON:
    """
    Common constants
    """
    CVE_FILE = "/allitems_prep.csv"
    SERVICES_FILE = "/nmap-services"
    DEFAULT_RECV_SIZE = 5000
    LARGE_RECV_SIZE = 1000000


class COMMANDS:
    """
    Constants related to arbitrary commands
    """
    CHANNEL_WHOAMI = "whoami\n"
    CHANNEL_SU_ROOT = "su root\n"
    CHANNEL_ROOT = "root\n"
    LIST_CACHE = "ls -1 "
    SUDO = "sudo"
    CHMOD_777 = "chmod 777"
    SLASH_DELIM = "/"
    TOUCH = "touch"
    NOHUP = "nohup"
    AMP = "&"
    PKILL = "pkill -f"
    RM_F = "rm -f"
    SPACE_DELIM = " "

class FILE_PATTERNS:
    """
    Constants related to file patterns for parsing
    """
    COST_FILE_SUFFIX = "_cost.txt"
    NMAP_ACTION_RESULT_SUFFIX = ".xml"
    ALERTS_FILE_SUFFIX = "_alerts.txt"


class NIKTO:
    """
    Constants related to Nikto commands
    """
    BASE_ARGS = "-port 80 -Format xml --maxtime 60s -timeout 5 "
    HOST_ARG = "-h "
    OUTPUT_ARG = "-output "


class NIKTO_XML:
    """
    Constants related to Nikto XML parsing
    """
    NIKTOSCAN = "niktoscan"
    SCANDETAILS = "scandetails"
    ITEM = "item"
    ITEM_ID = "id"
    OSVDB_ID = "osvdbid"
    DESCR = "description"
    NAMELINK = "namelink"
    IPLINK = "iplink"
    URI = "uri"
    TARGETPORT = "targetport"
    TARGETIP = "targetip"
    SITENAME = "sitename"
    METHOD = "method"


class MASSCAN:
    """
    Constants related to Masscan commands
    """
    BASE_ARGS = "-p0-1024 --max-rate 100000 --max-retries 1 --wait 0"
    HOST_ARG = "--source-ip "
    OUTPUT_ARG = "-oX "


class SSH_BACKDOOR:
    """
    Constants related to creation of SSH backdoors
    """
    BACKDOOR_PREFIX = "ssh_backdoor"
    DEFAULT_PW = "pycr_ctf"


class SHELL:
    """
    Constants related to shell commands
    """
    LIST_ALL_USERS = "cut -d: -f1 /etc/passwd"
    CHECK_FOR_SECLISTS = "test -e /SecLists && echo file exists || echo file not found"
    SAMBA_EXPLOIT = "/samba_exploit.py -e /libbindshell-samba.so -s data -r /data/libbindshell-samba.so -u " \
                    "sambacry -p nosambanocry -P 6699 -t "


class EXPLOIT_VULNERABILITES:
    """
    Constants related to exploit vulnerabilities
    """
    SSH_DICT_SAME_USER_PASS = "ssh-weak-password"
    FTP_DICT_SAME_USER_PASS = "ftp-weak-password"
    TELNET_DICTS_SAME_USER_PASS = "telnet-weak-password"
    IRC_DICTS_SAME_USER_PASS = "irc-weak-password"
    POSTGRES_DICTS_SAME_USER_PASS = "postgres-weak-password"
    SMTP_DICTS_SAME_USER_PASS = "smtp-weak-password"
    MYSQL_DICTS_SAME_USER_PASS = "mysql-weak-password"
    MONGO_DICTS_SAME_USER_PASS = "mongo-weak-password"
    CASSANDRA_DICTS_SAME_USER_PASS = "cassandra-weak-password"
    WEAK_PW_VULNS = [SSH_DICT_SAME_USER_PASS, FTP_DICT_SAME_USER_PASS, TELNET_DICTS_SAME_USER_PASS,
                     IRC_DICTS_SAME_USER_PASS, POSTGRES_DICTS_SAME_USER_PASS, SMTP_DICTS_SAME_USER_PASS,
                     MYSQL_DICTS_SAME_USER_PASS, MONGO_DICTS_SAME_USER_PASS, CASSANDRA_DICTS_SAME_USER_PASS]
    SAMBACRY_EXPLOIT = "cve-2017-7494"
    SHELLSHOCK_EXPLOIT = "cve-2014-6271"
    DVWA_SQL_INJECTION = "dvwa_sql_injection"
    CVE_2015_3306 = "cve-2015-3306"
    CVE_2015_1427 = "cve-2015-1427"
    CVE_2016_10033 = "cve-2016-10033"
    CVE_2010_0426 = "cve-2010-0426"
    CVE_2015_5602 = "cve-2015-5602"
    PENGINE_EXPLOIT = "pengine-exploit"
    CVE_VULNS = [SAMBACRY_EXPLOIT, SHELLSHOCK_EXPLOIT, CVE_2015_3306, CVE_2015_1427, CVE_2016_10033, CVE_2010_0426,
                 CVE_2015_5602]
    UNKNOWN = "unknown"
    WEAK_PASSWORD_CVSS = 10.0


class IDS_ROUTER:
    """
    Constants related to the IDS
    """
    MAX_ALERTS = 1000
    FAST_LOG_FILE = "/var/snort/fast.log"
    ALERTS_FILE = "/var/snort/alert.csv"
    TAIL_ALERTS_COMMAND = "sudo tail -" + str(MAX_ALERTS)
    TAIL_FAST_LOG_COMMAND = "sudo tail -" + str(str(MAX_ALERTS))
    TAIL_ALERTS_LATEST_COMMAND = "sudo tail -1"
    PRIORITY_REGEX = re.compile(r"Priority: \d")


class SUB_PROC_ENV:
    """
    Constants related to creation of Sub-proc-env environments
    """
    SLEEP_TIME_STARTUP = 5


class DUMMY_VEC_ENV:
    """
    Constants related to creation of Sub-proc-env environments
    """
    SLEEP_TIME_STARTUP = 1


class TRAFFIC_COMMANDS:
    """
    Constants related to traffic commands
    """
    DEFAULT_COMMANDS = {
        "ftp1": ["timeout 5 ftp {} > /dev/null 2>&1",
                 "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no {} > /dev/null 2>&1",
                 "timeout 5 curl {}:8080 > /dev/null 2>&1"],
        "ssh1": ["timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no {} > /dev/null 2>&1",
                 "timeout 5 curl {}:80 > /dev/null 2>&1"],
        "telnet1": ["timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no {} > /dev/null 2>&1",
                    "timeout 5 curl {} > /dev/null 2>&1",
                    "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {} > /dev/null 2>&1"],
        "honeypot1": ["timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no {} > /dev/null 2>&1",
                      "timeout 5 snmpwalk -v2c {} -c pycr_ctf1234 > /dev/null 2>&1",
                      "timeout 10 /irc_login_test.sh {} > /dev/null 2>&1",
                      "timeout 5 psql -h {} -p 5432 > /dev/null 2>&1"],
        "samba1": ["timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no {} > /dev/null 2>&1",
                   "(sleep 2; echo testpycruser; sleep 3;) | smbclient -L {} > /dev/null 2>&1"],
        "shellshock1": ["timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no {} > /dev/null 2>&1",
                        "timeout 5 curl {} > /dev/null 2>&1",
                        "timeout 5 snmpwalk -v2c {} -c pycr_ctf1234 > /dev/null 2>&1"],
        "sql_injection1": ["timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no {} > /dev/null 2>&1",
                           "timeout 5 curl {}/login.php > /dev/null 2>&1",
                           "timeout 10 /irc_login_test.sh {} > /dev/null 2>&1"],
        "cve_2010_0426_1": ["timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no {} > /dev/null 2>&1",
                            "timeout 5 curl {}:8080 > /dev/null 2>&1"],
        "cve_2015_1427_1": ["timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no {} > /dev/null 2>&1",
                            "snmpwalk -v2c {} -c pycr_ctf1234"],
        "cve_2015_3306_1": ["timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no {} > /dev/null 2>&1",
                            "snmpwalk -v2c {} -c pycr_ctf1234",
                            "timeout 5 curl {} > /dev/null 2>&1"],
        "cve_2015_5602_1": ["timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no {} > /dev/null 2>&1"],
        "cve_2015_10033_1": ["timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no {} > /dev/null 2>&1",
                             "timeout 5 curl {} > /dev/null 2>&1"],
        "honeypot2": ["timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no {} > /dev/null 2>&1",
                      "timeout 5 snmpwalk -v2c {} -c pycr_ctf1234 > /dev/null 2>&1",
                      "timeout 10 /irc_login_test.sh {} > /dev/null 2>&1",
                      "timeout 5 psql -h {} -p 5432 > /dev/null 2>&1"],
        "ssh2": ["timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no {} > /dev/null 2>&1",
                 "timeout 5 nslookup limmen.dev {} > /dev/null 2>&1"],
        "ssh3": ["timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no {} > /dev/null 2>&1",
                 "timeout 10 /irc_login_test.sh {} > /dev/null 2>&1"
                 ],
        "telnet2": ["timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no {} > /dev/null 2>&1",
                    "timeout 5 curl {}:8080 > /dev/null 2>&1",
                    "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {} > /dev/null 2>&1"],
        "telnet3": ["timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no {} > /dev/null 2>&1",
                    "timeout 5 curl {}:8080 > /dev/null 2>&1",
                    "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {} > /dev/null 2>&1"],
        "ftp2": ["timeout 5 ftp {} > /dev/null 2>&1",
                 "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no {} > /dev/null 2>&1",
                 "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {} > /dev/null 2>&1"],
        "client1_subnet": [
            "sudo nmap -sS -p- " + NMAP.SPEED_ARGS + " {} > /dev/null 2>&1",
            "sudo nmap -sP " + NMAP.SPEED_ARGS + " {} > /dev/null 2>&1",
            "sudo nmap -sU -p- " + NMAP.SPEED_ARGS + " {} > /dev/null 2>&1",
            "sudo nmap -sT -p- " + NMAP.SPEED_ARGS + " {} > /dev/null 2>&1",
            "sudo nmap -sF -p- " + NMAP.SPEED_ARGS + " {} > /dev/null 2>&1",
            "sudo nmap -sN -p- " + NMAP.SPEED_ARGS + " {} > /dev/null 2>&1",
            "sudo nmap -sX -p- " + NMAP.SPEED_ARGS + " {} > /dev/null 2>&1",
            "sudo nmap -O --osscan-guess --max-os-tries 1 " + NMAP.SPEED_ARGS + " {} > /dev/null 2>&1",
            "sudo nmap " + NMAP.HTTP_GREP + " " + NMAP.SPEED_ARGS + " {} > /dev/null 2>&1",
            "sudo nmap " + NMAP.FINGER + " " + NMAP.SPEED_ARGS + " {} > /dev/null 2>&1"
        ],
        "client1_host": [
            "ping {} > /dev/null 2>&1",
            "traceroute {} > /dev/null 2>&1"
        ],
        "pengine_exploit1": ["timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no {} > /dev/null 2>&1",
        "timeout 5 curl {}:4000 > /dev/null 2>&1",
                             "timeout 5 curl --header \"Content-Type: application/json\" --request POST \
                                  --data $'{\"application\": \"pengine_sandbox\", \"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, \"format\":\"json\", \"src_text\": \"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],[_,_,_,_,4,_,_,_,9]]).\n\"}' {}"
                             ]
    }
    TRAFFIC_GENERATOR_FILE_NAME = "traffic_generator.sh"
    BASH_PREAMBLE = "#!/bin/bash"


class PYCR_ADMIN:
    """
    Constants related to the PyCr admin account
    """
    user="pycr_admin"
    pw="pycr@admin-pw_191"


class DEFENDER:
    """
    Constants related to the defender's sensor commands
    """
    LIST_LOGGED_IN_USERS_CMD = "users"
    LIST_OPEN_CONNECTIONS_CMD = "netstat -n"
    LIST_USER_ACCOUNTS = "cat /etc/passwd"
    LIST_FAILED_LOGIN_ATTEMPTS = "sudo tail -50 /var/log/auth.log"
    LIST_SUCCESSFUL_LOGIN_ATTEMPTS = "last"
    LIST_NUMBER_OF_PROCESSES = "ps -e | wc -l"


class SYSTEM_IDENTIFICATION:
    """
    Constants related to the system identification process
    """
    NETWORK_CONF_FILE = "network_conf.pickle"
    DEFENDER_DYNAMICS_MODEL_FILE = "defender_dynamics_model.json"
    TRAJECTORIES_FILE = "taus.json"
    SYSTEM_ID_LOGS_FILE = "system_id_log.csv"


class AUXILLARY_COMMANDS:
    """
    Constants related to auxillary shell commands
    """
    WHOAMI = "whoami"


class INFO_DICT:
    """
    Constants for strings in the info dict of the PyCr_CTF Environment
    """
    FLAGS = "flags"
    CAUGHT_ATTACKER = "caught_attacker"
    EARLY_STOPPED = "early_stopped"
    SUCCESSFUL_INTRUSION = "successful_intrusion"
    SNORT_SEVERE_BASELINE_REWARD = "snort_severe_baseline_reward"
    SNORT_WARNING_BASELINE_REWARD = "snort_warning_baseline_reward"
    SNORT_CRITICAL_BASELINE_REWARD = "snort_critical_baseline_reward"
    VAR_LOG_BASELINE_REWARD = "var_log_baseline_reward"
    STEP_BASELINE_REWARD = "step_baseline_reward"
    SNORT_SEVERE_BASELINE_STEP = "snort_severe_baseline_step"
    SNORT_WARNING_BASELINE_STEP = "snort_warning_baseline_step"
    SNORT_CRITICAL_BASELINE_STEP = "snort_critical_baseline_step"
    VAR_LOG_BASELINE_STEP = "var_log_baseline_step"
    STEP_BASELINE_STEP = "step_baseline_step"
    SNORT_SEVERE_BASELINE_CAUGHT_ATTACKER = "snort_severe_baseline_caught_attacker"
    SNORT_WARNING_BASELINE_CAUGHT_ATTACKER = "snort_warning_baseline_caught_attacker"
    SNORT_CRITICAL_BASELINE_CAUGHT_ATTACKER = "snort_critical_baseline_caught_attacker"
    VAR_LOG_BASELINE_CAUGHT_ATTACKER = "var_log_baseline_caught_attacker"
    STEP_BASELINE_CAUGHT_ATTACKER = "step_baseline_caught_attacker"
    SNORT_SEVERE_BASELINE_EARLY_STOPPING = "snort_severe_baseline_early_stopping"
    SNORT_WARNING_BASELINE_EARLY_STOPPING = "snort_warning_baseline_early_stopping"
    SNORT_CRITICAL_BASELINE_EARLY_STOPPING = "snort_critical_baseline_early_stopping"
    VAR_LOG_BASELINE_EARLY_STOPPING = "var_log_baseline_early_stopping"
    STEP_BASELINE_EARLY_STOPPING = "step_baseline_early_stopping"
    SNORT_SEVERE_BASELINE_UNCAUGHT_INTRUSION_STEPS = "snort_severe_baseline_uncaught_intrusion_steps"
    SNORT_WARNING_BASELINE_UNCAUGHT_INTRUSION_STEPS = "snort_warning_baseline_uncaught_intrusion_steps"
    SNORT_CRITICAL_BASELINE_UNCAUGHT_INTRUSION_STEPS = "snort_critical_baseline_uncaught_intrusion_steps"
    VAR_LOG_BASELINE_UNCAUGHT_INTRUSION_STEPS = "var_log_baseline_uncaught_intrusion_steps"
    STEP_BASELINE_UNCAUGHT_INTRUSION_STEPS = "step_baseline_uncaught_intrusion_steps"
    ATTACKER_COST = "attacker_cost"
    ATTACKER_COST_NORM = "attacker_cost_norm"
    ATTACKER_ALERTS = "attacker_alerts"
    ATTACKER_ALERTS_NORM = "attacker_alerts_norm"
    INTRUSION_STEP = "intrusion_step"
    UNCAUGHT_INTRUSION_STEPS = "uncaught_intrusion_steps"
    OPTIMAL_DEFENDER_REWARD = "optimal_defender_reward"
    ATTACKER_NON_LEGAL_ACTIONS = "attacker_non_legal_actions"
    DEFENDER_NON_LEGAL_ACTIONS = "defender_non_legal_actions"
    IDX = "idx"
    NON_LEGAL_ACTIONS = "non_legal_actions"
    ATTACKER_ACTION = "attacker_action"