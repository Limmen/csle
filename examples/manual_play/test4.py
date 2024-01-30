import numpy as np
import math
import torch
import random
from gym_csle_cyborg.dao.csle_cyborg_wrapper_config import CSLECyborgWrapperConfig
from gym_csle_cyborg.envs.cyborg_scenario_two_wrapper import CyborgScenarioTwoWrapper
import csle_agents.constants.constants as constants
from csle_common.metastore.metastore_facade import MetastoreFacade

def rollout(rollout_a: int, env, s, num_rollouts = 100, max_horizon: int = 5, base_t: int = 0):
    returns = []
    for ep in range(num_rollouts):
        o, info = env.reset()
        R = 0
        t = 0
        # if base_t == 1 or base_t == 2 or base_t == 3:
        #     print(f"Setting state: {s}")
        env.set_state(s)
        while t <= max_horizon:
            if t == 0:
                a = rollout_a
            else:
                a = 29
            o, r, done, _, info = env.step(a)
            R += r
            t += 1
        returns.append(R)
    return np.mean(returns)

if __name__ == '__main__':
    config = CSLECyborgWrapperConfig(maximum_steps=100, gym_env_name="", save_trace=False, reward_shaping=True)
    env = CyborgScenarioTwoWrapper(config=config)
    eval_config = CSLECyborgWrapperConfig(maximum_steps=100, gym_env_name="", save_trace=False, reward_shaping=False)
    eval_env = CyborgScenarioTwoWrapper(config=eval_config)
    rollout_policy = MetastoreFacade.get_ppo_policy(id=58)
    rollout_policy.save_path = "/Users/kim/workspace/csle/examples/training/pomcp/cyborg_scenario_two_wrapper/ppo_test_1706439955.8221297/ppo_model2900_1706522984.6982665.zip"
    rollout_policy.load()

    num_episodes = 100
    A = env.get_action_space()
    returns = []
    max_horizon = 4
    num_rollouts = 100
    seed = 98171
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    for ep in range(num_episodes):
        done = False
        env.reset()
        o, info = eval_env.reset()
        R = 0
        t = 0
        s = info[constants.COMMON.STATE]
        while t <= 100:
            # dist = rollout_policy.model.policy.get_distribution(
            #     obs=torch.tensor([o]).to(rollout_policy.model.device)).log_prob(
            #     torch.tensor(A).to(rollout_policy.model.device)).cpu().detach().numpy()
            # dist = list(map(lambda i: (math.exp(dist[i]), A[i]), list(range(len(dist)))))
            # rollout_actions = list(map(lambda x: x[1], sorted(dist, reverse=True, key=lambda x: x[0])[:5]))
            rollout_actions = A
            # print(rollout_actions)
            # if t >= 2:
            #     print("longer horizon")
            #     max_horizon = 20
            # if t == 1:
            #     A = [0]
            a_values = []
            for a in rollout_actions:
                a_values.append(rollout(rollout_a=a, env=env, s=s, num_rollouts=num_rollouts, max_horizon=max_horizon,
                                        base_t=t))
            # print(a_values)
            best_a = np.argmax(a_values)
            print(f"t: {t}, best a: {rollout_actions[best_a]}, val: {a_values[best_a]}, R:{R}, \ns: {s[0]}")
            a = rollout_actions[best_a]
            # a = np.random.choice(A)
            # if t == 0:
            #     a = 31
            # elif t == 1:
            #     a = 32
            # else:
            #     a = 29
            env.set_state(s)
            o, r, done, _, info = eval_env.step(a)
            s = info[constants.COMMON.STATE]
            R += r
            t += 1
        returns.append(R)
        print(f"{ep}/{num_episodes}, avg R: {np.mean(returns)}, R: {R}")

