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
    total_times = []
    total_simulations = []
    for i in range(20):
        times = []
        simulations = []
        start = time.time()
        num_simulations = 0
        idx = 5
        while idx <= 130:
            env.reset()
            t = 0
            while t <= 100:
                env.step(np.random.choice(A))
                t+=1
            num_simulations += 1
            if time.time()-start >= idx:
                simulations.append(num_simulations)
                times.append(idx)
                idx += 5
        total_times.append(times)
        total_simulations.append(simulations)


    mean_times = []
    mean_simulations = []
    stds_simulations = []
    for j in range(len(total_times[0])):
        ts = []
        ss = []
        for i in range(20):
            ts.append(total_times[i][j])
            ss.append(total_simulations[i][j])
        mean_times.append(np.mean(ts))
        mean_simulations.append(np.mean(ss))
        stds_simulations.append(np.std(ss))

    for i in range(len(mean_times)):
        print(f"{mean_times[i]} {mean_simulations[i]} {stds_simulations[i]}")