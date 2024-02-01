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
    action_sequence = [2, 3, 0, 27, 27, 9, 27, 9, 8, 9, 27, 8, 9, 8 ,9, 9, 8, 27, 8, 8, 9, 8, 9, 8, 0, 8]
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
        blue_actions = []
        blue_targets = []
        blue_types = []
        while t < max_horizon:
            # a = np.random.choice([0, 8, 4, 27])
            # a = 27

            # if t < len(action_sequence):
            #     a = action_sequence[t]
            # else:
            a = np.random.choice(A)
            # a = 31
            # if t > 20:
            #     a = 3
            # a = 4
            # if t == 4:
            #     a = random.choice([8, 9])
            # if t < len(actions):
            #     a = actions[t]
            # if t == 3:
            #     # a = 22
            #     a = 16

            # if t == 6:
            #     # a = 10
            #     a = 1

            # a = ppo_policy.action(o=o)
            # if a == 0:
            #     zeros.append(0)
            # if a == 1:
            #     ones.append(1)

            # if t < 8:
            #     a = 32
            # else:
            #     a = 18
            # a = 27
            # if t == 0:
            #     a = 31
            # if t == 1:
            #     a = 30
            # if a == 34:
            #     import random
            #     a = random.choice([27, 28, 29])
            o, r, done, _, info = csle_cyborg_env.step(a)
            # print("STEP DONE")
            state_id = info[env_constants.ENV_METRICS.STATE]
            oid = info[env_constants.ENV_METRICS.OBSERVATION]
            s = CyborgEnvUtil.state_id_to_state_vector(state_id=state_id)
            obs = CyborgEnvUtil.state_id_to_state_vector(state_id=oid, observation=True)
            red_action = csle_cyborg_env.get_last_action(agent='Red')
            red_success = csle_cyborg_env.get_red_action_success()

            defender_action_type, defender_action_host = csle_cyborg_env.action_id_to_type_and_host[a]
            defender_action_host_id = csle_cyborg_env.cyborg_hostnames.index(defender_action_host)
            # if len(red_actions) > 2:
            #     if blue_actions[-2] == 0 and red_targets[-1] == 1:
            #         if not red_success:
            #             print(f"blue action: {blue_actions[-1]}")
            #             print(csle_cyborg_env.get_true_table())
            #             print(csle_cyborg_env.get_actions_table())
            # print(f"Red success: {red_success}")
            # if not red_success and "Exploit" in str(red_actions[-1]):
            #     pass

            if len(red_actions) > 0 and len(blue_actions) > 2:
                if not red_success and "Exploit" in str(red_actions[-1]):
                    if red_targets[-1] == blue_targets[-1] and blue_types[-1] in csle_cyborg_env.decoy_action_types:
                        if states[-1][red_targets[-1]][3] < len(csle_cyborg_env.decoy_actions_per_host[red_targets[-1]]):
                            print(f"Decoy at the same time as exploit and fail, activity: {observations[-1][red_targets[-1]][0]}, "
                                  f"target: {red_targets[-1]}, decoy state: {states[-1][red_targets[-1]][3]}, "
                                  f"blue type: {BlueAgentActionType(blue_types[-1])}")
                            # print(csle_cyborg_env.get_actions_table())
                        # if observations[-1][red_targets[-1]][0] != 2:
                        #     csle_cyborg_env.get_true_table()
                    # if observations[-1][red_targets[-1]][0] == 2:
                    #     print(f"Observed exploit activity after failed exploit, obs: {observations[-1][red_targets[-1]]}, target: {red_targets[-1]}")


                    # else:
                    #     if observations[-1][red_targets[-1]][0] == 0:
                    #         print(csle_cyborg_env.get_true_table())
                    #         print(csle_cyborg_env.get_actions_table())
                    # print(f"activity: {observations[-1][red_targets[-1]][0]}, state: {states[-1][red_targets[-1]][2]}")

            # if len(red_actions) > 0 and len(blue_actions) > 2:
            #     if not red_success and "Exploit" in str(red_actions[-1]):
            #         red_target = red_targets[-1]
            #         obs = observations[-1]
            #         if red_target == 1 and blue_actions[-1] != 0 and blue_actions[-2] == 0 and blue_actions[-1] == 8:
            #             print(obs[red_target][0] == 0)
            # print("Failed exploit, no scan on ent0")
            # # print(blue_targets[-1])
            # # print(red_target)
            # print(f"compromised state: {states[-1][red_target][2]}, blue action: {blue_actions[-1]}, "
            #       f"previous blue: {blue_actions[-2]}, obs: {obs[red_target]}, previous obs: {observations[-1][red_target]}")

            # if len(red_actions) > 0:
            #     if not red_success and "Exploit" in str(red_actions[-1]):
            #         red_target = red_targets[-1]
            #         obs = observations[-1]
            #         # if red_target == 1:
            #         #     print(f"failed red target is ent0, activity: {obs[red_target][0]}")
            #         if obs[red_target][0] == 0 and red_target == 1 and blue_actions[-1] != 0:
            #             print("Failed exploit, no scan on ent0")
            #             print()
            #             # print(blue_targets[-1])
            #             # print(red_target)
            #             print(f"compromised state: {states[-1][red_target][2]}, blue action: {blue_actions[-1]}, "
            #                   f"previous blue: {blue_actions[-2]}, obs: {obs[red_target]}, previous obs: {observations[-1][red_target]}")

            red_actions.append(red_action)
            states.append(s)
            observations.append(obs)
            blue_actions.append(a)
            blue_targets.append(defender_action_host_id)
            blue_types.append(defender_action_type)
            if "Exploit" in str(red_action):
                ip = red_action.ip_address
                host= csle_cyborg_env.get_ip_to_host_mapping()[str(ip)]
                host_id = csle_cyborg_env.cyborg_hostnames.index(host)
                red_targets.append(host_id)
            else:
                red_targets.append(0)

            # print(f"t: {t}, r: {r}, a: {a}, {csle_cyborg_env.get_last_action(agent='Red')}")

            # for host in range(len(obs)):
            #     if obs[host][0] == 2 and s[host][2] == 0:
            #         red_action = csle_cyborg_env.get_last_action(agent='Red')
            #         print(f"EXPLOIT FALSE POSITIVE: {obs[host]}, {s[host]}")
            #         print(red_action)
            #         print(csle_cyborg_env.get_actions_table())
            #         print(csle_cyborg_env.get_true_table())
            #         print(csle_cyborg_env.get_table())
            #         print(f"Exploit type: {obs[host][2]}")

            # if t == 1:
            #     if obs[12][0] == 1:
            #         user4_count += 1
            #     if obs[11][0] == 1:
            #         user3_count += 1
            #     if obs[10][0] == 1:
            #         user2_count += 1
            #     if obs[9][0] == 1:
            #         user1_count += 1
            #     sum = user1_count + user2_count + user3_count + user4_count
            # if sum > 50:
            #     print(f"user1: {user1_count/sum}, user2: {user2_count/sum}, user3: {user3_count/sum}, user4: {user4_count/sum}")


            # print(f"a: {a}")
            # print(s)
            # print(obs)
            # red_action = csle_cyborg_env.get_last_action(agent='Red')
            # print(t)
            # print(str(red_action))
            # if t== 4:
            #     print(str(red_action))
            # if t == 5 and "DiscoverNetworkServices" in str(red_action):
            #     print(f"SCAN, {obs[1][0]}, {obs[2][0]}")
            # if t==4 and obs[1][0] == 0 and obs[2][0] == 0 and "DiscoverNetworkServices" in str(red_action):
            #     print("Scan not detected")
            #     print(csle_cyborg_env.get_actions_table())
            #     print(csle_cyborg_env.get_true_table())


            # if "DiscoverNetworkServices" in str(red_action):
            #     ip = red_action.ip_address
            #     host= csle_cyborg_env.get_ip_to_host_mapping()[str(ip)]
            #     host_id = csle_cyborg_env.cyborg_hostnames.index(host)
            #     if obs[host_id][0] == 0:
            #         print("Scan not detected")
            #         print(csle_cyborg_env.get_actions_table())
            #         print(csle_cyborg_env.get_true_table())

            # if obs[1][0] == 0 and obs[2][0] == 0 and "DiscoverNetworkServices" in str(red_action):
            #     ip = red_action.ip_address
            #     host= csle_cyborg_env.get_ip_to_host_mapping()[str(ip)]
            #     if host in ["Enterprise0", "Enterprise1"]:
            #         print("Scan not detected")
            #         print(csle_cyborg_env.get_actions_table())
            #         print(csle_cyborg_env.get_true_table())

            # print(csle_cyborg_env.get_last_action(agent='Red'))
            # print(csle_cyborg_env.get_table())
            # print(f"t: {t}, a:{a}")
            # print(csle_cyborg_env.get_true_table())

            # print(obs[11])
            # print(o[14*10:14*10+14])
            # print(o[14*11:14*11+14])
            # print(o[14*12:14*12+14])
            # print(o[14*13:14*13+14])
            # print(o)
            # print(o)
            # if t == 0:
            #     print(o)
            #     print(type(o))
            #     print(list(o.tolist()).index(1))

            # print(f"t: {t}, r: {r}, a: {a}, s: {s}")
            # print(f"a: {csle_cyborg_env.action_id_to_type_and_host[a]}")
            # print(csle_cyborg_env.get_true_table())
            R += r
            t += 1
        returns.append(R)
        # print(f"{i}/{num_evaluations}, avg R: {np.mean(returns)}, R: {R}, ones: {len(ones)}, zeros: {len(zeros)}")