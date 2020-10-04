from typing import Tuple
import gym
import time
from abc import ABC
import numpy as np
import os
from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.dao.agent.agent_state import AgentState
from gym_pycr_pwcrack.dao.network.env_state import EnvState
from gym_pycr_pwcrack.dao.agent.agent_log import AgentLog
import gym_pycr_pwcrack.constants.constants as constants
from gym_pycr_pwcrack.envs.logic.transition_operator import TransitionOperator
from gym_pycr_pwcrack.dao.network.env_mode import EnvMode
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.envs.config.pycr_pwcrack_simple_base import PyCrPwCrackSimpleBase
from gym_pycr_pwcrack.dao.action.action_type import ActionType
from gym_pycr_pwcrack.dao.action.action_id import ActionId

class PyCRPwCrackEnv(gym.Env, ABC):
    """
    Abstract OpenAI Gym Env for the PyCr PwCrack minigame
    """

    def __init__(self, env_config : EnvConfig):
        self.env_config = env_config
        self.env_state = EnvState(network_config=self.env_config.network_conf, num_ports=self.env_config.num_ports,
                                  num_vuln=self.env_config.num_vuln, num_sh=self.env_config.num_sh,
                                  service_lookup=constants.SERVICES.service_lookup,
                                  vuln_lookup=constants.VULNERABILITIES.vuln_lookup,
                                  os_lookup=constants.OS.os_lookup, num_flags=self.env_config.num_flags)
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
        if self.env_config.env_mode == EnvMode.CLUSTER:
            self.env_config.cluster_config.connect_agent()
            self.env_config.cluster_config.download_cluster_services()
            self.env_state.merge_services_with_cluster(self.env_config.cluster_config.cluster_services)
            self.env_config.cluster_config.download_cves()
            self.env_state.merge_cves_with_cluster(self.env_config.cluster_config.cluster_cves)
            self.env_config.action_costs = self.env_config.cluster_config.load_action_costs(
                actions=self.env_config.action_conf.actions, dir=self.env_config.nmap_cache_dir,
                nmap_ids=self.env_config.action_conf.nmap_action_ids,
                network_service_ids=self.env_config.action_conf.network_service_action_ids,
                shell_ids=self.env_config.action_conf.shell_action_ids)
        self.env_config.scale_rewards_prep()
        self.agent_state = AgentState(obs_state=self.env_state.obs_state, env_log=AgentLog(),
                                      service_lookup=self.env_state.service_lookup,
                                      vuln_lookup=self.env_state.vuln_lookup,
                                      os_lookup=self.env_state.os_lookup)
        self.last_obs = self.env_state.get_observation()

    # -------- API ------------
    def step(self, action_id : int) -> Tuple[np.ndarray, int, bool, dict]:
        """
        Takes a step in the environment by executing the given action

        :param action_id: the action to take
        :return: (obs, reward, done, info)
        """
        info = {}
        if not self.is_action_legal(action_id, env_config=self.env_config, env_state=self.env_state):
            print("illegal action")
            done = False
            self.agent_state.time_step += 1
            if self.agent_state.time_step > self.env_config.max_episode_length:
                done = True
            return self.last_obs, -1, done, info
        if action_id > len(self.env_config.action_conf.actions)-1:
            raise ValueError("Action ID: {} not recognized".format(action_id))
        action = self.env_config.action_conf.actions[action_id]
        s_prime, reward, done = TransitionOperator.transition(s=self.env_state, a=action, env_config=self.env_config)
        if self.agent_state.time_step > self.env_config.max_episode_length:
            done = True
        self.env_state = s_prime
        if self.env_state.obs_state.detected:
            reward = reward - self.env_config.detection_reward
        m_obs, p_obs = self.env_state.get_observation()
        self.last_obs = m_obs
        self.agent_state.time_step += 1
        self.agent_state.episode_reward += reward
        self.agent_state.obs_state = self.env_state.obs_state
        self.__update_log(action)
        info["flags"] = self.env_state.obs_state.catched_flags
        return m_obs, reward, done, info

    def reset(self) -> np.ndarray:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :return: initial observation
        """
        self.__checkpoint_log()
        if self.env_state.obs_state.detected:
            self.agent_state.num_detections += 1
        elif self.env_state.obs_state.all_flags:
            self.agent_state.num_all_flags += 1
        self.env_state.reset_state()
        m_obs, p_obs = self.env_state.get_observation()
        self.last_obs = m_obs
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

    @staticmethod
    def is_action_legal(action_id : int, env_config: EnvConfig, env_state: EnvState):
        if not env_config.filter_illegal_actions:
            return True
        if action_id > len(env_config.action_conf.actions) - 1:
            return False
        action = env_config.action_conf.actions[action_id]

        # Recon on subnet is always possible
        if action.subnet:
            return True

        machine_discovered = False
        target_machine = None
        logged_in = False
        for m in env_state.obs_state.machines:
            if m.logged_in:
                logged_in = True
            if m.ip == action.ip:
                machine_discovered = True
                target_machine = m

        # If IP is discovered, then IP specific action without other prerequisites is legal
        if machine_discovered and (action.type == ActionType.RECON or action.type == ActionType.EXPLOIT):
            return True

        # If IP is discovered, and credentials are found and shell access, then post-exploit actions are legal
        if machine_discovered and action.type == ActionType.POST_EXPLOIT \
                and target_machine.shell_access and len(target_machine.shell_access_credentials) > 0:
            return True

        # Bash action not tied to specific IP only possible when having shell access and being logged in
        if action.id == ActionId.FIND_FLAG and logged_in:
            return True

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
        self.agent_state.env_log.add_entry(action.name + "[." + tag + "]" + " c:" + str(action.cost))

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


    def __checkpoint_log(self) -> None:
        """
        Checkpoints the agent log for an episode

        :return: None
        """
        if not self.env_config.checkpoint_dir == None \
                and self.agent_state.num_episodes % self.env_config.checkpoint_freq == 0:
            file_path = self.env_config.checkpoint_dir + "/ep_" + str(self.agent_state.num_episodes) + "_agent.log"
            with open(file_path, "w") as outfile:
                outfile.write("\n".join(self.agent_state.env_log.log))


# -------- Concrete envs ------------

# -------- Difficulty 1 (Simple) ------------

# -------- Simulation ------------

# -------- Version 1 ------------
class PyCRPwCrackSimpleSim1Env(PyCRPwCrackEnv):

    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackSimpleBase.render_conf()
            network_conf = PyCrPwCrackSimpleBase.network_conf()
            action_conf = PyCrPwCrackSimpleBase.action_conf(network_conf)
            env_config = PyCrPwCrackSimpleBase.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_conf=None, render_conf=render_config)
            env_config.simulate_detection = True
            # env_config.simulate_detection = False
            env_config.env_mode = EnvMode.SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
        super().__init__(env_config=env_config)

# -------- Cluster ------------

# -------- Version 1 ------------
class PyCRPwCrackSimpleCluster1Env(PyCRPwCrackEnv):
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackSimpleBase.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackSimpleBase.cluster_conf()
            network_conf = PyCrPwCrackSimpleBase.network_conf()
            action_conf = PyCrPwCrackSimpleBase.action_conf(network_conf)
            env_config = PyCrPwCrackSimpleBase.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config)
            env_config.env_mode = EnvMode.CLUSTER
            env_config.checkpoint_dir = checkpoint_dir
        super().__init__(env_config=env_config)


# -------- Difficulty 2 (Medium) ------------

# -------- Difficulty 3 (Hard) ------------
