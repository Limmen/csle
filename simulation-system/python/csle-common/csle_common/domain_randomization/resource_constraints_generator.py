import random
from csle_common.dao.emulation_config.resources_config import ResourcesConfig
from csle_common.dao.emulation_config.containers_config import ContainersConfig
from csle_common.dao.emulation_config.node_network_config import NodeNetworkConfig
from csle_common.dao.emulation_config.node_resources_config import NodeResourcesConfig
from csle_common.dao.emulation_config.packet_delay_distribution_type import PacketDelayDistributionType
from csle_common.dao.emulation_config.packet_loss_type import PacketLossType
from csle_common.util.experiment_util import ExperimentUtil


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
    def write_resources_config(resources_config: ResourcesConfig, path: str = None) -> None:
        """
        Writes the default configuration to a json file

        :param path: the path to write the configuration to
        :return: None
        """
        path = ExperimentUtil.default_resources_path(out_dir=path)
        ExperimentUtil.write_resources_config_file(resources_config, path)


