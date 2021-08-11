from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.envs_model.logic.simulation.find_pi_star_attacker import FindPiStarAttacker
import gym


def test_env(env_name : str, num_steps : int):

    emulation_config = EmulationConfig(agent_ip="172.18.1.191", agent_username="agent", agent_pw="agent",
                                     server_connection=False)
    env = gym.make(env_name, env_config=None, emulation_config=emulation_config)
    env.env_config.max_episode_length = 1000000000
    env.env_config.manual_play = True

    env.reset()
    FindPiStarAttacker.brute_force(env.env_config, env)

    # num_actions = env.env_config.attacker_action_conf.num_actions
    # actions = np.array(list(range(num_actions)))
    # print("num actions:{}".format(num_actions))
    # tot_rew = 0
    # for i in range(num_steps):
    #     legal_actions = list(filter(lambda x: env.is_action_legal(x, env.env_config, env.env_state), actions))
    #     action = np.random.choice(legal_actions)
    #     obs, reward, done, info = env.step(action)
    #     tot_rew += reward
    #     env.render()
    #     if done:
    #         print("tot_rew:{}".format(tot_rew))
    #         tot_rew = 0
    #         env.reset()
    #     #time.sleep(0.001)
    #     #time.sleep(0.5)
    # env.reset()
    # env.close()


def test():
    test_env("pycr-ctf-level-1-sim-v1", num_steps=1000000000)

if __name__ == '__main__':
    test()