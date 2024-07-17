from unittest.mock import patch, MagicMock
from csle_common.util.docker_util import DockerUtil
import csle_common.constants.constants as constants
import json


class TestDockerUtilSuite:
    """
    Test suite for docker util
    """

    @patch("docker.from_env")
    @patch("docker.APIClient")
    @patch("csle_common.util.docker_util.DockerUtil.parse_running_containers")
    @patch("csle_common.util.docker_util.DockerUtil.parse_running_emulation_envs")
    def test_parse_running_emulation_infos(
        self, mock_parse_running_emulation_envs, mock_parse_running_containers, mock_APIClient, mock_from_env
    ) -> None:
        """
        Test method that queries docker to get a list of all running emulation environments

        :param mock_parse_running_emulation_envs: mock_parse_running_emulation_envs
        :param mock_parse_running_containers: mock_parse_running_containers
        :param mock_APIClient: mock_APIClient
        :param mock_from_env: mock_from_env

        :return: None
        """
        mock_client_1 = MagicMock()
        mock_client_2 = MagicMock()
        mock_from_env.return_value = mock_client_1
        mock_APIClient.return_value = mock_client_2
        mock_parsed_containers = [MagicMock()]
        mock_parse_running_containers.return_value = mock_parsed_containers
        mock_parsed_envs = [MagicMock()]
        mock_parse_running_emulation_envs.return_value = mock_parsed_envs
        result = DockerUtil.parse_runnning_emulation_infos()
        mock_from_env.assert_called()
        mock_APIClient.assert_called()
        mock_parse_running_containers.assert_called()
        mock_parse_running_emulation_envs.assert_called()
        assert result == mock_parsed_envs

    @patch("docker.from_env")
    @patch("docker.APIClient")
    @patch("csle_common.util.docker_util.DockerUtil.parse_running_containers")
    def test_get_container_hex_id(self, mock_parse_running_containers, mock_APIClient, mock_from_env) -> None:
        """
        Test method that queries the docker engine for the id of a container with a given name

        :param mock_parse_running_containers: mock_parse_running_containers
        :param mock_APIClient: mock_APIClient
        :param mock_from_env: mock_from_env

        :return: None
        """
        mock_client_1 = MagicMock()
        mock_client_2 = MagicMock()
        mock_from_env.return_value = mock_client_1
        mock_APIClient.return_value = mock_client_2
        container_1 = MagicMock()
        container_1.name = "container_1"
        container_1.id = "1"
        container_2 = MagicMock()
        container_2.name = "container_2"
        container_2.id = "2"
        mock_parse_running_containers.return_value = [container_1, container_2]
        result = DockerUtil.get_container_hex_id("container_1")
        assert result == "1"

    @patch("csle_common.util.docker_util.DockerUtil.parse_containers")
    def test_parse_running_container(self, mock_parse_containers) -> None:
        """
        Test method that queries docker to get a list of all running containers

        :param mock_parse_containers: mock_parse_containers

        :return: None
        """
        mock_client_1 = MagicMock()
        mock_client_2 = MagicMock()
        container_1 = MagicMock()
        container_2 = MagicMock()
        mock_client_1.containers.list.return_value = [container_1, container_2]
        mock_parsed_container_1 = MagicMock()
        mock_parsed_container_2 = MagicMock()
        mock_parse_containers.return_value = [mock_parsed_container_1, mock_parsed_container_2]
        result = DockerUtil.parse_running_containers(client_1=mock_client_1, client_2=mock_client_2)
        mock_client_1.containers.list.assert_called()
        mock_parse_containers.assert_called()
        assert result == [mock_parsed_container_1, mock_parsed_container_2]

    @patch("csle_common.util.docker_util.DockerUtil.parse_containers")
    def test_parse_stopped_container(self, mock_parse_containers) -> None:
        """
        Test method that queries docker to get a list of all stopped csle containers

        :param mock_parse_containers: mock_parse_containers

        :return: None
        """
        mock_client_1 = MagicMock()
        mock_client_2 = MagicMock()
        container_1 = MagicMock()
        container_1.status = constants.DOCKER.CONTAINER_EXIT_STATUS
        container_2 = MagicMock()
        container_2.status = constants.DOCKER.CONTAINER_CREATED_STATUS
        mock_client_1.containers.list.return_value = [container_1, container_2]
        mock_parsed_container_1 = MagicMock()
        mock_parsed_container_2 = MagicMock()
        mock_parse_containers.return_value = [mock_parsed_container_1, mock_parsed_container_2]
        result = DockerUtil.parse_stopped_containers(client_1=mock_client_1, client2=mock_client_2)
        mock_client_1.containers.list.assert_called()
        mock_parse_containers.assert_called()
        assert result == [mock_parsed_container_1, mock_parsed_container_2]

    @patch("csle_common.metastore.metastore_facade.MetastoreFacade.get_emulation_by_name")
    def test_parse_running_emulation_envs(self, mock_get_emulation_by_name) -> None:
        """
        Test method that queries docker to get a list of all active emulation environments

        :param mock_get_emulation_by_name: mock_get_emulation_by_name

        :return: None
        """
        container_1 = MagicMock()
        container_1.emulation = "emulation1"
        container_1.ip = "192.168.1.2"
        container_1.ip_prefix_len = 24
        container_1.level = "level1"

        container_2 = MagicMock()
        container_2.emulation = "emulation1"
        container_2.ip = "192.168.1.3"
        container_2.ip_prefix_len = 24
        container_2.level = "level1"

        containers = [container_1, container_2]
        emulations = ["emulation1"]

        mock_em_record = MagicMock()
        mock_get_emulation_by_name.return_value = mock_em_record

        result = DockerUtil.parse_running_emulation_envs(emulations=emulations, containers=containers)
        mock_get_emulation_by_name.assert_called()
        assert result

    @patch("docker.APIClient.inspect_container")
    def test_parse_containers(self, mock_inspect_container) -> None:
        """
        Test method that queries docker to get a list of running or stopped csle containers

        :param mock_inspect_container: mock_inspect_container

        :return: None
        """
        mock_client2 = MagicMock()
        mock_inspect_info = {
            constants.DOCKER.NETWORK_SETTINGS: {
                constants.DOCKER.NETWORKS: {
                    "net": {
                        constants.DOCKER.IP_ADDRESS_INFO: "192.168.1.2",
                        constants.DOCKER.NETWORK_ID_INFO: "network_1",
                        constants.DOCKER.GATEWAY_INFO: "192.168.1.1",
                        constants.DOCKER.MAC_ADDRESS_INFO: "02:42:ac:11:00:02",
                        constants.DOCKER.IP_PREFIX_LEN_INFO: 24,
                    }
                }
            },
            constants.DOCKER.CREATED_INFO: "2021-01-01T00:00:00Z",
            constants.DOCKER.CONFIG: {constants.DOCKER.HOSTNAME_INFO: "container_1", constants.DOCKER.IMAGE: "image_1"},
        }
        mock_inspect_container.return_value = mock_inspect_info

        container_1 = MagicMock()
        container_1.name = "csle_container_1-level1-1"
        container_1.status = "running"
        container_1.short_id = "1"
        container_1.image.short_id = "image1"
        container_1.image.tags = ["latest"]
        container_1.id = "container_id_1"
        container_1.labels = {
            constants.DOCKER.CFG: "/path/to/config",
            constants.DOCKER.CONTAINER_CONFIG_DIR: "/path/to/dir",
            constants.DOCKER.EMULATION: "emulation_1",
            constants.DOCKER.KAFKA_CONFIG: "kafka_config_1",
        }
        containers = [container_1]
        result = DockerUtil.parse_containers(containers=containers, client2=mock_client2)
        # mock_inspect_container.assert_called_once_with("container_id_1")
        assert result

    @patch("os.popen")
    def test_get_docker_gw_bridge_ip(self, mock_popen) -> None:
        """
        Test method that gets the docker gw bridge ip of a container

        :param mock_popen: mock_popen

        :return: None
        """
        mock_json_output = json.dumps(
            [{constants.DOCKER.CONTAINERS_KEY: {"container_id_1": {constants.DOCKER.IPV4_KEY: "192.168.1.2/24"}}}]
        )
        mock_stream = MagicMock()
        mock_stream.read.return_value = mock_json_output
        mock_popen.return_value = mock_stream
        result = DockerUtil.get_docker_gw_bridge_ip("container_id_1")
        assert result == "192.168.1.2"
