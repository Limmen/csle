from typing import List, Union
import docker
from docker.models.containers import Container
import os
import json
from csle_common.dao.docker.docker_container_metadata import DockerContainerMetadata
from csle_common.dao.docker.docker_env_metadata import DockerEnvMetadata
from csle_common.metastore.metastore_facade import MetastoreFacade
import csle_common.constants.constants as constants


class DockerUtil:
    """
    Utility class for extracting information from running emulation environments
    """

    @staticmethod
    def parse_runnning_emulation_infos() -> List[DockerEnvMetadata]:
        """
        Queries docker to get a list of all running emulation environments

        :return: a list of environment DTOs
        """
        client_1: docker.DockerClient = docker.from_env()
        client_2: docker.APIClient = docker.APIClient(base_url=constants.DOCKER.UNIX_DOCKER_SOCK_URL)
        parsed_containers = DockerUtil.parse_running_containers(client_1=client_1, client_2=client_2)
        emulations: List[str] = list(set(list(map(lambda x: x.emulation, filter(lambda x: x is not None,
                                                                                parsed_containers)))))
        parsed_envs = DockerUtil.parse_running_emulation_envs(emulations=emulations, containers=parsed_containers)
        return parsed_envs

    @staticmethod
    def get_container_hex_id(name: str) -> Union[str, None]:
        """
        Queries the docker engine for the id of a container with a given name

        :return: the id
        """
        client_1: docker.DockerClient = docker.from_env()
        client_2: docker.APIClient = docker.APIClient(base_url=constants.DOCKER.UNIX_DOCKER_SOCK_URL)
        containers: List[DockerContainerMetadata] = DockerUtil.parse_running_containers(client_1=client_1,
                                                                                        client_2=client_2)
        for container in containers:
            if container.name == name:
                return container.id
        return None

    @staticmethod
    def parse_running_containers(client_1: docker.DockerClient, client_2: docker.APIClient) \
            -> List[DockerContainerMetadata]:
        """
        Queries docker to get a list of all running containers

        :param client_1: docker client 1
        :param client_2:  docker client 2
        :return: list of parsed running containers
        """
        containers: List[Container] = client_1.containers.list()
        parsed_containers = DockerUtil.parse_containers(containers=containers, client2=client_2)
        return parsed_containers

    @staticmethod
    def parse_stopped_containers(client_1: docker.DockerClient, client2: docker.APIClient) \
            -> List[DockerContainerMetadata]:
        """
        Queries docker to get a list of all stopped csle containers

        :param client_1: docker client 1
        :param client2: docker client 2
        :return: list of parsed containers
        """
        containers: List[docker.models.containers.Container] = client_1.containers.list(all=True)
        stopped_containers: List[docker.models.containers.Container] = list(filter(
            lambda x: (x.status == constants.DOCKER.CONTAINER_EXIT_STATUS
                       or x.status == constants.DOCKER.CONTAINER_CREATED_STATUS), containers))
        parsed_containers = DockerUtil.parse_containers(containers=stopped_containers, client2=client2)
        return parsed_containers

    @staticmethod
    def parse_running_emulation_envs(emulations: List[str], containers: List[DockerContainerMetadata]) \
            -> List[DockerEnvMetadata]:
        """
        Queries docker to get a list of all active emulation environments

        :param emulations: list of csle emulations
        :param containers: list of running csle containers
        :return: list of parsed emulation environments
        """
        parsed_envs = []
        for em in emulations:
            em_containers = list(filter(lambda x: x.emulation == em, containers))
            subnet_prefix = constants.COMMANDS.DOT_DELIM.join(em_containers[0].ip.rsplit(
                constants.COMMANDS.DOT_DELIM)[0:-1])
            subnet_mask = subnet_prefix + constants.COMMANDS.SLASH_DELIM + str(em_containers[0].ip_prefix_len)

            config = None
            em_record = MetastoreFacade.get_emulation_by_name(name=em)
            if em_record is not None:
                config = em_record

            p_env = DockerEnvMetadata(containers=em_containers, name=em, subnet_prefix=subnet_mask,
                                      subnet_mask=subnet_mask, level=em_containers[0].level, config=config,
                                      kafka_config=None)
            parsed_envs.append(p_env)
        return parsed_envs

    @staticmethod
    def parse_containers(containers: List[docker.models.containers.Container], client2: docker.APIClient) \
            -> List[DockerContainerMetadata]:
        """
        Queries docker to get a list of running or stopped csle containers

        :param containers: list of containers to parse
        :param client2: docker client
        :return: List of parsed container DTOs
        """
        parsed_containers = []
        for c in containers:
            if constants.CONTAINER_IMAGES.CSLE_PREFIX in c.name:
                name_parts = c.name.split("-")
                container_name_2 = name_parts[0]
                level = name_parts[1]
                inspect_info = client2.inspect_container(c.id)
                net = None
                if len(list(inspect_info[constants.DOCKER.NETWORK_SETTINGS][constants.DOCKER.NETWORKS].keys())) > 0:
                    net = list(inspect_info[constants.DOCKER.NETWORK_SETTINGS][constants.DOCKER.NETWORKS].keys())[0]
                labels = c.labels
                config_path = ""
                dir_path = ""
                emulation = ""
                kafka_config = ""
                if constants.DOCKER.CFG in labels:
                    config_path = labels[constants.DOCKER.CFG]
                if constants.DOCKER.CONTAINER_CONFIG_DIR in labels:
                    dir_path = labels[constants.DOCKER.CONTAINER_CONFIG_DIR]
                if constants.DOCKER.EMULATION in labels:
                    emulation = labels[constants.DOCKER.EMULATION]
                if constants.DOCKER.KAFKA_CONFIG in labels:
                    kafka_config = labels[constants.DOCKER.KAFKA_CONFIG]
                ip = ""
                network_id = -1
                gateway = ""
                mac = ""
                ip_prefix_len = 0
                if net is not None:
                    ip = inspect_info[constants.DOCKER.NETWORK_SETTINGS][constants.DOCKER.NETWORKS][net][
                        constants.DOCKER.IP_ADDRESS_INFO]
                    network_id = inspect_info[constants.DOCKER.NETWORK_SETTINGS][constants.DOCKER.NETWORKS][net][
                        constants.DOCKER.NETWORK_ID_INFO]
                    gateway = inspect_info[constants.DOCKER.NETWORK_SETTINGS][constants.DOCKER.NETWORKS][net][
                        constants.DOCKER.GATEWAY_INFO]
                    mac = inspect_info[constants.DOCKER.NETWORK_SETTINGS][constants.DOCKER.NETWORKS][net][
                        constants.DOCKER.MAC_ADDRESS_INFO]
                    ip_prefix_len = inspect_info[constants.DOCKER.NETWORK_SETTINGS][constants.DOCKER.NETWORKS][net][
                        constants.DOCKER.IP_PREFIX_LEN_INFO]
                if net is None:
                    net_str = ""
                else:
                    net_str = net
                parsed_c = DockerContainerMetadata(
                    name=c.name, status=c.status, short_id=c.short_id, image_short_id=c.image.short_id,
                    image_tags=c.image.tags, id=c.id,
                    created=inspect_info[constants.DOCKER.CREATED_INFO],
                    ip=ip, network_id=network_id, gateway=gateway, mac=mac, ip_prefix_len=ip_prefix_len,
                    name2=container_name_2, level=level,
                    hostname=inspect_info[constants.DOCKER.CONFIG][constants.DOCKER.HOSTNAME_INFO],
                    image_name=inspect_info[constants.DOCKER.CONFIG][constants.DOCKER.IMAGE],
                    net=net_str, dir=dir_path, config_path=config_path,
                    container_handle=c, emulation=emulation, kafka_container=kafka_config)
                parsed_containers.append(parsed_c)
        return parsed_containers

    @staticmethod
    def get_docker_gw_bridge_ip(container_id: str) -> str:
        """
        Gets the docker gw bridge ip of a container

        :param container_id: the id of the container
        :return: the ip in the gw bridge network
        """
        cmd = constants.DOCKER.INSPECT_DOCKER_GWBRIDGE
        stream = os.popen(cmd)
        json_output = stream.read()
        docker_gw_bridge_info = json.loads(json_output)[0]
        containers = docker_gw_bridge_info[constants.DOCKER.CONTAINERS_KEY]
        if container_id in containers:
            container = containers[container_id]
            ip = container[constants.DOCKER.IPV4_KEY]
            if isinstance(ip, str):
                ip = ip.split("/")[0]
                return ip
        raise ValueError(f"The container with id:{container_id} does not have an IP in the docker gw bridge network. "
                         f"Containers: {containers}")
