import numpy as np
from pycr_common.envs_model.logic.exploration.exploration_policy import ExplorationPolicy


class RandomExplorationPolicy(ExplorationPolicy):

    def __init__(self, num_actions : int):
        super(RandomExplorationPolicy, self).__init__(num_actions)

    def action(self, env, filter_illegal: bool = True) -> int:
        if filter_illegal:
            legal_actions = list(filter(lambda x: env.is_attack_action_legal(x, env.env_config, env.env_state),
                                        self.actions))
        else:
            legal_actions = self.actions
        if len(legal_actions) == 0:
            print("no legal actions, idx:{}".format(env.idx))
        action = np.random.choice(legal_actions)
        return action