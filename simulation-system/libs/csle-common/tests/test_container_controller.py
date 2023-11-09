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
        class from_env():
            def __init__(self) -> None:
                pass
            class containers:
                def list():
                    class element():
                        def __init__(self) -> None:
                            self.name = constants.CSLE.NAME
                        def stop(self):
                            return None
                    return [element()]
                
        from_env_mocker = mocker.MagicMock(side_effect=from_env)
        return from_env_mocker

    def test_stop_all_running_containers(self, mocker: pytest_mock.MockFixture, client_1) -> None:
        """
        Tests the stop_all_running_containers method of the ContainerController

        :param mocker: the Pytest mock object
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)

        assert ContainerController.stop_all_running_containers() is None

    def test_stop_container(self, mocker: pytest_mock.MockFixture,
                            client_1) -> None:
        """
        Test the stop_container method od the ContainerController
        :param mocker: the Pytest mock object
        :return: None
        """
        mocker.patch('docker.from_env', side_effect=client_1)
        assert ContainerController.stop_container(constants.CSLE.NAME) is True
        assert ContainerController.stop_container("John Doe") is False