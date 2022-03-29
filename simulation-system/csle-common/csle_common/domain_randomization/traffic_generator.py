from typing import List
from csle_common.dao.emulation_config.topology import Topology
from csle_common.dao.emulation_config.containers_config import ContainersConfig
from csle_common.dao.emulation_config.traffic_config import TrafficConfig
from csle_common.dao.emulation_config.node_traffic_config import NodeTrafficConfig
from csle_common.util.experiment_util import ExperimentsUtil


class TrafficGenerator:
    """
    A Utility Class for generating traffic generation configuration files
    """

    @staticmethod
    def generate(topology: Topology, containers_config: ContainersConfig, agent_container_names : List[str],
                 router_container_names : List[str]) \
            -> TrafficConfig:
        """
        Generates a traffic configuration

        :param topology: topology of the environment
        :param containers_config: container configuration of the envirinment
        :param agent_container_names: list of agent container names
        :param router_container_names: list of router container names
        :return: the created traffic configuration
        """
        # jumphosts_dict = {}
        # targethosts_dict = {}
        # containers_dict = {}
        #
        # for node in topology.node_configs:
        #     ip = node.get_ips()[0]
        #     jumphosts = TrafficGenerator._find_jumphosts(topology=topology, ip=ip)
        #     jumphosts_dict[ip] = jumphosts
        #     targethosts_dict[ip] = []
        #
        # for node in topology.node_configs:
        #     for k,v in jumphosts_dict.items():
        #         if node.ip in v:
        #             targethosts_dict[node.ip].append(k)
        #
        # for container in containers_config.containers:
        #     containers_dict[container.internal_ip] = container.name

        node_traffic_configs = []
        for node in topology.node_configs:
            commands = []
            # for target in targethosts_dict[node.ip]:
            #     if containers_dict[target] not in agent_container_names \
            #             and containers_dict[target] not in router_container_names:
            #         template_commands = constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[containers_dict[target]]
            #         for tc in template_commands:
            #             commands.append(tc.format(target))

            node_traffic_config = NodeTrafficConfig(ip=node.get_ips()[0],
                                                    jumphosts=[], target_hosts=[], commands=commands)
            node_traffic_configs.append(node_traffic_config)

        traffic_config = TrafficConfig(node_traffic_configs = node_traffic_configs)
        return traffic_config

    @staticmethod
    def write_traffic_config(traffic_config: TrafficConfig, path: str = None) -> None:
        """
        Writes the default configuration to a json file

        :param traffic_config: the traffic config to write
        :param path: the path to write the configuration to
        :return: None
        """
        path = ExperimentsUtil.default_traffic_path(out_dir=path)
        ExperimentsUtil.write_traffic_config_file(traffic_config, path)


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

