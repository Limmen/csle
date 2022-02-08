import os
from csle_common.dao.container_config.traffic_config import TrafficConfig
from csle_common.dao.container_config.node_traffic_config import NodeTrafficConfig
from csle_common.util.experiments_util import util
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.config.generator.traffic_generator import TrafficGenerator
import csle_common.constants.constants as constants


def default_traffic_generators(network_id: int) -> TrafficConfig:
    """
    :param network_id
    :return: the TrafficConfig of the emulation
    """
    traffic_generators = [
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.254",
                          commands=[
                              # f"timeout 120 sudo nmap -sS -p- --min-rate 100000 --max-retries 1 -T5 -n {
                              # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sP --min-rate 100000 --max-retries 1 -T5 -n {
                              # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sU -p- --min-rate 100000 --max-retries 1 -T5 -n {
                              # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sT -p- --min-rate 100000 --max-retries 1 -T5 -n {
                              # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sF -p- --min-rate 100000 --max-retries 1 -T5 -n {
                              # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sN -p- --min-rate 100000 --max-retries 1 -T5 -n {
                              # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sX -p- --min-rate 100000 --max-retries 1 -T5 -n {
                              # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -O --osscan-guess --max-os-tries 1 --min-rate 100000
                              # --max-retries 1 -T5 -n {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{
                              # network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap --script=http-grep --min-rate 100000 --max-retries 1 -T5 -n
                              # {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sv -sC --script=finger --min-rate 100000 --max-retries 1 -T5
                              # -n {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}2.2 "
                              f"> /dev/null 2>&1 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}2.2:80 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 "
                              f"> /dev/null 2>&1 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 "
                              f"> /dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | "
                              f"telnet {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"-c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"-p 5432 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh "
                              f"-oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 "
                              f"> /dev/null 2>&1",
                              f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 "
                              f"> /dev/null 2>&1",
                              f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 "
                              f"> /dev/null 2>&1",
                              f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"> /dev/null 2>&1",
                              f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 "
                              f"> /dev/null 2>&1",
                              f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10 "
                              f"> /dev/null 2>&1",
                              f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 "
                              f"> /dev/null 2>&1",
                              f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 "
                              f"> /dev/null 2>&1",
                              f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"> /dev/null 2>&1",
                              f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 "
                              f"> /dev/null 2>&1",
                              f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10 "
                              f"> /dev/null 2>&1"
                          ],
                          jumphosts=[],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.191",
                          commands=[],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10"
                          ],
                          target_hosts=[]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 "
                              f"> /dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"-c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                              f"timeout 5 psql -h "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"-p 5432 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 curl "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.191"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh "
                              f"-oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                              f"timeout 5 curl "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"-c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                              f"timeout 5 psql -h "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"-p 5432 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh "
                              f"-oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                              f"timeout 5 curl "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh "
                              f"-oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.54 > /dev/null 2>&1",
                              f"timeout 5 nslookup limmen.dev "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.54 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.191",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.54"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.54"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2:80 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"-c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"-p 5432 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.74 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.74 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61 > /dev/null 2>&1",
                              f"timeout 5 curl "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61:8080 > /dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | "
                              f"telnet {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61 "
                              f"> /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.74",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.74",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 "
                              f"> /dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 "
                              f"> /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.191",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 "
                              f"> /dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"-c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 psql -h "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p 5432 "
                              f"> /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.191",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.54",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.2 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 "
                              f"> /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.2",
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.2"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.74",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh "
                              f"-oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3 > /dev/null 2>&1",
                              f"timeout 5 curl "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3 > /dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | "
                              f"telnet {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101 "
                              f"-c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101 "
                              f"-p 5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' "
                              f"ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61 > /dev/null 2>&1",
                              f"timeout 5 curl "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61:8080 > /dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | "
                              f"telnet {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61 > /dev/null "
                              f"2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh "
                              f"-oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62 > /dev/null 2>&1",
                              f"timeout 5 curl "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62:8080 "
                              f"> /dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | "
                              f"telnet {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh "
                              f"-oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3 > /dev/null 2>&1",
                              f"timeout 5 curl "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3 > /dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | "
                              f"telnet {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh "
                              f"-oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.74 "
                              f"> /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.74 "
                              f"> /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.74"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.74"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62",
                          commands=[
                              f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.7 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.7 > /dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.7 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101 -c csle_ctf1234 > "
                              f"/dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101 > /dev/null 2>&1",
                              f"timeout 5 psql -h "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101 -p 5432 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh "
                              f"-oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.74 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.74 "
                              f"> /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.74",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.7",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.74",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.7"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.74 "
                              f"> /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.74 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62 "
                              f"> /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62:8080 "
                              f"> /dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.74",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62",
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.74",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.7",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}6.62 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.62:8080 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.62 > /dev/null "
                              f"2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.62"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.62"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.5 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.5 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.6 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.6 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.8 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.8 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.9 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.9 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.178 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.178 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.4 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.4 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.6 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.6 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.8 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.8 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.9 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.9 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.178 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.178 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.4 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.4 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.5 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.5 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.8 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.8 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.9 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.9 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.178 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.178 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.4 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.4 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.5 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.5 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.6 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.6 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.9 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.9 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.178 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.178 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178"
                          ],
                          target_hosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178"]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.4 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.4 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.5 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.5 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.6 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.6 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.8 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.8 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.178 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.178 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.4 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.4 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.5 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.5 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.6 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.6 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.8 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.8 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.9 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.2.9 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9"
                          ],
                          target_hosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9"]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 nslookup limmen.dev {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.54 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.12 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.12 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.13 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.13 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.14 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.14 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 nslookup limmen.dev {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.54 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.11 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.11 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.13 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.13 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.14 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.14 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 nslookup limmen.dev {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.54 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.11 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.11 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.12 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.12 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.14 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.14 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 nslookup limmen.dev {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.54 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.11 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.11 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.12 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.12 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.13 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.9.13 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.12",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.16 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.16 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.17 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.17 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.18 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.18 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18"
                          ],
                          target_hosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18"]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.15 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.15 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.17 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.17 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.18 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.18 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18"
                          ],
                          target_hosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18"]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.15 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.15 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.16 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.16 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.18 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.18 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18"
                          ],
                          target_hosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18"]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.15 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.15 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.16 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.16 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.17 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.7.17 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17"
                          ],
                          target_hosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17"]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.20 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.20 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.22 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.22 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.23 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.23 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.24 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.24 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.25 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.25 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                          ],
                          jumphosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25"],
                          target_hosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25"]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.19 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.19 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.22 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.22 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.23 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.23 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.24 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.24 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.25 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.25 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                          ],
                          jumphosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25"],
                          target_hosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25"]
                          ),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.19 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.19 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.20 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.20 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.23 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.23 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.24 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.24 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                          ],
                          jumphosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25"],
                          target_hosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25"]
                          ),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.19 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.19 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.20 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.20 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.22 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.22 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.24 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.24 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.25 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.25 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                          ],
                          jumphosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25"],
                          target_hosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25"]
                          ),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.19 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.19 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.20 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.20 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.22 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.22 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.23 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.23 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.25 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.25 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                          ],
                          jumphosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25"],
                          target_hosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25"]
                          ),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.19 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.19 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.20 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.20 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.22 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.22 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.23 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.23 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.24 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                              f"{network_id}.8.24 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                          ],
                          jumphosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24",
                                     f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19"],
                          target_hosts=[f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24",
                                        f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19"]
                          )
    ]
    traffic_conf = TrafficConfig(node_traffic_configs=traffic_generators)
    return traffic_conf


# Generates the traffic.json configuration file
if __name__ == '__main__':
    network_id = 3
    if not os.path.exists(util.default_traffic_path()):
        TrafficGenerator.write_traffic_config(default_traffic_generators(network_id=network_id))
    traffic_config = util.read_traffic_config(util.default_traffic_path())
    emulation_config = EmulationConfig(agent_ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.191",
                                       agent_username=constants.CSLE_ADMIN.USER,
                                       agent_pw=constants.CSLE_ADMIN.PW, server_connection=False)
    TrafficGenerator.create_traffic_scripts(traffic_config=traffic_config, emulation_config=emulation_config,
                                            sleep_time=1)
