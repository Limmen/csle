import os
from csle_common.dao.container_config.traffic_config import TrafficConfig
from csle_common.dao.container_config.node_traffic_config import NodeTrafficConfig
from csle_common.util.experiments_util import util
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.config.generator.traffic_generator import TrafficGenerator
import csle_common.constants.constants as constants


def default_traffic_generators(network_id: int = 8) -> TrafficConfig:
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
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
                              f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.42/login.php > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.42 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 -c "
                              "csle_ctf1234",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 -c "
                              "csle_ctf1234",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11 > /dev/null 2>&1",
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
                              f"timeout 15 ping {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > "
                              f"/dev/null 2>&1",
                              f"timeout 15 ping {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > "
                              f"/dev/null 2>&1",
                              f"timeout 15 ping {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42 > "
                              f"/dev/null 2>&1",
                              f"timeout 15 ping {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > "
                              f"/dev/null 2>&1",
                              f"timeout 15 ping {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 > "
                              f"/dev/null 2>&1",
                              f"timeout 15 ping {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > "
                              f"/dev/null 2>&1",
                              f"timeout 15 ping {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71 > "
                              f"/dev/null 2>&1",
                              f"timeout 15 ping {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11 > "
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
                              f"> /dev/null 2>&1",
                              f"timeout 25 traceroute {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 "
                              f"> /dev/null 2>&1",
                              f"timeout 25 traceroute {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 "
                              f"> /dev/null 2>&1",
                              f"timeout 25 traceroute {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42 "
                              f"> /dev/null 2>&1",
                              f"timeout 25 traceroute {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 "
                              f"> /dev/null 2>&1",
                              f"timeout 25 traceroute {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 "
                              f"> /dev/null 2>&1",
                              f"timeout 25 traceroute {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 "
                              f"> /dev/null 2>&1",
                              f"timeout 25 traceroute {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71 "
                              f"> /dev/null 2>&1",
                              f"timeout 25 traceroute {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11 "
                              f"> /dev/null 2>&1"
                          ],
                          jumphosts=[],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.191", commands=[],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.51",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.52",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.53",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.55",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.56",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.57",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.58",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.59",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.60",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62"
                          ],
                          target_hosts=[]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10", commands=[
            f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2 > /dev/null 2>&1",
            f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2:80 > /dev/null 2>&1",
            f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null 2>&1",
            f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null 2>&1",
            f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3 > /dev/null 2>&1",
            f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 > /dev/null 2>&1",
            f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 -c csle_ctf1234 "
            f"> /dev/null 2>&1",
            f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 > "
            f"/dev/null 2>&1",
            f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21 -p 5432 > /dev/null "
            f"2>&1",
            f"timeout 5 ftp {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > /dev/null 2>&1",
            f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > /dev/null 2>&1",
            f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79:8080 > /dev/null 2>&1",
            f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
            f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
            f"{network_id}.19 > /dev/null 2>&1",
            f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > /dev/null 2>&1",
            f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > /dev/null 2>&1",
            f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 -c csle_ctf1234 "
            f"> /dev/null 2>&1",
            f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42 > /dev/null 2>&1",
            f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42/login.php > /dev/null "
            f"2>&1",
            f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42 > "
            f"/dev/null 2>&1",
            f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > /dev/null 2>&1",
            "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 -c csle_ctf1234",
            f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > /dev/null 2>&1",
            f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 > /dev/null 2>&1",
            "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 -c csle_ctf1234",
            f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > /dev/null 2>&1",
            f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > /dev/null 2>&1",
            f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71 > /dev/null 2>&1",
            f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71:8080 > /dev/null 2>&1",
            f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11 > /dev/null 2>&1"
        ], jumphosts=[
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
            f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.51",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.52",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.53",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.55",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.56",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.57",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.58",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.59",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.60",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62"
        ], target_hosts=[
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.51",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.52",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.53",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.55",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.56",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.57",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.58",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.59",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.60",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
            f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62"]),
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
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
                              f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.31 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.42/login.php > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.42 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 -c "
                              "csle_ctf1234",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 -c "
                              "csle_ctf1234",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.52 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.52:80 > "
                              f"/dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.52"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.52"
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
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
                              f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.31 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.42/login.php > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.42 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 -c "
                              "csle_ctf1234",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 -c "
                              "csle_ctf1234",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              [f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                               f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                               f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                               f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                               f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                               f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
                               f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31",
                               f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
                               f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
                               f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
                               f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
                               f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71",
                               f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11"]
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11"
                          ]),
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
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
                              f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.31 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.42/login.php > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.42 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 -c "
                              "csle_ctf1234",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 -c "
                              "csle_ctf1234",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11"
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
                              f"5432 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
                              f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.31 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.42/login.php > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.42 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 -c "
                              "csle_ctf1234",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 -c "
                              "csle_ctf1234",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.51 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.51:80 > "
                              f"/dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.51"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.51"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
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
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.31 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.42/login.php > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.42 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 -c "
                              "csle_ctf1234",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 -c "
                              "csle_ctf1234",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31",
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
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
                              f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.42/login.php > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.42 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 -c "
                              "csle_ctf1234",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 -c "
                              "csle_ctf1234",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
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
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
                              f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.31 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 -c "
                              "csle_ctf1234",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 -c "
                              "csle_ctf1234",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
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
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
                              f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.31 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.42/login.php > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.42 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 -c "
                              "csle_ctf1234",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
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
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
                              f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.31 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.42/login.php > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.42 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 -c "
                              "csle_ctf1234",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.51 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.51:80 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.53 > /dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.53 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.53 > /dev/null 2>&1",
                              f"timeout 5 psql -h {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.53 -p "
                              f"5432 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.53",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.51"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.53",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.51"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
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
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
                              f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.31 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.42/login.php > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.42 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 -c "
                              "csle_ctf1234",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 -c "
                              "csle_ctf1234",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71",
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
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
                              f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.31 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.42/login.php > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.42 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 -c "
                              "csle_ctf1234",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 -c "
                              "csle_ctf1234",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11",
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
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
                              f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.31 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.42/login.php > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.42 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 -c "
                              "csle_ctf1234",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 -c "
                              "csle_ctf1234",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71:8080 > "
                              f"/dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.51",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 -c "
                              "csle_ctf1234",
                              f"timeout 5 ftp {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79:8080 > "
                              f"/dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.52",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2:80 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54 > /dev/null 2>&1",
                              f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.53",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82 -c "
                              "csle_ctf1234"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.52 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.52:80 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.55 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.55 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.55 -c csle_ctf1234 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.52",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.55"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.52",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.55"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.55",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54 > /dev/null 2>&1",
                              f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.56 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.56/login.php > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.56 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.56"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.56"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.56",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.55 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.55 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.55 -c csle_ctf1234 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.57 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.57 -c "
                              "csle_ctf1234",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.57 > "
                              f"/dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.55",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.57"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.55",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.57"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.57",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.56 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.56/login.php > /dev/null 2>&1",
                              f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}"
                              f"{network_id}.56 > /dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.58 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.58 -c "
                              "csle_ctf1234"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.56",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.58"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.56",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.58"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.58",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.57 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.57 -c "
                              "csle_ctf1234",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.57 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.59 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.59 > "
                              f"/dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.57",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.59"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.57",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.59"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.59",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.58 > /dev/null 2>&1",
                              "snmpwalk -v2c {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.58 -c "
                              "csle_ctf1234",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.60 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.60:8080 > "
                              f"/dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.58",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.60"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.58",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.60"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.60",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.59 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.59 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.59",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.59",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.60 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.60:8080 > "
                              f"/dev/null 2>&1",
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62 > /dev/null 2>&1",
                              f"timeout 5 curl {constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62:80 > "
                              f"/dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.60",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.60",
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62"
                          ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62",
                          commands=[
                              f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61 > /dev/null 2>&1"
                          ],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61"
                          ],
                          target_hosts=[
                              f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61"
                          ])
    ]
    traffic_conf = TrafficConfig(node_traffic_configs=traffic_generators)
    return traffic_conf


# Generates the traffic.json configuration file
if __name__ == '__main__':
    network_id = 8
    if not os.path.exists(util.default_traffic_path()):
        TrafficGenerator.write_traffic_config(default_traffic_generators(network_id=network_id))
    traffic_config = util.read_traffic_config(util.default_traffic_path())
    emulation_config = EmulationConfig(agent_ip=f"{constants.CSLE.CSLE_EXTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                                       agent_username=constants.CSLE_ADMIN.USER,
                                       agent_pw=constants.CSLE_ADMIN.PW, server_connection=False)
    TrafficGenerator.create_traffic_scripts(traffic_config=traffic_config, emulation_config=emulation_config,
                                            sleep_time=1)
