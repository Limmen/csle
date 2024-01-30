import numpy as np
from gym_csle_cyborg.dao.csle_cyborg_wrapper_config import CSLECyborgWrapperConfig
from gym_csle_cyborg.envs.cyborg_scenario_two_wrapper import CyborgScenarioTwoWrapper
import csle_agents.constants.constants as constants

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
    config = CSLECyborgWrapperConfig(maximum_steps=100, gym_env_name="", save_trace=False)
    env = CyborgScenarioTwoWrapper(config=config)

    num_episodes = 1
    A = env.get_action_space()
    returns = []
    max_horizon = 3
    num_rollouts = 1000
    for ep in range(num_episodes):
        done = False
        o, info = env.reset()
        R = 0
        t = 0
        s = info[constants.COMMON.STATE]
        while t <= 100:
            if t >= 2:
                print("longer horizon")
                max_horizon = 20
            # if t == 1:
            #     A = [0]
            a_values = []
            for a in A:
                a_values.append(rollout(rollout_a=a, env=env, s=s, num_rollouts=num_rollouts, max_horizon=max_horizon,
                                        base_t=t))
            print(a_values)
            best_a = np.argmax(a_values)
            print(f"best a: {best_a}, val: {a_values[best_a]}, , 31 val: {a_values[31]}, \ns: {s[0]}")
            a = best_a
            # a = np.random.choice(A)
            # if t == 0:
            #     a = 31
            # elif t == 1:
            #     a = 32
            # else:
            #     a = 29
            env.set_state(s)
            o, r, done, _, info = env.step(a)
            s = info[constants.COMMON.STATE]
            R += r
            t += 1
        returns.append(R)

        print(f"{ep}/{num_episodes}, avg R: {np.mean(returns)}, R: {R}")

