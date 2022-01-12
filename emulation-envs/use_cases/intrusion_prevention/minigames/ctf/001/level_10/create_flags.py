import os
from pycr_common.dao.container_config.flags_config import FlagsConfig
from pycr_common.dao.container_config.node_flags_config import NodeFlagsConfig
from pycr_common.util.experiments_util import util
from pycr_common.dao.network.emulation_config import EmulationConfig
from pycr_common.envs_model.config.generator.flags_generator import FlagsGenerator
import pycr_common.constants.constants as constants


def default_flags() -> FlagsConfig:
    """
    :return: the FlagsConfig of the emulation
    """
    flags = [
        NodeFlagsConfig(ip="172.18.10.79", flags = [("/tmp/flag3.txt", "flag3", "/tmp/", 3, False, 1)]),
        NodeFlagsConfig(ip="172.18.10.2", flags=[("/tmp/flag2.txt", "flag2", "/tmp/", 2, False, 1)]),
        NodeFlagsConfig(ip="172.18.10.3", flags=[("/root/flag1.txt", "flag1", "/root/", 1, True, 1)]),
        NodeFlagsConfig(ip="172.18.10.19", flags=[("/tmp/flag4.txt", "flag4", "/tmp/", 4, False, 1)]),
        NodeFlagsConfig(ip="172.18.10.31", flags=[("/tmp/flag5.txt", "flag5", "/tmp/", 5, False, 1)]),
        NodeFlagsConfig(ip="172.18.10.42", flags=[("/tmp/flag6.txt", "flag6", "/tmp/", 6, False, 1)]),
        NodeFlagsConfig(ip="172.18.10.37", flags=[("/tmp/flag7.txt", "flag7", "/tmp/", 7, False, 1)]),
        NodeFlagsConfig(ip="172.18.10.82", flags=[("/tmp/flag8.txt", "flag8", "/tmp/", 8, False, 1)]),
        NodeFlagsConfig(ip="172.18.10.75", flags=[("/tmp/flag9.txt", "flag9", "/tmp/", 9, False, 1)]),
        NodeFlagsConfig(ip="172.18.10.71", flags=[("/root/flag10.txt", "flag10", "/root/", 10, True, 1)]),
        NodeFlagsConfig(ip="172.18.10.11", flags=[("/root/flag11.txt", "flag11", "/root/", 11, True, 1)]),
        NodeFlagsConfig(ip="172.18.10.104", flags=[("/root/flag12.txt", "flag12", "/root/", 12, True, 1)])
    ]
    flags_config = FlagsConfig(flags=flags)
    return flags_config

# Generates the flags.json configuration file
if __name__ == '__main__':
    if not os.path.exists(util.default_flags_path()):
        FlagsGenerator.write_flags_config(default_flags())
    flags_config = util.read_flags_config(util.default_flags_path())
    emulation_config = EmulationConfig(agent_ip="172.18.10.191", agent_username=constants.PYCR_ADMIN.USER,
                                     agent_pw=constants.PYCR_ADMIN.PW, server_connection=False)
    FlagsGenerator.create_flags(flags_config=flags_config, emulation_config=emulation_config)