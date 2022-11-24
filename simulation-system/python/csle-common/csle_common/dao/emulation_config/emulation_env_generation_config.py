from typing import List, Tuple, Set


class EmulationEnvGenerationConfig:
    """
    A DTO representing the configuration of a dynamically created emulation environment
    """

    def __init__(self, min_num_users: int = 1, max_num_users: int = 5, min_num_flags: int = 1,
                 max_num_flags: int = 5, min_num_nodes: int = 4, max_num_nodes: int = 10,
                 container_pool: List[Tuple[str, str]] = None,
                 gw_vuln_compatible_containers: List[Tuple[str, str]] = None,
                 pw_vuln_compatible_containers: List[Tuple[str, str]] = None,
                 rce_vuln_compatible_containers: List[Tuple[str, str]] = None,
                 sql_injection_vuln_compatible_containers: List[Tuple[str, str]] = None,
                 priv_esc_vuln_compatible_containers: List[Tuple[str, str]] = None,
                 agent_containers: List[Tuple[str, str]] = None,
                 router_containers: List[Tuple[str, str]] = None,
                 path: str = "", subnet_id_blacklist: Set = None,
                 subnet_prefix: str = "", subnet_id: int = -1, num_flags: int = -1, num_nodes: int = -1,
                 min_cpus: int = 1, max_cpus: int = 1, min_mem_G: int = 4, max_mem_G: int = 4):
        """
        Initializes the object

        :param min_num_users: the minimum number of users
        :param max_num_users: the maximum number of users
        :param min_num_flags: the minimum number of flags
        :param max_num_flags: the maximum number of flags
        :param min_num_nodes: the minimum number of nodes
        :param max_num_nodes: the maximum number of nodes
        :param container_pool: the pool of containers for emulation
        :param gw_vuln_compatible_containers: the pool of gw-compatible containers
        :param pw_vuln_compatible_containers: the pool of pw-vuln-compatible containers
        :param rce_vuln_compatible_containers: the pool of rce-compatible containers
        :param sql_injection_vuln_compatible_containers: the pool of sql-injection-compatible containers
        :param priv_esc_vuln_compatible_containers: the pool of priv-esc-compatible containers
        :param agent_containers: the pool of agent containers
        :param router_containers: the pool of router containers
        :param path: the path to the config
        :param subnet_id_blacklist: the black list of subnet ids
        :param subnet_prefix: the prefix of the subnet
        :param subnet_id: the subnet id
        :param num_flags: the number of flags
        :param num_nodes: the number of nodes
        :param min_cpus: the minimum number of CPUs per container
        :param max_cpus: the maximum number of CPUs per container
        :param min_mem_G: the minimum number of memory GB for each container
        :param max_mem_G: the maximum number of memory GB for each container
        """
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
        self.min_cpus = min_cpus
        self.max_cpus = max_cpus
        self.min_mem_G = min_mem_G
        self.max_mem_G = max_mem_G

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
        return f"min_num_users:{self.min_num_users}, max_num_users:{self.max_num_users}, " \
               f"min_num_flags:{self.min_num_flags}, max_num_flags:{self.max_num_flags}," \
               f"min_num_nodes:{self.min_num_nodes}, max_num_nodes:{self.max_num_nodes}, " \
               f"container_pool:{self.container_pool}, " \
               f"gw_vuln_compatible_containers:{self.gw_vuln_compatible_containers}," \
               f"pw_vuln_compatible_containers:{self.pw_vuln_compatible_containers}, " \
               f"rce_vuln_compatible_containers:{self.rce_vuln_compatible_containers}, " \
               f"sql_injection_vuln_compatible_containers:{self.sql_injection_vuln_compatible_containers}, " \
               f"priv_esc_vuln_compatible_containers:{self.priv_esc_vuln_compatible_containers}" \
               f"agent_containers:{self.agent_containers}, router_containers:{self.router_containers}, " \
               f"path:{self.path}, subnet_id_blacklist:{self.subnet_id_blacklist}, " \
               f"subnet_prefix:{self.subnet_prefix}, subnet_id:{self.subnet_id}, num_flags:{self.num_flags}, " \
               f"num_nodes:{self.num_nodes}, min_cpus:{self.min_cpus}, max_cpus:{self.max_cpus}, " \
               f"min_mem_G:{self.min_mem_G}, max_mem_G:{self.max_mem_G}"

    def copy(self) -> "EmulationEnvGenerationConfig":
        """
        :return: a copy of the object
        """
        return EmulationEnvGenerationConfig(
            min_num_users=self.min_num_users, max_num_users=self.max_num_users, min_num_flags=self.min_num_flags,
            max_num_flags=self.max_num_flags, min_num_nodes=self.min_num_nodes, max_num_nodes=self.max_num_nodes,
            container_pool=self.container_pool, gw_vuln_compatible_containers=self.gw_vuln_compatible_containers,
            pw_vuln_compatible_containers=self.pw_vuln_compatible_containers,
            rce_vuln_compatible_containers=self.rce_vuln_compatible_containers,
            sql_injection_vuln_compatible_containers=self.sql_injection_vuln_compatible_containers,
            priv_esc_vuln_compatible_containers=self.priv_esc_vuln_compatible_containers,
            agent_containers=self.agent_containers, router_containers=self.router_containers,
            path=self.path, subnet_id_blacklist=self.subnet_id_blacklist.copy(),
            subnet_prefix=self.subnet_prefix, subnet_id=self.subnet_id, num_flags=self.num_flags,
            num_nodes=self.num_nodes, min_cpus=self.min_cpus, max_cpus=self.max_cpus,
            min_mem_G=self.min_mem_G, max_mem_G=self.max_mem_G
        )
