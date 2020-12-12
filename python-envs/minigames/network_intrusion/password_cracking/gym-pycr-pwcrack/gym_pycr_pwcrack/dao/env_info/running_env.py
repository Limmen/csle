from typing import List
import jsonpickle
import json
from gym_pycr_pwcrack.dao.env_info.running_env_container import RunningEnvContainer
from gym_pycr_pwcrack.dao.container_config.containers_config import ContainersConfig
from gym_pycr_pwcrack.dao.container_config.users_config import UsersConfig
from gym_pycr_pwcrack.dao.container_config.flags_config import FlagsConfig
from gym_pycr_pwcrack.dao.container_config.vulnerabilities_config import VulnerabilitiesConfig
from gym_pycr_pwcrack.dao.container_config.topology import Topology

class RunningEnv:

    def __init__(self, containers: List[RunningEnvContainer], name: str, subnet_prefix: str, minigame :str, id: int,
                 subnet_mask : str, level: str, containers_config: ContainersConfig, users_config: UsersConfig,
                 flags_config: FlagsConfig, vulnerabilities_config: VulnerabilitiesConfig,
                 topology_config: Topology):
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


    def to_dict(self):
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
        return d