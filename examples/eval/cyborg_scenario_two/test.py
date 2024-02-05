import numpy as np
import torch
import random
from csle_common.metastore.metastore_facade import MetastoreFacade
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender
import csle_agents.constants.constants as agents_constants

if __name__ == '__main__':
    # ppo_policy = MetastoreFacade.get_ppo_policy(id=3)
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False, cache_visited_states=False)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    num_evaluations = 1
    max_horizon = 100
    returns = []
    seed = 68172
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    A = csle_cyborg_env.get_action_space()
    print("Starting policy evaluation")
    # import sys
    from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil
    # print(CyborgEnvUtil.state_id_to_state_vector(state_id=1339274099499015287431538211443713, observation=True))
    # sys.exit()
    for i in range(num_evaluations):
        o, info = csle_cyborg_env.reset()
        print(csle_cyborg_env.get_true_table())
        R = 0
        t = 0
        s_prime = info[agents_constants.COMMON.STATE]
        s = CyborgEnvUtil.state_id_to_state_vector(state_id=s_prime)
        while t < max_horizon:
            # a = np.random.choice(A)
            a = 4
            if s[7][0] == 1:
                a = 35
            o, r, done, _, info = csle_cyborg_env.step(a)
            s_prime = info[agents_constants.COMMON.STATE]
            s = CyborgEnvUtil.state_id_to_state_vector(state_id=s_prime)
            print(csle_cyborg_env.get_last_action(agent='Red'))
            print(csle_cyborg_env.get_true_table())
            print(csle_cyborg_env.get_table())
            R += r
            t += 1
        returns.append(R)
        print(f"{i}/{num_evaluations}, avg R: {np.mean(returns)}, R: {R}")
