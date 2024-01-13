from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender
from gym_csle_cyborg.dao.blue_agent_action_type import BlueAgentActionType
import numpy as np


def get_host_value(hostname: str):
    """
    Gets the value of a host

    :param hostname: the hostname to get the value of
    :return: the value
    """
    if hostname == "Op_Server0":
        return 4
    if hostname == "Enterprise2":
        return 3
    if hostname in ["Enterprise0", "Enterprise1"]:
        return 2
    if hostname in ["User1", "User2", "User3", "User4"]:
        return 1


def get_decoy_host(t, decoy_state, true_table, csle_cyborg_env):
    """
    Gets the next decoy host to check

    :param t: the current time-step
    :param decoy_state: the decoy state
    :param true_table: the true table state
    :param csle_cyborg_env: the environment to use for evaluation
    :return: the decoy host or None
    """
    host_id_enterprise_0 = csle_cyborg_env.cyborg_hostnames.index("Enterprise0")
    host_id_enterprise_1 = csle_cyborg_env.cyborg_hostnames.index("Enterprise1")
    host_id_enterprise_2 = csle_cyborg_env.cyborg_hostnames.index("Enterprise2")
    host_id_op_server = csle_cyborg_env.cyborg_hostnames.index("Op_Server0")
    host_id_user_1 = csle_cyborg_env.cyborg_hostnames.index("User1")
    host_id_user_2 = csle_cyborg_env.cyborg_hostnames.index("User2")
    host_id_user_3 = csle_cyborg_env.cyborg_hostnames.index("User3")
    host_id_user_4 = csle_cyborg_env.cyborg_hostnames.index("User4")
    if t == 0:
        return "Enterprise0"
    if t == 1:
        return "Enterprise1"
    if t == 2:
        return "Enterprise0"
    if t == 3:
        return "Enterprise1"
    if t == 4:
        if true_table.rows[host_id_enterprise_0][3]:
            return "Enterprise0"
        elif true_table.rows[host_id_enterprise_1][3]:
            return "Enterprise1"

    if true_table.rows[host_id_enterprise_0][4] and true_table.rows[host_id_enterprise_0][5] == "None" \
            and not len(decoy_state["Enterprise0"]) == 5:
        return "Enterprise0"

    if true_table.rows[host_id_enterprise_1][4] and true_table.rows[host_id_enterprise_1][5] == "None" \
            and not len(decoy_state["Enterprise1"]) == 5:
        return "Enterprise1"

    if true_table.rows[host_id_enterprise_2][4] and true_table.rows[host_id_enterprise_2][5] == "None" \
            and not len(decoy_state["Enterprise2"]) == 5:
        return "Enterprise2"

    if true_table.rows[host_id_user_1][4] and not len(decoy_state["User1"]) == 5 and \
            true_table.rows[host_id_user_1][5] == "None":
        return "User1"
    if true_table.rows[host_id_user_2][4] and not len(decoy_state["User2"]) == 5 and \
            true_table.rows[host_id_user_2][5] == "None":
        return "User2"
    if true_table.rows[host_id_user_3][4] and not len(decoy_state["User3"]) == 5 and \
            true_table.rows[host_id_user_3][5] == "None":
        return "User3"
    if true_table.rows[host_id_user_4][4] and not len(decoy_state["User4"]) == 5 and \
            true_table.rows[host_id_user_4][5] == "None":
        return "User4"

    if true_table.rows[host_id_op_server][5] == "None" and not len(decoy_state["Op_Server0"]) == 5:
        return "Op_Server0"
    return None


def is_enterprise_or_opserver_compromised(true_table, csle_cyborg_env):
    """
    Utility function to check if a enterprise or opserver is compromised

    :param true_table: the true state
    :param csle_cyborg_env: the environment
    :return:
    """
    for i in range(len(true_table.rows)):
        if "Enterprise" not in csle_cyborg_env.cyborg_hostnames[i] and "Op_Server" \
                not in csle_cyborg_env.cyborg_hostnames[i]:
            continue
        if true_table.rows[i][5] == "User":
            return True
        elif true_table.rows[i][5] == "Privileged":
            return True
    return False


def eval(csle_cyborg_env) -> float:
    """
    Runs one evaluation run with the environment

    :param csle_cyborg_env: the environment to use for evaluation
    :return: the return
    """
    decoy_state = {}
    decoy_state["Enterprise0"] = []
    decoy_state["Enterprise1"] = []
    decoy_state["Enterprise2"] = []
    decoy_state["Op_Server0"] = []
    decoy_state["User1"] = []
    decoy_state["User2"] = []
    decoy_state["User3"] = []
    decoy_state["User4"] = []
    decoy_actions_order = [
        BlueAgentActionType.DECOY_FEMITTER,
        BlueAgentActionType.DECOY_HARAKA_SMPT,
        BlueAgentActionType.DECOY_TOMCAT,
        BlueAgentActionType.DECOY_SMSS,
        BlueAgentActionType.DECOY_SVCHOST,
        BlueAgentActionType.DECOY_SSHD
    ]
    R = 0
    true_table = csle_cyborg_env.get_true_table()
    decoy_host = get_decoy_host(t=0, decoy_state=decoy_state, true_table=true_table, csle_cyborg_env=csle_cyborg_env)
    decoy_action = decoy_actions_order[len(decoy_state[decoy_host])]
    decoy_state[decoy_host].append(decoy_action)
    a = csle_cyborg_env.cyborg_action_type_and_host_to_id[(decoy_action, decoy_host)]
    for t in range(100):
        o, r, done, _, info = csle_cyborg_env.step(a)
        R += r
        # print(f"time-step: {t+1}, cumulative reward: {R}, a: {a}")
        true_table = csle_cyborg_env.get_true_table()
        decoy_host = get_decoy_host(t=t + 1, decoy_state=decoy_state, true_table=true_table,
                                    csle_cyborg_env=csle_cyborg_env)
        is_key_compromised = is_enterprise_or_opserver_compromised(true_table=true_table,
                                                                   csle_cyborg_env=csle_cyborg_env)
        if decoy_host is not None and true_table.rows[csle_cyborg_env.cyborg_hostnames.index(decoy_host)][5] != "None":
            is_key_compromised = True
        if not is_key_compromised and decoy_host is not None:
            decoy_action = decoy_actions_order[len(decoy_state[decoy_host])]
            decoy_state[decoy_host].append(decoy_action)
            a = csle_cyborg_env.cyborg_action_type_and_host_to_id[(decoy_action, decoy_host)]
        else:
            host_recovery_actions = []
            host_recovery_priorities = []
            for i in range(len(true_table.rows)):
                if csle_cyborg_env.cyborg_hostnames[i] == "User0":
                    continue
                if true_table.rows[i][5] == "User":
                    host = csle_cyborg_env.cyborg_hostnames[i]
                    action_type = BlueAgentActionType.REMOVE
                    a = csle_cyborg_env.cyborg_action_type_and_host_to_id[(action_type, host)]
                    host_recovery_actions.append(a)
                    host_recovery_priorities.append(get_host_value(host))
                    break
                elif true_table.rows[i][5] == "Privileged" and "User" not in csle_cyborg_env.cyborg_hostnames[i]:
                    host = csle_cyborg_env.cyborg_hostnames[i]
                    action_type = BlueAgentActionType.RESTORE
                    a = csle_cyborg_env.cyborg_action_type_and_host_to_id[(action_type, host)]
                    host_recovery_actions.append(a)
                    host_recovery_priorities.append(get_host_value(host))
                    decoy_state[host] = []
                    break
            if len(host_recovery_actions) == 0:
                decoy_host = get_decoy_host(t=t + 1, decoy_state=decoy_state, true_table=true_table,
                                            csle_cyborg_env=csle_cyborg_env)
                if decoy_host is not None:
                    decoy_action = decoy_actions_order[len(decoy_state[decoy_host])]
                    decoy_state[decoy_host].append(decoy_action)
                    a = csle_cyborg_env.cyborg_action_type_and_host_to_id[(decoy_action, decoy_host)]
                a = 1
            else:
                host_recovery_idx = np.argmax(host_recovery_priorities)
                a = host_recovery_actions[host_recovery_idx]
    return R


if __name__ == '__main__':
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=False, decoy_state=False,
        scanned_state=False)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    csle_cyborg_env.reset()
    returns = []
    for i in range(20):
        print(f"{i}/{20}")
        returns.append(eval(csle_cyborg_env=csle_cyborg_env))
    print(np.mean(returns))

    # print(csle_cyborg_env.get_true_table())
    # print(csle_cyborg_env.get_actions_table())
    # print(csle_cyborg_env.get_true_table())
