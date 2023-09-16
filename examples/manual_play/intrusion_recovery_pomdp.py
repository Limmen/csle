import gymnasium as gym
import numpy as np
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_tolerance.util.general_util import GeneralUtil

if __name__ == '__main__':
    GeneralUtil.register_envs()
    simulation_name = "csle-tolerance-intrusion-recovery-pomdp-defender-001"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    env = gym.make("csle-tolerance-intrusion-recovery-pomdp-v1",
                   config=simulation_env_config.simulation_env_input_config)

    threshold = 0.5
    costs = []
    for i in range(100):
        cumulative_cost = 0
        s, _ = env.reset()
        done = False
        t = 0
        while not done:
            b = s[2]
            a = 0
            if b >= threshold:
                a = 1
            s, c, _, done, info = env.step(a)
            cumulative_cost += c
            t+= 1
        costs.append(cumulative_cost)
    print(float(np.mean(costs)))

    # env.manual_play()
