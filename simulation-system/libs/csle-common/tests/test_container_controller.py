import pytest_mock
from csle_common.controllers.container_controller import ContainerController
import csle_common.constants.constants as constants
import logging

class TestContainerControllerSuite:
    """
    Test suite for the container controller
    """

    def test_stop_all_running_containers(self, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stop_all_running_containers method of the ContainerController

        :param mocker: the Pytest mock object
        :return: None
        """
        mocked_docker_client = mocker.MagicMock()
        mocker.patch('docker.from_env', return_value=mocked_docker_client)
        mocked_container = mocker.MagicMock()
        name = constants.CSLE.NAME
        mocked_container.configure_mock(**{"name.return_value": f"{name}"})
        mocked_container.configure_mock(**{"stop.return_value": None})
        mocked_docker_client.configure_mock(**{"list.return_value": [mocked_container]})
        assert ContainerController.stop_all_running_containers() is None
