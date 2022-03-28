import subprocess
import random
from csle_common.dao.network.running_emulation_env_config import RunningEmulationEnvConfig
from csle_common.envs_model.logic.emulation.util.common.emulation_util import EmulationUtil
from csle_common.dao.emulation_config.resources_config import ResourcesConfig
from csle_common.dao.emulation_config.containers_config import ContainersConfig
from csle_common.dao.emulation_config.node_network_config import NodeNetworkConfig
from csle_common.dao.emulation_config.node_resources_config import NodeResourcesConfig
from csle_common.dao.emulation_config.packet_delay_distribution_type import PacketDelayDistributionType
from csle_common.dao.emulation_config.packet_loss_type import PacketLossType
from csle_common.envs_model.config.generator.generator_util import GeneratorUtil
from csle_common.util.experiments_util import util


class ResourceConstraintsGenerator:
    """
    A Utility Class for generating resource-constraints configuration files
    """

    @staticmethod
    def generate(containers_config: ContainersConfig,
                 min_cpus: int, max_cpus: int, min_mem_G: int, max_mem_G: int) -> ResourcesConfig:
        """
        Generate a random resource configuration for a given container configuration

        :param containers_config: the container configurations
        :param min_cpus: the minimum number of CPUs per container
        :param max_cpus: the maximum number of CPUs per container
        :param min_mem_G: the minimum memory in GB per container
        :param max_mem_G: the maximum memory in GB per container
        :return: the generated resources configuration
        """
        node_resources_configs = []
        for c in containers_config.containers:
            num_cpus = random.randint(min_cpus, max_cpus)
            num_mem_G = random.randint(min_mem_G, max_mem_G)
            network_resources_configs = []
            for i, ip_net in enumerate(c.ips_and_networks):
                ip, net = ip_net
                if ip != None:
                    net_id = ip.split(".")[2]
                    interface = f"eth{i}"
                    if net_id != 1:
                        network_resources_configs.append((ip,
                             NodeNetworkConfig(
                                 interface=interface,
                                 limit_packets_queue=30000, packet_delay_ms=0.1,
                                 packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                 packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                 packet_loss_type=PacketLossType.GEMODEL,
                                 loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                 loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                 packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                 packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                 packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                 rate_limit_mbit=1000, packet_overhead_bytes=0,
                                 cell_overhead_bytes=0
                             )))
                    else:
                        network_resources_configs.append(
                            (ip, NodeNetworkConfig(
                                interface=interface,
                                limit_packets_queue=30000, packet_delay_ms=2,
                                packet_delay_jitter_ms=0.5, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.02, loss_gemodel_r=0.97,
                                loss_gemodel_k=0.98, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.02,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=2,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                rate_limit_mbit=100, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            )))
            node_resources_config = NodeResourcesConfig(container_name=c.name, num_cpus=num_cpus,
                                                        available_memory_gb=num_mem_G,
                                                        ips_and_network_configs=network_resources_configs)
            node_resources_configs.append(node_resources_config)

        resources_config = ResourcesConfig(node_resources_configurations=node_resources_configs)
        return resources_config

    @staticmethod
    def apply_resource_constraints(resources_config: ResourcesConfig, emulation_config: RunningEmulationEnvConfig):
        """
        Creates users in an emulation environment according to a specified users-configuration

        :param users_config: the users configuration
        :param emulation_config: the emulation configuration
        :return: None
        """
        if emulation_config.server_connection:
            emulation_config.connect_server()
        for node_resource_config in resources_config.node_resources_configurations:
            ips = node_resource_config.get_ips()
            ip = ips[0]
            print(f"applying resource constraints on node:{ip}")
            GeneratorUtil.connect_admin(emulation_env_config=emulation_config, ip=ip)

            for ip_and_net_config in node_resource_config.ips_and_network_configs:
                _, net_config = ip_and_net_config
                # update cpus and memory
                cmd = f"docker update --memory={node_resource_config.available_memory_gb}G " \
                      f"--cpus={node_resource_config.num_cpus} {node_resource_config.container_name}"
                if emulation_config.server_connection:
                    o,e,_ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.server_conn)
                else:
                    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

                # delete existing netem rules
                cmd = f"sudo tc qdisc del dev {net_config.interface} root netem"
                o,e,_ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

                # add new netem rule that implements the traffic shaping configuration
                cmd = f"sudo tc qdisc add dev {net_config.interface} root netem " \
                      f"delay {net_config.packet_delay_ms:.6f}ms " \
                      f"{net_config.packet_delay_jitter_ms:.6f}ms " \
                      f"distribution {str(net_config.packet_delay_distribution)} " \
                      f"loss gemodel {net_config.loss_gemodel_p:.6f} " \
                      f"{net_config.loss_gemodel_r:.6f} " \
                      f"{(1 - net_config.loss_gemodel_h):.6f} " \
                      f"{(1 - net_config.loss_gemodel_k):.6f} " \
                      f"duplicate {net_config.packet_duplicate_percentage:.6f}% " \
                      f"{net_config.packet_duplicate_correlation_percentage:.6f}% corrupt " \
                      f"{net_config.packet_corrupt_percentage:.6f}% " \
                      f"reorder {net_config.packet_reorder_percentage:.6f}% " \
                      f"{net_config.packet_reorder_correlation_percentage:.6f}% " \
                      f"gap {net_config.packet_reorder_gap} " \
                      f"rate {net_config.rate_limit_mbit:.6f}mbit " \
                      f"limit {net_config.limit_packets_queue:.6f}"
                o,e,_ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
            GeneratorUtil.disconnect_admin(emulation_env_config=emulation_config)


    @staticmethod
    def write_resources_config(resources_config: ResourcesConfig, path: str = None) -> None:
        """
        Writes the default configuration to a json file

        :param path: the path to write the configuration to
        :return: None
        """
        path = util.default_resources_path(out_dir=path)
        util.write_resources_config_file(resources_config, path)


