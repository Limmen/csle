import os
from gym_pycr_pwcrack.dao.container_config.users_config import UsersConfig
from gym_pycr_pwcrack.dao.container_config.node_users_config import NodeUsersConfig
from gym_pycr_pwcrack.util.experiments_util import util
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.envs.logic.cluster.cluster_util import ClusterUtil

def connect_admin(cluster_config: ClusterConfig, ip : str):
    cluster_config.agent_ip = ip
    cluster_config.connect_agent()

def disconnect_admin(cluster_config: ClusterConfig):
    cluster_config.close()

def default_users() -> UsersConfig:
    users = [
        NodeUsersConfig(ip="172.18.3.79", users = [
            ("l_hopital", "l_hopital", True),
            ("pi", "pi", True),
            ("euler", "euler", False)
        ]),
        NodeUsersConfig(ip="172.18.3.191", users=[
            ("agent", "agent", True)
        ]),
        NodeUsersConfig(ip="172.18.3.21", users=[
            ("admin", "admin31151x", True),
            ("test", "qwerty", True),
            ("oracle", "abc123", False)
        ]),
        NodeUsersConfig(ip="172.18.3.10", users=[
            ("admin", "admin1235912", True),
            ("jessica", "water", False)
        ]),
        NodeUsersConfig(ip="172.18.3.2", users=[
            ("admin", "test32121", False),
            ("user1", "123123", True),
            ("puppet", "puppet", True)
        ]),
        NodeUsersConfig(ip="172.18.3.3", users=[
            ("admin", "admin", True),
            ("john", "doe", True),
            ("vagrant", "test_pw1", False)
        ]),
        NodeUsersConfig(ip="172.18.3.54", users=[
            ("vagrant", "vagrant", True),
            ("trent", "xe125@41!341", True)
        ]),
        NodeUsersConfig(ip="172.18.3.74", users=[
            ("administrator", "administrator", True)
        ]),
        NodeUsersConfig(ip="172.18.3.61", users=[
            ("adm", "adm", True)
        ]),
        NodeUsersConfig(ip="172.18.3.62", users=[
            ("guest", "guest", True)
        ]),
        NodeUsersConfig(ip="172.18.3.101", users=[
            ("zidane", "1b12ha9", True)
        ]),
        NodeUsersConfig(ip="172.18.3.7", users=[
            ("ec2-user", "ec2-user", True),
            ("zlatan", "pi12195e", True),
            ("kennedy", "eul1145x", False)
        ]),
        NodeUsersConfig(ip="172.18.3.4", users=[
            ("user1", "1235121", True)
        ]),
        NodeUsersConfig(ip="172.18.3.5", users=[
            ("user2", "1235121", True)
        ]),
        NodeUsersConfig(ip="172.18.3.6", users=[
            ("user3", "1bsae235121", True)
        ]),
        NodeUsersConfig(ip="172.18.3.7", users=[
            ("user4", "1bsae235121", True)
        ]),
        NodeUsersConfig(ip="172.18.3.8", users=[
            ("user5", "1gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.3.9", users=[
            ("user6", "1gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.3.11", users=[
            ("user7", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.3.12", users=[
            ("user8", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.3.13", users=[
            ("user9", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.3.14", users=[
            ("user10", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.3.15", users=[
            ("user11", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.3.16", users=[
            ("user12", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.3.17", users=[
            ("user13", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.3.18", users=[
            ("user14", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.3.19", users=[
            ("user15", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.3.20", users=[
            ("user16", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.3.28", users=[
            ("user17", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.3.22", users=[
            ("user18", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.3.23", users=[
            ("user19", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.3.24", users=[
            ("user20", "081gxq2", True)
        ]),
        NodeUsersConfig(ip="172.18.3.25", users=[
            ("user20", "081gxq2", True)
        ])
    ]
    users_conf = UsersConfig(users=users)
    return users_conf

def write_default_users_config(path:str = None) -> None:
    """
    Writes the default configuration to a json file

    :param path: the path to write the configuration to
    :return: None
    """
    if path is None:
        path = util.default_users_path()
    users_config = default_users()
    util.write_users_config_file(users_config, path)

def create_users(users_config: UsersConfig, cluster_config: ClusterConfig):
    for users_conf in users_config.users:
        connect_admin(cluster_config=cluster_config, ip=users_conf.ip)

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

        disconnect_admin(cluster_config=cluster_config)

if __name__ == '__main__':
    if not os.path.exists(util.default_users_path()):
        write_default_users_config()
    users_config = util.read_users_config(util.default_users_path())
    cluster_config = ClusterConfig(agent_ip="172.18.3.191", agent_username="pycr_admin",
                                   agent_pw="pycr@admin-pw_191", server_connection=False)
    create_users(users_config=users_config, cluster_config=cluster_config)