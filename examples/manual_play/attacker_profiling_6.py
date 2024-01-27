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

host_compromised_costs = {
    0: 0,
    1: -1,
    2: -1,
    3: -1,
    4: -0.1,
    5: -0.1,
    6: -0.1,
    7: -1,
    8: 0,
    9: -0.1,
    10: -0.1,
    11: -0.1,
    12: -0.1
}

def reward_function(state_vector, defender_action_type: BlueAgentActionType, red_action_type, red_success, op_server_restored):
    r = 0
    if defender_action_type == BlueAgentActionType.RESTORE:
        r -= 1
    for i in range(len(state_vector)):
        access_state = state_vector[i][2]
        if access_state == 2:
            r += host_compromised_costs[i]
    if red_action_type == 4 and red_success and not op_server_restored:
        r -= 10
    return r

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

    jumps = [0, 1, 2, 2, 2, 2, 5, 5, 5, 5, 9, 9, 9, 12, 13]
    horizon = 100
    episodes = 100000000
    save_every = 100
    id = 41
    seed = 4124775
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
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
        op_server_restored = False
        for i in range(horizon):
            # ad = np.random.choice(defender_actions)
            # ad = np.random.choice([11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32 ,33, 34, 35])
            # ad = np.random.choice([0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
            ad = np.random.choice([3, 18, 19, 20, 21, 22])
            # ad = 4
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

            sv = state_vectors[-1].copy()
            dat, dah = csle_cyborg_env.action_id_to_type_and_host[ad]
            sv = apply_defender_action_to_state(state_vector=sv, defender_action_type=dat,
                                                defender_action_host=cyborg_hosts.index(dah))
            das = action_deterministic_success(attacker_state=red_action_state, target=red_target,
                                               state_vector=sv)

            predicted_reward = reward_function(state_vector=true_state_vec,
                                               defender_action_type=defender_action_type,
                                               red_action_type=red_action_type,
                                               red_success=das, op_server_restored=op_server_restored)
            if ad == 3:
                op_server_restored = True
            if predicted_reward != r:
                print("MISS")
                print(f"predicted reward: {predicted_reward}, actual reward: {r}, ad: {ad}, "
                      f"{true_state_vec[7]}\n {state_vectors[-1][7]}")
                print(f"das: {das}, red_action_state: {red_action_state}, red action: {red_action}, "
                      f"{csle_cyborg_env.cyborg_challenge_env.env.env.env.env.env.environment_controller.observation['Red'].data['success']}")
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
