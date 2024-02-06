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
    config = CSLECyborgWrapperConfig(maximum_steps=100, gym_env_name="",
                                     save_trace=False, reward_shaping=False, scenario=2)
    env = CyborgScenarioTwoWrapper(config=config)
    num_evaluations = 1
    max_horizon = 100
    returns = []
    seed = 68172
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    A = env.get_action_space()
    s = CyborgWrapperState(
        s= [[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
            [0, 0, 0, 0], [1, 0, 2, 0], [1, 0, 0, 1], [1, 1, 2, 2], [1, 0, 0, 0], [1, 0, 0, 0]],
        scan_state=[0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        op_server_restored=False,
        obs=[[0, 0, 0, 0], [0, 0, 0, 0], [1, 2, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
             [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1], [0, 1, 2, 2], [0, 0, 0, 0], [0, 0, 0, 0]],
        red_action_targets= {0: 0, 1: 10, 2: 10, 3: 10, 4: 2},
        privilege_escalation_detected=None,
        red_agent_state=5,
        red_agent_target=2,
        attacker_observed_decoy=[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        detected=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        malware_state=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], ssh_access=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    )
    times = []
    for i in range(1000):
        start = time.time()
        # env.step(35)
        env.set_state(s)
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
