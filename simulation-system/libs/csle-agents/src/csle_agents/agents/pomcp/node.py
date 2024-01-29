from typing import List, Union
from abc import abstractmethod


class Node:
    """
    Abstract node type, represents a node in the lookahead tree
    """

    def __init__(self, id: int, history: List[int], parent=None, value: float = -2000, visit_count: int = 0,
                 observation: int = -1, action: int = -1) -> None:
        """
        Initializes the node

        :param id: the id of the node
        :param history: the history of the node
        :param parent: the parent node
        :param V: the value of the node
        :param visit_count: the visit count of the node
        :param observation: the observation of the node
        :param action: the action of the node
        """
        self.history = history
        self.value = value
        self.visit_count = visit_count
        self.id = id
        self.parent = parent
        self.children: List["Node"] = []
        self.observation = observation
        self.action = action

    @abstractmethod
    def add_child(self, node: "Node") -> None:
        """
        Method that adds a child to the node. Should be implemented by classes that inherit from this class

        :param node: the node to add
        :return: None
        """
        pass

    @abstractmethod
    def get_child(self, key: int) -> Union["Node", None]:
        """
        Method that gets the child to the node. Should be implemented by classes that inherit from this class

        :param key: the key to identify the child
        :return: the child
        """
        pass
