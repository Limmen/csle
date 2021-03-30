from typing import List
import random
import numpy as np
from gym_pycr_ctf.dao.container_config.topology import Topology
from gym_pycr_ctf.dao.container_config.containers_config import ContainersConfig
from gym_pycr_ctf.dao.container_config.node_firewall_config import NodeFirewallConfig
from gym_pycr_ctf.dao.network.cluster_config import ClusterConfig
from gym_pycr_ctf.envs.logic.cluster.util.cluster_util import ClusterUtil
from gym_pycr_ctf.envs.config.generator.generator_util import GeneratorUtil
from gym_pycr_ctf.dao.container_config.traffic_config import TrafficConfig
from gym_pycr_ctf.dao.container_config.node_traffic_config import NodeTrafficConfig
from gym_pycr_ctf.util.experiments_util import util
import gym_pycr_ctf.constants.constants as constants

class TrafficGenerator:

    @staticmethod
    def generate(topology: Topology, containers_config: ContainersConfig) -> TrafficConfig:
        jumphosts_dict = {}
        targethosts_dict = {}
        containers_dict = {}

        for node in topology.node_configs:
            ip = node.ip
            jumphosts = TrafficGenerator._find_jumphosts(topology=topology, ip=ip)
            jumphosts_dict[ip] = jumphosts
            targethosts_dict[ip] = []

        for node in topology.node_configs:
            for k,v in jumphosts_dict.items():
                if node.ip in v:
                    targethosts_dict[node.ip].append(k)

        for container in containers_config.containers:
            containers_dict[container.ip] = container.name

        node_traffic_configs = []
        for node in topology.node_configs:
            commands = constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[containers_dict[node.ip]]
            node_traffic_config = NodeTrafficConfig(ip=node.ip, jumphosts=targethosts_dict[node.ip],
                                                    target_hosts=targethosts_dict[node.ip], commands=commands)
            node_traffic_configs.append(node_traffic_config)

        traffic_config = TrafficConfig(node_traffic_configs = node_traffic_configs)
        return traffic_config


    @staticmethod
    def create_traffic_scripts(traffic_config: TrafficConfig, cluster_config: ClusterConfig):
        #GeneratorUtil.connect_admin(cluster_config=cluster_config, ip=node.ip)
        GeneratorUtil.disconnect_admin(cluster_config=cluster_config)


    @staticmethod
    def write_traffic_config(traffic_config: TrafficConfig, path: str = None) -> None:
        """
        Writes the default configuration to a json file

        :param traffic_config: the traffic config to write
        :param path: the path to write the configuration to
        :return: None
        """
        path = util.default_traffic_path(out_dir=path)
        util.write_traffic_config_file(traffic_config, path)


    @staticmethod
    def _find_jumphosts(topology: Topology, ip: str) -> List[str]:
        """
        Utility method to find Ips in a topology that can reach a specific ip

        :param topology: the topology
        :param ip: the ip to test
        :return: a list of ips that can reach the target ip
        """
        jumphosts = []
        for node in topology.node_configs:
            if ip in node.output_accept and ip in node.input_accept:
                jumphosts.append(node.ip)
        return jumphosts