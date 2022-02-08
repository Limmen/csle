from csle_common.dao.container_config.containers_config import ContainersConfig
from csle_common.dao.container_config.users_config import UsersConfig
from csle_common.dao.container_config.flags_config import FlagsConfig
from csle_common.dao.container_config.vulnerabilities_config import VulnerabilitiesConfig
from csle_common.dao.container_config.topology import Topology
from csle_common.dao.container_config.traffic_config import TrafficConfig
from csle_common.dao.container_config.resources_config import ResourcesConfig


class EmulationEnvConfig:
    """
    Class representing the configuration of an emulation
    """

    def __init__(self, name: str, containers_config: ContainersConfig, users_config: UsersConfig,
                 flags_config: FlagsConfig,
                 vuln_config: VulnerabilitiesConfig, topology_config: Topology, traffic_config: TrafficConfig,
                 resources_config: ResourcesConfig):
        """
        Initializes the object

        :param name: the name of the emulation
        :param containers_config: the containers configuration
        :param users_config: the users configuration
        :param flags_config: the flags configuration
        :param vuln_config: the vulnerabilities configuration
        :param topology_config: the topology configuration
        :param traffic_config: the traffic configuration
        :param resources_config: the resources configuration
        """
        self.name = name
        self.containers_config = containers_config
        self.users_config = users_config
        self.flags_config = flags_config
        self.vuln_config = vuln_config
        self.topology_config = topology_config
        self.traffic_config = traffic_config
        self.resources_config = resources_config


    def __str__(self) -> str:
        """
        :return:  a string representation of the object
        """
        return f"name: {self.name}, containers_config: {self.containers_config}, users_config: {self.users_config}, " \
               f"flags_config: {self.flags_config}, vuln_config: {self.vuln_config}, " \
               f"topology_config: {self.topology_config}, traffic_config: {self.traffic_config}, " \
               f"resources_config: {self.resources_config}"
