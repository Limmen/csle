from typing import List, Tuple, Union
import logging
import subprocess
import time
import docker
import re
import os
import grpc
import csle_collector.docker_stats_manager.docker_stats_manager_pb2_grpc
import csle_collector.docker_stats_manager.docker_stats_manager_pb2
import csle_collector.docker_stats_manager.query_docker_stats_manager
import csle_collector.docker_stats_manager.docker_stats_util
from csle_common.util.docker_util import DockerUtil
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.containers_config import ContainersConfig
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.dao.emulation_config.docker_stats_manager_config import DockerStatsManagerConfig
import csle_common.constants.constants as constants
from csle_common.logging.log import Logger
from csle_common.dao.emulation_config.emulation_execution import EmulationExecution
from csle_common.dao.emulation_config.docker_stats_managers_info import DockerStatsManagersInfo
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.controllers.management_system_controller import ManagementSystemController
from csle_common.dao.emulation_config.config import Config
from csle_common.util.general_util import GeneralUtil


class ContainerController:
    """
    A class for managing Docker containers and virtual networks
    """

    @staticmethod
    def stop_all_running_containers() -> None:
        """
        Utility function for stopping all running containers

        :return: None
        """
        client_1 = docker.from_env()
        containers = client_1.containers.list()
        containers = list(filter(lambda x: constants.CSLE.NAME in x.name, containers))
        for c in containers:
            Logger.__call__().get_logger().info(f"Stopping container: {c.name}")
            c.stop()

    @staticmethod
    def stop_container(name: str) -> bool:
        """
        Utility function for stopping a specific container

        :param name: the name of the container to stop
        :return: True if stopped, False otherwise
        """
        client_1 = docker.from_env()
        containers = client_1.containers.list()
        containers = list(filter(lambda x: constants.CSLE.NAME in x.name, containers))
        for c in containers:
            if c.name == name:
                c.stop()
                return True
        return False

    @staticmethod
    def rm_all_stopped_containers() -> None:
        """
        A utility function for removing all stopped containers

        :return: None
        """
        client_1 = docker.from_env()
        containers = client_1.containers.list(all=True)
        containers = list(filter(lambda x: (constants.CSLE.NAME in x.name
                                            and x.status == constants.DOCKER.CONTAINER_EXIT_STATUS
                                            or x.status == constants.DOCKER.CONTAINER_CREATED_STATUS), containers))
        for c in containers:
            Logger.__call__().get_logger().info(f"Removing container: {c.name}")
            c.remove()

    @staticmethod
    def rm_container(container_name: str) -> bool:
        """
        Remove a specific container

        :param container_name: the container to remove
        :return: True if the container was removed and False otherwise
        """
        client_1 = docker.from_env()
        containers = client_1.containers.list(all=True)
        for c in containers:
            if c.name == container_name:
                c.remove()
                return True
        return False

    @staticmethod
    def rm_all_images() -> None:
        """
        A utility function for removing all csle images

        :return: None
        """
        client_1 = docker.from_env()
        images = client_1.images.list()
        images = list(filter(lambda x: constants.CSLE.NAME in ",".join(x.attrs[constants.DOCKER.REPO_TAGS]), images))
        non_base_images = list(
            filter(lambda x: (constants.DOCKER.BASE_CONTAINER_TYPE
                              not in ",".join(x.attrs[constants.DOCKER.REPO_TAGS])), images))
        base_images = list(filter(lambda x: (constants.DOCKER.BASE_CONTAINER_TYPE
                                             in ",".join(x.attrs[constants.DOCKER.REPO_TAGS])), images))
        non_os_base_images = list(filter(
            lambda x: not (constants.OS.UBUNTU in ",".join(x.attrs[constants.DOCKER.REPO_TAGS])
                           or constants.OS.KALI in ",".join(x.attrs[constants.DOCKER.REPO_TAGS])), base_images))
        os_base_images = list(filter(lambda x: (constants.OS.UBUNTU in ",".join(x.attrs[constants.DOCKER.REPO_TAGS])
                                                or constants.OS.KALI in ",".join(x.attrs[constants.DOCKER.REPO_TAGS])),
                                     base_images))
        for img in non_base_images:
            Logger.__call__().get_logger().info("Removing image: {}".format(img.attrs[constants.DOCKER.REPO_TAGS]))
            client_1.images.remove(image=img.attrs[constants.DOCKER.REPO_TAGS][0], force=True)
        for img in non_os_base_images:
            Logger.__call__().get_logger().info("Removing image: {}".format(img.attrs[constants.DOCKER.REPO_TAGS]))
            client_1.images.remove(image=img.attrs[constants.DOCKER.REPO_TAGS][0], force=True)
        for img in os_base_images:
            Logger.__call__().get_logger().info("Removing image: {}".format(img.attrs[constants.DOCKER.REPO_TAGS]))
            client_1.images.remove(image=img.attrs[constants.DOCKER.REPO_TAGS][0], force=True)

    @staticmethod
    def rm_image(name) -> bool:
        """
        A utility function for removing a specific image

        :param name: the name of the image to remove
        :return: True if the image was removed and False otherwise
        """
        client_1 = docker.from_env()
        images = client_1.images.list()
        images = list(filter(lambda x: constants.CSLE.NAME in ",".join(x.attrs[constants.DOCKER.REPO_TAGS]), images))
        non_base_images = list(filter(
            lambda x: (constants.DOCKER.BASE_CONTAINER_TYPE not in ",".join(x.attrs[constants.DOCKER.REPO_TAGS])),
            images))
        base_images = list(filter(lambda x: (constants.DOCKER.BASE_CONTAINER_TYPE
                                             in ",".join(x.attrs[constants.DOCKER.REPO_TAGS])), images))
        non_os_base_images = list(
            filter(lambda x: not (constants.OS.UBUNTU in ",".join(x.attrs[constants.DOCKER.REPO_TAGS]) or
                                  constants.OS.KALI in ",".join(x.attrs[constants.DOCKER.REPO_TAGS])), base_images))
        os_base_images = list(
            filter(lambda x: (constants.OS.UBUNTU in ",".join(x.attrs[constants.DOCKER.REPO_TAGS]) or constants.OS.KALI
                              in ",".join(x.attrs[constants.DOCKER.REPO_TAGS])), base_images))
        for img in non_base_images:
            if img.attrs[constants.DOCKER.REPO_TAGS][0] == name:
                client_1.images.remove(image=img.attrs[constants.DOCKER.REPO_TAGS][0], force=True)
                return True
        for img in non_os_base_images:
            if img.attrs[constants.DOCKER.REPO_TAGS][0] == name:
                client_1.images.remove(image=img.attrs[constants.DOCKER.REPO_TAGS][0], force=True)
                return True
        for img in os_base_images:
            if img.attrs[constants.DOCKER.REPO_TAGS][0] == name:
                client_1.images.remove(image=img.attrs[constants.DOCKER.REPO_TAGS][0], force=True)
                return True

        return False

    @staticmethod
    def list_all_images() -> List[Tuple[str, str, str, str, int]]:
        """
        A utility function for listing all csle images

        :return: a list of the csle images
        """
        client_1 = docker.from_env()
        images = client_1.images.list()
        images = list(filter(lambda x: constants.CSLE.NAME in ",".join(x.attrs[constants.DOCKER.REPO_TAGS]), images))
        images_names_created_os_architecture_size = list(
            map(lambda x: (x.attrs[constants.DOCKER.REPO_TAGS][0],
                           x.attrs[constants.DOCKER.IMAGE_CREATED], x.attrs[constants.DOCKER.IMAGE_OS],
                           x.attrs[constants.DOCKER.IMAGE_ARCHITECTURE], x.attrs[constants.DOCKER.IMAGE_SIZE]), images))
        return images_names_created_os_architecture_size

    @staticmethod
    def list_docker_networks() -> Tuple[List[str], List[int]]:
        """
        Lists the csle docker networks

        :return: (network names, network ids)
        """
        cmd = constants.DOCKER.LIST_NETWORKS_CMD
        stream = os.popen(cmd)
        networks_str: str = stream.read()
        networks: List[str] = networks_str.split("\n")

        networks_list: List[List[str]] = list(map(lambda x: x.split(), networks))
        networks_list = list(filter(lambda x: len(x) > 1, networks_list))
        networks_ids_str: List[str] = list(map(lambda x: x[1], networks_list))

        networks_ids_str = list(filter(lambda x: re.match(
            r"{}\d".format(constants.CSLE.CSLE_NETWORK_PREFIX), x), networks_ids_str))
        network_ids: List[int] = list(map(lambda x: int(x.replace(constants.CSLE.CSLE_NETWORK_PREFIX, "")),
                                          networks_ids_str))
        return networks_ids_str, network_ids

    @staticmethod
    def list_all_networks() -> List[str]:
        """
        A utility function for listing all csle networks

        :return: a list of the networks
        """
        networks, network_ids = ContainerController.list_docker_networks()
        return networks

    @staticmethod
    def start_all_stopped_containers() -> None:
        """
        Starts all stopped csle containers

        :return: None
        """
        client_1 = docker.from_env()
        containers = client_1.containers.list(all=True)
        containers = list(filter(lambda x: (constants.CSLE.NAME in x.name
                                            and x.status == constants.DOCKER.CONTAINER_EXIT_STATUS
                                            or x.status == constants.DOCKER.CONTAINER_CREATED_STATUS), containers))
        for c in containers:
            Logger.__call__().get_logger().info("Starting container: {}".format(c.name))
            c.start()

    @staticmethod
    def start_container(name: str) -> bool:
        """
        Starts a stopped container with a specific name

        :param name: the name of the stopped container to start
        :return: True if started, False otherrwise
        """
        client_1 = docker.from_env()
        containers = client_1.containers.list(all=True)
        containers = list(filter(lambda x: (constants.CSLE.NAME in x.name
                                            and x.status == constants.DOCKER.CONTAINER_EXIT_STATUS
                                            or x.status == constants.DOCKER.CONTAINER_CREATED_STATUS), containers))
        for c in containers:
            if c.name == name:
                c.start()
                return True
        return False

    @staticmethod
    def list_all_running_containers() -> List[Tuple[str, str, str]]:
        """
        Lists all running csle containers

        :return: a list of the names of the running containers
        """
        parsed_envs = DockerUtil.parse_runnning_emulation_infos()
        container_name_image_ip: List[Tuple[str, str, str]] = []
        for env in parsed_envs:
            container_name_image_ip = (container_name_image_ip +
                                       list(map(lambda x: (x.name, x.image_name, x.ip), env.containers)))
        return container_name_image_ip

    @staticmethod
    def list_all_running_containers_in_emulation(emulation_env_config: EmulationEnvConfig) \
            -> Tuple[List[NodeContainerConfig], List[NodeContainerConfig]]:
        """
        Extracts the running containers and the stopped containers of a given emulation

        :param emulation_env_config: the emulation configuration
        :return: the list of running containers and the list of stopped containers
        """
        running_emulation_containers = []
        stopped_emulation_containers = []
        running_containers = ContainerController.list_all_running_containers()
        running_containers_names = list(map(lambda x: x[0], running_containers))
        for c in emulation_env_config.containers_config.containers:
            if c.full_name_str in running_containers_names:
                running_emulation_containers.append(c)
            else:
                stopped_emulation_containers.append(c)
        if emulation_env_config.kafka_config.container.full_name_str in running_containers_names:
            running_emulation_containers.append(emulation_env_config.kafka_config.container)
        else:
            stopped_emulation_containers.append(emulation_env_config.kafka_config.container)

        if emulation_env_config.elk_config.container.full_name_str in running_containers_names:
            running_emulation_containers.append(emulation_env_config.elk_config.container)
        else:
            stopped_emulation_containers.append(emulation_env_config.elk_config.container)

        if emulation_env_config.sdn_controller_config is not None:
            if emulation_env_config.sdn_controller_config.container.full_name_str in running_containers_names:

                running_emulation_containers.append(emulation_env_config.sdn_controller_config.container)
            else:
                stopped_emulation_containers.append(emulation_env_config.sdn_controller_config.container)
        return running_emulation_containers, stopped_emulation_containers

    @staticmethod
    def list_all_active_networks_for_emulation(emulation_env_config: EmulationEnvConfig) \
            -> Tuple[List[ContainerNetwork], List[ContainerNetwork]]:
        """
        Extracts the active networks of a given emulation

        :param emulation_env_config: the emulation configuration
        :return: the list of active networks and inactive networks of an emulation
        """
        active_emulation_networks = []
        inactive_emulation_networks = []
        active_networks_names = ContainerController.list_all_networks()
        for net in emulation_env_config.containers_config.networks:
            if net.name in active_networks_names:
                active_emulation_networks.append(net)
            else:
                inactive_emulation_networks.append(net)
        return active_emulation_networks, inactive_emulation_networks

    @staticmethod
    def is_emulation_running(emulation_env_config: EmulationEnvConfig) -> bool:
        """
        Checks if a given emulation config is running or not

        :param emulation_env_config: the emulation environment configuration
        :return: True if running otherwise False
        """
        running_emulations = ContainerController.list_running_emulations()
        return emulation_env_config.name in running_emulations

    @staticmethod
    def list_running_emulations() -> List[str]:
        """
        :return: A list of names of running emulations
        """
        parsed_envs = DockerUtil.parse_runnning_emulation_infos()
        emulation_names = set()
        for env in parsed_envs:
            emulation_names.add(env.name)
        return list(emulation_names)

    @staticmethod
    def list_all_stopped_containers() -> List[Tuple[str, str, str]]:
        """
        Lists all stopped csle containers

        :return: a list of the stopped containers
        """
        client_1 = docker.from_env()
        client2 = docker.APIClient(base_url=constants.DOCKER.UNIX_DOCKER_SOCK_URL)
        parsed_stopped_containers = DockerUtil.parse_stopped_containers(client_1=client_1, client2=client2)
        container_name_image_ips = list(map(lambda x: (x.name, x.image_name, x.ip), parsed_stopped_containers))
        return container_name_image_ips

    @staticmethod
    def get_network_references():
        """
        :return: a list of Docker network references
        """
        client_1 = docker.from_env()
        networks = client_1.networks.list()
        return networks

    @staticmethod
    def create_networks(containers_config: ContainersConfig, logger: logging.Logger) -> None:
        """
        Creates docker networks for a given containers configuration

        :param logger: the logger to use for logging
        :param containers_config: the containers configuration
        :return: None
        """
        for c in containers_config.containers:
            for ip_net in c.ips_and_networks:
                existing_networks = ContainerController.get_network_references()
                existing_networks = list(map(lambda x: x.name, existing_networks))
                ip, net = ip_net
                if net.name != "":
                    ContainerController.create_network_from_dto(network_dto=net,
                                                                existing_network_names=existing_networks,
                                                                logger=logger)

    @staticmethod
    def connect_containers_to_networks(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                                       logger: logging.Logger) -> None:
        """
        Connects running containers to networks

        :param emulation_env_config: the emulation config
        :param physical_server_ip: the ip of the physical server where the operation is executed
        :param logger: the logger to use for logging
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            container_name = c.get_full_name()
            # Disconnect from none
            cmd = f"docker network disconnect none {container_name}"
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)

            # Wait a few seconds before connecting
            time.sleep(2)

            for ip_net in c.ips_and_networks:
                time.sleep(2)
                ip, net = ip_net
                cmd = f"{constants.DOCKER.NETWORK_CONNECT} --ip {ip} {net.name} " \
                      f"{container_name}"
                logger.info(f"Connecting container:{container_name} to network:{net.name} with ip: {ip}, cmd: {cmd}")
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)

                if c.docker_gw_bridge_ip == "" or c.docker_gw_bridge_ip is None:
                    # Wait to make sure docker networks are updated
                    time.sleep(2)
                    # Extract the docker bridge gateway IP
                    container_id = DockerUtil.get_container_hex_id(name=container_name)
                    if container_id is None:
                        raise ValueError(f"Could not parse the container id with container name: {container_name}")
                    docker_gw_bridge_ip = DockerUtil.get_docker_gw_bridge_ip(container_id=container_id)
                    c.docker_gw_bridge_ip = docker_gw_bridge_ip

        if emulation_env_config.kafka_config.container.physical_host_ip == physical_server_ip:
            ContainerController.connect_container_to_network(container=emulation_env_config.kafka_config.container,
                                                             logger=logger)
        if emulation_env_config.elk_config.container.physical_host_ip == physical_server_ip:
            ContainerController.connect_container_to_network(container=emulation_env_config.elk_config.container,
                                                             logger=logger)
        if emulation_env_config.sdn_controller_config is not None and \
                emulation_env_config.sdn_controller_config.container.physical_host_ip == physical_server_ip:
            # Connect controller
            ContainerController.connect_container_to_network(
                container=emulation_env_config.sdn_controller_config.container, logger=logger)
            # Update IPs of OVS switches
            for ovs_sw in emulation_env_config.ovs_config.switch_configs:
                node_container_config = emulation_env_config.containers_config.get_container_from_ip(ovs_sw.ip)
                if node_container_config is None:
                    raise ValueError(f"Could not find node container config for IP: {ovs_sw.ip}")
                ovs_sw.docker_gw_bridge_ip = node_container_config.docker_gw_bridge_ip

    @staticmethod
    def connect_container_to_network(container: NodeContainerConfig, logger: logging.Logger) -> None:
        """
        Connect a running container to networks

        :param container: the container to connect
        :param logger: the logger to use for logging
        :return: None
        """
        container_name = container.get_full_name()
        # Disconnect from none
        cmd = f"docker network disconnect none {container_name}"
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)

        # Wait a few seconds before connecting
        time.sleep(2)

        for ip_net in container.ips_and_networks:
            time.sleep(2)
            ip, net = ip_net
            cmd = f"{constants.DOCKER.NETWORK_CONNECT} --ip {ip} {net.name} " \
                  f"{container_name}"
            logger.info(f"Connecting container:{container_name} to network:{net.name} with ip: {ip}, cmd: {cmd}")
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
            if container.docker_gw_bridge_ip == "" or container.docker_gw_bridge_ip is None:
                # Wait to make sure docker networks are updated
                time.sleep(2)
                # Extract the docker bridge gateway IP
                container_id = DockerUtil.get_container_hex_id(name=container_name)
                if container_id is None:
                    raise ValueError(f"Could not parse the container id for container name: {container_name}")
                docker_gw_bridge_ip = DockerUtil.get_docker_gw_bridge_ip(container_id=container_id)
                container.docker_gw_bridge_ip = docker_gw_bridge_ip

    @staticmethod
    def start_docker_stats_thread(execution: EmulationExecution, physical_server_ip: str,
                                  logger: logging.Logger) -> None:
        """
        Sends a request to the docker stats manager on the docker host for starting a docker stats monitor thread

        :param execution: the emulation execution
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        if not ManagementSystemController.is_statsmanager_running():
            ManagementSystemController.start_docker_statsmanager(
                logger=logger,
                port=execution.emulation_env_config.docker_stats_manager_config.docker_stats_manager_port,
                log_dir=execution.emulation_env_config.docker_stats_manager_config.docker_stats_manager_log_dir,
                log_file=execution.emulation_env_config.docker_stats_manager_config.docker_stats_manager_log_file,
                max_workers=execution.emulation_env_config.docker_stats_manager_config.docker_stats_manager_max_workers
            )
            time.sleep(5)
        ip = physical_server_ip
        logger.info(
            f"connecting to: {ip}:"
            f"{execution.emulation_env_config.docker_stats_manager_config.docker_stats_manager_port}")
        with grpc.insecure_channel(
                f'{ip}:'
                f'{execution.emulation_env_config.docker_stats_manager_config.docker_stats_manager_port}',
                options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.docker_stats_manager.docker_stats_manager_pb2_grpc.DockerStatsManagerStub(channel)
            container_ip_dtos = []
            for c in execution.emulation_env_config.containers_config.containers:
                if c.physical_host_ip == physical_server_ip:
                    name = c.get_full_name()
                    ip = c.get_ips()[0]
                    container_ip_dtos.append(csle_collector.docker_stats_manager.docker_stats_manager_pb2.ContainerIp(
                        ip=ip, container=name))
            logger.info("connected")

            csle_collector.docker_stats_manager.query_docker_stats_manager.start_docker_stats_monitor(
                stub=stub, emulation=execution.emulation_name,
                kafka_ip=execution.emulation_env_config.kafka_config.container.docker_gw_bridge_ip,
                stats_queue_maxsize=1000,
                time_step_len_seconds=execution.emulation_env_config.docker_stats_manager_config.time_step_len_seconds,
                kafka_port=execution.emulation_env_config.kafka_config.kafka_port_external,
                containers=container_ip_dtos, execution_first_ip_octet=execution.ip_first_octet)

    @staticmethod
    def stop_docker_stats_thread(execution: EmulationExecution, physical_server_ip: str,
                                 logger: logging.Logger) -> None:
        """
        Sends a request to the docker stats manager on the docker host for stopping a docker stats monitor thread

        :param logger: the logger to use for logging
        :param execution: the execution of the emulation for which the monitor should be stopped
        :param physical_server_ip: the ip of the physical server
        :return: None
        """
        if not ManagementSystemController.is_statsmanager_running():
            ManagementSystemController.stop_docker_statsmanager(logger=logger)
            time.sleep(5)
        ip = physical_server_ip
        with grpc.insecure_channel(
                f'{ip}:'
                f'{execution.emulation_env_config.docker_stats_manager_config.docker_stats_manager_port}',
                options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.docker_stats_manager.docker_stats_manager_pb2_grpc.DockerStatsManagerStub(channel)
            csle_collector.docker_stats_manager.query_docker_stats_manager.stop_docker_stats_monitor(
                stub=stub, emulation=execution.emulation_name, execution_first_ip_octet=execution.ip_first_octet)

    @staticmethod
    def get_docker_stats_manager_status(docker_stats_manager_config: DockerStatsManagerConfig) \
            -> csle_collector.docker_stats_manager.docker_stats_manager_pb2.DockerStatsMonitorDTO:
        """
        Sends a request to get the status of the docker stats manager

        :param docker_stats_manager_config: the docker stats manager configuration
        :return: None
        """
        ip = GeneralUtil.get_host_ip()
        docker_stats_monitor_dto = ContainerController.get_docker_stats_manager_status_by_ip_and_port(
            ip=ip, port=docker_stats_manager_config.docker_stats_manager_port)
        return docker_stats_monitor_dto

    @staticmethod
    def get_docker_stats_manager_status_by_ip_and_port(ip: str, port: int) \
            -> csle_collector.docker_stats_manager.docker_stats_manager_pb2.DockerStatsMonitorDTO:
        """
        Sends a request to get the status of the docker stats manager

        :param ip: ip of the host where the stats manager is running
        :param port: port that the host manager is listening to
        :return: None
        """
        try:
            with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
                stub = csle_collector.docker_stats_manager.docker_stats_manager_pb2_grpc.DockerStatsManagerStub(channel)

                docker_stats_monitor_dto = \
                    csle_collector.docker_stats_manager.query_docker_stats_manager.get_docker_stats_manager_status(
                        stub=stub)
                return docker_stats_monitor_dto
        except Exception:
            return None

    @staticmethod
    def create_network_from_dto(network_dto: ContainerNetwork, logger: logging.Logger,
                                existing_network_names=None) -> None:
        """
        Creates a network from a given DTO representing the network

        :param network_dto: details of the network to create
        :param existing_network_names: list of network names, if not None, check if network exists befeore creating
        :param logger: the logger to use for logging
        :return: None
        """
        config = Config.get_current_config()
        if config is None:
            raise ValueError("Could not parse the CSLE config")
        driver = constants.DOCKER.BRIDGE_NETWORK_DRIVER
        if len(config.cluster_config.cluster_nodes) > 0:
            driver = constants.DOCKER.OVERLAY_NETWORK_DRIVER
        ContainerController.create_network(name=network_dto.name, subnetmask=network_dto.subnet_mask,
                                           existing_network_names=existing_network_names, driver=driver,
                                           logger=logger)

    @staticmethod
    def create_network(name: str, subnetmask: str, logger: logging.Logger,
                       driver: str = "bridge", existing_network_names: Union[None, List[str]] = None) -> None:
        """
        Creates a network

        :param name: the name of the network to create
        :param subnetmask: the subnetmask of the network to create
        :param logger: the logger to use for logging
        :param driver: the driver of the network to create
        :param existing_network_names: list of network names, if not None, check if network exists befeore creating
        :return: None
        """
        client_1 = docker.from_env()
        ipam_pool = docker.types.IPAMPool(subnet=subnetmask)
        ipam_config = docker.types.IPAMConfig(pool_configs=[ipam_pool])
        network_names = []
        if existing_network_names is not None:
            network_names = existing_network_names
        if name not in network_names:
            logger.info(f"Creating network: {name}, subnetmask: {subnetmask}, driver: {driver}")
            client_1.networks.create(
                name,
                driver=driver,
                ipam=ipam_config,
                attachable=True
            )

    @staticmethod
    def remove_network(name: str, logger: logging.Logger) -> None:
        """
        Removes a network

        :param name: the name of the network to remove
        :param logger: the logger to use for logging
        :return: None
        """
        client_1 = docker.from_env()
        networks = client_1.networks.list()
        for net in networks:
            if net.name == name:
                logger.info(f"Removing network: {net.name}")
                try:
                    net.remove()
                except Exception:
                    pass

    @staticmethod
    def remove_networks(names: List[str], logger: logging.Logger) -> bool:
        """
        Removes a network

        :param name: the name of the network to remove
        :param logger: the logger to use for logging
        :return: True if at least one of the networks were successfully removed
        """
        client_1 = docker.from_env()
        networks = client_1.networks.list()
        network_removed = False
        for net in networks:
            if net.name in names:
                logger.info(f"Removing network: {net.name}")
                try:
                    net.remove()
                    network_removed = True
                except Exception:
                    pass
        return network_removed

    @staticmethod
    def rm_all_networks(logger: logging.Logger) -> None:
        """
        A utility function for removing all csle networks

        :param logger: the logger to use for logging
        :return: None
        """
        client_1 = docker.from_env()
        networks = client_1.networks.list()
        networks = list(filter(lambda x: constants.CSLE.NAME in x.name, networks))
        for net in networks:
            logger.info(f"Removing network:{net.name}")
            ContainerController.remove_network(name=net.name, logger=logger)

    @staticmethod
    def rm_network(name, logger: logging.Logger) -> bool:
        """
        A utility function for removing a network with a specific name

        :param name: the name of the network to remove
        :param logger: the logger to use for logging
        :return: True if it was removed or False otherwise
        """
        client_1 = docker.from_env()
        networks = client_1.networks.list()
        networks_names = []
        for net in networks:
            if constants.CSLE.NAME in net.name:
                net.name = constants.CSLE.NAME
                networks_names.append(net)
        networks = list(filter(lambda x: constants.CSLE.NAME in x.name, networks))
        for net in networks_names:
            if net.name == name:
                ContainerController.remove_network(name=net.name, logger=logger)
                return True
        return False

    @staticmethod
    def run_command(cmd: str) -> None:
        """
        Runs a container management command

        :param cmd: the command to run
        :return: None
        """
        if cmd == constants.MANAGEMENT.LIST_STOPPED:
            stopped_container_names = ContainerController.list_all_stopped_containers()
            Logger.__call__().get_logger().info(stopped_container_names)
        elif cmd == constants.MANAGEMENT.LIST_RUNNING:
            running_container_names = ContainerController.list_all_running_containers()
            Logger.__call__().get_logger().info(running_container_names)
        elif cmd == constants.MANAGEMENT.LIST_IMAGES:
            images_names = ContainerController.list_all_images()
            Logger.__call__().get_logger().info(images_names)
        elif cmd == constants.MANAGEMENT.STOP_RUNNING:
            ContainerController.stop_all_running_containers()
        elif cmd == constants.MANAGEMENT.RM_STOPPED:
            ContainerController.rm_all_stopped_containers()
        elif cmd == constants.MANAGEMENT.RM_IMAGES:
            ContainerController.rm_all_images()
        elif cmd == constants.MANAGEMENT.START_STOPPED:
            ContainerController.start_all_stopped_containers()
        elif cmd == constants.MANAGEMENT.LIST_NETWORKS:
            networks = ContainerController.list_all_networks()
            Logger.__call__().get_logger().info(networks)
        elif cmd == constants.MANAGEMENT.RM_NETWORKS:
            ContainerController.rm_all_networks(logger=Logger.__call__().get_logger())
        else:
            raise ValueError("Command: {} not recognized".format(cmd))

    @staticmethod
    def get_docker_stats_managers_ips(emulation_env_config: EmulationEnvConfig) -> List[str]:
        """
        A method that extracts the IPS of the Docker stats managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of IP addresses
        """
        return [GeneralUtil.get_host_ip()]

    @staticmethod
    def get_docker_stats_managers_ports(emulation_env_config: EmulationEnvConfig) -> List[int]:
        """
        A method that extracts the ports of the Docker stats managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of ports
        """
        return [emulation_env_config.docker_stats_manager_config.docker_stats_manager_port]

    @staticmethod
    def get_docker_stats_managers_info(emulation_env_config: EmulationEnvConfig, active_ips: List[str],
                                       physical_host_ip: str, logger: logging.Logger) \
            -> DockerStatsManagersInfo:
        """
        Extracts the information of the Docker stats managers for a given emulation

        :param emulation_env_config: the configuration of the emulation
        :param active_ips: list of active IPs
        :param physical_host_ip: the ip of the physical host
        :param logger: the logger to use for logging
        :return: a DTO with the status of the Docker stats managers
        """
        docker_stats_managers_ips = ContainerController.get_docker_stats_managers_ips(
            emulation_env_config=emulation_env_config)
        docker_stats_managers_ports = ContainerController.get_docker_stats_managers_ports(
            emulation_env_config=emulation_env_config)
        docker_stats_managers_statuses = []
        docker_stats_managers_running = []
        for ip in docker_stats_managers_ips:
            if ip not in active_ips or ip != physical_host_ip:
                continue
            running = False
            status = None
            try:
                status = ContainerController.get_docker_stats_manager_status_by_ip_and_port(
                    port=emulation_env_config.docker_stats_manager_config.docker_stats_manager_port, ip=ip)
                running = True
            except Exception as e:
                logger.debug(
                    f"Could not fetch Docker stats manager status on IP:{ip}, error: {str(e)}, {repr(e)}")
            if status is not None:
                docker_stats_managers_statuses.append(status)
            else:
                stats_util = csle_collector.docker_stats_manager.docker_stats_util.DockerStatsUtil
                docker_stats_managers_statuses.append(stats_util.docker_stats_monitor_dto_empty())
            docker_stats_managers_running.append(running)
        execution_id = emulation_env_config.execution_id
        emulation_name = emulation_env_config.name
        docker_stats_manager_info_dto = DockerStatsManagersInfo(
            docker_stats_managers_running=docker_stats_managers_running, ips=docker_stats_managers_ips,
            execution_id=execution_id, emulation_name=emulation_name,
            docker_stats_managers_statuses=docker_stats_managers_statuses, ports=docker_stats_managers_ports)
        return docker_stats_manager_info_dto
