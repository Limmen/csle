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


def default_resource_constraints() -> ResourcesConfig:
    """
    :return: generates the ResourcesConfig
    """
    node_resources_configurations = [
        NodeResourcesConfig(ip="172.18.7.191", container_name="csle-ctf-hacker_kali_1_1-level7",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface="eth0",
                                limit_packets_queue=30000, packet_delay_ms=2,
                                packet_delay_jitter_ms=0.5, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.02, loss_gemodel_r=0.97,
                                loss_gemodel_k=0.98, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.02,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=2,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5, packet_reorder_gap=5,
                                rate_limit_mbit=100, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            )),
        NodeResourcesConfig(ip="172.18.7.254", container_name="csle-ctf-client_1_1-level7",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface="eth0",
                                limit_packets_queue=30000, packet_delay_ms=2,
                                packet_delay_jitter_ms=0.5, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.02, loss_gemodel_r=0.97,
                                loss_gemodel_k=0.98, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.02,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=2,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5, packet_reorder_gap=5,
                                rate_limit_mbit=100, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            )),
        NodeResourcesConfig(ip="172.18.7.21", container_name="csle-ctf-honeypot_1_1-level7",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface="eth0",
                                limit_packets_queue=30000, packet_delay_ms=0.1,
                                packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5, packet_reorder_gap=5,
                                rate_limit_mbit=1000, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            )),
        NodeResourcesConfig(ip="172.18.7.10", container_name="csle-ctf-router_2_1-level7",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface="eth0",
                                limit_packets_queue=30000, packet_delay_ms=0.1,
                                packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5, packet_reorder_gap=5,
                                rate_limit_mbit=1000, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            )),
        NodeResourcesConfig(ip="172.18.7.2", container_name="csle-ctf-ssh_1_1-level7",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface="eth0",
                                limit_packets_queue=30000, packet_delay_ms=0.1,
                                packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5, packet_reorder_gap=5,
                                rate_limit_mbit=1000, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            )),
        NodeResourcesConfig(ip="172.18.7.3", container_name="csle-ctf-telnet_1_1-level7",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface="eth0",
                                limit_packets_queue=30000, packet_delay_ms=0.1,
                                packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5, packet_reorder_gap=5,
                                rate_limit_mbit=1000, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            )),
        NodeResourcesConfig(ip="172.18.7.79", container_name="csle-ctf-ftp_1_1-level7",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface="eth0",
                                limit_packets_queue=30000, packet_delay_ms=0.1,
                                packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5, packet_reorder_gap=5,
                                rate_limit_mbit=1000, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            )),
        NodeResourcesConfig(ip="172.18.7.19", container_name="csle-ctf-samba_1_1-level7",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface="eth0",
                                limit_packets_queue=30000, packet_delay_ms=0.1,
                                packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5, packet_reorder_gap=5,
                                rate_limit_mbit=1000, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            )),
        NodeResourcesConfig(ip="172.18.7.31", container_name="csle-ctf-shellshock_1_1-level7",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface="eth0",
                                limit_packets_queue=30000, packet_delay_ms=0.1,
                                packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5, packet_reorder_gap=5,
                                rate_limit_mbit=1000, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            )),
        NodeResourcesConfig(ip="172.18.7.42", container_name="csle-ctf-sql_injection_1_1-level7",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface="eth0",
                                limit_packets_queue=30000, packet_delay_ms=0.1,
                                packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5, packet_reorder_gap=5,
                                rate_limit_mbit=1000, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            )),
        NodeResourcesConfig(ip="172.18.7.37", container_name="csle-ctf-cve_2015_3306_1_1-level7",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface="eth0",
                                limit_packets_queue=30000, packet_delay_ms=0.1,
                                packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5, packet_reorder_gap=5,
                                rate_limit_mbit=1000, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            )),
        NodeResourcesConfig(ip="172.18.7.82", container_name="csle-ctf-cve_2015_1427_1_1-level7",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface="eth0",
                                limit_packets_queue=30000, packet_delay_ms=0.1,
                                packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5, packet_reorder_gap=5,
                                rate_limit_mbit=1000, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            )),
        NodeResourcesConfig(ip="172.18.7.75", container_name="csle-ctf-cve_2016_10033_1_1-level7",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface="eth0",
                                limit_packets_queue=30000, packet_delay_ms=0.1,
                                packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5, packet_reorder_gap=5,
                                rate_limit_mbit=1000, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            )),
        NodeResourcesConfig(ip="172.18.7.71", container_name="csle-ctf-cve_2010_0426_1_1-level7",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface="eth0",
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
        NodeResourcesConfig(ip="172.18.7.11", container_name="csle-ctf-cve_2015_5602_1_1-level7",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface="eth0",
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
    if not os.path.exists(util.default_resources_path()):
        ResourceConstraintsGenerator.write_resources_config(resources_config=default_resource_constraints())
    resources_config = util.read_resources_config(util.default_resources_path())
    emulation_config = EmulationConfig(agent_ip="172.18.7.191", agent_username=constants.csle_ADMIN.USER,
                                     agent_pw=constants.csle_ADMIN.PW, server_connection=False)
    ResourceConstraintsGenerator.apply_resource_constraints(resources_config=resources_config,
                                                            emulation_config=emulation_config)