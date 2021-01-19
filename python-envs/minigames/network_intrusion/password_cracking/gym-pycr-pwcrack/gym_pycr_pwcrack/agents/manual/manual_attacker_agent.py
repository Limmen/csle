"""
Manual attacker agent
"""
try:
    from gym_pycr_pwcrack.envs.rendering.viewer import Viewer
except:
    pass
from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.envs import PyCRPwCrackEnv
from gym_pycr_pwcrack.dao.network.network_config import NetworkConfig

class ManualAttackerAgent:
    """
    Class representing a manual attacker agent, controlled in the GUI by keyboard
    """

    def __init__(self, env_config: EnvConfig, env: PyCRPwCrackEnv):
        """
        Sets up the GUI with the manual attacker

        :param idsgame_config: the configuration
        """
        self.env = env
        self.env_config = env_config

        # net = NetworkConfig.load("/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/password_cracking/gym-pycr-pwcrack/examples/random_many/training/v1/generated_simulation/ppo_baseline/netconf9.pkl")
        # env_config = env_config.copy()
        # env_config.network_conf = net
        # # env_config.router_ip = router_ip
        # # env_config.hacker_ip = agent_ip
        # # env_config.ids_router = ids_router
        # env_config.num_flags = len(net.flags_lookup)
        # #env_config.blacklist_ips = [subnet_prefix + ".1"]
        # # env_config.num_nodes = len(randomized_nodes)
        # for a in env_config.action_conf.actions:
        #     if a.subnet:
        #         a.ip = net.subnet_mask
        # self.env.env_config = env_config

        self.env.env_config.action_conf.print_actions()

        agent_state = self.env.agent_state
        viewer = Viewer(self.env_config, init_state=agent_state)
        viewer.manual_start_attacker(env=self.env)
