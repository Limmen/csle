from typing import List, Tuple
import io
import random
import os
import re
import json
import shutil
from csle_common.dao.emulation_config.vulnerability_type import VulnType
from csle_common.domain_randomization.vuln_generator import VulnerabilityGenerator
from csle_common.domain_randomization.container_generator import ContainerGenerator
from csle_common.dao.emulation_config.containers_config import ContainersConfig
from csle_common.dao.emulation_config.resources_config import ResourcesConfig
from csle_common.dao.emulation_config.node_resources_config import NodeResourcesConfig
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.dao.emulation_config.emulation_env_generation_config import EmulationEnvGenerationConfig
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.domain_randomization.flags_generator import FlagsGenerator
from csle_common.domain_randomization.users_generator import UsersGenerator
from csle_common.domain_randomization.topology_generator import TopologyGenerator
from csle_common.domain_randomization.resource_constraints_generator import ResourceConstraintsGenerator
from csle_common.domain_randomization.traffic_generator import TrafficGenerator
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.controllers.emulation_env_manager import EmulationEnvManager
import csle_common.constants.constants as constants


class EmulationEnvConfigGenerator:
    """
    A Utility Class for generating emulation environments from given configurations
    """

    @staticmethod
    def generate_envs(container_env_config: EmulationEnvGenerationConfig, num_envs: int, name: str,
                      start_idx : int = 0) -> List[EmulationEnvConfig]:
        """
        Generates a <num_envs> number of emulation environments

        :param container_env_config: the environment configuration
        :param num_envs: the number of environments
        :param name: the name of the emulation environment to create
        :param start_idx: the start idx of the first environment to create
        :return: the blacklist of subnet ids
        """
        created_emulations = []
        for i in range(num_envs):
            container_env_config_c = container_env_config.copy()
            em_name = f"{name}_{start_idx + i}"
            created_emulation=  EmulationEnvConfigGenerator.create_env(container_env_config_c, name=em_name)
            created_emulations.append(created_emulation)
        return created_emulations

    @staticmethod
    def generate(container_env_config: EmulationEnvGenerationConfig, name: str) -> EmulationEnvConfig:
        """
        Generates a new emulation environment (creates the artifacts)

        :param container_env_config: configuration of the new environment
        :param name: the name of the emulation to create
        :return: the configuration of the generated emulation environment
        """

        topology, agent_ip, router_ip, vulnerable_nodes = \
            TopologyGenerator.generate(num_nodes=container_env_config.num_nodes,
                                       subnet_prefix=container_env_config.subnet_prefix,
                                       subnet_id = container_env_config.subnet_id)
        vulnerabilities = VulnerabilityGenerator.generate(
            topology=topology, vulnerable_nodes = vulnerable_nodes, agent_ip=agent_ip,
            subnet_prefix=container_env_config.subnet_prefix,
            num_flags=container_env_config.num_flags,
            access_vuln_types=[VulnType.WEAK_PW, VulnType.RCE, VulnType.SQL_INJECTION, VulnType.PRIVILEGE_ESCALATION],
            router_ip=router_ip)

        users = UsersGenerator.generate(max_num_users=container_env_config.max_num_users,
                                        topology=topology, agent_ip=agent_ip)
        flags = FlagsGenerator.generate(vuln_cfg=vulnerabilities, num_flags=container_env_config.num_flags)
        containers = ContainerGenerator.generate(
            topology=topology, vuln_cfg=vulnerabilities,
            container_pool=container_env_config.container_pool,
            gw_vuln_compatible_containers=container_env_config.gw_vuln_compatible_containers,
            pw_vuln_compatible_containers=container_env_config.pw_vuln_compatible_containers,
            subnet_id=container_env_config.subnet_id, num_flags=container_env_config.num_flags,
            agent_ip=agent_ip, router_ip=router_ip, agent_containers=container_env_config.agent_containers,
            router_containers=container_env_config.router_containers,
            subnet_prefix=container_env_config.subnet_prefix, vulnerable_nodes = vulnerable_nodes)
        resources = ResourceConstraintsGenerator.generate(containers_config=containers, min_cpus=1, max_cpus=1,
                                                          min_mem_G=1, max_mem_G=2)

        agent_container_names = list(map(lambda x: x[0], container_env_config.agent_containers))
        gateway_container_names = list(map(lambda x: x[0], container_env_config.router_containers))
        traffic = TrafficGenerator.generate(topology=topology, containers_config=containers,
                                            agent_container_names=agent_container_names,
                                            router_container_names = gateway_container_names
                                            )
        emulation_env_config = EmulationEnvConfig(
            name=name, topology_config=topology, containers_config = containers, vuln_config=vulnerabilities,
            users_config = users, flags_config = flags, traffic_config = traffic, resources_config=resources,
            services_config=None, log_sink_config=None)
        return emulation_env_config

    @staticmethod
    def get_free_network_ids(emulations: List[EmulationEnvConfig]) -> List[int]:
        """
        Returns a list of free network ids

        :param emulations: list of installed emulations
        :return: list of free network ids
        """
        network_ids = list(range(2,254))
        occupied_network_ids = []
        for em in emulations:
            for net in em.containers_config.networks:
                net_id = net.subnet_prefix.split(".")[-1]
                occupied_network_ids.append(net_id)
        free_network_ids = []
        for nid in network_ids:
            if nid not in occupied_network_ids:
                free_network_ids.append(int(nid))
        return free_network_ids

    @staticmethod
    def list_running_containers() -> List[str]:
        """
        Lists the running containers

        :return: names of the running containers
        """
        cmd = constants.DOCKER.LIST_RUNNING_CONTAINERS_CMD
        stream = os.popen(cmd)
        running_containers = stream.read()
        running_containers = running_containers.split("\n")
        running_containers = list(filter(lambda x: x!= "", running_containers))
        return running_containers

    @staticmethod
    def find_networks_in_use(containers: List[str]) -> Tuple[List[str], List[int]]:
        """
        Utility function for querying Docker to see which networks are currently in use

        :param containers: the list of containers to check the networks for
        :return: (list of networks in use, list of network ids in use
        """
        networks_in_use = []
        network_ids_in_use = []
        for c in containers:
            cmd = constants.DOCKER.INSPECT_CONTAINER_CONFIG_CMD + c + " -f '{{json .NetworkSettings.Networks }}'"
            stream = os.popen(cmd)
            network_info = stream.read()
            network_info = json.loads(network_info)
            for k in network_info.keys():
                if re.match(rf"{constants.CSLE.CSLE_NETWORK_PREFIX}_\d", k):
                   networks_in_use.append(k)
                   network_ids_in_use.append(int(k.replace(f"{constants.CSLE.CSLE_NETWORK_PREFIX}_", "")))

        return networks_in_use, network_ids_in_use

    @staticmethod
    def create_container_dirs(container_config: ContainersConfig, resources_config: ResourcesConfig,
                              emulation_name: str,
                              path: str = None,
                              create_folder_makefile: bool = True) -> None:
        """
        Utility function for creating the container directories with the start scripts

        :param container_config: the configuration of the containers
        :param resources_config: the resources config of the containers
        :param path: the path where to create the directories
        :param create_folder_makefile: a boolean flag indicating whether to create a Makefile for the folder or not
        :param emulation_name: the name of the emulation
        :return: None
        """
        containers_folders_dir = ExperimentUtil.default_containers_folders_path(out_dir=path)
        if not os.path.exists(containers_folders_dir):
            os.makedirs(containers_folders_dir)

        makefile_template_str = constants.DOCKER.CONTAINER_MAKEFILE_TEMPLATE_STR

        container_names = []
        for c in container_config.containers:
            ips = c.get_ips()
            container_resources : NodeResourcesConfig = None
            for r in resources_config.node_resources_configurations:
                for ip_net_resources in r.ips_and_network_configs:
                    ip, net_resources = ip_net_resources
                    if ip in ips:
                        container_resources : NodeResourcesConfig = r
                        break
            if container_resources is None:
                raise ValueError(f"Container resources not found for container with ips:{ips}, "
                                 f"resources:{resources_config}")

            c_dir = containers_folders_dir + "/" + c.name + c.suffix
            container_names.append(c.name + c.suffix)
            if not os.path.exists(c_dir):
                os.makedirs(c_dir)
                makefile_preamble = ""
                makefile_preamble = makefile_preamble + constants.MAKEFILE.PROJECT + "=csle\n"
                makefile_preamble = makefile_preamble + constants.MAKEFILE.EMULATION + "=" + emulation_name + "\n"
                makefile_preamble = makefile_preamble + constants.MAKEFILE.CONTAINER + "=" + c.name + "\n"
                makefile_preamble = makefile_preamble + constants.MAKEFILE.VERSION + "=" + c.version + "\n"
                makefile_preamble = makefile_preamble + constants.MAKEFILE.LEVEL + "=" + c.level + "\n"
                makefile_preamble = makefile_preamble + constants.MAKEFILE.DIR + "=" + path + "\n"
                makefile_preamble = makefile_preamble + constants.MAKEFILE.CFG + "=" + path + \
                                    constants.DOCKER.EMULATION_ENV_CFG_PATH + "\n"
                makefile_preamble = makefile_preamble + constants.MAKEFILE.RESTART_POLICY + "="+ c.restart_policy + "\n"
                makefile_preamble = makefile_preamble + constants.MAKEFILE.NUM_CPUS + "=" + \
                                    str(container_resources.num_cpus) + "\n"
                makefile_preamble = makefile_preamble + constants.MAKEFILE.MEMORY + "=" + \
                                    str(container_resources.available_memory_gb) + "G\n"
                makefile_preamble = makefile_preamble + constants.MAKEFILE.SUFFIX + "=" + c.suffix + "\n\n"

                makefile_str = makefile_preamble + makefile_template_str
                with io.open(c_dir + constants.DOCKER.MAKEFILE_PATH, 'w', encoding='utf-8') as f:
                    f.write(makefile_str)

        if create_folder_makefile:
            EmulationEnvConfigGenerator.create_makefile(container_names, path=path)

    @staticmethod
    def create_makefile(container_names, path: str = None) -> None:
        """
        Utility function for automatically generating the Makefile for managing a newly created emulation environment

        :param container_names: the names of the containers
        :param path: the path to where the Makefile will be stored
        :return: None
        """
        with io.open(ExperimentUtil.default_makefile_template_path(out_dir=path), 'r', encoding='utf-8') as f:
            makefile_template_str = f.read()

        makefile_template_str = makefile_template_str + constants.MANAGEMENT.RUN + ":\n"
        for c in container_names:
            makefile_template_str = makefile_template_str + "	cd containers/" + c + "/ && $(MAKE) run\n"

        makefile_template_str = makefile_template_str + "\n\n"
        makefile_template_str = makefile_template_str + constants.MANAGEMENT.STOP + ":\n"
        for c in container_names:
            makefile_template_str = makefile_template_str + "	cd containers/" + c + "/ && $(MAKE) stop\n"

        makefile_template_str = makefile_template_str + "\n\n"
        makefile_template_str = makefile_template_str + constants.MANAGEMENT.START + ":\n"
        for c in container_names:
            makefile_template_str = makefile_template_str + "	cd containers/" + c + "/ && $(MAKE) start\n"

        makefile_template_str = makefile_template_str + "\n\n"
        makefile_template_str = makefile_template_str + constants.MANAGEMENT.CLEAN + ":\n"
        for c in container_names:
            makefile_template_str = makefile_template_str + "	cd containers/" + c + "/ && $(MAKE) clean\n"
        makefile_template_str = makefile_template_str + "\n\n"
        with io.open(ExperimentUtil.default_makefile_path(out_dir=path), 'w', encoding='utf-8') as f:
            f.write(makefile_template_str)

    @staticmethod
    def cleanup_env_config(path: str = None) -> None:
        """
        A utility function for cleaning up the environment configuration

        :param path: the path to where the configuration is stored
        :return: None
        """
        # try:
        if os.path.exists(ExperimentUtil.default_users_path(out_dir=path)):
            os.remove(ExperimentUtil.default_users_path(out_dir=path))
        if os.path.exists(ExperimentUtil.default_topology_path(out_dir=path)):
            os.remove(ExperimentUtil.default_topology_path(out_dir=path))
        if os.path.exists(ExperimentUtil.default_flags_path(out_dir=path)):
            os.remove(ExperimentUtil.default_flags_path(out_dir=path))
        if os.path.exists(ExperimentUtil.default_vulnerabilities_path(out_dir=path)):
            os.remove(ExperimentUtil.default_vulnerabilities_path(out_dir=path))
        if os.path.exists(ExperimentUtil.default_containers_path(out_dir=path)):
            os.remove(ExperimentUtil.default_containers_path(out_dir=path))
        if os.path.exists(ExperimentUtil.default_containers_folders_path(out_dir=path)):
            shutil.rmtree(ExperimentUtil.default_containers_folders_path(out_dir=path))
        if os.path.exists(ExperimentUtil.default_traffic_path(out_dir=path)):
            os.remove(ExperimentUtil.default_traffic_path(out_dir=path))
        # except Exception as e:
        #     pass

    @staticmethod
    def cleanup_envs(path: str = None) -> None:
        """
        Utility function for cleaning up the artifacts of a created emulation environment

        :param path: the path where the emulation is created
        :return: None
        """
        if path == None:
            path = ExperimentUtil.default_output_dir()
        for f in os.listdir(path):
            if re.search("env_*", f):
                ExperimentUtil.rmtree(os.path.join(path, f))

    @staticmethod
    def get_env_dirs(path: str = None) -> List[str]:
        """
        Utility function for getting the directories of the emulation environment

        :param path: path to where the directories should be stored
        :return: A list of the directories
        """
        if path == None:
            path = ExperimentUtil.default_output_dir()
        env_dirs = []
        for f in os.listdir(path):
            if re.search("env_*", f):
                env_dirs.append(os.path.join(path, f))
        return env_dirs

    @staticmethod
    def get_all_envs_containers_config(path: str = None) -> List[ContainersConfig]:
        """
        Utility function for getting the configuration of all containers in the emulation environment

        :param path: the path to where the configuration should be stored
        :return: a list of container configurations
        """
        if path == None:
            path = ExperimentUtil.default_output_dir()
        env_dirs = EmulationEnvConfigGenerator.get_env_dirs(path)
        containers_configs = []
        for d in env_dirs:
            containers_configs.append(ExperimentUtil.read_containers_config(d + constants.DOCKER.CONTAINER_CONFIG_CFG_PATH))
        return containers_configs

    @staticmethod
    def config_exists(path: str = None) -> bool:
        """
        Checks whether a complete environment configuration exists in a given path or not

        :param path: the path to check
        :return: True if it exists, otherwise False
        """
        if not os.path.exists(ExperimentUtil.default_users_path(out_dir=path)):
            return False
        if not os.path.exists(ExperimentUtil.default_topology_path(out_dir=path)):
            return False
        if not os.path.exists(ExperimentUtil.default_flags_path(out_dir=path)):
            return False
        if not os.path.exists(ExperimentUtil.default_vulnerabilities_path(out_dir=path)):
            return False
        if not os.path.exists(ExperimentUtil.default_containers_path(out_dir=path)):
            return False
        if not os.path.exists(ExperimentUtil.default_containers_folders_path(out_dir=path)):
            return False
        if not os.path.exists(ExperimentUtil.default_makefile_path(out_dir=path)):
            return False
        if not os.path.exists(ExperimentUtil.default_traffic_path(out_dir=path)):
            return False

        return True

    @staticmethod
    def materialize_emulation_env_config(emulation_env_config: EmulationEnvConfig,
                    path: str = "", create_folder_makefile: bool = False) -> None:
        """
        Materializes the configuration to disk in a JSON format and creates container directories

        :param path: the path to materialize to
        :param create_folder_makefile: whether to create the folder makefile or not
        :return: None
        """
        if not os.path.exists(path+emulation_env_config.name):
            os.makedirs(path+emulation_env_config.name)

        if not os.path.exists(path + emulation_env_config.name + constants.COMMANDS.SLASH_DELIM + \
                              constants.DOCKER.EMULATION_ENV_CFG_PATH):
            ExperimentUtil.write_emulation_config_file(emulation_env_config, path + emulation_env_config.name
                                                       + constants.COMMANDS.SLASH_DELIM + \
                                                       constants.DOCKER.EMULATION_ENV_CFG_PATH)

        container_dirs_path = path + emulation_env_config.name + constants.COMMANDS.SLASH_DELIM + \
                              constants.DOCKER.CONTAINERS_DIR
        if not os.path.exists(container_dirs_path):
            EmulationEnvConfigGenerator.create_container_dirs(emulation_env_config.containers_config,
                                                              resources_config=emulation_env_config.resources_config,
                                                              path=path + emulation_env_config.name,
                                                              create_folder_makefile=create_folder_makefile,
                                                              emulation_name=emulation_env_config.name)


    @staticmethod
    def read_emulation_env_config(path: str = "") -> EmulationEnvConfig:
        """
        Reads the emulation env configuration from a json file

        :param path: the path to read
        :return: the parsed object
        """
        if path == "":
            path = ExperimentUtil.default_emulation_config_path(out_dir=ExperimentUtil.default_output_dir())
        return ExperimentUtil.read_emulation_env_config(path)


    @staticmethod
    def create_env(container_env_config: EmulationEnvGenerationConfig, name: str) -> EmulationEnvConfig:
        """
        Function that creates a new emulation environment given a configuration

        :param container_env_config: the configuration of the environment to create
        :param name: the name of the emulation to create
        :return: The configuration of the created emulation
        """
        emulations = MetastoreFacade.list_emulations()
        available_network_ids = EmulationEnvConfigGenerator.get_free_network_ids(emulations=emulations)
        container_env_config.subnet_id = available_network_ids[random.randint(0, len(available_network_ids) - 1)]
        container_env_config.num_nodes = random.randint(container_env_config.min_num_nodes,
                                                        container_env_config.max_num_nodes)
        container_env_config.subnet_prefix = container_env_config.subnet_prefix + str(container_env_config.subnet_id)
        container_env_config.num_flags = random.randint(container_env_config.min_num_flags,
                                                        min(container_env_config.max_num_flags,
                                                            container_env_config.num_nodes - 3))
        container_env_config.num_users = random.randint(container_env_config.min_num_users,
                                                        container_env_config.max_num_users)
        emulation_env_config = EmulationEnvConfigGenerator.generate(container_env_config, name=name)
        EmulationEnvManager.install_emulation(config=emulation_env_config)
        return emulation_env_config





