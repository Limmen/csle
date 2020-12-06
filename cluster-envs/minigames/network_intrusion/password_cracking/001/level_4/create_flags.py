import os
from gym_pycr_pwcrack.dao.container_config.flags_config import FlagsConfig
from gym_pycr_pwcrack.dao.container_config.node_flags_config import NodeFlagsConfig
from gym_pycr_pwcrack.util.experiments_util import util
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.envs.logic.cluster.cluster_util import ClusterUtil

def connect_admin(cluster_config: ClusterConfig, ip : str):
    cluster_config.agent_ip = ip
    cluster_config.connect_agent()

def disconnect_admin(cluster_config: ClusterConfig):
    cluster_config.close()

def default_flags() -> FlagsConfig:
    flags = [
        NodeFlagsConfig(ip="172.18.4.79", flags = [("/tmp/flag3.txt", "flag3")]),
        NodeFlagsConfig(ip="172.18.4.2", flags=[("/tmp/flag2.txt", "flag2")]),
        NodeFlagsConfig(ip="172.18.4.3", flags=[("/root/flag1.txt", "flag1")])
    ]
    flags_config = FlagsConfig(flags=flags)
    return flags_config

def write_default_flags_config(path:str = None) -> None:
    """
    Writes the default configuration to a json file

    :param path: the path to write the configuration to
    :return: None
    """
    if path is None:
        path = util.default_flags_path()
    flags_config = default_flags()
    util.write_flags_config_file(flags_config, path)

def create_flags(flags_config: FlagsConfig, cluster_config: ClusterConfig):
    for flags_conf in flags_config.flags:
        connect_admin(cluster_config=cluster_config, ip=flags_conf.ip)

        for flag in flags_conf.flags:
            path, content = flag
            cmd = "sudo rm -rf {}".format(path)
            ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)
            cmd = "sudo touch {}".format(path)
            ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)
            cmd = "echo '{}' >> {}".format(content, path)
            ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

        disconnect_admin(cluster_config=cluster_config)

if __name__ == '__main__':
    if not os.path.exists(util.default_flags_path()):
        write_default_flags_config()
    flags_config = util.read_flags_config(util.default_flags_path())
    cluster_config = ClusterConfig(agent_ip="172.18.4.191", agent_username="pycr_admin",
                                   agent_pw="pycr@admin-pw_191", server_connection=False)
    create_flags(flags_config=flags_config, cluster_config=cluster_config)