from typing import List, Tuple
import random
from csle_common.dao.container_config.vulnerabilities_config import VulnerabilitiesConfig
from csle_common.dao.container_config.topology import Topology
from csle_common.dao.container_config.node_container_config import NodeContainerConfig
from csle_common.dao.container_config.containers_config import ContainersConfig
from csle_common.dao.container_config.node_firewall_config import NodeFirewallConfig
from csle_common.util.experiments_util import util
import csle_common.constants.constants as constants


class ContainerGenerator:
    """
    Class implementing functionality for generating container configuraitons
    """

    @staticmethod
    def generate(topology: Topology, vuln_cfg : VulnerabilitiesConfig,
                 vulnerable_nodes : List[NodeFirewallConfig], container_pool: List[Tuple[str, str]],
                 gw_vuln_compatible_containers: List[Tuple[str, str]],
                 pw_vuln_compatible_containers: List[Tuple[str, str]], subnet_id: int, num_flags: int,
                 agent_ip: str, router_ip: str, agent_containers: List[Tuple[str, str]],
                 router_containers: List[Tuple[str, str]], subnet_prefix: str) -> ContainersConfig:
        """
        Generates a containers configuration

        :param topology: the topology
        :param vuln_cfg: the vulnerabiltiy configurations
        :param vulnerable_nodes: the gateways in the emulation
        :param container_pool: the pool of containers
        :param gw_vuln_compatible_containers: the list of containers that can be used as gateways
        :param pw_vuln_compatible_containers: the list of containers that has pw vulnerabilities
        :param subnet_id: the subnet id
        :param num_flags: the number of flags
        :param agent_ip: the ip of the agent
        :param router_ip: the ip of the router
        :param agent_containers: the containers that can be used to implement the agent
        :param router_containers: the containers that can be used to implement the routers
        :param subnet_prefix: the prefix of the subnetwork
        :return: a containers configuration
        """

        network = constants.CSLE.CSLE_NETWORK_PREFIX + str(subnet_id)
        minigame = constants.CSLE.CTF_MINIGAME
        level = "random_n" + str(len(topology.node_configs)) + "_f" + str(num_flags) \
                + "_rid_" + str(random.randint(0, 100000))
        container_configs = []
        vulnerabilities = vuln_cfg.vulnerabilities
        ids_enabled = True

        for node in topology.node_configs:

            if agent_ip in node.get_ips():
                container = agent_containers[random.randint(0, len(agent_containers)-1)]
            elif router_ip in node.get_ips():
                container = router_containers[random.randint(0, len(router_containers) - 1)]
                if container[0] == constants.CSLE.NON_IDS_ROUTER:
                    ids_enabled = False
            else:
                vuln_node = False
                for v in vulnerabilities:
                    if v.ip in node.get_ips():
                        vuln_node = True

                if not vuln_node:
                    container = container_pool[random.randint(0, len(container_pool)-1)]
                else:
                    container = gw_vuln_compatible_containers[random.randint(0, len(gw_vuln_compatible_containers) - 1)]

            container_name, container_version = container
            suffix = 1
            for c in container_configs:
                if c.name == container_name:
                    suffix += 1
            ips_and_networks = []
            for net_fw_config in node.ips_gw_default_policy_networks:
                ips_and_networks.append((net_fw_config.ip, net_fw_config.network))
            node.hostname = f"{container_name}_{suffix}"
            container_cfg = NodeContainerConfig(name=container_name, ips_and_networks=ips_and_networks,
                                                version=container_version,
                                                level=level, minigame = minigame, suffix=f"_{suffix}",
                                                restart_policy=constants.DOCKER.ON_FAILURE_3)
            container_configs.append(container_cfg)

        containers_cfg = ContainersConfig(containers=container_configs, agent_ip=agent_ip,
                                          router_ip=router_ip, ids_enabled=ids_enabled,
                                          vulnerable_nodes=vulnerable_nodes, networks = [])
        return containers_cfg

    @staticmethod
    def write_containers_config(containers_cfg: ContainersConfig, path: str = None) -> None:
        """
        Writes the default configuration to a json file

        :param containers_cfg: the config to write
        :param path: the path to write the configuration to
        :return: None
        """
        path = util.default_containers_path(out_dir=path)
        util.write_containers_config_file(containers_cfg, path)

