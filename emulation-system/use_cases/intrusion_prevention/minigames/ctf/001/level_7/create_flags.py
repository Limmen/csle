import os
from csle_common.dao.container_config.flags_config import FlagsConfig
from csle_common.dao.container_config.node_flags_config import NodeFlagsConfig
from csle_common.util.experiments_util import util
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.config.generator.flags_generator import FlagsGenerator
import csle_common.constants.constants as constants


def default_flags(network_id: int = 7) -> FlagsConfig:
    """
    :param network_id: the network id
    :return: the FlagsConfig of the emulation
    """
    flags = [
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                        flags=[("/tmp/flag3.txt", "flag3", "/tmp/", 3, False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                        flags=[("/tmp/flag2.txt", "flag2", "/tmp/", 2, False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                        flags=[("/root/flag1.txt", "flag1", "/root/", 1, True, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.19",
                        flags=[("/tmp/flag4.txt", "flag4", "/tmp/", 4, False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.31",
                        flags=[("/tmp/flag5.txt", "flag5", "/tmp/", 5, False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.42",
                        flags=[("/tmp/flag6.txt", "flag6", "/tmp/", 6, False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.37",
                        flags=[("/tmp/flag7.txt", "flag7", "/tmp/", 7, False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.82",
                        flags=[("/tmp/flag8.txt", "flag8", "/tmp/", 8, False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.75",
                        flags=[("/tmp/flag9.txt", "flag9", "/tmp/", 9, False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.71",
                        flags=[("/root/flag10.txt", "flag10", "/root/", 10, True, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.11",
                        flags=[("/root/flag11.txt", "flag11", "/root/", 11, True, 1)])
    ]
    flags_config = FlagsConfig(flags=flags)
    return flags_config


# Generates the flags.json configuration file
if __name__ == '__main__':
    network_id = 7
    if not os.path.exists(util.default_flags_path()):
        FlagsGenerator.write_flags_config(default_flags(network_id = network_id))
    flags_config = util.read_flags_config(util.default_flags_path())
    emulation_config = EmulationConfig(agent_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                                       agent_username=constants.csle_ADMIN.USER,
                                       agent_pw=constants.csle_ADMIN.PW, server_connection=False)
    FlagsGenerator.create_flags(flags_config=flags_config, emulation_config=emulation_config)
