from typing import List
import threading
import docker
from pycr_common.dao.env_info.env_container import EnvContainer
from pycr_common.envs_model.config.generator.env_info import EnvInfo
from pycr_common.envs_model.logic.emulation.util.common.docker_stats_util import DockerStatsUtil
import pycr_common.constants.constants as constants


class DockerStatsThread(threading.Thread):
    """
    Thread that collects performance statistics of Docker containers
    """

    def __init__(self, jumphost_ip: str = None):
        threading.Thread.__init__(self)
        self.jumphost_ip = jumphost_ip
        if jumphost_ip is not None:
            self.client1 = docker.DockerClient(base_url=constants.DOCKER.SSH_PREFIX + jumphost_ip)
            self.client2 = docker.APIClient(base_url=constants.DOCKER.SSH_PREFIX + jumphost_ip)
        else:
            self.client1 = docker.from_env()
            self.client2 = docker.APIClient(base_url=constants.DOCKER.UNIX_DOCKER_SOCK_URL)

        self.containers = EnvInfo.parse_running_containers(client1=self.client1, client2=self.client2)

        streams = []
        for container in self.containers:
            stream = container.container_handle.stats(decode=True, stream=True)
            streams.append((stream, container))
        self.streams = streams

    def run(self):
        while True:
            for stream, container in self.streams:
                stats_dict = next(stream)
                parsed_stats = DockerStatsUtil.parse_stats(stats_dict, container)
                print(parsed_stats)


