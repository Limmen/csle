from typing import List, Tuple
from gym_pycr_pwcrack.dao.container_config.vulnerability_type import VulnType
from gym_pycr_pwcrack.envs.config.generator.topology_generator import TopologyGenerator
from gym_pycr_pwcrack.envs.config.generator.vuln_generator import VulnerabilityGenerator
from gym_pycr_pwcrack.envs.config.generator.flags_generator import FlagsGenerator
from gym_pycr_pwcrack.envs.config.generator.users_generator import UsersGenerator
from gym_pycr_pwcrack.envs.config.generator.container_generator import ContainerGenerator
import os
import re
import json

class EnvConfigGenerator:

    @staticmethod
    def generate(num_nodes : int, subnet_prefix : str, num_flags: int, max_num_users: int,
                 container_pool: List[Tuple[str, str]], gw_vuln_compatible_containers: List[Tuple[str, str]],
                 pw_vuln_compatible_containers: List[Tuple[str, str]], subnet_id : int,
                 agent_containers, router_containers):
        adj_matrix, gws, topology, agent_ip, router_ip = TopologyGenerator.generate(num_nodes=num_nodes,
                                                                                    subnet_prefix=subnet_prefix)
        vulnerabilities = VulnerabilityGenerator.generate(topology=topology, gateways=gws, agent_ip=agent_ip,
                                                          subnet_prefix=subnet_prefix,
                                                          num_flags=num_flags, access_vuln_types=[VulnType.WEAK_PW],
                                                          router_ip=router_ip)
        users = UsersGenerator.generate(max_num_users=max_num_users, topology=topology, agent_ip=agent_ip)
        flags = FlagsGenerator.generate(vuln_cfg=vulnerabilities, num_flags=num_flags)
        containers = ContainerGenerator.generate(
            topology=topology, vuln_cfg=vulnerabilities, gateways=gws, container_pool=container_pool,
        gw_vuln_compatible_containers=gw_vuln_compatible_containers,
            pw_vuln_compatible_containers=pw_vuln_compatible_containers, subnet_id=subnet_id, num_flags=num_flags,
            agent_ip=agent_ip, router_ip=router_ip, agent_containers=agent_containers,
            router_containers=router_containers, subnet_prefix=subnet_prefix)

        return topology, vulnerabilities, users, flags, containers

    @staticmethod
    def list_docker_networks():
        cmd = "docker network ls"
        stream = os.popen(cmd)
        networks = stream.read()
        networks = networks.split("\n")
        networks = list(map(lambda x: x.split(), networks))
        networks = list(filter(lambda x: len(x) > 1, networks))
        networks = list(map(lambda x: x[1], networks))
        networks = list(filter(lambda x: re.match(r"pycr_net_\d", x), networks))
        network_ids = list(map(lambda x: int(x.replace("pycr_net_", "")), networks))
        return networks, network_ids


    @staticmethod
    def list_running_containers():
        cmd = "docker ps -q"
        stream = os.popen(cmd)
        running_containers = stream.read()
        running_containers = running_containers.split("\n")
        running_containers = list(filter(lambda x: x!= "", running_containers))
        return running_containers


    @staticmethod
    def find_networks_in_use(containers: List[str]):
        networks_in_use = []
        network_ids_in_use = []
        for c in containers:
            cmd = "docker inspect " + c + " -f '{{json .NetworkSettings.Networks }}'"
            stream = os.popen(cmd)
            network_info = stream.read()
            network_info = json.loads(network_info)
            for k in network_info.keys():
                if re.match(r"pycr_net_\d", k):
                   networks_in_use.append(k)
                   network_ids_in_use.append(int(k.replace("pycr_net_", "")))

        return networks_in_use, network_ids_in_use


if __name__ == '__main__':
    container_pool = [("ftp1", "0.0.1"), ("ftp2", "0.0.1"), ("honeypot1", "0.0.1"),
                      ("honeypot2", "0.0.1"),
                      ("ssh1", "0.0.1"), ("ssh2", "0.0.1"),
                      ("ssh3", "0.0.1"), ("telnet1", "0.0.1"), ("telnet2", "0.0.1"), ("telnet3", "0.0.1")]
    gw_vuln_compatible_containers = [("ssh1", "0.0.1"), ("ssh2", "0.0.1"), ("ssh3", "0.0.1"), ("telnet1", "0.0.1"),
                                     ("telnet2", "0.0.1"), ("telnet3", "0.0.1")]
    pw_vuln_compatible_containers = [("ftp1", "0.0.1"), ("ftp2", "0.0.1")]
    agent_containers = [(("hacker_kali1", "0.0.1"))]
    router_containers = [("router1", "0.0.1"), ("router2", "0.0.1")]
    # topology, vulnerabilities, users, flags, containers = EnvConfigGenerator.generate(
    #     num_nodes = 10, subnet_prefix="172.18.2.", num_flags=3, max_num_users=2, container_pool=container_pool,
    #     gw_vuln_compatible_containers=gw_vuln_compatible_containers,
    #     pw_vuln_compatible_containers=pw_vuln_compatible_containers, subnet_id=2, agent_containers=agent_containers,
    #     router_containers=router_containers)
    #EnvConfigGenerator.list_docker_networks()
    containers = EnvConfigGenerator.list_running_containers()
    EnvConfigGenerator.find_networks_in_use(containers)
    
