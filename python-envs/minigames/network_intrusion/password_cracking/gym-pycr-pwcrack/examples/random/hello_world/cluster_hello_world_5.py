from gym_pycr_pwcrack.envs.pycr_pwcrack_env import PyCRPwCrackLevel1Sim1Env, PyCRPwCrackLevel1Cluster1Env
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
import gym
import time
import numpy as np
from gym_pycr_pwcrack.util.experiments_util import util
from gym_pycr_pwcrack.envs.config.generator.env_config_generator import EnvConfigGenerator

def test_env(env_name : str, num_steps : int):
    # cluster_config = ClusterConfig(server_ip="172.31.212.91", agent_ip="172.18.1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
    #                                server_username="kim")
    # cluster_config = ClusterConfig(server_ip="172.31.212.91", agent_ip="172.18.1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
        "/home/kim/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/random_many/")
    flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
        "/home/kim/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/random_many/")
    eval_containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
        "/home/kim/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/random_many_2/")
    eval_flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
        "/home/kim/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/random_many_2/")
    containers_config = util.read_containers_config(
        "/home/kim/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/random_many/env_4_172.18.9./containers.json")
    flags_config = util.read_flags_config(
        "/home/kim/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/random_many/env_4_172.18.9./flags.json")
    max_num_nodes_train = max(list(map(lambda x: len(x.containers), containers_configs)))
    max_num_nodes_eval = max(list(map(lambda x: len(x.containers), eval_containers_configs)))
    max_num_nodes = max(max_num_nodes_train, max_num_nodes_eval)
    cluster_config = ClusterConfig(agent_ip=containers_config.agent_ip, agent_username="agent", agent_pw="agent",
                                   server_connection=False, port_forward_next_port=7300)
    env = gym.make(env_name, env_config=None, cluster_config=cluster_config,
                   containers_config=containers_config, flags_config=flags_config, num_nodes=max_num_nodes)
    env.env_config.max_episode_length = 1000000000
    env.env_config.manual_play = True

    env.reset()

    num_actions = env.env_config.action_conf.num_actions
    actions = np.array(list(range(num_actions)))
    print("num actions:{}".format(num_actions))
    tot_rew = 0
    for i in range(num_steps):
        print(i)
        legal_actions = list(filter(lambda x: env.is_action_legal(x, env.env_config, env.env_state), actions))
        action = np.random.choice(legal_actions)
        obs, reward, done, info = env.step(action)
        tot_rew += reward
        #env.render()
        if done:
            print("done")
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