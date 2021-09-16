import os
from gym_pycr_ctf.dao.container_config.traffic_config import TrafficConfig
from gym_pycr_ctf.dao.container_config.node_traffic_config import NodeTrafficConfig
from gym_pycr_ctf.util.experiments_util import util
from pycr_common.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.envs_model.config.generator.traffic_generator import TrafficGenerator

def default_traffic_generators() -> TrafficConfig:
    traffic_generators = [
        NodeTrafficConfig(ip="172.18.1.254",
                          commands=[
                              # "timeout 120 sudo nmap -sS -p- --min-rate 100000 --max-retries 1 -T5 -n 172.18.1.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sP --min-rate 100000 --max-retries 1 -T5 -n 172.18.1.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sU -p- --min-rate 100000 --max-retries 1 -T5 -n 172.18.1.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sT -p- --min-rate 100000 --max-retries 1 -T5 -n 172.18.1.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sF -p- --min-rate 100000 --max-retries 1 -T5 -n 172.18.1.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sN -p- --min-rate 100000 --max-retries 1 -T5 -n 172.18.1.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sX -p- --min-rate 100000 --max-retries 1 -T5 -n 172.18.1.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -O --osscan-guess --max-os-tries 1 --min-rate 100000 --max-retries 1 -T5 -n 172.18.1.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap --script=http-grep --min-rate 100000 --max-retries 1 -T5 -n  172.18.1.0/24 > /dev/null 2>&1",
                              # "timeout 120 sudo nmap -sv -sC --script=finger --min-rate 100000 --max-retries 1 -T5 -n 172.18.1.0/24 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.1.2 > /dev/null 2>&1 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.1.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.1.3 > /dev/null 2>&1 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.1.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.1.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.1.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.1.21 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.1.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.1.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.1.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.1.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.1.79:8080 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.1.2 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.1.3 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.1.21 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.1.79 > /dev/null 2>&1",
                              "timeout 15 ping 172.18.1.10 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.1.2 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.1.3 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.1.21 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.1.79 > /dev/null 2>&1",
                              "timeout 25 traceroute 172.18.1.10 > /dev/null 2>&1"
                          ],
                          jumphosts=[],
                          target_hosts=[
                              "172.18.1.2", "172.18.1.3", "172.18.1.21",
                              "172.18.1.79", "172.18.1.10"
                          ]),
        NodeTrafficConfig(ip="172.18.1.191",
                          commands=[],
                          jumphosts=[
                              "172.18.1.2", "172.18.1.3", "172.18.1.21",
                              "172.18.1.79", "172.18.1.10"
                          ],
                          target_hosts=[]),
        NodeTrafficConfig(ip="172.18.1.21",
                          commands=[
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.1.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.1.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.1.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.1.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.1.3 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.1.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.1.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.1.79:8080 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.1.2", "172.18.1.3", "172.18.1.21",
                              "172.18.1.79", "172.18.1.191", "172.18.1.10"
                          ],
                          target_hosts=[
                              "172.18.1.2", "172.18.1.3", "172.18.1.79"
                          ]),
        NodeTrafficConfig(ip="172.18.1.10",
                          commands=[
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.1.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.1.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.1.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.1.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.1.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.1.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.1.21 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.1.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.1.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.1.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.1.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.1.79:8080 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.1.2", "172.18.1.3", "172.18.1.21", "172.18.1.79",
                              "172.18.1.191"
                          ],
                          target_hosts=[
                              "172.18.1.2", "172.18.1.3", "172.18.1.21", "172.18.1.79"
                          ]),
        NodeTrafficConfig(ip="172.18.1.2",
                          commands=[
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.1.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.1.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.1.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.1.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.1.21 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.1.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.1.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.1.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.1.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.1.79:8080 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.1.3", "172.18.1.21", "172.18.1.79", "172.18.1.10"
                          ],
                          target_hosts=[
                              "172.18.1.3", "172.18.1.21", "172.18.1.79"
                          ]),
        NodeTrafficConfig(ip="172.18.1.3",
                          commands=[
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.1.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.1.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.1.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.1.21 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.1.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.1.21 -p 5432 > /dev/null 2>&1",
                              "timeout 5 ftp 172.18.1.79 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.1.79 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.1.79:8080 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.1.2", "172.18.1.21", "172.18.1.79", "172.18.1.191", "172.18.1.10"
                          ],
                          target_hosts=[
                              "172.18.1.2", "172.18.1.3", "172.18.1.21", "172.18.1.79"
                          ]),
        NodeTrafficConfig(ip="172.18.1.79",
                          commands=[
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.1.2 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.1.2:80 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.1.3 > /dev/null 2>&1",
                              "timeout 5 curl 172.18.1.3 > /dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet 172.18.1.3 > /dev/null 2>&1",
                              "timeout 5 sshpass -p 'testpycruser' ssh -oStrictHostKeyChecking=no 172.18.1.21 > /dev/null 2>&1",
                              "timeout 5 snmpwalk -v2c 172.18.1.21 -c pycr_ctf1234 > /dev/null 2>&1",
                              "timeout 10 /irc_login_test.sh 172.18.1.21 > /dev/null 2>&1",
                              "timeout 5 psql -h 172.18.1.21 -p 5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              "172.18.1.2", "172.18.1.3", "172.18.1.21", "172.18.1.191", "172.18.1.10"
                          ],
                          target_hosts=[
                              "172.18.1.2", "172.18.1.3", "172.18.1.21", "172.18.1.79"
                          ])
    ]
    traffic_conf = TrafficConfig(node_traffic_configs=traffic_generators)
    return traffic_conf


if __name__ == '__main__':
    if not os.path.exists(util.default_traffic_path()):
        TrafficGenerator.write_traffic_config(default_traffic_generators())
    traffic_config = util.read_users_config(util.default_traffic_path())
    emulation_config = EmulationConfig(agent_ip="172.18.1.191", agent_username="pycr_admin",
                                     agent_pw="pycr@admin-pw_191", server_connection=False)
    TrafficGenerator.create_traffic_scripts(traffic_config=traffic_config, emulation_config=emulation_config,
                                            sleep_time=1)