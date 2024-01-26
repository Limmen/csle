import numpy as np
import json
import io
from csle_common.metastore.metastore_facade import MetastoreFacade
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender
from gym_csle_cyborg.dao.blue_agent_action_type import BlueAgentActionType
import csle_agents.constants.constants as agents_constants
from csle_agents.agents.pomcp.pomcp_util import POMCPUtil

if __name__ == '__main__':
    ppo_policy = MetastoreFacade.get_ppo_policy(id=98)
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False, cache_visited_states=False)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    num_evaluations = 100000
    max_horizon = 100
    returns = []
    A = csle_cyborg_env.get_action_space()
    model = {}
    # observation_to_actions = {}
    import random
    import torch
    seed = 291512
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    for i in range(num_evaluations):
        print(f"episode: {i}/{num_evaluations}, model size: {len(model)}")
        done = False
        o, info = csle_cyborg_env.reset()
        s = info[agents_constants.COMMON.STATE]
        oid = info[agents_constants.COMMON.STATE]
        R = 0
        t = 0
        action_sequence = []
        while not done and t < max_horizon:
            a = POMCPUtil.rand_choice(A)
            # a = ppo_policy.action(o=o)
            o, r, done, _, info = csle_cyborg_env.step(a)
            s_prime = info[agents_constants.COMMON.STATE]
            oid = info[agents_constants.COMMON.OBSERVATION]
            R += r
            t += 1
            if s not in model:
                model[int(s)] = {}
            if s_prime not in model[s]:
                model[int(s)][int(s_prime)] = {}
            if a not in model[int(s)][int(s_prime)]:
                model[int(s)][int(s_prime)][int(a)] = 0
            else:
                model[int(s)][int(s_prime)][int(a)] += 1
            s = s_prime
        returns.append(R)

        if i % 100 ==  0:
            json_str = json.dumps(model, indent=4, sort_keys=True)
            with io.open(f"/home/kim/transition_model.json", 'w', encoding='utf-8') as f:
                f.write(json_str)
        # print(f"{i}/{num_evaluations}, avg R: {np.mean(returns)}")
