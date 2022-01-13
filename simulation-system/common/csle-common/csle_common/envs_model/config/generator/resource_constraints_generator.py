import random
import numpy as np
from random_username.generate import generate_username
import secrets
import string
from csle_common.dao.container_config.topology import Topology
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.logic.emulation.util.common.emulation_util import EmulationUtil
from csle_common.dao.container_config.resources_config import ResourcesConfig
from csle_common.dao.container_config.node_users_config import NodeUsersConfig
from csle_common.envs_model.config.generator.topology_generator import TopologyGenerator
from csle_common.envs_model.config.generator.generator_util import GeneratorUtil
from csle_common.util.experiments_util import util


class ResourceConstraintsGenerator:
    """
    A Utility Class for generating resource-constraints configuration files
    """


    @staticmethod
    def apply_resource_constraints(resources_config: ResourcesConfig, emulation_config: EmulationConfig):
        """
        Creates users in an emulation environment according to a specified users-configuration

        :param users_config: the users configuration
        :param emulation_config: the emulation configuration
        :return: None
        """
        for node_resource_config in resources_config.node_resources_configurations:
            GeneratorUtil.connect_admin(emulation_config=emulation_config, ip=node_resource_config.ip)

            # cmd="ls /home"
            # o,e,_ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
            # users_w_home = o.decode().split("\n")
            # users_w_home = list(filter(lambda x: x != '', users_w_home))
            #
            # for user in users_w_home:
            #     if user != "csle_admin":
            #         cmd = "sudo deluser {}".format(user)
            #         EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
            #         cmd = "sudo rm -rf /home/{}".format(user)
            #         EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
            #
            # for user in node_resource_config.users:
            #     username, pw, root = user
            #     if root:
            #         cmd = "sudo useradd -rm -d /home/{} -s /bin/bash -g root -G sudo -p \"$(openssl passwd -1 '{}')\" {}".format(username, pw, username)
            #     else:
            #         cmd = "sudo useradd -rm -d /home/{} -s /bin/bash -p \"$(openssl passwd -1 '{}')\" {}".format(username,pw,username)
            #     o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            GeneratorUtil.disconnect_admin(emulation_config=emulation_config)

    @staticmethod
    def write_resources_config(resources_config: ResourcesConfig, path: str = None) -> None:
        """
        Writes the default configuration to a json file

        :param path: the path to write the configuration to
        :return: None
        """
        path = util.default_users_path(out_dir=path)
        util.write_users_config_file(resources_config, path)


