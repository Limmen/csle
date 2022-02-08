from csle_common.envs_model.config.generator.topology_generator import TopologyGenerator
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.util.experiments_util import util
import csle_common.constants.constants as constants


def apply_config() -> None:
    """
    Applies the Topology config
    """
    topology_config = util.read_topology(util.default_topology_path())
    containers_config = util.read_containers_config(util.default_containers_path())
    print(containers_config.agent_ip)

    emulation_config = EmulationConfig(agent_ip=containers_config.agent_ip, agent_username=constants.CSLE_ADMIN.USER,
                                       agent_pw=constants.CSLE_ADMIN.PW, server_connection=False)
    TopologyGenerator.create_topology(topology=topology_config, emulation_config=emulation_config)

# Applies the topology config
if __name__ == '__main__':
    apply_config()