from abc import ABC, abstractmethod
import numpy as np


class ExplorationPolicy(ABC):
    """
    Abstract exploration policy to explor an environment
    """

    def __init__(self, num_actions : int):
        """
        Class constructor

        :param num_actions: number of actions in the environment
        """
        self.num_actions = num_actions
        self.actions = np.array(list(range(num_actions)))

    @abstractmethod
    def action(self, env, filter_illegal: bool = True) -> int:
        """
        Abstract method for sampling an action to take in the environment using the exploration policy.
        Should be implemented by sub-classes

        :param env: the environment to take the action
        :param filter_illegal: boolean flag whether to filter illegal actions or not
        :return: the action to take
        """
        pass