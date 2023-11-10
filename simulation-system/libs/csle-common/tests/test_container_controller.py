import pytest_mock
from csle_common.controllers.container_controller import ContainerController
import csle_common.constants.constants as constants
import logging
import io
import pytest

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
                    class element():
                        def __init__(self) -> None:
                            self.name = constants.CSLE.NAME
                            self.status = constants.DOCKER.CONTAINER_EXIT_STATUS
                        def stop(self):
                            return None
                        def remove(self):
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
                    return [element()]
                def remove(image, force):
                    return None
                
        from_env_mocker = mocker.MagicMock(side_effect=from_env)
        return from_env_mocker

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
        assert ContainerController.stop_container(constants.CSLE.NAME) is True
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
        assert ContainerController.rm_container(constants.CSLE.NAME) is True
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
        assert ContainerController.list_all_images() is None

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
        :param client_1: fixture for mocking the ContainerController
        :return: None
        """
        mocker.patch('os.popen', side_effect=file_opener)
        test_networks_ids_str, test_network_ids = ContainerController.list_docker_networks()
        assert test_networks_ids_str[0] == f"{constants.CSLE.CSLE_NETWORK_PREFIX}1"
        assert test_networks_ids_str[1] == f"{constants.CSLE.CSLE_NETWORK_PREFIX}2"
        assert test_network_ids[0] == 1
        assert test_network_ids[1] == 2
