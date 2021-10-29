from typing import List
import docker
from pycr_common.envs_model.config.generator.env_info import EnvInfo
from pycr_common.dao.container_config.containers_config import ContainersConfig
from pycr_common.util.experiments_util import util
from pycr_common.envs_model.config.generator.container_generator import ContainerGenerator
from pycr_common.envs_model.config.generator.env_config_generator import EnvConfigGenerator
import pycr_common.constants.constants as constants


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
        client1 = docker.from_env()
        containers = client1.containers.list()
        containers = list(filter(lambda x: constants.OS.KALI in x.name, containers))
        for c in containers:
            print("Stopping container: {}".format(c.name))
            c.stop()

    @staticmethod
    def rm_all_stopped_containers() -> None:
        """
        A utility function for removing all stopped containers

        :return: None
        """
        client1 = docker.from_env()
        containers = client1.containers.list(all=True)
        containers = list(filter(lambda x: (constants.PYCR.NAME in x.name
                                           and x.status == constants.DOCKER.CONTAINER_EXIT_STATUS
                                           or x.status == constants.DOCKER.CONTAINER_CREATED_STATUS), containers))
        for c in containers:
            print(f"Removing container: {c.name}")
            c.remove()

    @staticmethod
    def rm_all_images() -> None:
        """
        A utility function for removing all pycr images

        :return: None
        """
        client1 = docker.from_env()
        images = client1.images.list()
        images = list(filter(lambda x: constants.OS.KALI in ",".join(x.attrs[constants.DOCKER.REPO_TAGS]), images))
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
            client1.images.remove(image=img.attrs[constants.DOCKER.REPO_TAGS][0], force=True)
        for img in non_os_base_images:
            print("Removing image: {}".format(img.attrs[constants.DOCKER.REPO_TAGS]))
            client1.images.remove(image=img.attrs[constants.DOCKER.REPO_TAGS][0], force=True)
        for img in os_base_images:
            print("Removing image: {}".format(img.attrs[constants.DOCKER.REPO_TAGS]))
            client1.images.remove(image=img.attrs[constants.DOCKER.REPO_TAGS][0], force=True)

    @staticmethod
    def list_all_images() -> List[str]:
        """
        A utility function for listing all pycr images

        :return: a list of the pycr images
        """
        client1 = docker.from_env()
        images = client1.images.list()
        images = list(filter(lambda x: constants.PYCR.NAME in ",".join(x.attrs[constants.DOCKER.REPO_TAGS]), images))
        images_names = list(map(lambda x: x.attrs[constants.DOCKER.REPO_TAGS][0], images))
        return images_names

    @staticmethod
    def list_all_networks() -> List[str]:
        """
        A utility function for listing all pycr networks

        :return: a list of the networks
        """
        networks, network_ids = EnvConfigGenerator.list_docker_networks()
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
        client1 = docker.from_env()
        project = constants.PYCR.NAME
        ContainerGenerator.write_containers_config(containers_config=containers_config, path=path)
        for idx, c in enumerate(containers_config.containers):
            container = c.name
            version = c.version
            image = project + constants.COMMANDS.SLASH_DELIM + container + constants.COMMANDS.COLON_DELIM + version
            suffix = str(idx)
            name = project + constants.COMMANDS.DASH_DELIM + c.minigame + constants.COMMANDS.DASH_DELIM + container \
                   + suffix + constants.COMMANDS.DASH_DELIM + constants.PYCR.LEVEL + c.level
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
            client1.containers.run(image=image, name=name, hostname=name,
                                   detach=True, tty=True, network=c.network, labels=labels,
                                   publish_all_ports=True, cap_add=[constants.DOCKER.NET_ADMIN])

    @staticmethod
    def start_all_stopped_containers() -> None:
        """
        Starts all stopped pycr containers

        :return: None
        """
        client1 = docker.from_env()
        containers = client1.containers.list(all=True)
        containers = list(filter(lambda x: (constants.PYCR.NAME in x.name
                                           and x.status == constants.DOCKER.CONTAINER_EXIT_STATUS
                                           or x.status == constants.DOCKER.CONTAINER_CREATED_STATUS), containers))
        for c in containers:
            print("Starting container: {}".format(c.name))
            c.start()

    @staticmethod
    def list_all_running_containers() -> List[str]:
        """
        Lists all running pycr containers

        :return: a list of the names of the running containers
        """
        parsed_envs = EnvInfo.parse_env_infos()
        container_names = []
        for env in parsed_envs:
            container_names = container_names + list(map(lambda x: x.name, env.containers))
        return container_names

    @staticmethod
    def list_all_stopped_containers() -> List[str]:
        """
        Stops all stopped pycr containers

        :return: a list of the stopped containers
        """
        client1 = docker.from_env()
        client2 = docker.APIClient(base_url=constants.DOCKER.UNIX_DOCKER_SOCK_URL)
        parsed_stopped_containers = EnvInfo.parse_stopped_containers(client1=client1, client2=client2)
        container_names = list(map(lambda x: x.name, parsed_stopped_containers))
        return container_names

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
        else:
            raise ValueError("Command: {} not recognized".format(cmd))


if __name__ == '__main__':
    ContainerManager.rm_all_images()