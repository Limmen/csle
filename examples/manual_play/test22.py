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
    # ppo_policy = MetastoreFacade.get_ppo_policy(id=58)
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False, cache_visited_states=False)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    num_evaluations = 1000
    max_horizon = 25
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
        # action_sequence = [31, 27, 28, 4, 12, 32, 23, 31, 8, 35, 32, 13, 26, 7, 23, 33, 9, 11, 26, 24, 10, 30, 35, 8, 29, 24, 1, 25, 1, 5, 10, 33, 9, 24, 1, 27, 1, 29, 9, 1, 1, 32, 1, 4, 1, 6, 1, 35, 1, 26, 24, 8, 27, 21, 1, 15, 1, 11, 1, 35, 1, 15, 1, 26, 1, 12, 1, 29, 1, 10, 8, 10]
        mm = False
        kk = False
        s = None
        remove_done = False
        while t < max_horizon:
            # a = np.random.choice(A)
            # a = np.random.choice([5, 28])
            a = 31
            # if t > 1 and s[9][2] > 0:
            #     a = 12
            # if t > 2 and s[12][2] > 0:
            #     print(s[12][2])
            if t >= 2 and s[10][2] == 1:
                a = 23
                print("REMOVE")
            if remove_done:
                a = 13
                print("ANALYZE")
            if a == 23:
                remove_done = True
            defender_action_type, defender_action_host = csle_cyborg_env.action_id_to_type_and_host[a]
            defender_action_host_id = csle_cyborg_env.cyborg_hostnames.index(defender_action_host)
            # if a == 6:
            #     print("ANALYZE")
            o, r, done, _, info = csle_cyborg_env.step(a)
            state_id = info[env_constants.ENV_METRICS.STATE]
            oid = info[env_constants.ENV_METRICS.OBSERVATION]
            s = CyborgEnvUtil.state_id_to_state_vector(state_id=state_id)
            obs = CyborgEnvUtil.state_id_to_state_vector(state_id=oid, observation=True)
            # print(obs[9])
            if defender_action_type == BlueAgentActionType.ANALYZE:
                print(f"ANALYZE obs: {obs[10]}, s: {s[10]}")
                # print(csle_cyborg_env.get_true_table())
            if defender_action_type == BlueAgentActionType.REMOVE:
                print(f"REMOVE obs: {obs[10]}, s: {s[10]}")

            # if "Exploit" in str(csle_cyborg_env.get_last_action(agent="Red")):
            #     print(f"exploit: {csle_cyborg_env.get_last_action(agent='Red')}, "
            #           f"target: {csle_cyborg_env.get_ip_to_host_mapping()[str(csle_cyborg_env.get_last_action(agent='Red').ip_address)]}")
            # print(csle_cyborg_env.get_true_table())
            R += r
            t += 1
        returns.append(R)
        # print(f"{i}/{num_evaluations}, avg R: {np.mean(returns)}, R: {R}, ones: {len(ones)}, zeros: {len(zeros)}")