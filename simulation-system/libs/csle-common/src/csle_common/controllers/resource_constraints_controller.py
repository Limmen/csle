import logging
import subprocess
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.util.emulation_util import EmulationUtil


class ResourceConstraintsController:
    """
    Class managing resource constraints in the emulation environments
    """

    @staticmethod
    def apply_resource_constraints(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                                   logger: logging.Logger) -> None:
        """
        Creates users in an emulation environment according to a specified users-configuration

        :param emulation_env_config: the emulation env configuration
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        resource_constraints = emulation_env_config.resources_config.node_resources_configurations
        resource_constraints = resource_constraints + [emulation_env_config.kafka_config.resources]
        if emulation_env_config.sdn_controller_config is not None:
            resource_constraints = resource_constraints + [emulation_env_config.sdn_controller_config.resources]
        for node_resource_config in resource_constraints:
            if node_resource_config.physical_host_ip != physical_server_ip:
                continue
            ip = node_resource_config.docker_gw_bridge_ip
            logger.info(f"applying resource constraints on node: {ip}, "
                        f"{node_resource_config.container_name}")
            EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=ip)

            for ip_and_net_config in node_resource_config.ips_and_network_configs:
                _, net_config = ip_and_net_config
                if net_config is not None:
                    # update cpus and memory
                    cmd = f"docker update --memory={node_resource_config.available_memory_gb}G " \
                          f"--cpus={node_resource_config.num_cpus} {node_resource_config.container_name}"
                    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

                    # delete existing netem rules
                    cmd = f"sudo tc qdisc del dev {net_config.interface} root netem"
                    o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))

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
                    o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))
            EmulationUtil.disconnect_admin(emulation_env_config=emulation_env_config)
