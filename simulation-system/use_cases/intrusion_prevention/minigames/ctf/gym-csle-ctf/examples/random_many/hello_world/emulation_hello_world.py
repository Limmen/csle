from csle_common.dao.network.emulation_config import EmulationConfig
import gym
import numpy as np
from csle_common.envs_model.config.generator.env_config_generator import EnvConfigGenerator
from gym_csle_ctf.envs_model.logic.common.env_dynamics_util import EnvDynamicsUtil
import sys

def test_env(env_name : str, num_steps : int):
    # emulation_config = emulationConfig(server_ip="172.31.212.91", agent_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/csle_id_rsa",
    #                                server_username="kim")
    # emulation_config = emulationConfig(server_ip="172.31.212.91", agent_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
        "/home/kim/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many_train/")
    flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
        "/home/kim/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many_train/")
    # containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
    #     "/home/kim/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many_train/")
    # flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
    #     "/home/kim/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many_train/")
    print(list(map(lambda x: x.agent_ip, containers_configs)))
    sys.exit(0)
    # containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
    #     "/home/kim/storage/workspace/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many_eval/")
    # flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
    #     "/home/kim/storage/workspace/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many_eval/")
    max_num_nodes_train = max(list(map(lambda x: len(x.containers), containers_configs)))
    max_num_nodes_eval = max(list(map(lambda x: len(x.containers), containers_configs)))
    #max_num_nodes = max(max_num_nodes_train, max_num_nodes_eval)
    #max_num_nodes = max_num_nodes_train
    max_num_nodes = max_num_nodes_eval

    idx = 2
    print("ip:{}".format(containers_configs[idx].agent_ip))
    #sys.exit(0)
    emulation_config = EmulationConfig(agent_ip=containers_configs[idx].agent_ip, agent_username="agent",
                                       agent_pw="agent", server_connection=False,
                                       port_forward_next_port=1547,
                                       save_dynamics_model_dir="/home/kim/csle/simulation-system/use_cases/intrusion_prevention/minigames/ctf/gym-csle-ctf/examples/random_many/hello_world/",
                                       save_dynamics_model_file="defender_dynamics_model_" + str(idx) + ".json",
                                       save_netconf_file="network_conf_" + str(idx) + ".pickle",
                                       save_trajectories_file="taus_" + str(idx) + ".json",
                                       skip_exploration=False
                                       )
    # emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip=containers_configs[idx].agent_ip,
    #                                  agent_username="agent", agent_pw="agent", server_connection=True,
    #                                  server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                  server_username="kim", port_forward_next_port=1147)
    env = gym.make(env_name, env_config=None, emulation_config=emulation_config,
                   containers_configs=containers_configs, flags_configs=flags_configs, idx=idx,
                   num_nodes=max_num_nodes)
    env.env_config.max_episode_length = 1000000000
    env.env_config.manual_play = True

    env.reset()

    for n2 in env.env_config.network_conf.nodes:
        print("node:{}, flags:{}".format(n2.internal_ip, list(map(lambda x: str(x), n2.flags))))

    num_actions = env.env_config.attacker_action_conf.num_actions
    actions = np.array(list(range(num_actions)))
    print("num actions:{}".format(num_actions))
    tot_rew = 0
    tried_actions = []
    for i in range(num_steps):
        #print(i)
        legal_actions = list(filter(lambda x: env.is_attack_action_legal(x, env.env_config, env.env_state), actions))
        if len(legal_actions) == 0:
            print("no legal actions, {}".format(tried_actions))
            print(env.env_state.attacker_obs_state.actions_tried)
            for m in env.env_state.attacker_obs_state.machines:
                print(
                    "ip: {}, shell access:{}, root:{}, ssh_brute_t:{}, ftp_brute_t:{}, telnet_brute_t:{}, "
                    "samba_tried:{},shellsock_tried:{},dvwa_sql_injection_tried:{},"
                    "cve_2015_3306_tried:{}, cve_2015_1427_tried:{}, cve_2016_10033_tried:{},"
                    "cve_2010_0426_tried:{},cve_2015_5602_tried:{},"
                    "fs_searched:{},untried_cred:{},logged_in:{},"
                    "tools:{},backdoor:{},flags found:{}".format(
                        m.internal_ip, m.shell_access, m.root, m.telnet_brute_tried, m.ssh_brute_tried, m.ftp_brute_tried,
                        m.sambacry_tried, m.shellshock_tried, m.dvwa_sql_injection_tried,
                        m.cve_2015_3306_tried, m.cve_2015_1427_tried,
                        m.cve_2016_10033_tried, m.cve_2010_0426_tried, m.cve_2015_5602_tried,
                        m.filesystem_searched, m.untried_credentials,
                        m.logged_in, m.tools_installed, m.backdoor_installed, m.flags_found))
            print("all flags?:{}".format(
                EnvDynamicsUtil.is_all_flags_collected(s=env.env_state, env_config=env.env_config)))
            print("done?:{}".format(done))
        #legal_actions = actions
        attacker_action = np.random.choice(legal_actions)
        action = (attacker_action, None)
        obs, reward, done, info = env.step(action)
        tried_actions.append(attacker_action)
        attacker_reward, defender_reward = reward
        tot_rew += attacker_reward
        #env.render()
        if done:
            print("done:{}".format(tot_rew))
            tot_rew = 0
            env.reset()
            tried_actions = []
        #time.sleep(0.001)
        #time.sleep(0.5)
    env.reset()
    env.close()


def test_all():
    #test_env("csle-ctf-random-many-emulation-v1", num_steps=1000000000)
    test_env("csle-ctf-random-many-generated-sim-v1", num_steps=1000000000)


if __name__ == '__main__':
    test_all()