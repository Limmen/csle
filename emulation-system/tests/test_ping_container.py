import pytest
import docker
from docker.types import IPAMConfig, IPAMPool


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
def container1(docker_client, network) -> None:
    """
    Create and start the first container with a specific IP

    :param docker_client: docker_client
    :param network: network
    :yield: container
    
    :return: None
    """
    # Create and start the first container with a specific IP
    container = docker_client.containers.create(
        "kimham/csle_spark_1:0.6.0",
        command="sh -c 'while true; do sleep 3600; done'",
        name="test_container1",
        detach=True
    )
    network.connect(container, ipv4_address="15.15.15.15")
    container.start()
    yield container
    container.stop()
    container.remove()


@pytest.fixture(scope="module")
def container2(docker_client, network):
    """
    Create and start the second container with a specific IP

    :param docker_client: docker_client
    :param network: network
    :yield: container
    
    :return: None
    """
    # Create and start the second container with a specific IP
    container = docker_client.containers.create(
        "kimham/csle_elk_1:0.6.0",
        command="sh -c 'while true; do sleep 3600; done'",
        name="test_container2",
        detach=True
    )
    network.connect(container, ipv4_address="15.15.15.14")
    container.start()
    yield container
    container.stop()
    container.remove()


def test_ping_containers(container1, container2) -> None:
    """
    Ping container1 from container2

    :return: None
    """
    container1.start()
    container2.start()
    container1.reload()
    container2.reload()
    # Check if containers are running
    assert container1.status == 'running', "Container1 is not running"
    assert container2.status == 'running', "Container2 is not running"
    # Ping container2 from container1
    exec_result = container2.exec_run("ping -c 3 15.15.15.15")
    output = exec_result.output.decode('utf-8')
    # Check if the ping was successful
    assert "3 packets transmitted, 3 received" in output, f"Ping failed. Logs: {output}"
