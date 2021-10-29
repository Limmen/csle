import os
from pycr_common.dao.container_config.traffic_config import TrafficConfig
from pycr_common.dao.container_config.node_traffic_config import NodeTrafficConfig
from pycr_common.util.experiments_util import util
from pycr_common.dao.network.emulation_config import EmulationConfig
from pycr_common.envs_model.config.generator.traffic_generator import TrafficGenerator
import pycr_common.constants.constants as constants


def default_traffic_generators() -> TrafficConfig:
    traffic_generators = [
        NodeTrafficConfig(ip="172.18.5.254",
                          commands=[
                              # "timeout 120 sudo nmap -sS -p- --min-rate 100000 --max-retries 1 -T5 -n 172.18.5.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sP --min-rate 100000 --max-retries 1 -T5 -n 172.18.5.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sU -p- --min-rate 100000 --max-retries 1 -T5 -n 172.18.5.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sT -p- --min-rate 100000 --max-retries 1 -T5 -n 172.18.5.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sF -p- --min-rate 100000 --max-retries 1 -T5 -n 172.18.5.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sN -p- --min-rate 100000 --max-retries 1 -T5 -n 172.18.5.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sX -p- --min-rate 100000 --max-retries 1 -T5 -n 172.18.5.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -O --osscan-guess --max-os-tries 1 --min-rate 100000 --max-retries 1 -T5 -n 172.18.5.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap --script=http-grep --min-rate 100000 --max-retries 1 -T5 -n  172.18.5.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sv -sC --script=finger --min-rate 100000 --max-retries 1 -T5 -n 172.18.5.0/24 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.2 > /dev/null 2>&1 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.3 > /dev/null 2>&1 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.5.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.5.21 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.5.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.5.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.5.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.79:8080 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.5.2 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.5.3 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.5.21 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.5.79 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.5.10 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.5.2 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.5.3 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.5.21 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.5.79 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.5.10 > /dev/null 2>&1"
                          ],
                          jumphosts=[],
                          target_hosts=[
                              "172.18.5.2", "172.18.5.3", "172.18.5.21",
                              "172.18.5.79", "172.18.5.10"
                          ]),
        NodeTrafficConfig(ip="172.18.5.191",
                          commands=[],
                          jumphosts=[
                              "172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79", "172.18.5.10"
                          ],
                          target_hosts=[]),
        NodeTrafficConfig(ip="172.18.5.21",
                          commands=[
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.5.3 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.5.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.79:8080 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.5.2", "172.18.5.3", "172.18.5.79", "172.18.5.191",
                              "172.18.5.10"
                          ],
                          target_hosts=[
                              "172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79"
                          ]),
        NodeTrafficConfig(ip="172.18.5.10",
                          commands=[
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.5.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.5.21 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.5.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.5.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.5.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.79:8080 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79", "172.18.5.191"
                          ],
                          target_hosts=[
                              "172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79"
                          ]),
        NodeTrafficConfig(ip="172.18.5.2",
                          commands=[
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.5.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.5.21 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.5.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.5.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.5.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.79:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.54 > /dev/null 2>&1",
                              "timeout 5 nslookup limmen.dev 172.18.5.54 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.5.3", "172.18.5.21", "172.18.5.79", "172.18.5.191",
                              "172.18.5.10", "172.18.5.54"
                          ],
                          target_hosts=[
                              "172.18.5.3", "172.18.5.21", "172.18.5.79", "172.18.5.54"
                          ]),
        NodeTrafficConfig(ip="172.18.5.3",
                          commands=[
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.5.21 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.5.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.5.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.5.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.79:8080 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.5.7 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.7 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.5.7 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.101 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.5.101 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.5.101 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.5.101 -p 5432 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.74 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.5.74 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.61 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.61:8080 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.5.61 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.5.74", "172.18.5.7", "172.18.5.21", "172.18.5.79", "172.18.5.191",
                              "172.18.5.10", "172.18.5.101", "172.18.5.61"
                          ],
                          target_hosts=[
                              "172.18.5.74", "172.18.5.7", "172.18.5.21", "172.18.5.79",
                              "172.18.5.101", "172.18.5.61"
                          ]),
        NodeTrafficConfig(ip="172.18.5.79",
                          commands=[
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.5.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.5.21 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.5.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.5.21 -p 5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.191",
                              "172.18.5.10",
                          ],
                          target_hosts=[
                              "172.18.5.2", "172.18.5.3", "172.18.5.21"
                          ]),
        NodeTrafficConfig(ip="172.18.5.101",
                          commands=[
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.5.21 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.5.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.5.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.5.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.79:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.5.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.74 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.5.74 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.61 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.61:8080 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.5.61 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.62 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.62:8080 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.5.62 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.5.74", "172.18.5.7", "172.18.5.62",
                          ],
                          target_hosts=[
                              "172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79",
                              "172.18.5.61", "172.18.5.74", "172.18.5.62"
                          ]),
        NodeTrafficConfig(ip="172.18.5.54",
                          commands=[
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.5.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.5.21 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.5.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.5.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.5.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.79:8080 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.5.2",
                          ],
                          target_hosts=[
                              "172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79"
                          ]),
        NodeTrafficConfig(ip="172.18.5.74",
                          commands=[
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.5.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.5.21 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.5.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.5.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.5.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.79:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.101 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.5.101 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.5.101 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.5.101 -p 5432 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.61 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.61:8080 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.5.61 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.62 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.62:8080 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.5.62 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.5.3", "172.18.5.61", "172.18.5.62",
                              "172.18.5.7", "172.18.5.101"
                          ],
                          target_hosts=[
                              "172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79",
                              "172.18.5.61", "172.18.5.101", "172.18.5.62"
                          ]),
        NodeTrafficConfig(ip="172.18.5.61",
                          commands=[
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.5.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.5.21 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.5.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.5.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.5.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.79:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.74 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.5.74 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.5.3", "172.18.5.62", "172.18.5.74",
                              "172.18.5.7", "172.18.5.101"
                          ],
                          target_hosts=[
                              "172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79",
                              "172.18.5.74"
                          ]),
        NodeTrafficConfig(ip="172.18.5.62",
                          commands=[
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.5.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.5.21 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.5.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.5.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.5.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.79:8080 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.5.7 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.7 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.5.7 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.101 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.5.101 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.5.101 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.5.101 -p 5432 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.74 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.5.74 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.5.61 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.5.61:8080 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.5.61 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.5.74", "172.18.5.7", "172.18.5.101"
                          ],
                          target_hosts=[
                              "172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79",
                              "172.18.5.61", "172.18.5.74",
                              "172.18.5.101", "172.18.5.7"
                          ])
    ]
    traffic_conf = TrafficConfig(node_traffic_configs=traffic_generators)
    return traffic_conf


if __name__ == '__main__':
    if not os.path.exists(util.default_traffic_path()):
        TrafficGenerator.write_traffic_config(default_traffic_generators())
    traffic_config = util.read_traffic_config(util.default_traffic_path())
    emulation_config = EmulationConfig(agent_ip="172.18.5.191", agent_username=constants.PYCR_ADMIN.USER,
                                     agent_pw=constants.PYCR_ADMIN.PW, server_connection=False)
    TrafficGenerator.create_traffic_scripts(traffic_config=traffic_config, emulation_config=emulation_config,
                                            sleep_time=1)