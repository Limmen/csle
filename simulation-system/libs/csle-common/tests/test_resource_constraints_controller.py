import subprocess
from unittest.mock import patch, MagicMock
from csle_common.controllers.resource_constraints_controller import ResourceConstraintsController


class TestResourceConstraintsControllerSuite:
    """
    Test suite for ResourceConstraintsController
    """

    @patch("csle_common.util.emulation_util.EmulationUtil.connect_admin")
    @patch("csle_common.util.emulation_util.EmulationUtil.disconnect_admin")
    @patch("csle_common.util.emulation_util.EmulationUtil.execute_ssh_cmd")
    @patch("subprocess.Popen")
    def test_apply_resource_constraints(
            self, mock_popen, mock_execute_ssh_cmd, mock_disconnect_admin, mock_connect_admin) -> None:
        """
        Test the method that creates users in an emulation environment according to a specified users-configuration


        :param mock_popen: mock_popen
        :param mock_execute_ssh_cmd: mock_execute_ssh_cmd
        :param mock_disconnect_admin: mock_disconnect_admin
        :param mock_connect_admin: mock_connect_admin
        :return: None
        """
        emulation_env_config = MagicMock()
        network_config = MagicMock()
        network_config.interface = "eth0"
        network_config.packet_delay_ms = 10
        network_config.packet_delay_jitter_ms = 5
        network_config.packet_delay_distribution = "normal"
        network_config.loss_gemodel_p = 0.1
        network_config.loss_gemodel_r = 0.1
        network_config.loss_gemodel_h = 0.9
        network_config.loss_gemodel_k = 0.9
        network_config.packet_duplicate_percentage = 0.1
        network_config.packet_duplicate_correlation_percentage = 0.1
        network_config.packet_corrupt_percentage = 0.1
        network_config.packet_reorder_percentage = 0.1
        network_config.packet_reorder_correlation_percentage = 0.1
        network_config.packet_reorder_gap = 5
        network_config.rate_limit_mbit = 10
        network_config.limit_packets_queue = 100

        node_resource_config = MagicMock()
        node_resource_config.physical_host_ip = "192.168.1.1"
        node_resource_config.docker_gw_bridge_ip = "192.168.1.2"
        node_resource_config.container_name = "container_1"
        node_resource_config.available_memory_gb = 2
        node_resource_config.num_cpus = 1
        node_resource_config.ips_and_network_configs = [("192.168.1.2", network_config)]

        emulation_env_config.resources_config.node_resources_configurations = [node_resource_config]
        emulation_env_config.kafka_config.resources = node_resource_config
        emulation_env_config.sdn_controller_config.resources = node_resource_config
        emulation_env_config.connections = {"192.168.1.2": MagicMock()}
        physical_server_ip = "192.168.1.1"
        mock_execute_ssh_cmd.return_value = ("output", "error", 0)
        logger = MagicMock()
        ResourceConstraintsController.apply_resource_constraints(
            emulation_env_config=emulation_env_config, physical_server_ip=physical_server_ip, logger=logger)
        mock_connect_admin.assert_any_call(emulation_env_config=emulation_env_config, ip="192.168.1.2")
        expected_docker_update_cmd = "docker update --memory=2G --cpus=1 container_1"
        mock_popen.assert_any_call(expected_docker_update_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                   shell=True)
        mock_execute_ssh_cmd.assert_called()
        mock_disconnect_admin.assert_any_call(emulation_env_config=emulation_env_config)
