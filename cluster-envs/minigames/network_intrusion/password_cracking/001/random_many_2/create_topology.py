from gym_pycr_pwcrack.envs.config.generator.topology_generator import TopologyGenerator
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.util.experiments_util import util

def apply_config():
    topology_config = util.read_topology(util.default_topology_path())
    containers_config = util.read_containers_config(util.default_containers_path())
    print(containers_config.agent_ip)

    cluster_config = ClusterConfig(agent_ip=containers_config.agent_ip, agent_username="pycr_admin",
                                   agent_pw="pycr@admin-pw_191", server_connection=False)
    TopologyGenerator.create_topology(topology=topology_config, cluster_config=cluster_config)

if __name__ == '__main__':
    apply_config()