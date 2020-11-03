from gym_pycr_pwcrack.envs.pycr_pwcrack_env import PyCRPwCrackSimpleSim1Env, PyCRPwCrackSimpleCluster1Env
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
import gym
import time
import numpy as np

def test_env(env_name : str, num_steps : int):
    # cluster_config = ClusterConfig(server_ip="172.31.212.91", agent_ip="172.18.1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
    #                                server_username="kim")
    # cluster_config = ClusterConfig(server_ip="172.31.212.91", agent_ip="172.18.1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    cluster_config = ClusterConfig(agent_ip="172.18.1.191", agent_username="agent", agent_pw="agent",
                                   server_connection=False)
    env = gym.make(env_name, env_config=None, cluster_config=cluster_config)
    env.env_config.max_episode_length = 1000000000
    env.env_config.manual_play = True



    env.reset()

    num_actions = env.env_config.action_conf.num_actions
    actions = np.array(list(range(num_actions)))
    print("num actions:{}".format(num_actions))
    # actions = np.array([0,1,2,3,4,5,6, 7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,
    #                     34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,
    #                     63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,
    #                     92,93,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,
    #                     116,117,118,119,120,121,122,123,124,125,126,127,134,135,136,137,138,139, 140, 141, 142, 143, 144])
    #actions = np.array([127])
    #actions = np.array([119,120,121,122,123,124,125])
    for i in range(num_steps):
        legal_actions = list(filter(lambda x: env.is_action_legal(x, env.env_config, env.env_state), actions))
        action = np.random.choice(legal_actions)
        obs, reward, done, info = env.step(action)
        env.render()
        if done:
            env.reset()
        time.sleep(0.001)
        #time.sleep(0.5)
    env.reset()
    env.close()


def test_all():
    #test_env("pycr-pwcrack-simple-sim-v1", num_steps=1000000000)
    test_env("pycr-pwcrack-simple-cluster-v1", num_steps=1000000000)
    #test_env("pycr-pwcrack-simple-cluster-v2", num_steps=1000000000)
    #test_env("pycr-pwcrack-simple-cluster-base-v1", num_steps=1000000000)
    #test_env("pycr-pwcrack-simple-cluster-v3", num_steps=1000000000)
    #test_env("pycr-pwcrack-simple-cluster-v4", num_steps=1000000000)

if __name__ == '__main__':
    test_all()