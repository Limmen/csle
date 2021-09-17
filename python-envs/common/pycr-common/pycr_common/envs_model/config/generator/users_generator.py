import random
import numpy as np
from random_username.generate import generate_username
import secrets
import string
from pycr_common.dao.container_config.topology import Topology
from pycr_common.dao.network.emulation_config import EmulationConfig
from pycr_common.envs_model.logic.emulation.util.common.emulation_util import EmulationUtil
from pycr_common.dao.container_config.users_config import UsersConfig
from pycr_common.dao.container_config.node_users_config import NodeUsersConfig
from pycr_common.envs_model.config.generator.topology_generator import TopologyGenerator
from pycr_common.envs_model.config.generator.generator_util import GeneratorUtil
from pycr_common.util.experiments_util import util


class UsersGenerator:

    @staticmethod
    def generate(max_num_users: int, topology: Topology, agent_ip: str):
        """
        Generates a random user configuration for a emulation environment

        :param max_num_users: the maximum number of users
        :param topology: the topology of the emulation
        :param agent_ip: the agent ip
        :return: the created users configuration
        """
        alphabet = string.ascii_letters + string.digits
        user_configs = []
        for node in topology.node_configs:
            num_users = random.randint(1, max_num_users)
            users = []
            for i in range(num_users):
                username = generate_username(1)[0]
                password = ''.join(secrets.choice(alphabet) for i in range(20))  # secure 20-character password
                root = False
                if np.random.rand() < 0.4:
                    root = True
                users.append((username, password, root))
            user_cfg = NodeUsersConfig(ip = node.ip, users=users)
            user_configs.append(user_cfg)

        agent_user = ("agent", "agent", True)
        agent_user_cfg = NodeUsersConfig(ip=agent_ip, users=[agent_user])
        user_configs.append(agent_user_cfg)

        users_conf = UsersConfig(users=user_configs)
        return users_conf

    @staticmethod
    def create_users(users_config: UsersConfig, emulation_config: EmulationConfig):
        """
        Creates users in an emulation environment according to a specified users-configuration

        :param users_config: the users configuration
        :param emulation_config: the emulation configuration
        :return: None
        """
        for users_conf in users_config.users:
            GeneratorUtil.connect_admin(emulation_config=emulation_config, ip=users_conf.ip)

            cmd="ls /home"
            o,e,_ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
            users_w_home = o.decode().split("\n")
            users_w_home = list(filter(lambda x: x != '', users_w_home))

            for user in users_w_home:
                if user != "pycr_admin":
                    cmd = "sudo deluser {}".format(user)
                    EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
                    cmd = "sudo rm -rf /home/{}".format(user)
                    EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            for user in users_conf.users:
                username, pw, root = user
                if root:
                    cmd = "sudo useradd -rm -d /home/{} -s /bin/bash -g root -G sudo -p \"$(openssl passwd -1 '{}')\" {}".format(username, pw, username)
                else:
                    cmd = "sudo useradd -rm -d /home/{} -s /bin/bash -p \"$(openssl passwd -1 '{}')\" {}".format(username,pw,username)
                o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            GeneratorUtil.disconnect_admin(emulation_config=emulation_config)

    @staticmethod
    def write_users_config(users_config: UsersConfig, path: str = None) -> None:
        """
        Writes the default configuration to a json file

        :param path: the path to write the configuration to
        :return: None
        """
        path = util.default_users_path(out_dir=path)
        util.write_users_config_file(users_config, path)


if __name__ == '__main__':
    adj_matrix, gws, topology = TopologyGenerator.generate(num_nodes=10, subnet_prefix="172.18.2.")
    users_conf = UsersGenerator.generate(5, topology, "172.18.2.191")
