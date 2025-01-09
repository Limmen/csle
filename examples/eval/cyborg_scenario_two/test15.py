import numpy as np
import copy
import random
from csle_common.dao.encoding.np_encoder import NpEncoder
from gym_csle_cyborg.envs.cyborg_scenario_two_wrapper import CyborgScenarioTwoWrapper
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.dao.csle_cyborg_wrapper_config import CSLECyborgWrapperConfig

def get_decoy_str(state):
    decoy_state = state.get_decoy_state()
    return f"{min(2, decoy_state[1])},{min(1, decoy_state[2])},{min(1,decoy_state[3])},{min(2,decoy_state[9])},{min(2,decoy_state[10])},{min(1,decoy_state[11])}"

# def get_active_decoys(state):
#     decoy_state = state.get_decoy_state()
#     reachable_hosts = []
#     if 1 not in state.red_action_targets:
#         reachable_hosts = [12,11,10,9]
#     else:
#         reachable_hosts = [12,11,10,9,1,2,3]
#     active_decoys = 0
#     for h in range(len(decoy_state)):
#         if h in reachable_hosts:
#             active_decoys += decoy_state[h]
#     return active_decoys


if __name__ == '__main__':
    config = CSLECyborgWrapperConfig(maximum_steps=100, gym_env_name="",
                                     save_trace=False, reward_shaping=False, scenario=2,
                                     red_agent_type=RedAgentType.B_LINE_AGENT)
    env = CyborgScenarioTwoWrapper(config=config)

    N = 40000
    max_env_steps = 100
    A = env.get_action_space()
    # print(len(A))
    state_to_id = {}
    id_to_state = {}
    costs = {}
    transitions = {}
    state_id = 0
    action_to_id = {
        0: 27,
        1: 28,
        2: 29,
        3: 30,
        4: 31,
        5: 32
    }
    A = list(range(6))

    for i in range(N):
        print(f"{i}/{N}")
        done = False
        _, info = env.reset()
        s = info["s"]
        decoy_str = get_decoy_str(s)
        t = 1
        while not done and t <= max_env_steps:
            a = np.random.choice(A)
            o, r, done, _, info = env.step(action_to_id[a])
            s_prime = info["s"]
            # active_decoys_prime = get_active_decoys(s_prime)
            decoys_str_prime = get_decoy_str(s_prime)

            if f"{s.red_agent_state},{decoy_str}" not in state_to_id:
                state_to_id[f"{s.red_agent_state},{decoy_str}"] = state_id
                id_to_state[state_id] = [s.red_agent_state, decoy_str]
                state_id += 1

            if f"{s_prime.red_agent_state},{decoys_str_prime}" not in state_to_id:
                state_to_id[f"{s_prime.red_agent_state},{decoys_str_prime}"] = state_id
                id_to_state[state_id] = [s_prime.red_agent_state, decoys_str_prime]
                state_id += 1

            if state_to_id[f"{s.red_agent_state},{decoy_str}"] not in costs:
                costs[state_to_id[f"{s.red_agent_state},{decoy_str}"]] = {}
                transitions[state_to_id[f"{s.red_agent_state},{decoy_str}"]] = {}
            if state_to_id[f"{s_prime.red_agent_state},{decoys_str_prime}"] not in costs:
                costs[state_to_id[f"{s_prime.red_agent_state},{decoys_str_prime}"]] = {}
                transitions[state_to_id[f"{s_prime.red_agent_state},{decoys_str_prime}"]] = {}

            if a not in transitions[state_to_id[f"{s.red_agent_state},{decoy_str}"]]:
                transitions[state_to_id[f"{s.red_agent_state},{decoy_str}"]][int(a)] = {}
            if state_to_id[f"{s_prime.red_agent_state},{decoys_str_prime}"] not in transitions[state_to_id[f"{s.red_agent_state},{decoy_str}"]][a]:
                transitions[state_to_id[f"{s.red_agent_state},{decoy_str}"]][int(a)][state_to_id[f"{s_prime.red_agent_state},{decoys_str_prime}"]] = 0
            transitions[state_to_id[f"{s.red_agent_state},{decoy_str}"]][int(a)][state_to_id[f"{s_prime.red_agent_state},{decoys_str_prime}"]] += 1

            if a not in costs[state_to_id[f"{s.red_agent_state},{decoy_str}"]]:
                costs[state_to_id[f"{s.red_agent_state},{decoy_str}"]][int(a)] = []
            costs[state_to_id[f"{s.red_agent_state},{decoy_str}"]][int(a)].append(-r)
            s = s_prime
            decoy_str = decoys_str_prime

    import json, io

    json_str = json.dumps(state_to_id, indent=4, sort_keys=True, cls=NpEncoder)
    with io.open("./state_to_id_7.json", 'w', encoding='utf-8') as f:
        f.write(json_str)

    json_str = json.dumps(id_to_state, indent=4, sort_keys=True, cls=NpEncoder)
    with io.open("./id_to_state_7.json", 'w', encoding='utf-8') as f:
        f.write(json_str)

    json_str = json.dumps(costs, indent=4, sort_keys=True, cls=NpEncoder)
    with io.open("./costs_7.json", 'w', encoding='utf-8') as f:
        f.write(json_str)

    json_str = json.dumps(transitions, indent=4, sort_keys=True, cls=NpEncoder)
    with io.open("./transitions_7.json", 'w', encoding='utf-8') as f:
        f.write(json_str)
