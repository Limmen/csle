import numpy as np
from gym_csle_cyborg.envs.cyborg_model_wrapper import CyborgModelWrapper
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from csle_common.metastore.metastore_facade import MetastoreFacade

if __name__ == '__main__':
    with open(f'/home/kim/exploit_model.npy', 'rb') as f:
        exploit_success_probabilities = np.load(f)
    with open(f'/home/kim/exploit_root_model.npy', 'rb') as f:
        exploit_root_probabilities = np.load(f)
    with open(f'/home/kim/exploit_user_model.npy', 'rb') as f:
        exploit_user_probabilities = np.load(f)
    with open(f'/home/kim/activity_model.npy', 'rb') as f:
        activity_probabilities = np.load(f)
    with open(f'/home/kim/compromise_model.npy', 'rb') as f:
        compromise_probabilities = np.load(f)

    maximum_steps = 100
    env = CyborgModelWrapper(exploit_success_probabilities=exploit_success_probabilities,
                             exploit_root_probabilities=exploit_root_probabilities,
                             exploit_user_probabilities=exploit_user_probabilities,
                             activity_probabilities=activity_probabilities,
                             compromise_probabilities=compromise_probabilities, maximum_steps=maximum_steps)
    A = env.get_action_space()
    ppo_policy = MetastoreFacade.get_ppo_policy(id=98)
    episodes = 1
    for ep in range(episodes):
        print(f"{ep}/{episodes}")
        o, _ = env.reset()
        r=0
        print(f"r: {r}, s: {env.s}")
        for i in range(100):
            # a = np.random.choice(A)
            a = ppo_policy.action(o=np.array(o))
            # print(a)
            # a = 4
            o, r, done, _, info = env.step(a)
            print(info["obs_vec"])
            print(f"r: {r}, s: {env.s}")
