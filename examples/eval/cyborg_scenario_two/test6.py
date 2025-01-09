import numpy as np
import copy
import random
from csle_common.dao.encoding.np_encoder import NpEncoder
from gym_csle_cyborg.envs.cyborg_scenario_two_wrapper import CyborgScenarioTwoWrapper
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.dao.csle_cyborg_wrapper_config import CSLECyborgWrapperConfig
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil


def get_decoy_str(state):
    decoy_state = state.get_decoy_state()
    return f"{min(1, decoy_state[1])},{min(1, decoy_state[2])},{min(1,decoy_state[3])},{min(1,decoy_state[9])},{min(1,decoy_state[10])},{min(1,decoy_state[11])}"

if __name__ == '__main__':
    config = CSLECyborgWrapperConfig(maximum_steps=100, gym_env_name="",
                                     save_trace=False, reward_shaping=False, scenario=2,
                                     red_agent_type=RedAgentType.B_LINE_AGENT)
    env = CyborgScenarioTwoWrapper(config=config)
    action_id_to_type_and_host, type_and_host_to_action_id \
        = CyborgEnvUtil.get_action_dicts(scenario=2, reduced_action_space=True, decoy_state=True, decoy_optimization=False)
    print(action_id_to_type_and_host)
    print(CyborgEnvUtil.get_cyborg_hosts())
    # import sys
    # sys.exit(0)

    action_to_id = {
        0: 27,
        1: 28,
        2: 29,
        3: 30,
        4: 31,
        5: 32
    }

    N = 10000
    max_env_steps = 100
    mu = np.loadtxt("./mu6.txt")
    J = np.loadtxt("./J6.txt")
    import io, json
    with io.open("./state_to_id_6.json", 'r') as f:
        state_to_id = json.loads(f.read())
    for i in range(N):
        print(f"{i}/{N}")
        done = False
        _, info = env.reset()
        s = info["s"]
        t = 1
        R = 0
        while not done and t <= max_env_steps:
            decoy_str = get_decoy_str(s)
            state_id = state_to_id[f"{s.red_agent_state},{decoy_str}"]
            a = -1
            if s.s[1][2] == 2:
                a = 0 # Ent0
            if s.s[2][2] == 2:
                a = 1 # Ent 1
            if s.s[3][2] == 2:
                a = 2 # Ent 2
            if s.s[7][2] == 2:
                a = 3 # Opserver

            #Remove
            # if s.s[1][1] == 1:
            #     a = 8 # Ent0
            # if s.s[2][2] == 1:
            #     a = 9 # Ent 1
            # if s.s[3][2] == 1:
            #     a = 10 # Ent 2
            # if s.s[7][2] == 1:
            #     a = 11 # Opserver
            if s.s[9][2] == 1:
                a = 22 # User1
            if s.s[10][2] == 1:
                a = 23 # User2
            if s.s[11][2] == 1:
                a = 24 # User3
            if s.s[12][2] == 1:
                a = 25 # User4

            if t <= 2:
                a = 31

            if a == -1:
                if np.argmax(mu[state_id]) > 5:
                    a = 27
                else:
                    a = action_to_id[np.argmax(mu[state_id])]
            # print(a)
            # import sys
            # sys.exit()
            o, r, done, _, info = env.step(a)
            s = info["s"]
            t+= 1
            R+= r
            print(f"t:{t}, r: {r}, a: {action_id_to_type_and_host[a]}, R: {R}")