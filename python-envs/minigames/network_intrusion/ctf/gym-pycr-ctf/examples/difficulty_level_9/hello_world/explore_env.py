import threading
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.envs_model.logic.common.env_dynamics_util import EnvDynamicsUtil
import gym
import numpy as np
import random
import time
import sys

class ExploreThread(threading.Thread):

    def __init__(self, env_name: str, num_steps: int, port_start):
        threading.Thread.__init__(self)
        self.env_name = env_name
        self.num_steps = num_steps
        self.port_start = port_start

    def run(self):
        # emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip="172.18.9.191",
        #                                agent_username="agent", agent_pw="agent", server_connection=True,
        #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
        #                                server_username="kim")
        # emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip="172.18.9.191",
        #                                agent_username="agent", agent_pw="agent", server_connection=True,
        #                                server_private_key_file="/home/kim/.ssh/id_rsa",
        #                                server_username="kim")
        emulation_config = EmulationConfig(agent_ip="172.18.9.191", agent_username="agent", agent_pw="agent",
                                           server_connection=False)
        env = gym.make(self.env_name, env_config=None, emulation_config=emulation_config)
        env.env_config.max_episode_length = 1000000000
        env.reset()
        num_actions = env.env_config.attacker_action_conf.num_actions
        actions = np.array(list(range(num_actions)))
        print("num actions:{}".format(num_actions))
        trajectory = []
        done = False
        for i in range(self.num_steps):
            print(i)
            legal_actions = list(filter(lambda x: env.is_attack_action_legal(x, env.env_config, env.env_state), actions))
            if len(legal_actions) == 0:
                print("cont, trajectory:{}".format(trajectory))
                print("all actions illegal, actions tried: ")
                print(env.env_state.attacker_obs_state.actions_tried)
                for m in env.env_state.attacker_obs_state.machines:
                    print(
                        "ip: {}, shell access:{}, ssh_brute_t:{}, ftp_brute_t:{}, telnet_brute_t:{}, "
                        "samba_tried:{},shellsock_tried:{},dvwa_sql_injection_tried:{},"
                        "cve_2015_3306_tried:{}, cve_2015_1427_tried:{}, cve_2016_10033_tried:{},"
                        "cve_2010_0426_tried:{},cve_2015_5602_tried:{}"
                        "fs_searched:{},untried_cred:{},logged_in:{},"
                        "tools:{},backdoor:{},flags found:{}".format(
                            m.ip, m.shell_access, m.telnet_brute_tried, m.ssh_brute_tried, m.ftp_brute_tried,
                            m.sambacry_tried, m.shellshock_tried, m.dvwa_sql_injection_tried,
                            m.cve_2015_3306_tried, m.cve_2015_1427_tried,
                            m.cve_2016_10033_tried, m.cve_2010_0426_tried, m.cve_2015_5602_tried,
                            m.filesystem_searched, m.untried_credentials,
                            m.logged_in, m.tools_installed, m.backdoor_installed, m.flags_found))
                    print("all flags?:{}".format(
                        EnvDynamicsUtil.is_all_flags_collected(s=env.env_state, env_config=env.env_config)))
                    print("done?:{}".format(done))
                env.reset()
                trajectory = []
                continue
            attacker_action = np.random.choice(legal_actions)
            action = (attacker_action, None)
            obs, reward, done, info = env.step(action)
            sys.stdout.flush()
            attacker_reward, defender_reward = reward
            if not done and EnvDynamicsUtil.is_all_flags_collected(s=env.env_state, env_config=env.env_config):
                print("not done but got all flags???")
            trajectory.append(attacker_action)
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
    start_explore_threads(num_threads=15, env_name="pycr-ctf-level-9-emulation-v1",
                          num_steps=10000000)
