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
        NodeUsersConfig(ip="172.18.2.79", users = [
            ("l_hopital", "l_hopital", True),
            ("pi", "pi", True),
            ("euler", "euler", False)
        ]),
        NodeUsersConfig(ip="172.18.2.191", users=[
            ("agent", "agent", True)
        ]),
        NodeUsersConfig(ip="172.18.2.21", users=[
            ("admin", "admin31151x", True),
            ("test", "qwerty", True),
            ("oracle", "abc123", False)
        ]),
        NodeUsersConfig(ip="172.18.2.10", users=[
            ("admin", "admin1235912", True),
            ("jessica", "water", False)
        ]),
        NodeUsersConfig(ip="172.18.2.2", users=[
            ("admin", "test32121", False),
            ("user1", "123123", True),
            ("puppet", "puppet", True)
        ]),
        NodeUsersConfig(ip="172.18.2.3", users=[
            ("admin", "admin", True),
            ("john", "doe", True),
            ("vagrant", "test_pw1", False)
        ]),
        NodeUsersConfig(ip="172.18.2.54", users=[
            ("vagrant", "vagrant", True),
            ("trent", "xe125@41!341", True)
        ]),
        NodeUsersConfig(ip="172.18.2.74", users=[
            ("administrator", "administrator", True)
        ]),
        NodeUsersConfig(ip="172.18.2.61", users=[
            ("adm", "adm", True)
        ]),
        NodeUsersConfig(ip="172.18.2.62", users=[
            ("guest", "guest", True)
        ]),
        NodeUsersConfig(ip="172.18.2.101", users=[
            ("zidane", "1b12ha9", True)
        ]),
        NodeUsersConfig(ip="172.18.2.7", users=[
            ("ec2-user", "ec2-user", True),
            ("zlatan", "pi12195e", True),
            ("kennedy", "eul1145x", False)
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
    cluster_config = ClusterConfig(agent_ip="172.18.2.191", agent_username="pycr_admin",
                                   agent_pw="pycr@admin-pw_191", server_connection=False)
    create_users(users_config=users_config, cluster_config=cluster_config)