from gym_pycr_pwcrack.envs.config.generator.env_config_generator import EnvConfigGenerator
from gym_pycr_pwcrack.util.experiments_util import util

def generate_envs(num_envs : int):
    EnvConfigGenerator.cleanup_envs(path = util.default_output_dir())

    container_pool = [("ftp1", "0.0.1"), ("ftp2", "0.0.1"), ("honeypot1", "0.0.1"),
                      ("honeypot2", "0.0.1"),
                      ("ssh1", "0.0.1"), ("ssh2", "0.0.1"),
                      ("ssh3", "0.0.1"), ("telnet1", "0.0.1"), ("telnet2", "0.0.1"), ("telnet3", "0.0.1")]
    gw_vuln_compatible_containers = [("ssh1", "0.0.1"), ("ssh2", "0.0.1"), ("ssh3", "0.0.1"), ("telnet1", "0.0.1"),
                                     ("telnet2", "0.0.1"), ("telnet3", "0.0.1")]

    pw_vuln_compatible_containers = [("ssh1", "0.0.1"), ("ssh2", "0.0.1"), ("ssh3", "0.0.1"), ("telnet1", "0.0.1"),
                                     ("telnet2", "0.0.1"), ("telnet3", "0.0.1"), ("ftp1", "0.0.1"), ("ftp2", "0.0.1")]

    agent_containers = [(("hacker_kali1", "0.0.1"))]
    router_containers = [("router1", "0.0.1"), ("router2", "0.0.1")]

    EnvConfigGenerator.generate_envs(num_envs=num_envs,
                                     container_pool=container_pool,
                                     gw_vuln_compatible_containers=gw_vuln_compatible_containers,
                                     pw_vuln_compatible_containers=pw_vuln_compatible_containers,
                                     agent_containers=agent_containers, router_containers=router_containers,
                                     path=util.default_output_dir())
if __name__ == '__main__':
    generate_envs(2)
