from gym_pycr_pwcrack.envs.pycr_pwcrack_env import PyCRPwCrackLevel1Sim1Env, PyCRPwCrackLevel1Cluster1Env
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.agents.manual.manual_attacker_agent import ManualAttackerAgent
from gym_pycr_pwcrack.util.experiments_util import util
from gym_pycr_pwcrack.envs.config.generator.env_config_generator import EnvConfigGenerator
import gym

def manual_control():
    # cluster_config = ClusterConfig(server_ip="172.31.212.91", agent_ip="172.18.1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
    #                                server_username="kim")
    # cluster_config = ClusterConfig(server_ip="172.31.212.91", agent_ip="172.18.1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
        "/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/random_many/")
    flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
        "/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/random_many/")
    eval_containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
        "/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/random_many_2/")
    eval_flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
        "/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/random_many_2/")
    max_num_nodes_train = max(list(map(lambda x: len(x.containers), containers_configs)))
    max_num_nodes_eval = max(list(map(lambda x: len(x.containers), eval_containers_configs)))
    max_num_nodes = max(max_num_nodes_train, max_num_nodes_eval)

    # cluster_config = ClusterConfig(agent_ip=containers_configs.agent_ip, agent_username="agent", agent_pw="agent",
    #                                server_connection=False, port_forward_next_port=9800,
    #                                idx=1, num_nodes=max_num_nodes)
    idx = 1
    cluster_config = ClusterConfig(server_ip="172.31.212.92", agent_ip=containers_configs[idx].agent_ip,
                                   agent_username="agent", agent_pw="agent", server_connection=True,
                                   server_private_key_file="/home/kim/.ssh/id_rsa",
                                   server_username="kim")
    env_name = "pycr-pwcrack-random-many-cluster-v1"
    env = gym.make(env_name, env_config=None, cluster_config=cluster_config,
                   containers_configs=containers_configs, flags_configs=flags_configs, idx=idx,
                   num_nodes=max_num_nodes)


    ManualAttackerAgent(env=env, env_config=env.env_config)




if __name__ == '__main__':
    manual_control()