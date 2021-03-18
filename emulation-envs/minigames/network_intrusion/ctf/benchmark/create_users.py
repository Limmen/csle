from gym_pycr_ctf.envs.config.generator.users_generator import UsersGenerator
from gym_pycr_ctf.dao.network.cluster_config import ClusterConfig
from gym_pycr_ctf.util.experiments_util import util

def apply_config():
    users_config = util.read_users_config(util.default_users_path())
    containers_config = util.read_containers_config(util.default_containers_path())

    cluster_config = ClusterConfig(agent_ip=containers_config.agent_ip, agent_username="pycr_admin",
                                   agent_pw="pycr@admin-pw_191", server_connection=False)

    UsersGenerator.create_users(users_config=users_config, cluster_config=cluster_config)



if __name__ == '__main__':
    apply_config()