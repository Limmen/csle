from gym_pycr_ctf.envs.config.generator.flags_generator import FlagsGenerator
from gym_pycr_ctf.dao.network.cluster_config import ClusterConfig
from gym_pycr_ctf.util.experiments_util import util

def apply_config():
    flags_config = util.read_flags_config(util.default_flags_path())
    containers_config = util.read_containers_config(util.default_containers_path())

    cluster_config = ClusterConfig(agent_ip=containers_config.agent_ip, agent_username="pycr_admin",
                                   agent_pw="pycr@admin-pw_191", server_connection=False)

    FlagsGenerator.create_flags(flags_config=flags_config, cluster_config=cluster_config)

if __name__ == '__main__':
    apply_config()