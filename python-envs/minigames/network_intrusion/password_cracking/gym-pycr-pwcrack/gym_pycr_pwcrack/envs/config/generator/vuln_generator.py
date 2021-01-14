from typing import List
import random
import numpy as np
from gym_pycr_pwcrack.dao.container_config.topology import Topology
from gym_pycr_pwcrack.dao.container_config.node_firewall_config import NodeFirewallConfig
from gym_pycr_pwcrack.dao.container_config.node_vulnerability_config import NodeVulnerabilityConfig
from gym_pycr_pwcrack.dao.container_config.vulnerabilities_config import VulnerabilitiesConfig
from gym_pycr_pwcrack.dao.container_config.pw_vulnerability_config import PwVulnerabilityConfig
from gym_pycr_pwcrack.dao.container_config.vulnerability_type import VulnType
from gym_pycr_pwcrack.envs.config.generator.topology_generator import TopologyGenerator
from gym_pycr_pwcrack.envs.config.generator.generator_util import GeneratorUtil
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.envs.logic.cluster.cluster_util import ClusterUtil
from gym_pycr_pwcrack.util.experiments_util import util

class VulnerabilityGenerator:


    def __init__(self):
        pass


    @staticmethod
    def shortlist():
        names_shortlist = ["admin", "test", "guest", "info", "adm", "mysql", "user", "administrator",
                           "oracle", "ftp", "pi", "puppet", "ansible", "ec2-user", "vagrant", "azureuser"]
        return names_shortlist


    @staticmethod
    def generate(topology: Topology, gateways : dict, agent_ip : str, router_ip: str, subnet_prefix :str, num_flags,
                 access_vuln_types : List[VulnType]) -> VulnerabilitiesConfig:
        vulnerabilities = []
        vulnerable_nodes = set()

        # Start by creating necessary vulns
        for gw in gateways.values():
            ip = subnet_prefix + str(gw)
            if ip != agent_ip and ip != router_ip:
                vuln_idx = random.randint(0,len(access_vuln_types)-1)
                vuln_type = access_vuln_types[vuln_idx]
                if vuln_type == VulnType.WEAK_PW:
                    for node in topology.node_configs:
                        if node.ip == ip:
                            vuln_cfg = VulnerabilityGenerator.pw_vuln(node)
                            vulnerabilities.append(vuln_cfg)
                            vulnerable_nodes.add(ip)
                else:
                    raise ValueError("Unrecognized vulnerability type")


        for node in topology.node_configs:
            # Create vuln necessary for flags
            if len(vulnerable_nodes) < num_flags:
                if node.ip != agent_ip and node.ip != router_ip and node.ip not in vulnerable_nodes:
                    vuln_idx = random.randint(0, len(access_vuln_types) - 1)
                    vuln_type = access_vuln_types[vuln_idx]
                    if vuln_type == VulnType.WEAK_PW:
                        vuln_cfg = VulnerabilityGenerator.pw_vuln(node)
                        vulnerabilities.append(vuln_cfg)
                        vulnerable_nodes.add(node.ip)
                    else:
                        raise ValueError("Unrecognized vulnerability type")

            # Randomly create vuln
            if node.ip != agent_ip and node.ip != router_ip and node.ip not in vulnerable_nodes:
                if np.random.rand() < 0.2:
                    vuln_idx = random.randint(0, len(access_vuln_types) - 1)
                    vuln_type = access_vuln_types[vuln_idx]
                    if vuln_type == VulnType.WEAK_PW:
                        vuln_cfg = VulnerabilityGenerator.pw_vuln(node)
                        vulnerabilities.append(vuln_cfg)
                        vulnerable_nodes.add(node.ip)
                    else:
                        raise ValueError("Unrecognized vulnerability type")

        vulns_cfg = VulnerabilitiesConfig(vulnerabilities=vulnerabilities)
        return vulns_cfg, vulnerable_nodes


    @staticmethod
    def pw_vuln(node: NodeFirewallConfig) -> PwVulnerabilityConfig:
        pw_shortlist = VulnerabilityGenerator.shortlist()
        pw_idx = random.randint(0, len(pw_shortlist)-1)
        u = pw_shortlist[pw_idx]
        pw = pw_shortlist[pw_idx]
        vuln_config = PwVulnerabilityConfig(node_ip = node.ip, vuln_type=VulnType.WEAK_PW, username=u, pw=pw, root=True)
        return vuln_config


    @staticmethod
    def create_vulns(vuln_cfg: VulnerabilitiesConfig, cluster_config: ClusterConfig):
        vulnerabilities = vuln_cfg.vulnerabilities
        for vuln in vulnerabilities:
            GeneratorUtil.connect_admin(cluster_config=cluster_config, ip=vuln.node_ip)
            if vuln.vuln_type == VulnType.WEAK_PW:
                cmd = "ls /home"
                o, e, _ = ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)
                users_w_home = o.decode().split("\n")
                users_w_home = list(filter(lambda x: x != '', users_w_home))

                for user in users_w_home:
                    if user != "pycr_admin" and user == vuln.username:
                        cmd = "sudo deluser {}".format(user)
                        ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)
                        cmd = "sudo rm -rf /home/{}".format(user)
                        ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

                cmd = "sudo deluser {}".format(vuln.username)
                ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

                if vuln.root:
                    cmd = "sudo useradd -rm -d /home/{} -s /bin/bash -g root -G sudo -p \"$(openssl passwd -1 '{}')\" {}".format(
                        vuln.username, vuln.pw, vuln.username)
                else:
                    cmd = "sudo useradd -rm -d /home/{} -s /bin/bash -p \"$(openssl passwd -1 '{}')\" {}".format(
                        vuln.username, vuln.pw, vuln.username)
                o, e, _ = ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

            else:
                raise ValueError("Vulnerability type not recognized")


    @staticmethod
    def write_vuln_config(vulns_cfg: VulnerabilitiesConfig, path: str = None) -> None:
        """
        Writes the default configuration to a json file

        :param vulns_cfg: the config to write
        :param path: the path to write the configuration to
        :return: None
        """
        path = util.default_vulnerabilities_path(out_dir=path)
        util.write_vulns_config_file(vulns_cfg, path)


if __name__ == '__main__':
    adj_matrix, gws, topology, agent_ip, router_ip = TopologyGenerator.generate(num_nodes=10, subnet_prefix="172.18.2.")
    vulnerabilities = VulnerabilityGenerator.generate(topology=topology, gateways=gws, agent_ip=agent_ip, subnet_prefix="172.18.2.",
                                    num_flags = 3, access_vuln_types=[VulnType.WEAK_PW])
    print(vulnerabilities)




