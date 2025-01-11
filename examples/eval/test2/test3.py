import numpy as np
import random
from typing import Dict, List, Tuple
from gym_csle_cyborg.dao.blue_agent_action_type import BlueAgentActionType
from gym_csle_cyborg.dao.exploit_type import ExploitType
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil

def next_exploit(target_host: int, decoy_state: int, host_ports_map: Dict[int, List[Tuple[int, bool]]],
                 decoy_actions_per_host: List[List[BlueAgentActionType]], decoy_to_port: Dict[int, List[int]],
                 exploit_values: Dict[int, float], exploit_ports: Dict[int, List[int]],
                 exploits: List[ExploitType], top_choice_probability: float) -> Tuple[int, bool, bool, List[int]]:
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
    :param top_choice_probability: the probability of choosing the top choice exploit
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
    if len(feasible_exploits) == 1 or random.uniform(0, 1) < top_choice_probability:
        return (feasible_exploits[top_choice], feasible_exploit_access[top_choice], decoy_exploits[top_choice],
                feasible_exploit_ports[top_choice])
    else:
        alternatives = [x for x in list(range(len(feasible_exploits))) if x != top_choice]
        random_choice = np.random.choice(list(range(len(alternatives))))
        return (feasible_exploits[alternatives[random_choice]],
                feasible_exploit_access[alternatives[random_choice]],
                decoy_exploits[alternatives[random_choice]],
                feasible_exploit_ports[alternatives[random_choice]])


if __name__ == '__main__':
    host_ports_map = CyborgEnvUtil.cyborg_host_ports_map()
    decoy_to_port = CyborgEnvUtil.cyborg_decoy_actions_to_port()
    exploit_values = CyborgEnvUtil.exploit_values()
    exploit_ports = CyborgEnvUtil.exploit_ports()
    exploits = CyborgEnvUtil.exploits()
    host_to_subnet = CyborgEnvUtil.cyborg_host_to_subnet()
    decoy_actions_per_host = CyborgEnvUtil.get_decoy_actions_per_host(scenario=2)
    decoy_action_types = CyborgEnvUtil.get_decoy_action_types(scenario=2)
    # target_hosts = [1,2,3,7,9,10,11,12]
    target_hosts = [1,2,3,9,10,11]
    for host in target_hosts:
        for decoy_state in range(len(decoy_actions_per_host[host])+1):
            outcomes = []
            for k in range(500000):
                _, _, decoy, _ = next_exploit(
                    target_host=host, decoy_state=decoy_state, host_ports_map=host_ports_map,
                    decoy_actions_per_host=decoy_actions_per_host, decoy_to_port = decoy_to_port, exploit_values=exploit_values,
                    exploits=exploits, top_choice_probability=0.75, exploit_ports=exploit_ports
                )
                outcomes.append(int(decoy))
            print(f"host: {host}, decoy state: {decoy_state}, exploit_success_prob = {1-np.mean(outcomes)}")