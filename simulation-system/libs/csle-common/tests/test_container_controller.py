import pytest_mock
from csle_common.controllers.container_controller import ContainerController
import csle_common.constants.constants as constants
import logging
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
        Pytest fixture
        
        '''
        def from_env():
            class client1():
                def __init__(self) -> None:
                    pass
                class containers():
                    def __init__(self) -> None:
                        pass
                    def list():
                        class element():
                            def __init__(self) -> None:
                                self.name = constants.CSLE.NAME
                        return [element()]
            return client1
        from_env_mocker = mocker.MagicMock(side_effect=from_env)
        return from_env_mocker

    def test_stop_all_running_containers_1(self, mocker: pytest_mock.MockFixture, client_1) -> None:
        """
        Tests the stop_all_running_containers method of the ContainerController

        :param mocker: the Pytest mock object
        :return: None
        """
        mocker.patch('docker.from_env', return_value=client_1)

        assert ContainerController.stop_all_running_containers() is None

    def test_stop_all_running_containers_2(self, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stop_all_running_containers method of the ContainerController

        :param mocker: the Pytest mock object
        :return: None
        """
        mocked_docker_client = mocker.MagicMock()
        mocker.patch('docker.from_env', return_value=mocked_docker_client)
        mocked_container = mocker.MagicMock()
        mocked_container.configure_mock(**{"name.return_value": "test_container_name"})
        mocked_container.configure_mock(**{"stop.return_value": None})
        mocked_docker_client.configure_mock(**{"list.return_value": [mocked_container]})
        assert ContainerController.stop_all_running_containers() is None

    def test_stop_container(self, mocker: pytest_mock.MockFixtre) -> None:
        """
        Test the stop_container method od the ContainerController
        :param mocker: the Pytest mock object
        :return: None
        """