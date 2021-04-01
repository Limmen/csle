import os
from gym_pycr_ctf.dao.container_config.flags_config import FlagsConfig
from gym_pycr_ctf.dao.container_config.node_flags_config import NodeFlagsConfig
from gym_pycr_ctf.util.experiments_util import util
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.envs_model.config.generator.flags_generator import FlagsGenerator

def default_flags() -> FlagsConfig:
    flags = [
        NodeFlagsConfig(ip="172.18.2.79", flags = [("/tmp/flag3.txt", "flag3", "/tmp/", 3, True, 1)]),
        NodeFlagsConfig(ip="172.18.2.2", flags=[("/tmp/flag2.txt", "flag2", "/tmp/", 2, True, 1)]),
        NodeFlagsConfig(ip="172.18.2.3", flags=[("/root/flag1.txt", "flag1", "/root/", 1, True, 1)]),
        NodeFlagsConfig(ip="172.18.2.54", flags=[("/tmp/flag4.txt", "flag4", "/tmp/", 4, True, 1)]),
        NodeFlagsConfig(ip="172.18.2.61", flags=[("/root/flag5.txt", "flag5", "/root/", 5, True, 1)]),
        NodeFlagsConfig(ip="172.18.2.7", flags=[("/tmp/flag6.txt", "flag6", "/tmp/", 6, True, 1)])
    ]
    flags_config = FlagsConfig(flags=flags)
    return flags_config

if __name__ == '__main__':
    if not os.path.exists(util.default_flags_path()):
        FlagsGenerator.write_flags_config(default_flags())
    flags_config = util.read_flags_config(util.default_flags_path())
    emulation_config = EmulationConfig(agent_ip="172.18.2.191", agent_username="pycr_admin",
                                     agent_pw="pycr@admin-pw_191", server_connection=False)
    FlagsGenerator.create_flags(flags_config=flags_config, emulation_config=emulation_config)