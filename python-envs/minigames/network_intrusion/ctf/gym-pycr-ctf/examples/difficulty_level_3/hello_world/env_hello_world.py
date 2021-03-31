from gym_pycr_ctf.envs.pycr_ctf_env import PyCrCTFLevel2Base
import gym
import time
import numpy as np

def test_env(env_name : str, num_steps : int):
    env = gym.make(env_name, env_config=None)
    env.reset()

    num_actions = env.env_config.attacker_action_conf.num_actions
    actions = np.array(list(range(num_actions)))
    print("num actions:{}".format(num_actions))
    for i in range(num_steps):
        legal_actions = list(filter(lambda x: env.is_attack_action_legal(x, env.env_config, env.env_state), actions))
        action = np.random.choice(legal_actions)
        obs, reward, done, info = env.step(action)
        env.render()
        if done:
            env.reset()
        time.sleep(0.001)
    env.reset()
    env.close()

def test_all():
    test_env("pycr-ctf-level-3-sim-v1", num_steps=1000000000)

if __name__ == '__main__':
    test_all()