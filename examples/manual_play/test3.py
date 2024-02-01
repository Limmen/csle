import numpy as np
import torch
import random
from csle_common.metastore.metastore_facade import MetastoreFacade
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil
import gym_csle_cyborg.constants.constants as env_constants
from gym_csle_cyborg.dao.blue_agent_action_type import BlueAgentActionType

if __name__ == '__main__':
    ppo_policy = MetastoreFacade.get_ppo_policy(id=58)
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False, cache_visited_states=False)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    num_evaluations = 10000
    max_horizon = 100
    returns = []
    seed = 215125
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    A = csle_cyborg_env.get_action_space()
    print("Starting policy evaluation")
    user1_count = 0
    user2_count = 0
    user3_count = 0
    user4_count = 0
    for i in range(num_evaluations):
        done = False
        o, _ = csle_cyborg_env.reset()
        R = 0
        t = 0
        ones = []
        zeros = []
        # actions = [31, 31, 32, 8]
        # actions = [31, 31, 32, 29]
        red_actions = []
        states = []
        observations = []
        red_targets = []
        while t < max_horizon:
            a = np.random.choice(A)
            # a = 4
            o, r, done, _, info = csle_cyborg_env.step(a)
            state_id = info[env_constants.ENV_METRICS.STATE]
            oid = info[env_constants.ENV_METRICS.OBSERVATION]
            s = CyborgEnvUtil.state_id_to_state_vector(state_id=state_id)
            obs = CyborgEnvUtil.state_id_to_state_vector(state_id=oid, observation=True)
            red_action = csle_cyborg_env.get_last_action(agent='Red')
            red_success = csle_cyborg_env.get_red_action_success()
            red_state = csle_cyborg_env.get_red_action_state()
            red_target = -1
            if "Exploit" in str(red_action) or "NetworkServices"in str(red_action):
                ip = red_action.ip_address
                host= csle_cyborg_env.get_ip_to_host_mapping()[str(ip)]
                host_id = csle_cyborg_env.cyborg_hostnames.index(host)
                red_target = host_id
            elif "Privileg" in str(red_action):
                host = red_action.hostname
                host_id = csle_cyborg_env.cyborg_hostnames.index(host)
                red_target = host_id

            if a in [8, 9, 10, 11, 22, 23, 24, 25, 26]:
                defender_target =  1
                if a == 9:
                    defender_target = 2
                if a == 10:
                    defender_target = 3
                if a == 11:
                    defender_target = 7
                if a == 22:
                    defender_target = 9
                if a == 23:
                    defender_target = 10
                if a == 24:
                    defender_target = 11
                if a == 25:
                    defender_target = 12
                if a == 26:
                    defender_target = 0
                # if defender_target == 1 and obs[defender_target][2] != 3:
                #     print(csle_cyborg_env.get_true_table())
                #     print(csle_cyborg_env.get_table())
                #     print(csle_cyborg_env.get_actions_table())
                # if defender_target == 1 and red_state == 2 and s[defender_target][2] == 0:
                #     print(obs[defender_target][2])
                # if defender_target in [1,2,3, 9, 10, 11, 12, 0] \
                #         and s[defender_target][1] == 1 and s[defender_target][2] == 0 and "Privilege" in str(red_action) \
                #         and red_target == defender_target:
                #     if obs[defender_target][2] != 3:
                #         print("Privilege escalation but not unknown!")
                #         print(f"red target: {red_target}")
                #         print(f"defender target: {defender_target}")
                #         print(f"obs: {obs[defender_target]}")

                # if defender_target in [1,2,3, 9, 10, 11, 12, 0] \
                #         and s[defender_target][1] == 1 and s[defender_target][2] == 0 and red_target == defender_target:
                #     if obs[defender_target][2] != 3:
                #         print("Privilege escalation but not unknown!")
                #         print(f"red target: {red_target}")
                #         print(f"defender target: {defender_target}")
                #         print(f"obs: {obs[defender_target]}")
                #         print(f"state: {s[defender_target]}")
                #         print(f"red action: {red_action}")
                #         print("----------")


                phi = "Privilege" in str(red_action) and red_target == defender_target
                if defender_target in [1,2,3, 9, 10, 11, 12, 0] \
                        and s[defender_target][1] == 1 and s[defender_target][2] == 0 and not phi \
                        and obs[defender_target][2] == 3:
                    print("Unknown even though not comprimised and not escalation")
                    print(f"red target: {red_target}")
                    print(f"defender target: {defender_target}")
                    print(f"obs: {obs[defender_target]}")
                    print(f"previous obs: {observations[-1][defender_target]}")
                    print(f"state: {s[defender_target]}")
                    print(f"red action: {red_action}")
                    print("----------")

                # if defender_target in [1,2,3, 9, 10, 11, 12, 0] and obs[defender_target][2] == 3 and s[defender_target][1] == 1 and s[defender_target][2] == 0:
                #     print(f"target: {defender_target}, red action: {red_action}")
                    # print(red_state)
                    # print(csle_cyborg_env.get_true_table())
                    # # print(csle_cyborg_env.get_table())
                    # print(csle_cyborg_env.get_actions_table())
            states.append(s)
            observations.append(obs)

            # print(csle_cyborg_env.get_true_table())


            R += r
            t += 1
        returns.append(R)
        # print(f"{i}/{num_evaluations}, avg R: {np.mean(returns)}, R: {R}, ones: {len(ones)}, zeros: {len(zeros)}")