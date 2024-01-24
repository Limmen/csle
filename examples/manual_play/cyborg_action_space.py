from csle_common.metastore.metastore_facade import MetastoreFacade
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.dao.blue_agent_action_type import BlueAgentActionType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender

if __name__ == '__main__':
    ppo_policy = MetastoreFacade.get_ppo_policy(id=18)
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    for k, v in csle_cyborg_env.cyborg_action_id_to_type_and_host.items():
        action_id = k
        type, host = v
        print(f"{action_id}, {BlueAgentActionType(type).name}, {host}")
