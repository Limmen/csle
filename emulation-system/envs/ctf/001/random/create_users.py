from csle_common.envs_model.config.generator.users_generator import UsersGenerator
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.util.experiments_util import util
import csle_common.constants.constants as constants


def apply_config():
    users_config = util.read_users_config(util.default_users_path())
    containers_config = util.read_containers_config(util.default_containers_path())

    emulation_config = EmulationConfig(agent_ip=containers_config.agent_ip, agent_username=constants.CSLE_ADMIN.USER,
                                       agent_pw=constants.CSLE_ADMIN.PW, server_connection=False)

    UsersGenerator.create_users(users_config=users_config, emulation_config=emulation_config)



if __name__ == '__main__':
    apply_config()