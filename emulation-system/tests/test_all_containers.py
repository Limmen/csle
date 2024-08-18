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
def containers(docker_client) -> None:
    """
    Starts Docker containers before running tests and ensures its stopped and removed after tests complete.

    :param docker_client: docker_client
    
    :return: None
    """
    match_tag = "0.6.0"
    all_images = docker_client.images.list()
    images = [image for image in all_images
              if (any(match_tag in tag for tag in image.tags) and all("base" not in tag for tag in image.tags)
                  and all(f"{constants.CONTAINER_IMAGES.DOCKERHUB_USERNAME}/{constants.CONTAINER_IMAGES.BLANK_UBUNTU_22}:0.6.0" not in tag for tag in image.tags))]
    started_containers = []
    try:
        for image in images:
            container = docker_client.containers.run(image.id, detach=True)
            started_containers.append(container)
        yield started_containers
    finally:
        for container in started_containers:
            container.stop()
            container.remove()


def test_container_running(docker_client, containers) -> None:
    """
    Checks if the container is running and check if its in the running containers list

    :param docker_client: docker_client
    
    :return: None
    """
    running_containers = docker_client.containers.list()
    failed_containers = []
    for container in containers:
        if container not in running_containers:
            failed_containers.append(
                f"Container with ID {container.id} and image {container.image.tags} is not running.")
    assert not failed_containers, f"Some containers failed to run: {failed_containers}"
