from typing import List
from abc import abstractmethod


class Node:
    """
    Abstract node type, represents a node in the lookahead tree
    """

    def __init__(self, id: int, history: List[int], parent=None, value: float = 0, visit_count: int = 0) -> None:
        """
        Initializes the node

        :param id: the id of the node
        :param history: the history of the node
        :param parent: the parent node
        :param V: the value of the node
        :param visit_count: the visit count of the node
        """
        self.history = history
        self.value = value
        self.visit_count = visit_count
        self.id = id
        self.parent = parent
        self.children = []

    @abstractmethod
    def add_child(self, node: "Node") -> None:
        """
        Method that adds a child to the node. Should be implemented by classes that inherit from this class

        :param node: the node to add
        :return: None
        """
        pass

    @abstractmethod
    def get_child(self, *args) -> "Node":
        """
        Method that gets the child to the node. Should be implemented by classes that inherit from this class

        :param args: list of arguments to specify the child
        :return: the child
        """
        pass
