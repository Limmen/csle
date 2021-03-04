from typing import Tuple, List
import gym
import pickle
from abc import ABC
import numpy as np
import os
import sys
from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.dao.agent.agent_state import AgentState
from gym_pycr_pwcrack.dao.network.env_state import EnvState
from gym_pycr_pwcrack.dao.agent.agent_log import AgentLog
import gym_pycr_pwcrack.constants.constants as constants
from gym_pycr_pwcrack.envs.logic.transition_operator import TransitionOperator
from gym_pycr_pwcrack.dao.network.env_mode import EnvMode
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.envs.config.level_1.pycr_pwcrack_level_1_base import PyCrPwCrackLevel1Base
from gym_pycr_pwcrack.dao.action.action_type import ActionType
from gym_pycr_pwcrack.dao.action.action_id import ActionId
from gym_pycr_pwcrack.envs.config.level_1.pycr_pwcrack_level_1_nocache_v1 import PyCrPwCrackLevel1NoCacheV1
from gym_pycr_pwcrack.envs.config.level_1.pycr_pwcrack_level_1_v1 import PyCrPwCrackLevel1V1
from gym_pycr_pwcrack.envs.config.level_1.pycr_pwcrack_level_1_v2 import PyCrPwCrackLevel1V2
from gym_pycr_pwcrack.envs.config.level_1.pycr_pwcrack_level_1_v3 import PyCrPwCrackLevel1V3
from gym_pycr_pwcrack.envs.config.level_1.pycr_pwcrack_level_1_v4 import PyCrPwCrackLevel1V4
from gym_pycr_pwcrack.envs.config.level_2.pycr_pwcrack_level_2_base import PyCrPwCrackLevel2Base
from gym_pycr_pwcrack.envs.config.level_2.pycr_pwcrack_level_2_v1 import PyCrPwCrackLevel2V1
from gym_pycr_pwcrack.envs.config.level_2.pycr_pwcrack_level_2_v2 import PyCrPwCrackLevel2V2
from gym_pycr_pwcrack.envs.config.level_2.pycr_pwcrack_level_2_v3 import PyCrPwCrackLevel2V3
from gym_pycr_pwcrack.envs.config.level_2.pycr_pwcrack_level_2_v4 import PyCrPwCrackLevel2V4
from gym_pycr_pwcrack.envs.config.level_3.pycr_pwcrack_level_3_base import PyCrPwCrackLevel3Base
from gym_pycr_pwcrack.envs.config.level_3.pycr_pwcrack_level_3_v1 import PyCrPwCrackLevel3V1
from gym_pycr_pwcrack.envs.config.level_3.pycr_pwcrack_level_3_v2 import PyCrPwCrackLevel3V2
from gym_pycr_pwcrack.envs.config.level_3.pycr_pwcrack_level_3_v3 import PyCrPwCrackLevel3V3
from gym_pycr_pwcrack.envs.config.level_3.pycr_pwcrack_level_3_v4 import PyCrPwCrackLevel3V4
from gym_pycr_pwcrack.envs.config.level_4.pycr_pwcrack_level_4_base import PyCrPwCrackLevel4Base
from gym_pycr_pwcrack.envs.config.level_4.pycr_pwcrack_level_4_v1 import PyCrPwCrackLevel4V1
from gym_pycr_pwcrack.envs.config.level_4.pycr_pwcrack_level_4_v2 import PyCrPwCrackLevel4V2
from gym_pycr_pwcrack.envs.config.level_4.pycr_pwcrack_level_4_v3 import PyCrPwCrackLevel4V3
from gym_pycr_pwcrack.envs.config.level_4.pycr_pwcrack_level_4_v4 import PyCrPwCrackLevel4V4
from gym_pycr_pwcrack.envs.config.level_5.pycr_pwcrack_level_5_base import PyCrPwCrackLevel5Base
from gym_pycr_pwcrack.envs.config.level_5.pycr_pwcrack_level_5_v1 import PyCrPwCrackLevel5V1
from gym_pycr_pwcrack.envs.config.level_5.pycr_pwcrack_level_5_v2 import PyCrPwCrackLevel5V2
from gym_pycr_pwcrack.envs.config.level_5.pycr_pwcrack_level_5_v3 import PyCrPwCrackLevel5V3
from gym_pycr_pwcrack.envs.config.level_5.pycr_pwcrack_level_5_v4 import PyCrPwCrackLevel5V4
from gym_pycr_pwcrack.envs.config.level_6.pycr_pwcrack_level_6_base import PyCrPwCrackLevel6Base
from gym_pycr_pwcrack.envs.config.level_6.pycr_pwcrack_level_6_v1 import PyCrPwCrackLevel6V1
from gym_pycr_pwcrack.envs.config.level_6.pycr_pwcrack_level_6_v2 import PyCrPwCrackLevel6V2
from gym_pycr_pwcrack.envs.config.level_6.pycr_pwcrack_level_6_v3 import PyCrPwCrackLevel6V3
from gym_pycr_pwcrack.envs.config.level_6.pycr_pwcrack_level_6_v4 import PyCrPwCrackLevel6V4
from gym_pycr_pwcrack.envs.config.level_7.pycr_pwcrack_level_7_base import PyCrPwCrackLevel7Base
from gym_pycr_pwcrack.envs.config.level_7.pycr_pwcrack_level_7_v1 import PyCrPwCrackLevel7V1
from gym_pycr_pwcrack.envs.config.level_7.pycr_pwcrack_level_7_v2 import PyCrPwCrackLevel7V2
from gym_pycr_pwcrack.envs.config.level_7.pycr_pwcrack_level_7_v3 import PyCrPwCrackLevel7V3
from gym_pycr_pwcrack.envs.config.level_7.pycr_pwcrack_level_7_v4 import PyCrPwCrackLevel7V4
from gym_pycr_pwcrack.envs.config.random.pycr_pwcrack_random_base import PyCrPwCrackRandomBase
from gym_pycr_pwcrack.envs.config.random.pycr_pwcrack_random_v1 import PyCrPwCrackRandomV1
from gym_pycr_pwcrack.envs.config.random.pycr_pwcrack_random_v2 import PyCrPwCrackRandomV2
from gym_pycr_pwcrack.envs.config.random.pycr_pwcrack_random_v3 import PyCrPwCrackRandomV3
from gym_pycr_pwcrack.envs.config.random.pycr_pwcrack_random_v4 import PyCrPwCrackRandomV4
from gym_pycr_pwcrack.envs.config.multi_sim.pycr_pwcrack_multisim_base import PyCrPwCrackMultiSimBase
from gym_pycr_pwcrack.envs.config.multi_sim.pycr_pwcrack_multisim_v1 import PyCrPwCrackMultiSimV1
from gym_pycr_pwcrack.envs.logic.common.env_dynamics_util import EnvDynamicsUtil
import gym_pycr_pwcrack.envs.logic.common.util as util
from gym_pycr_pwcrack.envs.logic.cluster.system_id.simulation_generator import SimulationGenerator
from gym_pycr_pwcrack.envs.logic.exploration.random_exploration_policy import RandomExplorationPolicy
from gym_pycr_pwcrack.envs.logic.cluster.warmup.cluster_warmup import ClusterWarmup
from gym_pycr_pwcrack.dao.container_config.containers_config import ContainersConfig
from gym_pycr_pwcrack.dao.container_config.flags_config import FlagsConfig
from gym_pycr_pwcrack.envs.logic.common.domain_randomizer import DomainRandomizer
from gym_pycr_pwcrack.envs.logic.simulation.find_pi_star import FindPiStar

class PyCRPwCrackEnv(gym.Env, ABC):
    """
    Abstract OpenAI Gym Env for the PyCr PwCrack minigame
    """

    def __init__(self, env_config : EnvConfig, rs = None):
        self.env_config = env_config
        if util.is_network_conf_incomplete(env_config) and self.env_config.env_mode == EnvMode.SIMULATION:
            raise ValueError("Must provide a simulation model to run in simulation mode")
        self.env_state = EnvState(network_config=self.env_config.network_conf, num_ports=self.env_config.num_ports,
                                  num_vuln=self.env_config.num_vuln, num_sh=self.env_config.num_sh,
                                  num_nodes=env_config.num_nodes,
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
        self.env_config.pi_star_rew_list = []
        self.reward_range = (float(0), float(1))
        self.num_states = 100
        self.idx = self.env_config.idx
        self.viewer = None
        self.randomization_space = rs
        self.steps_beyond_done = None
        self.metadata = {
            'render.modes': ['human', 'rgb_array'],
            'video.frames_per_second': 50  # Video rendering speed
        }
        self.step_outcome = None
        if self.env_config.env_mode == EnvMode.CLUSTER or self.env_config.env_mode == EnvMode.GENERATED_SIMULATION:
            self.env_config.cluster_config.connect_agent()
            if self.env_config.load_services_from_server:
                self.env_config.cluster_config.download_cluster_services()
            self.env_state.merge_services_with_cluster(self.env_config.cluster_config.cluster_services)
            if self.env_config.load_cves_from_server:
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
            self.env_config.action_alerts = self.env_config.cluster_config.load_action_alerts(
                actions=self.env_config.action_conf.actions, dir=self.env_config.nmap_cache_dir,
                action_ids=self.env_config.action_conf.action_ids,
                action_lookup_d_val=self.env_config.action_conf.action_lookup_d_val,
                shell_ids=self.env_config.action_conf.shell_action_ids)

        self.env_config.scale_rewards_prep()
        self.agent_state = AgentState(obs_state=self.env_state.obs_state, env_log=AgentLog(),
                                      service_lookup=self.env_state.service_lookup,
                                      vuln_lookup=self.env_state.vuln_lookup,
                                      os_lookup=self.env_state.os_lookup)
        self.last_obs = self.env_state.get_observation()
        self.trajectory = []
        self.trajectories = []
        if self.env_config.cluster_config is not None and self.env_config.cluster_config.warmup \
                and (self.env_config.env_mode == EnvMode.GENERATED_SIMULATION or self.env_config.env_mode == EnvMode.CLUSTER):
            ClusterWarmup.warmup(exp_policy=RandomExplorationPolicy(num_actions=env_config.action_conf.num_actions),
                                 num_warmup_steps=env_config.cluster_config.warmup_iterations,
                                 env=self, render = False)
            print("[Warmup complete], nmap_cache_size:{}, fs_cache_size:{}, user_command_cache:{}, nikto_scan_cache:{},"
                  "cache_misses:{}".format(
                len(self.env_config.nmap_scan_cache.cache), len(self.env_config.filesystem_scan_cache.cache),
                len(self.env_config.user_command_cache.cache), len(self.env_config.nikto_scan_cache.cache),
                self.env_config.cache_misses))
        if self.env_config.env_mode == EnvMode.GENERATED_SIMULATION and not self.env_config.cluster_config.skip_exploration:
            self.env_config.network_conf, obs_state = SimulationGenerator.build_model(exp_policy=env_config.exploration_policy,
                                                           env_config=self.env_config, env=self)
            self.env_state.obs_state = obs_state
            self.env_config.env_mode = EnvMode.SIMULATION
            self.randomization_space = DomainRandomizer.generate_randomization_space([self.env_config.network_conf])
            self.reset()
        self.reset()
        actions = list(range(self.num_actions))
        self.initial_illegal_actions = list(filter(lambda action: not PyCRPwCrackEnv.is_action_legal(
                    action, env_config=self.env_config, env_state=self.env_state), actions))
        if (self.env_config.env_mode == EnvMode.SIMULATION or self.env_config.env_mode == EnvMode.GENERATED_SIMULATION) \
                and self.env_config.compute_pi_star:
            if not self.env_config.use_upper_bound_pi_star:
                pi_star_tau, pi_star_rew = FindPiStar.brute_force(self.env_config, self)
                self.env_config.pi_star_tau = pi_star_tau
                self.env_config.pi_star_rew = pi_star_rew
                self.env_config.pi_star_rew_list.append(pi_star_rew)
        if self.env_config.use_upper_bound_pi_star:
            self.env_config.pi_star_rew = FindPiStar.upper_bound_pi(self.env_config)
            self.env_config.pi_star_tau = None
            self.env_config.pi_star_rew_list.append(self.env_config.pi_star_rew)

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
        info = {"idx": self.idx}
        if not self.is_action_legal(action_id, env_config=self.env_config, env_state=self.env_state):
            print("illegal action:{}, idx:{}".format(action_id, self.idx))
            actions = list(range(len(self.env_config.action_conf.actions)))
            non_legal_actions = list(filter(lambda action: not PyCRPwCrackEnv.is_action_legal(
                action, env_config=self.env_config, env_state=self.env_state), actions))
            print("true illegal actins:{}, idx:{}".format(non_legal_actions, self.idx))
            legal_actions = list(filter(lambda action: PyCRPwCrackEnv.is_action_legal(
                action, env_config=self.env_config, env_state=self.env_state), actions))
            print("true legal actions:{}, idx:{}".format(legal_actions, self.idx))
            print("flags found:{}, idx:{}".format(self.env_state.num_flags, self.idx))
            print("flags found:{}, idx:{}".format(list(map(lambda x: x.flags_found, self.env_state.obs_state.machines)), self.idx))
            print("flags found:{}, idx:{}".format(self.env_state.obs_state.catched_flags, self.idx))
            print("total flags:{}, idx:{}".format(self.env_config.network_conf.flags_lookup, self.idx))
            print(self.env_config.network_conf)
            print("Idx:{}".format(self.idx))
            #self.env_config.network_conf.save("./netconf" + str(self.idx) + ".pkl")
            raise ValueError("Test")
            sys.exit(0)
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
        self.__update_log(action)
        self.trajectory.append(m_obs)
        self.trajectory.append(reward)
        info["flags"] = self.env_state.obs_state.catched_flags
        if self.env_config.save_trajectories:
            self.trajectories.append(self.trajectory)

        return m_obs, reward, done, info

    def reset(self, soft : bool = False) -> np.ndarray:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :return: initial observation
        """
        # if self.agent_state.num_episodes % self.env_config.print_cache_details_freq == 0:
        #     print("[reset], nmap_cache_size:{}, fs_cache_size:{}, user_command_cache:{}, nikto_scan_cache:{},"
        #           "cache_misses:{}".format(
        #         len(self.env_config.nmap_scan_cache.cache), len(self.env_config.filesystem_scan_cache.cache),
        #         len(self.env_config.user_command_cache.cache), len(self.env_config.nikto_scan_cache.cache),
        #         self.env_config.cache_misses))
        # print("sott:{},env_mode:{},dr:{},rs:{}".format(soft, self.env_config.env_mode,
        #                                                self.env_config.domain_randomization,
        #                                                self.randomization_space))
        if not soft and self.env_config.env_mode == EnvMode.SIMULATION \
                and self.env_config.domain_randomization and self.randomization_space is not None:
            randomized_network_conf, env_config = DomainRandomizer.randomize(subnet_prefix="172.18.",
                                                                             network_ids=list(range(1, 254)),
                                                                             r_space=self.randomization_space,
                                                                             env_config=self.env_config)
            # print("randomize env, max num nodes:{}, max num flags:{}, ips:{}".format(
            #     self.randomization_space.max_num_nodes, self.randomization_space.max_num_flags,
            #     list(map(lambda x: x.ip, randomized_network_conf.nodes))))
            self.env_config = env_config
            if self.env_config.compute_pi_star:
                if not self.env_config.use_upper_bound_pi_star:
                    pi_star_tau, pi_star_rew = FindPiStar.brute_force(self.env_config, self)
                else:
                    pi_star_rew = FindPiStar.upper_bound_pi(self.env_config)
                    pi_star_tau = None
                self.env_config.pi_star_tau = pi_star_tau
                self.env_config.pi_star_rew = pi_star_rew
                self.env_config.pi_star_rew_list.append(pi_star_rew)
            actions = list(range(self.num_actions))
            self.initial_illegal_actions = list(filter(lambda action: not PyCRPwCrackEnv.is_action_legal(
                action, env_config=self.env_config, env_state=self.env_state), actions))

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
        #self.viewer.mainframe.set_state(self.agent_state)
        if self.viewer is not None and self.viewer.mainframe is not None:
            self.viewer.mainframe.reset_state()
        if self.env_config.env_mode == EnvMode.SIMULATION:
            self.env_state.obs_state.agent_reachable = self.env_config.network_conf.agent_reachable
        self.env_config.cache_misses = 0
        sys.stdout.flush()
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
        #self.agent_state.obs_state = self.env_state.obs_state.copy()
        self.agent_state.obs_state = self.env_state.obs_state
        if mode not in self.metadata["render.modes"]:
            raise NotImplemented("mode: {} is not supported".format(mode))
        if self.viewer is None:
            self.__setup_viewer()
        self.viewer.mainframe.set_state(self.agent_state)
        arr = self.viewer.render(return_rgb_array=mode == 'rgb_array')
        return arr

    def randomize(self):
        randomized_network_conf, env_config = DomainRandomizer.randomize(subnet_prefix="172.18.",
                                                                         network_ids=list(range(1, 254)),
                                                                         r_space=self.randomization_space,
                                                                         env_config=self.env_config)
        self.env_config = env_config
        actions = list(range(self.num_actions))
        self.initial_illegal_actions = list(filter(lambda action: not PyCRPwCrackEnv.is_action_legal(
            action, env_config=self.env_config, env_state=self.env_state), actions))

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

        # Recon on set of all found machines is always possible if there exists such machiens
        if action.type == ActionType.RECON and action.index == -1 and len(env_state.obs_state.machines) > 0:
            return True

        machine_discovered = False
        target_machine = None
        target_machines = []
        logged_in = False
        unscanned_filesystems = False
        untried_credentials = False
        root_login = False
        uninstalled_tools = False
        machine_w_tools = False
        uninstalled_backdoor = False

        for m in env_state.obs_state.machines:
            if m_index == -1:
                target_machines.append(m)
                machine_discovered = True

            if m.logged_in:
                logged_in = True
                if not m.filesystem_searched:
                    unscanned_filesystems = True
                if m.root:
                    root_login = True
                    if not m.tools_installed and not m.install_tools_tried:
                        uninstalled_tools = True
                    else:
                        machine_w_tools = True
                    if m.tools_installed and not m.backdoor_installed and not m.backdoor_tried:
                        uninstalled_backdoor = True
            if m.ip == ip:
                machine_discovered = True
                target_machine = m
            # if m.shell_access and not m.logged_in:
            #     untried_credentials = True
            if m.untried_credentials:
                untried_credentials = m.untried_credentials

        if action.subnet or action.id == ActionId.NETWORK_SERVICE_LOGIN:
            machine_discovered = True

        print("m_disc:{}, logged_in:{}, root_loing:{}, type:{}".format(machine_discovered, logged_in, root_login, action.type))

        # Privilege escalation only legal if machine discovered and logged in and not root
        if action.type == ActionType.PRIVILEGE_ESCALATION and (not machine_discovered or not logged_in or root_login):
            return False

        # If IP is discovered, then IP specific action without other prerequisites is legal
        if machine_discovered and (action.type == ActionType.RECON or action.type == ActionType.EXPLOIT
                                   or action.type == ActionType.PRIVILEGE_ESCALATION):
            if action.subnet and target_machine is None:
                return True
            if m_index == -1:
                exploit_tried = all(list(map(lambda x: env_state.obs_state.exploit_tried(a=action, m=x))))
            else:
                exploit_tried = env_state.obs_state.exploit_tried(a=action, m=target_machine)
            if exploit_tried:
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
        self.env_state.cleanup()
        if self.env_config.cluster_config is not None:
            self.env_config.cluster_config.close()
        # if self.env_config.env_mode == EnvMode.SIMULATION:
        #     return
        # else:
        #     self.env_state.cleanup()
        #     if self.env_config.cluster_config is not None:
        #         self.env_config.cluster_config.close()

    def convert_ar_action(self, machine_idx, action_idx):
        """
        Converts an AR action id into a global action id

        :param machine_idx: the machine id
        :param action_idx: the action id
        :return: the global action id
        """
        key = (machine_idx, action_idx)
        print(self.env_config.action_conf.ar_action_converter)
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

# -------- Difficulty 1 (Level1) ------------

# -------- Pre-defined Simulations ------------

# -------- Base Version (for testing) ------------
class PyCRPwCrackLevel1SimBaseEnv(PyCRPwCrackEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel1Base.render_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf()
            action_conf = PyCrPwCrackLevel1Base.all_actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                                 subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                                 hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1Base.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_conf=None, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.simulate_detection = True
            env_config.save_trajectories = False
            # env_config.simulate_detection = False
            env_config.env_mode = EnvMode.SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 1 ------------
class PyCRPwCrackLevel1Sim1Env(PyCRPwCrackEnv):
    """
    Simulation.
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel1Base.render_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf()
            action_conf = PyCrPwCrackLevel1V1.actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=None, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.save_trajectories = False
            env_config.filter_illegal_actions = True
            env_config.max_episode_length = 200
            env_config.simulate_detection = False
            env_config.base_detection_p = 0.0
            env_config.env_mode = EnvMode.SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.compute_pi_star = True
            env_config.use_upper_bound_pi_star = True
            env_config.domain_randomization = True
        super().__init__(env_config=env_config)


# -------- Version 1 with costs ------------
class PyCRPwCrackLevel1SimWithCosts1Env(PyCRPwCrackEnv):
    """
    Simulation.
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel1Base.render_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf()
            action_conf = PyCrPwCrackLevel1V1.actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=None, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 2 ------------
class PyCRPwCrackLevel1Sim2Env(PyCRPwCrackEnv):
    """
    Simulation.
    Slightly more set of actions than V1. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel1Base.render_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf()
            action_conf = PyCrPwCrackLevel1V2.actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=None, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 2, Costs ------------
class PyCRPwCrackLevel1SimWithCosts2Env(PyCRPwCrackEnv):
    """
    Simulation.
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel1Base.render_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf()
            action_conf = PyCrPwCrackLevel1V2.actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=None, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 3 ------------
class PyCRPwCrackLevel1Sim3Env(PyCRPwCrackEnv):
    """
    Simulation.
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel1Base.render_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf()
            action_conf = PyCrPwCrackLevel1V3.actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=None, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 3, Costs ------------
class PyCRPwCrackLevel1SimWithCosts3Env(PyCRPwCrackEnv):
    """
    Simulation.
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel1Base.render_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf()
            action_conf = PyCrPwCrackLevel1V3.actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=None, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 4 ------------
class PyCRPwCrackLevel1Sim4Env(PyCRPwCrackEnv):
    """
    Simulation.
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel1Base.render_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf()
            action_conf = PyCrPwCrackLevel1V4.actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=None, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 4, Costs ------------
class PyCRPwCrackLevel1SimWithCosts4Env(PyCRPwCrackEnv):
    """
    Simulation.
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel1Base.render_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf()
            action_conf = PyCrPwCrackLevel1V4.actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=None, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Generated Simulations ------------

# -------- Version 1 ------------
class PyCRPwCrackLevel1GeneratedSim1Env(PyCRPwCrackEnv):
    """
    Generated Simulation.
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel1Base.cluster_conf()
            render_config = PyCrPwCrackLevel1Base.render_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf(generate=True)
            action_conf = PyCrPwCrackLevel1V1.actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.action_conf.num_actions)
            env_config.exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.max_exploration_steps = 100
            env_config.max_exploration_trajectories = 10

        super().__init__(env_config=env_config)


# -------- Version 1, costs ------------
class PyCRPwCrackLevel1GeneratedSimWithCosts1Env(PyCRPwCrackEnv):
    """
    Generated Simulation.
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel1Base.cluster_conf()
            render_config = PyCrPwCrackLevel1Base.render_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf(generate=True)
            action_conf = PyCrPwCrackLevel1V1.actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.action_conf.num_actions)
            env_config.exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.max_exploration_steps = 100
            env_config.max_exploration_trajectories = 10

        super().__init__(env_config=env_config)


# -------- Version 2 ------------

class PyCRPwCrackLevel1GeneratedSim2Env(PyCRPwCrackEnv):
    """
    Generated simulation.
    Slightly more set of actions than V1. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel1Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel1Base.cluster_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf()
            action_conf = PyCrPwCrackLevel1V2.actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.action_conf.num_actions)
            env_config.exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.max_exploration_steps = 100
            env_config.max_exploration_trajectories = 10
        super().__init__(env_config=env_config)

# -------- Version 2, costs ------------

class PyCRPwCrackLevel1GeneratedSimWithCosts2Env(PyCRPwCrackEnv):
    """
    Generated simulation.
    Slightly more set of actions than V1. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel1Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel1Base.cluster_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf()
            action_conf = PyCrPwCrackLevel1V2.actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.action_conf.num_actions)
            env_config.exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.max_exploration_steps = 100
            env_config.max_exploration_trajectories = 10
        super().__init__(env_config=env_config)

# -------- Version 3 ------------

class PyCRPwCrackLevel1GeneratedSim3Env(PyCRPwCrackEnv):
    """
    Generated simulation.
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel1Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel1Base.cluster_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf()
            action_conf = PyCrPwCrackLevel1V3.actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.action_conf.num_actions)
            env_config.exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.max_exploration_steps = 100
            env_config.max_exploration_trajectories = 10
        super().__init__(env_config=env_config)

# -------- Version 3, costs ------------

class PyCRPwCrackLevel1GeneratedSimWithCosts3Env(PyCRPwCrackEnv):
    """
    Generated simulation.
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel1Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel1Base.cluster_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf()
            action_conf = PyCrPwCrackLevel1V3.actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.action_conf.num_actions)
            env_config.exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.max_exploration_steps = 100
            env_config.max_exploration_trajectories = 10
        super().__init__(env_config=env_config)


# -------- Version 4 ------------

class PyCRPwCrackLevel1GeneratedSim4Env(PyCRPwCrackEnv):
    """
    Generated simulation.
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel1Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel1Base.cluster_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf()
            action_conf = PyCrPwCrackLevel1V4.actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.action_conf.num_actions)
            env_config.exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.max_exploration_steps = 100
            env_config.max_exploration_trajectories = 10
        super().__init__(env_config=env_config)

# -------- Version 4 ------------

class PyCRPwCrackLevel1GeneratedSimWithCosts4Env(PyCRPwCrackEnv):
    """
    Generated simulation.
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel1Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel1Base.cluster_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf()
            action_conf = PyCrPwCrackLevel1V4.actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.action_conf.num_actions)
            env_config.exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.max_exploration_steps = 100
            env_config.max_exploration_trajectories = 10
        super().__init__(env_config=env_config)

# -------- Cluster ------------

# -------- Base Version (for testing) ------------

class PyCRPwCrackLevel1ClusterBaseEnv(PyCRPwCrackEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel1Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel1Base.cluster_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf()
            action_conf = PyCrPwCrackLevel1Base.all_actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                                 subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                                 hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1Base.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 1 ------------

class PyCRPwCrackLevel1Cluster1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel1Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel1Base.cluster_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf()
            action_conf = PyCrPwCrackLevel1V1.actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 1 No Cache ------------

class PyCRPwCrackLevel1ClusterNoCache1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    No cache
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel1Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel1Base.cluster_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf()
            action_conf = PyCrPwCrackLevel1NoCacheV1.actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                                  subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                                  hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1NoCacheV1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                               cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 1 With costs ------------

class PyCRPwCrackLevel1ClusterWithCosts1Env(PyCRPwCrackEnv):
    """
    Uses a minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel1Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel1Base.cluster_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf()
            action_conf = PyCrPwCrackLevel1V1.actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 2 ------------

class PyCRPwCrackLevel1Cluster2Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V1. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel1Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel1Base.cluster_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf()
            action_conf = PyCrPwCrackLevel1V2.actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 with Costs ------------

class PyCRPwCrackLevel1ClusterWithCosts2Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel1Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel1Base.cluster_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf()
            action_conf = PyCrPwCrackLevel1V2.actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 ------------

class PyCRPwCrackLevel1Cluster3Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel1Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel1Base.cluster_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf()
            action_conf = PyCrPwCrackLevel1V3.actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 with Costs ------------

class PyCRPwCrackLevel1ClusterWithCosts3Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel1Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel1Base.cluster_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf()
            action_conf = PyCrPwCrackLevel1V3.actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 ------------

class PyCRPwCrackLevel1Cluster4Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel1Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel1Base.cluster_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf()
            action_conf = PyCrPwCrackLevel1V4.actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 with costs ------------

class PyCRPwCrackLevel1ClusterWithCosts4Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel1Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel1Base.cluster_conf()
            network_conf = PyCrPwCrackLevel1Base.network_conf()
            action_conf = PyCrPwCrackLevel1V4.actions_conf(num_nodes=PyCrPwCrackLevel1Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel1Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel1Base.hacker_ip())
            env_config = PyCrPwCrackLevel1V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Difficulty 2 (Level2) ------------

# -------- Simulation ------------

# -------- Base Version (for testing) ------------
class PyCRPwCrackLevel2SimBaseEnv(PyCRPwCrackEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel2Base.render_conf()
            network_conf = PyCrPwCrackLevel2Base.network_conf()
            action_conf = PyCrPwCrackLevel2Base.all_actions_conf(num_nodes=PyCrPwCrackLevel2Base.num_nodes(),
                                                                 subnet_mask=PyCrPwCrackLevel2Base.subnet_mask(),
                                                                 hacker_ip=PyCrPwCrackLevel2Base.hacker_ip())
            env_config = PyCrPwCrackLevel2Base.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_conf=None, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.simulate_detection = True
            env_config.save_trajectories = False
            # env_config.simulate_detection = False
            env_config.env_mode = EnvMode.SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Simulations ------------

# -------- Version 1 ------------
class PyCRPwCrackLevel2Sim1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel2Base.render_conf()
            network_conf = PyCrPwCrackLevel2Base.network_conf()
            action_conf = PyCrPwCrackLevel2V1.actions_conf(num_nodes=PyCrPwCrackLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel2Base.hacker_ip())
            env_config = PyCrPwCrackLevel2V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=None, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 1, Costs ------------
class PyCRPwCrackLevel2SimWithCosts1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel2Base.render_conf()
            network_conf = PyCrPwCrackLevel2Base.network_conf()
            action_conf = PyCrPwCrackLevel2V1.actions_conf(num_nodes=PyCrPwCrackLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel2Base.hacker_ip())
            env_config = PyCrPwCrackLevel2V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=None, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Generated Simulations ------------

# -------- Version 1 ------------
class PyCRPwCrackLevel2GeneratedSim1Env(PyCRPwCrackEnv):
    """
    Generated Simulation
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel2Base.cluster_conf()
            render_config = PyCrPwCrackLevel2Base.render_conf()
            network_conf = PyCrPwCrackLevel2Base.network_conf(generate=True)
            action_conf = PyCrPwCrackLevel2V1.actions_conf(num_nodes=PyCrPwCrackLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel2Base.hacker_ip())
            env_config = PyCrPwCrackLevel2V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.action_conf.num_actions)
            env_config.exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.max_exploration_steps = 100
            env_config.max_exploration_trajectories = 10

        super().__init__(env_config=env_config)

# -------- Version 1, Costs ------------
class PyCRPwCrackLevel2GeneratedSimWithCosts1Env(PyCRPwCrackEnv):
    """
    Generated Simulation.
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel2Base.cluster_conf()
            render_config = PyCrPwCrackLevel2Base.render_conf()
            network_conf = PyCrPwCrackLevel2Base.network_conf(generate=True)
            action_conf = PyCrPwCrackLevel2V1.actions_conf(num_nodes=PyCrPwCrackLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel2Base.hacker_ip())
            env_config = PyCrPwCrackLevel2V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.action_conf.num_actions)
            env_config.exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.max_exploration_steps = 100
            env_config.max_exploration_trajectories = 10

        super().__init__(env_config=env_config)


# -------- Version 2 ------------
class PyCRPwCrackLevel2GeneratedSim2Env(PyCRPwCrackEnv):
    """
    Generated Simulation.
    Slightly more set of actions than V1. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel2Base.cluster_conf()
            render_config = PyCrPwCrackLevel2Base.render_conf()
            network_conf = PyCrPwCrackLevel2Base.network_conf(generate=True)
            action_conf = PyCrPwCrackLevel2V2.actions_conf(num_nodes=PyCrPwCrackLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel2Base.hacker_ip())
            env_config = PyCrPwCrackLevel2V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.action_conf.num_actions)
            env_config.exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.max_exploration_steps = 100
            env_config.max_exploration_trajectories = 10

        super().__init__(env_config=env_config)

# -------- Version 2, Costs ------------
class PyCRPwCrackLevel2GeneratedSimWithCosts2Env(PyCRPwCrackEnv):
    """
    Generated Simulation.
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel2Base.cluster_conf()
            render_config = PyCrPwCrackLevel2Base.render_conf()
            network_conf = PyCrPwCrackLevel2Base.network_conf(generate=True)
            action_conf = PyCrPwCrackLevel2V2.actions_conf(num_nodes=PyCrPwCrackLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel2Base.hacker_ip())
            env_config = PyCrPwCrackLevel2V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.action_conf.num_actions)
            env_config.exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.max_exploration_steps = 100
            env_config.max_exploration_trajectories = 10

        super().__init__(env_config=env_config)

# -------- Version 3 ------------
class PyCRPwCrackLevel2GeneratedSim3Env(PyCRPwCrackEnv):
    """
    Generated Simulation.
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel2Base.cluster_conf()
            render_config = PyCrPwCrackLevel2Base.render_conf()
            network_conf = PyCrPwCrackLevel2Base.network_conf(generate=True)
            action_conf = PyCrPwCrackLevel2V3.actions_conf(num_nodes=PyCrPwCrackLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel2Base.hacker_ip())
            env_config = PyCrPwCrackLevel2V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.action_conf.num_actions)
            env_config.exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.max_exploration_steps = 100
            env_config.max_exploration_trajectories = 10

        super().__init__(env_config=env_config)

# -------- Version 3, Costs ------------
class PyCRPwCrackLevel2GeneratedSimWithCosts3Env(PyCRPwCrackEnv):
    """
    Generated Simulation.
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel2Base.cluster_conf()
            render_config = PyCrPwCrackLevel2Base.render_conf()
            network_conf = PyCrPwCrackLevel2Base.network_conf(generate=True)
            action_conf = PyCrPwCrackLevel2V3.actions_conf(num_nodes=PyCrPwCrackLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel2Base.hacker_ip())
            env_config = PyCrPwCrackLevel2V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.action_conf.num_actions)
            env_config.exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.max_exploration_steps = 100
            env_config.max_exploration_trajectories = 10

        super().__init__(env_config=env_config)

# -------- Version 4 ------------
class PyCRPwCrackLevel2GeneratedSim4Env(PyCRPwCrackEnv):
    """
    Generated Simulation.
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel2Base.cluster_conf()
            render_config = PyCrPwCrackLevel2Base.render_conf()
            network_conf = PyCrPwCrackLevel2Base.network_conf(generate=True)
            action_conf = PyCrPwCrackLevel2V4.actions_conf(num_nodes=PyCrPwCrackLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel2Base.hacker_ip())
            env_config = PyCrPwCrackLevel2V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.action_conf.num_actions)
            env_config.exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.max_exploration_steps = 100
            env_config.max_exploration_trajectories = 10

        super().__init__(env_config=env_config)

# -------- Version 4 ------------
class PyCRPwCrackLevel2GeneratedSimWithCosts4Env(PyCRPwCrackEnv):
    """
    Generated Simulation.
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel2Base.cluster_conf()
            render_config = PyCrPwCrackLevel2Base.render_conf()
            network_conf = PyCrPwCrackLevel2Base.network_conf(generate=True)
            action_conf = PyCrPwCrackLevel2V4.actions_conf(num_nodes=PyCrPwCrackLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel2Base.hacker_ip())
            env_config = PyCrPwCrackLevel2V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.save_trajectories = False
            env_config.simulate_detection = False
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            exp_policy = RandomExplorationPolicy(num_actions=env_config.action_conf.num_actions)
            env_config.exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.max_exploration_steps = 100
            env_config.max_exploration_trajectories = 10

        super().__init__(env_config=env_config)

# -------- Cluster ------------

# -------- Base Version (for testing) ------------

class PyCRPwCrackLevel2ClusterBaseEnv(PyCRPwCrackEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel2Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel2Base.cluster_conf()
            network_conf = PyCrPwCrackLevel2Base.network_conf()
            action_conf = PyCrPwCrackLevel2Base.all_actions_conf(num_nodes=PyCrPwCrackLevel2Base.num_nodes(),
                                                                 subnet_mask=PyCrPwCrackLevel2Base.subnet_mask(),
                                                                 hacker_ip=PyCrPwCrackLevel2Base.hacker_ip())
            env_config = PyCrPwCrackLevel2Base.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 1 ------------

class PyCRPwCrackLevel2Cluster1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel2Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel2Base.cluster_conf()
            network_conf = PyCrPwCrackLevel2Base.network_conf()
            action_conf = PyCrPwCrackLevel2V1.actions_conf(num_nodes=PyCrPwCrackLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel2Base.hacker_ip())
            env_config = PyCrPwCrackLevel2V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 1 with costs ------------

class PyCRPwCrackLevel2ClusterWithCosts1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel2Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel2Base.cluster_conf()
            network_conf = PyCrPwCrackLevel2Base.network_conf()
            action_conf = PyCrPwCrackLevel2V1.actions_conf(num_nodes=PyCrPwCrackLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel2Base.hacker_ip())
            env_config = PyCrPwCrackLevel2V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 2 ------------

class PyCRPwCrackLevel2Cluster2Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V1. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel2Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel2Base.cluster_conf()
            network_conf = PyCrPwCrackLevel2Base.network_conf()
            action_conf = PyCrPwCrackLevel2V2.actions_conf(num_nodes=PyCrPwCrackLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel2Base.hacker_ip())
            env_config = PyCrPwCrackLevel2V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 with costs ------------

class PyCRPwCrackLevel2ClusterWithCosts2Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel2Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel2Base.cluster_conf()
            network_conf = PyCrPwCrackLevel2Base.network_conf()
            action_conf = PyCrPwCrackLevel2V2.actions_conf(num_nodes=PyCrPwCrackLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel2Base.hacker_ip())
            env_config = PyCrPwCrackLevel2V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 ------------

class PyCRPwCrackLevel2Cluster3Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel2Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel2Base.cluster_conf()
            network_conf = PyCrPwCrackLevel2Base.network_conf()
            action_conf = PyCrPwCrackLevel2V3.actions_conf(num_nodes=PyCrPwCrackLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel2Base.hacker_ip())
            env_config = PyCrPwCrackLevel2V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 with costs ------------

class PyCRPwCrackLevel2ClusterWithCosts3Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel2Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel2Base.cluster_conf()
            network_conf = PyCrPwCrackLevel2Base.network_conf()
            action_conf = PyCrPwCrackLevel2V3.actions_conf(num_nodes=PyCrPwCrackLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel2Base.hacker_ip())
            env_config = PyCrPwCrackLevel2V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 4 ------------

class PyCRPwCrackLevel2Cluster4Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel2Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel2Base.cluster_conf()
            network_conf = PyCrPwCrackLevel2Base.network_conf()
            action_conf = PyCrPwCrackLevel2V4.actions_conf(num_nodes=PyCrPwCrackLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel2Base.hacker_ip())
            env_config = PyCrPwCrackLevel2V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 4 with costs ------------

class PyCRPwCrackLevel2ClusterWithCosts4Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel2Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel2Base.cluster_conf()
            network_conf = PyCrPwCrackLevel2Base.network_conf()
            action_conf = PyCrPwCrackLevel2V4.actions_conf(num_nodes=PyCrPwCrackLevel2Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel2Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel2Base.hacker_ip())
            env_config = PyCrPwCrackLevel2V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Difficulty 3 (Level3) ------------

# -------- Base Version (for testing) ------------

class PyCRPwCrackLevel3ClusterBaseEnv(PyCRPwCrackEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel3Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel3Base.cluster_conf()
            network_conf = PyCrPwCrackLevel3Base.network_conf()
            action_conf = PyCrPwCrackLevel3Base.all_actions_conf(num_nodes=PyCrPwCrackLevel3Base.num_nodes(),
                                                                 subnet_mask=PyCrPwCrackLevel3Base.subnet_mask(),
                                                                 hacker_ip=PyCrPwCrackLevel3Base.hacker_ip())
            env_config = PyCrPwCrackLevel3Base.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 1 ------------

class PyCRPwCrackLevel3Cluster1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel3Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel3Base.cluster_conf()
            network_conf = PyCrPwCrackLevel3Base.network_conf()
            action_conf = PyCrPwCrackLevel3V1.actions_conf(num_nodes=PyCrPwCrackLevel3Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel3Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel3Base.hacker_ip())
            env_config = PyCrPwCrackLevel3V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 1 with costs ------------

class PyCRPwCrackLevel3ClusterWithCosts1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel3Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel3Base.cluster_conf()
            network_conf = PyCrPwCrackLevel3Base.network_conf()
            action_conf = PyCrPwCrackLevel3V1.actions_conf(num_nodes=PyCrPwCrackLevel3Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel3Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel3Base.hacker_ip())
            env_config = PyCrPwCrackLevel3V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 2 ------------

class PyCRPwCrackLevel3Cluster2Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V1. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel3Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel3Base.cluster_conf()
            network_conf = PyCrPwCrackLevel3Base.network_conf()
            action_conf = PyCrPwCrackLevel3V2.actions_conf(num_nodes=PyCrPwCrackLevel3Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel3Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel3Base.hacker_ip())
            env_config = PyCrPwCrackLevel3V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 with costs ------------

class PyCRPwCrackLevel3ClusterWithCosts2Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel3Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel3Base.cluster_conf()
            network_conf = PyCrPwCrackLevel3Base.network_conf()
            action_conf = PyCrPwCrackLevel3V2.actions_conf(num_nodes=PyCrPwCrackLevel3Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel3Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel3Base.hacker_ip())
            env_config = PyCrPwCrackLevel3V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 3 ------------

class PyCRPwCrackLevel3Cluster3Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel3Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel3Base.cluster_conf()
            network_conf = PyCrPwCrackLevel3Base.network_conf()
            action_conf = PyCrPwCrackLevel3V3.actions_conf(num_nodes=PyCrPwCrackLevel3Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel3Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel3Base.hacker_ip())
            env_config = PyCrPwCrackLevel3V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 3 ------------

class PyCRPwCrackLevel3ClusterWithCosts3Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel3Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel3Base.cluster_conf()
            network_conf = PyCrPwCrackLevel3Base.network_conf()
            action_conf = PyCrPwCrackLevel3V3.actions_conf(num_nodes=PyCrPwCrackLevel3Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel3Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel3Base.hacker_ip())
            env_config = PyCrPwCrackLevel3V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 4 ------------

class PyCRPwCrackLevel3Cluster4Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel3Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel3Base.cluster_conf()
            network_conf = PyCrPwCrackLevel3Base.network_conf()
            action_conf = PyCrPwCrackLevel3V4.actions_conf(num_nodes=PyCrPwCrackLevel3Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel3Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel3Base.hacker_ip())
            env_config = PyCrPwCrackLevel3V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 4 with costs------------

class PyCRPwCrackLevel3ClusterWithCosts4Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel3Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel3Base.cluster_conf()
            network_conf = PyCrPwCrackLevel3Base.network_conf()
            action_conf = PyCrPwCrackLevel3V4.actions_conf(num_nodes=PyCrPwCrackLevel3Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel3Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel3Base.hacker_ip())
            env_config = PyCrPwCrackLevel3V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Difficulty 4 (Level4) ------------

# -------- Cluster ------------

# -------- Base Version (for testing) ------------

class PyCRPwCrackLevel4ClusterBaseEnv(PyCRPwCrackEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel4Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel4Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel4Base.router_ip()
            network_conf = PyCrPwCrackLevel4Base.network_conf()
            action_conf = PyCrPwCrackLevel4Base.all_actions_conf(num_nodes=PyCrPwCrackLevel4Base.num_nodes(),
                                                                 subnet_mask=PyCrPwCrackLevel4Base.subnet_mask(),
                                                                 hacker_ip=PyCrPwCrackLevel4Base.hacker_ip())
            env_config = PyCrPwCrackLevel4Base.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 1 ------------

class PyCRPwCrackLevel4Cluster1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel4Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel4Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel4Base.router_ip()
            network_conf = PyCrPwCrackLevel4Base.network_conf()
            action_conf = PyCrPwCrackLevel4V1.actions_conf(num_nodes=PyCrPwCrackLevel4Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel4Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel4Base.hacker_ip())
            env_config = PyCrPwCrackLevel4V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 1 with costs------------

class PyCRPwCrackLevel4ClusterWithCosts1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel4Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel4Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel4Base.router_ip()
            network_conf = PyCrPwCrackLevel4Base.network_conf()
            action_conf = PyCrPwCrackLevel4V1.actions_conf(num_nodes=PyCrPwCrackLevel4Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel4Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel4Base.hacker_ip())
            env_config = PyCrPwCrackLevel4V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 ------------

class PyCRPwCrackLevel4Cluster2Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel4Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel4Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel4Base.router_ip()
            network_conf = PyCrPwCrackLevel4Base.network_conf()
            action_conf = PyCrPwCrackLevel4V2.actions_conf(num_nodes=PyCrPwCrackLevel4Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel4Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel4Base.hacker_ip())
            env_config = PyCrPwCrackLevel4V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 with costs------------

class PyCRPwCrackLevel4ClusterWithCosts2Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel4Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel4Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel4Base.router_ip()
            network_conf = PyCrPwCrackLevel4Base.network_conf()
            action_conf = PyCrPwCrackLevel4V2.actions_conf(num_nodes=PyCrPwCrackLevel4Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel4Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel4Base.hacker_ip())
            env_config = PyCrPwCrackLevel4V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 ------------

class PyCRPwCrackLevel4Cluster3Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel4Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel4Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel4Base.router_ip()
            network_conf = PyCrPwCrackLevel4Base.network_conf()
            action_conf = PyCrPwCrackLevel4V3.actions_conf(num_nodes=PyCrPwCrackLevel4Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel4Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel4Base.hacker_ip())
            env_config = PyCrPwCrackLevel4V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 with costs------------

class PyCRPwCrackLevel4ClusterWithCosts3Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel4Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel4Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel4Base.router_ip()
            network_conf = PyCrPwCrackLevel4Base.network_conf()
            action_conf = PyCrPwCrackLevel4V3.actions_conf(num_nodes=PyCrPwCrackLevel4Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel4Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel4Base.hacker_ip())
            env_config = PyCrPwCrackLevel4V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 ------------

class PyCRPwCrackLevel4Cluster4Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel4Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel4Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel4Base.router_ip()
            network_conf = PyCrPwCrackLevel4Base.network_conf()
            action_conf = PyCrPwCrackLevel4V4.actions_conf(num_nodes=PyCrPwCrackLevel4Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel4Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel4Base.hacker_ip())
            env_config = PyCrPwCrackLevel4V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 with costs------------

class PyCRPwCrackLevel4ClusterWithCosts4Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel4Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel4Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel4Base.router_ip()
            network_conf = PyCrPwCrackLevel4Base.network_conf()
            action_conf = PyCrPwCrackLevel4V4.actions_conf(num_nodes=PyCrPwCrackLevel4Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel4Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel4Base.hacker_ip())
            env_config = PyCrPwCrackLevel4V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Difficulty 5 (Level5) ------------

# -------- Cluster ------------

# -------- Base Version (for testing) ------------

class PyCRPwCrackLevel5ClusterBaseEnv(PyCRPwCrackEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel5Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel5Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel5Base.router_ip()
            network_conf = PyCrPwCrackLevel5Base.network_conf()
            action_conf = PyCrPwCrackLevel5Base.all_actions_conf(num_nodes=PyCrPwCrackLevel5Base.num_nodes(),
                                                                 subnet_mask=PyCrPwCrackLevel5Base.subnet_mask(),
                                                                 hacker_ip=PyCrPwCrackLevel5Base.hacker_ip())
            env_config = PyCrPwCrackLevel5Base.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 1 ------------

class PyCRPwCrackLevel5Cluster1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel5Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel5Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel5Base.router_ip()
            network_conf = PyCrPwCrackLevel5Base.network_conf()
            action_conf = PyCrPwCrackLevel5V1.actions_conf(num_nodes=PyCrPwCrackLevel5Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel5Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel5Base.hacker_ip())
            env_config = PyCrPwCrackLevel5V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 1 with costs------------

class PyCRPwCrackLevel5ClusterWithCosts1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel5Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel5Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel5Base.router_ip()
            network_conf = PyCrPwCrackLevel5Base.network_conf()
            action_conf = PyCrPwCrackLevel5V1.actions_conf(num_nodes=PyCrPwCrackLevel5Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel5Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel5Base.hacker_ip())
            env_config = PyCrPwCrackLevel5V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 ------------

class PyCRPwCrackLevel5Cluster2Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel5Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel5Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel5Base.router_ip()
            network_conf = PyCrPwCrackLevel5Base.network_conf()
            action_conf = PyCrPwCrackLevel5V2.actions_conf(num_nodes=PyCrPwCrackLevel5Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel5Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel5Base.hacker_ip())
            env_config = PyCrPwCrackLevel5V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 with costs------------

class PyCRPwCrackLevel5ClusterWithCosts2Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel5Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel5Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel5Base.router_ip()
            network_conf = PyCrPwCrackLevel5Base.network_conf()
            action_conf = PyCrPwCrackLevel5V2.actions_conf(num_nodes=PyCrPwCrackLevel5Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel5Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel5Base.hacker_ip())
            env_config = PyCrPwCrackLevel5V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 ------------

class PyCRPwCrackLevel5Cluster3Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel5Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel5Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel5Base.router_ip()
            network_conf = PyCrPwCrackLevel5Base.network_conf()
            action_conf = PyCrPwCrackLevel5V3.actions_conf(num_nodes=PyCrPwCrackLevel5Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel5Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel5Base.hacker_ip())
            env_config = PyCrPwCrackLevel5V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 with costs------------

class PyCRPwCrackLevel5ClusterWithCosts3Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel5Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel5Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel5Base.router_ip()
            network_conf = PyCrPwCrackLevel5Base.network_conf()
            action_conf = PyCrPwCrackLevel5V3.actions_conf(num_nodes=PyCrPwCrackLevel5Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel5Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel5Base.hacker_ip())
            env_config = PyCrPwCrackLevel5V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 ------------

class PyCRPwCrackLevel5Cluster4Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel5Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel5Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel5Base.router_ip()
            network_conf = PyCrPwCrackLevel5Base.network_conf()
            action_conf = PyCrPwCrackLevel5V4.actions_conf(num_nodes=PyCrPwCrackLevel5Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel5Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel5Base.hacker_ip())
            env_config = PyCrPwCrackLevel5V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 with costs------------

class PyCRPwCrackLevel5ClusterWithCosts4Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel5Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel5Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel5Base.router_ip()
            network_conf = PyCrPwCrackLevel5Base.network_conf()
            action_conf = PyCrPwCrackLevel5V4.actions_conf(num_nodes=PyCrPwCrackLevel5Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel5Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel5Base.hacker_ip())
            env_config = PyCrPwCrackLevel5V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Difficulty 6 (Level6) ------------

# -------- Cluster ------------

# -------- Base Version (for testing) ------------

class PyCRPwCrackLevel6ClusterBaseEnv(PyCRPwCrackEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel6Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel6Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel6Base.router_ip()
            network_conf = PyCrPwCrackLevel6Base.network_conf()
            action_conf = PyCrPwCrackLevel6Base.all_actions_conf(num_nodes=PyCrPwCrackLevel6Base.num_nodes(),
                                                                 subnet_mask=PyCrPwCrackLevel6Base.subnet_mask(),
                                                                 hacker_ip=PyCrPwCrackLevel6Base.hacker_ip())
            env_config = PyCrPwCrackLevel6Base.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 1 ------------

class PyCRPwCrackLevel6Cluster1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel6Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel6Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel6Base.router_ip()
            network_conf = PyCrPwCrackLevel6Base.network_conf()
            action_conf = PyCrPwCrackLevel6V1.actions_conf(num_nodes=PyCrPwCrackLevel6Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel6Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel6Base.hacker_ip())
            env_config = PyCrPwCrackLevel6V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.filter_illegal_actions = False
            env_config.max_episode_length = 100
        super().__init__(env_config=env_config)


# -------- Version 1 with costs------------

class PyCRPwCrackLevel6ClusterWithCosts1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel6Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel6Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel6Base.router_ip()
            network_conf = PyCrPwCrackLevel6Base.network_conf()
            action_conf = PyCrPwCrackLevel6V1.actions_conf(num_nodes=PyCrPwCrackLevel6Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel6Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel6Base.hacker_ip())
            env_config = PyCrPwCrackLevel6V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 ------------

class PyCRPwCrackLevel6Cluster2Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel6Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel6Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel6Base.router_ip()
            network_conf = PyCrPwCrackLevel6Base.network_conf()
            action_conf = PyCrPwCrackLevel6V2.actions_conf(num_nodes=PyCrPwCrackLevel6Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel6Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel6Base.hacker_ip())
            env_config = PyCrPwCrackLevel6V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 with costs------------

class PyCRPwCrackLevel6ClusterWithCosts2Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel6Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel6Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel6Base.router_ip()
            network_conf = PyCrPwCrackLevel6Base.network_conf()
            action_conf = PyCrPwCrackLevel6V2.actions_conf(num_nodes=PyCrPwCrackLevel6Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel6Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel6Base.hacker_ip())
            env_config = PyCrPwCrackLevel6V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 ------------

class PyCRPwCrackLevel6Cluster3Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel6Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel6Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel6Base.router_ip()
            network_conf = PyCrPwCrackLevel6Base.network_conf()
            action_conf = PyCrPwCrackLevel6V3.actions_conf(num_nodes=PyCrPwCrackLevel6Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel6Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel6Base.hacker_ip())
            env_config = PyCrPwCrackLevel6V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 with costs------------

class PyCRPwCrackLevel6ClusterWithCosts3Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel6Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel6Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel6Base.router_ip()
            network_conf = PyCrPwCrackLevel6Base.network_conf()
            action_conf = PyCrPwCrackLevel6V3.actions_conf(num_nodes=PyCrPwCrackLevel6Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel6Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel6Base.hacker_ip())
            env_config = PyCrPwCrackLevel6V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 ------------

class PyCRPwCrackLevel6Cluster4Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel6Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel6Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel6Base.router_ip()
            network_conf = PyCrPwCrackLevel6Base.network_conf()
            action_conf = PyCrPwCrackLevel6V4.actions_conf(num_nodes=PyCrPwCrackLevel6Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel6Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel6Base.hacker_ip())
            env_config = PyCrPwCrackLevel6V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 with costs------------

class PyCRPwCrackLevel6ClusterWithCosts4Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel6Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel6Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel6Base.router_ip()
            network_conf = PyCrPwCrackLevel6Base.network_conf()
            action_conf = PyCrPwCrackLevel6V4.actions_conf(num_nodes=PyCrPwCrackLevel6Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel6Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel6Base.hacker_ip())
            env_config = PyCrPwCrackLevel6V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Difficulty 7 (level7) -----------

# -------- Cluster ------------

# -------- Base Version (for testing) ------------

class PyCRPwCrackLevel7ClusterBaseEnv(PyCRPwCrackEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel7Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel7Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel7Base.router_ip()
            network_conf = PyCrPwCrackLevel7Base.network_conf()
            action_conf = PyCrPwCrackLevel7Base.all_actions_conf(num_nodes=PyCrPwCrackLevel7Base.num_nodes(),
                                                                 subnet_mask=PyCrPwCrackLevel7Base.subnet_mask(),
                                                                 hacker_ip=PyCrPwCrackLevel7Base.hacker_ip())
            env_config = PyCrPwCrackLevel7Base.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 1 ------------

class PyCRPwCrackLevel7Cluster1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel7Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel7Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel7Base.router_ip()
            network_conf = PyCrPwCrackLevel7Base.network_conf()
            action_conf = PyCrPwCrackLevel7V1.actions_conf(num_nodes=PyCrPwCrackLevel7Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel7Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel7Base.hacker_ip())
            env_config = PyCrPwCrackLevel7V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 1 with costs------------

class PyCRPwCrackLevel7ClusterWithCosts1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel7Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel7Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel7Base.router_ip()
            network_conf = PyCrPwCrackLevel7Base.network_conf()
            action_conf = PyCrPwCrackLevel7V1.actions_conf(num_nodes=PyCrPwCrackLevel7Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel7Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel7Base.hacker_ip())
            env_config = PyCrPwCrackLevel7V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 ------------

class PyCRPwCrackLevel7Cluster2Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel7Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel7Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel7Base.router_ip()
            network_conf = PyCrPwCrackLevel7Base.network_conf()
            action_conf = PyCrPwCrackLevel7V2.actions_conf(num_nodes=PyCrPwCrackLevel7Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel7Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel7Base.hacker_ip())
            env_config = PyCrPwCrackLevel7V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 with costs------------

class PyCRPwCrackLevel7ClusterWithCosts2Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel7Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel7Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel7Base.router_ip()
            network_conf = PyCrPwCrackLevel7Base.network_conf()
            action_conf = PyCrPwCrackLevel7V2.actions_conf(num_nodes=PyCrPwCrackLevel7Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel7Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel7Base.hacker_ip())
            env_config = PyCrPwCrackLevel7V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 ------------

class PyCRPwCrackLevel7Cluster3Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel7Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel7Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel7Base.router_ip()
            network_conf = PyCrPwCrackLevel7Base.network_conf()
            action_conf = PyCrPwCrackLevel7V3.actions_conf(num_nodes=PyCrPwCrackLevel7Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel7Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel7Base.hacker_ip())
            env_config = PyCrPwCrackLevel7V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 with costs------------

class PyCRPwCrackLevel7ClusterWithCosts3Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel7Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel7Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel7Base.router_ip()
            network_conf = PyCrPwCrackLevel7Base.network_conf()
            action_conf = PyCrPwCrackLevel7V3.actions_conf(num_nodes=PyCrPwCrackLevel7Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel7Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel7Base.hacker_ip())
            env_config = PyCrPwCrackLevel7V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 ------------

class PyCRPwCrackLevel7Cluster4Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel7Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel7Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel7Base.router_ip()
            network_conf = PyCrPwCrackLevel7Base.network_conf()
            action_conf = PyCrPwCrackLevel7V4.actions_conf(num_nodes=PyCrPwCrackLevel7Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel7Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel7Base.hacker_ip())
            env_config = PyCrPwCrackLevel7V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 with costs------------

class PyCRPwCrackLevel7ClusterWithCosts4Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrPwCrackLevel7Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrPwCrackLevel7Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrPwCrackLevel7Base.router_ip()
            network_conf = PyCrPwCrackLevel7Base.network_conf()
            action_conf = PyCrPwCrackLevel7V4.actions_conf(num_nodes=PyCrPwCrackLevel7Base.num_nodes(),
                                                           subnet_mask=PyCrPwCrackLevel7Base.subnet_mask(),
                                                           hacker_ip=PyCrPwCrackLevel7Base.hacker_ip())
            env_config = PyCrPwCrackLevel7V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Difficulty Random (Random) ------------

# -------- Cluster ------------

# -------- Base Version (for testing) ------------

class PyCRPwCrackRandomClusterBaseEnv(PyCRPwCrackEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrPwCrackRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrPwCrackRandomBase.all_actions_conf(num_nodes=num_nodes-1,
                                                                 subnet_mask=containers_config.subnet_mask,
                                                                 hacker_ip=containers_config.agent_ip)
            env_config = PyCrPwCrackRandomBase.env_config(containers_config=containers_config, flags_config=flags_config,
                                                          action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config,
                                                          num_nodes=num_nodes-1)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 1 ------------

class PyCRPwCrackRandomCluster1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrPwCrackRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrPwCrackRandomV1.actions_conf(num_nodes=num_nodes-1,
                                                                 subnet_mask=containers_config.subnet_mask,
                                                                 hacker_ip=containers_config.agent_ip)
            env_config = PyCrPwCrackRandomV1.env_config(containers_config=containers_config,
                                                          flags_config=flags_config,
                                                          action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config,
                                                          num_nodes=num_nodes-1)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.filter_illegal_actions = False
            env_config.max_episode_length = 50
        super().__init__(env_config=env_config)


# -------- Version 1 with costs------------

class PyCRPwCrackRandomClusterWithCosts1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrPwCrackRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrPwCrackRandomV1.actions_conf(num_nodes=num_nodes-1,
                                                           subnet_mask=containers_config.subnet_mask,
                                                           hacker_ip=containers_config.agent_ip)
            env_config = PyCrPwCrackRandomV1.env_config(containers_config=containers_config,
                                                        flags_config=flags_config,
                                                        action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config,
                                                        num_nodes=num_nodes-1)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)

# -------- Version 1 Generated Sim ------------

class PyCRPwCrackRandomGeneratedSim1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrPwCrackRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrPwCrackRandomV1.actions_conf(num_nodes=num_nodes-1,
                                                                 subnet_mask=containers_config.subnet_mask,
                                                                 hacker_ip=containers_config.agent_ip)
            env_config = PyCrPwCrackRandomV1.env_config(containers_config=containers_config,
                                                          flags_config=flags_config,
                                                          action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config,
                                                          num_nodes=num_nodes-1)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.filter_illegal_actions = False
            env_config.max_episode_length = 50
            exp_policy = RandomExplorationPolicy(num_actions=env_config.action_conf.num_actions)
            env_config.exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.exploration_filter_illegal = True
        super().__init__(env_config=env_config)

# -------- Version 1 Generated Sim With Costs ------------

class PyCRPwCrackRandomGeneratedSimWithCosts1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrPwCrackRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrPwCrackRandomV1.actions_conf(num_nodes=num_nodes-1,
                                                                 subnet_mask=containers_config.subnet_mask,
                                                                 hacker_ip=containers_config.agent_ip)
            env_config = PyCrPwCrackRandomV1.env_config(containers_config=containers_config,
                                                          flags_config=flags_config,
                                                          action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config,
                                                          num_nodes=num_nodes-1)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.filter_illegal_actions = False
            env_config.max_episode_length = 100
            exp_policy = RandomExplorationPolicy(num_actions=env_config.action_conf.num_actions)
            env_config.exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.exploration_filter_illegal = True
        super().__init__(env_config=env_config)

# -------- Version 2 ------------

class PyCRPwCrackRandomCluster2Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrPwCrackRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrPwCrackRandomV2.actions_conf(num_nodes=num_nodes-1,
                                                           subnet_mask=containers_config.subnet_mask,
                                                           hacker_ip=containers_config.agent_ip)
            env_config = PyCrPwCrackRandomV2.env_config(containers_config=containers_config,
                                                        flags_config=flags_config,
                                                        action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config,
                                                        num_nodes=num_nodes-1)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.filter_illegal_actions = False
            env_config.max_episode_length = 50
        super().__init__(env_config=env_config)


# -------- Version 2 with costs------------

class PyCRPwCrackRandomClusterWithCosts2Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrPwCrackRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrPwCrackRandomV2.actions_conf(num_nodes=num_nodes-1,
                                                           subnet_mask=containers_config.subnet_mask,
                                                           hacker_ip=containers_config.agent_ip)
            env_config = PyCrPwCrackRandomV2.env_config(containers_config=containers_config,
                                                        flags_config=flags_config,
                                                        action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config,
                                                        num_nodes=num_nodes-1)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.filter_illegal_actions = False
            env_config.max_episode_length = 50
        super().__init__(env_config=env_config)

# -------- Version 2 Generated Sim ------------

class PyCRPwCrackRandomGeneratedSim2Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrPwCrackRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrPwCrackRandomV2.actions_conf(num_nodes=num_nodes-1,
                                                           subnet_mask=containers_config.subnet_mask,
                                                           hacker_ip=containers_config.agent_ip)
            env_config = PyCrPwCrackRandomV2.env_config(containers_config=containers_config,
                                                        flags_config=flags_config,
                                                        action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config,
                                                        num_nodes=num_nodes-1)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            exp_policy = RandomExplorationPolicy(num_actions=env_config.action_conf.num_actions)
            env_config.exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.exploration_filter_illegal = True
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.filter_illegal_actions = False
            env_config.max_episode_length = 50
        super().__init__(env_config=env_config)

# -------- Version 2 Generated Sim With Costs ------------

class PyCRPwCrackRandomGeneratedSimWithCosts2Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrPwCrackRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrPwCrackRandomV2.actions_conf(num_nodes=num_nodes-1,
                                                           subnet_mask=containers_config.subnet_mask,
                                                           hacker_ip=containers_config.agent_ip)
            env_config = PyCrPwCrackRandomV2.env_config(containers_config=containers_config,
                                                        flags_config=flags_config,
                                                        action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config,
                                                        num_nodes=num_nodes-1)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            exp_policy = RandomExplorationPolicy(num_actions=env_config.action_conf.num_actions)
            env_config.exploration_filter_illegal = True
            env_config.exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.filter_illegal_actions = False
            env_config.max_episode_length = 50
        super().__init__(env_config=env_config)

# -------- Version 3 ------------

class PyCRPwCrackRandomCluster3Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrPwCrackRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrPwCrackRandomV3.actions_conf(num_nodes=num_nodes-1,
                                                           subnet_mask=containers_config.subnet_mask,
                                                           hacker_ip=containers_config.agent_ip)
            env_config = PyCrPwCrackRandomV3.env_config(containers_config=containers_config,
                                                        flags_config=flags_config,
                                                        action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config,
                                                        num_nodes=num_nodes-1)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.filter_illegal_actions = False
            env_config.max_episode_length = 50
        super().__init__(env_config=env_config)

# -------- Version 3 with costs------------

class PyCRPwCrackRandomClusterWithCosts3Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrPwCrackRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrPwCrackRandomV3.actions_conf(num_nodes=num_nodes-1,
                                                           subnet_mask=containers_config.subnet_mask,
                                                           hacker_ip=containers_config.agent_ip)
            env_config = PyCrPwCrackRandomV3.env_config(containers_config=containers_config,
                                                        flags_config=flags_config,
                                                        action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config,
                                                        num_nodes=num_nodes-1)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.filter_illegal_actions = False
            env_config.max_episode_length = 50
        super().__init__(env_config=env_config)

# -------- Version 3, Generated Simulation ------------
class PyCRPwCrackRandomGeneratedSim3Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrPwCrackRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrPwCrackRandomV3.actions_conf(num_nodes=num_nodes-1,
                                                           subnet_mask=containers_config.subnet_mask,
                                                           hacker_ip=containers_config.agent_ip)
            env_config = PyCrPwCrackRandomV3.env_config(containers_config=containers_config,
                                                        flags_config=flags_config,
                                                        action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config,
                                                        num_nodes=num_nodes-1)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            exp_policy = RandomExplorationPolicy(num_actions=env_config.action_conf.num_actions)
            env_config.exploration_filter_illegal = True
            env_config.exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.filter_illegal_actions = False
            env_config.max_episode_length = 50
        super().__init__(env_config=env_config)

# -------- Version 3, Generated Simulation With Costs ------------
class PyCRPwCrackRandomGeneratedSimWithCosts3Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrPwCrackRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrPwCrackRandomV3.actions_conf(num_nodes=num_nodes-1,
                                                           subnet_mask=containers_config.subnet_mask,
                                                           hacker_ip=containers_config.agent_ip)
            env_config = PyCrPwCrackRandomV3.env_config(containers_config=containers_config,
                                                        flags_config=flags_config,
                                                        action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config,
                                                        num_nodes=num_nodes-1)
            env_config.cost_coefficient = 1
            env_config.alerts_coefficient = 1
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            exp_policy = RandomExplorationPolicy(num_actions=env_config.action_conf.num_actions)
            env_config.exploration_filter_illegal = True
            env_config.exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.filter_illegal_actions = False
            env_config.max_episode_length = 50
        super().__init__(env_config=env_config)

# -------- Version 4 ------------
class PyCRPwCrackRandomCluster4Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrPwCrackRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrPwCrackRandomV4.actions_conf(num_nodes= num_nodes-1,
                                                           subnet_mask=containers_config.subnet_mask,
                                                           hacker_ip=containers_config.agent_ip)
            env_config = PyCrPwCrackRandomV4.env_config(containers_config=containers_config,
                                                        flags_config=flags_config,
                                                        action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config,
                                                        num_nodes=num_nodes-1)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.filter_illegal_actions = False
            env_config.max_episode_length = 50
        super().__init__(env_config=env_config)


# -------- Version 4 with costs------------
class PyCRPwCrackRandomClusterWithCosts4Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrPwCrackRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrPwCrackRandomV4.actions_conf(num_nodes=num_nodes-1,
                                                           subnet_mask=containers_config.subnet_mask,
                                                           hacker_ip=containers_config.agent_ip)
            env_config = PyCrPwCrackRandomV4.env_config(containers_config=containers_config,
                                                        flags_config=flags_config,
                                                        action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config,
                                                        num_nodes=num_nodes-1)
            env_config.cost_coefficient = 1
            env_config.alerts_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.filter_illegal_actions = False
            env_config.max_episode_length = 50
        super().__init__(env_config=env_config)


# -------- Version 4, Generated Simulation ------------
class PyCRPwCrackRandomGeneratedSim4Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """

    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir: str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes: int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrPwCrackRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrPwCrackRandomV4.actions_conf(num_nodes=num_nodes - 1,
                                                           subnet_mask=containers_config.subnet_mask,
                                                           hacker_ip=containers_config.agent_ip)
            env_config = PyCrPwCrackRandomV4.env_config(containers_config=containers_config,
                                                        flags_config=flags_config,
                                                        action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config,
                                                        num_nodes=num_nodes - 1)
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            exp_policy = RandomExplorationPolicy(num_actions=env_config.action_conf.num_actions)
            env_config.exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.exploration_filter_illegal = True
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.filter_illegal_actions = False
            env_config.max_episode_length = 50
        super().__init__(env_config=env_config)

# -------- Version 4, Generated Simulation, With Costs------------
class PyCRPwCrackRandomGeneratedSimWithCosts4Env(PyCRPwCrackEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """

    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir: str,
                 containers_config: ContainersConfig, flags_config: FlagsConfig, num_nodes: int = -1):
        if num_nodes == -1:
            num_nodes = len(containers_config.containers)
        if env_config is None:
            render_config = PyCrPwCrackRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrPwCrackRandomV4.actions_conf(num_nodes=num_nodes - 1,
                                                           subnet_mask=containers_config.subnet_mask,
                                                           hacker_ip=containers_config.agent_ip)
            env_config = PyCrPwCrackRandomV4.env_config(containers_config=containers_config,
                                                        flags_config=flags_config,
                                                        action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config,
                                                        num_nodes=num_nodes - 1)
            env_config.cost_coefficient = 1
            env_config.alerts_coefficient = 1
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            exp_policy = RandomExplorationPolicy(num_actions=env_config.action_conf.num_actions)
            env_config.exploration_filter_illegal = True
            env_config.exploration_policy = exp_policy
            env_config.domain_randomization = False
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.filter_illegal_actions = False
            env_config.max_episode_length = 50
            env_config.compute_pi_star = False
            env_config.use_upper_bound_pi_star = True
        super().__init__(env_config=env_config)

# -------- Difficulty RandomMany (RandomMany) ------------

# -------- Cluster ------------

# -------- Base Version (for testing) ------------

# -------- Version 1 Cluster ------------


class PyCRPwCrackRandomManyCluster1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_configs: List[ContainersConfig], flags_configs: List[FlagsConfig], idx : int,
                 num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = max(list(map(lambda x: len(x.containers), containers_configs)))
        containers_config = containers_configs[idx]
        flags_config = flags_configs[idx]
        if env_config is None:
            render_config = PyCrPwCrackRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrPwCrackRandomV1.actions_conf(num_nodes=num_nodes-1,
                                                                 subnet_mask=containers_config.subnet_mask,
                                                                 hacker_ip=containers_config.agent_ip)
            env_config = PyCrPwCrackRandomV1.env_config(containers_config=containers_config,
                                                          flags_config=flags_config,
                                                          action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config,
                                                          num_nodes=num_nodes-1)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.idx = idx
            env_config.filter_illegal_actions = True
            env_config.max_episode_length = 200
            env_config.simulate_detection = False
            env_config.domain_randomization = False
            env_config.compute_pi_star = True
            env_config.use_upper_bound_pi_star = True
        super().__init__(env_config=env_config)


# -------- Version 1 With Costs ------------

class PyCRPwCrackRandomManyClusterWithCosts1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_configs: List[ContainersConfig], flags_configs: List[FlagsConfig], idx : int,
                 num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = max(list(map(lambda x: len(x.containers), containers_configs)))
        containers_config = containers_configs[idx]
        flags_config = flags_configs[idx]
        if env_config is None:
            render_config = PyCrPwCrackRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrPwCrackRandomV1.actions_conf(num_nodes=num_nodes-1,
                                                                 subnet_mask=containers_config.subnet_mask,
                                                                 hacker_ip=containers_config.agent_ip)
            env_config = PyCrPwCrackRandomV1.env_config(containers_config=containers_config,
                                                          flags_config=flags_config,
                                                          action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config,
                                                          num_nodes=num_nodes-1)
            env_config.cost_coefficient = 1
            env_config.alerts_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.idx=idx
            env_config.filter_illegal_actions = True
            env_config.max_episode_length = 200
            env_config.compute_pi_star = False
            env_config.use_upper_bound_pi_star = True
        super().__init__(env_config=env_config)


# -------- Version 1 Generated Sim ------------

class PyCRPwCrackRandomManyGeneratedSim1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 containers_configs: List[ContainersConfig], flags_configs: List[FlagsConfig], idx : int,
                 num_nodes : int = -1):
        if num_nodes == -1:
            num_nodes = max(list(map(lambda x: len(x.containers), containers_configs)))
        containers_config = containers_configs[idx]
        flags_config = flags_configs[idx]
        if env_config is None:
            render_config = PyCrPwCrackRandomBase.render_conf(containers_config=containers_config)
            if cluster_config is None:
                raise ValueError("Cluster config cannot be None")
            cluster_config.ids_router = containers_config.ids_enabled
            cluster_config.ids_router_ip = containers_config.router_ip
            action_conf = PyCrPwCrackRandomV1.actions_conf(num_nodes=num_nodes-1,
                                                                 subnet_mask=containers_config.subnet_mask,
                                                                 hacker_ip=containers_config.agent_ip)
            env_config = PyCrPwCrackRandomV1.env_config(containers_config=containers_config,
                                                          flags_config=flags_config,
                                                          action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config,
                                                          num_nodes=num_nodes-1)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.GENERATED_SIMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.idx=idx
            env_config.filter_illegal_actions = True
            env_config.max_episode_length = 200
            exp_policy = RandomExplorationPolicy(num_actions=env_config.action_conf.num_actions)
            env_config.exploration_filter_illegal = env_config.filter_illegal_actions
            env_config.simulate_detection = False
            env_config.exploration_policy = exp_policy
            env_config.domain_randomization = True
            env_config.max_exploration_steps = 1000
            env_config.max_exploration_trajectories = 100
            env_config.compute_pi_star = True
            env_config.use_upper_bound_pi_star = True
        super().__init__(env_config=env_config)


# -------- Difficulty MultiSim (MultiSim) ------------

# -------- Cluster ------------

# -------- Base Version (for testing) ------------

# -------- Version 1 Cluster ------------


class PyCRPwCrackMultiSim1Env(PyCRPwCrackEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str,
                 idx: int = -1, dr_max_num_nodes : int = 10, dr_min_num_nodes : int  = 4, dr_max_num_flags = 3,
                 dr_min_num_flags : int = 1, dr_min_num_users :int = 2, dr_max_num_users : int = 5):
        if env_config is None:
            render_config = PyCrPwCrackMultiSimBase.render_conf(num_nodes=dr_max_num_nodes)
            randomization_space = DomainRandomizer.generate_randomization_space(
                [], max_num_nodes=dr_max_num_nodes,
                min_num_nodes=dr_min_num_nodes, max_num_flags=dr_max_num_flags,
                min_num_flags=dr_min_num_flags, min_num_users=dr_min_num_users,
                max_num_users=dr_max_num_users,
                use_base_randomization=True)
            self.randomization_space = randomization_space
            action_conf = PyCrPwCrackMultiSimV1.actions_conf(num_nodes=dr_max_num_nodes-1,
                                                                 subnet_mask="172.18.2.0/24",
                                                                 hacker_ip="172.18.2.191")
            env_config = PyCrPwCrackMultiSimV1.env_config(action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config,
                                                          num_nodes=dr_max_num_nodes-1)
            env_config.domain_randomization = True
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.SIMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.idx=idx
            env_config.filter_illegal_actions = True
            env_config.max_episode_length = 200
            env_config.compute_pi_star = True
            env_config.use_upper_bound_pi_star = True
            randomized_network_conf, env_config = DomainRandomizer.randomize(subnet_prefix="172.18.",
                                                                             network_ids=list(range(1, 254)),
                                                                             r_space=self.randomization_space,
                                                                             env_config=env_config)
        super().__init__(env_config=env_config, rs=randomization_space)