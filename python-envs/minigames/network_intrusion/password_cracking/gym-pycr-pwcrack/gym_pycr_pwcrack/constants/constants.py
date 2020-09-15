"""
Constants for the pycr-pwcrack environment
"""

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
    LINE_WIDTH = 2
    CAPTION = "PyCr-PwCrack"
    DEFAULT_WIDTH = 950
    DEFAULT_HEIGHT = 900
    TITLE = "PyCr-PwCrack"
    FIREWALL_SPRITE_NAME = "firewall.png"
    HACKER_SPRITE_NAME = "hacker.png"
    FLAG_SPRITE_NAME = "flag_1.png"
    LINK_COLORS = [(132,87,87), (153,0,153), (153,0,0), (204,204,255), (0,102,0), (102, 0, 102), (153,153,0),
                   (128,128,128), (51,153,255), (0, 153, 153), (204,255,153), (255, 204, 153), (255, 153, 153),
                   (51,51,255), (255, 229, 204)]

class SERVICES:
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
    service_lookup_inv = {v: k for k, v in service_lookup.items()}

class VULNERABILITIES:
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
    vuln_lookup_inv = {v: k for k, v in vuln_lookup.items()}
    
    
class OS:
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
    TOP_USERNAMES_SHORTLIST = "/SecLists/Usernames/top-usernames-shortlist.txt"

class NMAP:
    SPEED_ARGS = "--min-rate 100000 --max-retries 1 -T5"
    FILE_ARGS = "-oX"
    TELNET_BRUTE_SUBNET = "-p 23 --script telnet-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST \
                          + ",passdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",telnet-brute.timeout=8s"
    TELNET_BRUTE_HOST = "-p 23 --script telnet-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST \
                        + ",passdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",telnet-brute.timeout=8s,brute.firstonly=true"
    SSH_BRUTE_SUBNET = "-p 22 --script ssh-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                       + SECLISTS.TOP_USERNAMES_SHORTLIST + ",ssh-brute.timeout=8s"
    SSH_BRUTE_HOST = "-p 22 --script ssh-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                     + SECLISTS.TOP_USERNAMES_SHORTLIST + ",ssh-brute.timeout=8s,brute.firstonly=true"
    FTP_BRUTE_SUBNET = "-p 21 --script ftp-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                       + SECLISTS.TOP_USERNAMES_SHORTLIST+",ftp-brute.timeout=8s"
    FTP_BRUTE_HOST = "-p 21 --script ftp-brute --script-args userdb="+SECLISTS.TOP_USERNAMES_SHORTLIST+",passdb="\
                     +SECLISTS.TOP_USERNAMES_SHORTLIST+",ftp-brute.timeout=8s,brute.firstonly=true"
    CASSANDRA_BRUTE_SUBNET = "-p 9160 --script cassandra-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                       + SECLISTS.TOP_USERNAMES_SHORTLIST + ",cassandra-brute.timeout=8s"
    CASSANDRA_BRUTE_HOST = "-p 9160 --script cassandra-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                     + SECLISTS.TOP_USERNAMES_SHORTLIST + ",cassandra-brute.timeout=8s,brute.firstonly=true"
    IRC_BRUTE_SUBNET = "-p 6667 --script irc-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                             + SECLISTS.TOP_USERNAMES_SHORTLIST + ",irc-brute.timeout=8s"
    IRC_BRUTE_HOST = "-p 6667 --script irc-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                           + SECLISTS.TOP_USERNAMES_SHORTLIST + ",irc-brute.timeout=8s,brute.firstonly=true"
    MONGO_BRUTE_SUBNET = "-p 27017 --script mongo-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                       + SECLISTS.TOP_USERNAMES_SHORTLIST + ",mongo-brute.timeout=8s"
    MONGO_BRUTE_HOST = "-p 27017 --script mongo-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                     + SECLISTS.TOP_USERNAMES_SHORTLIST + ",mongo-brute.timeout=8s,brute.firstonly=true"
    MYSQL_BRUTE_SUBNET = "-p 27017 --script mysql-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                         + SECLISTS.TOP_USERNAMES_SHORTLIST + ",mysql-brute.timeout=8s"
    MYSQL_BRUTE_HOST = "-p 27017 --script mysql-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                       + SECLISTS.TOP_USERNAMES_SHORTLIST + ",mysql-brute.timeout=8s,brute.firstonly=true"
    SMTP_BRUTE_SUBNET = "-p 25 --script smtp-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                         + SECLISTS.TOP_USERNAMES_SHORTLIST + ",smtp-brute.timeout=8s"
    SMTP_BRUTE_HOST = "-p 25 --script smtp-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                       + SECLISTS.TOP_USERNAMES_SHORTLIST + ",smtp-brute.timeout=8s,brute.firstonly=true"
    POSTGRES_BRUTE_SUBNET = "-p 5432 --script pgsql-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                        + SECLISTS.TOP_USERNAMES_SHORTLIST + ",pgsql-brute.timeout=8s"
    POSTGRES_BRUTE_HOST = "-p 5432 --script pgsql-brute --script-args userdb=" + SECLISTS.TOP_USERNAMES_SHORTLIST + ",passdb=" \
                      + SECLISTS.TOP_USERNAMES_SHORTLIST + ",pgsql-brute.timeout=8s,brute.firstonly=true"





