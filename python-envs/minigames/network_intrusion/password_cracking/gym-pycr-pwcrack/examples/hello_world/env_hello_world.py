from gym_pycr_pwcrack.envs.pycr_pwcrack_env import PyCRPwCrackSimpleSim1Env
import gym
import time

def test_env(env_name : str, num_steps : int):
    env = gym.make(env_name, env_config=None)
    env.reset()

    action = 1
    for i in range(num_steps):
        res = env.step(action)
        env.render()
        time.sleep(1)
    env.reset()
    env.close()

def test_all():
    test_env("pycr-pwcrack-simple-sim-v1", num_steps=10)

if __name__ == '__main__':
    test_all()