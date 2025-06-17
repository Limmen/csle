import numpy as np
import torch
import random
from csle_common.metastore.metastore_facade import MetastoreFacade
from gym_csle_cyborg.envs.cyborg_scenario_two_wrapper import CyborgScenarioTwoWrapper
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.dao.csle_cyborg_wrapper_config import CSLECyborgWrapperConfig

if __name__ == '__main__':
    # ppo_policy = MetastoreFacade.get_ppo_policy(id=15)
    config = CSLECyborgWrapperConfig(maximum_steps=100, gym_env_name="",
                                     save_trace=False, reward_shaping=False, scenario=2,
                                     red_agent_type=RedAgentType.B_LINE_AGENT)
    env = CyborgScenarioTwoWrapper(config=config)
    num_evaluations = 10000
    max_horizon = 100
    returns = []
    seed = 215125
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    # for k,v in env.action_id_to_type_and_host.items():
    #     print(k)
    #     print(v)
    # import sys
    # sys.exit(0)
    restore_ent0 = 0
    restore_ent1 = 1
    restore_ent2 = 2
    restore_op_server = 3
    for i in range(num_evaluations):
        o, _ = env.reset()
        R = 0
        t = 0
        while t < max_horizon:
            a = 21
            if env.s[7][2] == 1:
                a = 3
            elif env.s[1][2] == 1:
                a = 0
            elif env.s[2][2] == 1:
                a = 1
            elif env.s[3][2] == 1:
                a = 2
            compromised_hosts = []
            for i in range(len(env.s)):
                if env.s[i][2] == 1:
                    compromised_hosts.append(i)
            # print(compromised_hosts)
            defender_action_type, defender_action_host = env.action_id_to_type_and_host[a]
            # print(env.action_space)
            # a = ppo_policy.action(o=o)
            o, r, done, _, info = env.step(a)
            R += r
            t += 1
        returns.append(R)
        print(f"{i}/{num_evaluations}, avg R: {np.mean(returns)}, R: {R}, std: {np.std(returns)}")
