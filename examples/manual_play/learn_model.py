import numpy as np
import io
from csle_common.metastore.metastore_facade import MetastoreFacade
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender
import csle_agents.constants.constants as constants
import json
from csle_agents.agents.pomcp.pomcp_util import POMCPUtil
import math

if __name__ == '__main__':
    ppo_policy = MetastoreFacade.get_ppo_policy(id=22)
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False, cache_visited_states=True)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    transition_probabilities = {}
    observation_probabilities = {}
    initial_state_distribution = {}
    reward_function = {}
    episodes = 100000
    t_count = 0
    save_every = 500
    for i in range(episodes):
        print(f"episode {i}/{episodes}")
        o, info = csle_cyborg_env.reset()
        new_transitions = 0
        done = False
        s = info[constants.ENV_METRICS.STATE]
        if s not in initial_state_distribution:
            initial_state_distribution[s] = 1
        else:
            initial_state_distribution[s] = initial_state_distribution[s] + 1
        while not done:
            a = ppo_policy.action(o=o)
            o, r, done, _, info = csle_cyborg_env.step(action=a)
            s_prime = info[constants.ENV_METRICS.STATE]
            oid = info[constants.ENV_METRICS.OBSERVATION]
            if ",".join([str(s), str(s_prime), str(a)]) not in transition_probabilities:
                transition_probabilities[",".join([str(s), str(s_prime), str(a)])] = 1
                new_transitions += 1
            else:
                transition_probabilities[",".join([str(s), str(s_prime), str(a)])] = transition_probabilities[",".join([str(s), str(s_prime), str(a)])] + 1
            if ",".join([str(s), str(s_prime), str(a)]) not in reward_function:
                reward_function[",".join([str(s), str(s_prime), str(a)])] = r
            if ",".join([str(s_prime), str(oid)]) not in observation_probabilities:
                observation_probabilities[",".join([str(s_prime), str(oid)])] = 1
            else:
                observation_probabilities[",".join([str(s_prime), str(oid)])] = observation_probabilities[",".join([str(s_prime), str(oid)])] + 1
            t_count += 1
        print(f"new transitions: {new_transitions}")

        if i % save_every == 0:
            model = {}
            model["transitions"] = transition_probabilities
            model["rewards"] = reward_function
            model["episodes"] = i
            model["steps"] = t_count
            model["observations"] = observation_probabilities
            model["initial_state"] = initial_state_distribution
            json_str = json.dumps(model, indent=4, sort_keys=True)
            with io.open(f"/home/kim/cyborg_model_{i}.json", 'w', encoding='utf-8') as f:
                f.write(json_str)


