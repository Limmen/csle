import threading
from gym_pycr_pwcrack.envs.pycr_pwcrack_env import PyCRPwCrackLevel1Sim1Env, PyCRPwCrackLevel1Cluster1Env
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.envs.logic.common.env_dynamics_util import EnvDynamicsUtil
import gym
import numpy as np
import random
import time

class ExploreThread(threading.Thread):

    def __init__(self, env_name: str, num_steps: int, port_start):
        threading.Thread.__init__(self)
        self.env_name = env_name
        self.num_steps = num_steps
        self.port_start = port_start

    def run(self):
        # cluster_config = ClusterConfig(server_ip="172.31.212.91", agent_ip="172.18.3g.191",
        #                                agent_username="agent", agent_pw="agent", server_connection=True,
        #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
        #                                server_username="kim")
        # cluster_config = ClusterConfig(server_ip="172.31.212.91", agent_ip="172.18.3.191",
        #                                agent_username="agent", agent_pw="agent", server_connection=True,
        #                                server_private_key_file="/home/kim/.ssh/id_rsa",
        #                                server_username="kim")
        cluster_config = ClusterConfig(agent_ip="172.18.3.191", agent_username="agent", agent_pw="agent",
                                       server_connection=False, port_forward_next_port=self.port_start)
        env = gym.make(self.env_name, env_config=None, cluster_config=cluster_config)
        env.env_config.max_episode_length = 1000000000
        env.reset()
        num_actions = env.env_config.action_conf.num_actions
        actions = np.array(list(range(num_actions)))
        print("num actions:{}".format(num_actions))
        masscan_actions = [251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262]
        trajectory = []
        for i in range(self.num_steps):
            print(i)
            legal_actions = list(filter(lambda x: env.is_action_legal(x, env.env_config, env.env_state), actions))

            legal_actions = list(filter(lambda x: not x in masscan_actions, legal_actions))
            if len(legal_actions) == 0:
                print("cont, trajectory:{}".format(trajectory))
                print("all actions illegal, actions tried: ")
                print(env.env_state.obs_state.actions_tried)
                for m in env.env_state.obs_state.machines:
                    print(
                        "ip: {}, shell access:{}, ssh_brute_t:{}, ftp_brute_t:{}, telnet_brute_t:{}, fs_searched:{},untried_cred:{},logged_in:{},"
                        "tools:{},backdoor:{}, flags found:{}".format(
                            m.ip, m.shell_access, m.telnet_brute_tried, m.ssh_brute_tried, m.ftp_brute_tried,
                            m.filesystem_searched, m.untried_credentials,
                            m.logged_in, m.tools_installed, m.backdoor_installed, m.flags_found))
                print("all flags?:{}".format(
                    EnvDynamicsUtil.is_all_flags_collected(s=env.env_state, env_config=env.env_config)))
                env.reset()
                trajectory = []
                continue
            action = np.random.choice(legal_actions)
            obs, reward, done, info = env.step(action)
            if not done and EnvDynamicsUtil.is_all_flags_collected(s=env.env_state, env_config=env.env_config):
                print("not done but got all flags???")
            trajectory.append(action)
            #env.render()
            if done:
                print("done")
                env.reset()
                trajectory = []
            # time.sleep(0.001)
        env.reset()
        env.close()


def start_explore_threads(num_threads : int, env_name : str, num_steps: int = 10000000):
    threads = []
    for thread_id in range(num_threads):
        # Seed python RNG
        random.seed(thread_id*67)
        # Seed numpy RNG
        np.random.seed(thread_id*67)
        thread = ExploreThread(env_name=env_name, num_steps = num_steps, port_start=7200 + thread_id*100)
        thread.start()
        time.sleep(120)
        threads.append(thread)
    for t in threads:
        t.join()

if __name__ == '__main__':
    start_explore_threads(num_threads=15, env_name="pycr-pwcrack-level-3-cluster-v4",
                          num_steps=10000000)
