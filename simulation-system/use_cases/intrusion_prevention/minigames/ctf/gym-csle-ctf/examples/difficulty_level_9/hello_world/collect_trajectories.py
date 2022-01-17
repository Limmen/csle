import gym
import numpy as np
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.dao.network.trajectory import Trajectory


def test_env(env_name : str, num_trajectories : int):
    # emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}9.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/csle_id_rsa",
    #                                server_username="kim")
    emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}9.191",
                                   agent_username="agent", agent_pw="agent", server_connection=True,
                                   server_private_key_file="/home/kim/.ssh/id_rsa",
                                   server_username="kim")
    # emulation_config = EmulationConfig(agent_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}9.191", agent_username="agent", agent_pw="agent",
    #                                  server_connection=False, port_forward_next_port=3200)

    emulation_config.save_dynamics_model_dir = "/home/kim/storage/workspace/csle/simulation-system/minigames/" \
                                               "network_intrusion/ctf/gym-csle-ctf/examples/difficulty_level_9/" \
                                               "hello_world/"
    # emulation_config.save_dynamics_model_dir = "/home/kim/csle/simulation-system/use_cases/intrusion_prevention/minigames/ctf/" \
    #                                            "gym-csle-ctf/examples/difficulty_level_9/hello_world/"
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
    for i in range(num_trajectories):
        done = False
        obs = env.reset()
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
        print("Trajectory:{}".format(i))
        while not done:
            #print("i:{}".format(i))
            legal_actions = list(filter(lambda x: env.is_attack_action_legal(x, env.env_config, env.env_state), actions))
            if len(legal_actions) == 0:
                print("no legal actions")

            #attacker_action = np.random.choice(legal_actions)
            defender_action = 1
            action = (None, defender_action)
            obs, reward, done, info = env.step(action)
            attacker_obs, defender_obs = obs
            attacker_reward, defender_reward = reward
            trajectory.attacker_rewards.append(float(attacker_reward))
            trajectory.defender_rewards.append(float(defender_reward))
            trajectory.attacker_observations.append(attacker_obs.tolist())
            #print("defender obs, action:{}".format(defender_obs))
            trajectory.defender_observations.append(defender_obs.tolist())
            trajectory.infos.append(info)
            trajectory.dones.append(done)
            trajectory.attacker_actions.append(int(info["attacker_action"]))
            trajectory.defender_actions.append(int(defender_action))

        trajectories.append(trajectory)

    Trajectory.save_trajectories(emulation_config.save_dynamics_model_dir, trajectories, trajectories_file="taus2.json")

    env.reset()
    env.close()


def test_all():
    #test_env("csle-ctf-level-9-emulation-v1", num_steps=1000000000)
    #test_env("csle-ctf-level-9-emulation-v2", num_steps=1000000000)
    #test_env("csle-ctf-level-9-emulation-v3", num_steps=1000000000)
    #test_env("csle-ctf-level-9-emulation-v1", num_steps=1000000000)
    #test_env("csle-ctf-level-9-generated-sim-v1", num_steps=1000000000)
    test_env("csle-ctf-level-9-generated-sim-v5", num_trajectories=50)

if __name__ == '__main__':
    test_all()

# Test case: 99,33,1,70,104,105,106,107,99,165,200,58,104,105,106,331,99,266,104,105,106,99,113,104,105