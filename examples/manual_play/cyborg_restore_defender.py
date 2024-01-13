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
    a = 1
    R = 0
    for t in range(100):
        o, r, done, _, info = csle_cyborg_env.step(a)
        R += r
        print(f"time-step: {t+1}, cumulative reward: {R}, a: {a}")
        for i in range(len(info["obs_per_host"])):
            a = 1
            if info["obs_per_host"][i]["compromised"].value > 0:
                host = csle_cyborg_env.cyborg_hostnames[i]
                action_type = BlueAgentActionType.RESTORE
                a = csle_cyborg_env.cyborg_action_type_and_host_to_id[(action_type, host)]
                break
