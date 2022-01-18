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
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.254",
                          commands=[
                              # f"timeout 120 sudo nmap -sS -p- --min-rate 100000 --max-retries 1 -T5 -n
                              # {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sP --min-rate 100000 --max-retries 1 -T5 -n {
                              # constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} >
                              # /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sU -p- --min-rate 100000 --max-retries 1 -T5 -n
                              # {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sT -p- --min-rate 100000 --max-retries 1 -T5 -n
                              # {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sF -p- --min-rate 100000 --max-retries 1 -T5 -n
                              # {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sN -p- --min-rate 100000 --max-retries 1 -T5 -n
                              # {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sX -p- --min-rate 100000 --max-retries 1 -T5 -n
                              # {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -O --osscan-guess --max-os-tries 1 --min-rate 100000
                              # --max-retries 1 -T5 -n {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{
                              # network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap --script=http-grep --min-rate 100000 --max-retries 1 -T5 -n
                              # {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sv -sC --script=finger --min-rate 100000 --max-retries 1 -T5
                              # -n {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}{constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2 > "
                              f"/dev/null 2>&1 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2:80 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null "
                              f"2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 15 ping {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2 > "
                              f"/dev/null 2>&1",
                              f"timeout 15 ping {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"timeout 15 ping {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 > "
                              f"/dev/null 2>&1",
                              f"timeout 15 ping {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 15 ping {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10 > "
                              f"/dev/null 2>&1",
                              f"timeout 25 traceroute {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2 "
                              f"> /dev/null 2>&1",
                              f"timeout 25 traceroute {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 "
                              f"> /dev/null 2>&1",
                              f"timeout 25 traceroute {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 "
                              f"> /dev/null 2>&1",
                              f"timeout 25 traceroute {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 "
                              f"> /dev/null 2>&1",
                              f"timeout 25 traceroute {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10 "
                              f"> /dev/null 2>&1"
                          ],
                          jumphosts=[],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                          commands=[],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10"
                          ],
                          target_hosts=[]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2:80 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null "
                              f"2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.4 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.4 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.5 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.5 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.6 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.6 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.8 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.8 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.9 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.9 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.178 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.178 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null "
                              f"2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 nslookup limmen.dev {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.54 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79"
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2:80 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61:8080 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > /dev/null "
                              f"2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2:80 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null "
                              f"2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79:8080 > "
                              f"/dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2:80 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null "
                              f"2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2:80 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null "
                              f"2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.11 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.11 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.12 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.12 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.12 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.12 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.13 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.13 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.13 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.13 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.14 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.14 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.14 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.14 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.12",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.13",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.14"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.12",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.13",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.14"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2:80 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null "
                              f"2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.101 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.101 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61:8080 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > /dev/null "
                              f"2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2:80 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null "
                              f"2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74 > "
                              f"/dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.74 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.19 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.19 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.20 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.20 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.22 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.22 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.23 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.23 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.24 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.24 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.25 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.25 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.28 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.28 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2:80 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null "
                              f"2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7 > /dev/null "
                              f"2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.101 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.101 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61:8080 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > /dev/null "
                              f"2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.15 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.15 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.15 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.15 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.16 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.16 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.16 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.16 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.17 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.17 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.17 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.17 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.18 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.18 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.18 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.18 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.15",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.16",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.17",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.18"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.15",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.16",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.17",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.18"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2:80 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null "
                              f"2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74 > "
                              f"/dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.74 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61:8080 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > /dev/null "
                              f"2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62:8080 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62 > /dev/null "
                              f"2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2:80 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null "
                              f"2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.101 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.101 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74 > "
                              f"/dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.74 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61:8080 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > /dev/null "
                              f"2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62:8080 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62 > /dev/null "
                              f"2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.5 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.5 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.6 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.6 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.8 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.8 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.9 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.9 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.178 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.178 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.4 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.4 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.6 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.6 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.8 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.8 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.9 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.9 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.178 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.178 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.4 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.4 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.5 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.5 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.8 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.8 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.9 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.9 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.178 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.178 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.4 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.4 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.5 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.5 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.6 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.6 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.9 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.9 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.178 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.178 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178"
                          ],
                          target_hosts=[f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178"]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.4 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.4 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.5 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.5 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.6 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.6 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.8 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.8 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.178 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.178 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.4 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.4 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.5 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.5 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.6 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.6 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.8 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.8 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.9 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.9 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9"
                          ],
                          target_hosts=[f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9"]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 nslookup limmen.dev {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.54 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.12 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.12 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.12 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.12 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.13 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.13 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.13 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.13 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.14 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.14 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.14 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.14 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.12",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.13",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.14"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.12",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.13",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.14"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.12",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 nslookup limmen.dev {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.54 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.11 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.11 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.13 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.13 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.13 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.13 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.14 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.14 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.14 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.14 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.12",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.13",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.14"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.13",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.14"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.13",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 nslookup limmen.dev {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.54 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.11 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.11 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.12 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.12 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.12 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.12 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.14 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.14 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.14 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.14 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.12",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.14"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.12",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.14"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.14",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 nslookup limmen.dev {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.54 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.11 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.11 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.12 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.12 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.12 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.12 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.13 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.13 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.13 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.13 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.12",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.13",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.12",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.13",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.15",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.16 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.16 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.16 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.16 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.17 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.17 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.17 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.17 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.18 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.18 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.18 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.18 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.16",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.17",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.18"
                          ],
                          target_hosts=[f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.16",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.17",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.18"]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.16",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.15 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.15 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.15 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.15 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.17 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.17 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.17 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.17 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.18 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.18 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.18 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.18 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.15",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.17",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.18"
                          ],
                          target_hosts=[f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.15",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.17",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.18"]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.17",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.15 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.15 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.15 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.15 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.16 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.16 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.16 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.16 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.18 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.18 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.18 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.18 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.15",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.16",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.18"
                          ],
                          target_hosts=[f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.15",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.16",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.18"]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.18",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.15 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.15 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.15 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.15 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.16 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.16 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.16 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.16 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.17 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.17 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.17 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.17 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.15",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.16",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.17"
                          ],
                          target_hosts=[f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.15",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.16",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.17"]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.20 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.20 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.22 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.22 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.23 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.23 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.24 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.24 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.25 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.25 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.28 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.28 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28"],
                          target_hosts=[f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28"]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.19 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.19 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.22 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.22 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.23 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.23 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.24 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.24 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.25 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.25 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.28 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.28 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28"],
                          target_hosts=[f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28"]
                          ),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.19 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.19 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.20 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.20 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.23 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.23 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.24 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.24 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.28 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.28 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28"],
                          target_hosts=[f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28"]
                          ),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.19 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.19 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.20 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.20 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.22 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.22 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.24 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.24 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.25 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.25 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.28 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.28 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28"],
                          target_hosts=[f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28"]
                          ),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > /dev/null "
                              "2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.19 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.19 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.20 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.20 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.22 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.22 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.23 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.23 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.25 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.25 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.28 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.28 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28"],
                          target_hosts=[f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28"]
                          ),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.19 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.19 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.20 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.20 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.22 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.22 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.23 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.23 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.24 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.24 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.28 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.28 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28"],
                          target_hosts=[f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28"]
                          ),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61:8080 > "
                              f"/dev/null 2>&1",
                              "(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {"
                              "constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.19 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.19 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.20 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.20 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.22 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.22 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.23 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.23 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.24 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.24 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.25 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.25 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25",
                                     f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19"],
                          target_hosts=[f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25",
                                        f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19"]
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
    emulation_config = EmulationConfig(agent_ip=f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                                       agent_username=constants.CSLE_ADMIN.USER,
                                       agent_pw=constants.CSLE_ADMIN.PW, server_connection=False)
    TrafficGenerator.create_traffic_scripts(traffic_config=traffic_config, emulation_config=emulation_config,
                                            sleep_time=1)
