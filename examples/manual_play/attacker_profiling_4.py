import numpy as np
import copy
import torch
import random
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil
from gym_csle_cyborg.dao.blue_agent_action_type import BlueAgentActionType
import csle_agents.constants.constants as agents_constants
from csle_common.metastore.metastore_facade import MetastoreFacade

cyborg_hostname_values = {
    "Defender": 3,
    "Enterprise0": 3,
    "Enterprise1": 3,
    "Enterprise2": 4,
    "Op_Host0": 5,
    "Op_Host1": 5,
    "Op_Host2": 5,
    "Op_Server0": 6,
    "User0": 1,
    "User1": 2,
    "User2": 2,
    "User3": 2,
    "User4": 2
}
attacker_action_types = [
    "DiscoverRemoteSystems", "DiscoverNetworkServices", "ExploitRemoteService", "PrivilegeEscalate", "Impact"
]


def attacker_state_to_target_distribution(attacker_state: int, last_target: int = -1):
    if attacker_state == 0:
        return [1.0, 0, 0]
    elif attacker_state == 1:
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.25, 0.25, 0.25, 0.25]
    elif attacker_state in [2, 3, 5, 6, 9, 10, 12, 13, 14]:
        prob = [0] * 13
        prob[last_target] = 1
        return prob
    elif attacker_state == 4:
        if last_target == 12 or last_target == 11:
            return [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif last_target == 9 or last_target == 10:
            return [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        else:
            raise ValueError(f"Invalid last target: {last_target}")
    elif attacker_state == 7:
        return [0, 1.0, 0]
    elif attacker_state == 8:
        return [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif attacker_state == 11:
        return [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
    else:
        raise ValueError(f"Invalid attacker state: {attacker_state}")


def get_access_state(host_state_vector, access_state_lookup):
    known = host_state_vector[0]
    scanned = host_state_vector[1]
    access = host_state_vector[2]
    return access_state_lookup[(known, scanned, access)]


def get_access_state_lookup():
    lookup = {}
    s = 0
    for known in [0, 1]:
        for scanned in [0, 1]:
            for access in [0, 1, 2]:
                lookup[(known, scanned, access)] = s
                s += 1
    return lookup


def get_target(attacker_action, ip_to_host_map, hosts, subnets):
    if hasattr(attacker_action, 'hostname'):
        target = attacker_action.hostname
        return hosts.index(target)
    elif hasattr(attacker_action, 'subnet'):
        target = str(attacker_action.subnet)
        return subnets.index(target)
    elif hasattr(attacker_action, 'ip_address'):
        target = ip_to_host_map[str(attacker_action.ip_address)]
        return hosts.index(target)
    else:
        raise ValueError(f"Action: {attacker_action} not recognized")


def get_action_type_from_state(state: int):
    if state == 0:
        return 0
    elif state == 1:
        return 1
    elif state == 2:
        return 2
    elif state == 3:
        return 3
    elif state == 4:
        return 1
    elif state == 5:
        return 2
    elif state == 6:
        return 3
    elif state == 7:
        return 0
    elif state == 8:
        return 1
    elif state == 9:
        return 2
    elif state == 10:
        return 3
    elif state == 11:
        return 1
    elif state == 12:
        return 2
    elif state == 13:
        return 3
    elif state == 14:
        return 4
    else:
        raise ValueError(f"Invalid attacker state: {state}")


def initial_state_vector():
    return [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
            [0, 0, 0, 0], [1, 0, 2, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]


def apply_defender_action_to_state(state_vector, defender_action_type, defender_action_host):
    if (defender_action_type in CyborgEnvUtil.get_decoy_action_types(scenario=2)
            and state_vector[defender_action_host][3] == len(CyborgEnvUtil.get_decoy_actions_per_host(scenario=2)[defender_action_host])):
        defender_action_type = BlueAgentActionType.REMOVE

    if defender_action_type in CyborgEnvUtil.get_decoy_action_types(scenario=2):
        state_vector[defender_action_host][3] = min(
            state_vector[defender_action_host][3] + 1,
            len(CyborgEnvUtil.get_decoy_actions_per_host(scenario=2)[defender_action_host]))
    elif defender_action_type == BlueAgentActionType.RESTORE:
        state_vector[defender_action_host][2] = 0
    elif defender_action_type == BlueAgentActionType.REMOVE:
        if state_vector[defender_action_host][2] == 1:
            state_vector[defender_action_host][2] = 0
    return state_vector

def update_state_vector(state_vector, attacker_state, last_target, success, defender_action_type, defender_action_host,
                        reset, access_type, next_target):
    if defender_action_type in CyborgEnvUtil.get_decoy_action_types(scenario=2):
        state_vector[defender_action_host][3] = min(
            state_vector[defender_action_host][3] + 1,
            len(CyborgEnvUtil.get_decoy_actions_per_host(scenario=2)[defender_action_host]) - 1)
    elif defender_action_type == BlueAgentActionType.RESTORE:
        state_vector[defender_action_host][2] = 0
    elif defender_action_type == BlueAgentActionType.REMOVE:
        if state_vector[defender_action_host][2] == 1:
            state_vector[defender_action_host][2] = 0

    if attacker_state == 0 and success:
        state_vector[12][0] = 1
        state_vector[11][0] = 1
        state_vector[10][0] = 1
        state_vector[9][0] = 1
    elif attacker_state == 1 and success:
        state_vector[last_target][1] = 1
    elif attacker_state == 2 and success:
        state_vector[last_target][2] = access_type
    elif attacker_state == 3 and success:
        state_vector[last_target][2] = 2
        state_vector[next_target][0] = 1
    elif attacker_state == 4 and success:
        state_vector[last_target][1] = 1
    elif attacker_state == 5 and success:
        state_vector[last_target][2] = access_type
    elif attacker_state == 6 and success:
        state_vector[last_target][2] = 2
    elif attacker_state == 7 and success:
        state_vector[0][0] = 1
        state_vector[1][0] = 1
        state_vector[2][0] = 1
        state_vector[3][0] = 1
    elif attacker_state == 8 and success:
        state_vector[3][1] = 1
    elif attacker_state == 9 and success:
        state_vector[3][2] = access_type
    elif attacker_state == 10 and success:
        state_vector[3][2] = 2
        state_vector[7][0] = 1
    elif attacker_state == 11 and success:
        state_vector[7][1] = 1
    elif attacker_state == 12 and success:
        state_vector[7][2] = access_type
    elif attacker_state == 13 and success:
        state_vector[7][2] = 2

    if reset:
        pass


def get_action_type(red_action):
    action_str_id = str(red_action).split(" ")[0]
    return attacker_action_types.index(action_str_id)


def action_deterministic_success(attacker_state, state_vector, target):
    if attacker_state == 0:
        return True
    elif attacker_state == 1:
        return state_vector[target][0] == 1
    elif attacker_state == 2:
        return state_vector[target][1] == 1
    elif attacker_state == 3:
        return state_vector[target][2] > 0
    elif attacker_state == 4:
        return state_vector[target][0] == 1
    elif attacker_state == 5:
        return state_vector[target][1] == 1
    elif attacker_state == 6:
        return state_vector[target][2] > 0
    elif attacker_state == 7:
        return (state_vector[1][2] > 0 or state_vector[2][2] > 0)
    elif attacker_state == 8:
        return state_vector[3][0] == 1
    elif attacker_state == 9:
        return state_vector[3][1] == 1
    elif attacker_state == 10:
        return state_vector[3][2] > 0
    elif attacker_state == 11:
        return state_vector[3][2] == 2 and state_vector[7][0] == 1
    elif attacker_state == 12:
        return state_vector[7][1] == 1
    elif attacker_state == 13:
        return state_vector[7][2] > 0
    elif attacker_state == 14:
        return state_vector[7][2] == 2



if __name__ == '__main__':
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False, cache_visited_states=False, save_trace=False)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    cyborg_hosts = csle_cyborg_env.cyborg_hostnames
    defender_actions = csle_cyborg_env.get_action_space()
    subnets = csle_cyborg_env.get_subnetworks()
    decoys = CyborgEnvUtil.get_decoy_action_types(scenario=config.scenario)
    # ppo_policy = MetastoreFacade.get_ppo_policy(id=98)

    exploit_success = np.zeros((len(cyborg_hosts), len(decoys)))
    exploit_counts = np.zeros((len(cyborg_hosts), len(decoys)))
    exploit_root = np.zeros((len(cyborg_hosts), len(decoys)))
    exploit_user = np.zeros((len(cyborg_hosts), len(decoys)))
    exploit_type_counts = np.zeros((len(cyborg_hosts), len(decoys)))

    jumps = [0, 1, 2, 2, 2, 2, 5, 5, 5, 5, 9, 9, 9, 12, 13]
    horizon = 100
    episodes = 100000000
    save_every = 100
    id = 10
    seed = 10819202
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    user_counts = {
        9: 0,
        10: 0,
        11: 0,
        12: 0
    }
    for ep in range(episodes):
        print(f"{ep}/{episodes}")
        o, info = csle_cyborg_env.reset()
        s = info[agents_constants.COMMON.STATE]
        state_vec = initial_state_vector()
        ip_to_host = csle_cyborg_env.get_ip_to_host_mapping()
        subnets = csle_cyborg_env.get_subnetworks()
        attacker_targets = csle_cyborg_env.cyborg_hostnames + subnets
        prev_action = None
        b_line_action = 0
        last_target = 0
        last_targets = {}
        last_targets[b_line_action] = last_target
        red_action_states = [0]
        red_actions = []
        state_vectors = [state_vec.copy()]
        b_line_action_states = [0]
        targets = [0]
        defender_actions_history = []
        red_action_types = []
        for i in range(horizon):
            ad = np.random.choice(defender_actions)
            # ad = np.random.choice([27, 28, 29, 30, 31, 32 ,33, 34, 35])
            # ad = 31
            # ad = 4
            # ad = 27
            o, r, done, _, info = csle_cyborg_env.step(action=ad)
            s = info[agents_constants.COMMON.STATE]
            true_state_vec = CyborgEnvUtil.state_id_to_state_vector(state_id=s, observation=False)
            red_action = csle_cyborg_env.get_last_action(agent="Red")
            red_action_type = get_action_type(red_action=red_action)
            red_success = csle_cyborg_env.get_red_action_success()
            red_base_jump = csle_cyborg_env.get_red_base_jump()
            red_action_state = csle_cyborg_env.get_red_action_state()
            red_target = get_target(attacker_action=red_action, ip_to_host_map=ip_to_host, hosts=cyborg_hosts,
                                    subnets=subnets)
            # print(red_target)
            defender_action_type, defender_action_host = csle_cyborg_env.action_id_to_type_and_host[ad]
            if len(red_actions) > 1 and len(state_vectors) >= 2:
                sv = state_vectors[-2].copy()
                ad_old = defender_actions_history[-1]
                dat, dah = csle_cyborg_env.action_id_to_type_and_host[ad_old]
                sv = apply_defender_action_to_state(state_vector=sv, defender_action_type=dat,
                                                    defender_action_host=cyborg_hosts.index(dah))
                das = action_deterministic_success(attacker_state=red_action_states[-1], target=targets[-1],
                                                   state_vector=sv)

                if das and not red_success and get_action_type(red_actions[-1]) != 2:
                    print(f"red action failed, das: {das}, a_state:{red_action_states[-1]}, "
                          f"defender_action: {defender_actions_history[-1]},"
                          f"{red_actions[-1]}, state: {sv}")

                if das and get_action_type(red_actions[-1]) == 2:
                    host_idx = cyborg_hosts.index(ip_to_host[str(red_actions[-1].ip_address)])
                    host = ip_to_host[str(red_actions[-1].ip_address)]
                    if i == 3:
                        user_counts[host_idx] += 1
                    # if host == "User2":
                    #     print(f"i: {i}, Exploit {ip_to_host[str(red_actions[-1].ip_address)]}, id: {host_idx}, success: {red_success}")
                    host_decoy_state = sv[host_idx][3]
                    exploit_success[host_idx][host_decoy_state] += int(red_success)
                    exploit_counts[host_idx][host_decoy_state] += 1
                    e_access_type = state_vectors[-1][host_idx][2]
                    exploit_type_counts[host_idx][host_decoy_state] += 1
                    if e_access_type == 1:
                        exploit_user[host_idx][host_decoy_state] += 1
                    elif e_access_type == 2:
                        exploit_root[host_idx][host_decoy_state] += 1
            # if len(red_action_states) > 2 and red_action_states[-1] == 11 and red_action_state == 1:
            #     print("reset!")
            #     sv = state_vectors[-2].copy()
            #     print(state_vectors[-1])
            #     print(state_vectors[-2])
            #     print(state_vectors[-3])
            #     print(state_vectors[-4])
            #     print(state_vectors[-5])
            #     print(defender_actions_history[-5:])
            #     ad_old = defender_actions_history[-1]
            #     dat, dah = csle_cyborg_env.action_id_to_type_and_host[ad_old]
            #     sv = apply_defender_action_to_state(state_vector=sv, defender_action_type=dat,
            #                                         defender_action_host=cyborg_hosts.index(dah))
            #     das = action_deterministic_success(attacker_state=red_action_states[-1], target=targets[-1],
            #                                        state_vector=sv)
            #     print(f"reset das: {das}")
            red_action_states.append(red_action_state)
            red_actions.append(red_action)
            red_action_types.append(red_action_type)
            state_vectors.append(true_state_vec.copy())
            targets.append(red_target)
            defender_actions_history.append(ad)
            decoy_state = copy.deepcopy(csle_cyborg_env.decoy_state)
            access_type = 0
            if red_action_type == 2:
                host_idx = cyborg_hosts.index(ip_to_host[str(red_action.ip_address)])
                access_type = true_state_vec[host_idx][2]
            if red_base_jump:
                b_line_action = 1
                last_target = last_targets[b_line_action]
            else:
                if red_success:
                    b_line_action += 1 if b_line_action < 14 else 0
                else:
                    b_line_action = jumps[b_line_action]
                    last_target = last_targets[b_line_action]
            if b_line_action != red_action_state:
                print(f"mismatch: {b_line_action}, {red_action_state}")
            b_line_action_states.append(b_line_action)
            target_dist = attacker_state_to_target_distribution(attacker_state=b_line_action, last_target=last_target)
            last_target = np.random.choice(np.arange(0, len(target_dist)), p=target_dist)
            last_targets[b_line_action] = last_target


        # for host_idx in range(exploit_counts.shape[0]):
        #     for decoy_state in range(exploit_counts.shape[1]):
        #         exploit_prob = 0
        #         if exploit_counts[host_idx][decoy_state] > 0:
        #             exploit_prob = exploit_success[host_idx][decoy_state] / exploit_counts[host_idx][decoy_state]
        #         print(f"host: {cyborg_hosts[host_idx]}, decoy_state: {decoy_state} "
        #               f"exploit prob: {exploit_prob}"
        # if exploit_counts[10][0] > 0:
        # print(exploit_success[10][3]/exploit_counts[10][3])
        # print(exploit_success[1][0]/exploit_counts[1][0])
        # print(user_counts)

        if ep % save_every == 0:
            with open(f'/home/kim/exploit_success_{id}.npy', 'wb') as f:
                np.save(f, np.array(exploit_success))
            with open(f'/home/kim/exploit_counts_{id}.npy', 'wb') as f:
                np.save(f, np.array(exploit_counts))
            with open(f'/home/kim/exploit_root_{id}.npy', 'wb') as f:
                np.save(f, np.array(exploit_root))
            with open(f'/home/kim/exploit_user_{id}.npy', 'wb') as f:
                np.save(f, np.array(exploit_user))
            with open(f'/home/kim/exploit_type_counts_{id}.npy', 'wb') as f:
                np.save(f, np.array(exploit_type_counts))
