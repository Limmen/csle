import os
from gym_pycr_pwcrack.dao.container_config.users_config import UsersConfig
from gym_pycr_pwcrack.dao.container_config.node_users_config import NodeUsersConfig
from gym_pycr_pwcrack.util.experiments_util import util
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.envs.config.generator.users_generator import UsersGenerator

def default_users() -> UsersConfig:
    users = [
        NodeUsersConfig(ip="172.18.7.191", users=[
            ("agent", "agent", True)
        ]),
        NodeUsersConfig(ip="172.18.7.21", users=[
            ("admin", "admin31151x", True),
            ("test", "qwerty", True),
            ("oracle", "abc123", False)
        ]),
        NodeUsersConfig(ip="172.18.7.10", users=[
            ("admin", "admin1235912", True),
            ("jessica", "water", False)
        ]),
        NodeUsersConfig(ip="172.18.7.2", users=[
            ("admin", "test32121", True),
            ("user1", "123123", True)
        ]),
        NodeUsersConfig(ip="172.18.7.3", users=[
            ("john", "doe", True),
            ("vagrant", "test_pw1", False)
        ]),
        NodeUsersConfig(ip="172.18.7.19", users=[
            ("karl", "gustaf", True),
            ("steven", "carragher", False)
        ]),
        NodeUsersConfig(ip="172.18.7.31", users=[
            ("stefan", "zweig", True)
        ]),
        NodeUsersConfig(ip="172.18.7.42", users=[
            ("roy", "neruda", True)
        ]),
        NodeUsersConfig(ip="172.18.7.37", users=[
            ("john", "conway", True)
        ]),
        NodeUsersConfig(ip="172.18.7.82", users=[
            ("john", "nash", True)
        ]),
        NodeUsersConfig(ip="172.18.7.75", users=[
            ("larry", "samuelson", True)
        ]),
        NodeUsersConfig(ip="172.18.7.71", users=[
            ("robbins", "monro", True)
        ]),
        NodeUsersConfig(ip="172.18.7.11", users=[
            ("rich", "sutton", True)
        ])
    ]
    users_conf = UsersConfig(users=users)
    return users_conf


if __name__ == '__main__':
    if not os.path.exists(util.default_users_path()):
        UsersGenerator.write_users_config(default_users())
    users_config = util.read_users_config(util.default_users_path())
    cluster_config = ClusterConfig(agent_ip="172.18.7.191", agent_username="pycr_admin",
                                   agent_pw="pycr@admin-pw_191", server_connection=False)
    UsersGenerator.create_users(users_config=users_config, cluster_config=cluster_config)