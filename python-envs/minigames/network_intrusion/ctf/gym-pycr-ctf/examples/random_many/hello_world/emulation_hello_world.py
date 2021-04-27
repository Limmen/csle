from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
import gym
import numpy as np
from gym_pycr_ctf.envs_model.config.generator.env_config_generator import EnvConfigGenerator

def test_env(env_name : str, num_steps : int):
    # emulation_config = emulationConfig(server_ip="172.31.212.91", agent_ip="172.18.1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
    #                                server_username="kim")
    # emulation_config = emulationConfig(server_ip="172.31.212.91", agent_ip="172.18.1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
        "/home/kim/storage/workspace/pycr/emulation-envs/minigames/network_intrusion/ctf/001/random_many_train/")
    flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
        "/home/kim/storage/workspace/pycr/emulation-envs/minigames/network_intrusion/ctf/001/random_many_train/")
    # eval_containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
    #     "/home/kim/storage/workspace/pycr/emulation-envs/minigames/network_intrusion/ctf/001/random_many_2/")
    # eval_flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
    #     "/home/kim/storage/workspace/pycr/emulation-envs/minigames/network_intrusion/ctf/001/random_many_2/")
    max_num_nodes_train = max(list(map(lambda x: len(x.containers), containers_configs)))
    #max_num_nodes_eval = max(list(map(lambda x: len(x.containers), eval_containers_configs)))
    #max_num_nodes = max(max_num_nodes_train, max_num_nodes_eval)
    max_num_nodes = max_num_nodes_train

    idx = 2
    print("ip:{}".format(containers_configs[idx].agent_ip))
    emulation_config = EmulationConfig(agent_ip=containers_configs[idx].agent_ip, agent_username="agent",
                                       agent_pw="agent", server_connection=False, port_forward_next_port=9800)
    # emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip=containers_configs[idx].agent_ip,
    #                                  agent_username="agent", agent_pw="agent", server_connection=True,
    #                                  server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                  server_username="kim")
    env = gym.make(env_name, env_config=None, emulation_config=emulation_config,
                   containers_configs=containers_configs, flags_configs=flags_configs, idx=idx,
                   num_nodes=max_num_nodes)
    env.env_config.max_episode_length = 1000000000
    env.env_config.manual_play = True

    env.reset()

    num_actions = env.env_config.attacker_action_conf.num_actions
    actions = np.array(list(range(num_actions)))
    print("num actions:{}".format(num_actions))
    tot_rew = 0
    for i in range(num_steps):
        print(i)
        legal_actions = list(filter(lambda x: env.is_attack_action_legal(x, env.env_config, env.env_state), actions))
        #legal_actions = actions
        attacker_action = np.random.choice(legal_actions)
        action = (attacker_action, None)
        obs, reward, done, info = env.step(action)
        attacker_reward, defender_reward = reward
        tot_rew += attacker_reward
        #env.render()
        if done:
            print(tot_rew)
            tot_rew = 0
            env.reset()
        #time.sleep(0.001)
        #time.sleep(0.5)
    env.reset()
    env.close()


def test_all():
    test_env("pycr-ctf-random-many-emulation-v1", num_steps=1000000000)
    #test_env("pycr-ctf-random-many-generated-sim-v1", num_steps=1000000000)


if __name__ == '__main__':
    test_all()