import os
from gym_pycr_ctf.dao.container_config.users_config import UsersConfig
from gym_pycr_ctf.dao.container_config.node_users_config import NodeUsersConfig
from gym_pycr_ctf.util.experiments_util import util
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.envs_model.config.generator.users_generator import UsersGenerator

def default_users() -> UsersConfig:
    users = [
        NodeUsersConfig(ip="172.18.9.191", users=[
            ("agent", "agent", True)
        ]),
        NodeUsersConfig(ip="172.18.9.21", users=[
            ("admin", "admin31151x", True),
            ("test", "qwerty", True),
            ("oracle", "abc123", False)
        ]),
        NodeUsersConfig(ip="172.18.9.10", users=[
            ("admin", "admin1235912", True),
            ("jessica", "water", False)
        ]),
        NodeUsersConfig(ip="172.18.9.2", users=[
            ("admin", "test32121", False),
            ("user1", "123123", True)
        ]),
        NodeUsersConfig(ip="172.18.9.3", users=[
            ("admin", "admin", True),
            ("john", "doe", True),
            ("vagrant", "test_pw1", False)
        ]),
        NodeUsersConfig(ip="172.18.9.54", users=[
            ("trent", "xe125@41!341", True)
        ]),
        NodeUsersConfig(ip="172.18.9.101", users=[
            ("zidane", "1b12ha9", True)
        ]),
        NodeUsersConfig(ip="172.18.9.7", users=[
            ("zlatan", "pi12195e", True),
            ("kennedy", "eul1145x", False)
        ]),
        NodeUsersConfig(ip="172.18.9.4", users=[
            ("user1", "1235121", True)
        ]),
        NodeUsersConfig(ip="172.18.9.5", users=[
            ("user2", "1235121", True)
        ]),
        NodeUsersConfig(ip="172.18.9.6", users=[
            ("user3", "1bsae235121", True)
        ]),
        NodeUsersConfig(ip="172.18.9.8", users=[
            ("user4", "1bsae235121", True)
        ]),
        NodeUsersConfig(ip="172.18.9.9", users=[
            ("user5", "1gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.9.178", users=[
            ("user6", "1gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.9.11", users=[
            ("user7", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.9.12", users=[
            ("user8", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.9.13", users=[
            ("user9", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.9.14", users=[
            ("user10", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.9.15", users=[
            ("user11", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.9.16", users=[
            ("user12", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.9.17", users=[
            ("user13", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.9.18", users=[
            ("user14", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.9.19", users=[
            ("user15", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.9.20", users=[
            ("user16", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.9.28", users=[
            ("user17", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.9.22", users=[
            ("user18", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.9.23", users=[
            ("user19", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.9.24", users=[
            ("user20", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.9.25", users=[
            ("user20", "081gxq2", True)
        ])
    ]
    users_conf = UsersConfig(users=users)
    return users_conf


if __name__ == '__main__':
    if not os.path.exists(util.default_users_path()):
        UsersGenerator.write_users_config(default_users())
    users_config = util.read_users_config(util.default_users_path())
    emulation_config = EmulationConfig(agent_ip="172.18.9.191", agent_username="pycr_admin",
                                     agent_pw="pycr@admin-pw_191", server_connection=False)
    UsersGenerator.create_users(users_config=users_config, emulation_config=emulation_config)