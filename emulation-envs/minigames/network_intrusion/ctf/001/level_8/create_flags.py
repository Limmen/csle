import os
from gym_pycr_ctf.dao.container_config.flags_config import FlagsConfig
from gym_pycr_ctf.dao.container_config.node_flags_config import NodeFlagsConfig
from gym_pycr_ctf.util.experiments_util import util
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.envs.config.generator.flags_generator import FlagsGenerator

def default_flags() -> FlagsConfig:
    flags = [
        NodeFlagsConfig(ip="172.18.8.79", flags = [("/tmp/flag3.txt", "flag3", "/tmp/", 3, False, 1)]),
        NodeFlagsConfig(ip="172.18.8.2", flags=[("/tmp/flag2.txt", "flag2", "/tmp/", 2, False, 1)]),
        NodeFlagsConfig(ip="172.18.8.3", flags=[("/root/flag1.txt", "flag1", "/root/", 1, True, 1)]),
        NodeFlagsConfig(ip="172.18.8.19", flags=[("/tmp/flag4.txt", "flag4", "/tmp/", 4, False, 1)]),
        NodeFlagsConfig(ip="172.18.8.31", flags=[("/tmp/flag5.txt", "flag5", "/tmp/", 5, False, 1)]),
        NodeFlagsConfig(ip="172.18.8.42", flags=[("/tmp/flag6.txt", "flag6", "/tmp/", 6, False, 1)]),
        NodeFlagsConfig(ip="172.18.8.37", flags=[("/tmp/flag7.txt", "flag7", "/tmp/", 7, False, 1)]),
        NodeFlagsConfig(ip="172.18.8.82", flags=[("/tmp/flag8.txt", "flag8", "/tmp/", 8, False, 1)]),
        NodeFlagsConfig(ip="172.18.8.75", flags=[("/tmp/flag9.txt", "flag9", "/tmp/", 9, False, 1)]),
        NodeFlagsConfig(ip="172.18.8.71", flags=[("/root/flag10.txt", "flag10", "/root/", 10, True, 1)]),
        NodeFlagsConfig(ip="172.18.8.11", flags=[("/root/flag11.txt", "flag11", "/root/", 11, True, 1)]),
        NodeFlagsConfig(ip="172.18.8.51", flags=[("/tmp/flag12.txt", "flag12", "/tmp/", 12, False, 1)]),
        NodeFlagsConfig(ip="172.18.8.52", flags=[("/tmp/flag13.txt", "flag13", "/tmp/", 13, False, 1)]),
        NodeFlagsConfig(ip="172.18.8.54", flags=[("/tmp/flag14.txt", "flag14", "/tmp/", 14, False, 1)]),
        NodeFlagsConfig(ip="172.18.8.55", flags=[("/tmp/flag15.txt", "flag15", "/tmp/", 15, False, 1)]),
        NodeFlagsConfig(ip="172.18.8.56", flags=[("/tmp/flag16.txt", "flag16", "/tmp/", 16, False, 1)]),
        NodeFlagsConfig(ip="172.18.8.57", flags=[("/tmp/flag17.txt", "flag17", "/tmp/", 17, False, 1)]),
        NodeFlagsConfig(ip="172.18.8.58", flags=[("/tmp/flag18.txt", "flag18", "/tmp/", 18, False, 1)]),
        NodeFlagsConfig(ip="172.18.8.59", flags=[("/tmp/flag19.txt", "flag19", "/tmp/", 19, False, 1)]),
        NodeFlagsConfig(ip="172.18.8.60", flags=[("/root/flag20.txt", "flag20", "/root/", 20, True, 1)]),
        NodeFlagsConfig(ip="172.18.8.61", flags=[("/root/flag21.txt", "flag21", "/root/", 21, True, 1)]),
        NodeFlagsConfig(ip="172.18.8.62", flags=[("/tmp/flag22.txt", "flag22", "/tmp/", 22, False, 1)])
    ]
    flags_config = FlagsConfig(flags=flags)
    return flags_config


if __name__ == '__main__':
    if not os.path.exists(util.default_flags_path()):
        FlagsGenerator.write_flags_config(default_flags())
    flags_config = util.read_flags_config(util.default_flags_path())
    emulation_config = EmulationConfig(agent_ip="172.18.8.191", agent_username="pycr_admin",
                                     agent_pw="pycr@admin-pw_191", server_connection=False)
    FlagsGenerator.create_flags(flags_config=flags_config, emulation_config=emulation_config)