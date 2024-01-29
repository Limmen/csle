import numpy as np
import torch
import random
from csle_common.metastore.metastore_facade import MetastoreFacade
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil
import gym_csle_cyborg.constants.constants as env_constants
from gym_csle_cyborg.dao.blue_agent_action_type import BlueAgentActionType

if __name__ == '__main__':
    ppo_policy = MetastoreFacade.get_ppo_policy(id=58)
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False, cache_visited_states=False)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    num_evaluations = 1000
    max_horizon = 100
    returns = []
    seed = 346277
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    A = csle_cyborg_env.get_action_space()
    print("Starting policy evaluation")
    for i in range(num_evaluations):
        done = False
        o, _ = csle_cyborg_env.reset()
        R = 0
        t = 0
        while t < max_horizon:
            # a = np.random.choice(A)
            # a = 31
            # a = 27
            # if t > 20:
            #     a = 3
            # a = 4
            a = ppo_policy.action(o=o)
            # a = 27
            # if t == 0:
            #     a = 31
            # if t == 1:
            #     a = 30
            # if a == 34:
            #     import random
            #     a = random.choice([27, 28, 29])
            o, r, done, _, info = csle_cyborg_env.step(a)
            # state_id = info[env_constants.ENV_METRICS.STATE]
            # oid = info[env_constants.ENV_METRICS.OBSERVATION]
            # s = CyborgEnvUtil.state_id_to_state_vector(state_id=state_id)
            # obs = CyborgEnvUtil.state_id_to_state_vector(state_id=oid, observation=True)
            # print(f"t: {t}, r: {r}, a: {a}, {csle_cyborg_env.get_last_action(agent='Red')}")
            # print(s)
            # print(obs)
            # print(o)
            # if t == 0:
            #     print(o)
            #     print(type(o))
            #     print(list(o.tolist()).index(1))

            # print(f"t: {t}, r: {r}, a: {a}, s: {s}")
            # print(f"a: {csle_cyborg_env.action_id_to_type_and_host[a]}")
            # print(csle_cyborg_env.get_true_table())
            R += r
            t += 1
        returns.append(R)
        print(f"{i}/{num_evaluations}, avg R: {np.mean(returns)}, R: {R}")
