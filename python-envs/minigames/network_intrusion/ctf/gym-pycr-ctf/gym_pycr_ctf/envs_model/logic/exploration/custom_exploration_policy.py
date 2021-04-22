import numpy as np
from gym_pycr_ctf.envs_model.logic.exploration.exploration_policy import ExplorationPolicy

class CustomExplorationPolicy(ExplorationPolicy):

    def __init__(self, num_actions : int, strategy):
        super(CustomExplorationPolicy, self).__init__(num_actions)
        self.strategy = strategy

    def action(self, env, filter_illegal: bool = True) -> int:
        step = env.env_state.attacker_obs_state.step
        if step < len(self.strategy):
            action = self.strategy[step]
            print("action:{}, step:{}".format(action, step))
        else:
            if filter_illegal:
                legal_actions = list(filter(lambda x: env.is_attack_action_legal(x, env.env_config, env.env_state),
                                            self.actions))
            else:
                legal_actions = self.action
            print("random action")
            action = np.random.choice(legal_actions)
        return action