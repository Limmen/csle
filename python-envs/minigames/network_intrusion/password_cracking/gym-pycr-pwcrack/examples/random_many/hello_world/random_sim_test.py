from gym_pycr_pwcrack.envs.pycr_pwcrack_env import PyCRPwCrackLevel1Sim1Env, PyCRPwCrackLevel1Cluster1Env
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
import gym
import time
import numpy as np
from gym_pycr_pwcrack.util.experiments_util import util
from gym_pycr_pwcrack.envs.config.generator.env_config_generator import EnvConfigGenerator
from gym_pycr_pwcrack.envs.logic.common.domain_randomizer import DomainRandomizer

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
    max_num_nodes_train = max(list(map(lambda x: len(x.containers), containers_configs)))
    max_num_nodes_eval = max(list(map(lambda x: len(x.containers), eval_containers_configs)))
    max_num_nodes = max(max_num_nodes_train, max_num_nodes_eval)

    idx = 1
    print("ip:{}".format(containers_configs[idx].agent_ip))
    cluster_config = ClusterConfig(agent_ip=containers_configs[idx].agent_ip, agent_username="agent", agent_pw="agent",
                                   server_connection=False, port_forward_next_port=9800)
    # cluster_config = ClusterConfig(server_ip="172.31.212.92", agent_ip=containers_configs[idx].agent_ip,
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    env = gym.make(env_name, env_config=None, cluster_config=cluster_config,
                   containers_configs=containers_configs, flags_configs=flags_configs, idx=idx,
                   num_nodes=max_num_nodes)
    env.env_config.max_episode_length = 1000000000
    env.env_config.manual_play = True

    env.reset()

    num_actions = env.env_config.action_conf.num_actions
    actions = np.array(list(range(num_actions)))
    print("num actions:{}".format(num_actions))
    tot_rew = 0
    randomization_space = DomainRandomizer.generate_randomization_space([env.env_config.network_conf])
    for i in range(num_steps):
        #rint(i)
        #legal_actions = list(filter(lambda x: env.is_action_legal(x, env.env_config, env.env_state), actions))
        legal_actions = actions
        action = np.random.choice(legal_actions)
        obs, reward, done, info = env.step(action)
        tot_rew += reward
        #env.render()
        if done or (i >900 and i % 1000 == 0):
            print("env done")
            tot_rew = 0
            randomized_network_conf, env_config = DomainRandomizer.randomize(subnet_prefix="172.18.",
                                                                             network_ids=list(range(1, 254)),
                                                                             r_space=randomization_space,
                                                                             env_config=env.env_config)
            env.env_config = env_config
            env.reset()
        #time.sleep(0.001)
        #time.sleep(0.5)
    env.reset()
    env.close()


def test_all():
    #test_env("pycr-pwcrack-random-many-cluster-v1", num_steps=1000000000)
    test_env("pycr-pwcrack-random-many-generated-sim-v1", num_steps=1000000000)


if __name__ == '__main__':
    test_all()