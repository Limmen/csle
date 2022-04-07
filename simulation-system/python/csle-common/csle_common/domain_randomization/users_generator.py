import random
import numpy as np
from random_username.generate import generate_username
import secrets
import string
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.topology_config import TopologyConfig
from csle_common.dao.emulation_config.users_config import UsersConfig
from csle_common.dao.emulation_config.node_users_config import NodeUsersConfig
from csle_common.domain_randomization.topology_generator import TopologyGenerator
from csle_common.util.experiment_util import ExperimentUtil


class UsersGenerator:
    """
    A Utility Class for generating users configuration files
    """

    @staticmethod
    def generate(max_num_users: int, topology: TopologyConfig, agent_ip: str):
        """
        Generates a random user configuration for an emulation environment

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
            user_cfg = NodeUsersConfig(ip = node.get_ips()[0], users=users)
            user_configs.append(user_cfg)

        agent_user = ("agent", "agent", True)
        agent_user_cfg = NodeUsersConfig(ip=agent_ip, users=[agent_user])
        user_configs.append(agent_user_cfg)

        users_conf = UsersConfig(users_configs=user_configs)
        return users_conf

    @staticmethod
    def write_users_config(users_config: UsersConfig, path: str = None) -> None:
        """
        Writes the default configuration to a json file

        :param path: the path to write the configuration to
        :return: None
        """
        path = ExperimentUtil.default_users_path(out_dir=path)
        ExperimentUtil.write_users_config_file(users_config, path)


if __name__ == '__main__':
    topology, agent_ip, router_ip, vulnerable_nodes = TopologyGenerator.generate(
        num_nodes=15, subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}2", subnet_id=2)
    users_conf = UsersGenerator.generate(max_num_users=5, topology=topology, agent_ip=agent_ip)
