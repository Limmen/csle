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


def default_resource_constraints(network_id: int = 9) -> ResourcesConfig:
    """
    :param network_id: the network id
    :return: generates the ResourcesConfig
    """
    node_resources_configurations = [
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.HACKER_KALI_1}_1-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
                            )),
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.254",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.CLIENT_1}_1-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
                            )),
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.253",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.CLIENT_1}_2-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
                            )),
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.252",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.CLIENT_1}_3-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
                            )),
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.ROUTER_2}_1-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.SSH_1}_1-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.SAMBA_2}_1-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_1-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.FTP_1}_1-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.SHELLSHOCK_1}_1-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.SQL_INJECTION_1}_1-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.CVE_2010_0426_1}_1-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.CVE_2015_1427_1}_1-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_1-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.SAMBA_1}_1-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.4",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_2-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.5",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_3-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.6",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_4-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.8",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_5-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.9",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.HONEYPOT_1}_6-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.178",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.CVE_2015_3306_1}_1-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_2-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.12",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_3-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.13",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_4-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.14",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_5-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.16",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_6-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.16",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_7-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.17",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_8-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.18",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_9-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_10-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.20",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_11-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.22",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_12-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.23",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_13-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.24",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.HONEYPOT_2}_14-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.25",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.CVE_2015_5602_1}_1-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.28",
                            container_name=f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-"
                                           f"{constants.CONTAINER_IMAGES.CVE_2016_10033_1}_1_1-{constants.CSLE.LEVEL}9",
                            num_cpus=1, available_memory_gb=4,
                            network_config=NodeNetworkConfig(
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
                            ))
    ]
    resources_config = ResourcesConfig(node_resources_configurations=node_resources_configurations)
    return resources_config


# Generates the resources.json configuration file
if __name__ == '__main__':
    network_id = 9
    if not os.path.exists(util.default_resources_path()):
        ResourceConstraintsGenerator.write_resources_config(
            resources_config=default_resource_constraints(network_id=network_id))
    resources_config = util.read_resources_config(util.default_resources_path())
    emulation_config = EmulationConfig(agent_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                                       agent_username=constants.CSLE_ADMIN.USER,
                                       agent_pw=constants.CSLE_ADMIN.PW, server_connection=False)
    ResourceConstraintsGenerator.apply_resource_constraints(resources_config=resources_config,
                                                            emulation_config=emulation_config)
