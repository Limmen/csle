from csle_attack_profiler.dao.tactics import Tactics
from typing import List, Tuple, Union

ChildNode = Tuple[Tactics, int]
Node = Tuple[Tactics, List[ChildNode], int]


class AttackGraph:
    """
    Class representing the attack graph
    """

    def __init__(self) -> None:
        """
        Class constructor

        The graph is represented as a list of tuples. Each tuple contains the node name,
        the children of the node and the node id.
        """
        self.graph: List[Node] = []

    def add_node(self, node_name: Tactics, children: Union[List[ChildNode], None] = None,
                 node_id: Union[int, None] = None) -> None:
        """
        Add a node to the graph

        :params node_name: the name of the node
        :params children: the children of the node
        :params node_id: the id of the node
        :return: None
        """
        # We need to distinguish between nodes with an id
        # Every time we add a node, we increment the id by 1 if node_id is None
        if node_id is None:
            node_id = len(self.graph) + 1
        if children is None:
            children = []
        self.graph.append((node_name, children, node_id))

    def add_edge(self, parent_node_name: Tactics, parent_node_id: int,
                 child_node_name: Tactics, child_node_id: int) -> None:
        """
        Add an edge to the graph by defining the parent node and the children

        :params node_name: the name of the node
        :params children: the children of the node
        :return: None
        """
        for i, (node_name, children, node_id) in enumerate(self.graph):
            if node_name == parent_node_name and node_id == parent_node_id:

                if any(child[0] == child_node_name for child in children):
                    raise RuntimeError("Child node already exists in the parent node")
                else:
                    self.graph[i][1].append((child_node_name, child_node_id))

                break

    def get_node(self, node_name: Tactics, node_id: int) -> Union[None, Node]:
        """
        Get the node from the graph

        :params node_name: the name of the node

        :return: the node
        """
        for node in self.graph:
            if node_name == node[0] and node[2] == node_id:
                return node
        return None
    
    def get_root_node(self) -> Node:
        """
        Get the root node of the graph

        :return: the root node of the graph
        """
        return self.graph[0]
    
    def get_children(self, node_name: Tactics, node_id: int) -> Union[None, List[ChildNode]]:
        """
        Get the children of the node

        :params node_name: the name of the node
        :params node_id: the id of the node

        :return: the children of the node
        """
        for node in self.graph:
            if node_name == node[0] and node[2] == node_id:
                return node[1]
        return None
