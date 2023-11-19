from typing import Tuple, Any, Dict
import io
import docker
import logging
import pytest
import pytest_mock
from csle_common.controllers.container_controller import ContainerController
import csle_common.constants.constants as constants
from csle_collector.docker_stats_manager.docker_stats_manager_pb2 import DockerStatsMonitorDTO
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.emulation_execution import EmulationExecution
from csle_common.dao.emulation_config.containers_config import ContainersConfig
from csle_common.dao.emulation_config.docker_stats_manager_config import DockerStatsManagerConfig
from csle_common.dao.emulation_config.docker_stats_managers_info import DockerStatsManagersInfo
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.dao.emulation_config.config import Config
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.dao.docker.docker_env_metadata import DockerEnvMetadata


class TestContainerControllerSuite:
    """
    Test suite for the container controller
    """

    @pytest.fixture
    def client_1(self, mocker: pytest_mock.MockFixture) -> docker.from_env:
        """
        Pytest fixture for mocking the docker.from_env() method
        
        :param mocker: the Pytest mocker object
        :return: the mocked function
        """

        class from_env:
            def __init__(self) -> None:
                pass

            class containers:

                @staticmethod
                def list(all=False):
                    class image:
                        def __init__(self) -> None:
                            self.short_id = '1'
                            self.tags = ['tags']

                    class element:

                        def __init__(self) -> None:
                            self.name = constants.CONTAINER_IMAGES.CSLE_PREFIX + 'null' + '-' + 'level'
                            self.name = self.name + constants.CSLE.NAME + '--1'
                            self.status = constants.DOCKER.CONTAINER_EXIT_STATUS
                            self.labels = {constants.DOCKER.CFG: 'config_path',
                                           constants.DOCKER.CONTAINER_CONFIG_DIR: 'dir_path',
                                           constants.DOCKER.EMULATION: "JDoeEmulation"}
                            self.id = '1'
                            self.short_id = '1'
                            self.image = image()

                        def stop(self):
                            return None

                        def remove(self):
                            return None

                        def start(self):
                            return None

                    return [element()]

            class networks:

                @staticmethod
                def list():
                    class element:
                        def __init__(self) -> None:
                            self.name = constants.CONTAINER_IMAGES.CSLE_PREFIX + 'null' + '-' + 'level'
                            self.name = self.name + constants.CSLE.NAME + '--1'

                        def remove(self, ):
                            return None

                    return [element()]

                @staticmethod
                def create(name: str, driver: str, ipam: docker.types.IPAMConfig, attachable: bool):
                    return None

            class images:

                @staticmethod
                def list():
                    class element:
                        def __init__(self) -> None:
                            self.attrs = {constants.DOCKER.REPO_TAGS: [constants.CSLE.NAME,
                                                                       constants.DOCKER.BASE_CONTAINER_TYPE,
                                                                       constants.OS.UBUNTU, constants.OS.KALI],
                                          constants.DOCKER.IMAGE_CREATED: "yes",
                                          constants.DOCKER.IMAGE_OS: "os",
                                          constants.DOCKER.IMAGE_ARCHITECTURE: "csle-architecture",
                                          constants.DOCKER.IMAGE_SIZE: 100}
                            self.short_id = '1'
                            self.tags = ['tags']
                            self.name = constants.CSLE.NAME

                    return [element()]

                @staticmethod
                def remove(image, force):
                    return None

        from_env_mocker = mocker.MagicMock(side_effect=from_env)
        return from_env_mocker

    @pytest.fixture
    def ipam_pool(self, mocker: pytest_mock.MockFixture) -> docker.types.IPAMPool:
        """
        Pytest fixture for mocking the docker.types.IPAMPool class
        
        :param mocker: the pytest mocker object
        :return: the mocked object
        """

        class IPAMPool():
            def __init__(self, subnet) -> None:
                pass

        ipampool_mocker = mocker.MagicMock(side_effect=IPAMPool)
        return ipampool_mocker

    @pytest.fixture
    def ipam_config(self, mocker: pytest_mock.MockFixture) -> docker.types.IPAMConfig:
        """
        Pytest fixture for mocking the docker.types.ImpamConfig class

        :param mocker: the pytest mocker object
        :return: the mocked object
        """

        class IPAMConfig():
            def __init__(self, pool_configs) -> None:
                pass

        ipamconfig_mocker = mocker.MagicMock(side_effect=IPAMConfig)
        return ipamconfig_mocker

    @pytest.fixture
    def client_2(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the docker.APIClient
        
        :param mocker: the pytest mocker object
        :return: the mocked object
        """

        class APIClient():
            def __init__(self, base_url) -> None:
                self.base_url = base_url

            def inspect_container(self, param: int) -> Dict[str, Any]:
                dict = {
                    constants.DOCKER.NETWORK_SETTINGS: {
                        constants.DOCKER.NETWORKS: {
                            'net_key': {
                                constants.DOCKER.IP_ADDRESS_INFO: "123.456.78.99", constants.DOCKER.NETWORK_ID_INFO: 1,
                                constants.DOCKER.GATEWAY_INFO: "null", constants.DOCKER.MAC_ADDRESS_INFO: "null",
                                constants.DOCKER.IP_PREFIX_LEN_INFO: 1}
                        }
                    },
                    constants.DOCKER.CREATED_INFO: "created_info",
                    constants.DOCKER.CONFIG: {
                        constants.DOCKER.HOSTNAME_INFO: "JDoeHost",
                        constants.DOCKER.IMAGE: "JDoeImage"}
                }
                return dict

        api_mocker = mocker.MagicMock(side_effect=APIClient)
        return api_mocker

    @pytest.fixture
    def file_opener(self, mocker: pytest_mock.MockFixture) -> Any:
        """
        Pytest fixture for mocking the os.popen method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def popen(cmd: str):
            file = io.StringIO()
            file.write(f" test {constants.CSLE.CSLE_NETWORK_PREFIX}1 \n")
            file.write(f" test {constants.CSLE.CSLE_NETWORK_PREFIX}2\n")
            file.seek(0)
            return file

        popen_mocker = mocker.MagicMock(side_effect=popen)
        return popen_mocker

    @pytest.fixture
    def sub_popen(self, mocker: pytest_mock.MockFixture) -> Any:
        """
        Pytest fixture for mocking the suboprocess.Popen class

        :param mocker: the pytest mocker object
        :return: the mocked version
        """

        class Popen():
            def __init__(self, cmd: str, stdout, shell: bool) -> None:
                pass

            def __iter__(self, ):
                pass

            def communicate(self) -> Tuple[str, None]:
                return (constants.COMMANDS.SEARCH_DOCKER_STATS_MANAGER + '37752', None)

        sub_popen_mocker = mocker.MagicMock(side_effect=Popen)
        return sub_popen_mocker

    @pytest.fixture
    def true_running_stats_manager(self, mocker: pytest_mock.MockFixture) -> Any:
        """
        Pytest fixture for mocking the is_statsmanager_running method

        :param mocker: the pytest mocker object
        :return: True from the mocked function
        """

        def is_statsmanager_running() -> bool:
            return True

        is_statsmanager_running_mock = mocker.MagicMock(side_effect=is_statsmanager_running)
        return is_statsmanager_running_mock

    @pytest.fixture
    def false_running_stats_manager(self, mocker: pytest_mock.MockFixture) -> Any:
        """
        Pytest fixture for mocking the is_statsmanager_running method

        :param mocker: the pytest mocker object
        :return: False from the mocked function
        """

        def is_statsmanager_running() -> bool:
            return False

        is_statsmanager_running_mock = mocker.MagicMock(side_effect=is_statsmanager_running)
        return is_statsmanager_running_mock

    @pytest.fixture
    def pid_file(self, mocker: pytest_mock.MockFixture) -> Any:
        """
        Pytest fixture for mocking the read_pid_file in the ManagementSystemController

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def read_pid_file(path: str) -> int:
            return 100

        pid_file_mocker = mocker.MagicMock(side_effect=read_pid_file)
        return pid_file_mocker

    @pytest.fixture
    def start_fixture(self, mocker: pytest_mock.MockFixture) -> Any:
        """
        Pytest fixture for mocking the start_docker_stats_monitor in the csle_collector environment
        :param mocker: the pytest mocker object
        :return: None
        """

        def start_docker_stats_monitor(stub: str, emulation: EmulationEnvConfig,
                                       kafka_ip: str, stats_queue_maxsize: int,
                                       time_step_len_seconds: int,
                                       kafka_port: str, containers: NodeContainerConfig,
                                       execution_first_ip_octet: str) -> None:
            return None

        start_mocker = mocker.MagicMock(side_effect=start_docker_stats_monitor)
        return start_mocker

    @pytest.fixture
    def host_ip(self, mocker: pytest_mock.MockFixture) -> Any:
        """
        Pytest fixture for mocking the get_host_ip method
        
        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_host_ip() -> str:
            return "123.456.78.99"

        host_ip_mocker = mocker.MagicMock(side_effect=get_host_ip)
        return host_ip_mocker

    @pytest.fixture
    def stop_fixture(self, mocker: pytest_mock.MockFixture) -> Any:
        """
        Pytest fixture for mocking the stop_docker_stats_monitor in the csle_collector environment

        :param mocker: the pytest mocker object
        :return: None
        """

        def stop_docker_stats_monitor(stub: str, emulation: str, execution_first_ip_octet: str) -> None:
            return None

        stop_mocker = mocker.MagicMock(side_effect=stop_docker_stats_monitor)
        return stop_mocker

    @pytest.fixture
    def true_stop_fixture(self, mocker: pytest_mock.MockFixture) -> Any:
        """
        Pytest fixture for mocking the stop_docker_statsmanager method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_docker_statsmanager(logger: logging.Logger) -> bool:
            return True

        stop_fixture = mocker.MagicMock(side_effect=stop_docker_statsmanager)
        return stop_fixture

    @pytest.fixture
    def false_stop_fixture(self, mocker: pytest_mock.MockFixture) -> Any:
        """
        Pytest fixture for mocking the stop_docker_statsmanager method

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def stop_docker_statsmanager(logger: logging.Logger) -> bool:
            return False

        stop_fixture = mocker.MagicMock(side_effect=stop_docker_statsmanager)
        return stop_fixture

    @pytest.fixture
    def dsm_status(self, mocker: pytest_mock.MockFixture) -> Any:
        """
        Pytest fixture for mocking the get_docker_stats_manager_status method in the csle_collector environment

        :param mocker: the pytest mocker object
        :return: the mocked function
        """

        def get_docker_stats_manager_status(stub) -> DockerStatsMonitorDTO:
            return DockerStatsMonitorDTO(num_monitors=10, emulations=['JDoeEmulation'], emulation_executions=[10])

        dsm_status_mocker = mocker.MagicMock(side_effect=get_docker_stats_manager_status)
        return dsm_status_mocker

    @pytest.fixture
    def stub(self, mocker: pytest_mock.MockFixture) -> Any:
        """
        Pytest fixture for mocking the parameter stub fetched from csle_collector

        :param mocker: the pytest mocker object
        :return: the mocked object
        """

        class DockerStatsManagerStub():
            def __init__(self, channel) -> None:
                pass

        stub_mocker = mocker.MagicMock(side_effect=DockerStatsManagerStub)
        return stub_mocker

    @pytest.fixture
    def socket_fix(self, mocker: pytest_mock.MockFixture) -> Any:
        """
        Pytest fixture for mocking the imoprted socket module

        :param mocker: the pytest mocker object
        :return: the mocked object
        """

        class socket():
            def __init__(self, family: int = -1, type: int = -1, proto: int = -1, fileno: Any = None) -> None:
                self.family = family
                self.type = type
                self.proto = proto
                self.fileno = fileno

            def connect(self, a) -> None:
                return None

            def getsockname(self):
                return ["123.456.78.99"]

        socket_mocker = mocker.MagicMock(side_effect=socket)
        return socket_mocker

    def test_stop_all_running_containers(self, mocker: pytest_mock.MockFixture, client_1) -> None:
        """
        Tests the stop_all_running_containers method of the ContainerController

        :param mocker: the Pytest mock object
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)

        assert ContainerController.stop_all_running_containers() is None

    def test_stop_container(self, mocker: pytest_mock.MockFixture, client_1: pytest_mock.MockFixture) -> None:
        """
        Tests the stop_container method od the ContainerController

        :param mocker: the Pytest mock object
        :param client_1: fixture for mocking the docker.from_env class
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        assert ContainerController.stop_container(constants.CONTAINER_IMAGES.CSLE_PREFIX +
                                                  'null' + '-' + 'level' + constants.CSLE.NAME + '--1') is True
        assert ContainerController.stop_container("John Doe") is False

    def test_rm_all_stopped_containers(self, mocker: pytest_mock.MockFixture, client_1: pytest_mock.MockFixture):
        """
        Tests the rm_all_stopped_containers in the ContainerController

        :param mocker: the Pytest mocker object
        :param client_1: fixture for mocking the docker.from_env class
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        assert ContainerController.rm_all_stopped_containers() is None

    def test_rm_container(self, mocker: pytest_mock.MockFixture, client_1: pytest_mock.MockFixture) -> None:
        """
        Tests the rm_container method in the ContainerController
        
        :param mocker: the Pytest mocker object
        :param client_1: fixture for mocking the docker.from_env class
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        assert ContainerController.rm_container(constants.CONTAINER_IMAGES.CSLE_PREFIX +
                                                'null' + '-' + 'level' + constants.CSLE.NAME + '--1') is True
        assert ContainerController.rm_container("JohnDoe") is False

    def test_rm_all_images(self, mocker: pytest_mock.MockFixture, client_1: pytest_mock.MockFixture) -> None:
        """
        Tests the rm_all_images method in the ContainerController
        
        :param mocker: the Pytest mocker object
        :param client_1: fixture for mocking the docker.from_env class
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        assert ContainerController.rm_all_images() is None

    def test_rm_image(self, mocker: pytest_mock.MockFixture, client_1: pytest_mock.MockFixture) -> None:
        """
        Tests the rm_image method in the ContainerController
        
        :param mocker: the Pytest mocker object
        :param client_1: fixture for mocking the docker.from_env class
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        assert ContainerController.rm_image(constants.CSLE.NAME) is True
        assert ContainerController.rm_image("JDoeName") is False

    def test_list_all_images(self, mocker: pytest_mock.MockFixture, client_1: pytest_mock.MockFixture) -> None:
        """
        Tests the list_all_images method inte the ContainerController

        :param mocker: the Pytest mocker object
        :param client_1: fixture for mocking the ContainerController
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        images_names = ContainerController.list_all_images()[0]
        assert images_names[0] == constants.CSLE.NAME
        assert images_names[1] == "yes"
        assert images_names[2] == "os"
        assert images_names[3] == "csle-architecture"
        assert images_names[4] == 100

    def test_list_docker_networks(self, mocker: pytest_mock.MockFixture, file_opener: pytest_mock.MockFixture) -> None:
        """
        Tests the list_docker_networks method inte the ContainerController

        :param mocker: the Pytest mocker object
        :param file_opener: fixture for mocking the ContainerController
        :return: None
        """
        mocker.patch('os.popen', side_effect=file_opener)
        test_networks_ids_str, test_network_ids = ContainerController.list_docker_networks()
        assert test_networks_ids_str[0] == f"{constants.CSLE.CSLE_NETWORK_PREFIX}1"
        assert test_networks_ids_str[1] == f"{constants.CSLE.CSLE_NETWORK_PREFIX}2"
        assert test_network_ids[0] == 1
        assert test_network_ids[1] == 2

    def test_list_all_networks(self, mocker: pytest_mock.MockFixture, file_opener: pytest_mock.MockFixture) -> None:
        """
        Tests the list_all_networks method
        
        :param mocker: the pytest mocker object
        :param file_opener: fixture for mocking the ContainerController
        :return: None
        """
        mocker.patch('os.popen', side_effect=file_opener)
        test_networks_ids_str = ContainerController.list_all_networks()
        assert test_networks_ids_str[0] == f"{constants.CSLE.CSLE_NETWORK_PREFIX}1"
        assert test_networks_ids_str[1] == f"{constants.CSLE.CSLE_NETWORK_PREFIX}2"

    def test_start_all_stopped_containers(self, mocker: pytest_mock.MockFixture, client_1: pytest_mock.MockFixture) \
            -> None:
        """
        Testing the start_all_stopped_containers method in the ContainerController

        :param mocker: the pytest mocker object
        :param client_1: pytest fixture for mocking the ContainerController
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        assert ContainerController.start_all_stopped_containers() is None

    def test_start_container(self, mocker: pytest_mock.MockFixture, client_1: pytest_mock.MockFixture) -> None:
        """
        Testing the start_container method in the ContainerController
        
        :param mocker: the Pytest mocker object
        :param client_1: pytest fixture for mocking the ContainerController
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        assert ContainerController.start_container(constants.CONTAINER_IMAGES.CSLE_PREFIX +
                                                   'null' + '-' + 'level' + constants.CSLE.NAME + '--1') is True
        assert ContainerController.start_container("JohnDoe") is False

    def test_list_all_running_containers(self, mocker: pytest_mock.MockFixture, client_1: pytest_mock.MockFixture,
                                         client_2: pytest_mock.MockFixture,
                                         example_docker_env_metadata: DockerEnvMetadata) -> None:
        """
        Testing the list_all_running_containers method in the ContainerController

        :param mocker: the pytest mocker object
        :param client_1: pytest fixture for mocking the docker client 1
        :param client_2: pytest fixture for mocking the docker client 2
        :param example_docker_env_metadata: example docker env metadata
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        mocker.patch('docker.APIClient', side_effect=client_2)
        mocker.patch('csle_common.util.docker_util.DockerUtil.parse_runnning_emulation_infos',
                     result=[example_docker_env_metadata])
        assert len(ContainerController.list_all_running_containers()) == 0

    def test_list_all_running_containers_in_emulation(self, mocker: pytest_mock.MockFixture,
                                                      example_emulation_env_config, client_1: pytest_mock.MockFixture,
                                                      client_2: pytest_mock.MockFixture,
                                                      example_docker_env_metadata: DockerEnvMetadata) -> None:
        """
        Testing the list_all_running_containers_in_emulation in the ContainerController

        :param mocker: the pytest mocker object
        :param example_emulation_env_config: an example object being the emulation environmnt configuration
        :param client_1: pytest fixture for mocking the Docker first client
        :param client_2: pytest fixture for mocking the Docker second client
        :param example_docker_env_metadata: example docker env metadata
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        mocker.patch('docker.APIClient', side_effect=client_2)
        mocker.patch('csle_common.util.docker_util.DockerUtil.parse_runnning_emulation_infos',
                     result=[example_docker_env_metadata])
        running_emulation_containers, stopped_emulation_containers = ContainerController. \
            list_all_running_containers_in_emulation(example_emulation_env_config)
        assert len(running_emulation_containers) == 0
        assert stopped_emulation_containers[0].to_dict() == example_emulation_env_config. \
            containers_config.containers[0].to_dict()
        assert stopped_emulation_containers[1].to_dict() == example_emulation_env_config. \
            kafka_config.container.to_dict()
        assert stopped_emulation_containers[2].to_dict() == \
               example_emulation_env_config.elk_config.container.to_dict()
        assert stopped_emulation_containers[3].to_dict() == \
               example_emulation_env_config.sdn_controller_config.container.to_dict()

    def test_list_all_active_networks_for_emulation(self, mocker: pytest_mock.MockFixture,
                                                    example_emulation_env_config: EmulationEnvConfig,
                                                    file_opener) -> None:
        """
        Testing the list_all_active_networks_for_emulation in the ContainerController

        :param mocker: the pytest mocker object
        :param example_emulation_env_config: an example object being the emulation environment configuration
        :param file_opener: fixture for mocking the ContainerController
        :return: None
        """
        mocker.patch("os.popen", side_effect=file_opener)
        active_emulation_networks, inactive_emulation_networks = \
            ContainerController.list_all_active_networks_for_emulation(
                example_emulation_env_config)
        assert inactive_emulation_networks == []
        assert active_emulation_networks[0].to_dict() == \
               example_emulation_env_config.containers_config.networks[0].to_dict()

    def test_list_running_emulations(self, mocker: pytest_mock.MockFixture,
                                     example_emulation_env_config: EmulationEnvConfig,
                                     client_1: pytest_mock.MockFixture,
                                     client_2: pytest_mock.MockFixture,
                                     example_docker_env_metadata: DockerEnvMetadata) -> None:
        """
        Testing the list_running_emulations method in the ContainerController
        
        :param mocker:the pytest mocker object
        :param example_emulation_env_config: fixture for mocking, fetched from the conftest file
        :param client_1: pytest fixture for mocking the Docker first client
        :param client_2: pytest fixture for mocking the Docker second client
        :param example_docker_env_metadata: example docker env metadata
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        mocker.patch('docker.APIClient', side_effect=client_2)
        mocker.patch('csle_common.util.docker_util.DockerUtil.parse_runnning_emulation_infos',
                     result=[example_docker_env_metadata])
        emulation_name_list = ContainerController.list_running_emulations()
        assert len(emulation_name_list) == 0

    def test_is_emulation_running(self, mocker: pytest_mock.MockFixture,
                                  example_emulation_env_config: EmulationEnvConfig,
                                  client_1: pytest_mock.MockFixture,
                                  client_2: pytest_mock.MockFixture,
                                  example_docker_env_metadata: DockerEnvMetadata) -> None:
        """
        Testing the is_emulation_running method in the ContainerController

        :param mocker:the pytest mocker object
        :param example_emulation_env_config: fixture for mocking, fetched from the conftest file
        :param client_1: pytest fixture for mocking the Docker first client
        :param client_2: pytest fixture for mocking the Docker second client
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        mocker.patch('docker.APIClient', side_effect=client_2)
        mocker.patch('csle_common.util.docker_util.DockerUtil.parse_runnning_emulation_infos',
                     result=[example_docker_env_metadata])
        assert not ContainerController.is_emulation_running(example_emulation_env_config)

    def test_list_all_stopped_containers(self, mocker: pytest_mock.MockFixture, client_1: pytest_mock.MockFixture,
                                         client_2: pytest_mock.MockFixture) -> None:
        """
        Testing the is_emulation_running method in the ContainerController

        :param mocker:the pytest mocker object
        :param example_emulation_env_config: fixture for mocking, fetched from the conftest file
        :param client_1: pytest fixture for mocking the Docker first client
        :param client_2: pytest fixture for mocking the Docker second client
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        mocker.patch('docker.APIClient', side_effect=client_2)
        test_tuple = ContainerController.list_all_stopped_containers()[0]
        assert test_tuple[0] == constants.CONTAINER_IMAGES.CSLE_PREFIX + \
               'null' + '-' + 'level' + constants.CSLE.NAME + '--1'
        assert test_tuple[1] == 'JDoeImage'
        assert test_tuple[2] == '123.456.78.99'

    def test_get_network_references(self, mocker: pytest_mock.MockFixture, client_1: pytest_mock.MockFixture) -> None:
        """
        Testing the get_network_references method in the ContainerController

        :param mocker:the pytest mocker object
        :param client_1: pytest fixture for mocking the Docker first client
        :param client_2: pytest fixture for mocking the Docker second client
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        test_networks = ContainerController.get_network_references()
        assert test_networks[0].name == constants.CONTAINER_IMAGES.CSLE_PREFIX + \
               'null' + '-' + 'level' + constants.CSLE.NAME + '--1'

    def test_create_networks(self, mocker: pytest_mock.MockFixture, client_1,
                             example_containers_config: ContainersConfig, example_config: Config, ipam_pool,
                             ipam_config) -> None:
        """
        Testing the create_networks method in the ContainerController

        :param mocker: the pytest mocker object
        :param client_1: pytest fixture for mocking the Docker first client
        :param client_2: pytest fixture for mocking the Docker second client
        :param example_containers_config: example containers config
        :param example_config: example config DTO
        :param ipam_pool: fixture for the Docker ipam_pool
        :param ipam_config: fixture for the Docker ipam_config
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        mocker.patch('csle_common.dao.emulation_config.config.Config.get_current_config', result=example_config)
        mocker.patch('docker.types.IPAMPool', side_effect=ipam_pool)
        mocker.patch('docker.types.IPAMConfig', side_effect=ipam_config)
        creation = ContainerController.create_networks(example_containers_config, logging.Logger("test"))
        assert creation is None

    def test_connect_containers_to_networks(self, mocker: pytest_mock.MockFixture,
                                            example_emulation_env_config: EmulationEnvConfig,
                                            sub_popen, client_1, client_2, file_opener) -> None:
        """
        Testing the connect_containers_to_networks method

        :param mocker: the pytest mocker object
        :param example_emulation_env_config: EmulationEnvironmentConfig fetched from the conftest file
        :param sub_popen: fixture mocking the subprocess.Popen
        :param client_1: pytest fixture for mocking the Docker first client
        :param client_2: pytest fixture for mocking the Docker second client
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch('subprocess.Popen', side_effect=sub_popen)
        mocker.patch('docker.from_env', side_effect=client_1)
        mocker.patch('docker.APIClient', side_effect=client_2)
        mocker.patch('os.popen', side_effect=file_opener)
        connection = ContainerController.connect_containers_to_networks(example_emulation_env_config, '123.456.78.99',
                                                                        logger=logging.Logger("test"))
        assert connection is None

    def test_connect_container_to_network(self, mocker: pytest_mock.MockFixture,
                                          example_node_container_config: NodeContainerConfig, sub_popen,
                                          file_opener, client_1, client_2, ) -> None:
        """
        Testing connect_container_to_network method in the ContainerController
        
        :param mocker: the pytest mocker object
        :param example_node_container_config: an example NodeContainerConfig fetched from the conftest file
        :param sub_popen: fixture mocking the subprocess.Popen
        :param file_opener: fixture mocking the os.popen
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch('subprocess.Popen', side_effect=sub_popen)
        mocker.patch('docker.from_env', side_effect=client_1)
        mocker.patch('docker.APIClient', side_effect=client_2)
        mocker.patch('os.popen', side_effect=file_opener)
        connection = ContainerController.connect_container_to_network(
            example_node_container_config, logging.Logger("test"))
        assert connection is None

    def test_start_docker_stats_thread(self, mocker: pytest_mock.MockFixture,
                                       example_emulation_execution: EmulationExecution, true_running_stats_manager,
                                       false_running_stats_manager, sub_popen, start_fixture) -> None:
        """
        Testing the start_docker_stats_thread in the ContainerController

        :param mocker: the pytest mocker object
        :param example_node_container_config: an example NodeContainerConfig fetched from the conftest file
        :param sub_popen: fixture mocking the subprocess.Popen
        :param file_opener: fixture mocking the os.popen
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch('subprocess.Popen', side_effect=sub_popen)
        mocker.patch('csle_common.controllers.management_system_controller.' +
                     'ManagementSystemController.is_statsmanager_running',
                     side_effect=true_running_stats_manager)
        mocker.patch('csle_collector.docker_stats_manager.query_docker_stats_manager.start_docker_stats_monitor',
                     side_effect=start_fixture)
        starter = ContainerController.start_docker_stats_thread(example_emulation_execution,
                                                                physical_server_ip='123.456.78.99',
                                                                logger=logging.Logger("test"))
        assert starter is None
        mocker.patch('csle_common.controllers.management_system_controller.' +
                     'ManagementSystemController.is_statsmanager_running',
                     side_effect=false_running_stats_manager)
        ContainerController.start_docker_stats_thread(example_emulation_execution,
                                                      physical_server_ip='123.456.78.99',
                                                      logger=logging.Logger("test"))

    def test_stop_docker_stats_thread(self, mocker: pytest_mock.MockFixture,
                                      example_emulation_execution: EmulationExecution,
                                      true_stop_fixture, false_running_stats_manager,
                                      true_running_stats_manager,
                                      false_stop_fixture, stop_fixture):
        """
        Testing the stop_docker_stats_thread

        :param mocker: the pytest mocker object
        :param example_emulation_execution: EmulationExecution object fetched from the config file
        :param true_stop_fixture: pytest fixture
        :param false_running_stats_manager: pytest fixture
        :param true_running_stats_manager: pytest fixture
        :param false_stop_fixture: pytest fixture
        :param stop_fixture: pytest fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch('csle_collector.docker_stats_manager.query_docker_stats_manager.stop_docker_stats_monitor',
                     side_effect=stop_fixture)
        mocker.patch('csle_common.controllers.management_system_controller.' +
                     'ManagementSystemController.is_statsmanager_running',
                     side_effect=true_running_stats_manager)
        mocker.patch('csle_common.controllers.management_system_controller.' +
                     'ManagementSystemController.stop_docker_statsmanager',
                     side_effect=true_stop_fixture)
        stopper = ContainerController.stop_docker_stats_thread(example_emulation_execution, "123.456.78.99",
                                                               logging.getLogger("test"))
        assert stopper is None
        mocker.patch('csle_common.controllers.management_system_controller.' +
                     'ManagementSystemController.stop_docker_statsmanager',
                     side_effect=false_stop_fixture)
        stopper = ContainerController.stop_docker_stats_thread(example_emulation_execution, "123.456.78.99",
                                                               logging.getLogger("test"))
        assert stopper is None
        mocker.patch('csle_common.controllers.management_system_controller.' +
                     'ManagementSystemController.is_statsmanager_running',
                     side_effect=false_running_stats_manager)
        stopper = ContainerController.stop_docker_stats_thread(example_emulation_execution, "123.456.78.99",
                                                               logging.getLogger("test"))
        assert stopper is None

    def test_get_docker_stats_manager_status(self, mocker: pytest_mock.MockFixture, host_ip,
                                             example_docker_stats_manager_config: DockerStatsManagerConfig,
                                             dsm_status, stub):
        """
        Testing the get_docker_stats_manager_status method in the ContainerController

        :param mocker: the pytest mocker object
        :param host_ip: the host_ip fixture
        :param example_docker_stats_manager_config: the example_docker_stats_manager_config fixture
        :param dsm_status: the dsm_status fixture
        :param stub: the stub fixture
        :return: None
        """
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_host_ip', side_effect=host_ip)
        mocker.patch('csle_collector.docker_stats_manager.query_docker_stats_manager.get_docker_stats_manager_status',
                     side_effect=dsm_status)
        mocker.patch('csle_collector.docker_stats_manager.' +
                     'docker_stats_manager_pb2_grpc.DockerStatsManagerStub', side_effect=stub)
        dsm_dto = ContainerController.get_docker_stats_manager_status(example_docker_stats_manager_config)
        assert dsm_dto.num_monitors == 10
        assert dsm_dto.emulations == ["JDoeEmulation"]
        assert dsm_dto.emulation_executions == [10]

    def test_get_docker_stats_manager_status_by_ip_and_port(self, mocker: pytest_mock.MockFixture,
                                                            host_ip, dsm_status, stub):
        """
        Testing the get_docker_stats_manager_status_by_ip_and_port method in the ContainerController

        :param mocker: the pytest mocker object
        :param host_ip: the host_ip fixture
        :param dsm_status: the dsm_status fixture
        :param stub: the stub fixture
        :return: None
        """
        mocker.patch('csle_common.util.general_util.GeneralUtil.get_host_ip', side_effet=host_ip)
        mocker.patch('csle_collector.docker_stats_manager.query_docker_stats_manager.get_docker_stats_manager_status',
                     side_effect=dsm_status)
        mocker.patch('csle_collector.docker_stats_manager.docker_stats_manager_pb2_grpc' +
                     '.DockerStatsManagerStub', side_effect=stub)
        dsm_dto = ContainerController.get_docker_stats_manager_status_by_ip_and_port("123.456.78.99", 1)
        assert dsm_dto.num_monitors == 10
        assert dsm_dto.emulations == ["JDoeEmulation"]
        assert dsm_dto.emulation_executions == [10]

    def test_create_network_from_dto(self, mocker: pytest_mock.MockFixture, example_container_network: ContainerNetwork,
                                     client_1, ipam_pool, ipam_config, example_config: Config) -> None:
        """
        Testing the create_network_from_dto in the ContainerController

        :param mocker: the pytest mocker object
        :param client_1: the client_1 fixture
        :param ipam_pool: the ipam_pool fixture
        :param ipam_config: the ipam_confoig fixture
        :param example_config: the example_config fixture from conftest
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        mocker.patch('docker.types.IPAMPool', side_effect=ipam_pool)
        mocker.patch('docker.types.IPAMConfig', side_effect=ipam_config)
        mocker.patch('csle_common.dao.emulation_config.config.Config.get_current_config', result=example_config)
        creator = ContainerController.create_network_from_dto(example_container_network, logging.Logger("test"))
        assert creator is None

    def test_create_network(self, mocker: pytest_mock.MockFixture, client_1, ipam_pool, ipam_config) -> None:
        """
        Testing the create_network in the ContainerController

        :param mocker: the pytest mocker object
        :param client_1: the client_1 fixture
        :param ipam_pool: the ipam_pool fixture
        :param ipam_config: the ipam_confoig fixture
        :param example_config: the example_config fixture from conftest
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        mocker.patch('docker.types.IPAMPool', side_effect=ipam_pool)
        mocker.patch('docker.types.IPAMConfig', side_effect=ipam_config)
        creator = ContainerController.create_network(name="JDoeCreator",
                                                     subnetmask="null", logger=logging.Logger("test"))
        assert creator is None

    def test_remove_network(self, mocker: pytest_mock.MockFixture, client_1) -> None:
        """
        Testing the remove_network method in the ContainerController

        :param mocker: the pytest mocker object
        :param client_1: the client_1 fixture
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        remover = ContainerController.remove_network(constants.CONTAINER_IMAGES.CSLE_PREFIX +
                                                     'null' + '-' + 'level' + constants.CSLE.NAME + '--1',
                                                     logging.getLogger())
        assert remover is None

    def test_remove_networks(self, mocker: pytest_mock.MockFixture, client_1) -> None:
        """
        Testing the remove_network method in the ContainerController

        :param mocker: the pytests mocker object
        :param client_1: the client_1 fixture
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        remover = ContainerController.remove_networks([constants.CONTAINER_IMAGES.CSLE_PREFIX +
                                                       'null' + '-' + 'level' + constants.CSLE.NAME + '--1'],
                                                      logging.getLogger())
        assert remover is True
        remover = ContainerController.remove_networks(["JohnDoe"], logging.getLogger())
        assert remover is False

    def test_rm_all_networks(self, mocker: pytest_mock.MockFixture, client_1) -> None:
        """
        Testing the rm_all_networks method in the ContainerController
        :param mocker_ the pytest mocker object
        :param client_1: the client_1 fixture
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        remover = ContainerController.rm_all_networks(logging.getLogger())
        assert remover is None

    def test_rm_network(self, mocker: pytest_mock.MockFixture, client_1) -> None:
        """
        Testing the rm_network method in the ContainerController

        :param mocker: the pytest mocker object
        :param client_1: the client_1 fixture
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        remover = ContainerController.rm_network(constants.CSLE.NAME, logging.getLogger())
        assert remover is True
        remover = ContainerController.rm_network("JDoe", logging.getLogger())
        assert remover is False

    def test_run_command(self, mocker: pytest_mock.MockFixture, client_1, client_2):
        """
        Testing the run_command method in the ContainerController
        
        :param mocker: the pytest mocker object
        :param client_1: the client_1 fixture
        :param client_2: the client_2 fixture
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        mocker.patch('docker.APIClient', side_effect=client_2)
        runner = ContainerController.run_command(cmd=constants.MANAGEMENT.LIST_STOPPED)
        assert runner is None

    def test_get_docker_stats_managers_ips(self, mocker: pytest_mock.MockFixture, socket_fix,
                                           example_emulation_env_config: EmulationEnvConfig):
        """
        Testing the get_docker_stats_managers_ips
        
        :param mocker: the pytest mocker object
        :param host_ip: the host_ip fixture
        :param example_emulation_env_config: the example_emulation_env_config fixture from the conftest
        :return: None
        """
        mocker.patch('socket.socket', side_effect=socket_fix)
        ip = ContainerController.get_docker_stats_managers_ips(example_emulation_env_config)
        assert ip == ["123.456.78.99"]

    def test_get_docker_stats_managers_ports(self, example_emulation_env_config: EmulationEnvConfig):
        """
        Testing the get_docker_stats_managers_ports in the ContainerController

        :param mocker: the pytest mocker object
        :pram example_emulation_config: the example_emulation_config fixture fetched from the conftest file
        :return: None
        """
        test_list = ContainerController.get_docker_stats_managers_ports(example_emulation_env_config)
        assert test_list[0] == 50046

    def test_get_docker_stats_managers_info(self, mocker: pytest_mock.MockFixture, socket_fix,
                                            example_emulation_env_config: EmulationEnvConfig,
                                            host_ip, dsm_status, stub,
                                            example_docker_stats_managers_info: DockerStatsManagersInfo):
        """
        Testing the get_docker_stats_managers_info
        
        :param mocker: thepytest mocker object
        :param socket_fix: the socket_fix fixture
        :pram example_emulation_config: the example_emulation_config fixture fetched from the conftest file
        :param host_ip: the host_ip fixture
        :param dsm_status: the dsm_status fixture
        :param stub: the stub fixture
        :return: None
        """
        mocker.patch('time.sleep', return_value=None)
        mocker.patch('socket.socket', side_effect=socket_fix)
        mocker.patch('csle_collector.docker_stats_manager.query_docker_stats_manager.get_docker_stats_manager_status',
                     side_effect=dsm_status)
        mocker.patch('csle_collector.docker_stats_manager.docker_stats_manager_pb2_grpc.DockerStatsManagerStub',
                     side_effect=stub)
        docker_stat = ContainerController.get_docker_stats_managers_info(
            example_emulation_env_config, ["123.456.78.99"], "123.456.78.99", logging.getLogger())
        assert docker_stat.docker_stats_managers_running[0] is True
        assert docker_stat.ips[0] == "123.456.78.99"
        assert docker_stat.emulation_name == "JDoeEmulation"
        assert docker_stat.execution_id == 10
        docker_stat_dict = docker_stat.to_dict()
        assert docker_stat_dict["docker_stats_managers_statuses"][0]["num_monitors"] == 10
        assert docker_stat_dict["docker_stats_managers_statuses"][0]["emulations"][0] == "JDoeEmulation"
        assert docker_stat_dict["docker_stats_managers_statuses"][0]["emulation_executions"][0] == 10
        assert docker_stat.ports[0] == 50046
