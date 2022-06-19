from typing import List, Tuple
import subprocess
import time
import docker
import re
import os
import grpc
import socket
import csle_collector.docker_stats_manager.docker_stats_manager_pb2_grpc
import csle_collector.docker_stats_manager.docker_stats_manager_pb2
import csle_collector.docker_stats_manager.query_docker_stats_manager
from csle_common.util.docker_util import DockerUtil
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.containers_config import ContainersConfig
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.dao.emulation_config.log_sink_config import LogSinkConfig
import csle_common.constants.constants as constants
from csle_common.logging.log import Logger
from csle_common.dao.emulation_config.emulation_execution import EmulationExecution


class ContainerManager:
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
            Logger.__call__().get_logger().info("Stopping container: {}".format(c.name))
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
        non_base_images = list(filter(lambda x: (constants.DOCKER.BASE_CONTAINER_TYPE
                                                not in ",".join(x.attrs[constants.DOCKER.REPO_TAGS])), images))
        base_images = list(filter(lambda x: (constants.DOCKER.BASE_CONTAINER_TYPE
                                             in ",".join(x.attrs[constants.DOCKER.REPO_TAGS])), images))
        non_os_base_images = list(filter(lambda x: not
        (constants.OS.UBUNTU in ",".join(x.attrs[constants.DOCKER.REPO_TAGS])
         or constants.OS.KALI in ",".join(x.attrs[constants.DOCKER.REPO_TAGS])),
                                         base_images))
        os_base_images = list(filter(lambda x: constants.OS.UBUNTU in ",".join(x.attrs[constants.DOCKER.REPO_TAGS])
                                               or constants.OS.KALI in ",".join(x.attrs[constants.DOCKER.REPO_TAGS]),
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
        non_base_images = list(filter(lambda x: (constants.DOCKER.BASE_CONTAINER_TYPE
                                                 not in ",".join(x.attrs[constants.DOCKER.REPO_TAGS])),images))
        base_images = list(filter(lambda x: (constants.DOCKER.BASE_CONTAINER_TYPE
                                             in ",".join(x.attrs[constants.DOCKER.REPO_TAGS])),images))
        non_os_base_images = list(filter(lambda x: not
        (constants.OS.UBUNTU in ",".join(x.attrs[constants.DOCKER.REPO_TAGS])
         or constants.OS.KALI in ",".join(x.attrs[constants.DOCKER.REPO_TAGS])),
                                         base_images))
        os_base_images = list(filter(lambda x: constants.OS.UBUNTU in ",".join(x.attrs[constants.DOCKER.REPO_TAGS])
                                               or constants.OS.KALI in ",".join(x.attrs[constants.DOCKER.REPO_TAGS]),
                                     base_images))
        for img in non_base_images:
            if img == name:
                client_1.images.remove(image=img.attrs[constants.DOCKER.REPO_TAGS][0], force=True)
                return True
        for img in non_os_base_images:
            if img == name:
                client_1.images.remove(image=img.attrs[constants.DOCKER.REPO_TAGS][0], force=True)
                return True
        for img in os_base_images:
            if img == name:
                client_1.images.remove(image=img.attrs[constants.DOCKER.REPO_TAGS][0], force=True)
                return True

        return False

    @staticmethod
    def list_all_images() -> List[Tuple[str, str, str, str, str]]:
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
        networks = stream.read()
        networks = networks.split("\n")
        networks = list(map(lambda x: x.split(), networks))
        networks = list(filter(lambda x: len(x) > 1, networks))
        networks = list(map(lambda x: x[1], networks))
        networks = list(filter(lambda x: re.match(r"{}\d".format(constants.CSLE.CSLE_NETWORK_PREFIX), x),
                                        networks))
        network_ids = list(map(lambda x: int(x.replace(constants.CSLE.CSLE_NETWORK_PREFIX, "")),
                               networks))
        return networks, network_ids

    @staticmethod
    def list_all_networks() -> List[str]:
        """
        A utility function for listing all csle networks

        :return: a list of the networks
        """
        networks, network_ids = ContainerManager.list_docker_networks()
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
        container_name_image_ip = []
        for env in parsed_envs:
            container_name_image_ip = container_name_image_ip + \
                                      list(map(lambda x: (x.name, x.image_name, x.ip), env.containers))
        return container_name_image_ip

    @staticmethod
    def is_emulation_running(emulation_env_config: EmulationEnvConfig) -> bool:
        """
        Checks if a given emulation config is running or not

        :param emulation_env_config: the emulation environment configuraiton
        :return: True if running otherwise False
        """
        running_emulations = ContainerManager.list_running_emulations()
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
    def create_networks(containers_config: ContainersConfig) -> None:
        """
        Creates docker networks for a given containers configuration

        :param containers_config: the containers configuration
        :return: None
        """
        for c in containers_config.containers:
            for ip_net in c.ips_and_networks:
                networks = ContainerManager.get_network_references()
                networks = list(map(lambda x: x.name, networks))
                ip, net = ip_net
                ContainerManager.create_network_from_dto(network_dto=net, existing_network_names=networks)

    @staticmethod
    def connect_containers_to_networks(containers_config: ContainersConfig) -> None:
        """
        Connects running containers to networks

        :param containers_config: the containers configuration
        :return: None
        """
        for c in containers_config.containers:
            container_name = c.get_full_name()
            # Disconnect from none
            cmd = f"docker network disconnect none {container_name}"
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)

            # Wait a few seconds before connecting
            time.sleep(2)

            for ip_net in c.ips_and_networks:
                ip, net = ip_net
                cmd = f"{constants.DOCKER.NETWORK_CONNECT} --ip {ip} {net.name} " \
                      f"{container_name}"
                Logger.__call__().get_logger().info(f"Connecting container:{container_name} to network:{net.name} with ip: {ip}")
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)

    @staticmethod
    def connect_logsink_to_network(log_sink_config: LogSinkConfig) -> None:
        """
        Connect a running logsink to neworks

        :param log_sink_config: the log_sink config
        :return: None
        """
        c = log_sink_config.container
        container_name = c.get_full_name()
        # Disconnect from none
        cmd = f"docker network disconnect none {container_name}"
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)

        # Wait a few seconds before connecting
        time.sleep(2)

        for ip_net in c.ips_and_networks:
            ip, net = ip_net
            cmd = f"{constants.DOCKER.NETWORK_CONNECT} --ip {ip} {net.name} " \
                  f"{container_name}"
            Logger.__call__().get_logger().info(f"Connecting container:{container_name} to network:{net.name} with ip: {ip}")
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)

    @staticmethod
    def start_docker_stats_thread(execution: EmulationExecution) -> None:
        """
        Sends a request to the docker stats manager on the docker host for starting a docker stats monitor thread

        :param execution: the emulation execution
        :return: None
        """
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        with grpc.insecure_channel(f'{ip}:{execution.emulation_env_config.log_sink_config.default_grpc_port}') as channel:
            stub = csle_collector.docker_stats_manager.docker_stats_manager_pb2_grpc.DockerStatsManagerStub(channel)
            container_ip_dtos = []
            for c in execution.emulation_env_config.containers_config.containers:
                name = c.get_full_name()
                ip = c.get_ips()[0]
                container_ip_dtos.append(csle_collector.docker_stats_manager.docker_stats_manager_pb2.ContainerIp(
                    ip=ip, container=name))

            csle_collector.docker_stats_manager.query_docker_stats_manager.start_docker_stats_monitor(
                stub=stub, emulation=execution.emulation_name,
                sink_ip=execution.emulation_env_config.log_sink_config.container.get_ips()[0],
                stats_queue_maxsize=1000,
                time_step_len_seconds=execution.emulation_env_config.log_sink_config.time_step_len_seconds,
                sink_port=execution.emulation_env_config.log_sink_config.kafka_port,
                containers=container_ip_dtos, execution_first_ip_octet=execution.ip_first_octet)

    @staticmethod
    def stop_docker_stats_thread(execution: EmulationExecution) -> None:
        """
        Sends a request to the docker stats manager on the docker host for stopping a docker stats monitor thread

        :param execution: the execution of the emulation for which the monitor should be stopped
        :return: None
        """
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        with grpc.insecure_channel(f'{ip}:{execution.emulation_env_config.log_sink_config.default_grpc_port}') \
                as channel:
            stub = csle_collector.docker_stats_manager.docker_stats_manager_pb2_grpc.DockerStatsManagerStub(channel)
            csle_collector.docker_stats_manager.query_docker_stats_manager.stop_docker_stats_monitor(
                stub=stub, emulation=execution.emulation_name, execution_first_ip_octet = execution.ip_first_octet)


    @staticmethod
    def get_docker_stats_manager_status(log_sink_config: LogSinkConfig) \
            -> csle_collector.docker_stats_manager.docker_stats_manager_pb2.DockerStatsMonitorDTO:
        """
        Sends a request to get the status of the docker stats manager

        :param log_sink_config: configuration of the log sink
        :return: None
        """
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        with grpc.insecure_channel(f'{ip}:{log_sink_config.default_grpc_port}') as channel:
            stub = csle_collector.docker_stats_manager.docker_stats_manager_pb2_grpc.DockerStatsManagerStub(channel)
            docker_stats_monitor_dto = \
                csle_collector.docker_stats_manager.query_docker_stats_manager.get_docker_stats_manager_status(
                    stub=stub)
            return docker_stats_monitor_dto



    @staticmethod
    def connect_containers_to_logsink(containers_config: ContainersConfig, log_sink_config: LogSinkConfig) -> None:
        """
        Connects running containers to the log sink

        :param containers_config: the containers configuration
        :param log_sink_config: the configuration of the logsink
        :return: None
        """
        log_sink_ip, logsink_net = log_sink_config.container.ips_and_networks[0]
        log_sink_network_prefix = ".".join(log_sink_ip.split(".")[0:-1])
        for c in containers_config.containers:
            for ovs_image in constants.CONTAINER_IMAGES.OVS_IMAGES:
                if ovs_image in c.name:
                    continue
            container_name = c.get_full_name()

            ip_suffix = c.ips_and_networks[0][0].split(".")[-1]
            c_ip = log_sink_network_prefix + "." + ip_suffix
            cmd = f"{constants.DOCKER.NETWORK_CONNECT} --ip {c_ip} {logsink_net.name} " \
                  f"{container_name}"
            Logger.__call__().get_logger().info(
                f"Connecting container:{container_name} to network:{logsink_net.name} with ip: {c_ip}")
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)

    @staticmethod
    def create_network_from_dto(network_dto: ContainerNetwork, existing_network_names = None) -> None:
        """
        Creates a network from a given DTO representing the network

        :param existing_network_names: list of network names, if not None, check if network exists befeore creating
        :return: None
        """
        ContainerManager.create_network(name=network_dto.name, subnetmask=network_dto.subnet_mask,
                                        existing_network_names=existing_network_names)

    @staticmethod
    def create_network(name: str, subnetmask: str, driver: str = "bridge", existing_network_names : List = None) -> None:
        """
        Creates a network

        :param name: the name of the network to create
        :param subnetmask: the subnetmask of the network to create
        :param driver: the driver of the network to create
        :param existing_network_names: list of network names, if not None, check if network exists befeore creating
        :return: None
        """
        client_1 = docker.from_env()
        ipam_pool = docker.types.IPAMPool(
            subnet=subnetmask
        )
        ipam_config = docker.types.IPAMConfig(
            pool_configs=[ipam_pool],
        )
        network_names = []
        if existing_network_names is not None:
            network_names = existing_network_names
        if name not in network_names:
            Logger.__call__().get_logger().info(f"Creating network: {name}, subnetmask: {subnetmask}")
            client_1.networks.create(
                name,
                driver=driver,
                ipam=ipam_config
            )

    @staticmethod
    def remove_network(name: str) -> None:
        """
        Removes a network

        :param name: the name of the network to remove
        :return: None
        """
        client_1 = docker.from_env()
        networks = client_1.networks.list()
        for net in networks:
            if net.name == name:
                Logger.__call__().get_logger().info(f"Removing network: {net.name}")
                try:
                    net.remove()
                except:
                    pass

    @staticmethod
    def remove_networks(names: List[str]) -> None:
        """
        Removes a network

        :param name: the name of the network to remove
        :return: None
        """
        client_1 = docker.from_env()
        networks = client_1.networks.list()
        for net in networks:
            if net.name in names:
                Logger.__call__().get_logger().info(f"Removing network: {net.name}")
                try:
                    net.remove()
                except:
                    pass

    @staticmethod
    def rm_all_networks() -> None:
        """
        A utility function for removing all csle networks

        :return: None
        """
        client_1 = docker.from_env()
        networks = client_1.networks.list()
        networks = list(filter(lambda x: constants.CSLE.NAME in x.name, networks))
        for net in networks:
            Logger.__call__().get_logger().info(f"Removing network:{net.name}")
            ContainerManager.remove_network(name = net.name)


    @staticmethod
    def rm_network(name) -> bool:
        """
        A utility function for removing a network with a specific name

        :return: True if it was removed or False otherwise
        """
        client_1 = docker.from_env()
        networks = client_1.networks.list()
        networks = list(filter(lambda x: constants.CSLE.NAME in x.name, networks))
        for net in networks:
            if net == name:
                ContainerManager.remove_network(name = net.name)
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
            names = ContainerManager.list_all_stopped_containers()
            Logger.__call__().get_logger().info(names)
        elif cmd == constants.MANAGEMENT.LIST_RUNNING:
            names = ContainerManager.list_all_running_containers()
            Logger.__call__().get_logger().info(names)
        elif cmd == constants.MANAGEMENT.LIST_IMAGES:
            names = ContainerManager.list_all_images()
            Logger.__call__().get_logger().info(names)
        elif cmd == constants.MANAGEMENT.STOP_RUNNING:
            ContainerManager.stop_all_running_containers()
        elif cmd == constants.MANAGEMENT.RM_STOPPED:
            ContainerManager.rm_all_stopped_containers()
        elif cmd == constants.MANAGEMENT.RM_IMAGES:
            ContainerManager.rm_all_images()
        elif cmd == constants.MANAGEMENT.START_STOPPED:
            ContainerManager.start_all_stopped_containers()
        elif cmd == constants.MANAGEMENT.LIST_NETWORKS:
            networks = ContainerManager.list_all_networks()
            Logger.__call__().get_logger().info(networks)
        elif cmd == constants.MANAGEMENT.RM_NETWORKS:
            ContainerManager.rm_all_networks()
        else:
            raise ValueError("Command: {} not recognized".format(cmd))
