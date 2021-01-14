from typing import List, Union
from gym_pycr_pwcrack.dao.network.node import Node
from gym_pycr_pwcrack.dao.network.node_type import NodeType
import numpy as np

class NetworkConfig:

    def __init__(self, subnet_mask: str, nodes: List[Node], adj_matrix: np.ndarray, flags_lookup: dict,
                 agent_reachable: set, vulnerable_nodes = None):
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
        self.vulnerable_nodes = vulnerable_nodes

    def __str__(self):
        return "subnet_mask:{}, nodes:{}, adj_matrix:{}, hacker:{}, router: {}, flags_lookup: {}, agent_reachable: {}, " \
               "vulnerable_nodes: {}:".format(
            self.subnet_mask, list(map(lambda x: str(x), self.nodes)), self.adj_matrix, self.hacker, self.router, self.flags_lookup,
            self.agent_reachable, self.vulnerable_nodes)

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

    def optimal_reward(self, flag_found_reward_mult : int, port_found_reward_mult : int, os_found_reward_mult: int,
                       cve_vuln_found_reward_mult: int, machine_found_reward_mult: int, shell_access_found_reward_mult: int,
                       root_found_reward_mult: int, osvdb_vuln_found_reward_mult: int, new_login_reward_mult : int,
                       new_tools_installed_reward_mult: int, new_backdoors_installed_reward_mult : int
                       ):
        reward = len(self.flags_lookup)*flag_found_reward_mult


    def shortest_paths(self):
        shortest_paths = self._find_nodes(reachable=self.agent_reachable, path=[], flags=[])
        return shortest_paths
        # print(shortest_paths)
        # print("num paths:{}".format(len(shortest_paths)))
        # print(set(list(map(lambda x: x[0][0], shortest_paths))))
        # print(len(set(list(map(lambda x: ",".join(x[0]), shortest_paths)))))

    def _find_nodes(self, reachable, path, flags):
        paths = []
        min_path_len = len(self.nodes)
        for n in self.nodes:
            l_reachable = reachable.copy()
            l_path = path.copy()
            l_flags = flags.copy()
            if n.ip in l_reachable and n.ip in self.vulnerable_nodes and n.ip not in l_path:
                l_reachable.update(n.reachable_nodes)
                l_path.append(n.ip)
                l_flags = l_flags + n.flags
                if len(l_flags)== len(self.flags_lookup):
                    paths.append((l_path, l_flags.copy()))
                    if len(l_path) < min_path_len:
                        min_path_len = len(l_path)
                elif len(l_path) < min_path_len:
                    paths = paths + self._find_nodes(l_reachable, l_path, l_flags)
        return paths

