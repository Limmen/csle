from typing import List, Tuple
import io
import shutil
import random
import os
import re
import json
import subprocess
from gym_pycr_pwcrack.dao.container_config.vulnerability_type import VulnType
from gym_pycr_pwcrack.envs.config.generator.topology_generator import TopologyGenerator
from gym_pycr_pwcrack.envs.config.generator.vuln_generator import VulnerabilityGenerator
from gym_pycr_pwcrack.envs.config.generator.flags_generator import FlagsGenerator
from gym_pycr_pwcrack.envs.config.generator.users_generator import UsersGenerator
from gym_pycr_pwcrack.envs.config.generator.container_generator import ContainerGenerator
from gym_pycr_pwcrack.dao.container_config.containers_config import ContainersConfig
from gym_pycr_pwcrack.dao.container_config.flags_config import FlagsConfig
from gym_pycr_pwcrack.util.experiments_util import util
from gym_pycr_pwcrack.dao.container_config.topology import Topology
from gym_pycr_pwcrack.dao.container_config.vulnerabilities_config import VulnerabilitiesConfig
from gym_pycr_pwcrack.dao.container_config.users_config import UsersConfig

class EnvConfigGenerator:

    @staticmethod
    def execute_env_cmd(path :str, cmd: str):
        env_dirs = EnvConfigGenerator.get_env_dirs(path=path)
        cmds = ["clean", "clean_config", "gen_config", "apply_config", "run", "stop", "start", "topology", "users",
                "flags", "vuln", "all", "clean_fs_cache"]
        if cmd in cmds:
            for dir in env_dirs:
                cmd_full = "make " + cmd
                subprocess.call(cmd_full, shell=True, cwd=dir)
        elif cmd == "clean_envs":
            EnvConfigGenerator.cleanup_envs(path=util.default_output_dir())

    @staticmethod
    def generate_envs(num_envs: int, container_pool: List[Tuple[str, str]] = None,
                 gw_vuln_compatible_containers: List[Tuple[str, str]] = None,
                 pw_vuln_compatible_containers: List[Tuple[str, str]] = None, subnet_id: int = 1,
                 agent_containers : List[Tuple[str, str]] = None, router_containers : List[Tuple[str, str]]= None,
                 path: str = None, min_num_users : int = 1, max_num_users : int = 5, min_num_flags: int = 1,
                 max_num_flags : int = 5, min_num_nodes : int = 4, max_num_nodes : int = 10,
                 subnet_prefix: str = "172.18.", cleanup_old_envs : bool = True):
        if cleanup_old_envs:
            EnvConfigGenerator.cleanup_envs(path=util.default_output_dir())

        envs_dirs_path = path
        subnet_id_blacklist = set()
        for i in range(num_envs):
            dir_name = "env_" + str(i)
            dir_path = os.path.join(envs_dirs_path, dir_name)
            os.makedirs(dir_path)
            env_path = os.path.join(envs_dirs_path, dir_name + "/")
            shutil.copyfile(util.default_container_makefile_template_path(out_dir=util.default_output_dir()),
                            util.default_container_makefile_template_path(out_dir=env_path))
            shutil.copyfile(util.default_makefile_template_path(out_dir=util.default_output_dir()),
                            util.default_makefile_template_path(out_dir=env_path))
            shutil.copyfile(os.path.join(envs_dirs_path, "./create_flags.py"),
                            os.path.join(env_path, "./create_flags.py"))
            shutil.copyfile(os.path.join(envs_dirs_path, "./create_topology.py"),
                            os.path.join(env_path, "./create_topology.py"))
            shutil.copyfile(os.path.join(envs_dirs_path, "./create_vuln.py"),
                            os.path.join(env_path, "./create_vuln.py"))
            shutil.copyfile(os.path.join(envs_dirs_path, "./create_users.py"),
                            os.path.join(env_path, "./create_users.py"))
            gen_subnet_prefix, subnet_id = EnvConfigGenerator.create_env(min_num_users=min_num_users,
                                                                     max_num_users=max_num_users,
                                                                     min_num_flags=min_num_flags,
                                                                     max_num_flags=max_num_flags,
                                                                     min_num_nodes=min_num_nodes,
                                                                     max_num_nodes=max_num_nodes,
                                                                     container_pool=container_pool,
                                                                     gw_vuln_compatible_containers=gw_vuln_compatible_containers,
                                                                     pw_vuln_compatible_containers=pw_vuln_compatible_containers,
                                                                     agent_containers=agent_containers,
                                                                     router_containers=router_containers,
                                                                     path=env_path, subnet_prefix=subnet_prefix,
                                                                     subnet_id_blacklist=subnet_id_blacklist)
            subnet_id_blacklist.add(subnet_id)
            os.rename(envs_dirs_path + "/" + dir_name, envs_dirs_path + "/" + dir_name + "_" + gen_subnet_prefix)

    @staticmethod
    def generate(num_nodes: int = 5, subnet_prefix: str = "172.18.", num_flags: int = 1,
                 max_num_users: int = 5,
                 container_pool: List[Tuple[str, str]] = None,
                 gw_vuln_compatible_containers: List[Tuple[str, str]] = None,
                 pw_vuln_compatible_containers: List[Tuple[str, str]] = None, subnet_id: int = 1,
                 agent_containers : List[Tuple[str, str]] = None, router_containers : List[Tuple[str, str]]= None) \
            -> Tuple[Topology, VulnerabilitiesConfig, UsersConfig, FlagsConfig, ContainersConfig]:

        adj_matrix, gws, topology, agent_ip, router_ip = TopologyGenerator.generate(num_nodes=num_nodes,
                                                                                    subnet_prefix=subnet_prefix)
        vulnerabilities = VulnerabilityGenerator.generate(topology=topology, gateways=gws, agent_ip=agent_ip,
                                                          subnet_prefix=subnet_prefix,
                                                          num_flags=num_flags, access_vuln_types=[VulnType.WEAK_PW],
                                                          router_ip=router_ip)
        users = UsersGenerator.generate(max_num_users=max_num_users, topology=topology, agent_ip=agent_ip)
        flags = FlagsGenerator.generate(vuln_cfg=vulnerabilities, num_flags=num_flags)
        containers = ContainerGenerator.generate(
            topology=topology, vuln_cfg=vulnerabilities, gateways=gws, container_pool=container_pool,
            gw_vuln_compatible_containers=gw_vuln_compatible_containers,
            pw_vuln_compatible_containers=pw_vuln_compatible_containers, subnet_id=subnet_id, num_flags=num_flags,
            agent_ip=agent_ip, router_ip=router_ip, agent_containers=agent_containers,
            router_containers=router_containers, subnet_prefix=subnet_prefix)

        return topology, vulnerabilities, users, flags, containers

    @staticmethod
    def create_env(min_num_users: int, max_num_users: int, min_num_flags: int, max_num_flags: int, min_num_nodes: int,
                   max_num_nodes: int,
                   container_pool :list, gw_vuln_compatible_containers : list,
                   pw_vuln_compatible_containers: list,
                   agent_containers : list, router_containers: list, path: str = None,
                   subnet_prefix: str = "172.18.", subnet_id_blacklist : set = None):

        if subnet_id_blacklist is None:
            subnet_id_blacklist = set()

        EnvConfigGenerator.cleanup_env_config(path=path)

        networks, network_ids = EnvConfigGenerator.list_docker_networks()
        running_containers = EnvConfigGenerator.list_running_containers()
        networks_in_use, network_ids_in_use = EnvConfigGenerator.find_networks_in_use(containers=running_containers)

        available_network_ids = list(filter(lambda x: x != 0 and x not in network_ids_in_use and x not in subnet_id_blacklist, network_ids))
        subnet_id = available_network_ids[random.randint(0, len(available_network_ids) - 1)]
        num_nodes = random.randint(min_num_nodes, max_num_nodes)
        subnet_prefix = subnet_prefix + str(subnet_id) + "."
        num_flags = random.randint(min_num_flags, min(max_num_flags, num_nodes - 3))
        num_users = random.randint(min_num_users, max_num_users)


        topology, vulnerabilities, users, flags, containers = EnvConfigGenerator.generate(
            num_nodes=num_nodes, subnet_prefix=subnet_prefix, num_flags=num_flags, max_num_users=num_users,
            container_pool=container_pool,
            gw_vuln_compatible_containers=gw_vuln_compatible_containers,
            pw_vuln_compatible_containers=pw_vuln_compatible_containers, subnet_id=subnet_id,
            agent_containers=agent_containers,
            router_containers=router_containers)

        UsersGenerator.write_users_config(users, path=path)
        TopologyGenerator.write_topology(topology, path=path)
        FlagsGenerator.write_flags_config(flags, path=path)
        VulnerabilityGenerator.write_vuln_config(vulnerabilities, path=path)
        ContainerGenerator.write_containers_config(containers, path=path)

        EnvConfigGenerator.create_container_dirs(containers, path=path)
        return subnet_prefix, subnet_id

    @staticmethod
    def list_docker_networks():
        cmd = "docker network ls"
        stream = os.popen(cmd)
        networks = stream.read()
        networks = networks.split("\n")
        networks = list(map(lambda x: x.split(), networks))
        networks = list(filter(lambda x: len(x) > 1, networks))
        networks = list(map(lambda x: x[1], networks))
        networks = list(filter(lambda x: re.match(r"pycr_net_\d", x), networks))
        network_ids = list(map(lambda x: int(x.replace("pycr_net_", "")), networks))
        return networks, network_ids


    @staticmethod
    def list_running_containers():
        cmd = "docker ps -q"
        stream = os.popen(cmd)
        running_containers = stream.read()
        running_containers = running_containers.split("\n")
        running_containers = list(filter(lambda x: x!= "", running_containers))
        return running_containers


    @staticmethod
    def find_networks_in_use(containers: List[str]):
        networks_in_use = []
        network_ids_in_use = []
        for c in containers:
            cmd = "docker inspect " + c + " -f '{{json .NetworkSettings.Networks }}'"
            stream = os.popen(cmd)
            network_info = stream.read()
            network_info = json.loads(network_info)
            for k in network_info.keys():
                if re.match(r"pycr_net_\d", k):
                   networks_in_use.append(k)
                   network_ids_in_use.append(int(k.replace("pycr_net_", "")))

        return networks_in_use, network_ids_in_use


    @staticmethod
    def create_container_dirs(container_config: ContainersConfig, path: str = None):
        containers_folders_dir = util.default_containers_folders_path(out_dir=path)
        if not os.path.exists(containers_folders_dir):
            os.makedirs(containers_folders_dir)

        with io.open(util.default_container_makefile_template_path(out_dir=path), 'r', encoding='utf-8') as f:
            makefile_template_str = f.read()

        counts = {}
        container_names = []
        for c in container_config.containers:
            count = 1
            if c.name in counts:
                count = counts[c.name] + 1
            counts[c.name] = count + 1
            c_dir = containers_folders_dir + "/" + c.name + "_" + str(count)
            container_names.append(c.name + "_" + str(count))
            if not os.path.exists(c_dir):
                os.makedirs(c_dir)
                makefile_preamble = ""
                makefile_preamble = makefile_preamble + "PROJECT=pycr\n"
                makefile_preamble = makefile_preamble + "NETWORK=" + c.network + "\n"
                makefile_preamble = makefile_preamble + "MINIGAME=" + c.minigame + "\n"
                makefile_preamble = makefile_preamble + "CONTAINER=" + c.name + "\n"
                makefile_preamble = makefile_preamble + "VERSION=" + c.version + "\n"
                makefile_preamble = makefile_preamble + "LEVEL=" + c.level + "\n"
                makefile_preamble = makefile_preamble + "DIR=" + path + "\n"
                makefile_preamble = makefile_preamble + "CFG=" + path + "/containers.json\n"
                makefile_preamble = makefile_preamble + "FLAGSCFG=" + path + "/flags.json\n"
                makefile_preamble = makefile_preamble + "TOPOLOGYCFG=" + path + "/topology.json\n"
                makefile_preamble = makefile_preamble + "USERSCFG=" + path + "/users.json\n"
                makefile_preamble = makefile_preamble + "VULNERABILITIESCFG=" + path + "/vulnerabilities.json\n"
                makefile_preamble = makefile_preamble + "IP=" + c.ip + "\n"
                makefile_preamble = makefile_preamble + "SUFFIX=" + str(count) + "\n\n"
                makefile_str = makefile_preamble + makefile_template_str
                with io.open(c_dir + "/Makefile", 'w', encoding='utf-8') as f:
                    f.write(makefile_str)

        EnvConfigGenerator.create_makefile(container_names, path=path)

    @staticmethod
    def create_makefile(container_names, path: str = None):
        with io.open(util.default_makefile_template_path(out_dir=path), 'r', encoding='utf-8') as f:
            makefile_template_str = f.read()

        makefile_template_str = makefile_template_str + "run:\n"
        for c in container_names:
            makefile_template_str = makefile_template_str + "	cd containers/" + c + "/ && $(MAKE) run\n"

        makefile_template_str = makefile_template_str + "\n\n"
        makefile_template_str = makefile_template_str + "stop:\n"
        for c in container_names:
            makefile_template_str = makefile_template_str + "	cd containers/" + c + "/ && $(MAKE) stop\n"

        makefile_template_str = makefile_template_str + "\n\n"
        makefile_template_str = makefile_template_str + "start:\n"
        for c in container_names:
            makefile_template_str = makefile_template_str + "	cd containers/" + c + "/ && $(MAKE) start\n"

        makefile_template_str = makefile_template_str + "\n\n"
        makefile_template_str = makefile_template_str + "clean:\n"
        for c in container_names:
            makefile_template_str = makefile_template_str + "	cd containers/" + c + "/ && $(MAKE) clean\n"
        makefile_template_str = makefile_template_str + "\n\n"
        with io.open(util.default_makefile_path(out_dir=path), 'w', encoding='utf-8') as f:
            f.write(makefile_template_str)

    @staticmethod
    def cleanup_env_config(path: str = None):
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
        # except Exception as e:
        #     pass

    @staticmethod
    def cleanup_envs(path: str = None):
        if path == None:
            path = util.default_output_dir()
        for f in os.listdir(path):
            if re.search("env_*", f):
                shutil.rmtree(os.path.join(path, f))

    @staticmethod
    def get_env_dirs(path: str = None):
        if path == None:
            path = util.default_output_dir()
        env_dirs = []
        for f in os.listdir(path):
            if re.search("env_*", f):
                env_dirs.append(os.path.join(path, f))
        return env_dirs

    @staticmethod
    def get_all_envs_containers_config(path: str = None) -> List[ContainersConfig]:
        if path == None:
            path = util.default_output_dir()
        env_dirs = EnvConfigGenerator.get_env_dirs(path)
        containers_configs = []
        for d in env_dirs:
            containers_configs.append(util.read_containers_config(d + "/containers.json"))
        return containers_configs

    @staticmethod
    def get_all_envs_flags_config(path: str = None) -> List[FlagsConfig]:
        if path == None:
            path = util.default_output_dir()
        env_dirs = EnvConfigGenerator.get_env_dirs(path)
        flags_config = []
        for d in env_dirs:
            flags_config.append(util.read_containers_config(d + "/flags.json"))
        return flags_config

    @staticmethod
    def config_exists(path: str = None):
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

        return True

    @staticmethod
    def compute_approx_pi_star(env, ids_enabled, num_flags) -> float:
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


if __name__ == '__main__':
    container_pool = [("ftp1", "0.0.1"), ("ftp2", "0.0.1"), ("honeypot1", "0.0.1"),
                      ("honeypot2", "0.0.1"),
                      ("ssh1", "0.0.1"), ("ssh2", "0.0.1"),
                      ("ssh3", "0.0.1"), ("telnet1", "0.0.1"), ("telnet2", "0.0.1"), ("telnet3", "0.0.1")]
    gw_vuln_compatible_containers = [("ssh1", "0.0.1"), ("ssh2", "0.0.1"), ("ssh3", "0.0.1"), ("telnet1", "0.0.1"),
                                     ("telnet2", "0.0.1"), ("telnet3", "0.0.1")]
    pw_vuln_compatible_containers = [("ftp1", "0.0.1"), ("ftp2", "0.0.1")]
    agent_containers = [(("hacker_kali1", "0.0.1"))]
    router_containers = [("router1", "0.0.1"), ("router2", "0.0.1")]
    # topology, vulnerabilities, users, flags, containers = EnvConfigGenerator.generate(
    #     num_nodes = 10, subnet_prefix="172.18.2.", num_flags=3, max_num_users=2, container_pool=container_pool,
    #     gw_vuln_compatible_containers=gw_vuln_compatible_containers,
    #     pw_vuln_compatible_containers=pw_vuln_compatible_containers, subnet_id=2, agent_containers=agent_containers,
    #     router_containers=router_containers)
    #EnvConfigGenerator.list_docker_networks()
    containers = EnvConfigGenerator.list_running_containers()
    EnvConfigGenerator.find_networks_in_use(containers)
    
