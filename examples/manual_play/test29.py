import numpy as np
import torch
import random
from gym_csle_cyborg.envs.cyborg_model_wrapper import CyborgModelWrapper
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from csle_common.metastore.metastore_facade import MetastoreFacade

if __name__ == '__main__':
    # with open(f'/home/kim/exploit_model.npy', 'rb') as f:
    #     exploit_success_probabilities = np.load(f)
    # with open(f'/home/kim/exploit_root_model.npy', 'rb') as f:
    #     exploit_root_probabilities = np.load(f)
    # with open(f'/home/kim/exploit_user_model.npy', 'rb') as f:
    #     exploit_user_probabilities = np.load(f)
    # with open(f'/home/kim/activity_model.npy', 'rb') as f:
    #     activity_probabilities = np.load(f)
    # with open(f'/home/kim/compromise_model.npy', 'rb') as f:
    #     compromise_probabilities = np.load(f)

    # print(exploit_success_probabilities[9][0])

    maximum_steps = 100
    env = CyborgModelWrapper(maximum_steps=maximum_steps)
    A = env.get_action_space()
    seed = 2623
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    ppo_policy = MetastoreFacade.get_ppo_policy(id=58)
    episodes = 1000
    returns = []
    for ep in range(episodes):
        o, info = env.reset()
        R = 0
        # print(f"s: {env.s}")
        for i in range(maximum_steps):
            # a = 27
            # a = np.random.choice(A)
            # a = 27
            # if i > 20:
            #     a = 3
            # a = 4
            a = ppo_policy.action(o=o)
            # print(a)
            # a = 4
            o, r, done, _, info = env.step(a)
            # print(f"t: {i}, r: {r}, a: {a}")
            # print(f"s: {env.s}")
            # print(f"o: {info['obs_vec']}")
            # if i == 0:
            #     print(o)
            #     print(type(o))
            #     print(list(o.tolist()).index(1))
            R += r
        returns.append(R)
        print(f"{ep}/{episodes}, Mean R: {np.mean(returns)}, R: {R}")
