import time

import numpy as np
import torch
import random
from csle_common.metastore.metastore_facade import MetastoreFacade
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender
from gym_csle_cyborg.envs.cyborg_scenario_two_wrapper import CyborgScenarioTwoWrapper
from gym_csle_cyborg.dao.cyborg_wrapper_state import CyborgWrapperState
from gym_csle_cyborg.dao.csle_cyborg_wrapper_config import CSLECyborgWrapperConfig
import csle_agents.constants.constants as agents_constants

if __name__ == '__main__':
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False, cache_visited_states=True)
    env = CyborgScenarioTwoDefender(config=config)
    num_evaluations = 1
    max_horizon = 100
    returns = []
    seed = 68172
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    A = env.get_action_space()
    env.reset()
    o, r, done, _, info = env.step(35)
    o, r, done, _, info = env.step(35)
    o, r, done, _, info = env.step(35)
    o, r, done, _, info = env.step(35)
    o, r, done, _, info = env.step(35)
    s_prime = info[agents_constants.COMMON.STATE]
    obs_id = info[agents_constants.COMMON.OBSERVATION]
    # print(eval_env.get_true_table())
    # print(eval_env.get_table())
    # print(eval_env.get_actions_table())
    # print(action)
    # print(CyborgEnvUtil.state_id_to_state_vector(state_id=s_prime))
    # print(CyborgEnvUtil.state_id_to_state_vector(state_id=obs_id, observation=True))
    times = []
    for i in range(1000):
        start = time.time()
        env.set_state(s_prime)
        times.append((time.time()-start)*1000)
    print(np.mean(times))
    print(np.std(times))
    # env.set_state(s)
    # env.step(35)
    # print(env.red_agent_target)
    # env.step(35)
    # print(env.red_agent_target)
    # acs = env.get_reachable_hosts(particles=[s])
    # print(acs)
