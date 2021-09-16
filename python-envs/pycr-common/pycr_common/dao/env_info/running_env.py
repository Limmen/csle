from typing import List
import jsonpickle
import json
from gym_pycr_ctf.dao.env_info.running_env_container import RunningEnvContainer
from pycr_common.dao.container_config.containers_config import ContainersConfig
from gym_pycr_ctf.dao.container_config.users_config import UsersConfig
from pycr_common.dao.container_config.flags_config import FlagsConfig
from gym_pycr_ctf.dao.container_config.vulnerabilities_config import VulnerabilitiesConfig
from gym_pycr_ctf.dao.container_config.topology import Topology
from gym_pycr_ctf.dao.container_config.traffic_config import TrafficConfig


class RunningEnv:
    """
    DTO Object representing a running environment
    """

    def __init__(self, containers: List[RunningEnvContainer], name: str, subnet_prefix: str, minigame :str, id: int,
                 subnet_mask : str, level: str, containers_config: ContainersConfig, users_config: UsersConfig,
                 flags_config: FlagsConfig, vulnerabilities_config: VulnerabilitiesConfig,
                 topology_config: Topology, traffic_config: TrafficConfig):
        """
        Intializes the DTO

        :param containers: the list of running containers
        :param name: the environment name
        :param subnet_prefix: the subnet prefix
        :param minigame: the minigame of the environment
        :param id: the id of the environment
        :param subnet_mask: the subnet mask
        :param level: the level of the environment
        :param containers_config: the configurations of the containers in the environment
        :param users_config: the configuration of the users in the environment
        :param flags_config: the configuration of the flags in the environment
        :param vulnerabilities_config: the configuration of the vulnerabilities in the environment
        :param topology_config: the configuration of the environment's topology
        :param traffic_config: the configuration of the environment's traffic generators
        """
        self.containers = containers
        self.name = name
        self.subnet_prefix=subnet_prefix
        self.minigame = minigame
        self.id=id
        self.subnet_mask = subnet_mask
        self.level = level
        self.containers_config = containers_config
        self.users_config = users_config
        self.flags_config = flags_config
        self.vulnerabilities_config = vulnerabilities_config
        self.topology_config = topology_config
        self.traffic_config = traffic_config

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["containers"] = list(map(lambda x: x.to_dict(), self.containers))
        d["name"] = self.name
        d["subnet_prefix"] = self.subnet_prefix
        d["minigame"] = self.minigame
        d["id"] = self.id
        d["subnet_mask"] = self.subnet_mask
        d["num_containers"] = len(self.containers)
        d["level"] = len(self.level)
        d["containers_config"] = json.loads(jsonpickle.encode(self.containers_config))
        d["users_config"] = json.loads(jsonpickle.encode(self.users_config))
        d["flags_config"] = json.loads(jsonpickle.encode(self.flags_config))
        d["vulnerabilities_config"] = json.loads(jsonpickle.encode(self.vulnerabilities_config))
        d["topology_config"] = json.loads(jsonpickle.encode(self.topology_config))
        d["traffic_config"] = json.loads(jsonpickle.encode(self.traffic_config))
        return d