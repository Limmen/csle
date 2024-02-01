from typing import Dict, List, Tuple
import numpy as np
import random
from gym_csle_cyborg.dao.blue_agent_action_type import BlueAgentActionType
from gym_csle_cyborg.dao.exploit_type import ExploitType
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil
from gym_csle_cyborg.envs.cyborg_scenario_two_wrapper import CyborgScenarioTwoWrapper
from gym_csle_cyborg.dao.csle_cyborg_wrapper_config import CSLECyborgWrapperConfig
from gym_csle_cyborg.dao.cyborg_wrapper_state import CyborgWrapperState


def next_exploit(target_host: int, decoy_state: int, host_ports_map: Dict[int, List[Tuple[int, bool]]],
                 decoy_actions_per_host: List[List[BlueAgentActionType]], decoy_to_port: Dict[int, List[int]],
                 exploit_values: Dict[int, float], exploit_ports: Dict[int, List[int]],
                 exploits: List[ExploitType]) -> Tuple[int, bool, bool, List[int]]:
    """
    Calculates the next exploit of the attacker

    :param target_host: the target of the attacker
    :param decoy_state: the decoy state of the targeted host
    :param host_ports_map: a map from host to ports
    :param decoy_actions_per_host: a list of decoy actions per host
    :param decoy_to_port: a map from decoy action to port
    :param exploit_values: a map of exploits to their values to the attacker
    :param exploit_ports: a map from exploit to required ports
    :param exploits: the list of exploits
    :return: the next exploit, whether it gives root or not, whether it is a decoy or not, and list of ports
    """
    decoy_actions = decoy_actions_per_host[target_host]
    decoy_ports = []
    for i in range(decoy_state):
        decoy_ports.extend(decoy_to_port[decoy_actions[i]])
    ports = host_ports_map[target_host]
    feasible_exploits = []
    feasible_exploits_values = []
    feasible_exploit_access = []
    feasible_exploit_ports = []
    decoy_exploits = []
    for exploit in exploits:
        exploit_access = False
        exploit_feasible = False
        exploit_decoy = False
        target_ports = []
        for port_access in ports:
            port, access = port_access
            if port in exploit_ports[exploit.value]:
                exploit_feasible = True
                target_ports.append(port)
                if not exploit_access:
                    exploit_access = access
        if not exploit_feasible:
            for port in decoy_ports:
                if port in exploit_ports[exploit.value]:
                    exploit_decoy = True
                    exploit_feasible = True
                    target_ports.append(port)
        if exploit_feasible:
            feasible_exploits.append(exploit)
            feasible_exploits_values.append(exploit_values[exploit.value])
            feasible_exploit_access.append(exploit_access)
            decoy_exploits.append(exploit_decoy)
            feasible_exploit_ports.append(target_ports)

    if len(feasible_exploits) == 0:
        return -1, False, False, []
    top_choice = np.argmax(feasible_exploits_values)
    if len(feasible_exploits) == 1 or random.uniform(0, 1) < 0.75:
        return feasible_exploits[top_choice], feasible_exploit_access[top_choice], decoy_exploits[top_choice], \
               feasible_exploit_ports[top_choice]
    else:
        alternatives = [x for x in list(range(len(feasible_exploits))) if x != top_choice]
        random_choice = np.random.choice(list(range(len(alternatives))))
        return (feasible_exploits[random_choice], feasible_exploit_access[random_choice],
                decoy_exploits[random_choice], feasible_exploit_ports[random_choice])

if __name__ == '__main__':
    decoy_state = 1
    target_host = 2
    host_ports_map = CyborgEnvUtil.cyborg_host_ports_map()
    decoy_actions_per_host = CyborgEnvUtil.get_decoy_actions_per_host(scenario=2)
    decoy_to_port = CyborgEnvUtil.cyborg_decoy_actions_to_port()
    exploit_values = CyborgEnvUtil.exploit_values()
    exploit_ports = CyborgEnvUtil.exploit_ports()
    exploits = CyborgEnvUtil.exploits()
    exploit_action, root, decoy, exploit_ports = next_exploit(target_host=target_host, decoy_state=decoy_state, host_ports_map=host_ports_map,
                 decoy_actions_per_host=decoy_actions_per_host, decoy_to_port=decoy_to_port,
                 exploit_values=exploit_values, exploit_ports=exploit_ports, exploits=exploits)
    print(f"exploit: {exploit_action}, root: {root}, decoy: {decoy}, exploit_ports: {exploit_ports}")

    config = CSLECyborgWrapperConfig(maximum_steps=100, gym_env_name="", save_trace=False, reward_shaping=True)
    env = CyborgScenarioTwoWrapper(config=config)
    state = CyborgWrapperState(
        s=[[0, 0, 0, 1], [0, 0, 0, 4], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
           [1, 0, 2, 0], [1, 0, 0, 0], [1, 1, 2, 0], [1, 0, 0, 0], [1, 0, 0, 0]],
        scan_state=[0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        op_server_restored=True,
        obs=[[0, 0, 0, 1], [0, 0, 0, 4], [0, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
             [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        red_agent_state=5,
        privilege_escalation_detected=None,
        red_agent_target=2, red_action_targets={0: 0, 1: 10, 2: 10, 3: 10, 4: 2, 5: 2, 6: 2},
        attacker_observed_decoy=[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    )
    env.set_state(state)
    action = 28


    state = CyborgWrapperState(
        s=[[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
           [0, 0, 0, 0], [1, 0, 2, 0], [1, 0, 0, 0], [1, 1, 2, 0], [1, 0, 0, 0], [1, 0, 0, 0]],
        scan_state=[0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        op_server_restored=False,
        obs=[[0, 0, 0, 0], [0, 0, 0, 0], [1, 2, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
             [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        red_agent_state=5,
        privilege_escalation_detected=None,
        red_agent_target=2, red_action_targets={0: 0, 1: 10, 2: 10, 3: 10, 4: 2},
        attacker_observed_decoy=[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    )
    env.set_state(state)
    action = 8



    state = CyborgWrapperState(
        s=[[0, 0, 0, 0], [1, 1, 0, 2], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
           [0, 0, 0, 0], [1, 0, 2, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 2, 0]],
        scan_state=[0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        op_server_restored=True,
        obs=[[0, 0, 0, 0], [1, 2, 0, 2], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
             [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 0]],
        red_agent_state=5,
        privilege_escalation_detected=None,
        red_agent_target=1, red_action_targets={0: 0, 1: 10, 2: 10, 3: 10, 4: 2},
        attacker_observed_decoy=[0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    )
    action=27
    env.set_state(state)


    state = CyborgWrapperState(
        s=[[0, 0, 0, 0], [1, 1, 0, 0], [0, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
           [0, 0, 0, 0], [1, 0, 2, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 2, 0]],
        scan_state=[0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        op_server_restored=False,
        obs=[[0, 0, 0, 0], [0, 2, 0, 0], [0, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
             [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 0]],
        red_agent_state=5,
        privilege_escalation_detected=None,
        red_agent_target=1, red_action_targets={0: 0, 1: 12, 2: 12, 3: 12, 4: 1, 5: 1, 6: 1},
        attacker_observed_decoy=[0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    )
    action=9
    env.set_state(state)


    state = CyborgWrapperState(
        s=[[0, 0, 0, 0], [0, 0, 0, 4], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
           [0, 0, 0, 0], [1, 0, 2, 0], [1, 0, 0, 0], [1, 1, 2, 0], [1, 0, 0, 0], [1, 0, 0, 0]],
        scan_state=[0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        op_server_restored=True,
        obs=[[0, 0, 0, 0], [0, 0, 0, 4], [0, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
             [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        red_agent_state=5,
        privilege_escalation_detected=None,
        red_agent_target=2, red_action_targets={0: 0, 1: 10, 2: 10, 3: 10, 4: 2, 5: 2, 6: 2},
        attacker_observed_decoy=[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    )
    action=28
    env.set_state(state)



    state = CyborgWrapperState(
        s=[[0, 0, 0, 0], [0, 0, 0, 3], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
           [0, 0, 0, 0], [1, 0, 2, 0], [1, 1, 2, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]],
        scan_state=[0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        op_server_restored=False,
        obs=[[0, 0, 0, 0], [0, 0, 0, 3], [0, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
             [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        red_agent_state=5,
        privilege_escalation_detected=None,
        red_agent_target=2, red_action_targets={0: 0, 1: 9, 2: 9, 3: 9, 4: 2, 5: 2, 6: 2},
        attacker_observed_decoy=[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    )
    action=28
    env.set_state(state)

    state = CyborgWrapperState(
        s=[[0, 0, 0, 0], [1, 1, 0, 3], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
           [0, 0, 0, 0], [1, 0, 2, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 2, 0], [1, 0, 0, 0]],
        scan_state=[0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        op_server_restored=True,
        obs=[[0, 0, 0, 0], [1, 2, 0, 3], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
             [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0]],
        red_agent_state=5,
        privilege_escalation_detected=None,
        red_agent_target=1, red_action_targets={0: 0, 1: 11, 2: 11, 3: 11, 4: 1, 5: 1},
        attacker_observed_decoy=[0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    )
    action=27
    env.set_state(state)


    # state = CyborgWrapperState(
    #     s=[[0, 0, 0, 0], [0, 0, 0, 2], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
    #        [0, 0, 0, 0], [1, 0, 2, 0], [1, 1, 2, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]],
    #     scan_state=[0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    #     op_server_restored=True,
    #     obs=[[0, 0, 0, 0], [0, 0, 0, 2], [0, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
    #          [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    #     red_agent_state=5,
    #     privilege_escalation_detected=None,
    #     red_agent_target=2, red_action_targets={0: 0, 1: 9, 2: 9, 3: 9, 4: 2, 5: 2, 6: 2},
    #     attacker_observed_decoy=[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # )
    # action=28
    env.set_state(state)

    o, r, done, _, info = env.step(action)
    print(env.last_obs)
    print(env.s)