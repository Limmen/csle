import os
from csle_common.dao.container_config.traffic_config import TrafficConfig
from csle_common.dao.container_config.node_traffic_config import NodeTrafficConfig
from csle_common.util.experiments_util import util
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.config.generator.traffic_generator import TrafficGenerator
import csle_common.constants.constants as constants


def default_traffic_generators(network_id: int = 5) -> TrafficConfig:
    """
    :param network_id: the network id
    :return: the TrafficConfig of the emulation
    """
    traffic_generators = [
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.254",
                          commands=[
                              # f"timeout 120 sudo nmap -sS -p- --min-rate 100000 --max-retries 1 -T5 -n {
                              # constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}{
                              # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sP --min-rate 100000 --max-retries 1 -T5 -n {
                              # constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}{
                              # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sU -p- --min-rate 100000 --max-retries 1 -T5 -n {
                              # constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}{
                              # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sT -p- --min-rate 100000 --max-retries 1 -T5 -n {
                              # constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}{
                              # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sF -p- --min-rate 100000 --max-retries 1 -T5 -n {
                              # constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}{
                              # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sN -p- --min-rate 100000 --max-retries 1 -T5 -n {
                              # constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}{
                              # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sX -p- --min-rate 100000 --max-retries 1 -T5 -n {
                              # constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}{
                              # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -O --osscan-guess --max-os-tries 1 --min-rate 100000
                              # --max-retries 1 -T5 -n {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}{
                              # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap --script=http-grep --min-rate 100000 --max-retries 1 -T5 -n
                              # {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}{
                              # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              # f"timeout 120 sudo nmap -sv -sC --script=finger --min-rate 100000 --max-retries 1 -T5
                              # -n {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}{
                              # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2 > /dev/null 2>&1 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2:80 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null 2>&1 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > /dev/null 2>&1",
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
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2:80 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79:8080 > "
                              f"/dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2:80 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79:8080 > "
                              f"/dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.191"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54 > /dev/null 2>&1",
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
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2:80 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7 > /dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.101 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.101 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.74 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61:8080 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > /dev/null 2>&1"
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
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2:80 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 > /dev/null 2>&1",
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
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2:80 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.74 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61:8080 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62:8080 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62",
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
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2:80 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79:8080 > "
                              f"/dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2:80 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.101 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.101 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61:8080 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62:8080 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62 > /dev/null 2>&1"
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
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2:80 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.74 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2:80 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.21 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 ftp {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7 > /dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.101 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.101 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101 -p "
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.74 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61:8080 > "
                              f"/dev/null 2>&1",
                              f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7"
                          ])
    ]
    traffic_conf = TrafficConfig(node_traffic_configs=traffic_generators)
    return traffic_conf


# Generates the traffic.json configuration file
if __name__ == '__main__':
    network_id = 5
    if not os.path.exists(util.default_traffic_path()):
        TrafficGenerator.write_traffic_config(default_traffic_generators(network_id=5))
    traffic_config = util.read_traffic_config(util.default_traffic_path())
    emulation_config = EmulationConfig(agent_ip=f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                                       agent_username=constants.CSLE_ADMIN.USER,
                                       agent_pw=constants.CSLE_ADMIN.PW, server_connection=False)
    TrafficGenerator.create_traffic_scripts(traffic_config=traffic_config, emulation_config=emulation_config,
                                            sleep_time=1)
