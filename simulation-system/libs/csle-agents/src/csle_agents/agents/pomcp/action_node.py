from typing import List, Dict, Union
from csle_agents.agents.pomcp.node import Node


class ActionNode(Node):
    """
    A node in the POMCP history tree where the last element of the history was an action
    """

    def __init__(self, id: int, history: List[int], action: int, parent=None, value: float = -2000,
                 visit_count: int = 0) -> None:
        """
        Initializes the node

        :param id: the id of the node
        :param history: the history of the node
        :param action: the action of the node
        :param parent: the parent node
        :param value: the value of the node
        :param visit_count: the visit count of the node
        """
        Node.__init__(self, id=id, history=history, parent=parent, value=value, visit_count=visit_count, action=action,
                      observation=-1)
        self.mean_immediate_reward: float = 0.0
        self.observation_to_node_map: Dict[int, Node] = {}

    def update_stats(self, immediate_reward: float) -> None:
        """
        Updates the mean return from the node by computing the rolling average

        :param immediate_reward: the latest reward sample
        :return: None
        """
        self.mean_immediate_reward = (self.mean_immediate_reward * self.visit_count + immediate_reward) / \
                                     (self.visit_count + 1)

    def add_child(self, node: Node) -> None:
        """
        Adds a child node to the tree. Since an action is always followed by an observation in the history, the next
        node will be an observation/belief node

        :param node: the new child node to add
        :return: None
        """
        self.children.append(node)
        self.observation_to_node_map[node.observation] = node

    def get_child(self, key: int) -> Union[None, Node]:
        """
        Gets the child node corresponding to a specific observation

        :param key: the observation to get the node for
        :return: the child node or None if it was not found
        """
        return self.observation_to_node_map.get(key, None)
