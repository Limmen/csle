import pytest
import docker 
import csle_common.constants.constants as constants

@pytest.fixture(scope="module")
def docker_client() -> None:
    return docker.from_env()

@pytest.fixture(scope="module")
def container(docker_client) -> None:
    image_with_tag = f"kimham/{constants.CONTAINER_IMAGES.FTP_1}:0.6.0"
    container = docker_client.containers.run(image_with_tag, detach=True)
    yield container
    container.stop()
    container.remove()
    
def test_container_running(docker_client, container) -> None:
    running_containers = docker_client.containers.list()
    assert container in running_containers