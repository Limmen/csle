import numpy as np
from gym_pycr_pwcrack.envs.logic.exploration.exploration_policy import ExplorationPolicy

class RandomExplorationPolicy(ExplorationPolicy):

    def __init__(self, num_actions : int):
        super(RandomExplorationPolicy, self).__init__(num_actions)

    def action(self, env) -> int:
        legal_actions = list(filter(lambda x: env.is_action_legal(x, env.env_config, env.env_state), self.actions))
        action = np.random.choice(legal_actions)
        return action