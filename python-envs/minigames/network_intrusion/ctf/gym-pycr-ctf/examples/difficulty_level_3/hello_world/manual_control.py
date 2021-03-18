from gym_pycr_ctf.envs.pycr_ctf_env import PyCRctfLevel1Sim1Env, PyCRctfLevel1Cluster1Env
from gym_pycr_ctf.dao.network.cluster_config import ClusterConfig
from gym_pycr_ctf.agents.manual.manual_attacker_agent import ManualAttackerAgent
import gym

def manual_control():
    # cluster_config = ClusterConfig(server_ip="172.31.212.91", agent_ip="172.18.3.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
    #                                server_username="kim")
    # cluster_config = ClusterConfig(server_ip="172.31.212.91", agent_ip="172.18.3.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    # cluster_config = ClusterConfig(agent_ip="172.18.3.191", agent_username="agent", agent_pw="agent",
    #                                server_connection=False)
    # cluster_config = ClusterConfig(server_ip="172.31.212.92", agent_ip="172.18.3.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    cluster_config = ClusterConfig(server_ip="172.31.212.92", agent_ip="172.18.3.191",
                                   agent_username="agent", agent_pw="agent", server_connection=True,
                                   server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
                                   server_username="kim")

    #env = gym.make("pycr-ctf-level-2-cluster-base-v1", env_config=None, cluster_config=cluster_config)
    env = gym.make("pycr-ctf-level-3-cluster-v4", env_config=None, cluster_config=cluster_config)
    #env = gym.make("pycr-ctf-level-2-sim-v1", env_config=None, cluster_config=cluster_config)

    #env = gym.make("pycr-ctf-level-2-sim-base-v1", env_config=None)
    ManualAttackerAgent(env=env, env_config=env.env_config)




if __name__ == '__main__':
    manual_control()