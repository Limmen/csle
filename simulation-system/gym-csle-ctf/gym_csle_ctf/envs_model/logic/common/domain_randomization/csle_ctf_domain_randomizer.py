from typing import List, Tuple
import random
import numpy as np
from csle_common.dao.network.network_config import NetworkConfig
from csle_common.envs_model.config.generator.topology_generator import TopologyGenerator
from csle_common.envs_model.config.generator.vuln_generator import VulnerabilityGenerator
from csle_common.envs_model.config.generator.users_generator import UsersGenerator
from csle_common.envs_model.config.generator.flags_generator import FlagsGenerator
from csle_common.dao.container_config.vulnerability_type import VulnType
from gym_csle_ctf.dao.domain_randomization.csle_ctf_randomization_space import CSLECTFRandomizationSpace
from csle_common.envs_model.config.domain_randomization.base_randomization_space import BaseRandomizationSpace
from csle_common.dao.network.flag import Flag
from csle_common.envs_model.logic.domain_randomization.csle_domain_randomizer import CSLEDomainRandomizer
from gym_csle_ctf.dao.network.env_config import CSLEEnvConfig
from gym_csle_ctf.envs_model.logic.common.domain_randomization.csle_ctf_node_randomizer import CSLECTFNodeRandomizer
from gym_csle_ctf.dao.domain_randomization.csle_ctf_randomization_space_config import CSLECTFRandomizationSpaceConfig
from gym_csle_ctf.dao.domain_randomization.csle_ctf_node_randomizer_config import CSLECTFNodeRandomizerConfig


class CSLECTFCSLEDomainRandomizer(CSLEDomainRandomizer):
    """
    Utility class for domain randomization to improve generalization performance
    """

    @staticmethod
    def generate_randomization_space(config: CSLECTFRandomizationSpaceConfig) -> CSLECTFRandomizationSpace:
        """
        Creates a randomization space according to the given parameters

        :param config: the randomization space config
        :return: the created randomization space
        """
        services = set()
        vulnerabilities = set()
        os = set()
        if config.os is None:
            os = set()
        if config.use_base_randomization:
            services = services.union(set(BaseRandomizationSpace.base_services()))
            os = os.union(BaseRandomizationSpace.base_os())
            vulnerabilities = vulnerabilities.union(BaseRandomizationSpace.base_vulns())
        min_num_nodes = config.min_num_nodes
        max_num_nodes = config.max_num_nodes
        min_num_flags=config.min_num_flags
        max_num_flags=config.max_num_flags
        min_num_users=config.min_num_users
        max_num_users=config.max_num_users
        for nc in config.network_confs:
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
        r_space = CSLECTFRandomizationSpace(CSLECTFRandomizationSpaceConfig(
            services=filtered_services, vulnerabilities=filtered_vulnerabilities, os=os,
            min_num_nodes=min_num_nodes, max_num_nodes=max_num_nodes,
            min_num_flags=min_num_flags, max_num_flags=max_num_flags,
            min_num_users=min_num_users, max_num_users=max_num_users, network_confs=config.network_confs))
        return r_space


    @staticmethod
    def randomize(subnet_prefix: str, network_ids: List, r_space: CSLECTFRandomizationSpace, env_config: CSLEEnvConfig) \
            -> Tuple[NetworkConfig, CSLEEnvConfig]:
        """
        Randomizes a given MDP using a specified randomization space

        :param subnet_prefix: the subnet prefix
        :param network_ids: the list of network ids to consider for randomization
        :param r_space: the randomization space
        :param env_config: the environment config
        :return: a new randomized network configuration
        """
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
            ip_id = int(node.internal_ip.rsplit(".", 1)[-1])
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
                if node_users.internal_ip == node.internal_ip:
                    users = node_users
            flags = None
            for flags_users in flags_config.flags:
                if flags_users.ip == node.internal_ip:
                    flags = flags_users
            vulns = None
            for vulns_users in vulnerabilities.vulnerabilities:
                if vulns_users.ip == node.internal_ip:
                    vulns = vulns_users
            router = (node.internal_ip == router_ip)
            agent = (node.internal_ip == agent_ip)
            if agent:
                agent_reachable=reachable
            node_randomize_config = CSLECTFNodeRandomizerConfig(
                ip=node.internal_ip, id=id, reachable=reachable, router=router, agent=agent, r_space=r_space,
                users_config=users, flags_config=flags, vulns_config=vulns, gateway=gateway)
            n = CSLECTFNodeRandomizer.randomize(config=node_randomize_config)
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
        for a in env_config.attacker_action_conf.actions:
            if a.subnet:
                a.internal_ip = subnet_mask
        return randomized_network_conf, env_config

