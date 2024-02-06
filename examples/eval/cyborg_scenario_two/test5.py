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
        scanned_state=True, decoy_optimization=False, cache_visited_states=False)
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