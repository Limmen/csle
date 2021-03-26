from gym_pycr_ctf.envs.derived_envs.level1.simulation.pycr_ctf_level1_sim_env import PyCRCTFLevel1Sim1Env
from gym_pycr_ctf.envs.derived_envs.level1.cluster.pycr_ctf_level1_cluster_env import PyCRCTFLevel1Cluster1Env
from gym_pycr_ctf.dao.network.cluster_config import ClusterConfig
from gym_pycr_ctf.agents.manual.manual_attacker_agent import ManualAttackerAgent
import gym

def manual_control():
    # cluster_config = ClusterConfig(server_ip="172.31.212.91", agent_ip="172.18.8.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
    #                                server_username="kim")
    # cluster_config = ClusterConfig(server_ip="172.31.212.91", agent_ip="172.18.8.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    # cluster_config = ClusterConfig(agent_ip="172.18.8.191", agent_username="agent", agent_pw="agent",
    #                                port_forward_next_port=4600,
    #                                server_connection=True, warmup=False, warmup_iterations=500,
    #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
    #                                server_username="kim", server_ip="172.31.212.92"
    #                                )
    cluster_config = ClusterConfig(agent_ip="172.18.8.191", agent_username="agent", agent_pw="agent",
                                   server_connection=False, port_forward_next_port=9600)
    env = gym.make("pycr-ctf-level-8-cluster-v1", env_config=None, cluster_config=cluster_config)
    ManualAttackerAgent(env=env, env_config=env.env_config)


if __name__ == '__main__':
    manual_control()