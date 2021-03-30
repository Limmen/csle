import os
from gym_pycr_ctf.dao.container_config.traffic_config import TrafficConfig
from gym_pycr_ctf.dao.container_config.node_traffic_config import NodeTrafficConfig
from gym_pycr_ctf.util.experiments_util import util
from gym_pycr_ctf.dao.network.cluster_config import ClusterConfig
from gym_pycr_ctf.envs.config.generator.traffic_generator import TrafficGenerator

def default_traffic_generators() -> TrafficConfig:
    traffic_generators = [
        NodeTrafficConfig(ip="172.18.1.191",
                          commands=[],
                          jumphosts=[
                              "172.18.1.2", "172.18.1.3", "172.18.1.21",
                              "172.18.1.79", "172.18.1.191", "172.18.1.10"
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
    cluster_config = ClusterConfig(agent_ip="172.18.1.191", agent_username="pycr_admin",
                                   agent_pw="pycr@admin-pw_191", server_connection=False)
    TrafficGenerator.create_traffic_scripts(traffic_config=traffic_config, cluster_config=cluster_config)