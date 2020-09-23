from gym_pycr_pwcrack.envs.pycr_pwcrack_env import PyCRPwCrackSimpleSim1Env
import gym
import time
import numpy as np

def test_env(env_name : str, num_steps : int):
    env = gym.make(env_name, env_config=None)
    env.reset()

    num_actions = env.env_config.action_conf.num_actions
    actions = np.array(list(range(num_actions)))
    print("num actions:{}".format(num_actions))
    #actions = np.array([70, 127, 132])

    #actions = np.array([71])
    #actions = np.array([9, 16])
    #actions = np.array([9])
    #actions = np.array([10, 17])
    #actions = np.array([7, 8])
    #actions = np.array([5,2])
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
    test_env("pycr-pwcrack-simple-sim-v1", num_steps=10000)

if __name__ == '__main__':
    test_all()