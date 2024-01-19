from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender
import gym_csle_cyborg.constants.constants as env_constants

if __name__ == '__main__':
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    o, info = csle_cyborg_env.reset()
    initial_state_id = info[env_constants.ENV_METRICS.STATE]
    o, r, done, _, info = csle_cyborg_env.step(1)
    # csle_cyborg_env.get_table()
    obs = info[env_constants.ENV_METRICS.OBSERVATION]
    # print("FIRST OBS:")
    # print(csle_cyborg_env.get_observation_from_id(obs_id=obs))
    csle_cyborg_env.set_state(state=initial_state_id)
    # print(csle_cyborg_env.cyborg_challenge_env.env.env.env.env.env.environment_controller.observation["Red"].data["User0"])
    csle_cyborg_env.step(1)
    csle_cyborg_env.get_table()

    # print("INITIAL2 STATE")
    # print(csle_cyborg_env.get_true_table())
    # # csle_cyborg_env.get_true_table()
    # o, r, done, _, info = csle_cyborg_env.step(1)
    # print("INITIAL1 STATE")
    # print(csle_cyborg_env.get_true_table())
    # initial_obs_id = info[env_constants.ENV_METRICS.OBSERVATION]
    # initial_state_id = info[env_constants.ENV_METRICS.STATE]
    # # csle_cyborg_env.set_state(state=initial_state_id)
    # csle_cyborg_env.step(1)
    # print("SECOND STATE")
    # print(csle_cyborg_env.get_true_table())
    # csle_cyborg_env.step(1)
    # csle_cyborg_env.step(1)
    # csle_cyborg_env.step(1)
    # csle_cyborg_env.step(1)
    # csle_cyborg_env.step(1)
    # csle_cyborg_env.step(1)
    # print(csle_cyborg_env.get_true_table())
    # print("SET STATE")
    # csle_cyborg_env.set_state(state=initial_state_id)
    # print(csle_cyborg_env.get_true_table())
    # csle_cyborg_env.step(1)
    # print(csle_cyborg_env.get_true_table())
    # csle_cyborg_env.step(1)
    # print(csle_cyborg_env.get_true_table())
    # csle_cyborg_env.step(1)
    # print(csle_cyborg_env.get_true_table())
    # csle_cyborg_env.step(1)
    # csle_cyborg_env.step(1)
    # csle_cyborg_env.step(1)
    # csle_cyborg_env.step(1)
    # print(csle_cyborg_env.get_true_table())
