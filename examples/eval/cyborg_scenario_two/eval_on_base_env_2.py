import time

import numpy as np
import torch
import random
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.ppo_policy import PPOPolicy
from csle_common.dao.training.player_type import PlayerType
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender

if __name__ == '__main__':
    meander_policy = MetastoreFacade.get_ppo_policy(id=224)
    # bline_policy = PPOPolicy(model=None, simulation_name="",
    #                        save_path="/tmp/csle/ppo_test_1707078811.4761195/ppo_model1630_1707115775.1994205.zip",
    #                        player_type=PlayerType.DEFENDER, actions=[], states=[], experiment_config=None, avg_R=0)
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.MEANDER_AGENT,
                                                                                     RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False, cache_visited_states=False)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    num_evaluations = 1
    max_horizon = 100
    returns = []
    seed = 998103
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    print("Starting policy evaluation")
    for i in range(num_evaluations):
        o, _ = csle_cyborg_env.reset()
        R = 0
        t = 0
        previous_action_scan = False
        while t < max_horizon:
            a = meander_policy.action(o=o)
            # a = 35
            o, r, done, _, info = csle_cyborg_env.step(a)
            R += r
            t += 1
            print(csle_cyborg_env.get_true_table())
            print(csle_cyborg_env.get_table())
            print(csle_cyborg_env.get_actions_table())
            print(f"t:{t}, r: {r}")
        returns.append(R)
        print(f"{i}/{num_evaluations}, avg R: {np.mean(returns)}, R: {R}, std: {np.std(returns)}")
