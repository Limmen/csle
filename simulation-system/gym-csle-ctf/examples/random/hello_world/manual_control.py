from csle_common.dao.network.emulation_config import EmulationConfig
from gym_csle_ctf.agents.manual.manual_attacker_agent import ManualAttackerAgent
from csle_common.util.experiments_util import util
from csle_common.envs_model.config.generator.env_config_generator import EnvConfigGenerator
import gym

def manual_control():
    # emulation_config = emulationConfig(server_ip="172.31.212.91", agent_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/csle_id_rsa",
    #                                server_username="kim")
    # emulation_config = emulationConfig(server_ip="172.31.212.91", agent_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
        "/home/kim/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many/")
    flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
        "/home/kim/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many/")
    eval_containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
        "/home/kim/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many_2/")
    eval_flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
        "/home/kim/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many_2/")
    containers_config = util.read_containers_config("/home/kim/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many/env_0_172.18.2./containers.json")
    flags_config = util.read_flags_config("/home/kim/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many/env_0_172.18.2./flags.json")
    max_num_nodes_train = max(list(map(lambda x: len(x.containers), containers_configs)))
    max_num_nodes_eval = max(list(map(lambda x: len(x.containers), eval_containers_configs)))
    max_num_nodes = max(max_num_nodes_train, max_num_nodes_eval)
    emulation_config = EmulationConfig(agent_ip=containers_config.agent_ip, agent_username="agent", agent_pw="agent",
                                     server_connection=False, port_forward_next_port=9600)
    env = gym.make("csle-ctf-random-emulation-v1", env_config=None, emulation_config=emulation_config,
                   containers_config=containers_config, flags_config=flags_config, num_nodes=max_num_nodes)
    ManualAttackerAgent(env=env, env_config=env.env_config)




if __name__ == '__main__':
    manual_control()