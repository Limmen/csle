from gym_pycr_ctf.envs.derived_envs.level1.simulation.pycr_ctf_level1_sim_env import PyCRCTFLevel1Sim1Env
from gym_pycr_ctf.envs.derived_envs.level1.cluster.pycr_ctf_level1_cluster_env import PyCRCTFLevel1Cluster1Env
from gym_pycr_ctf.dao.network.cluster_config import ClusterConfig
import gym
import time
import numpy as np
from gym_pycr_ctf.envs.logic.common.env_dynamics_util import EnvDynamicsUtil

def test_env(env_name : str, num_steps : int):
    # cluster_config = ClusterConfig(server_ip="172.31.212.92", agent_ip="172.18.8.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
    #                                server_username="kim")
    # cluster_config = ClusterConfig(server_ip="172.31.212.92", agent_ip="172.18.8.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    cluster_config = ClusterConfig(agent_ip="172.18.8.191", agent_username="agent", agent_pw="agent",
                                   server_connection=False)
    env = gym.make(env_name, env_config=None, cluster_config=cluster_config)
    env.env_config.max_episode_length = 1000000000
    env.env_config.manual_play = False

    env.reset()

    num_actions = env.env_config.action_conf.num_actions
    actions = np.array(list(range(num_actions)))
    print("num actions:{}".format(num_actions))
    tot_rew = 0
    tried_actions = []
    for i in range(num_steps):
        #print("i:{}".format(i))
        legal_actions = list(filter(lambda x: env.is_action_legal(x, env.env_config, env.env_state), actions))
        if len(legal_actions) == 0:
            print("no legal actions, {}".format(tried_actions))
            print(env.env_state.obs_state.actions_tried)
            for m in env.env_state.obs_state.machines:
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

        action = np.random.choice(legal_actions)
        # if i < 1:
        #     action = 21
        # else:
        #     action = 40
        #env.render()
        print("a:{}".format(action))
        obs, reward, done, info = env.step(action)
        tried_actions.append(action)
        tot_rew += reward
        if EnvDynamicsUtil.is_all_flags_collected(s=env.env_state, env_config=env.env_config) and not done:
            print("All flags but done")
        if done:
            print("tot_rew:{}".format(tot_rew))
            tot_rew = 0
            env.reset()
            tried_actions = []
            done = False
        #time.sleep(0.001)
        #time.sleep(0.5)
    env.reset()
    env.close()


def test_all():
    #test_env("pycr-ctf-level-8-cluster-v1", num_steps=1000000000)
    #test_env("pycr-ctf-level-8-cluster-v2", num_steps=1000000000)
    #test_env("pycr-ctf-level-8-cluster-v3", num_steps=1000000000)
    test_env("pycr-ctf-level-8-cluster-v1", num_steps=1000000000)

if __name__ == '__main__':
    test_all()