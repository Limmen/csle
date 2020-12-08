import random
import numpy as np
from gym_pycr_pwcrack.dao.container_config.topology import Topology
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.envs.logic.cluster.cluster_util import ClusterUtil
from gym_pycr_pwcrack.dao.container_config.users_config import UsersConfig
from gym_pycr_pwcrack.dao.container_config.node_users_config import NodeUsersConfig
from gym_pycr_pwcrack.envs.config.generator.topology_generator import TopologyGenerator
from gym_pycr_pwcrack.envs.config.generator.generator_util import GeneratorUtil
from random_username.generate import generate_username
import secrets
import string

class UsersGenerator:


    @staticmethod
    def generate(max_num_users: int, topology: Topology):
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
        users_conf = UsersConfig(users=user_configs)
        return users_conf

    @staticmethod
    def create_users(users_config: UsersConfig, cluster_config: ClusterConfig):
        for users_conf in users_config.users:
            GeneratorUtil.connect_admin(cluster_config=cluster_config, ip=users_conf.ip)

            cmd="ls /home"
            o,e,_ = ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)
            users_w_home = o.decode().split("\n")
            users_w_home = list(filter(lambda x: x != '', users_w_home))

            for user in users_w_home:
                if user != "pycr_admin":
                    cmd = "sudo deluser {}".format(user)
                    ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)
                    cmd = "sudo rm -rf /home/{}".format(user)
                    ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

            for user in users_conf.users:
                username, pw, root = user
                if root:
                    cmd = "sudo useradd -rm -d /home/{} -s /bin/bash -g root -G sudo -p \"$(openssl passwd -1 '{}')\" {}".format(username, pw, username)
                else:
                    cmd = "sudo useradd -rm -d /home/{} -s /bin/bash -p \"$(openssl passwd -1 '{}')\" {}".format(username,pw,username)
                o, e, _ = ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

            GeneratorUtil.disconnect_admin(cluster_config=cluster_config)

if __name__ == '__main__':
    adj_matrix, gws, topology = TopologyGenerator.generate(num_nodes=10, subnet_prefix="172.18.2.")
    users_conf = UsersGenerator.generate(5, topology)
