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
import csle_collector.snort_ids_manager.snort_ids_manager_pb2_grpc
import csle_collector.snort_ids_manager.snort_ids_manager_pb2
import csle_collector.snort_ids_manager.query_snort_ids_manager
import csle_collector.snort_ids_manager.snort_ids_manager_util
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


def get_containers(docker_client) -> List[Any]:
    """
    Get the containers

    :param docker_client: docker_client

    :return: None
    """
    all_images = constants.CONTAINER_IMAGES.SNORT_IDS_IMAGES
    return all_images


@pytest.fixture(scope="module", params=get_containers(docker.from_env()))
def container_setup(request, docker_client, network) -> Generator:
    """
    Starts a Docker container before running tests and ensures its stopped and removed after tests complete.

    :param request: request
    :param docker_client: docker_client
    :yield: container

    :return: None
    """
    # Create and start each derived container
    config = MetastoreFacade.get_config(id=1)
    version = config.version
    image = request.param
    container = docker_client.containers.create(
        f"{constants.CONTAINER_IMAGES.DOCKERHUB_USERNAME}/{image}:{version}",
        command="sh -c 'while true; do sleep 3600; done'",
        detach=True,
    )
    network.connect(container)
    container.start()
    yield container
    logging.info(f"Stopping and removing container: {container.id} with image: {container.image.tags}")
    container.stop()
    container.remove()


def test_start_snort_manager(container_setup) -> None:
    """
    Start snort_manager in a container

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
    emulation_env_config.snort_ids_manager_config = MagicMock()
    emulation_env_config.snort_ids_manager_config.snort_ids_manager_port = 50051
    emulation_env_config.snort_ids_manager_config.snort_ids_manager_log_dir = "/var/log/snort"
    emulation_env_config.snort_ids_manager_config.snort_ids_manager_log_file = "snort.log"
    emulation_env_config.snort_ids_manager_config.snort_ids_manager_max_workers = 4

    ip = container_setup.attrs[constants.DOCKER.NETWORK_SETTINGS][constants.DOCKER.IP_ADDRESS_INFO]
    port = emulation_env_config.snort_ids_manager_config.snort_ids_manager_port
    try:
        # Start host_manager command
        cmd = (
            f"/root/miniconda3/bin/python3 /snort_ids_manager.py "
            f"--port {emulation_env_config.snort_ids_manager_config.snort_ids_manager_port} "
            f"--logdir {emulation_env_config.snort_ids_manager_config.snort_ids_manager_log_dir} "
            f"--logfile {emulation_env_config.snort_ids_manager_config.snort_ids_manager_log_file} "
            f"--maxworkers {emulation_env_config.snort_ids_manager_config.snort_ids_manager_max_workers}"
        )
        # Run cmd in the container
        logging.info(f"Starting snort manager in container: {container_setup.id} "
                     f"with image: {container_setup.image.tags}")
        container_setup.exec_run(cmd, detach=True)
        # Check if snort_manager starts
        cmd = (
            f"sh -c '{constants.COMMANDS.PS_AUX} | {constants.COMMANDS.GREP} "
            f"{constants.COMMANDS.SPACE_DELIM}{constants.TRAFFIC_COMMANDS.SNORT_IDS_MANAGER_FILE_NAME}'"
        )
        logging.info(f"Verifying that snort manager is running in container: {container_setup.id} "
                     f"with image: {container_setup.image.tags}")
        result = container_setup.exec_run(cmd)
        output = result.output.decode("utf-8")
        assert constants.COMMANDS.SEARCH_SNORT_IDS_MANAGER in output, "Snort manager is not running in the container"
        time.sleep(5)
        # Call grpc
        with grpc.insecure_channel(f"{ip}:{port}", options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.snort_ids_manager.snort_ids_manager_pb2_grpc.SnortIdsManagerStub(channel)
            status = csle_collector.snort_ids_manager.query_snort_ids_manager.get_snort_ids_monitor_status(stub=stub)
        assert status
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
        logging.info("Containers that failed to start the snort manager:")
        logging.info(containers_info)
    assert not failed_containers, f"T{failed_containers} failed"
    
    
def test_start_snort_ids(container_setup) -> None:
    """
    Start snort_ids in a container

    :param container_setup: container_setup

    :return: None
    """
    emulation_env_config = MagicMock()
    emulation_env_config.snort_ids_manager_config = MagicMock()
    emulation_env_config.snort_ids_manager_config.snort_ids_manager_port = 50051
    emulation_env_config.execution_id = "1"
    emulation_env_config.level = "2"
    logger = logging.getLogger("test_logger")
    ip = container_setup.attrs[constants.DOCKER.NETWORK_SETTINGS][constants.DOCKER.IP_ADDRESS_INFO]
    port = emulation_env_config.snort_ids_manager_config.snort_ids_manager_port
    # Set up parameters
    subnetmask = f"{emulation_env_config.execution_id}.{emulation_env_config.level}" \
                 f"{constants.CSLE.CSLE_LEVEL_SUBNETMASK_SUFFIX}"
    ingress_interface = constants.NETWORKING.ETH2
    egress_interface = constants.NETWORKING.ETH0
    logger.debug(f"Attempting to connect to gRPC server at {ip}:{port}")
    # gRPC call
    try:
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.snort_ids_manager.snort_ids_manager_pb2_grpc.SnortIdsManagerStub(channel)
            response = csle_collector.snort_ids_manager.query_snort_ids_manager.start_snort_ids(
                stub=stub, ingress_interface=ingress_interface, egress_interface=egress_interface,
                subnetmask=subnetmask
            )
            logger.info(f"gRPC Response: {response}")
            assert response, f"Failed to start Snort IDS on {ip}. Response: {response}"
    except grpc.RpcError as e:
        logger.error(f"gRPC Error: {e}")
        assert False, f"gRPC call failed with error: {e}"
        

def test_stop_snort_ids(container_setup) -> None:
    """
    Stop snort_ids in a container

    :param container_setup: container_setup

    :return: None
    """
    emulation_env_config = MagicMock()
    emulation_env_config.snort_ids_manager_config = MagicMock()
    emulation_env_config.snort_ids_manager_config.snort_ids_manager_port = 50051
    emulation_env_config.execution_id = "1"
    emulation_env_config.level = "2"
    logger = logging.getLogger("test_logger")
    ip = container_setup.attrs[constants.DOCKER.NETWORK_SETTINGS][constants.DOCKER.IP_ADDRESS_INFO]
    port = emulation_env_config.snort_ids_manager_config.snort_ids_manager_port
    logger.debug(f"Attempting to connect to gRPC server at {ip}:{port}")
    # gRPC call
    try:
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.snort_ids_manager.snort_ids_manager_pb2_grpc.SnortIdsManagerStub(channel)
            response = csle_collector.snort_ids_manager.query_snort_ids_manager.stop_snort_ids(
                stub=stub
            )
            logger.info(f"gRPC Response: {response}")
            assert response, f"Failed to stop IDS on {ip}. Response: {response}"
    except grpc.RpcError as e:
        logger.error(f"gRPC Error: {e}")
        assert False, f"gRPC call failed with error: {e}"
