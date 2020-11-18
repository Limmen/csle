"""
Manual attacker agent
"""
try:
    from gym_pycr_pwcrack.envs.rendering.viewer import Viewer
except:
    pass
from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.envs import PyCRPwCrackEnv

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
        self.env.env_config.action_conf.print_actions()
        agent_state = self.env.agent_state
        viewer = Viewer(self.env_config, init_state=agent_state)
        viewer.manual_start_attacker(env=self.env)
