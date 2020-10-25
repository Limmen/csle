from gym_pycr_pwcrack.envs.pycr_pwcrack_env import PyCrPwCrackMediumBase
import gym
import time
import numpy as np

def test_env(env_name : str, num_steps : int):
    env = gym.make(env_name, env_config=None)
    env.reset()

    num_actions = env.env_config.action_conf.num_actions
    actions = np.array(list(range(num_actions)))
    print("num actions:{}".format(num_actions))
    actions = np.array([1, 2, 3, 4])
    for i in range(num_steps):
        action = np.random.choice(actions)
        obs, reward, done, info = env.step(action)
        env.render()
        if done:
            env.reset()
        time.sleep(0.001)
    env.reset()
    env.close()

def test_all():
    test_env("pycr-pwcrack-medium-sim-base-v1", num_steps=1000000000)

if __name__ == '__main__':
    test_all()