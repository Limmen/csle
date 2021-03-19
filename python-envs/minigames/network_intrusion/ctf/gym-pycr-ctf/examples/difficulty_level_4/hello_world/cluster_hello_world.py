from gym_pycr_ctf.envs.derived_envs.level1.simulation.pycr_ctf_level1_sim_env import PyCRCTFLevel1Sim1Env
from gym_pycr_ctf.envs.derived_envs.level1.cluster.pycr_ctf_level1_cluster_env import PyCRCTFLevel1Cluster1Env
from gym_pycr_ctf.dao.network.cluster_config import ClusterConfig
import gym
import time
import numpy as np

def test_env(env_name : str, num_steps : int):
    # cluster_config = ClusterConfig(server_ip="172.31.212.91", agent_ip="172.18.4.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
    #                                server_username="kim")
    # cluster_config = ClusterConfig(server_ip="172.31.212.91", agent_ip="172.18.4.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    cluster_config = ClusterConfig(agent_ip="172.18.4.191", agent_username="agent", agent_pw="agent",
                                   server_connection=False)
    env = gym.make(env_name, env_config=None, cluster_config=cluster_config)
    env.env_config.max_episode_length = 1000000000
    env.env_config.manual_play = False

    env.reset()

    num_actions = env.env_config.action_conf.num_actions
    actions = np.array(list(range(num_actions)))
    print("num actions:{}".format(num_actions))
    tot_rew = 0
    for i in range(num_steps):
        legal_actions = list(filter(lambda x: env.is_action_legal(x, env.env_config, env.env_state), actions))
        action = np.random.choice(legal_actions)
        obs, reward, done, info = env.step(action)
        tot_rew += reward
        env.render()
        if done:
            print("tot_rew:{}".format(tot_rew))
            tot_rew = 0
            env.reset()
        #time.sleep(0.001)
        #time.sleep(0.5)
    env.reset()
    env.close()


def test_all():
    #test_env("pycr-ctf-level-4-cluster-v1", num_steps=1000000000)
    #test_env("pycr-ctf-level-4-cluster-v2", num_steps=1000000000)
    #test_env("pycr-ctf-level-4-cluster-v3", num_steps=1000000000)
    test_env("pycr-ctf-level-4-cluster-v4", num_steps=1000000000)

if __name__ == '__main__':
    test_all()