from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender
from gym_csle_cyborg.envs.cyborg_scenario_two_wrapper import CyborgScenarioTwoWrapper
from gym_csle_cyborg.dao.cyborg_wrapper_state import CyborgWrapperState
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil
from gym_csle_cyborg.dao.csle_cyborg_wrapper_config import CSLECyborgWrapperConfig
import csle_agents.constants.constants as agents_constants

def get_wrapper_state_from_cyborg(cyborg_env: CyborgScenarioTwoDefender, obs_id, t) -> CyborgWrapperState:
    scan_state = cyborg_env.scan_state
    op_server_restored = False
    privilege_escalation_detected = False
    obs_vector = CyborgEnvUtil.state_id_to_state_vector(state_id=obs_id, observation=True)
    decoy_state = cyborg_env.decoy_state.copy()
    bline_base_jump = False
    scanned_subnets = [0, 0, 0]
    for i in range(len(scan_state)):
        if i in [9, 10, 11, 12] and scan_state[i] > 0:
            scanned_subnets[0] = 1
        if i in [3,4,5,6,7] and scan_state[i] > 0:
            scanned_subnets[1] = 1
        if i in [4,5,6,7] and scan_state[i] > 0:
            scanned_subnets[2] = 1
    red_action_targets = {}
    red_action_targets[0] = 0
    if scan_state[9] > 0:
        red_action_targets[1] = 9
        red_action_targets[2] = 9
        red_action_targets[3] = 9
        red_action_targets[4] = 2
        red_action_targets[5] = 2
        red_action_targets[6] = 2
    elif scan_state[10] > 0:
        red_action_targets[1] = 10
        red_action_targets[2] = 10
        red_action_targets[3] = 10
        red_action_targets[4] = 2
        red_action_targets[5] = 2
        red_action_targets[6] = 2
    elif scan_state[11] > 0:
        red_action_targets[1] = 11
        red_action_targets[2] = 11
        red_action_targets[3] = 11
        red_action_targets[4] = 1
        red_action_targets[5] = 1
        red_action_targets[6] = 1
    elif scan_state[12] > 0:
        red_action_targets[1] = 12
        red_action_targets[2] = 12
        red_action_targets[3] = 12
        red_action_targets[4] = 1
        red_action_targets[5] = 1
        red_action_targets[6] = 1
    red_action_targets[7] = 1
    red_action_targets[8] = 3
    red_action_targets[9] = 3
    red_action_targets[10] = 7
    red_action_targets[11] = 7
    red_action_targets[12] = 7
    s = []
    access_list = csle_cyborg_env.get_access_list()
    red_agent_state = csle_cyborg_env.get_bline_state()
    for i in range(len(CyborgEnvUtil.get_cyborg_hosts())):
        known = 0
        scanned = min(scan_state[i], 1)
        if scanned:
            known = 1
        if t > 0 and i in [9, 10, 11, 12]:
            known = 1
        if red_agent_state >= 6 and i in [0,1, 2, 3]:
            known = 1
        if red_agent_state >= 8 and i in [4,5,6,7]:
            known = 1
        access = access_list[i]
        decoy = len(decoy_state[i])
        host_state = [known, scanned, access, decoy]
        s.append(host_state)
    malware_state = [0 for _ in range(len(scan_state))]
    ssh_access = [0 for _ in range(len(scan_state))]
    escalated = [0 for _ in range(len(scan_state))]
    exploited = [0 for _ in range(len(scan_state))]
    detected = [0 for _ in range(len(scan_state))]
    red_agent_target = red_action_targets[red_agent_state]
    wrapper_state = CyborgWrapperState(s=s, scan_state=scan_state, op_server_restored=op_server_restored,
                                       obs=obs_vector,
                                       red_action_targets=red_action_targets,
                                       privilege_escalation_detected=privilege_escalation_detected,
                                       red_agent_state=red_agent_state, red_agent_target=red_agent_target, malware_state=malware_state,
                                       ssh_access=ssh_access, escalated=escalated, exploited=exploited,
                                       bline_base_jump=bline_base_jump, scanned_subnets=scanned_subnets,
                                       attacker_observed_decoy=decoy_state, detected=detected)
    return wrapper_state

if __name__ == '__main__':
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False, cache_visited_states=False)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    csle_cyborg_env.reset()
    config = CSLECyborgWrapperConfig(maximum_steps=100, gym_env_name="",
                                     save_trace=False, reward_shaping=False, scenario=2,
                                     red_agent_type=RedAgentType.B_LINE_AGENT)
    train_env = CyborgScenarioTwoWrapper(config=config)
    # print(train_env.scanned_subnets)
    t = 0
    while t <= 3:
        _, _, _, _, info = csle_cyborg_env.step(31)
        obs = info[agents_constants.COMMON.OBSERVATION]
        state = get_wrapper_state_from_cyborg(cyborg_env=csle_cyborg_env, obs_id=obs, t=t)
        t+= 1



