from abc import ABC, abstractmethod
import numpy as np

class ExplorationPolicy(ABC):

    def __init__(self, num_actions : int):
        self.num_actions = num_actions
        self.actions = np.array(list(range(num_actions)))

    @abstractmethod
    def action(self, env, filter_illegal: bool = True) -> int:
        pass