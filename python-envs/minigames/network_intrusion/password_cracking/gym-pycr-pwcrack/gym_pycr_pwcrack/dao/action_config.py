from typing import List
import gym
from gym_pycr_pwcrack.dao.action import Action

class ActionConfig:

    def __init__(self, actions: List[Action]):
        self.actions = actions
        self.num_actions = len(self.actions)
        self.action_space = gym.spaces.Discrete(self.num_actions)
        self.action_lookup_d = {}
        for action in actions:
            self.action_lookup_d[action.id] = action