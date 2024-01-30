import numpy as np
from gym_csle_cyborg.dao.csle_cyborg_wrapper_config import CSLECyborgWrapperConfig
from gym_csle_cyborg.envs.cyborg_scenario_two_wrapper import CyborgScenarioTwoWrapper
import csle_agents.constants.constants as constants

if __name__ == '__main__':
    config = CSLECyborgWrapperConfig(maximum_steps=100, gym_env_name="", save_trace=False)
    env = CyborgScenarioTwoWrapper(config=config)

    num_episodes = 1000
    A = env.get_action_space()
    returns = []
    max_horizon = 5
    for ep in range(num_episodes):
        done = False
        o, info = env.reset()
        R = 0
        t = 0
        while t <= max_horizon:
            # a = np.random.choice(A)
            if t == 0:
                a = 31
            elif t == 1:
                a = 32
            else:
                a = 29
            o, r, done, _, info = env.step(a)
            R += r
            t += 1
        returns.append(R)

        print(f"{ep}/{num_episodes}, avg R: {np.mean(returns)}, R: {R}")

