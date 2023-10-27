import pytest_mock
from csle_common.controllers.container_controller import ContainerController


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
        mocked_container.configure_mock(**{"name.return_value": "test_container_name"})
        mocked_container.configure_mock(**{"stop.return_value": None})
        mocked_docker_client.configure_mock(**{"list.return_value": [mocked_container]})
        ContainerController.stop_all_running_containers()
