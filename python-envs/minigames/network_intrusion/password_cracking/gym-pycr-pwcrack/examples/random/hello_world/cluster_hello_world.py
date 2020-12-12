from gym_pycr_pwcrack.envs.pycr_pwcrack_env import PyCRPwCrackLevel1Sim1Env, PyCRPwCrackLevel1Cluster1Env
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
import gym
import time
import numpy as np
from gym_pycr_pwcrack.util.experiments_util import util

def test_env(env_name : str, num_steps : int):
    # cluster_config = ClusterConfig(server_ip="172.31.212.91", agent_ip="172.18.1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
    #                                server_username="kim")
    # cluster_config = ClusterConfig(server_ip="172.31.212.91", agent_ip="172.18.1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    containers_config = util.read_containers_config(
        "/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/random_many/env_0_172.18.5./containers.json")
    flags_config = util.read_flags_config(
        "/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/random_many/env_0_172.18.5./flags.json")
    cluster_config = ClusterConfig(agent_ip=containers_config.agent_ip, agent_username="agent", agent_pw="agent",
                                   server_connection=False, port_forward_next_port=9600)
    env = gym.make(env_name, env_config=None, cluster_config=cluster_config,
                   containers_config=containers_config, flags_config=flags_config)
    env.env_config.max_episode_length = 1000000000
    env.env_config.manual_play = True

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
            tot_rew = 0
            env.reset()
        #time.sleep(0.001)
        #time.sleep(0.5)
    env.reset()
    env.close()


def test_all():
    test_env("pycr-pwcrack-random-cluster-v1", num_steps=1000000000)

if __name__ == '__main__':
    test_all()