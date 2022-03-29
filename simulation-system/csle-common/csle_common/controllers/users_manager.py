from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.util.emulation_util import EmulationUtil


class UsersManager:
    """
    Class managing users in the emulation environments
    """

    @staticmethod
    def create_users(emulation_env_config: EmulationEnvConfig):
        """
        Creates users in an emulation environment according to a specified users-configuration

        :param users_config: the users configuration
        :param emulation_config: the emulation configuration
        :return: None
        """
        for users_conf in emulation_env_config.users_config.users:
            EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=users_conf.ip)

            cmd="ls /home"
            o,e,_ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.connections[users_conf.ip])
            users_w_home = o.decode().split("\n")
            users_w_home = list(filter(lambda x: x != '', users_w_home))

            for user in users_w_home:
                if user != "csle_admin":
                    cmd = "sudo deluser {}".format(user)
                    EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.connections[users_conf.ip])
                    cmd = "sudo rm -rf /home/{}".format(user)
                    EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.connections[users_conf.ip])

            for user in users_conf.users:
                username, pw, root = user
                if root:
                    cmd = "sudo useradd -rm -d /home/{} -s /bin/bash -g root -G sudo -p " \
                          "\"$(openssl passwd -1 '{}')\" {}".format(username, pw, username)
                else:
                    cmd = "sudo useradd -rm -d /home/{} -s /bin/bash " \
                          "-p \"$(openssl passwd -1 '{}')\" {}".format(username,pw,username)
                o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.connections[users_conf.ip])

            EmulationUtil.disconnect_admin(emulation_env_config=emulation_env_config)