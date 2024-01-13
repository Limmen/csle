from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender
from gym_csle_cyborg.dao.blue_agent_action_type import BlueAgentActionType

if __name__ == '__main__':
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=False, decoy_state=False,
        scanned_state=False)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    R = 0
    a = 1
    for t in range(12):
        o, r, done, _, info = csle_cyborg_env.step(a)
        R += r
        print(f"time-step: {t + 1}, cumulative reward: {R}, a: {a}")
    print(csle_cyborg_env.get_true_table())
    print(csle_cyborg_env.get_actions_table())
    print("--------------------------------------")
    a = csle_cyborg_env.cyborg_action_type_and_host_to_id[(BlueAgentActionType.ANALYZE, "Enterprise2")]
    csle_cyborg_env.step(a)
    print(csle_cyborg_env.get_true_table())
    print(csle_cyborg_env.get_table())
    print(csle_cyborg_env.get_actions_table())
