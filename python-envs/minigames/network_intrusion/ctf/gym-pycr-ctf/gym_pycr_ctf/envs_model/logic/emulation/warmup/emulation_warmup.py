from typing import Tuple
import numpy as np
from gym_pycr_ctf.envs_model.logic.exploration.exploration_policy import ExplorationPolicy

class EmulationWarmup:
    """
    Utility class for warming up an emulation environment by taking some actions
    """


    @staticmethod
    def warmup(exp_policy: ExplorationPolicy, num_warmup_steps: int, env, render: bool = False) \
            -> Tuple[np.ndarray, np.ndarray]:
        """
        Performs some actions in the environment according to a given exploration policy

        :param exp_policy: the exploration policy
        :param num_warmup_steps: the number of warmup steps
        :param env: the environment where to take the actions
        :param render: whether to render the environment or not
        :return: The latest observation of the environment
        """
        env.reset()
        obs = None
        for i in range(num_warmup_steps):
            if i % 10 == 0:
                print("Warmup {}%".format(float(i/num_warmup_steps)))
            attacker_action = exp_policy.action(env=env)
            defender_action = None
            action = (attacker_action, defender_action)
            obs, reward, done, info = env.step(action)

            if render:
                env.render()
            if done:
                env.reset()
        return obs