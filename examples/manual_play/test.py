import numpy as np
from gym_csle_cyborg.dao.csle_cyborg_wrapper_config import CSLECyborgWrapperConfig
from gym_csle_cyborg.envs.cyborg_scenario_two_wrapper import CyborgScenarioTwoWrapper
from csle_common.metastore.metastore_facade import MetastoreFacade
import csle_agents.constants.constants as constants
import random
import torch

if __name__ == '__main__':
    config = CSLECyborgWrapperConfig(maximum_steps=100, gym_env_name="", save_trace=False, reward_shaping=False)
    env = CyborgScenarioTwoWrapper(config=config)
    ppo_policy = MetastoreFacade.get_ppo_policy(id=58)
    num_episodes = 1000
    A = env.get_action_space()
    returns = []
    max_horizon = 100
    seed = 1612312
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    for ep in range(num_episodes):
        done = False
        o, info = env.reset()
        R = 0
        t = 0
        zeros = []
        ones = []
        while t <= max_horizon:
            # a = np.random.choice(A)
            a = ppo_policy.action(o=o, deterministic=False)
            if a == 0:
                zeros.append(0)
            if a == 1:
                ones.append(1)
            o, r, done, _, info = env.step(a)
            # if ep == 132:
            # if ep == 0:
            #     print(f"t: {t}, a: {a}, r: {r}")
            #     print(env.s)
            #     print(env.last_obs)
            #     print(f"{env.red_agent_target}, {env.get_red_agent_action_type_from_state(env.red_agent_state)}")
            # if ep == 1:
            #     import sys
            #     sys.exit()

            # print(o)
            # print(o[14*1:14*1+14])
            # print(r)
            # print(a)
            R += r
            t += 1
        returns.append(R)

        print(f"{ep}/{num_episodes}, avg R: {np.mean(returns)}, R: {R}, ones: {len(ones)}, zeros: {len(zeros)}")

