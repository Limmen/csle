import pytest
import docker
import logging
import grpc
from docker.types import IPAMConfig, IPAMPool
import time
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
import csle_common.constants.constants as constants
import csle_collector.constants.constants as collector_constants
import csle_collector.kafka_manager.kafka_manager_pb2_grpc
import csle_collector.kafka_manager.kafka_manager_pb2
import csle_collector.kafka_manager.query_kafka_server
from csle_common.metastore.metastore_facade import MetastoreFacade
from typing import Generator
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.dao.emulation_config.kafka_config import KafkaConfig
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.dao.emulation_config.node_resources_config import NodeResourcesConfig
from csle_common.dao.emulation_config.node_firewall_config import NodeFirewallConfig
from csle_common.dao.emulation_config.kafka_topic import KafkaTopic


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


@pytest.fixture(scope="module")
def container_setup(docker_client, network) -> Generator:
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
    image = constants.CONTAINER_IMAGES.KAFKA_1
    logging.info(f"image:{image}")
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


def test_start_kafka_manager(container_setup) -> None:
    """
    Start kafka_manager in a container
    
    :param container_setup: container_setup
    :return: None
    """
    failed_containers = []
    containers_info = []
    container_setup.reload()
    assert container_setup.status == "running"

    container_network = ContainerNetwork(
        name="test_network",
        subnet_mask="255.255.255.0",
        bitmask="24",
        subnet_prefix="15.15.15.0/24",
        interface="eth0"
    )

    # Initialize NodeContainerConfig with necessary arguments
    ips_and_networks = [
        (container_setup.attrs['NetworkSettings']['IPAddress'], container_network)
    ]

    container_config = NodeContainerConfig(
        name="kafka_container",
        ips_and_networks=ips_and_networks,
        version="latest",
        level="production",
        restart_policy="always",
        suffix="kafka",
        os="linux",
        docker_gw_bridge_ip=container_setup.attrs[constants.DOCKER.NETWORK_SETTINGS][constants.DOCKER.IP_ADDRESS_INFO],
        physical_host_ip="192.168.1.1"
    )

    # Initialize NodeResourcesConfig
    resources_config = NodeResourcesConfig(
        container_name="kafka_container",
        num_cpus=2,
        available_memory_gb=4,
        ips_and_network_configs=ips_and_networks,
        docker_gw_bridge_ip=container_setup.attrs[constants.DOCKER.NETWORK_SETTINGS][constants.DOCKER.IP_ADDRESS_INFO],
        physical_host_ip="192.168.1.1"
    )

    firewall_config = NodeFirewallConfig(
        ips_gw_default_policy_networks=[],
        hostname="kafka_container",
        output_accept=None,
        input_accept=None,
        forward_accept=None,
        output_drop=None,
        input_drop=None,
        forward_drop=None,
        routes=None,
        docker_gw_bridge_ip=None,
        physical_host_ip=None
    )

    kafka_topic_1 = KafkaTopic(
        name="test-topic-1",
        num_partitions=3,
        num_replicas=1,
        attributes=["column1", "column2", "column3"],
        retention_time_hours=72
    )

    kafka_topic_2 = KafkaTopic(
        name="test-topic-2",
        num_partitions=2,
        num_replicas=1,
        attributes=["column1", "column2"],
        retention_time_hours=48
    )

    topics = [kafka_topic_1, kafka_topic_2]

    kafka_config = KafkaConfig(
        container=container_config,
        resources=resources_config,
        firewall_config=firewall_config,
        topics=topics,
        kafka_manager_log_file='kafka_manager.log',
        kafka_manager_log_dir='/var/log/kafka_manager',
        kafka_manager_max_workers=4,
        kafka_port=9092,
        kafka_port_external=9292,
        time_step_len_seconds=15,
        kafka_manager_port=50051,
        version="0.0.1"
    )

    emulation_env_config = EmulationEnvConfig(
        name="test_env",
        containers_config=None,
        users_config=None,
        flags_config=None,
        vuln_config=None,
        topology_config=None,
        traffic_config=None,
        resources_config=None,
        kafka_config=kafka_config,
        services_config=None,
        descr="Test environment description",
        static_attacker_sequences=None,
        ovs_config=None,
        sdn_controller_config=None,
        host_manager_config=None,
        snort_ids_manager_config=None,
        ossec_ids_manager_config=None,
        docker_stats_manager_config=None,
        elk_config=None,
        beats_config=None,
        level=1,
        version="1.0",
        execution_id=12345,
        csle_collector_version=collector_constants.LATEST_VERSION,
        csle_ryu_version=collector_constants.LATEST_VERSION
    )

    ip = emulation_env_config.kafka_config.container.docker_gw_bridge_ip
    port = emulation_env_config.kafka_config.kafka_manager_port

    try:
        cmd = (
            f"/root/miniconda3/bin/python3 /kafka_manager.py "
            f"--port {emulation_env_config.kafka_config.kafka_manager_port} "
            f"--logdir {emulation_env_config.kafka_config.kafka_manager_log_dir} "
            f"--logfile {emulation_env_config.kafka_config.kafka_manager_log_file} "
            f"--maxworkers {emulation_env_config.kafka_config.kafka_manager_max_workers}"
        )
        logging.info(
            f"Starting kafka manager in container: {container_setup.id} "
            f"with image: {container_setup.image.tags}"
        )
        container_setup.exec_run(cmd, detach=True)

        cmd = (
            f"sh -c '{constants.COMMANDS.PS_AUX} | {constants.COMMANDS.GREP} "
            f"{constants.COMMANDS.SPACE_DELIM}{constants.TRAFFIC_COMMANDS.KAFKA_MANAGER_FILE_NAME}'"
        )
        logging.info(
            f"Verifying that kafka manager is running in container: {container_setup.id} "
            f"with image: {container_setup.image.tags}"
        )
        result = container_setup.exec_run(cmd)
        output = result.output.decode("utf-8")
        assert constants.COMMANDS.SEARCH_KAFKA_MANAGER in output, "Kafka manager is not running in the container"
        time.sleep(5)

        with grpc.insecure_channel(f"{ip}:{port}", options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.kafka_manager.kafka_manager_pb2_grpc.KafkaManagerStub(channel)
            kafka_dto = csle_collector.kafka_manager.query_kafka_server.get_kafka_status(stub)
        assert kafka_dto
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
        logging.info("Containers that failed to start the kafka manager:")
        logging.info(containers_info)
    assert not failed_containers, f"T{failed_containers} failed"
    
    
def test_start_kafka_server(container_setup) -> None:
    """
    Start kafka server in a container
    
    :param container_setup: container_setup
    :return: None
    """
    container_setup.reload()
    assert container_setup.status == "running"

    container_network = ContainerNetwork(
        name="test_network",
        subnet_mask="255.255.255.0",
        bitmask="24",
        subnet_prefix="15.15.15.0/24",
        interface="eth0"
    )

    # Initialize NodeContainerConfig with necessary arguments
    ips_and_networks = [
        (container_setup.attrs['NetworkSettings']['IPAddress'], container_network)
    ]

    container_config = NodeContainerConfig(
        name="kafka_container",
        ips_and_networks=ips_and_networks,
        version="latest",
        level="production",
        restart_policy="always",
        suffix="kafka",
        os="linux",
        docker_gw_bridge_ip=container_setup.attrs[constants.DOCKER.NETWORK_SETTINGS][constants.DOCKER.IP_ADDRESS_INFO],
        physical_host_ip="192.168.1.1"
    )

    # Initialize NodeResourcesConfig
    resources_config = NodeResourcesConfig(
        container_name="kafka_container",
        num_cpus=2,
        available_memory_gb=4,
        ips_and_network_configs=ips_and_networks,
        docker_gw_bridge_ip=container_setup.attrs[constants.DOCKER.NETWORK_SETTINGS][constants.DOCKER.IP_ADDRESS_INFO],
        physical_host_ip="192.168.1.1"
    )

    firewall_config = NodeFirewallConfig(
        ips_gw_default_policy_networks=[],
        hostname="kafka_container",
        output_accept=None,
        input_accept=None,
        forward_accept=None,
        output_drop=None,
        input_drop=None,
        forward_drop=None,
        routes=None,
        docker_gw_bridge_ip=None,
        physical_host_ip=None
    )

    kafka_topic_1 = KafkaTopic(
        name="test-topic-1",
        num_partitions=3,
        num_replicas=1,
        attributes=["column1", "column2", "column3"],
        retention_time_hours=72
    )

    kafka_topic_2 = KafkaTopic(
        name="test-topic-2",
        num_partitions=2,
        num_replicas=1,
        attributes=["column1", "column2"],
        retention_time_hours=48
    )

    topics = [kafka_topic_1, kafka_topic_2]

    kafka_config = KafkaConfig(
        container=container_config,
        resources=resources_config,
        firewall_config=firewall_config,
        topics=topics,
        kafka_manager_log_file='kafka_manager.log',
        kafka_manager_log_dir='/var/log/kafka_manager',
        kafka_manager_max_workers=4,
        kafka_port=9092,
        kafka_port_external=9292,
        time_step_len_seconds=15,
        kafka_manager_port=50051,
        version="0.0.1"
    )

    emulation_env_config = EmulationEnvConfig(
        name="test_env",
        containers_config=None,
        users_config=None,
        flags_config=None,
        vuln_config=None,
        topology_config=None,
        traffic_config=None,
        resources_config=None,
        kafka_config=kafka_config,
        services_config=None,
        descr="Test environment description",
        static_attacker_sequences=None,
        ovs_config=None,
        sdn_controller_config=None,
        host_manager_config=None,
        snort_ids_manager_config=None,
        ossec_ids_manager_config=None,
        docker_stats_manager_config=None,
        elk_config=None,
        beats_config=None,
        level=1,
        version="1.0",
        execution_id=12345,
        csle_collector_version=collector_constants.LATEST_VERSION,
        csle_ryu_version=collector_constants.LATEST_VERSION
    )

    ip = emulation_env_config.kafka_config.container.docker_gw_bridge_ip
    port = emulation_env_config.kafka_config.kafka_manager_port
    logger = logging.getLogger("test_logger")
    try:
        
        internal_ip = emulation_env_config.kafka_config.container.get_ips()[0]
        kafka_config_file = collector_constants.KAFKA.KAFKA_CONFIG_FILE

        internal_ip_cmd = (
            f"sed -i 's/{collector_constants.KAFKA.INTERNAL_IP_PLACEHOLDER}/"
            f"{internal_ip}/g' {kafka_config_file}"
        )
        result_internal_ip = container_setup.exec_run(internal_ip_cmd)
        if result_internal_ip.exit_code != 0:
            raise Exception(f"Failed to configure INTERNAL_IP: {result_internal_ip.output.decode('utf-8')}")

        # Replace EXTERNAL_IP
        external_ip_cmd = (
            f"sed -i 's/{collector_constants.KAFKA.EXTERNAL_IP_PLACEHOLDER}/"
            f"{ip}/g' {kafka_config_file}"
        )
        result_external_ip = container_setup.exec_run(external_ip_cmd)
        if result_external_ip.exit_code != 0:
            raise Exception(f"Failed to configure EXTERNAL_IP: {result_external_ip.output.decode('utf-8')}")

    except Exception as e:
        logger.error(f"Error configuring broker IPs: {e}")
        assert False, f"Failed to configure broker IPs: {e}"

    try:
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.kafka_manager.kafka_manager_pb2_grpc.KafkaManagerStub(channel)
            kafka_dto = csle_collector.kafka_manager.query_kafka_server.start_kafka(stub)
            logging.info(f"kafka_dto:{kafka_dto}")
            assert kafka_dto.running, f"Failed to start kafka on {ip}."
            logger.info(f"kafka has been successfully started on {ip}.")
    except grpc.RpcError as e:
        logger.error(f"gRPC Error: {e}")
        assert False, f"gRPC call failed with error: {e}"
   
        
def test_create_topics(container_setup) -> None:
    """
    Create topics in a container
    
    :param container_setup: container_setup
    :return: None
    """
    container_setup.reload()
    assert container_setup.status == "running"

    container_network = ContainerNetwork(
        name="test_network",
        subnet_mask="255.255.255.0",
        bitmask="24",
        subnet_prefix="15.15.15.0/24",
        interface="eth0"
    )

    # Initialize NodeContainerConfig with necessary arguments
    ips_and_networks = [
        (container_setup.attrs['NetworkSettings']['IPAddress'], container_network)
    ]

    container_config = NodeContainerConfig(
        name="kafka_container",
        ips_and_networks=ips_and_networks,
        version="latest",
        level="production",
        restart_policy="always",
        suffix="kafka",
        os="linux",
        docker_gw_bridge_ip=container_setup.attrs[constants.DOCKER.NETWORK_SETTINGS][constants.DOCKER.IP_ADDRESS_INFO],
        physical_host_ip="192.168.1.1"
    )

    # Initialize NodeResourcesConfig
    resources_config = NodeResourcesConfig(
        container_name="kafka_container",
        num_cpus=2,
        available_memory_gb=4,
        ips_and_network_configs=ips_and_networks,
        docker_gw_bridge_ip=container_setup.attrs[constants.DOCKER.NETWORK_SETTINGS][constants.DOCKER.IP_ADDRESS_INFO],
        physical_host_ip="192.168.1.1"
    )

    firewall_config = NodeFirewallConfig(
        ips_gw_default_policy_networks=[],
        hostname="kafka_container",
        output_accept=None,
        input_accept=None,
        forward_accept=None,
        output_drop=None,
        input_drop=None,
        forward_drop=None,
        routes=None,
        docker_gw_bridge_ip=None,
        physical_host_ip=None
    )

    kafka_topic_1 = KafkaTopic(
        name="test-topic-1",
        num_partitions=3,
        num_replicas=1,
        attributes=["column1", "column2", "column3"],
        retention_time_hours=72
    )

    kafka_topic_2 = KafkaTopic(
        name="test-topic-2",
        num_partitions=2,
        num_replicas=1,
        attributes=["column1", "column2"],
        retention_time_hours=48
    )

    topics = [kafka_topic_1, kafka_topic_2]

    kafka_config = KafkaConfig(
        container=container_config,
        resources=resources_config,
        firewall_config=firewall_config,
        topics=topics,
        kafka_manager_log_file='kafka_manager.log',
        kafka_manager_log_dir='/var/log/kafka_manager',
        kafka_manager_max_workers=4,
        kafka_port=9092,
        kafka_port_external=9292,
        time_step_len_seconds=15,
        kafka_manager_port=50051,
        version="0.0.1"
    )

    emulation_env_config = EmulationEnvConfig(
        name="test_env",
        containers_config=None,
        users_config=None,
        flags_config=None,
        vuln_config=None,
        topology_config=None,
        traffic_config=None,
        resources_config=None,
        kafka_config=kafka_config,
        services_config=None,
        descr="Test environment description",
        static_attacker_sequences=None,
        ovs_config=None,
        sdn_controller_config=None,
        host_manager_config=None,
        snort_ids_manager_config=None,
        ossec_ids_manager_config=None,
        docker_stats_manager_config=None,
        elk_config=None,
        beats_config=None,
        level=1,
        version="1.0",
        execution_id=12345,
        csle_collector_version=collector_constants.LATEST_VERSION,
        csle_ryu_version=collector_constants.LATEST_VERSION
    )

    ip = emulation_env_config.kafka_config.container.docker_gw_bridge_ip
    port = emulation_env_config.kafka_config.kafka_manager_port
    logger = logging.getLogger("test_logger")
    try:
        # Run each sed command
        internal_ip = emulation_env_config.kafka_config.container.get_ips()[0]
        kafka_config_file = collector_constants.KAFKA.KAFKA_CONFIG_FILE

        # Replace INTERNAL_IP
        internal_ip_cmd = (
            f"sed -i 's/{collector_constants.KAFKA.INTERNAL_IP_PLACEHOLDER}/"
            f"{internal_ip}/g' {kafka_config_file}"
        )
        result_internal_ip = container_setup.exec_run(internal_ip_cmd)
        if result_internal_ip.exit_code != 0:
            raise Exception(f"Failed to configure INTERNAL_IP: {result_internal_ip.output.decode('utf-8')}")

        # Replace EXTERNAL_IP
        external_ip_cmd = (
            f"sed -i 's/{collector_constants.KAFKA.EXTERNAL_IP_PLACEHOLDER}/"
            f"{ip}/g' {kafka_config_file}"
        )
        result_external_ip = container_setup.exec_run(external_ip_cmd)
        if result_external_ip.exit_code != 0:
            raise Exception(f"Failed to configure EXTERNAL_IP: {result_external_ip.output.decode('utf-8')}")

    except Exception as e:
        logger.error(f"Error configuring broker IPs: {e}")
        assert False, f"Failed to configure broker IPs: {e}"

    try:
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.kafka_manager.kafka_manager_pb2_grpc.KafkaManagerStub(channel)
            kafka_dto = csle_collector.kafka_manager.query_kafka_server.start_kafka(stub)
            logging.info(f"kafka_dto:{kafka_dto}")
            assert kafka_dto.running, f"Failed to start kafka on {ip}."
            logger.info(f"kafka has been successfully started on {ip}.")
    except grpc.RpcError as e:
        logger.error(f"gRPC Error: {e}")
        assert False, f"gRPC call failed with error: {e}"
        
    try:
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.kafka_manager.kafka_manager_pb2_grpc.KafkaManagerStub(channel)
            kafka_dto = csle_collector.kafka_manager.query_kafka_server.start_kafka(stub)
            logging.info(f"kafka_dto:{kafka_dto}")
            assert kafka_dto.running, f"Failed to start kafka on {ip}."
            logger.info(f"kafka has been successfully started on {ip}.")
            time.sleep(10)
            # create topics
            for topic in emulation_env_config.kafka_config.topics:
                logger.info(f"Creating topic: {topic.name}")
                create_response = csle_collector.kafka_manager.query_kafka_server.create_topic(
                    stub,
                    name=topic.name,
                    partitions=topic.num_partitions,
                    replicas=topic.num_replicas,
                    retention_time_hours=topic.retention_time_hours
                )
                assert topic.name in create_response.topics, (
                    f"Topic creation failed or topic name mismatch: {topic.name}"
                )
                logger.info(f"Successfully created topic: {topic.name}")
    except grpc.RpcError as e:
        logger.error(f"gRPC Error: {e}")
        assert False, f"gRPC call failed with error: {e}"
        
