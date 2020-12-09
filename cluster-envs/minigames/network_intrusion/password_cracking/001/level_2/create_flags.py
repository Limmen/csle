import os
from gym_pycr_pwcrack.dao.container_config.flags_config import FlagsConfig
from gym_pycr_pwcrack.dao.container_config.node_flags_config import NodeFlagsConfig
from gym_pycr_pwcrack.util.experiments_util import util
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.envs.config.generator.flags_generator import FlagsGenerator

def default_flags() -> FlagsConfig:
    flags = [
        NodeFlagsConfig(ip="172.18.2.79", flags = [("/tmp/flag3.txt", "flag3")]),
        NodeFlagsConfig(ip="172.18.2.2", flags=[("/tmp/flag2.txt", "flag2")]),
        NodeFlagsConfig(ip="172.18.2.3", flags=[("/root/flag1.txt", "flag1")]),
        NodeFlagsConfig(ip="172.18.2.54", flags=[("/tmp/flag4.txt", "flag4")]),
        NodeFlagsConfig(ip="172.18.2.61", flags=[("/root/flag5.txt", "flag5")]),
        NodeFlagsConfig(ip="172.18.2.7", flags=[("/tmp/flag6.txt", "flag6")])
    ]
    flags_config = FlagsConfig(flags=flags)
    return flags_config

if __name__ == '__main__':
    if not os.path.exists(util.default_flags_path()):
        FlagsGenerator.write_flags_config(default_flags())
    flags_config = util.read_flags_config(util.default_flags_path())
    cluster_config = ClusterConfig(agent_ip="172.18.2.191", agent_username="pycr_admin",
                                   agent_pw="pycr@admin-pw_191", server_connection=False)
    FlagsGenerator.create_flags(flags_config=flags_config, cluster_config=cluster_config)