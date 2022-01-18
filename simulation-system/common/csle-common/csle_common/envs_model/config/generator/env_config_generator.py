from typing import List, Tuple, Set
import io
import shutil
import random
import os
import re
import json
import subprocess
from csle_common.dao.container_config.vulnerability_type import VulnType
from csle_common.envs_model.config.generator.topology_generator import TopologyGenerator
from csle_common.envs_model.config.generator.vuln_generator import VulnerabilityGenerator
from csle_common.envs_model.config.generator.flags_generator import FlagsGenerator
from csle_common.envs_model.config.generator.users_generator import UsersGenerator
from csle_common.envs_model.config.generator.container_generator import ContainerGenerator
from csle_common.envs_model.config.generator.traffic_generator import TrafficGenerator
from csle_common.dao.container_config.containers_config import ContainersConfig
from csle_common.dao.container_config.resources_config import ResourcesConfig
from csle_common.dao.container_config.node_resources_config import NodeResourcesConfig
from csle_common.dao.container_config.flags_config import FlagsConfig
from csle_common.util.experiments_util import util
from csle_common.dao.container_config.container_env_config import ContainerEnvConfig
from csle_common.dao.container_config.created_env_config import CreatedEnvConfig
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
    def generate_envs(container_env_config: ContainerEnvConfig, num_envs: int,
                 cleanup_old_envs : bool = True, start_idx : int = 0) -> Set:
        """
        Generates a <num_envs> number of emulation environments

        :param container_env_config: the environment configuration
        :param num_envs: the number of environments
        :param cleanup_old_envs: boolean flag whether to clean up old environments or not
        :param start_idx: the start idx of the first environment to create
        :return: the blacklist of subnet ids
        """
        if cleanup_old_envs:
            EnvConfigGenerator.cleanup_envs(path=util.default_output_dir())

        envs_dirs_path = container_env_config.path

        for i in range(num_envs):
            dir_name = "env_" + str(start_idx + i)
            dir_path = os.path.join(envs_dirs_path, dir_name)
            os.makedirs(dir_path)
            env_path = os.path.join(envs_dirs_path, dir_name + constants.COMMANDS.SLASH_DELIM)
            shutil.copyfile(util.default_container_makefile_template_path(out_dir=util.default_output_dir()),
                            util.default_container_makefile_template_path(out_dir=env_path))
            shutil.copyfile(util.default_makefile_template_path(out_dir=util.default_output_dir()),
                            util.default_makefile_template_path(out_dir=env_path))
            shutil.copyfile(os.path.join(envs_dirs_path, constants.DOCKER.CREATE_FLAGS_SCRIPT),
                            os.path.join(env_path, constants.DOCKER.CREATE_FLAGS_SCRIPT))
            shutil.copyfile(os.path.join(envs_dirs_path, constants.DOCKER.CREATE_TOPOLOGY_SCRIPT),
                            os.path.join(env_path, constants.DOCKER.CREATE_TOPOLOGY_SCRIPT))
            shutil.copyfile(os.path.join(envs_dirs_path, constants.DOCKER.CREATE_VULN_SCRIPT),
                            os.path.join(env_path, constants.DOCKER.CREATE_VULN_SCRIPT))
            shutil.copyfile(os.path.join(envs_dirs_path, constants.DOCKER.CREATE_USERS_SCRIPT),
                            os.path.join(env_path, constants.DOCKER.CREATE_USERS_SCRIPT))
            shutil.copyfile(os.path.join(envs_dirs_path, constants.DOCKER.CREATE_TRAFFIC_GENERATORS_SCRIPT),
                            os.path.join(env_path, constants.DOCKER.CREATE_TRAFFIC_GENERATORS_SCRIPT))
            container_env_config_c = container_env_config.copy()
            container_env_config_c.path = env_path
            gen_subnet_prefix, subnet_id = EnvConfigGenerator.create_env(container_env_config_c)
            container_env_config.subnet_id_blacklist.add(subnet_id)
            os.rename(envs_dirs_path + constants.COMMANDS.SLASH_DELIM + dir_name, envs_dirs_path +
                      constants.COMMANDS.SLASH_DELIM + dir_name + constants.COMMANDS.UNDERSCORE_DELIM
                      + gen_subnet_prefix)
        return container_env_config.subnet_id_blacklist

    @staticmethod
    def generate(container_env_config: ContainerEnvConfig) -> Tuple[CreatedEnvConfig]:
        """
        Generates a new emulation environment (creates the artifacts)

        :param container_env_config: configuration of the new environment
        :return: the configuration of the generated emulation environment
        """

        adj_matrix, gws, topology, agent_ip, router_ip, node_id_d, node_id_d_inv = \
            TopologyGenerator.generate(num_nodes=container_env_config.num_nodes,
                                       subnet_prefix=container_env_config.subnet_prefix)
        vulnerabilities, vulnerable_nodes = VulnerabilityGenerator.generate(topology=topology, gateways=gws, agent_ip=agent_ip,
                                                          subnet_prefix=container_env_config.subnet_prefix,
                                                          num_flags=container_env_config.num_flags, access_vuln_types=[VulnType.WEAK_PW],
                                                          router_ip=router_ip)
        users = UsersGenerator.generate(max_num_users=container_env_config.max_num_users, topology=topology, agent_ip=agent_ip)
        flags = FlagsGenerator.generate(vuln_cfg=vulnerabilities, num_flags=container_env_config.num_flags)
        containers = ContainerGenerator.generate(
            topology=topology, vuln_cfg=vulnerabilities, gateways=gws, container_pool=container_env_config.container_pool,
            gw_vuln_compatible_containers=container_env_config.gw_vuln_compatible_containers,
            pw_vuln_compatible_containers=container_env_config.pw_vuln_compatible_containers,
            subnet_id=container_env_config.subnet_id, num_flags=container_env_config.num_flags,
            agent_ip=agent_ip, router_ip=router_ip, agent_containers=container_env_config.agent_containers,
            router_containers=container_env_config.router_containers,
            subnet_prefix=container_env_config.subnet_prefix, vulnerable_nodes = vulnerable_nodes)

        agent_container_names = list(map(lambda x: x[0], container_env_config.agent_containers))
        gateway_container_names = list(map(lambda x: x[0], container_env_config.router_containers))
        traffic = TrafficGenerator.generate(topology=topology, containers_config=containers,
                                            agent_container_names=agent_container_names,
                                            router_container_names = gateway_container_names
                                            )
        created_env_config = CreatedEnvConfig(
            topology=topology, containers_config = containers, vuln_config=vulnerabilities,
            users_config = users, flags_config = flags, traffic_config = traffic)
        return created_env_config

    @staticmethod
    def create_env(container_env_config: ContainerEnvConfig) -> Tuple[str, id]:
        """
        Function that creates a new emulation environment given a configuration

        :param container_env_config: the configuration of the environment to create
        :return: (subnet_prefix, subnet_id) of the created environment
        """

        EnvConfigGenerator.cleanup_env_config(path=container_env_config.path)

        networks, network_ids = EnvConfigGenerator.list_docker_networks()
        running_containers = EnvConfigGenerator.list_running_containers()
        networks_in_use, network_ids_in_use = EnvConfigGenerator.find_networks_in_use(containers=running_containers)

        available_network_ids = list(filter(lambda x: x != 0 and
                                                      (x not in network_ids_in_use and
                                                       x not in container_env_config.subnet_id_blacklist), network_ids))
        container_env_config.subnet_id = available_network_ids[random.randint(0, len(available_network_ids) - 1)]
        container_env_config.num_nodes = random.randint(container_env_config.min_num_nodes,
                                                        container_env_config.max_num_nodes)
        container_env_config.subnet_prefix = container_env_config.subnet_prefix + \
                                             str(container_env_config.subnet_id) + constants.COMMANDS.DOT_DELIM
        container_env_config.num_flags = random.randint(container_env_config.min_num_flags,
                                                        min(container_env_config.max_num_flags,
                                                            container_env_config.num_nodes - 3))
        container_env_config.num_users = random.randint(container_env_config.min_num_users,
                                                        container_env_config.max_num_users)

        created_env_config = EnvConfigGenerator.generate(container_env_config)

        UsersGenerator.write_users_config(created_env_config.users_config, path=container_env_config.path)
        TopologyGenerator.write_topology(created_env_config.topology, path=container_env_config.path)
        FlagsGenerator.write_flags_config(created_env_config.flags_config, path=container_env_config.path)
        VulnerabilityGenerator.write_vuln_config(created_env_config.vuln_config,
                                                 path=container_env_config.path)
        ContainerGenerator.write_containers_config(created_env_config.containers_config,
                                                   path=container_env_config.path)
        TrafficGenerator.write_traffic_config(created_env_config.traffic_config, path=container_env_config.path)

        EnvConfigGenerator.create_container_dirs(created_env_config.containers_config, path=container_env_config.path)
        return container_env_config.subnet_prefix, container_env_config.subnet_id

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
        internal_networks = list(filter(lambda x: re.match(r"{}\d".format(constants.CSLE.CSLE_NETWORK_PREFIX), x),
                                        networks))
        external_networks = list(filter(lambda x: re.match(r"{}\d".format(constants.CSLE.CSLE_EXTERNAL_NET_PREFIX), x),
                                        networks))
        internal_network_ids = list(map(lambda x: int(x.replace(constants.CSLE.CSLE_NETWORK_PREFIX, "")),
                                        internal_networks))
        external_network_ids = list(map(lambda x: int(x.replace(constants.CSLE.CSLE_EXTERNAL_NET_PREFIX, "")),
                                        external_networks))
        network_ids = internal_network_ids + external_network_ids
        networks = internal_networks + external_networks
        return networks, network_ids


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
    def find_networks_in_use(containers: List[str]) -> Tuple[List[str], List[str]]:
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
                              path: str = None,
                              create_folder_makefile: bool = True) -> None:
        """
        Utility function for creating the container directories with the start scripts

        :param container_config: the configuration of the containers
        :param resources_config: the resources config of the containers
        :param path: the path where to create the directories
        :param create_folder_makefile: a boolean flag indicating whether to create a Makefile for the folder or not
        :return: None
        """
        containers_folders_dir = util.default_containers_folders_path(out_dir=path)
        if not os.path.exists(containers_folders_dir):
            os.makedirs(containers_folders_dir)

        with io.open(util.default_container_makefile_template_path(out_dir=path), 'r', encoding='utf-8') as f:
            makefile_template_str = f.read()

        counts = {}
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
            count = 1
            if c.name in counts:
                count = counts[c.name] + 1
            counts[c.name] = count + 1
            c_dir = containers_folders_dir + "/" + c.name + "_" + str(count)
            container_names.append(c.name + "_" + str(count))
            if not os.path.exists(c_dir):
                os.makedirs(c_dir)
                makefile_preamble = ""
                makefile_preamble = makefile_preamble + constants.MAKEFILE.PROJECT + "=csle\n"
                makefile_preamble = makefile_preamble + constants.MAKEFILE.MINIGAME + "=" + c.minigame + "\n"
                makefile_preamble = makefile_preamble + constants.MAKEFILE.CONTAINER + "=" + c.name + "\n"
                makefile_preamble = makefile_preamble + constants.MAKEFILE.VERSION + "=" + c.version + "\n"
                makefile_preamble = makefile_preamble + constants.MAKEFILE.LEVEL + "=" + c.level + "\n"
                makefile_preamble = makefile_preamble + constants.MAKEFILE.DIR + "=" + path + "\n"
                makefile_preamble = makefile_preamble + constants.MAKEFILE.CFG + "=" + path + \
                                    constants.DOCKER.CONTAINER_CONFIG_CFG_PATH + "\n"
                makefile_preamble = makefile_preamble + constants.MAKEFILE.FLAGSCFG + "=" + path + \
                                    constants.DOCKER.CONTAINER_CONFIG_FLAGS_CFG_PATH + "\n"
                makefile_preamble = makefile_preamble + constants.MAKEFILE.TOPOLOGYCFG + "=" + path + \
                                    constants.DOCKER.CONTAINER_CONFIG_TOPOLOGY_CFG_PATH + "\n"
                makefile_preamble = makefile_preamble + constants.MAKEFILE.USERSCFG + "=" + path + \
                                    constants.DOCKER.CONTAINER_CONFIG_USERS_CFG_PATH + "\n"
                makefile_preamble = makefile_preamble + constants.MAKEFILE.VULNERABILITIESCFG + "=" \
                                    + path + constants.DOCKER.CONTAINER_CONFIG_VULNERABILITIES_CFG_PATH + "\n"
                makefile_preamble = makefile_preamble + constants.MAKEFILE.RESTART_POLICY + "="+ c.restart_policy + "\n"
                makefile_preamble = makefile_preamble + constants.MAKEFILE.NUM_CPUS + "=" + \
                                    str(container_resources.num_cpus) + "\n"
                makefile_preamble = makefile_preamble + constants.MAKEFILE.MEMORY + "=" + \
                                    str(container_resources.available_memory_gb) + "G\n"
                makefile_preamble = makefile_preamble + constants.MAKEFILE.SUFFIX + "=_" + str(count) + "\n\n"

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


