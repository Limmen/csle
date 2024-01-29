from typing import List, Union, Any, Dict
from csle_agents.agents.pomcp.node import Node
from csle_agents.agents.pomcp.action_node import ActionNode
from csle_agents.agents.pomcp.belief_node import BeliefNode


class BeliefTree:
    """
    The belief tree of POMCP. Each node in the tree corresponds to a history of the POMDP, where a history is a sequence
    of actions and observations.
    """

    def __init__(self, root_particles: List[int], default_node_value: float, root_observation: int,
                 initial_visit_count: int = 0) -> None:
        """
        Initializes the tree with a belief node with a set of particles

        :param root_particles: the particles to add to the root belief node
        :param default_node_value: the default value of nodes in the tree
        :param root_observation: the root observation
        :param initial_visit_count: the initial visit count
        :return: None
        """
        self.tree_size = 0
        self.root_observation = root_observation
        self.nodes: Dict[int, Union[Node, None]] = {}
        self.default_node_value = default_node_value
        self.initial_visit_count = initial_visit_count
        node: Node = self.add(history=[root_observation], particle=root_particles, parent=None,
                              value=default_node_value)
        if isinstance(node, BeliefNode):
            self.root: BeliefNode = node
        else:
            raise ValueError("Invalid root node")

    def add(self, history: List[int], parent: Union[Node, ActionNode, BeliefNode, None],
            action: Union[int, None] = None, observation: Union[int, None] = None, particle: Union[Any, None] = None,
            value: float = 0, initial_visit_count: int = 0) -> Node:
        """
        Creates and adds a new belief node or action node to the belief search tree

        :param h: history sequence
        :param parent: either ActionNode or BeliefNode
        :param action: action
        :param observation: observation
        :param particle: new node's particle set
        :param cost: action cost of an action node
        :param value: the value of the node
        :param initial_visit_count: the initial visit count
        :return: The newly added node
        """
        # Create the node
        if action is not None:
            new_node: Node = ActionNode(self.tree_size, history, parent=parent, action=action, value=value,
                                        visit_count=initial_visit_count)
        else:
            if observation is None:
                observation = 0
            new_node = BeliefNode(self.tree_size, history, parent=parent, observation=observation, value=value,
                                  visit_count=initial_visit_count)

        if particle is not None and isinstance(new_node, BeliefNode):
            new_node.add_particle(particle)

        # add the node to belief tree
        self.nodes[new_node.id] = new_node
        self.tree_size += 1

        # register node as parent's child
        if parent is not None:
            parent.add_child(node=new_node)
        return new_node

    def find_or_create(self, history: List[int], parent: Union[None, BeliefNode, ActionNode], observation: int,
                       initial_value: float, initial_visit_count: int) -> Node:
        """
        Search for the node that corresponds to given history, otherwise create one using given params

        :param history: the current history
        :param parent: the parent of the node
        :param observation: the latest observation
        :param initial_value: the initial value of a created node
        :param initial_visit_count: the initial visit count of a created node
        :return: the new node
        """
        # Start the search from the root node
        root_node = self.root
        current_node: Union[None, Node] = root_node

        # Start from the root node and then traverse down to the depth of the given history to see if the node
        # of this history  exists or not, otherwise add it
        history_length, root_history_length = len(history), len(self.root.history)
        for step in range(root_history_length, history_length):
            if current_node is not None:
                current_node = current_node.get_child(history[step])

            # Node of this history does not exists so we add it
            if current_node is None:
                return self.add(history=history, parent=parent, observation=observation, value=initial_value,
                                initial_visit_count=initial_visit_count)
        if current_node is None:
            raise ValueError("Could not create a new node")
        return current_node

    def prune(self, node, exclude=None):
        """
        Removes the entire subtree subscribed to 'node' with exceptions.
        :param node: root of the subtree to be removed
        :param exclude: exception component
        :return:
        """
        for child in node.children:
            if exclude and exclude.id != child.id:
                self.prune(child, exclude)

        self.nodes[node.id] = None
        del self.nodes[node.id]
