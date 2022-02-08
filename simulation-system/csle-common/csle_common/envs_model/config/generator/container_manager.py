from typing import List, Tuple
import subprocess
import time
import docker
import re
import os
from csle_common.envs_model.config.generator.env_info import EnvInfo
from csle_common.dao.container_config.containers_config import ContainersConfig
from csle_common.util.experiments_util import util
from csle_common.envs_model.config.generator.container_generator import ContainerGenerator
from csle_common.dao.container_config.container_network import ContainerNetwork
import csle_common.constants.constants as constants


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
            print("Stopping container: {}".format(c.name))
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
            print(f"Removing container: {c.name}")
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
                                                not in ",".join(x.attrs[constants.DOCKER.REPO_TAGS]), images)))
        base_images = list(filter(lambda x: (constants.DOCKER.BASE_CONTAINER_TYPE
                                             in ",".join(x.attrs[constants.DOCKER.REPO_TAGS]), images)))
        non_os_base_images = list(filter(lambda x: not
        (constants.OS.UBUNTU in ",".join(x.attrs[constants.DOCKER.REPO_TAGS])
         or constants.OS.KALI in ",".join(x.attrs[constants.DOCKER.REPO_TAGS])),
                                         base_images))
        os_base_images = list(filter(lambda x: constants.OS.UBUNTU in ",".join(x.attrs[constants.DOCKER.REPO_TAGS])
                                               or constants.OS.KALI in ",".join(x.attrs[constants.DOCKER.REPO_TAGS]),
                                     base_images))
        for img in non_base_images:
            print("Removing image: {}".format(img.attrs[constants.DOCKER.REPO_TAGS]))
            client_1.images.remove(image=img.attrs[constants.DOCKER.REPO_TAGS][0], force=True)
        for img in non_os_base_images:
            print("Removing image: {}".format(img.attrs[constants.DOCKER.REPO_TAGS]))
            client_1.images.remove(image=img.attrs[constants.DOCKER.REPO_TAGS][0], force=True)
        for img in os_base_images:
            print("Removing image: {}".format(img.attrs[constants.DOCKER.REPO_TAGS]))
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
                                                 not in ",".join(x.attrs[constants.DOCKER.REPO_TAGS]), images)))
        base_images = list(filter(lambda x: (constants.DOCKER.BASE_CONTAINER_TYPE
                                             in ",".join(x.attrs[constants.DOCKER.REPO_TAGS]), images)))
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
    def list_all_images() -> List[str]:
        """
        A utility function for listing all csle images

        :return: a list of the csle images
        """
        client_1 = docker.from_env()
        images = client_1.images.list()
        images = list(filter(lambda x: constants.CSLE.NAME in ",".join(x.attrs[constants.DOCKER.REPO_TAGS]), images))
        images_names = list(map(lambda x: x.attrs[constants.DOCKER.REPO_TAGS][0], images))
        return images_names

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
    def run_container_config(containers_config: ContainersConfig, path: str = None) -> None:
        """
        Starts all containers with a given set of configurations

        :param containers_config: the container configurations
        :param path: the path where to store created artifacts
        :return: None
        """
        if path == None:
            path = util.default_output_dir()
        client_1 = docker.from_env()
        project = constants.CSLE.NAME
        ContainerGenerator.write_containers_config(containers_cfg=containers_config, path=path)
        for idx, c in enumerate(containers_config.containers):
            container = c.name
            version = c.version
            image = project + constants.COMMANDS.SLASH_DELIM + container + constants.COMMANDS.COLON_DELIM + version
            suffix = str(idx)
            name = project + constants.COMMANDS.DASH_DELIM + c.minigame + constants.COMMANDS.DASH_DELIM + container \
                   + suffix + constants.COMMANDS.DASH_DELIM + constants.CSLE.LEVEL + c.level
            labels = {}
            labels[constants.DOCKER.CONTAINER_CONFIG_DIR]=path
            labels[constants.DOCKER.CONTAINER_CONFIG_CFG]=path + constants.DOCKER.CONTAINER_CONFIG_CFG_PATH
            labels[constants.DOCKER.CONTAINER_CONFIG_FLAGS_CFG] = \
                path + constants.DOCKER.CONTAINER_CONFIG_FLAGS_CFG_PATH
            labels[constants.DOCKER.CONTAINER_CONFIG_TOPOLOGY_CFG] = \
                path + constants.DOCKER.CONTAINER_CONFIG_TOPOLOGY_CFG_PATH
            labels[constants.DOCKER.CONTAINER_CONFIG_USERS_CFG] = \
                path + constants.DOCKER.CONTAINER_CONFIG_USERS_CFG_PATH
            labels[constants.DOCKER.CONTAINER_CONFIG_VULNERABILITIES_CFG] = \
                path + constants.DOCKER.CONTAINER_CONFIG_VULNERABILITIES_CFG_PATH
            labels[constants.DOCKER.CONTAINER_CONFIG_TRAFFIC_CFG] = \
                path + constants.DOCKER.CONTAINER_CONFIG_TRAFFIC_CFG_PATH
            print("Running container: {}".format(name))
            client_1.containers.run(image=image, name=name, hostname=name,
                                    detach=True, tty=True, network=c.internal_network, labels=labels,
                                    publish_all_ports=True, cap_add=[constants.DOCKER.NET_ADMIN])

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
            print("Starting container: {}".format(c.name))
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
    def list_all_running_containers() -> List[str]:
        """
        Lists all running csle containers

        :return: a list of the names of the running containers
        """
        parsed_envs = EnvInfo.parse_env_infos()
        container_name_image_ip = []
        for env in parsed_envs:
            container_name_image_ip = container_name_image_ip + list(map(lambda x: (x.name, x.image_name, x.ip), env.containers))
        return container_name_image_ip

    @staticmethod
    def list_running_emulations() -> List[str]:
        parsed_envs = EnvInfo.parse_env_infos()
        emulation_names = set()
        for env in parsed_envs:
            emulation_names.add(env.name)
        return list(emulation_names)

    @staticmethod
    def list_all_stopped_containers() -> List[str]:
        """
        Stops all stopped csle containers

        :return: a list of the stopped containers
        """
        client_1 = docker.from_env()
        client2 = docker.APIClient(base_url=constants.DOCKER.UNIX_DOCKER_SOCK_URL)
        parsed_stopped_containers = EnvInfo.parse_stopped_containers(client_1=client_1, client2=client2)
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
            container_name = f"{constants.CSLE.NAME}-{constants.CSLE.CTF_MINIGAME}-{c.name}{c.suffix}-" \
                             f"{constants.CSLE.LEVEL}{c.level}"
            # Disconnect from none
            cmd = f"docker network disconnect none {container_name}"
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)

            # Wait a few seconds before connecting
            time.sleep(2)

            for ip_net in c.ips_and_networks:
                ip, net = ip_net
                cmd = f"{constants.DOCKER.NETWORK_CONNECT} --ip {ip} {net.name} " \
                      f"{container_name}"
                print(f"Connecting container:{container_name} to network:{net.name} with ip: {ip}")
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
            print(f"Creating network: {name}, subnetmask: {subnetmask}")
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
                print(f"Removing network: {net.name}")
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
                print(f"Removing network: {net.name}")
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
            print(f"Removing network:{net.name}")
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
            print(names)
        elif cmd == constants.MANAGEMENT.LIST_RUNNING:
            names = ContainerManager.list_all_running_containers()
            print(names)
        elif cmd == constants.MANAGEMENT.LIST_IMAGES:
            names = ContainerManager.list_all_images()
            print(names)
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
            print(networks)
        elif cmd == constants.MANAGEMENT.RM_NETWORKS:
            ContainerManager.rm_all_networks()
        else:
            raise ValueError("Command: {} not recognized".format(cmd))
