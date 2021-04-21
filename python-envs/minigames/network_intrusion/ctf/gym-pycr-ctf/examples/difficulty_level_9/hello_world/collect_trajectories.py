import gym
import numpy as np
import json
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.dao.network.trajectory import Trajectory

def test_env(env_name : str, num_steps : int):
    # emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip="172.18.9.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
    #                                server_username="kim")
    # emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip="172.18.9.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    emulation_config = EmulationConfig(agent_ip="172.18.9.191", agent_username="agent", agent_pw="agent",
                                     server_connection=False, port_forward_next_port=3200)

    # emulation_config.save_dynamics_model_dir = "/home/kim/storage/workspace/pycr/python-envs/minigames/" \
    #                                            "network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/" \
    #                                            "hello_world/"
    emulation_config.save_dynamics_model_dir = "/home/kim/pycr/python-envs/minigames/network_intrusion/ctf/" \
                                               "gym-pycr-ctf/examples/difficulty_level_9/hello_world/"
    trajectories_save_dir = emulation_config.save_dynamics_model_dir
    emulation_config.skip_exploration = True
    env = gym.make(env_name, env_config=None, emulation_config=emulation_config)
    env.env_config.max_episode_length = 1000000000
    env.env_config.manual_play = False
    env.reset()

    num_actions = env.env_config.attacker_action_conf.num_actions
    actions = np.array(list(range(num_actions)))
    print("num actions:{}".format(num_actions))
    trajectories = []
    trajectory = Trajectory()
    for i in range(num_steps):
        #print("i:{}".format(i))
        legal_actions = list(filter(lambda x: env.is_attack_action_legal(x, env.env_config, env.env_state), actions))
        if len(legal_actions) == 0:
            print("no legal actions")

        attacker_action = np.random.choice(legal_actions)
        defender_action = 1
        action = (attacker_action, defender_action)
        print(action)
        obs, reward, done, info = env.step(action)
        attacker_obs, defender_obs = obs
        attacker_reward, defender_reward = reward
        trajectory.attacker_rewards.append(float(attacker_reward))
        trajectory.defender_rewards.append(float(defender_reward))
        trajectory.attacker_observations.append(attacker_obs.tolist())
        trajectory.defender_observations.append(defender_obs.tolist())
        trajectory.infos.append(info)
        trajectory.dones.append(done)
        trajectory.attacker_actions.append(int(attacker_action))
        trajectory.defender_actions.append(int(defender_action))

        if done:
            tot_rew = 0
            obs = env.reset()
            trajectories.append(trajectory.to_dict())

            with open(trajectories_save_dir + "/taus.json", 'w') as fp:
                json.dump({"trajectories": trajectories}, fp)

            done = False
            attacker_obs, defender_obs = obs
            trajectory = Trajectory()
            trajectory.attacker_rewards.append(0)
            trajectory.defender_rewards.append(0)
            trajectory.attacker_observations.append(attacker_obs.tolist())
            trajectory.defender_observations.append(defender_obs.tolist())
            trajectory.infos.append({})
            trajectory.dones.append(done)
            trajectory.attacker_actions.append(-1)
            trajectory.defender_actions.append(-1)

    env.reset()
    env.close()


def test_all():
    #test_env("pycr-ctf-level-9-emulation-v1", num_steps=1000000000)
    #test_env("pycr-ctf-level-9-emulation-v2", num_steps=1000000000)
    #test_env("pycr-ctf-level-9-emulation-v3", num_steps=1000000000)
    #test_env("pycr-ctf-level-9-emulation-v1", num_steps=1000000000)
    #test_env("pycr-ctf-level-9-generated-sim-v1", num_steps=1000000000)
    test_env("pycr-ctf-level-9-generated-sim-v5", num_steps=1000000000)

if __name__ == '__main__':
    test_all()

# Test case: 99,33,1,70,104,105,106,107,99,165,200,58,104,105,106,331,99,266,104,105,106,99,113,104,105