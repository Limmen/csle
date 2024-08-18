from typing import Generator
import pytest
import docker
import logging
from docker.types import IPAMConfig, IPAMPool
import csle_common.constants.constants as constants
from csle_common.metastore.metastore_facade import MetastoreFacade


@pytest.fixture(scope="module")
def docker_client() -> None:
    """
    Initialize and Provide a Docker client instance for the test

    :return: None
    """
    return docker.from_env()


@pytest.fixture(scope="module")
def network(docker_client) -> Generator:
    """
    Create a custom network with a specific subnet

    :param docker_client: docker_client
    :yield: network
    :return: None
    """
    subnet = "15.15.15.0/24"
    ipam_pool = IPAMPool(subnet=subnet)
    ipam_config = IPAMConfig(pool_configs=[ipam_pool])
    logging.info(f"Creating virtual network with subnet: {subnet}")
    network = docker_client.networks.create("test_network", driver="bridge", ipam=ipam_config)
    yield network
    network.remove()


@pytest.fixture(scope="module")
def blank1(docker_client, network) -> Generator:
    """
    Create and start the first container with a specific IP

    :param docker_client: docker_client
    :param network: network
    :yield: container
    :return: None
    """
    ip = "15.15.15.10"
    config = MetastoreFacade.get_config(id=1)
    version = config.version
    container = docker_client.containers.create(
        f"{constants.CONTAINER_IMAGES.DOCKERHUB_USERNAME}/{constants.CONTAINER_IMAGES.BLANK_1}:{version}",
        command="sh -c 'apt-get update && apt-get install -y iputils-ping && while true; do sleep 3600; done'",
        detach=True)
    logging.info(f"Attaching {ip} to container: {container.id} with image: {container.image.tags}")
    network.connect(container, ipv4_address=ip)
    logging.info(f"Starting container: {container.id} with image: {container.image.tags}")
    container.start()
    yield container
    logging.info(f"Stopping and removing container: {container.id} with image: {container.image.tags}")
    container.stop()
    container.remove()


@pytest.fixture(scope="module")
def other_containers(docker_client, network) -> Generator:
    """
    Create and start the second container with a specific IP

    :param docker_client: docker_client
    :param network: network
    :yield: container
    :return: None
    """
    config = MetastoreFacade.get_config(id=1)
    match_tag = config.version
    all_images = docker_client.images.list()
    images = [
        image
        for image in all_images
        if (any(match_tag in tag for tag in image.tags)
            and all(constants.CONTAINER_IMAGES.BASE not in tag for tag in image.tags)
            and all(constants.CONTAINER_IMAGES.BLANK not in tag for tag in image.tags))]
    containers = []
    start_ip = 11
    for image in images:
        ip = f"15.15.15.{start_ip}"
        container = docker_client.containers.create(
            image.tags[0],
            command="sh -c 'apt-get update && apt-get install -y iputils-ping && while true; do sleep 3600; done'",
            detach=True,
        )
        logging.info(f"Attaching {ip} to container: {container.id} with image: {container.image.tags}")
        network.connect(container, ipv4_address=ip)
        logging.info(f"Starting container: {container.id} with image: {container.image.tags}")
        container.start()
        containers.append((container, f"15.15.15.{start_ip}"))
        start_ip += 1
    yield containers
    for container, _ in containers:
        logging.info(f"Stopping and removing container: {container.id} with image: {container.image.tags}")
        container.stop()
        container.remove()


def test_ping_containers(blank1, other_containers) -> None:
    """
    Ping container1 from container2

    :return: None
    """
    failed_tests = []
    blank1.start()
    blank1.reload()
    # Check if containers are running
    assert blank1.status == "running", "Container1 is not running"
    # Ping container2 from blank1
    for container, ip in other_containers:
        logging.info(f"Starting container: {container.id} with image: {container.image.tags}")
        container.start()
        container.reload()
        assert container.status == "running", "Container2 is not running"
        try:
            logging.info(f"Pinging ip: {ip} from container {blank1.id} with image: {blank1.image.tags}")
            exec_result = blank1.exec_run(f"ping -c 3 {ip}")
            output = exec_result.output.decode("utf-8")
            # Check if the ping was successful
            assert "3 packets transmitted, 3 received" in output, f"Ping failed. Logs: {output}"
            if "3 packets transmitted, 3 received" not in output:
                failed_tests.append(f"Ping to {container.image.tags} from blank1 failed. Logs: {output}")
        except Exception as e:
            logging.info(f"Failed to ping ip: {ip} from container {blank1.id} with image: {blank1.image.tags}")
            failed_tests.append(
                f"Ping to {container.image.tags} from blank1 failed. Container: {container.image.tags}, "
                f"IP: {ip}, Error: {str(e)}")
    if failed_tests:
        for fail in failed_tests:
            logging.info(fail)
        assert False, "Some ping tests failed, see the output above for details."
