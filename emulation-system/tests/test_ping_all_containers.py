import pytest
import docker
from docker.types import IPAMConfig, IPAMPool
import csle_common.constants.constants as constants


@pytest.fixture(scope="module")
def docker_client() -> None:
    """
    Initialize and Provide a Docker client instance for the test

    :return: None
    """
    return docker.from_env()


@pytest.fixture(scope="module")
def network(docker_client) -> None:
    """
    Create a custom network with a specific subnet

    :param docker_client: docker_client
    :yield: network

    :return: None
    """
    # Create a custom network
    ipam_pool = IPAMPool(subnet="15.15.15.0/24")
    ipam_config = IPAMConfig(pool_configs=[ipam_pool])
    network = docker_client.networks.create("test_network", driver="bridge", ipam=ipam_config)
    yield network
    network.remove()


@pytest.fixture(scope="module")
def blank1(docker_client, network) -> None:
    """
    Create and start the first container with a specific IP

    :param docker_client: docker_client
    :param network: network
    :yield: container

    :return: None
    """
    # Create and start the first container with a specific IP
    container = docker_client.containers.create(
        f"{constants.CONTAINER_IMAGES.DOCKERHUB_USERNAME}/{constants.CONTAINER_IMAGES.BLANK_1}:0.6.0",
        command="sh -c 'apt-get update && apt-get install -y iputils-ping && while true; do sleep 3600; done'",
        detach=True)
    network.connect(container, ipv4_address="15.15.15.10")
    container.start()
    yield container
    container.stop()
    container.remove()


@pytest.fixture(scope="module")
def other_containers(docker_client, network) -> None:
    """
    Create and start the second container with a specific IP

    :param docker_client: docker_client
    :param network: network
    :yield: container

    :return: None
    """
    # Create and start the second container with a specific IP
    match_tag = "0.6.0"
    all_images = docker_client.images.list()
    images = [
        image
        for image in all_images
        if any(match_tag in tag for tag in image.tags)
           and all(constants.CONTAINER_IMAGES.BASE not in tag for tag in image.tags)
           and all(f"{constants.CONTAINER_IMAGES.DOCKERHUB_USERNAME}/{constants.CONTAINER_IMAGES.BLANK_UBUNTU_22}:0.6.0"
                   not in tag for tag in image.tags)
    ]
    containers = []
    start_ip = 11
    for image in images:
        container = docker_client.containers.create(
            image.tags[0],
            command="sh -c 'apt-get update && apt-get install -y iputils-ping && while true; do sleep 3600; done'",
            detach=True,
        )
        network.connect(container, ipv4_address=f"15.15.15.{start_ip}")
        container.start()
        containers.append((container, f"15.15.15.{start_ip}"))
        start_ip += 1
    yield containers
    for container, _ in containers:
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
        container.start()
        container.reload()
        assert container.status == "running", "Container2 is not running"
        try:
            exec_result = blank1.exec_run(f"ping -c 3 {ip}")
            output = exec_result.output.decode("utf-8")
            # Check if the ping was successful
            assert "3 packets transmitted, 3 received" in output, f"Ping failed. Logs: {output}"
            if "3 packets transmitted, 3 received" not in output:
                failed_tests.append(f"Ping to {container.image.tags} from blank1 failed. Logs: {output}")
        except Exception as e:
            failed_tests.append(
                f"Ping to {container.image.tags} from blank1 failed. Container: {container.image.tags}, "
                f"IP: {ip}, Error: {str(e)}")
    if failed_tests:
        for fail in failed_tests:
            print(fail)
        assert False, "Some ping tests failed, see the output above for details."
