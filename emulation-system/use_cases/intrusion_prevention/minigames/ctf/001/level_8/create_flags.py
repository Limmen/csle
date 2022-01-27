import os
from csle_common.dao.container_config.flags_config import FlagsConfig
from csle_common.dao.container_config.node_flags_config import NodeFlagsConfig
from csle_common.util.experiments_util import util
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.config.generator.flags_generator import FlagsGenerator
import csle_common.constants.constants as constants


def default_flags(network_id: int = 8) -> FlagsConfig:
    """
    :param network_id: the network id
    :return: the FlagsConfig of the emulation
    """
    flags = [
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.79",
                        flags=[(
                               f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}3"
                               f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                               f"{constants.COMMON.FLAG_FILENAME_PREFIX}3", f"/{constants.COMMANDS.TMP_DIR}/", 3,
                               False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.2",
                        flags=[(
                               f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}2"
                               f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                               f"{constants.COMMON.FLAG_FILENAME_PREFIX}2", f"/{constants.COMMANDS.TMP_DIR}/", 2,
                               False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.3",
                        flags=[(
                               f"/{constants.COMMANDS.ROOT_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}1"
                               f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                               f"{constants.COMMON.FLAG_FILENAME_PREFIX}1", f"/{constants.COMMANDS.ROOT_DIR}/", 1,
                               True, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.19",
                        flags=[(
                               f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}4"
                               f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                               f"{constants.COMMON.FLAG_FILENAME_PREFIX}4", f"/{constants.COMMANDS.TMP_DIR}/", 4,
                               False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.31",
                        flags=[(
                               f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}5"
                               f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                               f"{constants.COMMON.FLAG_FILENAME_PREFIX}5", f"/{constants.COMMANDS.TMP_DIR}/", 5,
                               False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.42",
                        flags=[(
                               f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}6"
                               f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                               f"{constants.COMMON.FLAG_FILENAME_PREFIX}6", f"/{constants.COMMANDS.TMP_DIR}/", 6,
                               False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.37",
                        flags=[(
                               f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}7"
                               f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                               f"{constants.COMMON.FLAG_FILENAME_PREFIX}7", f"/{constants.COMMANDS.TMP_DIR}/", 7,
                               False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.82",
                        flags=[(
                               f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}8"
                               f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                               f"{constants.COMMON.FLAG_FILENAME_PREFIX}8", f"/{constants.COMMANDS.TMP_DIR}/", 8,
                               False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.75",
                        flags=[(
                               f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}9"
                               f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                               f"{constants.COMMON.FLAG_FILENAME_PREFIX}9", f"/{constants.COMMANDS.TMP_DIR}/", 9,
                               False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.71",
                        flags=[(
                               f"/{constants.COMMANDS.ROOT_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}10"
                               f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                               f"{constants.COMMON.FLAG_FILENAME_PREFIX}10", f"/{constants.COMMANDS.ROOT_DIR}/", 10,
                               True, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.2.11",
                        flags=[(
                               f"/{constants.COMMANDS.ROOT_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}11"
                               f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                               f"{constants.COMMON.FLAG_FILENAME_PREFIX}11", f"/{constants.COMMANDS.ROOT_DIR}/", 11,
                               True, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.4.51",
                        flags=[(
                               f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}12"
                               f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                               f"{constants.COMMON.FLAG_FILENAME_PREFIX}12", f"/{constants.COMMANDS.TMP_DIR}/", 12,
                               False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.3.52",
                        flags=[(
                               f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}13"
                               f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                               f"{constants.COMMON.FLAG_FILENAME_PREFIX}13", f"/{constants.COMMANDS.TMP_DIR}/", 13,
                               False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.5.54",
                        flags=[(
                               f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}14"
                               f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                               f"{constants.COMMON.FLAG_FILENAME_PREFIX}14", f"/{constants.COMMANDS.TMP_DIR}/", 14,
                               False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.6.55",
                        flags=[(
                               f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}15"
                               f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                               f"{constants.COMMON.FLAG_FILENAME_PREFIX}15", f"/{constants.COMMANDS.TMP_DIR}/", 15,
                               False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.7.56",
                        flags=[(
                               f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}16"
                               f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                               f"{constants.COMMON.FLAG_FILENAME_PREFIX}16", f"/{constants.COMMANDS.TMP_DIR}/", 16,
                               False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.8.57",
                        flags=[(
                               f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}17"
                               f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                               f"{constants.COMMON.FLAG_FILENAME_PREFIX}17", f"/{constants.COMMANDS.TMP_DIR}/", 17,
                               False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.9.58",
                        flags=[(
                               f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}18"
                               f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                               f"{constants.COMMON.FLAG_FILENAME_PREFIX}18", f"/{constants.COMMANDS.TMP_DIR}/", 18,
                               False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.10.59",
                        flags=[(
                               f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}19"
                               f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                               f"{constants.COMMON.FLAG_FILENAME_PREFIX}19", f"/{constants.COMMANDS.TMP_DIR}/", 19,
                               False, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.11.60",
                        flags=[(
                               f"/{constants.COMMANDS.ROOT_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}20"
                               f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                               f"{constants.COMMON.FLAG_FILENAME_PREFIX}20", f"/{constants.COMMANDS.ROOT_DIR}/", 20,
                               True, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.12.61",
                        flags=[(
                               f"/{constants.COMMANDS.ROOT_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}21"
                               f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                               f"{constants.COMMON.FLAG_FILENAME_PREFIX}21", f"/{constants.COMMANDS.ROOT_DIR}/", 21,
                               True, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.13.62",
                        flags=[(
                               f"/{constants.COMMANDS.TMP_DIR}/{constants.COMMON.FLAG_FILENAME_PREFIX}22"
                               f"{constants.FILE_PATTERNS.TXT_FILE_SUFFIX}",
                               f"{constants.COMMON.FLAG_FILENAME_PREFIX}22", f"/{constants.COMMANDS.TMP_DIR}/", 22,
                               False, 1)])
    ]
    flags_config = FlagsConfig(flags=flags)
    return flags_config


# Generates the flags.json configuration file
if __name__ == '__main__':
    network_id = 8
    if not os.path.exists(util.default_flags_path()):
        FlagsGenerator.write_flags_config(default_flags(network_id=network_id))
    flags_config = util.read_flags_config(util.default_flags_path())
    emulation_config = EmulationConfig(agent_ip=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{network_id}.1.191",
                                       agent_username=constants.CSLE_ADMIN.USER,
                                       agent_pw=constants.CSLE_ADMIN.PW, server_connection=False)
    FlagsGenerator.create_flags(flags_config=flags_config, emulation_config=emulation_config)
