from abc import ABC


class BaseDefenderActionConfig(ABC):

    def __init__(self, num_actions : int):
        self.num_actions = num_actions