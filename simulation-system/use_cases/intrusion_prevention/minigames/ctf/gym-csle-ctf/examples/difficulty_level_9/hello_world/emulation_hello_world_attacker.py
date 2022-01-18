from csle_common.dao.network.emulation_config import EmulationConfig
import gym
import numpy as np
import sys
from gym_csle_ctf.envs_model.logic.common.env_dynamics_util import EnvDynamicsUtil

def test_env(env_name : str, num_steps : int):
    # emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}9.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/csle_id_rsa",
    #                                server_username="kim")
    # emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}9.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    emulation_config = EmulationConfig(agent_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}9.191", agent_username="agent", agent_pw="agent",
                                     server_connection=False, port_forward_next_port=3200)

    # emulation_config.save_dynamics_model_dir = "/home/kim/storage/workspace/csle/simulation-system/minigames/" \
    #                                            "network_intrusion/ctf/gym-csle-ctf/examples/difficulty_level_9/" \
    #                                            "hello_world/"
    emulation_config.save_dynamics_model_dir = "/home/kim/csle/simulation-system/use_cases/intrusion_prevention/minigames/ctf/" \
                                               "gym-csle-ctf/examples/difficulty_level_9/hello_world/"
    emulation_config.skip_exploration = False
    env = gym.make(env_name, env_config=None, emulation_config=emulation_config)
    env.env_config.max_episode_length = 1000000000
    env.env_config.manual_play = False

    env.reset()

    num_actions = env.env_config.attacker_action_conf.num_actions
    actions = np.array(list(range(num_actions)))
    print("num actions:{}".format(num_actions))
    tot_rew = 0
    tried_actions = []
    for i in range(num_steps):
        #print("i:{}".format(i))
        legal_actions = list(filter(lambda x: env.is_attack_action_legal(x, env.env_config, env.env_state), actions))
        if len(legal_actions) == 0:
            print("no legal actions, {}".format(tried_actions))
            print(env.env_state.attacker_obs_state.actions_tried)
            for m in env.env_state.attacker_obs_state.machines:
                print(
                    "ip: {}, shell access:{}, ssh_brute_t:{}, ftp_brute_t:{}, telnet_brute_t:{}, "
                    "samba_tried:{},shellsock_tried:{},dvwa_sql_injection_tried:{},"
                    "cve_2015_3306_tried:{}, cve_2015_1427_tried:{}, cve_2016_10033_tried:{},"
                    "cve_2010_0426_tried:{},cve_2015_5602_tried:{}"
                    "fs_searched:{},untried_cred:{},logged_in:{},"
                    "tools:{},backdoor:{},flags found:{}".format(
                        m.internal_ip, m.shell_access, m.telnet_brute_tried, m.ssh_brute_tried, m.ftp_brute_tried,
                        m.sambacry_tried, m.shellshock_tried, m.dvwa_sql_injection_tried,
                        m.cve_2015_3306_tried, m.cve_2015_1427_tried,
                        m.cve_2016_10033_tried, m.cve_2010_0426_tried, m.cve_2015_5602_tried,
                        m.filesystem_searched, m.untried_credentials,
                        m.logged_in, m.tools_installed, m.backdoor_installed, m.flags_found))
            print("all flags?:{}".format(
                EnvDynamicsUtil.is_all_flags_collected(s=env.env_state, env_config=env.env_config)))
            print("done?:{}".format(done))

        attacker_action = np.random.choice(legal_actions)
        defender_action = None
        action = (attacker_action, defender_action)
        # if i < 1:
        #     action = 21
        # else:
        #     action = 40
        #env.render()
        print("a:{}".format(attacker_action))
        obs, reward, done, info = env.step(action)
        sys.stdout.flush()
        attacker_reward, _ = reward
        tried_actions.append(attacker_action)
        tot_rew += attacker_reward
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
    #test_env("csle-ctf-level-9-emulation-v1", num_steps=1000000000)
    #test_env("csle-ctf-level-9-emulation-v2", num_steps=1000000000)
    #test_env("csle-ctf-level-9-emulation-v3", num_steps=1000000000)
    #test_env("csle-ctf-level-9-emulation-v1", num_steps=1000000000)
    #test_env("csle-ctf-level-9-generated-sim-v1", num_steps=1000000000)
    test_env("csle-ctf-level-9-generated-sim-v5", num_steps=1000000000)

if __name__ == '__main__':
    test_all()

# Test case: 99,33,1,70,104,105,106,107,99,165,200,58,104,105,106,331,99,266,104,105,106,99,113,104,105