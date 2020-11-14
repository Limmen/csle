from gym_pycr_pwcrack.envs.pycr_pwcrack_env import PyCRPwCrackSimpleSim1Env, PyCRPwCrackSimpleCluster1Env
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.envs.logic.cluster.cluster_util import ClusterUtil
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
    cmd = "sudo find / -name 'flag*.txt'  2>&1 | grep -v 'Permission denied'"
    for i in range(100):
        outdata, errdata, total_time = ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)
        flags = outdata.decode().split("\n")
        print("outdata:{}".format(flags))
        # if "flag191.txt" not in outdata:
        #     print("error: {}".format(outdata))

    # num_actions = env.env_config.action_conf.num_actions
    # actions = np.array(list(range(num_actions)))
    # print("num actions:{}".format(num_actions))
    # for i in range(num_steps):
    #     legal_actions = list(filter(lambda x: env.is_action_legal(x, env.env_config, env.env_state), actions))
    #     action = np.random.choice(legal_actions)
    #     obs, reward, done, info = env.step(action)
    #     env.render()
    #     if done:
    #         env.reset()
    #     #time.sleep(0.001)
    #     #time.sleep(0.5)
    # env.reset()
    # env.close()


def test_all():
    #test_env("pycr-pwcrack-simple-sim-v1", num_steps=1000000000)
    #test_env("pycr-pwcrack-simple-cluster-v1", num_steps=1000000000)
    #test_env("pycr-pwcrack-simple-cluster-v2", num_steps=1000000000)
    #test_env("pycr-pwcrack-simple-cluster-base-v1", num_steps=1000000000)
    #test_env("pycr-pwcrack-simple-cluster-v3", num_steps=1000000000)
    test_env("pycr-pwcrack-simple-cluster-v1", num_steps=1000000000)
    #test_env("pycr-pwcrack-simple-generated-sim-v1", num_steps=1000000000)

if __name__ == '__main__':
    test_all()