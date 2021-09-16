from pycr_common.envs_model.config.generator.users_generator import UsersGenerator
from pycr_common.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.util.experiments_util import util

def apply_config():
    users_config = util.read_users_config(util.default_users_path())
    containers_config = util.read_containers_config(util.default_containers_path())

    emulation_config = EmulationConfig(agent_ip=containers_config.agent_ip, agent_username="pycr_admin",
                                     agent_pw="pycr@admin-pw_191", server_connection=False)

    UsersGenerator.create_users(users_config=users_config, emulation_config=emulation_config)



if __name__ == '__main__':
    apply_config()