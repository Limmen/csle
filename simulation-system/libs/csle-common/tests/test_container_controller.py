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
                                pass
                            def name(self):
                                return "JohnDoe"
                        return [element()]
            return client1
        from_env_mocker = mocker.MagicMock(side_effect=from_env)
        return from_env_mocker

    def test_stop_all_running_containers(self, mocker: pytest_mock.MockFixture, client_1) -> None:
        """
        Tests the stop_all_running_containers method of the ContainerController

        :param mocker: the Pytest mock object
        :return: None
        """
        # mocked_docker_client = client_1
        '''class client1():
            def __init__(self) -> None:
                pass
            class containers():
                def __init__(self) -> None:
                    pass
                def list():
                    return ["johndoe"]'''
        
        # mocker.patch('docker.from_env', return_value=client1)
        mocker.patch('docker.from_env', side_effect=client_1)
        # mocker.patch('docker.from_env.containers.list', return_value=container.list())
        # mocked_container = mocker.MagicMock()
        # name = constants.CSLE.NAME
        # mocked_container.configure_mock(**{"name.return_value": f"{name}"})
        # mocked_container.configure_mock(**{"stop.return_value": None})
        #   mocked_docker_client.configure_mock(**{"list.return_value": [mocked_container]})
        assert ContainerController.stop_all_running_containers() is None
