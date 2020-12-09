import random
import os
from gym_pycr_pwcrack.envs.config.generator.env_config_generator import EnvConfigGenerator
from gym_pycr_pwcrack.envs.config.generator.users_generator import UsersGenerator
from gym_pycr_pwcrack.envs.config.generator.topology_generator import TopologyGenerator
from gym_pycr_pwcrack.envs.config.generator.flags_generator import FlagsGenerator
from gym_pycr_pwcrack.envs.config.generator.vuln_generator import VulnerabilityGenerator
from gym_pycr_pwcrack.envs.config.generator.container_generator import ContainerGenerator
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.util.experiments_util import util
from gym_pycr_pwcrack.dao.container_config.containers_config import ContainersConfig
import io
import shutil

def cleanup():
    #try:
    if os.path.exists(util.default_users_path()):
        os.remove(util.default_users_path())
    if os.path.exists(util.default_topology_path()):
        os.remove(util.default_topology_path())
    if os.path.exists(util.default_flags_path()):
        os.remove(util.default_flags_path())
    if os.path.exists(util.default_vulnerabilities_path()):
        os.remove(util.default_vulnerabilities_path())
    if os.path.exists(util.default_containers_path()):
        os.remove(util.default_containers_path())
    if os.path.exists(util.default_containers_folders_path()):
        shutil.rmtree(util.default_containers_folders_path())
    # except Exception as e:
    #     pass

def create_container_dirs(container_config: ContainersConfig):
    containers_folders_dir = util.default_containers_folders_path()
    if not os.path.exists(containers_folders_dir):
        os.makedirs(containers_folders_dir)

    with io.open(util.default_container_makefile_template_path(), 'r', encoding='utf-8') as f:
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
            makefile_preamble = makefile_preamble + "IP=" + c.ip + "\n"
            makefile_preamble = makefile_preamble + "SUFFIX=" + str(count) + "\n\n"
            makefile_str = makefile_preamble + makefile_template_str
            with io.open(c_dir + "/Makefile", 'w', encoding='utf-8') as f:
                f.write(makefile_str)

    create_makefile(container_names)

def create_makefile(container_names):
    with io.open(util.default_makefile_template_path(), 'r', encoding='utf-8') as f:
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
    with io.open(util.default_makefile_path(), 'w', encoding='utf-8') as f:
        f.write(makefile_template_str)


def generate_config():
    cleanup()

    container_pool = [("ftp1", "0.0.1"), ("ftp2", "0.0.1"), ("honeypot1", "0.0.1"),
                      ("honeypot2", "0.0.1"),
                      ("ssh1", "0.0.1"), ("ssh2", "0.0.1"),
                      ("ssh3", "0.0.1"), ("telnet1", "0.0.1"), ("telnet2", "0.0.1"), ("telnet3", "0.0.1")]
    gw_vuln_compatible_containers = [("ssh1", "0.0.1"), ("ssh2", "0.0.1"), ("ssh3", "0.0.1"), ("telnet1", "0.0.1"),
                                     ("telnet2", "0.0.1"), ("telnet3", "0.0.1")]

    pw_vuln_compatible_containers = [("ssh1", "0.0.1"), ("ssh2", "0.0.1"), ("ssh3", "0.0.1"), ("telnet1", "0.0.1"),
                                     ("telnet2", "0.0.1"), ("telnet3", "0.0.1"), ("ftp1", "0.0.1"), ("ftp2", "0.0.1")]

    agent_containers = [(("hacker_kali1", "0.0.1"))]
    router_containers = [("router1", "0.0.1"), ("router2", "0.0.1")]

    networks, network_ids = EnvConfigGenerator.list_docker_networks()
    running_containers = EnvConfigGenerator.list_running_containers()
    networks_in_use, network_ids_in_use = EnvConfigGenerator.find_networks_in_use(containers=running_containers)

    available_network_ids = list(filter(lambda x: x!= 0 and x not in network_ids_in_use, network_ids))
    subnet_id = available_network_ids[random.randint(0, len(available_network_ids)-1)]
    num_nodes = random.randint(4, 10)
    subnet_prefix = "172.18." + str(subnet_id) + "."
    num_flags = random.randint(1, num_nodes-3)
    max_num_users = random.randint(1, 5)

    topology, vulnerabilities, users, flags, containers = EnvConfigGenerator.generate(
        num_nodes=num_nodes, subnet_prefix=subnet_prefix, num_flags=num_flags, max_num_users=max_num_users, container_pool=container_pool,
        gw_vuln_compatible_containers=gw_vuln_compatible_containers,
        pw_vuln_compatible_containers=pw_vuln_compatible_containers, subnet_id=subnet_id, agent_containers=agent_containers,
        router_containers=router_containers)

    UsersGenerator.write_users_config(users)
    TopologyGenerator.write_topology(topology)
    FlagsGenerator.write_flags_config(flags)
    VulnerabilityGenerator.write_vuln_config(vulnerabilities)
    ContainerGenerator.write_containers_config(containers)

    create_container_dirs(containers)

if __name__ == '__main__':
    all_exists = True
    if not os.path.exists(util.default_users_path()):
        all_exists = False
    if not os.path.exists(util.default_topology_path()):
        all_exists = False
    if not os.path.exists(util.default_flags_path()):
        all_exists = False
    if not os.path.exists(util.default_vulnerabilities_path()):
        all_exists = False
    if not os.path.exists(util.default_containers_path()):
        all_exists = False
    if not os.path.exists(util.default_containers_folders_path()):
        all_exists = False
    if not os.path.exists(util.default_makefile_path()):
        all_exists = False
    if not all_exists:
        generate_config()
    else:
        print("Reusing existing configuration")
