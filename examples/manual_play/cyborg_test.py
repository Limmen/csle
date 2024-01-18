import random
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil

if __name__ == '__main__':
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    str_info = str(csle_cyborg_env.cyborg_challenge_env.env.env.env.info)
    states = {}
    state_idx = 0
    host_ids = list(csle_cyborg_env.cyborg_hostname_to_id.values())

    for i in range(100000):
        done = False
        csle_cyborg_env.reset()
        actions = list(csle_cyborg_env.action_id_to_type_and_host.keys())
        state_id = str(csle_cyborg_env.cyborg_challenge_env.env.env.env.info)
        if state_id not in states:
            states[state_id] = state_idx
            state_idx += 1

        while not done:
            a = random.choice(actions)
            o, r, done, _, info = csle_cyborg_env.step(a)
            state_vector = CyborgEnvUtil.state_to_vector(state=csle_cyborg_env.get_true_table().rows,
                                                         decoy_state=csle_cyborg_env.decoy_state, host_ids=host_ids,
                                                         scan_state=csle_cyborg_env.scan_state)
            state_id = CyborgEnvUtil.state_vector_to_state_id(state_vector=state_vector)
            converted_state_vector = CyborgEnvUtil.state_id_to_state_vector(state_id=state_id)
            assert converted_state_vector == state_vector
            obs_vector = CyborgEnvUtil.state_to_vector(state=csle_cyborg_env.get_table().rows,
                                                       decoy_state=csle_cyborg_env.decoy_state,
                                                       host_ids=host_ids, scan_state=csle_cyborg_env.scan_state,
                                                       observation=True)
            obs_id = CyborgEnvUtil.state_vector_to_state_id(state_vector=obs_vector, observation=True)
            converted_obs_vector = CyborgEnvUtil.state_id_to_state_vector(state_id=obs_id, observation=True)
            assert converted_obs_vector == obs_vector
