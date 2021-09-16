from gym_pycr_ctf.util.experiments_util import util
from pycr_common.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.envs_model.config.generator.traffic_generator import TrafficGenerator


def apply_config():
    containers_config = util.read_containers_config(util.default_containers_path())
    traffic_config = util.read_traffic_config(util.default_traffic_path())
    emulation_config = EmulationConfig(agent_ip=containers_config.agent_ip, agent_username="pycr_admin",
                                       agent_pw="pycr@admin-pw_191", server_connection=False)
    TrafficGenerator.create_traffic_scripts(traffic_config=traffic_config, emulation_config=emulation_config,
                                            sleep_time=1)

if __name__ == '__main__':
    apply_config()