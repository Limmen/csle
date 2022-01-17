from csle_common.util.experiments_util import util
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.config.generator.traffic_generator import TrafficGenerator
import csle_common.constants.constants as constants


def apply_config() -> None:
    """
    Applies the traffic config
    """
    containers_config = util.read_containers_config(util.default_containers_path())
    traffic_config = util.read_traffic_config(util.default_traffic_path())
    emulation_config = EmulationConfig(agent_ip=containers_config.agent_ip, agent_username=constants.CSLE_ADMIN.USER,
                                       agent_pw=constants.CSLE_ADMIN.PW, server_connection=False)
    TrafficGenerator.create_traffic_scripts(traffic_config=traffic_config, emulation_config=emulation_config,
                                            sleep_time=1)

# Applies the traffic config
if __name__ == '__main__':
    apply_config()