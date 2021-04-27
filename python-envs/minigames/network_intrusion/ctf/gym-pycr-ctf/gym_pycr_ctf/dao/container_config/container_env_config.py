from typing import List, Tuple, Set


class ContainerEnvConfig:
    """
    A DTO representing the configuration of a dynamically created emulation environment
    """

    def __init__(self, min_num_users: int = 1, max_num_users : int = 5, min_num_flags : int = 1,
                 max_num_flags : int = 5, min_num_nodes : int = 4, max_num_nodes : int = 10,
                 container_pool: List[Tuple[str, str]] = None,
                 gw_vuln_compatible_containers : List[Tuple[str, str]] = None,
                 pw_vuln_compatible_containers : List[Tuple[str, str]] = None,
                 rce_vuln_compatible_containers: List[Tuple[str, str]] = None,
                 sql_injection_vuln_compatible_containers: List[Tuple[str, str]] = None,
                 priv_esc_vuln_compatible_containers: List[Tuple[str, str]] = None,
                 agent_containers : List[Tuple[str, str]] = None,
                 router_containers : List[Tuple[str, str]] = None,
                 path : str = "", subnet_id_blacklist : Set = None,
                 subnet_prefix: str = "", subnet_id :int = -1, num_flags :int = -1, num_nodes : int = -1
                 ):
        self.min_num_users = min_num_users
        self.max_num_users = max_num_users
        self.min_num_flags = min_num_flags
        self.max_num_flags = max_num_flags
        self.min_num_nodes = min_num_nodes
        self.max_num_nodes = max_num_nodes
        self.container_pool = container_pool
        self.gw_vuln_compatible_containers = gw_vuln_compatible_containers
        self.pw_vuln_compatible_containers = pw_vuln_compatible_containers
        self.rce_vuln_compatible_containers = rce_vuln_compatible_containers
        self.sql_injection_vuln_compatible_containers = sql_injection_vuln_compatible_containers
        self.priv_esc_vuln_compatible_containers = priv_esc_vuln_compatible_containers
        self.agent_containers = agent_containers
        self.router_containers = router_containers
        self.path = path
        self.subnet_id_blacklist = subnet_id_blacklist
        self.subnet_prefix = subnet_prefix
        self.subnet_id = subnet_id
        self.num_flags = num_flags
        self.num_nodes = num_nodes

        if self.container_pool is None:
            self.container_pool = []
        if self.gw_vuln_compatible_containers is None:
            self.gw_vuln_compatible_containers = []
        if self.pw_vuln_compatible_containers is None:
            self.pw_vuln_compatible_containers = []
        if self.rce_vuln_compatible_containers is None:
            self.rce_vuln_compatible_containers = []
        if self.sql_injection_vuln_compatible_containers is None:
            self.sql_injection_vuln_compatible_containers = []
        if self.priv_esc_vuln_compatible_containers is None:
            self.priv_esc_vuln_compatible_containers = []
        if self.agent_containers is None:
            self.agent_containers = []
        if self.router_containers is None:
            self.router_containers = []
        if self.subnet_id_blacklist is None:
            self.subnet_id_blacklist = set()

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "min_num_users:{}, max_num_users:{}, min_num_flags:{}, max_num_flags:{}," \
               "min_num_nodes:{}, max_num_nodes:{}, container_pool:{}, gw_vuln_compatible_containers:{}," \
               "pw_vuln_compatible_containers:{}, rce_vuln_compatible_containers:{}, " \
               "sql_injection_vuln_compatible_containers:{}, priv_esc_vuln_compatible_containers:{}" \
               "agent_containers:{},router_containers:{},path:{}," \
               "subnet_id_blacklist:{}, subnet_prefix:{}, subnet_id:{}, num_flags:{}, num_nodes:{}".format(
            self.min_num_users, self.max_num_users, self.min_num_flags, self.max_num_flags, self.min_num_nodes,
            self.max_num_nodes, self.container_pool, self.gw_vuln_compatible_containers,
            self.pw_vuln_compatible_containers, self.rce_vuln_compatible_containers,
            self.sql_injection_vuln_compatible_containers, self.priv_esc_vuln_compatible_containers,
            self.agent_containers, self.router_containers,
            self.path, self.subnet_id_blacklist, self.subnet_prefix, self.subnet_id, self.num_flags, self.num_nodes)