import random
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender


def info_to_vec(info, decoy_state, hosts):
    """
    Creates the state vector

    :param info: the info
    :param decoy_state: the decoy state
    :param hosts: the host list
    :return: the state vector
    """
    state_vec = []
    for host in hosts:
        known = info[host][3]
        known = int(known)
        scanned = info[host][4]
        scanned = int(scanned)
        access = info[host][5]
        if access == "None":
            access = 0
        elif access == "User":
            access = 1
        else:
            access = 2
        d_state = len(decoy_state[host])
        state_vec.append([known, scanned, access, d_state])
    return state_vec


def state_vec_to_id(state_vec):
    """
    Converts a state vector to an id

    :param state_vec: the state vector to convert
    :return: the id
    """
    bin_id = ""
    for host_vec in state_vec:
        host_bin_str = ""
        for i, elem in enumerate(host_vec):
            if i == 0:
                host_bin_str += format(elem, '01b')
            if i == 1:
                host_bin_str += format(elem, '01b')
            if i == 2:
                host_bin_str += format(elem, '02b')
            if i == 3:
                host_bin_str += format(elem, '03b')
        bin_id += host_bin_str
    id = int(bin_id, 2)
    return id


def id_to_state_vec(id: int):
    """
    Converts an id to a state vector

    :param id: the id to convert
    :return: the state vector
    """
    bin_str = format(id, "091b")
    host_bins = [bin_str[i:i + 7] for i in range(0, len(bin_str), 7)]
    state_vec = []
    for host_bin in host_bins:
        known = int(host_bin[0:1], 2)
        scanned = int(host_bin[1:2], 2)
        access = int(host_bin[2:4], 2)
        decoy = int(host_bin[4:7], 2)
        host_vec = [known, scanned, access, decoy]
        state_vec.append(host_vec)
    return state_vec


if __name__ == '__main__':
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    str_info = str(csle_cyborg_env.cyborg_challenge_env.env.env.env.info)
    states = {}
    state_idx = 0
    host_state_lookup = host_state_to_id(hostnames=csle_cyborg_env.cyborg_hostnames)
    host_ids = list(csle_cyborg_env.cyborg_hostname_to_id.values())

    for i in range(100000):
        done = False
        csle_cyborg_env.reset()
        actions = list(csle_cyborg_env.action_id_to_type_and_host.keys())
        state_key = str(csle_cyborg_env.cyborg_challenge_env.env.env.env.info)
        if state_key not in states:
            states[state_key] = state_idx
            state_idx += 1

        while not done:
            a = random.choice(actions)
            o, r, done, _, info = csle_cyborg_env.step(a)
            state_vec = info_to_vec(csle_cyborg_env.get_true_table().rows, csle_cyborg_env.decoy_state,
                                    host_state_lookup, host_ids)
            state_key = state_vec_to_id(state_vec=state_vec)
            stv = id_to_state_vec(id=state_key)
            assert stv == state_vec
