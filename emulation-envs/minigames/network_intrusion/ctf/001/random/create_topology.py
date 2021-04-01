from gym_pycr_ctf.envs_model.config.generator.topology_generator import TopologyGenerator
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.util.experiments_util import util

def apply_config():
    topology_config = util.read_topology(util.default_topology_path())
    containers_config = util.read_containers_config(util.default_containers_path())
    print(containers_config.agent_ip)

    emulation_config = EmulationConfig(agent_ip=containers_config.agent_ip, agent_username="pycr_admin",
                                     agent_pw="pycr@admin-pw_191", server_connection=False)
    TopologyGenerator.create_topology(topology=topology_config, emulation_config=emulation_config)

if __name__ == '__main__':
    apply_config()