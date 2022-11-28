import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.util.emulation_util import EmulationUtil
from csle_common.logging.log import Logger


class FlagsController:
    """
    Class managing flags in the emulation environments
    """

    @staticmethod
    def create_flags(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Connects to a node in the emulation and creates the flags according to a given flags config

        :param emulation_env_config: the emulation env config
        :return: None
        """
        for flags_conf in emulation_env_config.flags_config.node_flag_configs:
            EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=flags_conf.ip)

            for flag in flags_conf.flags:
                Logger.__call__().get_logger().info(f"Creating flag:{flag.name} on {flags_conf.ip}")
                cmd = constants.COMMANDS.SUDO_RM_RF + " {}".format(flag.path)
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=flags_conf.ip))
                cmd = constants.COMMANDS.SUDO_TOUCH + " {}".format(flag.path)
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=flags_conf.ip))
                cmd = constants.COMMANDS.ECHO + " '{}' >> {}".format(flag.name, flag.path)
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=flags_conf.ip))

            EmulationUtil.disconnect_admin(emulation_env_config=emulation_env_config)
