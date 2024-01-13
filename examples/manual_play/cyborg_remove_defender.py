from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender

if __name__ == '__main__':
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=False, decoy_state=False,
        scanned_state=False)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    a = 1
    R = 0
    for t in range(16):
        o, r, done, _, info = csle_cyborg_env.step(a)
        R += r
        print(f"time-step: {t + 1}, cumulative reward: {R}, a: {a}")
        # print(csle_cyborg_env.get_true_table())
        print(csle_cyborg_env.get_table())
        print(csle_cyborg_env.get_actions_table())
        # state = csle_cyborg_env.get_true_state()
        # pprint(state["User1"]["Processes"])
        # for i in range(len(csle_cyborg_env.get_true_table().rows)):
        #     if csle_cyborg_env.cyborg_hostnames[i] == "User0":
        #         continue
        #     a = 1
        #     if csle_cyborg_env.get_true_table().rows[i][5] == "User":
        #         host = csle_cyborg_env.cyborg_hostnames[i]
        #         action_type = BlueAgentActionType.REMOVE
        #         a = csle_cyborg_env.cyborg_action_type_and_host_to_id[(action_type, host)]
        #         print((action_type, host))
        #         break
