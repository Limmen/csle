import numpy as np
import torch
import random
from csle_common.metastore.metastore_facade import MetastoreFacade
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.dao.red_agent_action_type import RedAgentActionType
from gym_csle_cyborg.dao.blue_agent_action_type import BlueAgentActionType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil
import csle_agents.constants.constants as agents_constants


def meander_agent(scanned_subnets, scanned_hosts, exploited_hosts, escalated_hosts):
    pass

def last_action_unsuccessful(state_vec, red_action_type, red_action_target):
    if red_action_type == RedAgentActionType.IMPACT and state_vec[red_action_target][2] < 2:
        return False
    if red_action_type == RedAgentActionType.PRIVILEGE_ESCALATE and state_vec[red_action_target] [2] < 2:
        return False
    if red_action_type == RedAgentActionType.EXPLOIT_REMOTE_SERVICE and state_vec[red_action_target][2] < 1:
        return False
    return True


if __name__ == '__main__':
    # ppo_policy = MetastoreFacade.get_ppo_policy(id=3)
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False, cache_visited_states=False)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    num_evaluations = 1000
    max_horizon = 100
    returns = []
    seed = 68172
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    A = csle_cyborg_env.get_action_space()
    # for a in A:
    #     blue_action_type, blue_action_host = csle_cyborg_env.action_id_to_type_and_host[a]
    #     print(f"{a}, {str(blue_action_type)}, {blue_action_host}")
    # print("Starting policy evaluation")
    for i in range(num_evaluations):
        o, info = csle_cyborg_env.reset()
        # print(csle_cyborg_env.get_true_table())
        R = 0
        t = 0
        s_prime = info[agents_constants.COMMON.STATE]
        s = CyborgEnvUtil.state_id_to_state_vector(state_id=s_prime)

        scanned_subnets = []
        scanned_hosts = []
        exploited_hosts = []
        escalated_hosts = []
        last_host = None
        last_ip = None

        red_action_types = []
        red_action_targets = []
        observations = []
        states = []
        while t < max_horizon:
            actions = A.copy()
            # actions.remove(3)
            a = np.random.choice(actions)
            # a = np.random.choice([0, 1, 2, 3, 16, 17, 18, 19, 20])
            # a = 35
            # if t > 5:
            #     a = np.random.choice([26, 2])
            # a = 4
            # if t == 11:
            #     a = 1
            o, r, done, _, info = csle_cyborg_env.step(a)
            s = info[agents_constants.COMMON.STATE]
            obs_id = info[agents_constants.COMMON.OBSERVATION]
            s_vec = CyborgEnvUtil.state_id_to_state_vector(state_id=s)
            obs_vec = CyborgEnvUtil.state_id_to_state_vector(state_id=obs_id, observation=True)
            blue_action_type, blue_action_host = csle_cyborg_env.action_id_to_type_and_host[a]
            blue_action_host_id = csle_cyborg_env.cyborg_hostnames.index(blue_action_host)

            red_action_type = csle_cyborg_env.get_attacker_action_type()
            red_action_target = csle_cyborg_env.get_attacker_action_target()
            # red_success = last_action_unsuccessful(state_vec=s_vec, red_action_type=red_action_type,
            #                                        red_action_target=red_action_target)
            states.append(s_vec)
            observations.append(obs_vec)

            if red_action_target == 7 and red_action_type == 2 and s_vec[7][2] == 0:
                # print(obs_vec[7])
                if obs_vec[7][0] == 0:
                    print(f"ent2: {s_vec[3][2]}")
                    print(obs_vec[7])
                    print(a)
                    # print(csle_cyborg_env.get_true_table())
                    # print(csle_cyborg_env.get_actions_table())
                    # print(csle_cyborg_env.get_table())


            # if red_action_target == 7 and red_action_type == 2:
            #     print(csle_cyborg_env.get_true_table())
            #     print(csle_cyborg_env.get_table())
            #     print(csle_cyborg_env.get_actions_table())

            # if not red_success:
            #     print(f"FAILED RED, {red_action_type}, {red_action_target}, {s_vec}")
            # else:
            #     print(f"RED SUCCESS, {red_action_type}, {red_action_target}, {s_vec}")
            # red_success = csle_cyborg_env.get_red_action_success()
            # if len(red_action_targets) > 0:
            #     if red_action_types[-1] == RedAgentActionType.EXPLOIT_REMOTE_SERVICE and red_success:
            #         if red_action_targets[-1] not in exploited_hosts:
            #             exploited_hosts.append(red_action_targets[-1])
            #     if red_action_types[-1] == RedAgentActionType.PRIVILEGE_ESCALATE and red_success:
            #         if red_action_targets[-1] not in escalated_hosts:
            #             escalated_hosts.append(red_action_targets[-1])
            #     if red_action_types[-1] == RedAgentActionType.DISCOVER_NETWORK_SERVICES and red_success:
            #         if red_action_targets[-1] not in scanned_hosts:
            #             scanned_hosts.append(red_action_targets[-1])
            #     if red_action_types[-1] == RedAgentActionType.DISCOVER_REMOTE_SYSTEMS and red_success:
            #         if red_action_targets[-1] not in scanned_subnets:
            #             scanned_subnets.append(red_action_targets[-1])
            #
            # if blue_action_type == BlueAgentActionType.RESTORE:
            #     escalated_hosts.remove(blue_action_host_id)
            #     exploited_hosts.remove(blue_action_host_id)
            # if blue_action_type == BlueAgentActionType.REMOVE:
            #     pass
            red_action_targets.append(red_action_target)
            red_action_targets.append(red_action_target)

            # s_prime = info[agents_constants.COMMON.STATE]
            # s = CyborgEnvUtil.state_id_to_state_vector(state_id=s_prime)
            # print(csle_cyborg_env.get_last_action(agent='Red'))
            # print(csle_cyborg_env.get_true_table())
            # if t == 11 or t == 12:
            #     print(csle_cyborg_env.get_true_table())
            #     print(csle_cyborg_env.get_actions_table())
            R += r
            t += 1
        returns.append(R)
        # print(f"{i}/{num_evaluations}, avg R: {np.mean(returns)}, R: {R}")
