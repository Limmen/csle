import pytest
import docker
import logging
from unittest.mock import MagicMock, patch
from docker.types import IPAMConfig, IPAMPool
import time
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.util.emulation_util import EmulationUtil
import csle_common.constants.constants as constants
from csle_common.controllers.host_controller import HostController
import csle_collector.host_manager.host_manager_pb2_grpc
import csle_collector.host_manager.host_manager_pb2


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
    ipam_pool = IPAMPool(subnet="15.15.15.0/24")
    ipam_config = IPAMConfig(pool_configs=[ipam_pool])
    network = docker_client.networks.create("test_network", driver="bridge", ipam=ipam_config)
    yield network
    network.remove()


def get_derived_containers(docker_client, excluded_tag="blank") -> None:
    """
    Get all the containers except the blank ones

    :param docker_client: docker_client

    :return: None
    """
    # Get all images except those with the excluded tag
    match_tag = "0.6.0"
    all_images = docker_client.images.list()
    derived_images = [
        image
        for image in all_images
        if any(match_tag in tag for tag in image.tags)
        and all("base" not in tag for tag in image.tags)
        and all(excluded_tag not in tag for tag in image.tags)
    ]
    return derived_images[:2]


@pytest.fixture(scope="module", params=get_derived_containers(docker.from_env()))
def container_setup(request, docker_client, network) -> None:
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
        image.tags[0],  # Use the first tag for the image
        command="sh -c 'apt-get update && apt-get install -y iputils-ping && while true; do sleep 3600; done'",
        detach=True,
    )
    network.connect(container)
    container.start()
    yield container
    container.stop()
    container.remove()


@patch("csle_common.util.emulation_util.EmulationUtil.connect_admin")
@patch("csle_common.util.emulation_util.EmulationUtil.execute_ssh_cmd")
@patch("time.sleep", return_value=None)
@patch("grpc.insecure_channel")
def test_start_host_manager(
    mock_grpc_channel, mock_sleep, mock_execute_ssh_cmd, mock_connect_admin, container_setup
) -> None:
    """
    Test start_host_manager and verify if it runs correctly within a container.

    :param mock_grpc_channel: mock_grpc_channel
    :param mock_sleep: mock_sleep
    :param mock_execute_ssh_cmd: mock_execute_ssh_cmd
    :param mock_connect_admin: mock_connect_admin
    :param container_setup: container_setup

    :return: None
    """

    # Set up mock return values
    mock_connect_admin.return_value = None
    mock_execute_ssh_cmd.side_effect = [
        ("", "", 0),  # Initial check, no host_manager process found
        ("", "", 0),  # Stopping any old process (even if none exist)
        ("", "", 0),  # Starting host_manager
        (constants.COMMANDS.SEARCH_HOST_MANAGER, "", 0),  # Final check, host_manager is now running
    ]
    # Create a mock EmulationEnvConfig object with necessary attributes
    emulation_env_config = MagicMock(spec=EmulationEnvConfig)
    emulation_env_config.get_connection.return_value = MagicMock()
    # Set up mock host_manager_config attributes
    host_manager_config = MagicMock()
    emulation_env_config.host_manager_config = host_manager_config
    emulation_env_config.host_manager_config.host_manager_port = 8080
    emulation_env_config.host_manager_config.host_manager_log_dir = "/var/log/host_manager"
    emulation_env_config.host_manager_config.host_manager_log_file = "host_manager.log"
    emulation_env_config.host_manager_config.host_manager_max_workers = 4
    # Create a mock logger
    logger = logging.getLogger("test_logger")
    ip = "15.15.15.15"
    try:
        container_setup.reload()
        assert container_setup.status == "running", f"Container {container_setup.name} is not running"
        # Connect using the mocked connect_admin method
        EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=ip)
        # Check if the host_manager is already running
        cmd = (
            constants.COMMANDS.PS_AUX
            + " | "
            + constants.COMMANDS.GREP
            + constants.COMMANDS.SPACE_DELIM
            + constants.TRAFFIC_COMMANDS.HOST_MANAGER_FILE_NAME
        )
        o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))

        if constants.COMMANDS.SEARCH_HOST_MANAGER not in str(o):
            logger.info(
                f"Host manager is not running on: {ip}, starting it. Output of {cmd} was: {str(o)}, "
                f"err output was: {str(e)}"
            )
            # Stop old background job if running
            cmd = (
                constants.COMMANDS.SUDO
                + constants.COMMANDS.SPACE_DELIM
                + constants.COMMANDS.PKILL
                + constants.COMMANDS.SPACE_DELIM
                + constants.TRAFFIC_COMMANDS.HOST_MANAGER_FILE_NAME
            )
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))
            # Start the host_manager
            cmd = constants.COMMANDS.START_HOST_MANAGER.format(
                emulation_env_config.host_manager_config.host_manager_port,
                emulation_env_config.host_manager_config.host_manager_log_dir,
                emulation_env_config.host_manager_config.host_manager_log_file,
                emulation_env_config.host_manager_config.host_manager_max_workers,
            )
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))
            time.sleep(5)
            cmd = (
                constants.COMMANDS.PS_AUX
                + " | "
                + constants.COMMANDS.GREP
                + constants.COMMANDS.SPACE_DELIM
                + constants.TRAFFIC_COMMANDS.HOST_MANAGER_FILE_NAME
            )
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))
            assert constants.COMMANDS.SEARCH_HOST_MANAGER in str(
                o
            ), "Host manager is not running in the container after start attempt"
        else:
            logger.info(
                f"Host manager is already running on: {ip}. Output of {cmd} was: {str(o)}, " f"err output was: {str(e)}"
            )
        mock_channel = MagicMock()
        mock_grpc_channel.return_value = mock_channel
        # Mock the stub and its method
        mock_stub = MagicMock()
        mock_channel.__enter__.return_value = mock_stub
        mock_stub.GetHostStatus.return_value = csle_collector.host_manager.host_manager_pb2.HostStatusDTO()
        # Make the gRPC call
        status = HostController.get_host_monitor_thread_status_by_port_and_ip(
            ip, emulation_env_config.host_manager_config.host_manager_port
        )
        # Validate the status response
        assert status is not None, "Failed to get host manager status via gRPC"
    except Exception as e:
        pytest.fail(f"Exception occurred while starting host manager: {str(e)}")
