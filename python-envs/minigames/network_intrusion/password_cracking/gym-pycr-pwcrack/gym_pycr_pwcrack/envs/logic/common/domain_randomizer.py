from typing import List
import random
import numpy as np
from gym_pycr_pwcrack.dao.network.network_config import NetworkConfig
from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.envs.config.generator.topology_generator import TopologyGenerator
from gym_pycr_pwcrack.envs.config.generator.vuln_generator import VulnerabilityGenerator
from gym_pycr_pwcrack.envs.config.generator.users_generator import UsersGenerator
from gym_pycr_pwcrack.envs.config.generator.flags_generator import FlagsGenerator
from gym_pycr_pwcrack.dao.container_config.vulnerability_type import VulnType
from gym_pycr_pwcrack.envs.logic.common.node_randomizer import NodeRandomizer
from gym_pycr_pwcrack.dao.domain_randomization.randomization_space import RandomizationSpace
from gym_pycr_pwcrack.envs.config.domain_randomization.base_randomization_space import BaseRandomizationSpace
from gym_pycr_pwcrack.dao.network.flag import Flag

class DomainRandomizer:

    @staticmethod
    def generate_randomization_space(network_confs: List[NetworkConfig], min_num_nodes : int=4,
                                     max_num_nodes : int=4, min_num_flags : int = 1, max_num_flags : int = 1,
                                     min_num_users: int = 1, max_num_users : int = 1,
                                     services = None, vulnerabilities = None, os = None,
                                     use_base_randomization: bool = False) -> RandomizationSpace:
        if services is None:
            services = set()
        if vulnerabilities is None:
            vulnerabilities = set()
        if os is None:
            os = set()
        if use_base_randomization:
            services = services.union(set(BaseRandomizationSpace.base_services()))
            os = os.union(BaseRandomizationSpace.base_os())
            vulnerabilities = vulnerabilities.union(BaseRandomizationSpace.base_vulns())
        min_num_nodes = min_num_nodes
        max_num_nodes = max_num_nodes
        min_num_flags=min_num_flags
        max_num_flags=max_num_flags
        min_num_users=min_num_users
        max_num_users=max_num_users
        for nc in network_confs:
            node_services = set()
            node_vulns = set()
            for node in nc.nodes:
                node_services.update(node.services)
                node_vulns.update(node.vulnerabilities)
                os.add(node.os)
                if len(node.credentials) > max_num_users:
                    max_num_users = len(node.credentials)
                if len(node.flags) > max_num_flags:
                    max_num_flags = len(node.flags)

            services = services.union(node_services)
            vulnerabilities = vulnerabilities.union(node_vulns)
            if len(nc.nodes) > max_num_nodes:
                max_num_nodes = len(nc.nodes)

        services = list(services)
        vulnerabilities = list(vulnerabilities)
        os = list(os)
        filtered_services = []
        services_names = set()
        for s in services:
            if s.name not in services_names:
                s = s.copy()
                s.port = int(s.port)
                s.credentials = []
                filtered_services.append(s)
                services_names.add(s.name)
        filtered_vulnerabilities = []
        vulnerabilities_names = set()
        for v in vulnerabilities:
            if v.name not in vulnerabilities_names:
                v = v.copy()
                v.port = int(v.port)
                v.credentials = []
                filtered_vulnerabilities.append(v)
                vulnerabilities_names.add(v.name)
        r_space = RandomizationSpace(services=filtered_services, vulnerabilities=filtered_vulnerabilities, os=os,
                                     min_num_nodes=min_num_nodes, max_num_nodes=max_num_nodes,
                                     min_num_flags=min_num_flags, max_num_flags=max_num_flags,
                                     min_num_users=min_num_users, max_num_users=max_num_users)
        print("randomization space created, num nodes:{}, num services:{}, num_vulns:{}, os:{}".format(max_num_nodes, len(services), len(vulnerabilities),
                                                                                                       len(os)))
        return r_space

    @staticmethod
    def randomize(subnet_prefix: str, network_ids: List, r_space: RandomizationSpace, env_config: EnvConfig) -> NetworkConfig:
        subnet_id = network_ids[random.randint(0, len(network_ids) - 1)]
        num_nodes = random.randint(r_space.min_num_nodes, r_space.max_num_nodes)
        subnet_prefix = subnet_prefix + str(subnet_id) + "."
        num_flags = random.randint(r_space.min_num_flags, min(r_space.max_num_flags, num_nodes - 3))
        num_users = random.randint(r_space.min_num_users, r_space.max_num_users)
        adj_matrix, gws, topology, agent_ip, router_ip, node_id_d, node_id_d_inv = \
            TopologyGenerator.generate(num_nodes=num_nodes, subnet_prefix=subnet_prefix)
        vulnerabilities, vulnerable_nodes = VulnerabilityGenerator.generate(topology=topology, gateways=gws, agent_ip=agent_ip,
                                                          subnet_prefix=subnet_prefix,
                                                          num_flags=num_flags, access_vuln_types=[VulnType.WEAK_PW],
                                                          router_ip=router_ip)
        users_config = UsersGenerator.generate(max_num_users=r_space.max_num_users, topology=topology, agent_ip=agent_ip)
        flags_config = FlagsGenerator.generate(vuln_cfg=vulnerabilities, num_flags=num_flags)
        randomized_nodes = []
        agent_reachable = set()
        ids_router = False
        if np.random.rand() < 0.5:
            ids_router = True
        for node in topology.node_configs:
            reachable = set()
            ip_id = int(node.ip.rsplit(".", 1)[-1])
            id = node_id_d[ip_id]
            gateway = False
            if ip_id in gws.values():
                gateway = True
            for i in range(len(adj_matrix[id])):
                if adj_matrix[id][i] == 1:
                    node_ip_suffix = node_id_d_inv[i]
                    node_ip = subnet_prefix + str(node_ip_suffix)
                    reachable.add(node_ip)
            users = None
            for node_users in users_config.users:
                if node_users.ip == node.ip:
                    users = node_users
            flags = None
            for flags_users in flags_config.flags:
                if flags_users.ip == node.ip:
                    flags = flags_users
            vulns = None
            for vulns_users in vulnerabilities.vulnerabilities:
                if vulns_users.node_ip == node.ip:
                    vulns = vulns_users
            router = (node.ip == router_ip)
            agent = (node.ip == agent_ip)
            if agent:
                agent_reachable=reachable
            n = NodeRandomizer.randomize(ip=node.ip, id=id, reachable=reachable, router=router, agent=agent, r_space=r_space,
                                     users_config=users, flags_config=flags, vulns_config=vulns, gateway=gateway)
            randomized_nodes.append(n)

        flags_lookup = {}
        for fl in flags_config.flags:
            if len(fl.flags) > 0:
                flags_lookup[(fl.ip, fl.flags[0][0].replace(".txt", ""))] = Flag(name=fl.flags[0][1],
                                                                                 path=fl.flags[0][2],
                                                                                 id=fl.flags[0][3],
                                                                                 requires_root=fl.flags[0][4],
                                                                                 score=fl.flags[0][5])
        subnet_mask = subnet_prefix + "0/24"
        randomized_network_conf = NetworkConfig(subnet_mask=subnet_mask, nodes=randomized_nodes, adj_matrix=adj_matrix,
                                     flags_lookup=flags_lookup, agent_reachable=agent_reachable,
                                                vulnerable_nodes=vulnerable_nodes)
        env_config = env_config.copy()
        env_config.network_conf=randomized_network_conf
        env_config.router_ip=router_ip
        env_config.hacker_ip=agent_ip
        env_config.ids_router=ids_router
        env_config.num_flags = len(flags_lookup)
        env_config.blacklist_ips = [subnet_prefix + ".1"]
        #env_config.num_nodes = len(randomized_nodes)
        for a in env_config.action_conf.actions:
            if a.subnet:
                a.ip = subnet_mask
        return randomized_network_conf, env_config

    @staticmethod
    def perturb(network_conf: NetworkConfig):
        pass



if __name__ == '__main__':
    DomainRandomizer.randomize(network_conf=None, min_num_nodes=5, max_num_nodes=10, min_num_flags=1, max_num_flags=5,
                               min_num_users=3, max_num_users=5, subnet_prefix="172.18.",
                               network_ids=list(range(1,254)))