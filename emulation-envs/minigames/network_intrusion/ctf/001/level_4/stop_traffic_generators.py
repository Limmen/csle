import os
from gym_pycr_ctf.util.experiments_util import util
from gym_pycr_ctf.dao.network.cluster_config import ClusterConfig
from gym_pycr_ctf.envs.config.generator.traffic_generator import TrafficGenerator

if __name__ == '__main__':
    if not os.path.exists(util.default_traffic_path()):
        raise ValueError("You must first generate the traffic.json file")
    traffic_config = util.read_users_config(util.default_traffic_path())
    cluster_config = ClusterConfig(agent_ip="172.18.4.191", agent_username="pycr_admin",
                                   agent_pw="pycr@admin-pw_191", server_connection=False)
    TrafficGenerator.stop_traffic_generators(traffic_config=traffic_config, cluster_config=cluster_config)