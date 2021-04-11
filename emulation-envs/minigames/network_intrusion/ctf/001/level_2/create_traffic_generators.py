import os
from gym_pycr_ctf.dao.container_config.traffic_config import TrafficConfig
from gym_pycr_ctf.dao.container_config.node_traffic_config import NodeTrafficConfig
from gym_pycr_ctf.util.experiments_util import util
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.envs_model.config.generator.traffic_generator import TrafficGenerator

def default_traffic_generators() -> TrafficConfig:
    traffic_generators = [
        NodeTrafficConfig(ip="172.18.2.254",
                          commands=[
                              # "timeout 120 sudo nmap -sS -p- --min-rate 100000 --max-retries 1 -T5 -n 172.18.2.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sP --min-rate 100000 --max-retries 1 -T5 -n 172.18.2.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sU -p- --min-rate 100000 --max-retries 1 -T5 -n 172.18.2.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sT -p- --min-rate 100000 --max-retries 1 -T5 -n 172.18.2.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sF -p- --min-rate 100000 --max-retries 1 -T5 -n 172.18.2.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sN -p- --min-rate 100000 --max-retries 1 -T5 -n 172.18.2.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sX -p- --min-rate 100000 --max-retries 1 -T5 -n 172.18.2.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -O --osscan-guess --max-os-tries 1 --min-rate 100000 --max-retries 1 -T5 -n 172.18.2.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap --script=http-grep --min-rate 100000 --max-retries 1 -T5 -n  172.18.2.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sv -sC --script=finger --min-rate 100000 --max-retries 1 -T5 -n 172.18.2.0/24 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.2 > /dev/null 2>&1 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.3 > /dev/null 2>&1 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.2.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.2.21 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.2.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.2.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.2.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.79:8080 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.2.2 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.2.3 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.2.21 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.2.79 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.2.10 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.2.2 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.2.3 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.2.21 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.2.79 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.2.10 > /dev/null 2>&1"
                          ],
                          jumphosts=[],
                          target_hosts=[
                              "172.18.2.2", "172.18.2.3", "172.18.2.21",
                              "172.18.2.79", "172.18.2.10"
                          ]),
        NodeTrafficConfig(ip="172.18.2.191",
                          commands=[],
                          jumphosts=[
                              "172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79", "172.18.2.10"
                          ],
                          target_hosts=[]),
        NodeTrafficConfig(ip="172.18.2.21",
                          commands=[
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.2.3 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.2.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.79:8080 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.2.2", "172.18.2.3", "172.18.2.79", "172.18.2.191",
                              "172.18.2.10"
                          ],
                          target_hosts=[
                              "172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79"
                          ]),
        NodeTrafficConfig(ip="172.18.2.10",
                          commands=[
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.2.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.2.21 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.2.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.2.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.2.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.79:8080 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79", "172.18.2.191"
                          ],
                          target_hosts=[
                              "172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79"
                          ]),
        NodeTrafficConfig(ip="172.18.2.2",
                          commands=[
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.2.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.2.21 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.2.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.2.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.2.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.79:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.54 > /dev/null 2>&1",
                              "timeout 5 nslookup limmen.dev 172.18.2.54 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.2.3", "172.18.2.21", "172.18.2.79", "172.18.2.191",
                              "172.18.2.10", "172.18.2.54"
                          ],
                          target_hosts=[
                              "172.18.2.3", "172.18.2.21", "172.18.2.79", "172.18.2.54"
                          ]),
        NodeTrafficConfig(ip="172.18.2.3",
                          commands=[
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.2.21 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.2.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.2.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.2.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.79:8080 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.2.7 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.7 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.2.7 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.101 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.2.101 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.2.101 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.2.101 -p 5432 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.74 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.2.74 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.61 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.61:8080 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.2.61 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.2.74", "172.18.2.7", "172.18.2.21", "172.18.2.79", "172.18.2.191",
                              "172.18.2.10", "172.18.2.101", "172.18.2.61"
                          ],
                          target_hosts=[
                              "172.18.2.74", "172.18.2.7", "172.18.2.21", "172.18.2.79",
                              "172.18.2.101", "172.18.2.61"
                          ]),
        NodeTrafficConfig(ip="172.18.2.79",
                          commands=[
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.2.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.2.21 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.2.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.2.21 -p 5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.191",
                              "172.18.2.10",
                          ],
                          target_hosts=[
                              "172.18.2.2", "172.18.2.3", "172.18.2.21"
                          ]),
        NodeTrafficConfig(ip="172.18.2.101",
                          commands=[
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.2.21 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.2.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.2.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.2.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.79:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.2.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.74 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.2.74 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.61 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.61:8080 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.2.61 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.62 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.62:8080 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.2.62 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.2.74", "172.18.2.7", "172.18.2.62",
                          ],
                          target_hosts=[
                              "172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79",
                              "172.18.2.61", "172.18.2.74", "172.18.2.62"
                          ]),
        NodeTrafficConfig(ip="172.18.2.54",
                          commands=[
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.2.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.2.21 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.2.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.2.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.2.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.79:8080 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.2.2",
                          ],
                          target_hosts=[
                              "172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79"
                          ]),
        NodeTrafficConfig(ip="172.18.2.74",
                          commands=[
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.2.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.2.21 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.2.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.2.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.2.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.79:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.101 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.2.101 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.2.101 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.2.101 -p 5432 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.61 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.61:8080 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.2.61 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.62 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.62:8080 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.2.62 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.2.3", "172.18.2.61", "172.18.2.62",
                              "172.18.2.7", "172.18.2.101"
                          ],
                          target_hosts=[
                              "172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79",
                              "172.18.2.61", "172.18.2.101", "172.18.2.62"
                          ]),
        NodeTrafficConfig(ip="172.18.2.61",
                          commands=[
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.2.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.2.21 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.2.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.2.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.2.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.79:8080 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.74 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.2.74 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.2.3", "172.18.2.62", "172.18.2.74",
                              "172.18.2.7", "172.18.2.101"
                          ],
                          target_hosts=[
                              "172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79",
                              "172.18.2.74"
                          ]),
        NodeTrafficConfig(ip="172.18.2.62",
                          commands=[
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.2.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.2.21 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.2.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.2.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.2.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.79:8080 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.2.7 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.7 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.2.7 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.101 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.2.101 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.2.101 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.2.101 -p 5432 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.74 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.2.74 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.2.61 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.2.61:8080 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.2.61 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.2.74", "172.18.2.7", "172.18.2.101"
                          ],
                          target_hosts=[
                              "172.18.2.2", "172.18.2.3", "172.18.2.21", "172.18.2.79",
                              "172.18.2.61", "172.18.2.74",
                              "172.18.2.101", "172.18.2.7"
                          ])
    ]
    traffic_conf = TrafficConfig(node_traffic_configs=traffic_generators)
    return traffic_conf


if __name__ == '__main__':
    if not os.path.exists(util.default_traffic_path()):
        TrafficGenerator.write_traffic_config(default_traffic_generators())
    traffic_config = util.read_users_config(util.default_traffic_path())
    emulation_config = EmulationConfig(agent_ip="172.18.2.191", agent_username="pycr_admin",
                                     agent_pw="pycr@admin-pw_191", server_connection=False)
    TrafficGenerator.create_traffic_scripts(traffic_config=traffic_config, emulation_config=emulation_config,
                                            sleep_time=1)