from typing import Tuple
import gym
import pickle
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
from gym_pycr_pwcrack.envs.config.simple.pycr_pwcrack_simple_base import PyCrPwCrackSimpleBase
from gym_pycr_pwcrack.dao.action.action_type import ActionType
from gym_pycr_pwcrack.dao.action.action_id import ActionId
from gym_pycr_pwcrack.envs.config.simple.pycr_pwcrack_simple_v1 import PyCrPwCrackSimpleV1
from gym_pycr_pwcrack.envs.config.simple.pycr_pwcrack_simple_v2 import PyCrPwCrackSimpleV2
from gym_pycr_pwcrack.envs.config.simple.pycr_pwcrack_simple_v3 import PyCrPwCrackSimpleV3
from gym_pycr_pwcrack.envs.config.simple.pycr_pwcrack_simple_v4 import PyCrPwCrackSimpleV4
from gym_pycr_pwcrack.envs.config.medium.pycr_pwcrack_medium_base import PyCrPwCrackMediumBase
from gym_pycr_pwcrack.envs.config.medium.pycr_pwcrack_medium_v1 import PyCrPwCrackMediumV1
from gym_pycr_pwcrack.envs.logic.common.env_dynamics_util import EnvDynamicsUtil

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
                                  os_lookup=constants.OS.os_lookup, num_flags=self.env_config.num_flags,
                                  state_type=self.env_config.state_type)
        self.observation_space = self.env_state.observation_space
        self.m_selection_observation_space = self.env_state.m_selection_observation_space
        self.m_action_observation_space = self.env_state.m_action_observation_space
        self.action_space = self.env_config.action_conf.action_space
        self.m_selection_action_space = gym.spaces.Discrete(self.env_state.obs_state.num_machines+1)
        self.m_action_space = self.env_config.action_conf.m_action_space
        self.num_actions = self.env_config.action_conf.num_actions
        self.network_orig_shape = self.env_state.network_orig_shape
        self.machine_orig_shape = self.env_state.machine_orig_shape
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
                shell_ids=self.env_config.action_conf.shell_action_ids,
                nikto_ids=self.env_config.action_conf.nikto_action_ids,
                masscan_ids=self.env_config.action_conf.masscan_action_ids,
                action_lookup_d_val = self.env_config.action_conf.action_lookup_d_val)
        self.env_config.scale_rewards_prep()
        self.agent_state = AgentState(obs_state=self.env_state.obs_state, env_log=AgentLog(),
                                      service_lookup=self.env_state.service_lookup,
                                      vuln_lookup=self.env_state.vuln_lookup,
                                      os_lookup=self.env_state.os_lookup)
        self.last_obs = self.env_state.get_observation()
        self.trajectory = []
        self.trajectories = []

    # -------- API ------------
    def step(self, action_id : int) -> Tuple[np.ndarray, int, bool, dict]:
        """
        Takes a step in the environment by executing the given action

        :param action_id: the action to take
        :return: (obs, reward, done, info)
        """
        self.trajectory = []
        self.trajectory.append(self.last_obs)
        self.trajectory.append(action_id)
        info = {}
        if not self.is_action_legal(action_id, env_config=self.env_config, env_state=self.env_state):
            print("illegal action:{}".format(action_id))
            done = False
            info["flags"] = self.env_state.obs_state.catched_flags
            self.agent_state.time_step += 1
            if self.agent_state.time_step > self.env_config.max_episode_length:
                done = True
            return self.last_obs, self.env_config.illegal_reward_action, done, info
        if action_id > len(self.env_config.action_conf.actions)-1:
            raise ValueError("Action ID: {} not recognized".format(action_id))
        action = self.env_config.action_conf.actions[action_id]
        action.ip = self.env_state.obs_state.get_action_ip(action)
        s_prime, reward, done = TransitionOperator.transition(s=self.env_state, a=action, env_config=self.env_config)
        if done:
            reward = reward - self.env_config.final_steps_reward_coefficient*self.agent_state.time_step
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
        self.trajectory.append(m_obs)
        self.trajectory.append(reward)
        info["flags"] = self.env_state.obs_state.catched_flags
        if self.env_config.save_trajectories:
            self.trajectories.append(self.trajectory)
        return m_obs, reward, done, info

    def reset(self) -> np.ndarray:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :return: initial observation
        """
        self.__checkpoint_log()
        self.__checkpoint_trajectories()
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
        self.agent_state.obs_state = self.env_state.obs_state
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
    def is_action_legal(action_id : int, env_config: EnvConfig, env_state: EnvState, m_selection: bool = False,
                        m_action: bool = False, m_index : int = None) -> bool:
        """
        Checks if a given action is legal in the current state of the environment

        :param action_id: the id of the action to check
        :param env_config: the environment config
        :param env_state: the environment state
        :param m_selection: boolean flag whether using AR policy m_selection or not
        :param m_action: boolean flag whether using AR policy m_action or not
        :param m_index: index of machine in case using AR policy
        :return: True if legal, else false
        """
        # If using AR policy
        if m_selection:
            return PyCRPwCrackEnv._is_action_legal_m_selection(action_id=action_id,env_config=env_config,
                                                               env_state=env_state)
        elif m_action:
            return PyCRPwCrackEnv._is_action_legal_m_action(action_id=action_id, env_config=env_config,
                                                            env_state=env_state, machine_index=m_index)

        if not env_config.filter_illegal_actions:
            return True
        if action_id > len(env_config.action_conf.actions) - 1:
            return False

        action = env_config.action_conf.actions[action_id]
        ip = env_state.obs_state.get_action_ip(action)

        logged_in_ips_str = EnvDynamicsUtil.logged_in_ips_str(env_config=env_config, a=action, s=env_state)
        if (action.id, action.index, logged_in_ips_str) in env_state.obs_state.actions_tried:
            return False

        # Recon on subnet is always possible
        if action.type == ActionType.RECON and action.subnet:
            return True

        machine_discovered = False
        target_machine = None
        logged_in = False
        unscanned_filesystems = False
        untried_credentials = False
        root_login = False
        uninstalled_tools = False
        machine_w_tools = False
        uninstalled_backdoor = False

        for m in env_state.obs_state.machines:
            if m.logged_in:
                logged_in = True
                if not m.filesystem_searched:
                    unscanned_filesystems = True
                if m.root:
                    root_login = True
                    if not m.tools_installed:
                        uninstalled_tools = True
                    else:
                        machine_w_tools = True
                    if not m.backdoor_installed:
                        uninstalled_backdoor = True
            if m.ip == ip:
                machine_discovered = True
                target_machine = m
            if m.shell_access and not m.logged_in:
                untried_credentials = True
            # if m.untried_credentials:
            #     untried_credentials = m.untried_credentials

        if action.subnet or action.id == ActionId.NETWORK_SERVICE_LOGIN:
            machine_discovered = True

        # If IP is discovered, then IP specific action without other prerequisites is legal
        if machine_discovered and (action.type == ActionType.RECON or action.type == ActionType.EXPLOIT):
            if action.subnet and target_machine is None:
                return True
            brute_tried = env_state.obs_state.brute_tried(a=action, m=target_machine)
            if brute_tried:
                return False
            return True

        # If nothing new to scan, find-flag is illegal
        if action.id == ActionId.FIND_FLAG and not unscanned_filesystems:
            return False

        # If nothing new to backdoor, install backdoor is illegal
        if action.id == ActionId.SSH_BACKDOOR and not uninstalled_backdoor:
            return False

        # If no new credentials, login to service is illegal
        if action.id == ActionId.NETWORK_SERVICE_LOGIN and not untried_credentials:
            return False

        # Pivot recon possible if logged in on pivot machine with tools installed
        if machine_discovered and action.type == ActionType.POST_EXPLOIT and logged_in and machine_w_tools:
            return True

        # If IP is discovered, and credentials are found and shell access, then post-exploit actions are legal
        if machine_discovered and action.type == ActionType.POST_EXPLOIT \
                and ((target_machine is not None and target_machine.shell_access
                      and len(target_machine.shell_access_credentials) > 0)
                     or action.subnet or action.id == ActionId.NETWORK_SERVICE_LOGIN):
            return True

        # Bash action not tied to specific IP only possible when having shell access and being logged in
        if action.id == ActionId.FIND_FLAG and logged_in and unscanned_filesystems:
            return True

        # Bash action not tied to specific IP only possible when having shell access and being logged in and root
        if action.id == ActionId.INSTALL_TOOLS and logged_in and root_login and uninstalled_tools:
            return True

        # Bash action not tied to specific IP only possible when having shell access and being logged in and root
        if action.id == ActionId.SSH_BACKDOOR and logged_in and root_login and machine_w_tools and uninstalled_backdoor:
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

    def cleanup(self) -> None:
        """
        Cleans up environment state. This method is particularly useful in cluster mode where there are
        SSH/Telnet/FTP... connections that should be cleaned up, as well as background threads.

        :return: None
        """
        if self.env_config.env_mode == EnvMode.SIMULATION:
            return
        else:
            self.env_state.cleanup()

    def convert_ar_action(self, machine_idx, action_idx):
        """
        Converts an AR action id into a global action id

        :param machine_idx: the machine id
        :param action_idx: the action id
        :return: the global action id
        """
        key = (machine_idx, action_idx)
        return self.env_config.action_conf.ar_action_converter[key]

    # -------- Private methods ------------

    def __update_log(self, action : Action) -> None:
        """
        Updates the log for rendering with a new action

        :param action: the new action to add to the log
        :return: None
        """
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

    def __checkpoint_trajectories(self) -> None:
        """
        Checkpoints agent trajectories

        :return: None
        """
        if self.env_config.save_trajectories and not self.env_config.checkpoint_dir == None \
                and self.agent_state.num_episodes % self.env_config.checkpoint_freq == 0:
            file_path = self.env_config.checkpoint_dir + "/ep_" + str(self.agent_state.num_episodes) + "_trajectories.pickle"
            with open(file_path, "wb") as outfile:
                pickle.dump(self.trajectories, outfile, protocol=pickle.HIGHEST_PROTOCOL)
                self.trajectories = []

    @staticmethod
    def _is_action_legal_m_selection(action_id: int, env_config: EnvConfig, env_state: EnvState) -> bool:
        """
        Utility method to check if a m_selection action is legal for AR policies

        :param action_id: the action id of the m_selection to  check
        :param env_config: the environment config
        :param env_state: the environment state
        :return: True if legal else False
        """
        # Subnet actions are always legal
        if action_id == env_config.num_nodes:
            return True

        # If machine is discovered then it is a legal action
        if action_id < len(env_state.obs_state.machines):
            m = env_state.obs_state.machines[action_id]
            if m is not None:
                return True

        return False

    @staticmethod
    def _is_action_legal_m_action(action_id: int, env_config: EnvConfig, env_state: EnvState, machine_index : int) \
            -> bool:
        """
        Utility method to check if a machine-specific action is legal or not for AR-policies

        :param action_id: the machine-specific-action-id
        :param env_config: the environment config
        :param env_state: the environment state
        :param machine_index: index of the machine to apply the action to
        :return: True if legal else False
        """
        action_id_id = env_config.action_conf.action_ids[action_id]
        key = (action_id_id, machine_index)
        if key not in env_config.action_conf.action_lookup_d:
            return False
        action = env_config.action_conf.action_lookup_d[(action_id_id, machine_index)]
        logged_in = False
        for m in env_state.obs_state.machines:
            if m.logged_in:
                logged_in = True

        if machine_index == env_config.num_nodes:
            if action.subnet or action.index == env_config.num_nodes:
                # Recon an exploits are always legal
                if action.type == ActionType.RECON or action.type == ActionType.EXPLOIT:
                    return True
                # Bash action not tied to specific IP only possible when having shell access and being logged in
                if action.id == ActionId.FIND_FLAG and logged_in:
                    return True
                return False
            else:
                return False
        else:
            if action.subnet or action.index == env_config.num_nodes:
                return False
            else:
                # Recon an exploits are always legal
                if action.type == ActionType.RECON or action.type == ActionType.EXPLOIT:
                    return True

                if machine_index < len(env_state.obs_state.machines):
                    env_state.obs_state.sort_machines()
                    target_machine = env_state.obs_state.machines[machine_index]

                    # If IP is discovered, and credentials are found and shell access, then post-exploit actions are legal
                    if action.type == ActionType.POST_EXPLOIT and target_machine.shell_access \
                            and len(target_machine.shell_access_credentials) > 0:
                        return True

                    # Bash action not tied to specific IP only possible when having shell access and being logged in
                    if action.id == ActionId.FIND_FLAG and logged_in:
                        return True
        return False


# -------- Concrete envs ------------

# -------- Difficulty 1 (Simple) ------------

# -------- Simulation ------------

# -------- Base Version (for testing) ------------
class PyCRPwCrackSimpleSimBaseEnv(PyCRPwCrackEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackSimpleBase.render_conf()
            network_conf = PyCrPwCrackSimpleBase.network_conf()
            action_conf = PyCrPwCrackSimpleBase.all_actions_conf(network_conf)
            env_config = PyCrPwCrackSimpleBase.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_conf=None, render_conf=render_config)
            env_config.simulate_detection = True
            env_config.save_trajectories = False
            # env_config.simulate_detection = False
            env_config.env_mode = EnvMode.SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 1 ------------
class PyCRPwCrackSimpleSim1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackSimpleBase.render_conf()
            network_conf = PyCrPwCrackSimpleBase.network_conf()
            action_conf = PyCrPwCrackSimpleV1.actions_conf(network_conf)
            env_config = PyCrPwCrackSimpleV1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_conf=None, render_conf=render_config)
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Cluster ------------

# -------- Base Version (for testing) ------------

class PyCRPwCrackSimpleClusterBaseEnv(PyCRPwCrackEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackSimpleBase.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackSimpleBase.cluster_conf()
            network_conf = PyCrPwCrackSimpleBase.network_conf()
            action_conf = PyCrPwCrackSimpleBase.all_actions_conf(network_conf)
            env_config = PyCrPwCrackSimpleBase.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config)
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 1 ------------

class PyCRPwCrackSimpleCluster1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackSimpleBase.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackSimpleBase.cluster_conf()
            network_conf = PyCrPwCrackSimpleBase.network_conf()
            action_conf = PyCrPwCrackSimpleV1.actions_conf(network_conf)
            env_config = PyCrPwCrackSimpleV1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config)
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 2 ------------

class PyCRPwCrackSimpleCluster2Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V1. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackSimpleBase.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackSimpleBase.cluster_conf()
            network_conf = PyCrPwCrackSimpleBase.network_conf()
            action_conf = PyCrPwCrackSimpleV2.actions_conf(network_conf)
            env_config = PyCrPwCrackSimpleV2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config)
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 ------------

class PyCRPwCrackSimpleCluster3Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackSimpleBase.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackSimpleBase.cluster_conf()
            network_conf = PyCrPwCrackSimpleBase.network_conf()
            action_conf = PyCrPwCrackSimpleV3.actions_conf(network_conf)
            env_config = PyCrPwCrackSimpleV3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config)
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 ------------

class PyCRPwCrackSimpleCluster4Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackSimpleBase.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackSimpleBase.cluster_conf()
            network_conf = PyCrPwCrackSimpleBase.network_conf()
            action_conf = PyCrPwCrackSimpleV4.actions_conf(network_conf)
            env_config = PyCrPwCrackSimpleV4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config)
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Difficulty 2 (Medium) ------------

# -------- Simulation ------------

# -------- Base Version (for testing) ------------
class PyCRPwCrackMediumSimBaseEnv(PyCRPwCrackEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackMediumBase.render_conf()
            network_conf = PyCrPwCrackMediumBase.network_conf()
            action_conf = PyCrPwCrackMediumBase.all_actions_conf(network_conf)
            env_config = PyCrPwCrackMediumBase.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_conf=None, render_conf=render_config)
            env_config.simulate_detection = True
            env_config.save_trajectories = False
            # env_config.simulate_detection = False
            env_config.env_mode = EnvMode.SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Cluster ------------

# -------- Base Version (for testing) ------------

class PyCRPwCrackMediumClusterBaseEnv(PyCRPwCrackEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackMediumBase.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackMediumBase.cluster_conf()
            network_conf = PyCrPwCrackMediumBase.network_conf()
            action_conf = PyCrPwCrackMediumBase.all_actions_conf(network_conf)
            env_config = PyCrPwCrackMediumBase.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config)
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 1 ------------

class PyCRPwCrackMediumCluster1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackMediumBase.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackMediumBase.cluster_conf()
            network_conf = PyCrPwCrackMediumBase.network_conf()
            action_conf = PyCrPwCrackMediumV1.actions_conf(network_conf)
            env_config = PyCrPwCrackMediumV1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config)
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Difficulty 3 (Hard) ------------
