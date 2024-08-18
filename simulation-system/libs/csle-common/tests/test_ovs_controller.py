import pytest
import logging
from unittest.mock import patch, MagicMock
import csle_common.constants.constants as constants
from csle_common.controllers.ovs_controller import OVSController
from csle_common.dao.emulation_config.containers_config import ContainersConfig


class TestOVSControllerSuite:
    """
    Test suite for OVS controller
    """

    @pytest.fixture
    def mock_containers_config(self) -> ContainersConfig:
        """
        Test method that sets up OVS switches on containers

        :return: None
        """
        container1 = MagicMock()
        container1.physical_host_ip = "192.168.1.1"
        container1.name = "ovs_container1"
        container1.get_full_name.return_value = "container1"
        container1.ips_and_networks = [("192.168.1.100", MagicMock(interface="eth0", bitmask="255.255.255.0"))]
        container2 = MagicMock()
        container2.physical_host_ip = "192.168.1.2"
        container2.name = "ovs_container2"
        container2.get_full_name.return_value = "container2"
        container2.ips_and_networks = [("192.168.1.101", MagicMock(interface="eth0", bitmask="255.255.255.0"))]
        containers_config = MagicMock(spec=ContainersConfig)
        containers_config.containers = [container1, container2]
        return containers_config

    @patch("subprocess.Popen")
    @patch("time.sleep")
    def test_create_virtual_switches_on_container(self, mock_sleep, mock_popen, mock_containers_config) -> None:
        """
        Test method that creates the OVS switches

        :param mock_sleep: mock_sleep
        :param mock_popen: mock_popen
        :param mock_containers_config: mock_containers_config
        :return: None
        """
        logger = MagicMock()
        physical_server_ip = "192.168.1.1"
        constants.CONTAINER_IMAGES.OVS_IMAGES = ["ovs_container1"]
        OVSController.create_virtual_switches_on_container(mock_containers_config, physical_server_ip, logger)
        mock_popen.assert_called()
        assert mock_sleep.call_count == 5

    @patch("csle_common.util.emulation_util.EmulationUtil.connect_admin")
    @patch("csle_common.util.emulation_util.EmulationUtil.execute_ssh_cmd")
    def test_apply_ovs_config(self, mock_execute_ssh_cmd, mock_connect_admin) -> None:
        """
        Test method that applies the OVS configuration

        :param mock_execute_ssh_cmd: mock_execute_ssh_cmd
        :param mock_connect_admin: mock_connect_admin
        :return: None
        """
        emulation_env_config = MagicMock()
        ovs_switch_config = MagicMock()
        ovs_switch_config.container_name = "ovs_container_1"
        ovs_switch_config.physical_host_ip = "192.168.1.1"
        ovs_switch_config.docker_gw_bridge_ip = "192.168.1.3"
        emulation_env_config.ovs_switch_config = ovs_switch_config
        emulation_env_config.ovs_switch_config.switch_configs = [ovs_switch_config]
        emulation_env_config.connections = {"192.168.1.3": MagicMock()}
        physical_server_ip = "192.168.1.2"
        logger = MagicMock(spec=logging.Logger)
        OVSController.apply_ovs_config(emulation_env_config=emulation_env_config, physical_server_ip=physical_server_ip,
                                       logger=logger)
        mock_connect_admin.assert_not_called()
        mock_execute_ssh_cmd.assert_not_called()
