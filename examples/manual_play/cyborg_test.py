from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender

if __name__ == '__main__':
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=False, decoy_state=False,
        scanned_state=False)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    print(csle_cyborg_env.cyborg_action_id_to_type_and_host[44])
    print(csle_cyborg_env.cyborg_action_id_to_type_and_host[107])
    print(csle_cyborg_env.cyborg_action_id_to_type_and_host[104])
    print(csle_cyborg_env.cyborg_action_id_to_type_and_host[126])
    print(csle_cyborg_env.cyborg_action_id_to_type_and_host[120])
    print(csle_cyborg_env.cyborg_action_id_to_type_and_host[50])
    print(csle_cyborg_env.cyborg_action_id_to_type_and_host[57])
    print(csle_cyborg_env.cyborg_action_id_to_type_and_host[2])
    print(csle_cyborg_env.cyborg_action_id_to_type_and_host[23])
    print(csle_cyborg_env.cyborg_action_id_to_type_and_host[6])
    print(csle_cyborg_env.cyborg_action_id_to_type_and_host[133])
