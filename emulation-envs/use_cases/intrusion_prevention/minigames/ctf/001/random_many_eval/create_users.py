from pycr_common.envs_model.config.generator.users_generator import UsersGenerator
from pycr_common.dao.network.emulation_config import EmulationConfig
from pycr_common.util.experiments_util import util
import pycr_common.constants.constants as constants


def apply_config() -> None:
    """
    Applies the users config
    """
    users_config = util.read_users_config(util.default_users_path())
    containers_config = util.read_containers_config(util.default_containers_path())

    emulation_config = EmulationConfig(agent_ip=containers_config.agent_ip, agent_username=constants.PYCR_ADMIN.USER,
                                     agent_pw=constants.PYCR_ADMIN.PW, server_connection=False)

    UsersGenerator.create_users(users_config=users_config, emulation_config=emulation_config)



if __name__ == '__main__':
    apply_config()