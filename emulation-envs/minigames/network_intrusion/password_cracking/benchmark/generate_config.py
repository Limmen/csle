from gym_pycr_pwcrack.envs.config.generator.env_config_generator import EnvConfigGenerator
from gym_pycr_pwcrack.util.experiments_util import util

def generate_envs(num_envs : int, min_num_users : int = 1, max_num_users : int = 5, min_num_flags: int = 1,
                 max_num_flags : int = 5, min_num_nodes : int = 4, max_num_nodes : int = 10,
                 subnet_prefix: str = "172.18.", idx: int = 0, subnet_id_blacklist = None):
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

    subnet_id_blacklist = EnvConfigGenerator.generate_envs(num_envs=num_envs,
                                     container_pool=container_pool,
                                     gw_vuln_compatible_containers=gw_vuln_compatible_containers,
                                     pw_vuln_compatible_containers=pw_vuln_compatible_containers,
                                     agent_containers=agent_containers, router_containers=router_containers,
                                     path=util.default_output_dir(),
                                     min_num_users=min_num_users, max_num_users=max_num_users,
                                     min_num_flags=min_num_flags, max_num_flags=max_num_flags,
                                     min_num_nodes=min_num_nodes, max_num_nodes=max_num_nodes,
                                     subnet_prefix=subnet_prefix, cleanup_old_envs = False,
                                     start_idx=idx, subnet_id_blacklist=subnet_id_blacklist)
    return subnet_id_blacklist
if __name__ == '__main__':
    subnet_id_blacklist = generate_envs(1, min_num_users=1, max_num_users=3, min_num_flags=8, max_num_flags=8, min_num_nodes=25,
                  max_num_nodes=25, subnet_prefix="172.18.", idx=0)
    subnet_id_blacklist = generate_envs(1, min_num_users=1, max_num_users=3, min_num_flags=14, max_num_flags=14, min_num_nodes=50,
                  max_num_nodes=50, subnet_prefix="172.18.", idx=1, subnet_id_blacklist=subnet_id_blacklist)
    subnet_id_blacklist = generate_envs(1, min_num_users=1, max_num_users=3, min_num_flags=22, max_num_flags=22, min_num_nodes=75,
                  max_num_nodes=70, subnet_prefix="172.18.", idx=2, subnet_id_blacklist=subnet_id_blacklist)
    subnet_id_blacklist = generate_envs(1, min_num_users=1, max_num_users=3, min_num_flags=29, max_num_flags=29, min_num_nodes=100,
                  max_num_nodes=100, subnet_prefix="172.18.", idx=3, subnet_id_blacklist=subnet_id_blacklist)
