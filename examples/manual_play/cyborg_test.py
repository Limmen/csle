from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender

if __name__ == '__main__':
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=False, decoy_state=False,
        scanned_state=False)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    print(f"time-step: {0}")
    print(csle_cyborg_env.get_table())
    print(csle_cyborg_env.get_true_table())
    for t in range(15):
        o, r, done, _, info = csle_cyborg_env.step(1)
        print(f"time-step: {t+1}, reward: {r}")
        print(csle_cyborg_env.get_table())
        print(info["vector_obs_per_host"])
        print(csle_cyborg_env.get_true_table())
    print(csle_cyborg_env.get_actions_table())
