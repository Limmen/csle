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
        NodeResourcesConfig(ip="172.18.1.191", num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                limit_packets_queue=30000, transmission_delay_ms=0.1,
                                transmission_delay_jitter_ms=0.01, transmission_delay_correlation_percentage=25,
                                transmission_delay_distribution=PacketDelayDistributionType.NORMAL,
                                packet_loss_type=PacketLossType.GEMODEL, packet_loss_rate_random_percentage=3,
                                packet_loss_random_correlation_percentage=25,
                                loss_state_markov_chain_p13=0.1, loss_state_markov_chain_p31=0.1,
                                loss_state_markov_chain_p23=0.1, loss_state_markov_chain_p32=0.1,
                                loss_state_markov_chain_p14=0.1, loss_gemodel_p=0.1, loss_gemodel_r=0.1,
                                loss_gemodel_k=0.1, packet_corrupt_percentage=0.1,
                                packet_corrupt_correlation_percentage=0.0, packet_duplicate_percentage=0.0,
                                packet_duplicate_correlation_percentage=0.0, packet_reorder_percentage=0.0,
                                packet_reorder_correlation_percentage=0.0,
                                ingress_rate_limit_mbit=100, ingress_packet_overhead_bytes=0,
                                ingress_cell_overhead_bytes=0
                            )),
        NodeResourcesConfig(ip="172.18.1.21", users=[
            ("admin", "admin31151x", True),
            ("test", "qwerty", True),
            ("oracle", "abc123", False)
        ]),
        NodeResourcesConfig(ip="172.18.1.10", users=[
            ("admin", "admin1235912", True),
            ("jessica", "water", False)
        ]),
        NodeResourcesConfig(ip="172.18.1.2", users=[
            ("admin", "test32121", True),
            ("user1", "123123", True)
        ]),
        NodeResourcesConfig(ip="172.18.1.3", users=[
            ("john", "doe", True),
            ("vagrant", "test_pw1", False)
        ])
    ]
    users_conf = ResourcesConfig(node_resources_configurations=node_resources_configurations)
    return users_conf


# Generates the resources.json configuration file
if __name__ == '__main__':
    if not os.path.exists(util.default_resources_path()):
        ResourceConstraintsGenerator.write_resources_config_file(default_resource_constraints())
    resources_config = util.read_resources_config(util.default_resources_path())
    emulation_config = EmulationConfig(agent_ip="172.18.1.191", agent_username=constants.csle_ADMIN.USER,
                                     agent_pw=constants.csle_ADMIN.PW, server_connection=False)
    ResourceConstraintsGenerator.apply_resource_constraints(resources_config=resources_config,
                                                            emulation_config=emulation_config)