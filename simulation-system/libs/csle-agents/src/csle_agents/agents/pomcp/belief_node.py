from typing import List, Dict, Union, Any
from csle_agents.agents.pomcp.node import Node
from csle_agents.agents.pomcp.pomcp_util import POMCPUtil


class BeliefNode(Node):
    """
    Represents a node that holds the belief distribution given its history sequence in a belief tree.
    It also holds the received observation after which the belief is updated accordingly
    """

    def __init__(self, id: int, history: List[int], observation: int, parent=None, value: float = -2000,
                 visit_count: int = 0) -> None:
        """
        Initializing the node

        :param id: the id of the node
        :param h: the history of the node
        :param observation: the latest observation
        :param parent: the parent node
        :param value: the value of the node (mean return of all simulations starting from this node)
        :param visit_count: the number of times the node has been visited in simulations
        """
        Node.__init__(self, id=id, history=history, parent=parent, value=value, visit_count=visit_count,
                      observation=observation, action=-1)
        self.particles: List[int] = []
        self.action_to_node_map: Dict[int, Node] = {}

    def add_child(self, node: Node) -> None:
        """
        Adds a child node to this node. Since an observation is always followed by an action in the history, the next
        node will be an action node

        :param node: the child action node
        :return: None
        """
        self.children.append(node)
        self.action_to_node_map[node.action] = node

    def get_child(self, key: int) -> Union[Node, None]:
        """
        Gets the child node corresponding to a specific action

        :param key: the action to get the node for
        :return: the node or None if it was not found
        """
        return self.action_to_node_map.get(key, None)

    def sample_state(self) -> Any:
        """
        Samples a state from the belief state

        :return: the sampled state
        """
        return POMCPUtil.rand_choice(self.particles)

    def add_particle(self, particle: Union[int, List[int]]) -> None:
        """
        Adds a paticle (a sample state) to the list of particles

        :param particle: the particle to add
        :return: None
        """
        if type(particle) is list:
            self.particles.extend(particle)
        elif type(particle) is int:
            self.particles.append(particle)
