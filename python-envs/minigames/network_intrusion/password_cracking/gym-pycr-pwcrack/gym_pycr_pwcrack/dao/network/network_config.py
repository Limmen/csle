from typing import List, Union
from gym_pycr_pwcrack.dao.network.node import Node
from gym_pycr_pwcrack.dao.network.node_type import NodeType
import numpy as np

class NetworkConfig:

    def __init__(self, subnet_mask: str, nodes: List[Node], adj_matrix: np.ndarray, flags_lookup: dict,
                 agent_reachable: set):
        self.subnet_mask = subnet_mask
        self.nodes = nodes
        self.adj_matrix = adj_matrix
        node_d, hacker, router, levels_d = self.create_lookup_dicts()
        self.node_d = node_d
        self.hacker = hacker
        self.router = router
        self.levels_d = levels_d
        self.flags_lookup = flags_lookup
        self.agent_reachable = agent_reachable

    def __str__(self):
        return "subnet_mask:{}, nodes:{}, adj_matrix:{}, hacker:{}, router: {}, flags_lookup: {}, agent_reachable: {}".format(
            self.subnet_mask, list(map(lambda x: str(x), self.nodes)), self.adj_matrix, self.hacker, self.router, self.flags_lookup,
            self.agent_reachable)

    def create_lookup_dicts(self) -> Union[dict, Node, Node, dict]:
        levels_d = {}
        node_d = {}
        hacker = None
        router = None
        for node in self.nodes:
            node_d[node.id] = node
            if node.type == NodeType.HACKER:
                if hacker is not None:
                    raise ValueError("Invalid Network Config: 2 Hackers")
                hacker = node
            elif node.type == NodeType.ROUTER:
                if router is not None:
                    raise ValueError("Invalid Network Config: 2 Routers")
                router = node
            if node.level in levels_d:
                levels_d[node.level].append(node)
                #levels_d[node.level] = n_level
            else:
                levels_d[node.level] = [node]

        return node_d, hacker, router, levels_d


    def copy(self):
        return NetworkConfig(
            subnet_mask=self.subnet_mask, nodes=self.nodes, adj_matrix=self.adj_matrix, flags_lookup=self.flags_lookup,
            agent_reachable=self.agent_reachable)