import numpy as np
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil
import copy
import random
from csle_common.dao.encoding.np_encoder import NpEncoder
from gym_csle_cyborg.envs.cyborg_scenario_two_wrapper import CyborgScenarioTwoWrapper
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.dao.csle_cyborg_wrapper_config import CSLECyborgWrapperConfig

if __name__ == '__main__':
    config = CSLECyborgWrapperConfig(maximum_steps=100, gym_env_name="",
                                     save_trace=False, reward_shaping=False, scenario=2,
                                     red_agent_type=RedAgentType.B_LINE_AGENT)
    env = CyborgScenarioTwoWrapper(config=config)
    print(CyborgEnvUtil.get_cyborg_hosts())
    import sys
    sys.exit()

    N = 100000
    max_env_steps = 100
    A = env.get_action_space()
    print(len(A))
    costs = {}
    transitions = {}
    for i in range(N):
        print(f"{i}/{N}")
        done = False
        _, info = env.reset()
        s = info["s"]
        t = 1
        while not done and t <= max_env_steps:
            a = np.random.choice(A)
            o, r, done, _, info = env.step(a)
            s_prime = info["s"]
            if s.red_agent_state not in costs:
                costs[int(s.red_agent_state)] = {}
                transitions[int(s.red_agent_state)] = {}
            if s_prime.red_agent_state not in costs:
                costs[int(s_prime.red_agent_state)] = {}
                transitions[int(s_prime.red_agent_state)] = {}

            if a not in transitions[s.red_agent_state]:
                transitions[int(s.red_agent_state)][int(a)] = {}
            if s_prime.red_agent_state not in transitions[s.red_agent_state][a]:
                transitions[int(s.red_agent_state)][int(a)][int(s_prime.red_agent_state)] = 0
            transitions[int(s.red_agent_state)][int(a)][int(s_prime.red_agent_state)] += 1

            if a not in costs[s.red_agent_state]:
                costs[int(s.red_agent_state)][int(a)] = []
            costs[int(s.red_agent_state)][int(a)].append(-r)
            s = s_prime

    import json, io
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