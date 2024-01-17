from typing import List, Union, Any
from csle_agents.agents.pomcp.action_node import ActionNode
from csle_agents.agents.pomcp.belief_node import BeliefNode


class BeliefTree:
    """
    The belief tree of POMCP. Each node in the tree corresponds to a history of the POMDP, where a history is a sequence
    of actions and observations.
    """

    def __init__(self, root_particles: List[int]) -> None:
        """
        Initializes the tree with a belief node with a set of particles

        :param root_particles: the particles to add to the root belief node
        """
        self.tree_size = 0
        self.nodes = {}
        self.root = self.add(history=[], particle=root_particles, parent=None)

    def add(self, history: List[int], parent: Union[ActionNode, BeliefNode, None], action: Union[int, None] = None,
            observation: Union[int, None] = None, particle: Union[Any, None] = None):
        """
        Creates and adds a new belief node or action node to the belief search tree

        :param h: history sequence
        :param parent: either ActionNode or BeliefNode
        :param action: action
        :param observation: observation
        :param particle: new node's particle set
        :param cost: action cost of an action node
        :return:
        """
        # Create the node
        if action is not None:
            new_node = ActionNode(self.tree_size, history, parent=parent, action=action)
        else:
            new_node = BeliefNode(self.tree_size, history, parent=parent, observation=observation)

        if particle is not None:
            new_node.add_particle(particle)

        # add the node to belief tree
        self.nodes[new_node.id] = new_node
        self.tree_size += 1

        # register node as parent's child
        if parent is not None:
            parent.add_child(node=new_node)
        return new_node

    def find_or_create(self, history: List[int], parent: Union[None, BeliefNode, ActionNode], observation: int):
        """
        Search for the node corresponds to given history, otherwise create one using given params
        """
        # Start the search from the root node
        current_node = self.root

        # Start from the root node and then traverse down to the depth of the given history to see if the node
        # of this history  exists or not, otherwise add it
        history_length, root_history_length = len(history), len(self.root.history)
        for step in range(root_history_length, history_length):
            current_node = current_node.get_child(history[step])

            # Node of this history does not exists so we add it
            if current_node is None:
                return self.add(history=history, parent=parent, observation=observation)
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
