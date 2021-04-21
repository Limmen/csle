from typing import List
import docker
from gym_pycr_ctf.envs_model.config.generator.env_info import EnvInfo
from gym_pycr_ctf.dao.container_config.containers_config import ContainersConfig
from gym_pycr_ctf.util.experiments_util import util
from gym_pycr_ctf.envs_model.config.generator.container_generator import ContainerGenerator
from gym_pycr_ctf.envs_model.config.generator.env_config_generator import EnvConfigGenerator


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
        containers = list(filter(lambda x: "pycr" in x.name, containers))
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
        containers = list(filter(lambda x: "pycr" in x.name and x.status == "exited" or x.status == "created", containers))
        for c in containers:
            print("Removing container: {}".format(c.name))
            c.remove()

    @staticmethod
    def rm_all_images() -> None:
        """
        A utility function for removing all pycr images

        :return: None
        """
        client1 = docker.from_env()
        images = client1.images.list()
        images = list(filter(lambda x: "pycr" in ",".join(x.attrs["RepoTags"]), images))
        non_base_images = list(filter(lambda x: "base" not in ",".join(x.attrs["RepoTags"]), images))
        base_images = list(filter(lambda x: "base" in ",".join(x.attrs["RepoTags"]), images))
        non_os_base_images = list(filter(lambda x: not ("ubuntu" in ",".join(x.attrs["RepoTags"]) or "kali" in ",".join(x.attrs["RepoTags"])), base_images))
        os_base_images = list(filter(lambda x: "ubuntu" in ",".join(x.attrs["RepoTags"]) or "kali" in ",".join(x.attrs["RepoTags"]), base_images))
        for img in non_base_images:
            print("Removing image: {}".format(img.attrs["RepoTags"]))
            client1.images.remove(image=img.attrs["RepoTags"][0], force=True)
        for img in non_os_base_images:
            print("Removing image: {}".format(img.attrs["RepoTags"]))
            client1.images.remove(image=img.attrs["RepoTags"][0], force=True)
        for img in os_base_images:
            print("Removing image: {}".format(img.attrs["RepoTags"]))
            client1.images.remove(image=img.attrs["RepoTags"][0], force=True)

    @staticmethod
    def list_all_images() -> List[str]:
        """
        A utility function for listing all pycr images

        :return: a list of the pycr images
        """
        client1 = docker.from_env()
        images = client1.images.list()
        images = list(filter(lambda x: "pycr" in ",".join(x.attrs["RepoTags"]), images))
        images_names = list(map(lambda x: x.attrs["RepoTags"][0], images))
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
        project = "pycr"
        ContainerGenerator.write_containers_config(containers_config=containers_config, path=path)
        for idx, c in enumerate(containers_config.containers):
            container = c.name
            version = c.version
            image = project + "/" + container + ":" + version
            suffix = str(idx)
            name = project + "-" + c.minigame + "-" + container + suffix + "-level" + c.level
            labels = {}
            labels["dir"]=path
            labels["containers_cfg"]=path + "/containers.json"
            labels["flags_cfg"] = path + "/flags.json"
            labels["topology_cfg"] = path + "/topology.json"
            labels["users_cfg"] = path + "/users.json"
            labels["vulnerabilities_cfg"] = path + "/vulnerabilities.json"
            print("Running container: {}".format(name))
            client1.containers.run(image=image, name=name, detach=True, tty=True, network=c.network, labels=labels,
                                   publish_all_ports=True, cap_add=["NET_ADMIN"])

    @staticmethod
    def start_all_stopped_containers() -> None:
        """
        Starts all stopped pycr containers

        :return: None
        """
        client1 = docker.from_env()
        containers = client1.containers.list(all=True)
        containers = list(filter(lambda x: "pycr" in x.name and x.status == "exited" or x.status == "created", containers))
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
        client2 = docker.APIClient(base_url='unix://var/run/docker.sock')
        parsed_stopped_containers = EnvInfo.parse_stopped_containers(client1=client1, client2=client2)
        container_names = list(map(lambda x: x.name, parsed_stopped_containers))
        return container_names

    @staticmethod
    def run_command(cmd: str) -> None:
        """
        Runs a container management command

        :param cmd: the command to run
        :return:
        """

        if cmd == "list_stopped":
            names = ContainerManager.list_all_stopped_containers()
            print(names)
        elif cmd == "list_running":
            names = ContainerManager.list_all_running_containers()
            print(names)
        elif cmd == "list_images":
            names = ContainerManager.list_all_images()
            print(names)
        elif cmd == "stop_running":
            ContainerManager.stop_all_running_containers()
        elif cmd == "rm_stopped":
            ContainerManager.rm_all_stopped_containers()
        elif cmd == "rm_images":
            ContainerManager.rm_all_images()
        elif cmd == "start_stopped":
            ContainerManager.start_all_stopped_containers()
        elif cmd == "list_networks":
            networks = ContainerManager.list_all_networks()
            print(networks)
        else:
            raise ValueError("Command: {} not recognized".format(cmd))


if __name__ == '__main__':
    ContainerManager.rm_all_images()