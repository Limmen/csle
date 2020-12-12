from typing import List
import docker
from gym_pycr_pwcrack.dao.env_info.running_env_container import RunningEnvContainer
from gym_pycr_pwcrack.dao.env_info.running_env import RunningEnv
from gym_pycr_pwcrack.util.experiments_util import util

class EnvInfo:

    @staticmethod
    def parse_env_infos() -> List[RunningEnv]:
        client1 = docker.from_env()
        containers = client1.containers.list()
        client2 = docker.APIClient(base_url='unix://var/run/docker.sock')
        parsed_containers = EnvInfo.parse_containers(containers=containers, client2=client2)
        networks = list(set(list(map(lambda x: x.net, parsed_containers))))
        parsed_envs = EnvInfo.parse_envs(networks=networks, containers=parsed_containers)
        return parsed_envs


    @staticmethod
    def parse_envs(networks: List[str], containers: List[RunningEnvContainer]) -> List[RunningEnv]:
        parsed_envs = []
        for net in networks:
            net_containers = list(filter(lambda x: x.net == net, containers))
            subnet_prefix = ".".join(net_containers[0].ip.rsplit(".")[0:-1])
            subnet_mask = subnet_prefix + "/" + str(net_containers[0].ip_prefix_len)
            minigame = net_containers[0].minigame
            id = net.split("_")[-1]

            containers_config = None
            users_config = None
            topology_config = None
            flags_config = None
            vulnerabilities_config = None

            if net_containers[0].containers_config_path is not None:
                try:
                    containers_config = util.read_containers_config(net_containers[0].containers_config_path)
                except:
                    pass

            if net_containers[0].users_config_path is not None:
                try:
                    users_config = util.read_users_config(net_containers[0].users_config_path)
                except:
                    pass

            if net_containers[0].topology_config_path is not None:
                try:
                    topology_config = util.read_topology(net_containers[0].topology_config_path)
                except:
                    pass

            if net_containers[0].flags_config_path is not None:
                try:
                    flags_config = util.read_flags_config(net_containers[0].flags_config_path)
                except:
                    pass

            if net_containers[0].vulnerabilities_config_path is not None:
                try:
                    vulnerabilities_config = util.read_vulns_config(net_containers[0].vulnerabilities_config_path)
                except:
                    pass

            p_env = RunningEnv(containers=net_containers, name=net, subnet_prefix=subnet_mask, minigame=minigame, id=id,
                               subnet_mask=subnet_mask, level= net_containers[0].level,
                               flags_config=flags_config, containers_config=containers_config,
                               topology_config=topology_config, vulnerabilities_config=vulnerabilities_config,
                               users_config=users_config)
            parsed_envs.append(p_env)
        return parsed_envs


    @staticmethod
    def parse_containers(containers, client2) -> List[RunningEnvContainer]:
        parsed_containers = []
        for c in containers:
            if "pycr-" in c.name:
                name_parts = c.name.split("-")
                minigame = name_parts[1]
                container_name_2 = name_parts[2]
                level = name_parts[3]
                inspect_info = client2.inspect_container(c.id)
                net = list(inspect_info["NetworkSettings"]["Networks"].keys())[0]
                labels = c.labels
                containers_config_path = None
                dir_path = None
                flags_config_path = None
                topology_config_path = None
                users_config_path = None
                vulnerabilities_config_path = None
                if "containers_cfg" in labels:
                    containers_config_path = labels["containers_cfg"]
                if "dir" in labels:
                    dir_path = labels["dir"]
                if "flags_cfg" in labels:
                    flags_config_path = labels["flags_cfg"]
                if "topology_cfg" in labels:
                    topology_config_path = labels["topology_cfg"]
                if "users_cfg" in labels:
                    users_config_path = labels["users_cfg"]
                if "vulnerabilities_cfg" in labels:
                    vulnerabilities_config_path = labels["vulnerabilities_cfg"]
                parsed_c = RunningEnvContainer(
                    name=c.name, status=c.status, short_id=c.short_id, image_short_id=c.image.short_id,
                    image_tags = c.image.tags, id=c.id,
                    created=inspect_info["Created"],
                    ip=inspect_info["NetworkSettings"]["Networks"][net]["IPAddress"],
                    network_id=inspect_info["NetworkSettings"]["Networks"][net]["NetworkID"],
                    gateway=inspect_info["NetworkSettings"]["Networks"][net]["Gateway"],
                    mac=inspect_info["NetworkSettings"]["Networks"][net]["MacAddress"],
                    ip_prefix_len=inspect_info["NetworkSettings"]["Networks"][net]["IPPrefixLen"],
                    minigame=minigame, name2=container_name_2, level=level, hostname=inspect_info["Config"]["Hostname"],
                    image_name=inspect_info["Config"]["Image"],
                    net=net, dir=dir_path, containers_config_path=containers_config_path,
                    users_config_path=users_config_path, flags_config_path=flags_config_path,
                    vulnerabilities_config_path=vulnerabilities_config_path, topology_config_path=topology_config_path
                )
                parsed_containers.append(parsed_c)
        return parsed_containers


if __name__ == '__main__':
    EnvInfo.parse_env_infos()