import os
from pycr_common.util.experiments_util import util
from pycr_common.dao.network.emulation_config import EmulationConfig
from pycr_common.envs_model.config.generator.traffic_generator import TrafficGenerator

if __name__ == '__main__':
    if not os.path.exists(util.default_traffic_path()):
        raise ValueError("You must first generate the traffic.json file")
    traffic_config = util.read_users_config(util.default_traffic_path())
    emulation_config = EmulationConfig(agent_ip="172.18.7.191", agent_username="pycr_admin",
                                     agent_pw="pycr@admin-pw_191", server_connection=False)
    TrafficGenerator.stop_traffic_generators(traffic_config=traffic_config, emulation_config=emulation_config)