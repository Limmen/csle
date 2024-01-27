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


def update_state_vector(state_vector, attacker_state, last_target, success, defender_action_type, defender_action_host):
    if defender_action_type in CyborgEnvUtil.get_decoy_action_types(scenario=2):
        state_vector[defender_action_host][3] = min(
            state_vector[defender_action_host][3] + 1,
            len(CyborgEnvUtil.get_decoy_actions_per_host(scenario=2)[host_idx]) - 1)
    elif defender_action_type == BlueAgentActionType.RESTORE:
        state_vector[defender_action_host][2] = 0

    if attacker_state == 0 and success:
        state_vector[12][0] = 1
        state_vector[11][0] = 1
        state_vector[10][0] = 1
        state_vector[9][0] = 1
    elif attacker_state and success == 1:
        state_vector[last_target][1] = 1
    elif attacker_state and success == 2:
        state_vector[last_target][1] = 1


def get_action_type(red_action):
    action_str_id = str(red_action).split(" ")[0]
    return attacker_action_types.index(action_str_id)


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
    id = 50
    seed = 5024775
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    reset_counts = 0
    total_counts = 0
    for ep in range(episodes):
        print(f"{ep}/{episodes}")
        o, info = csle_cyborg_env.reset()
        s = info[agents_constants.COMMON.STATE]
        state_vec = initial_state_vector()
        true_prev_state_vec = None
        ip_to_host = csle_cyborg_env.get_ip_to_host_mapping()
        subnets = csle_cyborg_env.get_subnetworks()
        attacker_targets = csle_cyborg_env.cyborg_hostnames + subnets
        prev_action = None
        b_line_action = 0
        last_target = 0
        last_targets = {}
        last_targets[b_line_action] = last_target
        red_action_states = [0]
        b_line_action_states = [0]
        for i in range(horizon):
            ad = np.random.choice(defender_actions)
            # ad = ppo_policy.action(o=o)
            o, r, done, _, info = csle_cyborg_env.step(action=ad)
            s = info[agents_constants.COMMON.STATE]
            true_state_vec = CyborgEnvUtil.state_id_to_state_vector(state_id=s, observation=False)
            red_action = csle_cyborg_env.get_last_action(agent="Red")
            red_action_type = get_action_type(red_action=red_action)
            red_success = csle_cyborg_env.get_red_action_success(agent="Red")
            red_action_state = csle_cyborg_env.get_red_action_state()
            red_action_states.append(red_action_state)
            red_target = get_target(attacker_action=red_action, ip_to_host_map=ip_to_host, hosts=cyborg_hosts,
                                    subnets=subnets)
            decoy_state = copy.deepcopy(csle_cyborg_env.decoy_state)
            defender_action_type, defender_action_host = csle_cyborg_env.action_id_to_type_and_host[ad]
            access_type = 0
            if red_action_type == 2:
                host_idx = cyborg_hosts.index(ip_to_host[str(red_action.ip_address)])
                access_type = true_state_vec[host_idx][2]
            if red_success:
                b_line_action += 1 if b_line_action < 14 else 0
            else:
                b_line_action = jumps[b_line_action]
                last_target = last_targets[b_line_action]
            b_line_action_states.append(b_line_action)
            if len(red_action_states) > 2 and red_action_states[-2] == 11:
                total_counts += 1
                if red_action_states[-1] == 1:
                    reset_counts += 1
            # if b_line_action != red_action_state:
            #     raise ValueError(f"i: {i}, red_action_states: {red_action_states}, b_line_action: {b_line_action}, "
            #                      f"b_line_actions: {b_line_action_states}, success: {red_success}, blue action: {ad}, "
            #                      f"{(defender_action_type, defender_action_host)}")
            # if get_action_type_from_state(state=b_line_action) != red_action_type:
            #     raise ValueError("err2")
            target_dist = attacker_state_to_target_distribution(attacker_state=b_line_action, last_target=last_target)
            last_target = np.random.choice(np.arange(0, len(target_dist)), p=target_dist)
            last_targets[b_line_action] = last_target

            if prev_action is None:
                prev_action = (red_action_type, red_action_state, red_action, decoy_state)
                true_prev_state_vec = (true_state_vec.copy(), b_line_action, last_target,
                                       defender_action_type, cyborg_hosts.index(defender_action_host))
                continue

        reset_prob = 0
        if total_counts > 0:
            reset_prob = reset_counts/total_counts
        print(f"total count: {total_counts}, reset count: {reset_counts}, reset_prob: {reset_prob}")