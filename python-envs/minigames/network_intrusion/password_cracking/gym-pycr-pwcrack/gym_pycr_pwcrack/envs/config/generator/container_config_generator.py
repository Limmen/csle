from gym_pycr_pwcrack.dao.container_config.vulnerability_type import VulnType
from gym_pycr_pwcrack.envs.config.generator.topology_generator import TopologyGenerator
from gym_pycr_pwcrack.envs.config.generator.vuln_generator import VulnerabilityGenerator
from gym_pycr_pwcrack.envs.config.generator.flags_generator import FlagsGenerator
from gym_pycr_pwcrack.envs.config.generator.users_generator import UsersGenerator


class ContainerConfigGenerator:

    @staticmethod
    def generate(num_nodes : int, subnet_prefix : str, num_flags: int, max_num_users: int):
        adj_matrix, gws, topology, agent_ip, router_ip = TopologyGenerator.generate(num_nodes=10,
                                                                                    subnet_prefix="172.18.2.")
        vulnerabilities = VulnerabilityGenerator.generate(topology=topology, gateways=gws, agent_ip=agent_ip,
                                                          subnet_prefix="172.18.2.",
                                                          num_flags=3, access_vuln_types=[VulnType.WEAK_PW])
        users = UsersGenerator.generate(max_num_users=5, topology=topology)
        flags = FlagsGenerator.generate(vulnerabilities=vulnerabilities, num_flags=2)

        return topology, vulnerabilities, users, flags



if __name__ == '__main__':
    topology, vulnerabilities, users, flags = ContainerConfigGenerator.generate(num_nodes = 10, subnet_prefix="172.18.2.", num_flags=3, max_num_users=2)
    
