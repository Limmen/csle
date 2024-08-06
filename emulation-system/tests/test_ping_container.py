import pytest
import docker 
import time
import csle_common.constants.constants as constants
from docker.types import IPAMConfig, IPAMPool

@pytest.fixture(scope="module")
def docker_client() -> None:
    """
    Provide a Docker client instance

    :return: None
    """
    return docker.from_env()

@pytest.fixture(scope="module")
def network(docker_client) -> None:
    """_summary_

    :param docker_client: _description_
    :type docker_client: _type_
    :yield: _description_
    :rtype: _type_
    """
    ipam_pool = IPAMPool(subnet="15.15.15.0/24")
    ipam_config = IPAMConfig(pool_configs=[ipam_pool])
    
    network = docker_client.networks.create(
        "test_network",
        driver="bridge",
        ipam=ipam_config
    )
    print(f"Network '{network.name}' created successfully.")
    """ networks = docker_client.networks.list()
    for net in networks:
        print(net.name) """
    yield network
    network.remove()

@pytest.fixture(scope="module")
def container(docker_client,network) -> None:
    """
    Starts a Docker container before running tests and ensures its stopped and removed after tests complete.

    :param docker_client: docker_client
    
    :return: None
    """
    image_with_tag = f"kimham/{constants.CONTAINER_IMAGES.KAFKA_1}:0.6.0"
    container_ip = "15.15.15.2"
    container = docker_client.containers.create(image_with_tag, command="sh",detach=True)
    network.connect(container, ipv4_address=container_ip)
    container.start()
    container.reload()
    print(f"Container '{container.name}' connected to network with IP {container_ip}")
    print("Available networks:", container.attrs['NetworkSettings']['Networks'].keys())
    inspect_result = container.attrs['NetworkSettings']['Networks']['test_network']['IPAddress']
    print("Assigned IP Address:", inspect_result)
    
    yield container
    container.stop()
    container.remove()
    
def test_check_container_running(docker_client, container) -> None:
    # Check if the container is running
    container_status = container.attrs['State']['Status']
    assert container_status == 'running', f"Container is not running. Status: {container_status}"
    
    # Check if the container has the correct IP
    inspect_result = container.attrs['NetworkSettings']['Networks']['test_network']['IPAddress']
    expected_ip = "15.15.15.2"
    assert inspect_result == expected_ip, f"Container IP address mismatch. Expected: {expected_ip}, Got: {inspect_result}"
    
    print(f"Container with IP {expected_ip} is running and reachable.")
    
def test_ping_container(docker_client, network, container) -> None:
    container_ip = "15.15.15.2"
    time.sleep(10)
    #print("Available networks:", container.attrs['NetworkSettings']['Networks'].keys())
    inspect_result = container.attrs['NetworkSettings']['Networks']['test_network']['IPAddress']
    print("Container IP",inspect_result)
    assert inspect_result == container_ip, f"Container IP address mismatch. Expected: {container_ip}, Got: {inspect_result}"
    
    #start a temp container to ping the test container
    image_with_tag = f"kimham/{constants.CONTAINER_IMAGES.FTP_1}:0.6.0"
    temp_container = docker_client.containers.run(image_with_tag,f"ping -c 3 {container_ip}",
        network="test_network", detach=True)
    temp_container.reload()
    temp_container_networks = temp_container.attrs['NetworkSettings']['Networks']
    print(f"Temporary container connected to networks: {temp_container_networks}")
    temp_container.wait()
    logs = temp_container.logs().decode('utf-8')
    temp_container.remove()
    assert "3 packets transmitted, 3 received" in logs, \
        f"Ping failed. Logs: {logs}"