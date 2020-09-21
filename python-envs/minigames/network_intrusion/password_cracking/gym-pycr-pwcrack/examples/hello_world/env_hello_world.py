from gym_pycr_pwcrack.envs.pycr_pwcrack_env import PyCRPwCrackSimpleSim1Env
import gym
import time
import numpy as np

def test_env(env_name : str, num_steps : int):
    env = gym.make(env_name, env_config=None)
    env.reset()

    #actions = np.array([0,1,2,3,4,5,6,7,8])
    actions = np.array([7, 8])
    #actions = np.array([5,2])
    for i in range(num_steps):
        action = np.random.choice(actions)
        res = env.step(action)
        env.render()
        time.sleep(0.5)
    env.reset()
    env.close()

def test_all():
    test_env("pycr-pwcrack-simple-sim-v1", num_steps=1000)

if __name__ == '__main__':
    test_all()