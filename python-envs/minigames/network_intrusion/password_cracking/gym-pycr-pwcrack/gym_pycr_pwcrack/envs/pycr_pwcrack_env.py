from typing import Union
import gym
from abc import ABC
import numpy as np
import os
from gym_pycr_pwcrack.dao.env_config import EnvConfig
from gym_pycr_pwcrack.dao.agent_state import AgentState
from gym_pycr_pwcrack.dao.env_state import EnvState
from gym_pycr_pwcrack.dao.agent_log import AgentLog
import gym_pycr_pwcrack.constants.constants as constants
from gym_pycr_pwcrack.envs.logic.transition_operator import TransitionOperator
from gym_pycr_pwcrack.dao.node import Node
from gym_pycr_pwcrack.dao.flag import Flag
from gym_pycr_pwcrack.dao.node_type import NodeType
from gym_pycr_pwcrack.dao.network_config import NetworkConfig
from gym_pycr_pwcrack.dao.render_config import RenderConfig
from gym_pycr_pwcrack.dao.env_mode import EnvMode
from gym_pycr_pwcrack.dao.action_config import ActionConfig
from gym_pycr_pwcrack.dao.cluster_config import ClusterConfig

class PyCRPwCrackEnv(gym.Env, ABC):
    """
    TODO
    """

    def __init__(self, env_config : EnvConfig):
        self.env_config = env_config
        self.env_state = EnvState(network_config=self.env_config.network_conf)
        self.agent_state = AgentState(num_servers=self.env_config.num_nodes, num_ports=self.env_config.num_ports,
                                      num_vuln = self.env_config.num_vuln, env_log=AgentLog(),
                                      service_lookup=constants.SERVICES.service_lookup,
                                      vuln_lookup=constants.VULNERABILITIES.vuln_lookup,
                                      os_lookup = constants.OS.os_lookup)
        self.observation_space = gym.spaces.Box(low=0, high=10, dtype=np.int32, shape=(10, 10,))
        self.reward_range = (float(0), float(1))
        self.num_states = 100
        self.viewer = None
        self.steps_beyond_done = None
        self.metadata = {
            'render.modes': ['human', 'rgb_array'],
            'video.frames_per_second': 50  # Video rendering speed
        }
        self.step_outcome = None

    # -------- API ------------
    def step(self, action_id : int) -> Union[np.ndarray, int, bool, dict]:
        info = {}
        s_prime, reward, done = TransitionOperator.transition(s=self.env_state, a=action_id, env_config=self.env_config)
        self.env_state = s_prime
        obs = self.env_state.get_observation()
        return obs, reward, done, info

    def reset(self) -> np.ndarray:
        self.env_state.reset_state()
        obs = self.env_state.get_observation()
        return obs

    def render(self, mode: str = 'human'):
        """
        Renders the environment
        Supported rendering modes:
        - human: render to the current display or terminal and
          return nothing. Usually for human consumption.
        - rgb_array: Return an numpy.ndarray with shape (x, y, 3),
          representing RGB values for an x-by-y pixel image, suitable
          for turning into a video.
        :param mode: the rendering mode
        :return: True (if human mode) otherwise an rgb array
        """
        if mode not in self.metadata["render.modes"]:
            raise NotImplemented("mode: {} is not supported".format(mode))
        if self.viewer is None:
            self.__setup_viewer()
        self.viewer.mainframe.set_state(self.agent_state)
        arr = self.viewer.render(return_rgb_array=mode == 'rgb_array')
        return arr

    def close(self) -> None:
        """
        Closes the viewer (cleanup)
        :return: None
        """
        if self.viewer:
            self.viewer.close()
            self.viewer.mainframe.new_window()
            self.viewer = None

    # -------- Private methods ------------
    def __setup_viewer(self):
        """
        Setup for the viewer to use for rendering
        :return: None
        """
        from gym_pycr_pwcrack.envs.rendering.viewer import Viewer
        script_dir = os.path.dirname(__file__)
        resource_path = os.path.join(script_dir, './rendering/frames/', constants.RENDERING.RESOURCES_DIR)
        self.env_config.render_config.resources_dir = resource_path
        self.viewer = Viewer(env_config=self.env_config, init_state=self.agent_state)
        self.viewer.start()

# -------- Concrete envs ------------

# -------- Difficulty 1 (Simple) ------------

# -------- Version 1 ------------
class PyCRPwCrackSimpleSim1Env(PyCRPwCrackEnv):

    def __init__(self, env_config: EnvConfig):
        if env_config is None:
            nodes = [Node(ip="172.18.1.10", ip_id=10, id=1, type=NodeType.ROUTER, flags=[], level=2),
                     Node(ip="172.18.1.2", ip_id=2, id=2, type=NodeType.SERVER,
                          flags=[Flag(name="flag2", path="/home/kim", id=2)], level=3),
                     Node(ip="172.18.1.3", ip_id=3, id=3, type=NodeType.SERVER,
                          flags=[Flag(name="flag1", path="/home/admin", id=1)], level=3),
                     Node(ip="172.18.1.21", ip_id=21, id=4, type=NodeType.SERVER, flags=[], level=3),
                     Node(ip="172.18.1.79", ip_id=79, id=5, type=NodeType.SERVER,
                          flags=[Flag(name="flag3", path="/home/euler", id=3),
                                 Flag(name="flag4", path="/home/euler", id=4)], level=3),
                     Node(ip="172.18.1.191", ip_id=191, id=6, type=NodeType.HACKER, flags=[], level=1)]
            subnet_mask = "172.18.1.0/24"
            adj_matrix = [
                [0, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0],
            ]
            network_conf = NetworkConfig(subnet_mask=subnet_mask, nodes=nodes, adj_matrix=adj_matrix)
            render_config = RenderConfig()
            cluster_config = ClusterConfig()
            env_config = EnvConfig(network_conf=network_conf, action_conf=ActionConfig(actions=[]), num_ports=5, num_vuln=5,
                                   render_config=render_config, env_mode=EnvMode.SIMULATION, cluster_config=cluster_config)
        super().__init__(env_config=env_config)

# -------- Difficulty 2 (Medium) ------------

# -------- Difficulty 3 (Hard) ------------
