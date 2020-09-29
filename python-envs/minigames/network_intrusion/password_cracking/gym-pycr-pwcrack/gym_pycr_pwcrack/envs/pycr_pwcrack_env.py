from typing import Union
import gym
from abc import ABC
import numpy as np
import os
from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.dao.agent.agent_state import AgentState
from gym_pycr_pwcrack.dao.network.env_state import EnvState
from gym_pycr_pwcrack.dao.agent.agent_log import AgentLog
import gym_pycr_pwcrack.constants.constants as constants
from gym_pycr_pwcrack.envs.logic.transition_operator import TransitionOperator
from gym_pycr_pwcrack.dao.render.render_config import RenderConfig
from gym_pycr_pwcrack.dao.network.env_mode import EnvMode
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.envs.config.pycr_pwcrack_simple_base import PyCrPwCrackSimpleBase

class PyCRPwCrackEnv(gym.Env, ABC):
    """
    Abstract OpenAI Gym Env for the PyCr PwCrack minigame
    """

    def __init__(self, env_config : EnvConfig):
        self.env_config = env_config
        self.env_state = EnvState(network_config=self.env_config.network_conf, num_ports=self.env_config.num_ports,
                                  num_vuln=self.env_config.num_vuln,
                                  service_lookup=constants.SERVICES.service_lookup,
                                  vuln_lookup=constants.VULNERABILITIES.vuln_lookup,
                                  os_lookup=constants.OS.os_lookup)
        self.agent_state = AgentState(obs_state=self.env_state.obs_state, env_log=AgentLog(),
                                      service_lookup=constants.SERVICES.service_lookup,
                                      vuln_lookup=constants.VULNERABILITIES.vuln_lookup,
                                      os_lookup = constants.OS.os_lookup)
        self.observation_space = self.env_state.observation_space
        self.action_space = self.env_config.action_conf.action_space
        self.num_actions = self.env_config.action_conf.num_actions
        self.reward_range = (float(0), float(1))
        self.num_states = 100
        self.viewer = None
        self.steps_beyond_done = None
        self.metadata = {
            'render.modes': ['human', 'rgb_array'],
            'video.frames_per_second': 50  # Video rendering speed
        }
        self.step_outcome = None
        self.env_config.cluster_config.connect_agent()

    # -------- API ------------
    def step(self, action_id : int) -> Union[np.ndarray, int, bool, dict]:
        """
        Takes a step in the environment by executing the given action

        :param action_id: the action to take
        :return: (obs, reward, done, info)
        """
        info = {}
        if action_id > len(self.env_config.action_conf.actions)-1:
            raise ValueError("Action ID: {} not recognized".format(action_id))
        action = self.env_config.action_conf.actions[action_id]
        s_prime, reward, done = TransitionOperator.transition(s=self.env_state, a=action, env_config=self.env_config)
        self.env_state = s_prime
        if self.env_state.obs_state.detected:
            reward = reward - self.env_config.detection_reward
        m_obs, p_obs = self.env_state.get_observation()
        self.agent_state.time_step += 1
        self.agent_state.episode_reward += reward
        self.agent_state.obs_state = self.env_state.obs_state
        self.__update_log(action)
        return m_obs, reward, done, info

    def reset(self) -> np.ndarray:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :return: initial observation
        """
        if self.env_state.obs_state.detected:
            self.agent_state.num_detections += 1
        elif self.env_state.obs_state.all_flags:
            self.agent_state.num_all_flags += 1
        self.env_state.reset_state()
        m_obs, p_obs = self.env_state.get_observation()
        self.agent_state.num_episodes += 1
        self.agent_state.cumulative_reward += self.agent_state.episode_reward
        self.agent_state.time_step = 0
        self.agent_state.episode_reward = 0
        self.agent_state.env_log.reset()
        return m_obs

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

    def is_action_legal(self, action_id : int):
        if action_id <= len(self.env_config.action_conf.actions)-1:
            return True
        else:
            return False

    def close(self) -> None:
        """
        Closes the viewer (cleanup)
        :return: None
        """
        if self.viewer:
            self.viewer.close()
            self.viewer = None
            #self.
            #self.viewer.mainframe.new_window()

    # -------- Private methods ------------

    def __update_log(self, action : Action) -> None:
        tag = "-"
        if not action.subnet:
            if action.ip is not None:
                tag = str(action.ip.rsplit(".", 1)[-1])
        else:
            tag = "*"
        self.agent_state.env_log.add_entry(action.name + "[." + tag + "]")

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

# -------- Simulation ------------

# -------- Version 1 ------------
class PyCRPwCrackSimpleSim1Env(PyCRPwCrackEnv):

    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig):
        if env_config is None:
            render_config = PyCrPwCrackSimpleBase.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackSimpleBase.cluster_conf()
            network_conf = PyCrPwCrackSimpleBase.network_conf()
            action_conf = PyCrPwCrackSimpleBase.action_conf(network_conf)
            env_config = PyCrPwCrackSimpleBase.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_config=cluster_config, render_config=render_config)
        super().__init__(env_config=env_config)

# -------- Cluster ------------

# -------- Version 1 ------------
class PyCRPwCrackSimpleCluster1Env(PyCRPwCrackEnv):

    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig):
        if env_config is None:
            render_config = PyCrPwCrackSimpleBase.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackSimpleBase.cluster_conf()
            network_conf = PyCrPwCrackSimpleBase.network_conf()
            action_conf = PyCrPwCrackSimpleBase.action_conf(network_conf)
            env_config = PyCrPwCrackSimpleBase.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_config=cluster_config, render_config=render_config)
            env_config.env_mode = EnvMode.CLUSTER

        super().__init__(env_config=env_config)


# -------- Difficulty 2 (Medium) ------------

# -------- Difficulty 3 (Hard) ------------
