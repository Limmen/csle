from typing import Generator
import pytest
import docker
import logging
import csle_common.constants.constants as constants
from csle_common.metastore.metastore_facade import MetastoreFacade


@pytest.fixture(scope="module")
def docker_client() -> None:
    """
    Provide a Docker client instance

    :return: None
    """
    return docker.from_env()


@pytest.fixture(scope="module")
def containers(docker_client) -> Generator:
    """
    Starts Docker containers before running tests and ensures its stopped and removed after tests complete.

    :param docker_client: docker_client
    :return: None
    """
    config = MetastoreFacade.get_config(id=1)
    match_tag = config.version
    all_images = docker_client.images.list()
    images = [image for image in all_images
              if (any(match_tag in tag for tag in image.tags)
                  and all(constants.CONTAINER_IMAGES.BASE not in tag for tag in image.tags)
                  and all(f"{constants.CONTAINER_IMAGES.BLANK}" not in tag for tag in image.tags))]
    started_containers = []
    try:
        for image in images:
            logging.info(f"Starting a container with image {image.tags}")
            container = docker_client.containers.run(image.id, detach=True)
            started_containers.append(container)
        yield started_containers
    finally:
        for container in started_containers:
            logging.info(f"Stopping and removing container: {container.id} with image {container.image.tags}")
            container.stop()
            container.remove()


def test_container_running(docker_client, containers) -> None:
    """
    Checks if the container is running and check if it is in the running containers list

    :param docker_client: docker_client
    :return: None
    """
    running_containers = docker_client.containers.list()
    failed_containers = []
    for container in containers:
        logging.info(f"Verifying that container {container.id} with image {container.image.tags} is running")
        if container not in running_containers:
            logging.info(f"Container {container.id} with image {container.image.tags} is not running")
            failed_containers.append(f"Container with ID {container.id} and image {container.image.tags} is not "
                                     f"running.")
    assert not failed_containers, f"Some containers failed to run: {failed_containers}"
