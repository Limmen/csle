import gym
import numpy as np
import sys
from pycr_common.dao.network.emulation_config import EmulationConfig

def test_env(env_name : str, num_steps : int):
    # emulation_config = EmulationConfig(server_ip="172.31.212.91", agent_ip="172.18.4.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
    #                                server_username="kim")
    # emulation_config = EmulationConfig(server_ip="172.31.212.91", agent_ip="172.18.4.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    emulation_config = EmulationConfig(agent_ip="172.18.4.191", agent_username="agent", agent_pw="agent",
                                     server_connection=False)
    # emulation_config.save_dynamics_model_dir = "/home/kim/pycr/python-envs/use_cases/intrusion_prevention/minigames/ctf/" \
    #                                            "gym-pycr-ctf/examples/difficulty_level_4/hello_world/"
    emulation_config.save_dynamics_model_dir = "/home/kim/storage/workspace/pycr/python-envs/minigames/" \
                                               "network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_4/" \
                                               "hello_world/"
    env = gym.make(env_name, env_config=None, emulation_config=emulation_config)
    env.env_config.max_episode_length = 1000000000
    env.env_config.manual_play = False

    env.reset()

    num_actions = env.env_config.attacker_action_conf.num_actions
    actions = np.array(list(range(num_actions)))
    print("num actions:{}".format(num_actions))
    tot_rew = 0
    for i in range(num_steps):
        print(i)
        legal_attacker_actions = list(filter(lambda x: env.is_attack_action_legal(x, env.env_config, env.env_state), actions))
        attack_action = np.random.choice(legal_attacker_actions)
        defender_action = None
        action = (attack_action, defender_action)
        obs, reward, done, info = env.step(action)
        sys.stdout.flush()
        attacker_obs, defender_obs = obs
        attacker_reward, defender_reward = reward
        tot_rew += attacker_reward
        #env.render()
        if done:
            print("tot_rew:{}".format(tot_rew))
            tot_rew = 0
            env.reset()
        #time.sleep(0.001)
        #time.sleep(0.5)
    env.reset()
    env.close()


def test_all():
    #test_env("pycr-ctf-level-4-emulation-v1", num_steps=1000000000)
    #test_env("pycr-ctf-level-4-generated-sim-v1", num_steps=1000000000)
    #test_env("pycr-ctf-level-4-emulation-v2", num_steps=1000000000)
    #test_env("pycr-ctf-level-4-emulation-v3", num_steps=1000000000)
    #test_env("pycr-ctf-level-4-emulation-v4", num_steps=1000000000)
    #test_env("pycr-ctf-level-4-emulation-v5", num_steps=1000000000)
    test_env("pycr-ctf-level-4-generated-sim-v5", num_steps=1000000000)

if __name__ == '__main__':
    test_all()