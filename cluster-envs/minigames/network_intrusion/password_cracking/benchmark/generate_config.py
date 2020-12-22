from gym_pycr_pwcrack.envs.config.generator.env_config_generator import EnvConfigGenerator
from gym_pycr_pwcrack.util.experiments_util import util

def generate_envs(num_envs : int, min_num_users : int = 1, max_num_users : int = 5, min_num_flags: int = 1,
                 max_num_flags : int = 5, min_num_nodes : int = 4, max_num_nodes : int = 10,
                 subnet_prefix: str = "172.18."):
    #EnvConfigGenerator.cleanup_envs(path = util.default_output_dir())

    container_pool = [("ftp1", "0.0.1"), ("ftp2", "0.0.1"), ("honeypot1", "0.0.1"),
                      ("honeypot2", "0.0.1"),
                      ("ssh1", "0.0.1"), ("ssh2", "0.0.1"),
                      ("ssh3", "0.0.1"), ("telnet1", "0.0.1"), ("telnet2", "0.0.1"), ("telnet3", "0.0.1")]
    gw_vuln_compatible_containers = [("ssh1", "0.0.1"), ("ssh2", "0.0.1"), ("ssh3", "0.0.1"), ("telnet1", "0.0.1"),
                                     ("telnet2", "0.0.1"), ("telnet3", "0.0.1")]

    pw_vuln_compatible_containers = [("ssh1", "0.0.1"), ("ssh2", "0.0.1"), ("ssh3", "0.0.1"), ("telnet1", "0.0.1"),
                                     ("telnet2", "0.0.1"), ("telnet3", "0.0.1"), ("ftp1", "0.0.1"), ("ftp2", "0.0.1")]

    agent_containers = [(("hacker_kali1", "0.0.1"))]
    #router_containers = [("router1", "0.0.1"), ("router2", "0.0.1")]
    router_containers = [("router2", "0.0.1")]

    EnvConfigGenerator.generate_envs(num_envs=num_envs,
                                     container_pool=container_pool,
                                     gw_vuln_compatible_containers=gw_vuln_compatible_containers,
                                     pw_vuln_compatible_containers=pw_vuln_compatible_containers,
                                     agent_containers=agent_containers, router_containers=router_containers,
                                     path=util.default_output_dir(),
                                     min_num_users=min_num_users, max_num_users=max_num_users,
                                     min_num_flags=min_num_flags, max_num_flags=max_num_flags,
                                     min_num_nodes=min_num_nodes, max_num_nodes=max_num_nodes,
                                     subnet_prefix=subnet_prefix, cleanup_old_envs = False)
if __name__ == '__main__':
    generate_envs(1, min_num_users=1, max_num_users=3, min_num_flags=1, max_num_flags=1, min_num_nodes=5,
                  max_num_nodes=5, subnet_prefix="172.18.")
    generate_envs(1, min_num_users=1, max_num_users=3, min_num_flags=2, max_num_flags=2, min_num_nodes=10,
                  max_num_nodes=10, subnet_prefix="172.18.")
    generate_envs(1, min_num_users=1, max_num_users=3, min_num_flags=5, max_num_flags=5, min_num_nodes=20,
                  max_num_nodes=20, subnet_prefix="172.18.")
    generate_envs(1, min_num_users=1, max_num_users=3, min_num_flags=8, max_num_flags=8, min_num_nodes=30,
                  max_num_nodes=30, subnet_prefix="172.18.")
    generate_envs(1, min_num_users=1, max_num_users=3, min_num_flags=11, max_num_flags=11, min_num_nodes=40,
                  max_num_nodes=40, subnet_prefix="172.18.")
    generate_envs(1, min_num_users=1, max_num_users=3, min_num_flags=14, max_num_flags=14, min_num_nodes=50,
                  max_num_nodes=50, subnet_prefix="172.18.")
    generate_envs(1, min_num_users=1, max_num_users=3, min_num_flags=17, max_num_flags=17, min_num_nodes=60,
                  max_num_nodes=60, subnet_prefix="172.18.")
    generate_envs(1, min_num_users=1, max_num_users=3, min_num_flags=20, max_num_flags=20, min_num_nodes=70,
                  max_num_nodes=70, subnet_prefix="172.18.")
    generate_envs(1, min_num_users=1, max_num_users=3, min_num_flags=23, max_num_flags=23, min_num_nodes=80,
                  max_num_nodes=80, subnet_prefix="172.18.")
    generate_envs(1, min_num_users=1, max_num_users=3, min_num_flags=26, max_num_flags=26, min_num_nodes=90,
                  max_num_nodes=90, subnet_prefix="172.18.")
    generate_envs(1, min_num_users=1, max_num_users=3, min_num_flags=29, max_num_flags=29, min_num_nodes=100,
                  max_num_nodes=100, subnet_prefix="172.18.")
