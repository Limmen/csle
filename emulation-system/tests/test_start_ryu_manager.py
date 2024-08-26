from typing import List, Any
import pytest
import docker
import logging
import grpc
from unittest.mock import MagicMock
from docker.types import IPAMConfig, IPAMPool
import time
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
import csle_common.constants.constants as constants
import csle_collector.ryu_manager.ryu_manager_pb2_grpc
import csle_collector.ryu_manager.ryu_manager_pb2
import csle_collector.ryu_manager.query_ryu_manager
from csle_common.metastore.metastore_facade import MetastoreFacade
from typing import Generator


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

    :return: Generator
    """
    subnet = "15.15.15.0/24"
    ipam_pool = IPAMPool(subnet=subnet)
    ipam_config = IPAMConfig(pool_configs=[ipam_pool])
    logging.info(f"Creating virtual network with subnet: {subnet}")
    network = docker_client.networks.create("test_network", driver="bridge", ipam=ipam_config)
    yield network
    network.remove()


def get_derived_containers(docker_client, excluded_tag=constants.CONTAINER_IMAGES.BLANK) -> List[Any]:
    """
    Get all the containers except the blank ones

    :param docker_client: docker_client

    :return: None
    """
    # Get all images except those with the excluded tag
    config = MetastoreFacade.get_config(id=1)
    match_tag = config.version
    all_images = docker_client.images.list()
    derived_images = [
        image
        for image in all_images
        if any(match_tag in tag for tag in image.tags)
        and all(constants.CONTAINER_IMAGES.BASE not in tag for tag in image.tags)
        and all(excluded_tag not in tag for tag in image.tags)
    ]
    return derived_images


@pytest.fixture(scope="module", params=get_derived_containers(docker.from_env()))
def container_setup(request, docker_client, network) -> Generator:
    """
    Starts a Docker container before running tests and ensures its stopped and removed after tests complete.

    :param request: request
    :param docker_client: docker_client
    :yield: container

    :return: None
    """
    # Create and start each derived container
    image = request.param
    container = docker_client.containers.create(
        image.tags[0],
        command="sh -c 'while true; do sleep 3600; done'",
        detach=True,
    )
    network.connect(container)
    container.start()
    yield container
    logging.info(f"Stopping and removing container: {container.id} with image: {container.image.tags}")
    container.stop()
    container.remove()


def test_start_ryu_manager(container_setup) -> None:
    """
    Start ryu_manager in a container

    :param container_setup: container_setup

    :return: None
    """
    failed_containers = []
    containers_info = []
    container_setup.reload()
    assert container_setup.status == "running"
    # Mock emulation_env_config
    emulation_env_config = MagicMock(spec=EmulationEnvConfig)
    emulation_env_config.get_connection.return_value = MagicMock()
    emulation_env_config.sdn_controller_config = MagicMock()
    emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip = container_setup.attrs[
        constants.DOCKER.NETWORK_SETTINGS
    ][constants.DOCKER.IP_ADDRESS_INFO]
    emulation_env_config.sdn_controller_config.get_connection.return_value = MagicMock()
    emulation_env_config.sdn_controller_config.ryu_manager_port = 50051
    emulation_env_config.sdn_controller_config.ryu_manager_log_dir = "/var/log/ryu"
    emulation_env_config.sdn_controller_config.ryu_manager_log_file = "ryu.log"
    emulation_env_config.sdn_controller_config.ryu_manager_max_workers = 4

    ip = emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip
    port = emulation_env_config.sdn_controller_config.ryu_manager_port
    try:
        # Start ryu_manager command
        cmd = (
            f"/root/miniconda3/bin/python3 /ryu_manager.py "
            f"--port {emulation_env_config.sdn_controller_config.ryu_manager_port} "
            f"--logdir {emulation_env_config.sdn_controller_config.ryu_manager_log_dir} "
            f"--logfile {emulation_env_config.sdn_controller_config.ryu_manager_log_file} "
            f"--maxworkers {emulation_env_config.sdn_controller_config.ryu_manager_max_workers}"
        )
        # Run cmd in the container
        logging.info(
            f"Starting ryu manager in container: {container_setup.id} " f"with image: {container_setup.image.tags}"
        )
        container_setup.exec_run(cmd, detach=True)
        # Check if ryu_manager starts
        cmd = (
            f"sh -c '{constants.COMMANDS.PS_AUX} | {constants.COMMANDS.GREP} "
            f"{constants.COMMANDS.SPACE_DELIM}{constants.TRAFFIC_COMMANDS.RYU_MANAGER_FILE_NAME}'"
        )
        logging.info(
            f"Verifying that ryu manager is running in container: {container_setup.id} "
            f"with image: {container_setup.image.tags}"
        )
        result = container_setup.exec_run(cmd)
        output = result.output.decode("utf-8")
        assert constants.COMMANDS.SEARCH_RYU_MANAGER in output, "ryu manager is not running in the container"
        time.sleep(5)
        # Call grpc
        with grpc.insecure_channel(f"{ip}:{port}", options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.ryu_manager.ryu_manager_pb2_grpc.RyuManagerStub(channel)
            ryu_dto = csle_collector.ryu_manager.query_ryu_manager.get_ryu_status(stub)
        assert ryu_dto
    except Exception as e:
        print(f"Error occurred in container {container_setup.name}: {e}")
        failed_containers.append(container_setup.name)
        containers_info.append(
            {
                "container_status": container_setup.status,
                "container_image": container_setup.image.tags,
                "name": container_setup.name,
                "error": str(e),
            }
        )
    if failed_containers:
        logging.info("Containers that failed to start the ryu manager:")
        logging.info(containers_info)
    assert not failed_containers, f"T{failed_containers} failed"
