import os
from csle_common.dao.container_config.resources_config import ResourcesConfig
from csle_common.dao.container_config.node_resources_config import NodeResourcesConfig
from csle_common.dao.container_config.node_network_config import NodeNetworkConfig
from csle_common.dao.container_config.packet_loss_type import PacketLossType
from csle_common.dao.container_config.packet_delay_distribution_type import PacketDelayDistributionType
from csle_common.util.experiments_util import util
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.config.generator.resource_constraints_generator import ResourceConstraintsGenerator
import csle_common.constants.constants as constants


def default_resource_constraints(network_id: int = 3, level: int = 3) -> ResourcesConfig:
    """
    :param level: the level parameter of the emulation
    :param network_id: the network id
    :return: generates the ResourcesConfig
    """
    node_resources_configurations = [
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.ROUTER_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.10",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
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
                 )),
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.10", NodeNetworkConfig(
                    interface=constants.NETWORKING.ETH1,
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
                ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.SSH_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
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
                 )),
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.2",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH1,
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
                 ))
            ]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.TELNET_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
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
                 )),
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.3",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH1,
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
                 ))
            ]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.21",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
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
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.FTP_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
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
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HACKER_KALI_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.191",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
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
                 ))]),
        NodeResourcesConfig(container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.SSH_2}_1-{constants.CSLE.LEVEL}{level}",
                            num_cpus=1, available_memory_gb=4,
                            ips_and_network_configs=[
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.54",
                                 NodeNetworkConfig(
                                     interface=constants.NETWORKING.ETH0,
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
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.54",
                                 NodeNetworkConfig(
                                     interface=constants.NETWORKING.ETH1,
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
                                 ))
                            ]),
        NodeResourcesConfig(container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.SSH_3}_1-{constants.CSLE.LEVEL}{level}",
                            num_cpus=1, available_memory_gb=4,
                            ips_and_network_configs=[
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.74",
                                 NodeNetworkConfig(
                                     interface=constants.NETWORKING.ETH0,
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
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.74",
                                 NodeNetworkConfig(
                                     interface=constants.NETWORKING.ETH1,
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
                                 ))]),
        NodeResourcesConfig(container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.TELNET_2}_1-{constants.CSLE.LEVEL}{level}",
                            num_cpus=1, available_memory_gb=4,
                            ips_and_network_configs=[
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.61",
                                 NodeNetworkConfig(
                                     interface=constants.NETWORKING.ETH0,
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
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.61",
                                 NodeNetworkConfig(
                                     interface=constants.NETWORKING.ETH1,
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
                                 ))
                            ]),
        NodeResourcesConfig(container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.TELNET_3}_1-{constants.CSLE.LEVEL}{level}",
                            num_cpus=1, available_memory_gb=4,
                            ips_and_network_configs=[
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.62",
                                 NodeNetworkConfig(
                                     interface=constants.NETWORKING.ETH0,
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
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.62",
                                 NodeNetworkConfig(
                                     interface=constants.NETWORKING.ETH1,
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
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.62",
                                 NodeNetworkConfig(
                                     interface=constants.NETWORKING.ETH2,
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
                                 ))
                            ]),
        NodeResourcesConfig(container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_1-{constants.CSLE.LEVEL}{level}",
                            num_cpus=1, available_memory_gb=4,
                            ips_and_network_configs=[
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.101",
                                 NodeNetworkConfig(
                                     interface=constants.NETWORKING.ETH0,
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
                                 )),
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.101",
                                 NodeNetworkConfig(
                                     interface=constants.NETWORKING.ETH1,
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
                                 )),
                            ]),
        NodeResourcesConfig(container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.FTP_2}_1-{constants.CSLE.LEVEL}{level}",
                            num_cpus=1, available_memory_gb=4,
                            ips_and_network_configs=[
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.7",
                                 NodeNetworkConfig(
                                     interface=constants.NETWORKING.ETH0,
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
                                 ))]),
        NodeResourcesConfig(container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_2-{constants.CSLE.LEVEL}{level}",
                            num_cpus=1, available_memory_gb=4,
                            ips_and_network_configs=[
                                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.4",
                                 NodeNetworkConfig(
                                     interface=constants.NETWORKING.ETH0,
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
                                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_3-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.5",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
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
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_4-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.6",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
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
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_5-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.8",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
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
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_6-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.9",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
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
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_7-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.178",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
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
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_2-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.11",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
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
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_3-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.2",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
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
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_4-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.13",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
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
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_5-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.14",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
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
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_6-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.15",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
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
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_7-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.16",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
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
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_8-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.17",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
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
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_9-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.18",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
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
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_10-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.19",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
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
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_11-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.20",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
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
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_12-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.22",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
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
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_13-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.23",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
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
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_14-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.24",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
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
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_15-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.25",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
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
                 ))]),
        NodeResourcesConfig(
            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                           f"{constants.CONTAINER_IMAGES.CLIENT_1}_1-{constants.CSLE.LEVEL}{level}",
            num_cpus=1, available_memory_gb=4,
            ips_and_network_configs=[
                (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.254",
                 NodeNetworkConfig(
                     interface=constants.NETWORKING.ETH0,
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
                 ))])
    ]
    resources_config = ResourcesConfig(node_resources_configurations=node_resources_configurations)
    return resources_config


# Generates the resources.json configuration file
if __name__ == '__main__':
    network_id = 3
    level = 3
    if not os.path.exists(util.default_resources_path()):
        ResourceConstraintsGenerator.write_resources_config(
            resources_config=default_resource_constraints(network_id=network_id, level=level))
    resources_config = util.read_resources_config(util.default_resources_path())
    emulation_config = EmulationConfig(agent_ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.191",
                                       agent_username=constants.CSLE_ADMIN.USER,
                                       agent_pw=constants.CSLE_ADMIN.PW, server_connection=False)
    ResourceConstraintsGenerator.apply_resource_constraints(resources_config=resources_config,
                                                            emulation_config=emulation_config)
