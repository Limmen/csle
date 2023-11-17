import pytest_mock

from csle_common.controllers.container_controller import ContainerController
import csle_common.constants.constants as constants
import io
import pytest
import logging


class TestContainerControllerSuite:
    """
    Test suite for the container controller
    """

    @pytest.fixture
    def from_env_fixt(self, mocker: pytest_mock.MockFixture):
        def from_env():
            class containers():

                def __init__(self) -> None:
                    pass

                def list(self):
                    return ["JohnDoe"]
        from_env_mocker = mocker.MagicMock(side_effect=from_env)
        return from_env_mocker

    @pytest.fixture
    def client_1(self, mocker: pytest_mock.MockFixture):
        '''
        Pytest fixture for mocking the docker.from_env() method
        
        :param mocker: the Pytest mocker object
        :return: the mocked function
        '''
        class from_env():
            def __init__(self) -> None:
                pass

            class containers:

                def list(all=False):
                    class image():
                        def __init__(self) -> None:
                            self.short_id = '1'
                            self.tags = ['tags']
            
                    class element():

                        def __init__(self) -> None:
                            self.name = constants.CONTAINER_IMAGES.CSLE_PREFIX +\
                                'null' + '-' + 'level' + constants.CSLE.NAME + '--1'
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

            class images:

                def list():
                    class element():
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

                def remove(image, force):
                    return None
                
        from_env_mocker = mocker.MagicMock(side_effect=from_env)
        return from_env_mocker

    @pytest.fixture
    def client_2(self, mocker: pytest_mock.MockFixture):
        """
        Pytest fixture for mocking the docker.APIClient
        
        :param mocker: the Pytest mocker object
        :return: the mocked object
        """
        class APIClient():
            def __init__(self, base_url) -> None:
                self.base_url = base_url
            
            def inspect_container(self, param: int):
                dict = {constants.DOCKER.NETWORK_SETTINGS:
                        {constants.DOCKER.NETWORKS:
                         {'net_key': {constants.DOCKER.IP_ADDRESS_INFO: "123.456.78.99",
                                      constants.DOCKER.NETWORK_ID_INFO: 1,
                                      constants.DOCKER.GATEWAY_INFO: "null",
                                      constants.DOCKER.MAC_ADDRESS_INFO: "null",
                                      constants.DOCKER.IP_PREFIX_LEN_INFO: 1}}},
                        constants.DOCKER.CREATED_INFO: "created_info",
                        constants.DOCKER.CONFIG: {constants.DOCKER.HOSTNAME_INFO: "JDoeHost",
                                                  constants.DOCKER.IMAGE: "JDoeImage"}}
                return dict
        api_mocker = mocker.MagicMock(side_effect=APIClient)
        return api_mocker

    @pytest.fixture
    def file_opener(self, mocker: pytest_mock.MockFixture):
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

    def test_stop_all_running_containers(self, mocker: pytest_mock.MockFixture, client_1) -> None:
        """
        Tests the stop_all_running_containers method of the ContainerController

        :param mocker: the Pytest mock object
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)

        assert ContainerController.stop_all_running_containers() is None

    def test_stop_container(self, mocker: pytest_mock.MockFixture,
                            client_1: pytest_mock.MockFixture) -> None:
        """
        Tests the stop_container method od the ContainerController
        :param mocker: the Pytest mock object
        :param client_1: fixture for mocking the docker.from_env class
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        assert ContainerController.stop_container(constants.CONTAINER_IMAGES.CSLE_PREFIX +\
                                                  'null' + '-' + 'level' + constants.CSLE.NAME + '--1') is True
        assert ContainerController.stop_container("John Doe") is False

    def test_rm_all_stopped_containers(self, mocker: pytest_mock.MockFixture,
                                       client_1: pytest_mock.MockFixture):
        """
        Tests the rm_all_stopped_containers in the ContainerController
        :param mocker: the Pytest mocker object
        :param client_1: fixture for mocking the docker.from_env class
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        assert ContainerController.rm_all_stopped_containers() is None

    def test_rm_container(self, mocker: pytest_mock.MockFixture,
                          client_1: pytest_mock.MockFixture) -> None:
        """
        Tests the rm_container method in the ContainerController
        
        :param mocker: the Pytest mocker object
        :param client_1: fixture for mocking the docker.from_env class
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        assert ContainerController.rm_container(constants.CONTAINER_IMAGES.CSLE_PREFIX +\
                                                'null' + '-' + 'level' + constants.CSLE.NAME + '--1') is True
        assert ContainerController.rm_container("JohnDoe") is False

    def test_rm_all_images(self, mocker: pytest_mock.MockFixture,
                           client_1: pytest_mock.MockFixture) -> None:
        """
        Tests the rm_all_images method in the ContainerController
        
        :param mocker: the Pytest mocker object
        :param client_1: fixture for mocking the docker.from_env class
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        assert ContainerController.rm_all_images() is None

    def test_rm_image(self, mocker: pytest_mock.MockFixture,
                      client_1: pytest_mock.MockFixture) -> None:
        """
        Tests the rm_image method in the ContainerController
        
        :param mocker: the Pytest mocker object
        :param client_1: fixture for mocking the docker.from_env class
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        assert ContainerController.rm_image(constants.CSLE.NAME) is True
        assert ContainerController.rm_image("JDoeName") is False

    def test_list_all_images(self, mocker: pytest_mock.MockFixture,
                             client_1: pytest_mock.MockFixture) -> None:
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

    def test_list_docker_networks(self, mocker: pytest_mock.MockFixture,
                                  file_opener: pytest_mock.MockFixture) -> None:
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

    def test_list_all_networks(self, mocker: pytest_mock.MockFixture,
                               file_opener: pytest_mock.MockFixture) -> None:
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

    def test_start_all_stopped_containers(self, mocker: pytest_mock.MockFixture,
                                          client_1: pytest_mock.MockFixture) -> None:
        """
        Testing the start_all_stopped_containers method in the ContainerController

        :param mocker: the pytest mocker object
        :param client_1: pytest fixture for mocking the ContainerController
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        assert ContainerController.start_all_stopped_containers() is None

    def test_start_container(self, mocker: pytest_mock.MockFixture,
                             client_1: pytest_mock.MockFixture) -> None:
        """
        Testing the start_container method in the ContainerController
        
        :param mocker: the Pytest mocker object
        :param client_1: pytest fixture for mocking the ContainerController
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        assert ContainerController.start_container(constants.CONTAINER_IMAGES.CSLE_PREFIX +\
                                                   'null' + '-' + 'level' + constants.CSLE.NAME + '--1') is True
        assert ContainerController.start_container("JohnDoe") is False

    def test_list_all_running_containers(self, mocker: pytest_mock.MockFixture,
                                         client_1: pytest_mock.MockFixture,
                                         client_2: pytest_mock.MockFixture) -> None:
        """
        Testing the list_all_running_containers method in the ContainerController

        :param mocker: the pytest mocker object
        :param client_1: pytest fixture for mocking the ContainerController
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        mocker.patch('docker.APIClient', side_effect=client_2)
        for parsed_env_tuple in ContainerController.list_all_running_containers():
            assert parsed_env_tuple[0] == constants.CONTAINER_IMAGES.CSLE_PREFIX +\
                'null' + '-' + 'level' + constants.CSLE.NAME + '--1'
            assert parsed_env_tuple[1] == "JDoeImage"
            assert parsed_env_tuple[2] == "123.456.78.99"

    def test_list_all_running_containers_in_emulation(self, mocker: pytest_mock.MockFixture,
                                                      example_emulation_env_config,
                                                      client_1: pytest_mock.MockFixture,
                                                      client_2: pytest_mock.MockFixture) -> None:
        """
        Testing the list_all_running_containers_in_emulation in the ContainerController
        :param mocker: the pytest mocker object
        :param example_emulation_env_config: an example object being the emulation environmnt configuration
        :param client_1: pytest fixture for mocking the ContainerController
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        mocker.patch('docker.APIClient', side_effect=client_2)
        running_emulation_containers, stopped_emulation_containers = ContainerController.\
            list_all_running_containers_in_emulation(example_emulation_env_config)
        assert stopped_emulation_containers == []
        assert running_emulation_containers[0].to_dict() == example_emulation_env_config.\
            containers_config.containers[0].to_dict()
        assert running_emulation_containers[1].to_dict() == example_emulation_env_config.\
            kafka_config.container.to_dict()
        assert running_emulation_containers[2].to_dict() == example_emulation_env_config.\
                    elk_config.container.to_dict()
        assert running_emulation_containers[3].to_dict() == example_emulation_env_config.\
                    sdn_controller_config.container.to_dict()

    def test_list_all_active_networks_for_emulation(self, mocker: pytest_mock.MockFixture,
                                                    example_emulation_env_config,
                                                    client_1: pytest_mock.MockFixture,
                                                    client_2: pytest_mock.MockFixture,
                                                    file_opener) -> None:
        """
        Testing the list_all_active_networks_for_emulation in the ContainerController
        :param mocker: the pytest mocker object
        :param example_emulation_env_config: an example object being the emulation environmnt configuration
        :param client_1: pytest fixture for mocking the ContainerController
        :return: None
        """
        mocker.patch("os.popen", side_effect=file_opener)
        active_emulation_networks, inactive_emulation_networks = ContainerController.list_all_active_networks_for_emulation(example_emulation_env_config)
        assert inactive_emulation_networks == []
        assert active_emulation_networks[0].to_dict() == example_emulation_env_config.containers_config.networks[0].to_dict()