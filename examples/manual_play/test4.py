import io
import random

import numpy as np
from collections import Counter
from csle_common.metastore.metastore_facade import MetastoreFacade
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil
import csle_agents.constants.constants as constants
import json


def get_position(cyborg_hostname_values, state_vector, hostnames):
    access_values = []
    for i in range(len(list(cyborg_hostname_values.keys()))):
        access_state = state_vector[i][2]
        if access_state in [1, 2]:
            access_values.append(cyborg_hostname_values[hostnames[i]])
        else:
            access_values.append(0)
    position_idx = np.argmax(access_values)
    return position_idx

def get_position2(cyborg_hostname_values, access_states, hostnames):
    access_values = []
    for i in range(len(list(cyborg_hostname_values.keys()))):
        access_state = access_states[i]
        if access_state in [1, 2]:
            access_values.append(cyborg_hostname_values[hostnames[i]])
        else:
            access_values.append(0)
    position_idx = np.argmax(access_values)
    return position_idx


def get_target(attacker_action, ip_to_host_map, attacker_targets):
    if hasattr(attacker_action, 'hostname'):
        target = attacker_action.hostname
    elif hasattr(attacker_action, 'subnet'):
        target = str(attacker_action.subnet)
    elif hasattr(attacker_action, 'ip_address'):
        target = ip_to_host_map[str(attacker_action.ip_address)]
    else:
        raise ValueError(f"Action: {attacker_action} not recognized")
    target_idx = attacker_targets.index(target)
    return target_idx


def update_model(attacker_model, access, observation):
    if access not in attacker_model["observation_given_access"]:
        attacker_model["observation_given_access"][access] = []
    attacker_model["observation_given_access"][access].append(observation)
    return attacker_model

def convert_samples_to_distribution(samples):
    """
    Converts a list of samples to a probability distribution

    :param samples: the list of samples
    :return: a dict with the sample values and their probabilities
    """
    cnt = Counter(samples)
    _sum = sum(cnt.values())
    return {k: v / _sum for k, v in cnt.items()}


def get_action_type(red_action, action_types):
    action_str_id = str(red_action).split(" ")[0]
    return action_types.index(action_str_id)


def get_access_state_lookup():
    lookup = {}
    s = 0
    for known in [0 ,1]:
        for scanned in [0,1]:
            for access in [0,1,2]:
                lookup[(known, scanned, access)] = s
                s+= 1
    return lookup

def get_obs_lookup():
    lookup = {}
    s = 0
    for activity in [0 ,1, 2]:
        for access in [0,1,2, 3]:
            lookup[(activity, access)] = s
            s+= 1
    return lookup

def get_access_state(host_state_vector, access_state_lookup):
    known = host_state_vector[0]
    scanned = host_state_vector[1]
    access = host_state_vector[2]
    return access_state_lookup[(known, scanned, access)]


def get_obs(host_obs_vector, obs_lookup):
    activity = host_obs_vector[0]
    access = host_obs_vector[1]
    return obs_lookup[(activity, access)]

def parse_attacker_model():
    model = {}
    with io.open("/home/kim/attacker_model.json", 'r', encoding='utf-8') as f:
        json_str = f.read()
        model_1 = json.loads(json_str)
        model["R"] = model_1["red_action_given_target_and_access"]
        model["T"] = model_1["target_given_position_and_access"]
    with io.open("/home/kim/attacker_model2.json", 'r', encoding='utf-8') as f:
        json_str = f.read()
        model_2 = json.loads(json_str)
        model["A"] = model_2["access_given_target_redaction_decoystate_and_access"]

    with io.open("/home/kim/attacker_model3.json", 'r', encoding='utf-8') as f:
        json_str = f.read()
        model_3 = json.loads(json_str)
        model["O"] = model_3["observation_given_access"]
    return model

def position_probability(hosts, access_state_lookup, cyborg_hostname_values, hostnames, b, position):
    positions = hosts
    access_states = []
    for host in hosts:
        max_access_state = np.argmax(b[host])
        for k,v in access_state_lookup.items():
            if v == max_access_state:
                (known, scanned, access) = k
                access_states.append(access)
    ce_position = get_position2(cyborg_hostname_values, access_states, hostnames)
    if position == ce_position:
        return 1.0
    else:
        return 0.0

def compute_beliefs(obs: int, attacker_model, host: int, access_state_lookup, b, hosts, hostnames,
                    cyborg_hostname_values):
    positions = hosts
    new_belief = []
    normalizing_constant = 0
    for access_val in list(access_state_lookup.keys()):
        for access_val_2 in list(access_state_lookup.keys()):
            for p in positions:
                p_prob = position_probability(
                    hosts=hosts, access_state_lookup=access_state_lookup,
                    cyborg_hostname_values=cyborg_hostname_values, hostnames=hostnames, b=b, position=p)
                print(attacker_model["T"][p].keys())
                # normalizing_constant += attacker_model["T"][p][access_val_2]*b[host][access_val_2]*p_prob*attacker_model["O"][access_val][obs]

    for access_val in list(access_state_lookup.keys()):
        prob = 0
        for p in positions:
            p_prob = position_probability(
                hosts=hosts, access_state_lookup=access_state_lookup,
                cyborg_hostname_values=cyborg_hostname_values, hostnames=hostnames, b=b, position=p)
            for access_val_2 in list(access_state_lookup.keys()):
                prob2 = attacker_model["T"][p][access_val_2]*b[host][access_val_2]*p_prob*attacker_model["O"][access_val][obs]
                prob += prob2
        new_belief.append(prob/normalizing_constant)
    return new_belief



if __name__ == '__main__':
    # ppo_policy = MetastoreFacade.get_ppo_policy(id=22)
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False, cache_visited_states=True)
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
    action_types = [
        "DiscoverRemoteSystems", "DiscoverNetworkServices", "ExploitRemoteService", "PrivilegeEscalate", "Impact"
    ]
    defender_actions = [27, 28, 29, 30, 31, 32, 33, 34, 35]
    access_state_lookup = get_access_state_lookup()
    obs_lookup = get_obs_lookup()
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    o, info = csle_cyborg_env.reset()
    s = info[constants.ENV_METRICS.STATE]
    b = ([[0]*len(access_state_lookup)])*len(csle_cyborg_env.cyborg_hostnames)
    print(b)
    state_vector = CyborgEnvUtil.state_id_to_state_vector(state_id=s, observation=False)
    for host_idx in range(len(csle_cyborg_env.cyborg_hostnames)):
        a_state = get_access_state(host_state_vector=state_vector[host_idx], access_state_lookup=access_state_lookup)
        b[host_idx][a_state]=1

    attacker_model = parse_attacker_model()
    print(attacker_model)
    num_episodes = 1000
    for i in range(num_episodes):
        print(f"episode {i}/{num_episodes}")
        o, info = csle_cyborg_env.reset()
        subnets = csle_cyborg_env.get_subnetworks()
        attacker_targets = csle_cyborg_env.cyborg_hostnames + subnets
        ip_to_host = csle_cyborg_env.get_ip_to_host_mapping()
        done = False
        while not done:
            a = random.choice(defender_actions)
            o, r, done, _, info = csle_cyborg_env.step(action=a)
            s = info[constants.ENV_METRICS.STATE]
            oid = info[constants.ENV_METRICS.OBSERVATION]
            obs_vector = CyborgEnvUtil.state_id_to_state_vector(state_id=oid, observation=True)
            host = 0
            obs = get_obs(host_obs_vector=obs_vector[host], obs_lookup=obs_lookup)
            b[host] = compute_beliefs(obs=obs, attacker_model=attacker_model, host=host, access_state_lookup=access_state_lookup,
                            hosts=list(range(len(csle_cyborg_env.cyborg_hostnames))),
                            hostnames=csle_cyborg_env.cyborg_hostnames, cyborg_hostname_values=cyborg_hostname_values,
                            b=b)
            # position = get_position(cyborg_hostname_values=cyborg_hostname_values,
            #                         state_vector=CyborgEnvUtil.state_id_to_state_vector(state_id=s, observation=False),
            #                         hostnames=csle_cyborg_env.cyborg_hostnames)
            # red_action = csle_cyborg_env.get_last_action(agent="Red")
            # red_action_type = get_action_type(red_action=red_action, action_types=action_types)
            # target_idx = get_target(attacker_action=red_action, ip_to_host_map=ip_to_host,
            #                         attacker_targets=attacker_targets)
            # state_vector = CyborgEnvUtil.state_id_to_state_vector(state_id=s, observation=False)
            # obs_vector = CyborgEnvUtil.state_id_to_state_vector(state_id=oid, observation=True)
            # target_decoy_state = 0
            # target_access_state = 0
            # target_obs_state = 0
            # if target_idx < len(state_vector):
            #     target_access_state = get_access_state(host_state_vector=state_vector[target_idx],
            #                                            access_state_lookup=access_state_lookup)
            #     target_decoy_state = csle_cyborg_env.get_host_decoy_state(host_id=target_idx)
            # for host_id in range(len(csle_cyborg_env.cyborg_hostnames)):
            #     obs = get_obs(host_obs_vector=obs_vector[host_id], obs_lookup=obs_lookup)
            #     access_state = get_access_state(host_state_vector=state_vector[host_id],
            #                                            access_state_lookup=access_state_lookup)
            #     counts = update_model(attacker_model=counts,  access=access_state, observation=obs)
            #
            # position_access_state = 0
            # if position < len(state_vector):
            #     position_access_state = get_access_state(host_state_vector=state_vector[position],
            #                                            access_state_lookup=access_state_lookup)