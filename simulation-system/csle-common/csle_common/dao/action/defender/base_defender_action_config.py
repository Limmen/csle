from abc import ABC


class BaseDefenderActionConfig(ABC):
    """
    Abstract base class that represent a defender action configuration in csle
    """

    def __init__(self, num_actions : int):
        """
        Class constructor for initializing the defender action configuration

        :param num_actions: the number of actions
        """
        self.num_actions = num_actions