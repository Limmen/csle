import os
from csle_common.dao.container_config.users_config import UsersConfig
from csle_common.dao.container_config.node_users_config import NodeUsersConfig
from csle_common.util.experiments_util import util
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.config.generator.users_generator import UsersGenerator
import csle_common.constants.constants as constants


def default_users(network_id: int = 5) -> UsersConfig:
    """
    :param network_id: the network id
    :return: the UsersConfig of the emulation
    """
    users = [
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191", users=[
            ("agent", "agent", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21", users=[
            ("admin", "admin31151x", True),
            ("test", "qwerty", True),
            ("oracle", "abc123", False)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10", users=[
            ("admin", "admin1235912", True),
            ("jessica", "water", False)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2", users=[
            ("admin", "test32121", False),
            ("user1", "123123", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3", users=[
            ("john", "doe", True),
            ("vagrant", "test_pw1", False)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54", users=[
            ("trent", "xe125@41!341", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101", users=[
            ("zidane", "1b12ha9", True)
        ]),
        NodeUsersConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7", users=[
            ("zlatan", "pi12195e", True),
            ("kennedy", "eul1145x", False)
        ])
    ]
    users_conf = UsersConfig(users=users)
    return users_conf


# Generates the users.json configuration file
if __name__ == '__main__':
    network_id = 5
    if not os.path.exists(util.default_users_path()):
        UsersGenerator.write_users_config(default_users(network_id=network_id))
    users_config = util.read_users_config(util.default_users_path())
    emulation_config = EmulationConfig(agent_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                                       agent_username=constants.CSLE_ADMIN.USER,
                                       agent_pw=constants.CSLE_ADMIN.PW, server_connection=False)
    UsersGenerator.create_users(users_config=users_config, emulation_config=emulation_config)
