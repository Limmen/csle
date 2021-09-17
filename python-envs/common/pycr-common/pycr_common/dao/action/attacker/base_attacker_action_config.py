from abc import ABC


class BaseAttackerActionConfig(ABC):
    """
    Abstract base class that represent attaction action configurations in PyCR
    """

    def __init__(self, num_actions : int):
        """
        Constructor for initializing the attacker configuration

        :param num_actions: the number of actions
        """
        self.num_actions = num_actions