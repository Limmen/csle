import os
from csle_common.dao.container_config.traffic_config import TrafficConfig
from csle_common.dao.container_config.node_traffic_config import NodeTrafficConfig
from csle_common.util.experiments_util import util
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.config.generator.traffic_generator import TrafficGenerator
import csle_common.constants.constants as constants


def default_traffic_generators(network_id: int = 10) -> TrafficConfig:
    """
    :param: network_id: the network id
    :return: the TrafficConfig of the emulation
    """
    traffic_generators = [
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.254",
            commands=[
                # f"timeout 120 sudo nmap -sS -p- --min-rate 100000 --max-retries 1 -T5 -n {
                # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{
                # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                # f"timeout 120 sudo nmap -sP --min-rate 100000 --max-retries 1 -T5 -n {
                # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{
                # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                # f"timeout 120 sudo nmap -sU -p- --min-rate 100000 --max-retries 1 -T5 -n {
                # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{
                # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                # f"timeout 120 sudo nmap -sT -p- --min-rate 100000 --max-retries 1 -T5 -n {
                # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{
                # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                # f"timeout 120 sudo nmap -sF -p- --min-rate 100000 --max-retries 1 -T5 -n {
                # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{
                # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                # f"timeout 120 sudo nmap -sN -p- --min-rate 100000 --max-retries 1 -T5 -n {
                # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{
                # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                # f"timeout 120 sudo nmap -sX -p- --min-rate 100000 --max-retries 1 -T5 -n {
                # constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{
                # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                # f"timeout 120 sudo nmap -O --osscan-guess --max-os-tries 1 --min-rate 100000
                # --max-retries 1 -T5 -n {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{
                # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                # f"timeout 120 sudo nmap --script=http-grep --min-rate 100000 --max-retries 1 -T5 -n
                # {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{
                # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                # f"timeout 120 sudo nmap -sv -sC --script=finger --min-rate 100000 --max-retries 1 -T5
                # -n {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}{
                # constants.CSLE.CSLE_SUBNETMASK} > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1 > "
                f"/dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1 > "
                f"/dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p "
                f"5432 > /dev/null 2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42/login.php > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c "
                "csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c "
                "csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > "
                f"/dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > "
                f"/dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > "
                f"/dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10 > "
                f"/dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > "
                f"/dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > "
                f"/dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > "
                f"/dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > "
                f"/dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > "
                f"/dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > "
                f"/dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > "
                f"/dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > "
                f"/dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 "
                f"> /dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 "
                f"> /dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 "
                f"> /dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 "
                f"> /dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10 "
                f"> /dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 "
                f"> /dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 "
                f"> /dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 "
                f"> /dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 "
                f"> /dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 "
                f"> /dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 "
                f"> /dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 "
                f"> /dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 "
                f"> /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ],
            jumphosts=[],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.191", commands=[],
                          jumphosts=[
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                              f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
                          ],
                          target_hosts=[]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
            commands=
            [
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -c csle_ctf1234 "
                f"> /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > "
                f"/dev/null 2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p 5432 > /dev/null "
                f"2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 -c csle_ctf1234 "
                f"> /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42/login.php > /dev/null "
                f"2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ], jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ], target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
            commands=[
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p "
                f"5432 > /dev/null 2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > "
                f"/dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.31 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42/login.php > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c "
                "csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c "
                "csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ],
            jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
            commands=[
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p "
                f"5432 > /dev/null 2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > "
                f"/dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.31 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42/login.php > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c "
                "csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c "
                "csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ],
            jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
            commands=[
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > "
                f"/dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.31 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42/login.php > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c "
                "csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c "
                "csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ],
            jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
            commands=[
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p "
                f"5432 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > "
                f"/dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.31 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42/login.php > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c "
                "csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c "
                "csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ],
            jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
            commands=[
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p "
                f"5432 > /dev/null 2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > "
                f"/dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.31 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42/login.php > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c "
                "csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c "
                "csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ],
            jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
            commands=[
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p "
                f"5432 > /dev/null 2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42/login.php > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c "
                "csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c "
                "csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ],
            jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
            commands=[
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p "
                f"5432 > /dev/null 2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > "
                f"/dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.31 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c "
                "csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c "
                "csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ],
            jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
            commands=[
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p "
                f"5432 > /dev/null 2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > "
                f"/dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.31 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42/login.php > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c "
                "csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ],
            jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
            commands=[
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p "
                f"5432 > /dev/null 2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > "
                f"/dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.31 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42/login.php > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c "
                "csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ],
            jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
            commands=[
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p "
                f"5432 > /dev/null 2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > "
                f"/dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.31 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42/login.php > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c "
                "csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c "
                "csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ],
            jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
            commands=[
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p "
                f"5432 > /dev/null 2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > "
                f"/dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.31 -c csle_ctf1234 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42/login.php > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c "
                "csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c "
                "csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ],
            jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
            commands=[
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -c csle_ctf1234 > "
                f"/dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null "
                f"2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p 5432 > /dev/null 2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 -c csle_ctf1234 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42/login.php > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null "
                f"2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000 "
                f"> /dev/null 2>&1",
                f"timeout 5 curl "
                "--header \"Content-Type: application/json\" --request POST \
                --data $'{\"application\": \"pengine_sandbox\", "
                "\"ask\": \"problem(1, Rows), sudoku(Rows)\", \"chunk\": 1, \"destroy\": true, "
                "\"format\":\"json\", \"src_text\": "
                "\"problem(1, [[_,_,_,_,_,_,_,_,_],[_,_,_,_,_,3,_,8,5],"
                "[_,_,1,_,2,_,_,_,_],[_,_,_,5,_,7,_,_,_],[_,_,4,_,_,_,1,_,_],"
                "[_,9,_,_,_,_,_,_,_],[5,_,_,_,_,_,_,7,3],[_,_,2,_,1,_,_,_,_],"
                "[_,_,_,_,4,_,_,_,9]]).\n\"}' "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104:4000/pengine/create"
            ],
            jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104"
            ]),
        NodeTrafficConfig(
            ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.104",
            commands=[
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2:80 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > "
                f"/dev/null 2>&1",
                f"(sleep 2; echo test; sleep 2; echo test; sleep 3;) | telnet "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -c csle_ctf1234 > "
                f"/dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 > /dev/null "
                f"2>&1",
                f"timeout 5 psql -h {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21 -p 5432 > /dev/null 2>&1",
                f"timeout 5 ftp {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79:8080 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19 > /dev/null 2>&1",
                f"(sleep 2; echo testcsleuser; sleep 3;) | smbclient -L {constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                f"{network_id}.2.19 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 > /dev/null 2>&1",
                f"timeout 5 snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31 -c csle_ctf1234 > "
                f"/dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42/login.php > /dev/null 2>&1",
                f"timeout 10 /irc_login_test.sh {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42 > /dev/null "
                f"2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 -c csle_ctf1234",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 > /dev/null 2>&1",
                "snmpwalk -v2c {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82 -c csle_ctf1234",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71 > /dev/null 2>&1",
                f"timeout 5 curl {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71:8080 > /dev/null 2>&1",
                f"timeout 5 sshpass -p 'testcsleuser' ssh -oStrictHostKeyChecking=no "
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > /dev/null 2>&1",
                f"timeout 15 ping {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 > "
                f"/dev/null 2>&1",
                f"timeout 25 traceroute {constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11 "
                f"> /dev/null 2>&1"
            ],
            jumphosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.191",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11"
            ],
            target_hosts=[
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11"
            ])
    ]
    traffic_conf = TrafficConfig(node_traffic_configs=traffic_generators)
    return traffic_conf


# Generates the traffic.json configuration file
if __name__ == '__main__':
    network_id = 10
    if not os.path.exists(util.default_traffic_path()):
        TrafficGenerator.write_traffic_config(default_traffic_generators(network_id=network_id))
    traffic_config = util.read_traffic_config(util.default_traffic_path())
    emulation_config = EmulationConfig(agent_ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.191",
                                       agent_username=constants.CSLE_ADMIN.USER,
                                       agent_pw=constants.CSLE_ADMIN.PW, server_connection=False)
    TrafficGenerator.create_traffic_scripts(traffic_config=traffic_config, emulation_config=emulation_config,
                                            sleep_time=1)
