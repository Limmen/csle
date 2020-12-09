from typing import List, Tuple
import random
from gym_pycr_pwcrack.dao.container_config.vulnerabilities_config import VulnerabilitiesConfig
from gym_pycr_pwcrack.dao.container_config.topology import Topology
from gym_pycr_pwcrack.dao.container_config.node_container_config import NodeContainerConfig
from gym_pycr_pwcrack.dao.container_config.containers_config import ContainersConfig
from gym_pycr_pwcrack.util.experiments_util import util

class ContainerGenerator:

    @staticmethod
    def generate(topology: Topology, vuln_cfg : VulnerabilitiesConfig,
                 gateways : dict, container_pool: List[Tuple[str, str]],
                 gw_vuln_compatible_containers: List[Tuple[str, str]],
                 pw_vuln_compatible_containers: List[Tuple[str, str]], subnet_id: int, num_flags: int,
                 agent_ip: str, router_ip: str, agent_containers: List[Tuple[str, str]],
                 router_containers: List[Tuple[str, str]], subnet_prefix: str) -> ContainersConfig:

        network = "pycr_net_" + str(subnet_id)
        minigame = "pwcrack"
        level = "random_n" + str(len(topology.node_configs)) + "_f" + str(num_flags) \
                + "_rid_" + str(random.randint(0, 100000))
        container_configs = []
        vulnerabilities = vuln_cfg.vulnerabilities
        ids_enabled = True

        for node in topology.node_configs:
            ip = node.ip
            if ip == agent_ip:
                container = agent_containers[random.randint(0, len(agent_containers)-1)]
            elif ip == router_ip:
                container = router_containers[random.randint(0, len(agent_containers) - 1)]
                if container == "router1":
                    ids_enabled = False
            else:
                gw_node = False
                vuln_node = False
                ip_suffix = int(ip.rsplit(".", 1)[-1])
                if ip_suffix in gateways.values():
                    gw_node = True
                for v in vulnerabilities:
                    if v.node_ip == ip:
                        vuln_node = True

                if not gw_node and not vuln_node:
                    container = container_pool[random.randint(0, len(container_pool)-1)]
                elif not gw_node and vuln_node:
                    container = pw_vuln_compatible_containers[random.randint(0, len(pw_vuln_compatible_containers) - 1)]
                elif gw_node and vuln_node:
                    container = gw_vuln_compatible_containers[random.randint(0, len(gw_vuln_compatible_containers) - 1)]
                else:
                    raise AssertionError("Invalid container config")

            container_name, container_version = container
            container_cfg = NodeContainerConfig(name=container_name, network=network, version=container_version,
                                            level=level, ip=ip, minigame = minigame)
            container_configs.append(container_cfg)

        subnet_mask = subnet_prefix + "0/24"
        containers_cfg = ContainersConfig(containers=container_configs, network=network, agent_ip=agent_ip,
                                          router_ip=router_ip, subnet_mask=subnet_mask, subnet_prefix=subnet_prefix,
                                          ids_enabled=ids_enabled)
        return containers_cfg

    @staticmethod
    def write_containers_config(containers_cfg: VulnerabilitiesConfig, path: str = None) -> None:
        """
        Writes the default configuration to a json file

        :param containers_cfg: the config to write
        :param path: the path to write the configuration to
        :return: None
        """
        if path is None:
            path = util.default_containers_path()
        util.write_containers_config_file(containers_cfg, path)

