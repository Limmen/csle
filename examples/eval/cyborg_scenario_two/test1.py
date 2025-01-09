import numpy as np
import copy
import random
from csle_common.dao.encoding.np_encoder import NpEncoder
from gym_csle_cyborg.envs.cyborg_scenario_two_wrapper import CyborgScenarioTwoWrapper
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.dao.csle_cyborg_wrapper_config import CSLECyborgWrapperConfig

def get_active_decoys(state):
    decoy_state = state.get_decoy_state()
    reachable_hosts = []
    if 1 not in state.red_action_targets:
        reachable_hosts = [12,11,10,9]
    else:
        reachable_hosts = [12,11,10,9,1,2,3]
    active_decoys = 0
    for h in range(len(decoy_state)):
        if h in reachable_hosts:
            active_decoys += decoy_state[h]
    return active_decoys


if __name__ == '__main__':
    config = CSLECyborgWrapperConfig(maximum_steps=100, gym_env_name="",
                                     save_trace=False, reward_shaping=False, scenario=2,
                                     red_agent_type=RedAgentType.B_LINE_AGENT)
    env = CyborgScenarioTwoWrapper(config=config)

    N = 10000
    max_env_steps = 100
    A = env.get_action_space()
    # print(len(A))
    state_to_id = {}
    id_to_state = {}
    costs = {}
    transitions = {}
    state_id = 0
    for i in range(N):
        print(f"{i}/{N}")
        done = False
        _, info = env.reset()
        s = info["s"]
        active_decoys = get_active_decoys(s)
        t = 1
        while not done and t <= max_env_steps:
            a = np.random.choice(A)
            o, r, done, _, info = env.step(a)
            s_prime = info["s"]
            active_decoys_prime = get_active_decoys(s_prime)

            if f"{s.red_agent_state},{active_decoys}" not in state_to_id:
                state_to_id[f"{s.red_agent_state},{active_decoys}"] = state_id
                id_to_state[state_id] = [s.red_agent_state, active_decoys]
                state_id += 1

            if f"{s_prime.red_agent_state},{active_decoys_prime}" not in state_to_id:
                state_to_id[f"{s_prime.red_agent_state},{active_decoys_prime}"] = state_id
                id_to_state[state_id] = [s_prime.red_agent_state, active_decoys_prime]
                state_id += 1

            if state_to_id[f"{s.red_agent_state},{active_decoys}"] not in costs:
                costs[state_to_id[f"{s.red_agent_state},{active_decoys}"]] = {}
                transitions[state_to_id[f"{s.red_agent_state},{active_decoys}"]] = {}
            if state_to_id[f"{s_prime.red_agent_state},{active_decoys_prime}"] not in costs:
                costs[state_to_id[f"{s_prime.red_agent_state},{active_decoys_prime}"]] = {}
                transitions[state_to_id[f"{s_prime.red_agent_state},{active_decoys_prime}"]] = {}

            if a not in transitions[state_to_id[f"{s.red_agent_state},{active_decoys}"]]:
                transitions[state_to_id[f"{s.red_agent_state},{active_decoys}"]][int(a)] = {}
            if state_to_id[f"{s_prime.red_agent_state},{active_decoys_prime}"] not in transitions[state_to_id[f"{s.red_agent_state},{active_decoys}"]][a]:
                transitions[state_to_id[f"{s.red_agent_state},{active_decoys}"]][int(a)][state_to_id[f"{s_prime.red_agent_state},{active_decoys_prime}"]] = 0
            transitions[state_to_id[f"{s.red_agent_state},{active_decoys}"]][int(a)][state_to_id[f"{s_prime.red_agent_state},{active_decoys_prime}"]] += 1

            if a not in costs[state_to_id[f"{s.red_agent_state},{active_decoys}"]]:
                costs[state_to_id[f"{s.red_agent_state},{active_decoys}"]][int(a)] = []
            costs[state_to_id[f"{s.red_agent_state},{active_decoys}"]][int(a)].append(-r)
            s = s_prime
            active_decoys = active_decoys_prime

    import json, io

    json_str = json.dumps(state_to_id, indent=4, sort_keys=True, cls=NpEncoder)
    with io.open("./state_to_id.json", 'w', encoding='utf-8') as f:
        f.write(json_str)

    json_str = json.dumps(id_to_state, indent=4, sort_keys=True, cls=NpEncoder)
    with io.open("./id_to_state.json", 'w', encoding='utf-8') as f:
        f.write(json_str)

    json_str = json.dumps(costs, indent=4, sort_keys=True, cls=NpEncoder)
    with io.open("./costs.json", 'w', encoding='utf-8') as f:
        f.write(json_str)

    json_str = json.dumps(transitions, indent=4, sort_keys=True, cls=NpEncoder)
    with io.open("./transitions.json", 'w', encoding='utf-8') as f:
        f.write(json_str)



# def to_json_str(self) -> str:
#     """
#     Converts the DTO into a json string
#
#     :return: the json string representation of the DTO
#     """
#     import json
#     json_str = json.dumps(self.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
#     return json_str
#
# def to_json_file(self, json_file_path: str) -> None:
#     """
#     Saves the DTO to a json file
#
#     :param json_file_path: the json file path to save  the DTO to
#     :return: None
#     """
#     import io
#     json_str = self.to_json_str()
#     with io.open(json_file_path, 'w', encoding='utf-8') as f:
#         f.write(json_str)
#
# @staticmethod
# def from_json_file(json_file_path: str) -> "GPSystemModel":
#     """
#     Reads a json file and converts it to a DTO
#
#     :param json_file_path: the json file path
#     :return: the converted DTO
#     """
#     import io
#     import json
#     with io.open(json_file_path, 'r') as f:
#         json_str = f.read()
#     return GPSystemModel.from_dict(json.loads(json_str))