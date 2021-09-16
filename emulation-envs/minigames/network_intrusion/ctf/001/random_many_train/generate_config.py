from pycr_common.envs_model.config.generator.env_config_generator import EnvConfigGenerator
from pycr_common.util.experiments_util import util
from pycr_common.dao.container_config.container_env_config import ContainerEnvConfig

def generate_envs(num_envs : int, min_num_users : int = 1, max_num_users : int = 5, min_num_flags: int = 1,
                 max_num_flags : int = 5, min_num_nodes : int = 4, max_num_nodes : int = 10,
                 subnet_prefix: str = "172.18."):
    EnvConfigGenerator.cleanup_envs(path = util.default_output_dir())

    # container_pool = [("ftp1", "0.0.1"), ("ftp2", "0.0.1"), ("honeypot1", "0.0.1"),
    #                   ("honeypot2", "0.0.1"),
    #                   ("ssh1", "0.0.1"), ("ssh2", "0.0.1"),
    #                   ("ssh3", "0.0.1"), ("telnet1", "0.0.1"), ("telnet2", "0.0.1"), ("telnet3", "0.0.1"),
    #                   ("cve_2015_1427_1", "0.0.1"), ("cve_2015_3306_1", "0.0.1"), ("cve_2016_10033_1", "0.0.1"),
    #                   ("samba1", "0.0.1"), ("sql_injection1", "0.0.1"), ("shellshock1", "0.0.1"),
    #                   ("cve_2010_0426_1", "0.0.1"), ("cve_2015_5602_1", "0.0.1")
    #                   ]
    container_pool = [("ftp1", "0.0.1"), ("ftp2", "0.0.1"), ("honeypot1", "0.0.1"),
                      ("honeypot2", "0.0.1"),
                      ("ssh1", "0.0.1"), ("ssh2", "0.0.1"),
                      ("ssh3", "0.0.1"), ("telnet1", "0.0.1"), ("telnet2", "0.0.1"), ("telnet3", "0.0.1"),
                      ]

    # gw_vuln_compatible_containers = [("ssh1", "0.0.1"), ("ssh2", "0.0.1"), ("ssh3", "0.0.1"), ("telnet1", "0.0.1"),
    #                                  ("telnet2", "0.0.1"), ("telnet3", "0.0.1"),
    #                                  ("cve_2015_1427_1", "0.0.1"), ("cve_2015_3306_1", "0.0.1"),
    #                                  ("cve_2016_10033_1", "0.0.1"),
    #                                  ("samba1", "0.0.1"), ("sql_injection1", "0.0.1"),
    #                                  ("shellshock1", "0.0.1")
    #                                  ]
    gw_vuln_compatible_containers = [("ssh1", "0.0.1"), ("ssh2", "0.0.1"), ("ssh3", "0.0.1"), ("telnet1", "0.0.1"),
                                     ("telnet2", "0.0.1"), ("telnet3", "0.0.1")]

    pw_vuln_compatible_containers = [("ssh1", "0.0.1"), ("ssh2", "0.0.1"), ("ssh3", "0.0.1"), ("telnet1", "0.0.1"),
                                     ("telnet2", "0.0.1"), ("telnet3", "0.0.1"), ("ftp1", "0.0.1"), ("ftp2", "0.0.1")
                                     ]
    # rce_vuln_compatible_containers = [("cve_2015_1427_1", "0.0.1"), ("cve_2015_3306_1", "0.0.1"),
    #                                   ("cve_2016_10033_1", "0.0.1"),
    #                                   ("samba1", "0.0.1"), ("sql_injection1", "0.0.1"),
    #                                   ("shellshock1", "0.0.1")
    #                                   ]
    rce_vuln_compatible_containers = []
    # sql_injection_vuln_compatible_containers = [("sql_injection1", "0.0.1")]
    sql_injection_vuln_compatible_containers = []
    # priv_esc_vuln_compatible_containers = [("cve_2010_0426_1", "0.0.1"), ("cve_2015_5602_1", "0.0.1")]
    priv_esc_vuln_compatible_containers = []

    agent_containers = [(("hacker_kali1", "0.0.1"))]
    #router_containers = [("router1", "0.0.1"), ("router2", "0.0.1")]
    router_containers = [("router2", "0.0.1")]

    container_env_config = ContainerEnvConfig(
        min_num_users=min_num_users, max_num_users=max_num_users, min_num_flags=min_num_flags,
        max_num_flags=max_num_flags, min_num_nodes=min_num_nodes, max_num_nodes=max_num_nodes,
        container_pool=container_pool, gw_vuln_compatible_containers=gw_vuln_compatible_containers,
        pw_vuln_compatible_containers=pw_vuln_compatible_containers,
        rce_vuln_compatible_containers=rce_vuln_compatible_containers,
        sql_injection_vuln_compatible_containers=sql_injection_vuln_compatible_containers,
        priv_esc_vuln_compatible_containers=priv_esc_vuln_compatible_containers,
        agent_containers=agent_containers, router_containers=router_containers,
        path=util.default_output_dir(), subnet_id_blacklist=set(), subnet_prefix=subnet_prefix
    )

    EnvConfigGenerator.generate_envs(num_envs=num_envs, container_env_config = container_env_config,
                                     cleanup_old_envs=True)
if __name__ == '__main__':
    generate_envs(20, min_num_users=1, max_num_users=3, min_num_flags=1, max_num_flags=4, min_num_nodes=6,
                  max_num_nodes=15, subnet_prefix="172.18.")
