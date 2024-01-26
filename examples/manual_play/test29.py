import json
import numpy as np
import io
from gym_csle_cyborg.envs.cyborg_model_wrapper import CyborgModelWrapper
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
import csle_agents.constants.constants as agents_constants

if __name__ == '__main__':
    # with io.open(f"/home/kim/particle_model.json", 'r', encoding='utf-8') as f:
    #     json_str = f.read()
    #     temp = json.loads(json_str)
    # particle_model = {}
    # for k, v in temp.items():
    #     v_2 = [int(x) for x in v]
    #     particle_model[int(k)] = v_2


    with io.open(f"/home/kim/observation_model.json", 'r', encoding='utf-8') as f:
        json_str = f.read()
        temp = json.loads(json_str)
    observation_model = {}
    for k, v in temp.items():
        v_2 = [int(x) for x in v]
        observation_model[int(k)] = v_2
    print("loaded observation model")


    with io.open(f"/home/kim/new_transition_model.json", 'r', encoding='utf-8') as f:
        json_str = f.read()
        temp = json.loads(json_str)
    print("loaded model, converting to int")
    transition_model = {}
    for k, v in temp.items():
        transition_model[int(k)] = {}
        for k2, v2 in v.items():
            v_2 = [int(x) for x in v2]
            transition_model[int(k)][int(k2)] = v_2

    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False, cache_visited_states=False)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    _, info = csle_cyborg_env.reset()
    s = info[agents_constants.COMMON.STATE]
    o = info[agents_constants.COMMON.OBSERVATION]
    observation_model[s] = [o]
    env = CyborgModelWrapper(transition_model=transition_model, observation_model=observation_model, initial_state=s,
                             action_id_to_type_and_host=csle_cyborg_env.action_id_to_type_and_host)
    # print(transition_model)
    # print(list(transition_model[s].keys()))
    A = csle_cyborg_env.get_action_space()
    episodes = 1000
    for ep in range(episodes):
        print(f"{ep}/{episodes}")
        env.reset()
        for i in range(100):
            a = np.random.choice(A)
            o, r, done, _, info = env.step(a)
            print(f"{o}: {o}, r: {r}")
