import pytest
import docker 
import csle_common.constants.constants as constants

@pytest.fixture(scope="module")
def docker_client() -> None:
    """
    Provide a Docker client instance

    :return: None
    """
    return docker.from_env()

@pytest.fixture(scope="module")
def container(docker_client) -> None:
    """
    Starts a Docker container before running tests and ensures its stopped and removed after tests complete.

    :param docker_client: docker_client
    
    :return: None
    """
    image_with_tag = f"kimham/{constants.CONTAINER_IMAGES.FTP_1}:0.6.0"
    container = docker_client.containers.run(image_with_tag, detach=True)
    yield container
    container.stop()
    container.remove()
    
def test_container_running(docker_client, container) -> None:
    """
    Checks if the container is running and check if its in the running containers list

    :param docker_client: docker_client
    
    :return: None
    """
    running_containers = docker_client.containers.list()
    assert container in running_containers