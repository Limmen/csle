import time
from typing import List, Tuple, Set
import io
import shutil
import random
import os
import re
import subprocess
import psycopg
import json
import jsonpickle
from csle_common.dao.container_config.vulnerability_type import VulnType
from csle_common.envs_model.config.generator.vuln_generator import VulnerabilityGenerator
from csle_common.envs_model.config.generator.container_generator import ContainerGenerator
from csle_common.dao.container_config.containers_config import ContainersConfig
from csle_common.dao.container_config.resources_config import ResourcesConfig
from csle_common.dao.container_config.node_resources_config import NodeResourcesConfig
from csle_common.dao.container_config.flags_config import FlagsConfig
from csle_common.util.experiments_util import util
from csle_common.dao.container_config.emulation_env_generation_config import EmulationEnvGenerationConfig
from csle_common.dao.container_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.container_config.log_sink_config import LogSinkConfig
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.config.generator.flags_generator import FlagsGenerator
from csle_common.envs_model.config.generator.container_manager import ContainerManager
from csle_common.envs_model.config.generator.log_sink_manager import LogSinkManager
from csle_common.envs_model.config.generator.users_generator import UsersGenerator
from csle_common.envs_model.config.generator.topology_generator import TopologyGenerator
from csle_common.envs_model.config.generator.resource_constraints_generator import ResourceConstraintsGenerator
from csle_common.envs_model.config.generator.traffic_generator import TrafficGenerator
from csle_common.envs_model.config.generator.metastore_facade import MetastoreFacade
import csle_common.constants.constants as constants


class EnvConfigGenerator:
    """
    A Utility Class for generating emulation environments from given configurations
    """

    @staticmethod
    def execute_env_cmd(path :str, cmd: str) -> None:
        """
        Utility function for executing make commands for an emulation

        :param path: the path to where the emulation config is stored
        :param cmd: the make command
        :return: None
        """
        env_dirs = EnvConfigGenerator.get_env_dirs(path=path)
        cmds = [constants.MANAGEMENT.CLEAN, constants.MANAGEMENT.CLEAN_CONFIG, constants.MANAGEMENT.GEN_CONFIG,
                constants.MANAGEMENT.APPLY_CONFIG, constants.MANAGEMENT.RUN, constants.MANAGEMENT.STOP,
                constants.MANAGEMENT.START, constants.MANAGEMENT.TOPOLOGY, constants.MANAGEMENT.USERS,
                constants.MANAGEMENT.FLAGS, constants.MANAGEMENT.VULN, constants.MANAGEMENT.ALL,
                constants.MANAGEMENT.CLEAN_FS_CACHE, constants.MANAGEMENT.TRAFFIC]
        if cmd in cmds:
            for dir in env_dirs:
                cmd_full = "make " + cmd
                subprocess.call(cmd_full, shell=True, cwd=dir)
        elif cmd == constants.MANAGEMENT.CLEAN_ENVS:
            EnvConfigGenerator.cleanup_envs(path=util.default_output_dir())

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
            created_emulation=  EnvConfigGenerator.create_env(container_env_config_c, name=em_name)
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
        emulation_env_config = EmulationEnvConfig(name=name,
            topology_config=topology, containers_config = containers, vuln_config=vulnerabilities,
            users_config = users, flags_config = flags, traffic_config = traffic, resources_config=resources)
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
    def create_env(container_env_config: EmulationEnvGenerationConfig, name: str) -> EmulationEnvConfig:
        """
        Function that creates a new emulation environment given a configuration

        :param container_env_config: the configuration of the environment to create
        :param name: the name of the emulation to create
        :return: The configuration of the created emulation
        """
        emulations = MetastoreFacade.list_emulations()
        available_network_ids = EnvConfigGenerator.get_free_network_ids(emulations=emulations)
        container_env_config.subnet_id = available_network_ids[random.randint(0, len(available_network_ids) - 1)]
        container_env_config.num_nodes = random.randint(container_env_config.min_num_nodes,
                                                        container_env_config.max_num_nodes)
        container_env_config.subnet_prefix = container_env_config.subnet_prefix + str(container_env_config.subnet_id)
        container_env_config.num_flags = random.randint(container_env_config.min_num_flags,
                                                        min(container_env_config.max_num_flags,
                                                            container_env_config.num_nodes - 3))
        container_env_config.num_users = random.randint(container_env_config.min_num_users,
                                                        container_env_config.max_num_users)
        emulation_env_config = EnvConfigGenerator.generate(container_env_config, name=name)
        EnvConfigGenerator.install_emulation(config=emulation_env_config)
        return emulation_env_config

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
        containers_folders_dir = util.default_containers_folders_path(out_dir=path)
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
                makefile_preamble = makefile_preamble + constants.MAKEFILE.MINIGAME + "=" + c.minigame + "\n"
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
            EnvConfigGenerator.create_makefile(container_names, path=path)

    @staticmethod
    def create_makefile(container_names, path: str = None) -> None:
        """
        Utility function for automatically generating the Makefile for managing a newly created emulation environment

        :param container_names: the names of the containers
        :param path: the path to where the Makefile will be stored
        :return: None
        """
        with io.open(util.default_makefile_template_path(out_dir=path), 'r', encoding='utf-8') as f:
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
        with io.open(util.default_makefile_path(out_dir=path), 'w', encoding='utf-8') as f:
            f.write(makefile_template_str)

    @staticmethod
    def cleanup_env_config(path: str = None) -> None:
        """
        A utility function for cleaning up the environment configuration

        :param path: the path to where the configuration is stored
        :return: None
        """
        # try:
        if os.path.exists(util.default_users_path(out_dir=path)):
            os.remove(util.default_users_path(out_dir=path))
        if os.path.exists(util.default_topology_path(out_dir=path)):
            os.remove(util.default_topology_path(out_dir=path))
        if os.path.exists(util.default_flags_path(out_dir=path)):
            os.remove(util.default_flags_path(out_dir=path))
        if os.path.exists(util.default_vulnerabilities_path(out_dir=path)):
            os.remove(util.default_vulnerabilities_path(out_dir=path))
        if os.path.exists(util.default_containers_path(out_dir=path)):
            os.remove(util.default_containers_path(out_dir=path))
        if os.path.exists(util.default_containers_folders_path(out_dir=path)):
            shutil.rmtree(util.default_containers_folders_path(out_dir=path))
        if os.path.exists(util.default_traffic_path(out_dir=path)):
            os.remove(util.default_traffic_path(out_dir=path))
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
            path = util.default_output_dir()
        for f in os.listdir(path):
            if re.search("env_*", f):
                shutil.rmtree(os.path.join(path, f))

    @staticmethod
    def get_env_dirs(path: str = None) -> List[str]:
        """
        Utility function for getting the directories of the emulation environment

        :param path: path to where the directories should be stored
        :return: A list of the directories
        """
        if path == None:
            path = util.default_output_dir()
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
            path = util.default_output_dir()
        env_dirs = EnvConfigGenerator.get_env_dirs(path)
        containers_configs = []
        for d in env_dirs:
            containers_configs.append(util.read_containers_config(d + constants.DOCKER.CONTAINER_CONFIG_CFG_PATH))
        return containers_configs

    @staticmethod
    def get_all_envs_flags_config(path: str = None) -> List[FlagsConfig]:
        """
        Utility function for getting the configuration of all flags in the emulation environment

        :param path: the path where the configuration should be stored
        :return: A list with the flag configurations
        """
        if path == None:
            path = util.default_output_dir()
        env_dirs = EnvConfigGenerator.get_env_dirs(path)
        flags_config = []
        for d in env_dirs:
            flags_config.append(util.read_containers_config(d + constants.DOCKER.CONTAINER_CONFIG_FLAGS_CFG_PATH))
        return flags_config

    @staticmethod
    def config_exists(path: str = None) -> bool:
        """
        Checks whether a complete environment configuration exists in a given path or not

        :param path: the path to check
        :return: True if it exists, otherwise False
        """
        if not os.path.exists(util.default_users_path(out_dir=path)):
            return False
        if not os.path.exists(util.default_topology_path(out_dir=path)):
            return False
        if not os.path.exists(util.default_flags_path(out_dir=path)):
            return False
        if not os.path.exists(util.default_vulnerabilities_path(out_dir=path)):
            return False
        if not os.path.exists(util.default_containers_path(out_dir=path)):
            return False
        if not os.path.exists(util.default_containers_folders_path(out_dir=path)):
            return False
        if not os.path.exists(util.default_makefile_path(out_dir=path)):
            return False
        if not os.path.exists(util.default_traffic_path(out_dir=path)):
            return False

        return True

    @staticmethod
    def compute_approx_pi_star(env, ids_enabled: bool, num_flags: int) -> float:
        """
        Utility function for computing the approximate optimal pi* reward for the attacker in a given environment

        :param env: the environment
        :param ids_enabled: whether IDS is enabled
        :param num_flags: the number of flags in the environment
        :return: the approximate optimal reward
        """
        action_costs = env.env_config.action_costs
        action_alerts = env.env_config.action_alerts
        pi_star = 0
        if env.env_config.cost_coefficient == 0 and not ids_enabled:
            pi_star = (-env.env_config.base_step_reward)*num_flags
        elif env.env_config.cost_coefficient > 0 and not ids_enabled:
            pi_star = (-env.env_config.base_step_reward) * num_flags # dont' know optimal cost, this is upper bound on optimality
        elif env.env_config.cost_coefficient == 0 and ids_enabled:
            pi_star = (-env.env_config.base_step_reward) * num_flags # dont' know optimal cost, this is upper bound on optimality
        else:
            pi_star = (-env.env_config.base_step_reward) * num_flags  # dont' know optimal cost, this is upper bound on optimality
        return pi_star


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
            util.write_emulation_config_file(emulation_env_config, path + emulation_env_config.name
                                             + constants.COMMANDS.SLASH_DELIM + \
                                             constants.DOCKER.EMULATION_ENV_CFG_PATH)

        container_dirs_path = path + emulation_env_config.name + constants.COMMANDS.SLASH_DELIM + \
                              constants.DOCKER.CONTAINERS_DIR
        if not os.path.exists(container_dirs_path):
            EnvConfigGenerator.create_container_dirs(emulation_env_config.containers_config,
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
            path = util.default_emulation_config_path(out_dir=util.default_output_dir())
        return util.read_emulation_env_config(path)

    @staticmethod
    def apply_emulation_env_config(emulation_env_config: EmulationEnvConfig, no_traffic: bool = False) -> None:
        """
        Applies the emulation env config

        :param emulation_env_config: the config to apply
        :param no_traffic: a boolean parameter that is True if the traffic generators should be skipped
        :return: None
        """
        emulation_config = EmulationConfig(agent_ip=emulation_env_config.containers_config.agent_ip,
                                           agent_username=constants.CSLE_ADMIN.USER,
                                           agent_pw=constants.CSLE_ADMIN.PW, server_connection=False)
        steps = 11
        if no_traffic:
            steps = steps-1
        current_step = 1
        print(f"-- Configuring the emulation --")
        print(f"-- Step {current_step}/{steps}: Creating networks --")
        ContainerManager.create_networks(containers_config=emulation_env_config.containers_config)

        current_step += 1
        print(f"-- Step {current_step}/{steps}: Connect containers to networks --")
        ContainerManager.connect_containers_to_networks(containers_config=emulation_env_config.containers_config)

        current_step += 1
        print(f"-- Step {current_step}/{steps}: Apply log sink config --")
        EnvConfigGenerator.apply_log_sink_config(log_sink_config=emulation_env_config.log_sink_config)

        current_step += 1
        print(f"-- Step {current_step}/{steps}: Connect containers to log sink --")
        ContainerManager.connect_containers_to_logsink(containers_config=emulation_env_config.containers_config,
                                                       log_sink_config=emulation_env_config.log_sink_config)

        current_step += 1
        print(f"-- Step {current_step}/{steps}: Creating users --")
        UsersGenerator.create_users(users_config=emulation_env_config.users_config, emulation_config=emulation_config)

        current_step += 1
        print(f"-- Step {current_step}/{steps}: Creating flags --")
        FlagsGenerator.create_flags(flags_config=emulation_env_config.flags_config, emulation_config=emulation_config)

        current_step += 1
        print(f"-- Step {current_step}/{steps}: Creating topology --")
        TopologyGenerator.create_topology(topology=emulation_env_config.topology_config,
                                          emulation_config=emulation_config)

        current_step += 1
        print(f"-- Step {current_step}/{steps}: Creating resource constraints --")
        ResourceConstraintsGenerator.apply_resource_constraints(resources_config=emulation_env_config.resources_config,
                                                                emulation_config=emulation_config)

        if not no_traffic:
            current_step += 1
            print(f"-- Step {current_step}/{steps}: Creating traffic generators --")
            TrafficGenerator.create_and_start_internal_traffic_generators(
                traffic_config=emulation_env_config.traffic_config,
                containers_config=emulation_env_config.containers_config,
                emulation_config=emulation_config, sleep_time=1)
            TrafficGenerator.start_client_population(
                traffic_config=emulation_env_config.traffic_config,
                containers_config=emulation_env_config.containers_config,
                emulation_config=emulation_config, log_sink_config=emulation_env_config.log_sink_config)

        current_step += 1
        print(f"-- Step {current_step}/{steps}: Starting the Intrusion Detection System --")
        ContainerGenerator.start_ids(containers_cfg=emulation_env_config.containers_config,
                                     emulation_config=emulation_config)

        current_step += 1
        print(f"-- Step {current_step}/{steps}: Starting the Docker stats monitor --")
        #TODO


    @staticmethod
    def apply_log_sink_config(log_sink_config: LogSinkConfig) -> None:
        """
        Applies the log sink config

        :param log_sink_config: the config to apply
        :return: None
        """
        emulation_config = EmulationConfig(agent_ip=log_sink_config.container.ips_and_networks[0][0],
                                           agent_username=constants.CSLE_ADMIN.USER,
                                           agent_pw=constants.CSLE_ADMIN.PW, server_connection=False)
        steps = 4
        current_step = 1
        print(f"-- Configuring the logsink --")

        print(f"-- Log sink configuration step {current_step}/{steps}: Creating networks --")
        networks = ContainerManager.get_network_references()
        networks = list(map(lambda x: x.name, networks))
        ip, net = log_sink_config.container.ips_and_networks[0]
        ContainerManager.create_network_from_dto(network_dto=net, existing_network_names=networks)

        current_step += 1
        print(f"-- Log sink configuration step {current_step}/{steps}: Connect log sink container to network --")
        ContainerManager.connect_logsink_to_network(log_sink_config=log_sink_config)

        print(f"-- Log sink configuration step {current_step}/{steps}: Restarting the Kafka server --")
        LogSinkManager.stop_kafka_server(log_sink_config=log_sink_config, emulation_config=emulation_config)
        time.sleep(20)
        LogSinkManager.start_kafka_server(log_sink_config=log_sink_config, emulation_config=emulation_config)
        time.sleep(20)

        current_step += 1
        print(f"-- Log sink configuration step {current_step}/{steps}: Create topics --")
        LogSinkManager.create_topics(log_sink_config=log_sink_config, emulation_config=emulation_config)


    @staticmethod
    def start_custom_traffic(emulation_env_config : EmulationEnvConfig) -> None:
        """
        Utility function for starting traffic generators and client population on a given emulation

        :param emulation_env_config: the configuration of the emulation
        :return: None
        """
        emulation_config = EmulationConfig(agent_ip=emulation_env_config.containers_config.agent_ip,
                                           agent_username=constants.CSLE_ADMIN.USER,
                                           agent_pw=constants.CSLE_ADMIN.PW, server_connection=False)

        TrafficGenerator.create_and_start_internal_traffic_generators(
            traffic_config=emulation_env_config.traffic_config,
            containers_config=emulation_env_config.containers_config,
            emulation_config=emulation_config, sleep_time=1)
        TrafficGenerator.start_client_population(
            traffic_config=emulation_env_config.traffic_config,
            containers_config=emulation_env_config.containers_config,
            emulation_config=emulation_config, log_sink_config=emulation_env_config.log_sink_config)


    @staticmethod
    def stop_custom_traffic(emulation_env_config : EmulationEnvConfig) -> None:
        """
        Stops the traffic generators on all internal nodes and stops the arrival process of clients

        :param emulation_env_config: the configuration for connecting to the emulation
        :return: None
        """
        emulation_config = EmulationConfig(agent_ip=emulation_env_config.containers_config.agent_ip,
                                           agent_username=constants.CSLE_ADMIN.USER,
                                           agent_pw=constants.CSLE_ADMIN.PW, server_connection=False)
        TrafficGenerator.stop_internal_traffic_generators(traffic_config=emulation_env_config.traffic_config,
                                                          emulation_config=emulation_config)
        TrafficGenerator.stop_client_population(traffic_config=emulation_env_config.traffic_config,
                                                emulation_config=emulation_config)


    @staticmethod
    def delete_networks_of_log_sink(log_sink_config: LogSinkConfig) -> None:
        """
        Deletes the docker networks of a log sink

        :param log_sink_config: the log sink config
        :return: None
        """
        c = log_sink_config.container
        for ip_net in c.ips_and_networks:
            ip, net = ip_net
            ContainerManager.remove_network(name=net.name)


    @staticmethod
    def delete_networks_of_emulation_env_config(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Deletes the docker networks

        :param emulation_env_config: the emulation env config
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            for ip_net in c.ips_and_networks:
                ip, net = ip_net
                ContainerManager.remove_network(name=net.name)

        c = emulation_env_config.log_sink_config.container
        for ip_net in c.ips_and_networks:
            ip, net = ip_net
            ContainerManager.remove_network(name=net.name)


    @staticmethod
    def run_containers(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Run containers in the emulation env config

        :param emulation_env_config: the config
        :return: None
        """
        path = util.default_output_dir()
        for c in emulation_env_config.containers_config.containers:
            ips = c.get_ips()
            container_resources : NodeResourcesConfig = None
            for r in emulation_env_config.resources_config.node_resources_configurations:
                for ip_net_resources in r.ips_and_network_configs:
                    ip, net_resources = ip_net_resources
                    if ip in ips:
                        container_resources : NodeResourcesConfig = r
                        break
            if container_resources is None:
                raise ValueError(f"Container resources not found for container with ips:{ips}, "
                                 f"resources:{emulation_env_config.resources_config}")

            name = f"csle-{c.minigame}-{c.name}{c.suffix}-level{c.level}"
            print(f"Starting container:{name}")
            cmd = f"docker container run -dt --name {name} " \
                  f"--hostname={c.name}{c.suffix} --label dir={path} " \
                  f"--label cfg={path + constants.DOCKER.EMULATION_ENV_CFG_PATH} " \
                  f"--label emulation={emulation_env_config.name} --network=none --publish-all=true " \
                  f"--memory={container_resources.available_memory_gb}G --cpus={container_resources.num_cpus} " \
                  f"--restart={c.restart_policy} --cap-add NET_ADMIN csle/{c.name}:{c.version}"
            subprocess.call(cmd, shell=True)

        c = emulation_env_config.log_sink_config.container
        container_resources : NodeResourcesConfig = emulation_env_config.log_sink_config.resources

        name = f"csle-{c.minigame}-{c.name}{c.suffix}-level{c.level}"
        print(f"Starting container:{name}")
        cmd = f"docker container run -dt --name {name} " \
              f"--hostname={c.name}{c.suffix} --label dir={path} " \
              f"--label cfg={path + constants.DOCKER.EMULATION_ENV_CFG_PATH} " \
              f"--label emulation={emulation_env_config.name} --network=none --publish-all=true " \
              f"--memory={container_resources.available_memory_gb}G --cpus={container_resources.num_cpus} " \
              f"--restart={c.restart_policy} --cap-add NET_ADMIN csle/{c.name}:{c.version}"
        subprocess.call(cmd, shell=True)


    @staticmethod
    def run_container(image: str, name: str, memory : int = 4, num_cpus: int = 1) -> None:
        """
        Runs a given container

        :param image: image of the container
        :param name: name of the container
        :param memory: memory in GB
        :param num_cpus: number of CPUs to allocate
        :return: None
        """
        net_id = random.randint(128, 254)
        sub_net_id= random.randint(2, 254)
        host_id= random.randint(2, 254)
        net_name = f"csle_custom_net_{name}_{net_id}"
        ip = f"55.{net_id}.{sub_net_id}.{host_id}"
        ContainerManager.create_network(name=net_name,
                                        subnetmask=f"55.{net_id}.0.0/16",
                                        existing_network_names=[])
        print(f"Starting container with image:{image} and name:csle-custom-{name}-level1")
        cmd = f"docker container run -dt --name csle-custom-{name}-level1 " \
              f"--hostname={name} " \
              f"--network={net_name} --ip {ip} --publish-all=true " \
              f"--memory={memory}G --cpus={num_cpus} " \
              f"--restart={constants.DOCKER.ON_FAILURE_3} --cap-add NET_ADMIN {image}"
        subprocess.call(cmd, shell=True)

    @staticmethod
    def stop_containers(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Stop containers in the emulation env config

        :param emulation_env_config: the config
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            name = f"csle-{c.minigame}-{c.name}{c.suffix}-level{c.level}"
            print(f"Stopping container:{name}")
            cmd = f"docker stop {name}"
            subprocess.call(cmd, shell=True)

        c = emulation_env_config.log_sink_config.container
        name = f"csle-{c.minigame}-{c.name}{c.suffix}-level{c.level}"
        print(f"Stopping container:{name}")
        cmd = f"docker stop {name}"
        subprocess.call(cmd, shell=True)


    @staticmethod
    def rm_containers(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Remove containers in the emulation env config

        :param emulation_env_config: the config
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            name = f"csle-{c.minigame}-{c.name}{c.suffix}-level{c.level}"
            print(f"Removing container:{name}")
            cmd = f"docker rm {name}"
            subprocess.call(cmd, shell=True)

        c = emulation_env_config.log_sink_config.container
        name = f"csle-{c.minigame}-{c.name}{c.suffix}-level{c.level}"
        print(f"Removing container:{name}")
        cmd = f"docker rm {name}"
        subprocess.call(cmd, shell=True)


    @staticmethod
    def install_emulation(config: EmulationEnvConfig) -> None:
        """
        Installs the emulation configuration in the metastore

        :param config: the config to install
        :return: None
        """
        print(f"Installing emulation:{config.name} in the metastore")
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                try:
                    config.vuln_config = config.vuln_config.to_dict()
                    config_json_str = json.dumps(json.loads(jsonpickle.encode(config)), indent=4, sort_keys=True)
                    cur.execute(f"INSERT INTO {constants.METADATA_STORE.EMULATIONS_TABLE} (name, config) "
                                f"VALUES (%s, %s)", (config.name, config_json_str))
                    conn.commit()
                    print(f"Emulation {config.name} installed successfully")
                except psycopg.errors.UniqueViolation as e:
                    print(f"Emulation {config.name} is already installed")


    @staticmethod
    def uninstall_emulation(config: EmulationEnvConfig) -> None:
        """
        Uninstalls the emulation configuration in the metastore

        :param config: the config to uninstall
        :return: None
        """
        print(f"Uninstalling emulation:{config.name} from the metastore")
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.EMULATIONS_TABLE} WHERE name = %s", (config.name,))
                conn.commit()
                print(f"Emulation {config.name} uninstalled successfully")





