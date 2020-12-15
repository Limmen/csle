from gym_pycr_pwcrack.envs.pycr_pwcrack_env import PyCRPwCrackLevel1Sim1Env, PyCRPwCrackLevel1Cluster1Env
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.agents.manual.manual_attacker_agent import ManualAttackerAgent
from gym_pycr_pwcrack.util.experiments_util import util
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
    containers_config = util.read_containers_config(
        "/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/random_many/env_2_172.18.9./containers.json")
    flags_config = util.read_flags_config(
        "/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/random_many/env_2_172.18.9./flags.json")
    cluster_config = ClusterConfig(agent_ip=containers_config.agent_ip, agent_username="agent", agent_pw="agent",
                                   server_connection=False, port_forward_next_port=4600)
    env = gym.make("pycr-pwcrack-random-cluster-v1", env_config=None, cluster_config=cluster_config,
                   containers_config=containers_config, flags_config=flags_config)
    ManualAttackerAgent(env=env, env_config=env.env_config)




if __name__ == '__main__':
    manual_control()