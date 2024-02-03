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
    # action_sequence = [2, 3, 3, 27, 27, 8, 9, 27, 9, 8, 8, 8, 9, 8, 27, 8, 28, 33]
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
        red_types = []
        blue_actions = []
        blue_targets = []
        blue_types = []
        action_sequence = [31, 27, 28, 4, 12, 32, 23, 31, 8, 35, 32, 13, 26, 7, 23, 33, 9, 11, 26, 24, 10, 30, 35, 8, 29, 24, 1, 25, 1, 5, 10, 33, 9, 24, 1, 27, 1, 29, 9, 1, 1, 32, 1, 4, 1, 6, 1, 35, 1, 26, 24, 8, 27, 21, 1, 15, 1, 11, 1, 35, 1, 15, 1, 26, 1, 12, 1, 29, 1, 10, 8, 10]
        mm = False
        kk = False
        while t < max_horizon:
            a = np.random.choice(A)

            defender_action_type, defender_action_host = csle_cyborg_env.action_id_to_type_and_host[a]
            defender_action_host_id = csle_cyborg_env.cyborg_hostnames.index(defender_action_host)
            o, r, done, _, info = csle_cyborg_env.step(a)

            state_id = info[env_constants.ENV_METRICS.STATE]
            oid = info[env_constants.ENV_METRICS.OBSERVATION]
            s = CyborgEnvUtil.state_id_to_state_vector(state_id=state_id)
            obs = CyborgEnvUtil.state_id_to_state_vector(state_id=oid, observation=True)
            red_action = csle_cyborg_env.get_last_action(agent='Red')
            red_success = csle_cyborg_env.get_red_action_success()

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
                red_types.append(2)
            elif "Privilege" in str(red_action):
                host = red_action.hostname
                host_id = csle_cyborg_env.cyborg_hostnames.index(host)
                red_targets.append(host_id)
                red_types.append(3)
            elif "Impact" in str(red_action):
                red_types.append(4)
                red_targets.append(-1)
            elif "Systems" in str(red_action):
                red_types.append(0)
                red_targets.append(-1)
            elif "Services" in str(red_action):
                red_types.append(1)
                red_targets.append(-1)
            else:
                red_targets.append(0)
                red_types.append(0)
                red_targets.append(-1)

            if defender_action_type == BlueAgentActionType.ANALYZE.value:
                if obs[defender_action_host_id][2] > s[defender_action_host_id][2]:
                    print(f"obs: {obs[defender_action_host_id]}, s: {s[defender_action_host_id]}, "
                          f"host: {defender_action_host_id}, last attacker target: {red_targets[-1]} "
                          f"last attacker type: {red_types[-1]}")
                    last_restore = 0
                    for i in range(len(blue_actions)):
                        if blue_types[i] == BlueAgentActionType.RESTORE and blue_targets[i] == defender_action_host_id:
                            last_restore = i
                    num_exploits_since_last_restore = 0
                    previous_states = []
                    attacker_actions = []
                    for i in range(len(red_actions)):
                        if i >= last_restore:
                            previous_states.append(states[i][defender_action_host_id])
                            attacker_actions.append((red_types[i], red_targets[i]))
                        if red_types[i] == 2 and red_targets[i] == defender_action_host_id and i >= last_restore:
                            num_exploits_since_last_restore += 1
                    print(f"Exploits since restore: {num_exploits_since_last_restore}")
                    print(f"States since restore: \n{previous_states}")
                    print(f"Attacker actions since restore: \n{attacker_actions}")
                # if obs[defender_action_host_id][2] == 2 and s[defender_action_host_id][2] == 0:
                #     last_restore = 0
                #     for i in range(len(blue_actions)):
                #         if blue_types[i] == BlueAgentActionType.RESTORE and blue_targets[i] == defender_action_host_id:
                #             last_restore = i
                #     num_exploits_since_last_restore = 0
                #     for i in range(len(red_actions)):
                #         if red_types[i] == 2 and red_targets[i] == defender_action_host_id and i >= last_restore:
                #             num_exploits_since_last_restore += 1
                #
                #     print(f"Observed old malware, exploits since restore: {num_exploits_since_last_restore}")


            R += r
            t += 1
        returns.append(R)
        # print(f"{i}/{num_evaluations}, avg R: {np.mean(returns)}, R: {R}, ones: {len(ones)}, zeros: {len(zeros)}")