import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.util.emulation_util import EmulationUtil


class UsersController:
    """
    Class managing users in the emulation environments
    """

    @staticmethod
    def create_users(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Creates users in an emulation environment according to a specified users-configuration

        :param emulation_env_config: the emulation env configuration
        :return: None
        """
        for users_conf in emulation_env_config.users_config.users_configs:
            EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=users_conf.ip)

            cmd = "ls /home"
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.connections[users_conf.ip])
            users_w_home = o.decode().split("\n")
            users_w_home = list(filter(lambda x: x != '', users_w_home))

            for user in users_w_home:
                if user != constants.CSLE_ADMIN.SSH_USER:
                    cmd = "sudo deluser {}".format(user)
                    EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.connections[users_conf.ip])
                    cmd = "sudo rm -rf /home/{}".format(user)
                    EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.connections[users_conf.ip])

            for user in users_conf.users:
                if user.root:
                    cmd = "sudo useradd -rm -d /home/{} -s /bin/bash -g root -G sudo -p " \
                          "\"$(openssl passwd -1 '{}')\" {}".format(user.username, user.pw, user.username)
                else:
                    cmd = "sudo useradd -rm  -d /home/{} -s /bin/bash -g {}" \
                          "-p \"$(openssl passwd -1 '{}')\" {}".format(user.username, user.username, user.pw,
                                                                       user.username)
                o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.connections[users_conf.ip])

            EmulationUtil.disconnect_admin(emulation_env_config=emulation_env_config)

        for vuln in emulation_env_config.vuln_config.node_vulnerability_configs:
            EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=vuln.ip)
            for cr in vuln.credentials:
                if cr.root:
                    cmd = "sudo useradd -rm -d /home/{} -s /bin/bash -g root -G sudo -p " \
                          "\"$(openssl passwd -1 '{}')\" {}".format(cr.username, cr.pw, cr.username)
                else:
                    cmd = "sudo useradd -rm -d /home/{} -s /bin/bash -g {} " \
                          "-p \"$(openssl passwd -1 '{}')\" {}".format(cr.username, cr.username, cr.pw, cr.username)
                o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd,
                                                        conn=emulation_env_config.get_connection(ip=vuln.ip))

            EmulationUtil.disconnect_admin(emulation_env_config=emulation_env_config)
