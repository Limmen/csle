from typing import Tuple
import gym
import pickle
from abc import ABC
import numpy as np
import os
import sys
import time
import random
from pycr_common import AgentLog
from pycr_common.dao.network import EnvMode
from pycr_common import RandomExplorationPolicy
from pycr_common.envs_model.logic.emulation.warmup import EmulationWarmup
from pycr_common import InitialStateRandomizer
import pycr_common as constants
import pycr_common.envs_model.logic.common.util as util
from pycr_common import BasePyCREnv
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.agent.attacker_agent_state import AttackerAgentState
from gym_pycr_ctf.dao.network.env_state import EnvState
from gym_pycr_ctf.envs_model.logic.emulation.system_id.simulation_generator import SimulationGenerator
from gym_pycr_ctf.envs_model.logic.transition_operator import TransitionOperator
from gym_pycr_ctf.dao.action.attacker.attacker_action import AttackerAction
from gym_pycr_ctf.envs_model.logic.common.env_dynamics_util import EnvDynamicsUtil
from gym_pycr_ctf.envs_model.logic.common.domain_randomizer import DomainRandomizer
from gym_pycr_ctf.envs_model.logic.simulation.find_pi_star_attacker import FindPiStarAttacker
from gym_pycr_ctf.envs_model.logic.simulation.find_pi_star_defender import FindPiStarDefender
from gym_pycr_ctf.envs_model.logic.common.stopping_baselines_util import StoppingBaselinesUtil
from gym_pycr_ctf.envs_model.util.env_util import EnvUtil
from gym_pycr_ctf.dao.action.defender.defender_action_id import DefenderActionId


class PyCRCTFEnv(gym.Env, ABC, BasePyCREnv):
    """
    Abstract OpenAI Gym Env for the PyCr CTF minigame
    """

    def __init__(self, env_config : EnvConfig, rs = None):
        self.env_config = env_config
        if util.is_network_conf_incomplete(env_config.network_conf) and self.env_config.env_mode == EnvMode.SIMULATION:
            raise ValueError("Must provide a simulation model to run in simulation mode")

        # Initialize environment state
        self.env_state = EnvState(env_config=self.env_config, num_ports=self.env_config.attacker_num_ports_obs,
                                  num_vuln=self.env_config.attacker_num_vuln_obs,
                                  num_sh=self.env_config.attacker_num_sh_obs,
                                  num_nodes=env_config.num_nodes,
                                  service_lookup=constants.SERVICES.service_lookup,
                                  vuln_lookup=constants.VULNERABILITIES.vuln_lookup,
                                  os_lookup=constants.OS.os_lookup, num_flags=self.env_config.num_flags,
                                  state_type=self.env_config.state_type,
                                  ids=env_config.ids_router)

        # Setup Attacker Spaces
        self.attacker_observation_space = self.env_state.attacker_observation_space
        self.attacker_m_selection_observation_space = self.env_state.attacker_m_selection_observation_space
        self.attacker_m_action_observation_space = self.env_state.attacker_m_action_observation_space
        self.attacker_action_space = self.env_config.attacker_action_conf.action_space
        self.attacker_m_selection_action_space = gym.spaces.Discrete(self.env_state.attacker_obs_state.num_machines + 1)
        self.attacker_m_action_space = self.env_config.attacker_action_conf.m_action_space
        self.attacker_num_actions = self.env_config.attacker_action_conf.num_actions
        self.attacker_network_orig_shape = self.env_state.attacker_network_orig_shape
        self.attacker_machine_orig_shape = self.env_state.attacker_machine_orig_shape

        # Setup Defender Spaces
        self.defender_observation_space = self.env_state.defender_observation_space
        self.defender_action_space = self.env_config.defender_action_conf.action_space
        self.defender_num_actions = self.env_config.defender_action_conf.num_actions

        # Setup Config
        self.env_config.pi_star_rew_list_attacker = []
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



        # System Identification
        if self.env_config.env_mode == EnvMode.EMULATION or self.env_config.env_mode == EnvMode.GENERATED_SIMULATION:

            # Connect to emulation
            self.env_config.emulation_config.connect_agent()

            if self.env_config.env_mode == EnvMode.EMULATION and self.env_config.defender_update_state:
                # Initialize Defender's state
                defender_init_action = self.env_config.defender_action_conf.state_init_action
                s_prime, _, _ = TransitionOperator.defender_transition(s=self.env_state, defender_action=defender_init_action,
                                                       env_config=self.env_config)
                self.env_state = s_prime
                self.env_config.network_conf.defender_dynamics_model.normalize()

            if self.env_config.load_services_from_server:
                self.env_config.emulation_config.download_emulation_services()
            self.env_state.merge_services_with_emulation(self.env_config.emulation_config.emulation_services)
            if self.env_config.load_cves_from_server:
                self.env_config.emulation_config.download_cves()
            self.env_state.merge_cves_with_emulation(self.env_config.emulation_config.emulation_cves)
            self.env_config.attacker_action_costs = self.env_config.emulation_config.load_action_costs(
                actions=self.env_config.attacker_action_conf.actions, dir=self.env_config.nmap_cache_dir,
                nmap_ids=self.env_config.attacker_action_conf.nmap_action_ids,
                network_service_ids=self.env_config.attacker_action_conf.network_service_action_ids,
                shell_ids=self.env_config.attacker_action_conf.shell_action_ids,
                nikto_ids=self.env_config.attacker_action_conf.nikto_action_ids,
                masscan_ids=self.env_config.attacker_action_conf.masscan_action_ids,
                action_lookup_d_val = self.env_config.attacker_action_conf.action_lookup_d_val)
            self.env_config.attacker_action_alerts = self.env_config.emulation_config.load_action_alerts(
                actions=self.env_config.attacker_action_conf.actions, dir=self.env_config.nmap_cache_dir,
                action_ids=self.env_config.attacker_action_conf.action_ids,
                action_lookup_d_val=self.env_config.attacker_action_conf.action_lookup_d_val,
                shell_ids=self.env_config.attacker_action_conf.shell_action_ids)

        if self.env_config.env_mode == EnvMode.GENERATED_SIMULATION \
                and self.env_config.emulation_config.skip_exploration:
            self.load_dynamics_model()

        self.env_config.scale_rewards_prep_attacker()
        self.env_config.scale_rewards_prep_defender()
        self.attacker_agent_state = AttackerAgentState(attacker_obs_state=self.env_state.attacker_obs_state,
                                                       env_log=AgentLog(),
                                                       service_lookup=self.env_state.service_lookup,
                                                       vuln_lookup=self.env_state.vuln_lookup,
                                                       os_lookup=self.env_state.os_lookup)

        # Setup Attacker Trajectories
        self.attacker_last_obs = self.env_state.get_attacker_observation()
        self.attacker_trajectory = []
        self.attacker_trajectories = []

        # Setup Defender Trajectories
        self.defender_last_obs = self.env_state.get_attacker_observation()
        self.defender_trajectory = []
        self.defender_trajectories = []
        self.defender_time_step = 1

        # Reset and setup action spaces
        self.reset()
        attacker_actions = list(range(self.attacker_num_actions))
        self.attacker_initial_illegal_actions = list(filter(lambda action: not PyCRCTFEnv.is_attack_action_legal(
                    action, env_config=self.env_config, env_state=self.env_state), attacker_actions))
        defender_actions = list(range(self.defender_num_actions))
        self.defender_initial_illegal_actions = list(filter(lambda action: not PyCRCTFEnv.is_defense_action_legal(
            action, env_config=self.env_config, env_state=self.env_state), defender_actions))

        # Fix upper bounds for evaluation
        self.env_config = FindPiStarAttacker.update_pi_star(self.env_config, self)

    # -------- API ------------
    def step(self, action_id : Tuple[int, int]) -> Tuple[Tuple[np.ndarray, np.ndarray], Tuple[int, int], bool, dict]:
        """
        Takes a step in the environment by executing the given action

        :param action_id: the action to take
        :return: (obs, reward, done, info)
        """
        if isinstance(action_id, int) or isinstance(action_id, np.int64):
            action_id = (action_id, None)
            print("[WARNING]: This is a multi-agent environment where the input should be "
                  "(attacker_action, defender_action)")
        # Initialization
        attack_action_id, defense_action_id = action_id
        static_attack_started = False
        attacker_done = False
        if (attack_action_id == -1 or attack_action_id is None) and self.env_config.attacker_static_opponent is not None:
            attack_action_id, attacker_done = self.env_config.attacker_static_opponent.action(
                env=self, filter_illegal=self.env_config.attacker_filter_illegal_actions)
            if self.env_config.attacker_static_opponent.started:
                static_attack_started = True

        if attack_action_id is not None:
            attack_action_id = int(attack_action_id)
        if defense_action_id is not None:
            defense_action_id = int(defense_action_id)
        defender_reward = 0
        defender_info = None
        attacker_reward = 0
        done = False
        info = None

        defender_info = PyCRCTFEnv.initialize_info_dict()

        # First step defender
        if defense_action_id is not None:
            if (self.env_config.env_mode == EnvMode.EMULATION
                    or self.env_config.env_mode == EnvMode.GENERATED_SIMULATION) \
                    and not self.env_config.use_attacker_action_stats_to_update_defender_state:
                time.sleep(self.env_config.defender_sleep_before_state_update)
            defender_reward, attacker_reward, done, defender_info = \
                self.step_defender(defender_action_id=defense_action_id,
                                   attacker_action=self.env_state.attacker_obs_state.last_attacker_action,
                                   attacker_opponent=self.env_config.attacker_static_opponent)
            attacker_reward = attacker_reward
        else:
            print("defender action is none")

        defender_info[constants.INFO_DICT.SUCCESSFUL_INTRUSION] = False
        defender_info[constants.INFO_DICT.ATTACKER_COST] = self.env_state.attacker_obs_state.cost
        defender_info[constants.INFO_DICT.ATTACKER_COST_NORM] = self.env_state.attacker_obs_state.cost_norm
        defender_info[constants.INFO_DICT.ATTACKER_ALERTS] = self.env_state.attacker_obs_state.alerts
        defender_info[constants.INFO_DICT.ATTACKER_ALERTS_NORM] = self.env_state.attacker_obs_state.alerts_norm
        defender_info[constants.INFO_DICT.FLAGS] = 0
        defender_info[constants.INFO_DICT.EPISODE_LENGTH] = self.env_state.defender_obs_state.step

        if not done:

            # Second step attacker
            attacker_reward, done, info = self.step_attacker(attacker_action_id=attack_action_id)
            if done:
                print("attacker done? {}, action:{}".format(attack_action_id))
            done = done or attacker_done
            self.env_state.attacker_obs_state.intrusion_started = self.env_state.attacker_obs_state.intrusion_started \
                                                                  or static_attack_started

        if done:
            self.env_state.attacker_obs_state.intrusion_completed = True
            if self.env_state.defender_obs_state.caught_attacker:
                defense_action = self.env_config.defender_action_conf.actions[defense_action_id]
                if defense_action.id == DefenderActionId.CONTINUE:
                    defender_reward = 0
                # defender_reward = defender_reward + self.env_config.defender_caught_attacker_reward

        # Merge infos
        if info is None:
            info = defender_info
        else:
            if defender_info is not None:
                for k,v in defender_info.items():
                    if k not in info:
                        info[k] = v
        info[constants.INFO_DICT.ATTACKER_ACTION] = attack_action_id

        # Update state
        if self.env_config.defender_update_state and not done:
            if self.env_state.defender_obs_state.caught_attacker:
                attacker_action_idx = self.env_config.attacker_action_conf.get_continue_action_idx()
                attacker_action = self.env_config.attacker_action_conf.actions[attacker_action_idx]
            else:
                attacker_action = self.env_state.attacker_obs_state.last_attacker_action
            # Update defender's state
            s_prime, _, _ = TransitionOperator.defender_transition(
                s=self.env_state, defender_action=self.env_config.defender_action_conf.state_update_action,
                env_config=self.env_config, attacker_action=attacker_action)
            self.env_state = s_prime

        # Extract observations
        defender_m_obs, defender_network_obs = self.env_state.get_defender_observation()
        attacker_m_obs, attacker_p_obs = self.env_state.get_attacker_observation()
        attacker_m_obs = np.append(np.array([self.attacker_agent_state.time_step]), attacker_m_obs.flatten())
        defender_obs = np.append(defender_network_obs, defender_m_obs.flatten())
        self.defender_last_obs = defender_obs
        self.attacker_last_obs = attacker_m_obs
        self.defender_time_step += 1
        self.attacker_agent_state.time_step += 1
        if attack_action_id != 372:
            self.env_state.attacker_obs_state.step += 1
            if self.env_state.attacker_obs_state.intrusion_step == -1:
                self.env_state.attacker_obs_state.intrusion_step = self.env_state.defender_obs_state.step
        info[constants.INFO_DICT.INTRUSION_STEP] = self.env_state.attacker_obs_state.intrusion_step

        # Update trajectories
        if self.env_config.save_trajectories:
            self.defender_trajectory = []
            self.defender_trajectory.append(defender_obs)
            self.defender_trajectory.append(defender_reward)
            self.attacker_trajectory = []
            self.attacker_trajectory.append(self.attacker_last_obs)
            self.attacker_trajectory.append(attack_action_id)
            self.attacker_agent_state.episode_reward += attacker_reward
            self.attacker_trajectory.append(attacker_m_obs)
            self.attacker_trajectory.append(attacker_reward)
            self.defender_trajectories.append(self.defender_trajectory)
            self.attacker_trajectories.append(self.attacker_trajectory)

        return (attacker_m_obs, defender_obs), (attacker_reward, defender_reward), done, info

    def step_attacker(self, attacker_action_id) -> Tuple[int, bool, dict]:
        """
        Takes a step in the environment as the attacker by executing the given action

        :param attacker_action_id: the action to take
        :return: (obs, reward, done, info)
        """

        info = {constants.INFO_DICT.IDX: self.idx}
        info[constants.INFO_DICT.SUCCESSFUL_INTRUSION] = False
        # Check if action is illegal
        if not self.is_attack_action_legal(attacker_action_id, env_config=self.env_config, env_state=self.env_state):
            actions = list(range(len(self.env_config.attacker_action_conf.actions)))
            print("[Warning] illegal attack action:{}, idx:{}, ip:{},\nillegal actions:{},\nlegal_actions:{}".format(
                attacker_action_id, self.idx, self.env_config.router_ip,
                list(filter(lambda action: not PyCRCTFEnv.is_attack_action_legal(action, env_config=self.env_config,
                                                                                 env_state=self.env_state), actions)),
                list(filter(lambda action: PyCRCTFEnv.is_attack_action_legal(
                    action, env_config=self.env_config, env_state=self.env_state), actions))
            ))
            self.attacker_agent_state.time_step += 1
            attacker_reward = self.env_config.attacker_illegal_reward_action
            return attacker_reward, True, info

        if attacker_action_id > len(self.env_config.attacker_action_conf.actions) - 1:
            raise ValueError("Action ID: {} not recognized".format(attacker_action_id))

        # Prepare action for execution
        attack_action = self.env_config.attacker_action_conf.actions[attacker_action_id]

        attack_action.ip = self.env_state.attacker_obs_state.get_action_ip(attack_action)
        self.env_state.attacker_obs_state.cost += attack_action.cost
        self.env_state.attacker_obs_state.cost_norm += EnvDynamicsUtil.normalize_action_costs(
            action=attack_action, env_config=self.env_config)
        self.env_state.attacker_obs_state.alerts += attack_action.alerts[0]
        self.env_state.attacker_obs_state.alerts_norm += EnvDynamicsUtil.normalize_action_alerts(
            action=attack_action, env_config=self.env_config)
        info[constants.INFO_DICT.ATTACKER_COST] = self.env_state.attacker_obs_state.cost
        info[constants.INFO_DICT.ATTACKER_COST_NORM] = self.env_state.attacker_obs_state.cost_norm
        info[constants.INFO_DICT.ATTACKER_ALERTS] = self.env_state.attacker_obs_state.alerts
        info[constants.INFO_DICT.ATTACKER_ALERTS_NORM] = self.env_state.attacker_obs_state.alerts_norm
        # Step in the environment
        s_prime, attacker_reward, done = TransitionOperator.attacker_transition(
            s=self.env_state, attacker_action=attack_action, env_config=self.env_config)

        # Parse result of action
        if done:
            attacker_reward = attacker_reward - self.env_config.attacker_final_steps_reward_coefficient \
                              * self.attacker_agent_state.time_step
        if self.attacker_agent_state.time_step > self.env_config.max_episode_length:
            done = True
            attacker_reward = attacker_reward + self.env_config.max_episode_length_reward
            info[constants.INFO_DICT.CAUGHT_ATTACKER] = True


        if s_prime.attacker_obs_state.all_flags:
            info[constants.INFO_DICT.SUCCESSFUL_INTRUSION] = True

        if s_prime.attacker_obs_state.all_flags:
            attacker_reward = attacker_reward - self.env_state.attacker_obs_state.cost_norm \
                              - self.env_state.attacker_obs_state.alerts_norm

        self.env_state = s_prime
        if self.env_state.attacker_obs_state.detected:
            info[constants.INFO_DICT.CAUGHT_ATTACKER] = True
        info[constants.INFO_DICT.FLAGS] = self.env_state.attacker_obs_state.catched_flags
        if self.env_config.save_trajectories:
            self.attacker_trajectories.append(self.attacker_trajectory)

        self.__update_log(attack_action)

        self.env_state.attacker_obs_state.last_attacker_action = attack_action
        return attacker_reward, done, info

    def step_defender(self, defender_action_id, attacker_action: AttackerAction,
                      attacker_opponent = None) -> Tuple[np.ndarray, int, bool, dict]:
        """
        Takes a step in the environment as the defender by executing the given action

        :param defender_action_id: the action to take
        :param done_attacker: whether the environment completed after attacker action
        :return: (obs, reward, done, info)
        """
        info = {constants.INFO_DICT.IDX: self.idx}
        info[constants.INFO_DICT.FLAGS] = self.env_state.attacker_obs_state.catched_flags

        # Update trajectory
        self.defender_trajectory = []
        self.defender_trajectory.append(self.defender_last_obs)
        self.defender_trajectory.append(defender_action_id)
        if not self.is_defense_action_legal(defender_action_id, env_config=self.env_config,
                                            env_state=self.env_state):
            print("illegal defense action:{}, idx:{}".format(defender_action_id, self.idx))
            raise ValueError("illegal defense action")
            #sys.exit(0)
            done = False
            return self.defender_last_obs, self.env_config.illegal_reward_action, done, info

        # Prepare action for execution in the environment
        if defender_action_id > len(self.env_config.defender_action_conf.actions) - 1:
            raise ValueError("Action ID: {} not recognized".format(defender_action_id))
        defense_action = self.env_config.defender_action_conf.actions[defender_action_id]
        defense_action.ip = self.env_state.defender_obs_state.get_action_ip(defense_action)

        # Step in the environment
        s_prime, defender_reward, done = TransitionOperator.defender_transition(
            s=self.env_state, defender_action=defense_action, attacker_action=attacker_action,
            env_config=self.env_config)

        # Snort baselines
        StoppingBaselinesUtil.compute_baseline_metrics(
            s=self.env_state, s_prime=s_prime, env_config=self.env_config)

        # Parse result
        attacker_reward = 0

        if self.defender_time_step > self.env_config.max_episode_length:
            done = True
            attacker_reward = attacker_reward + self.env_config.max_episode_length_reward

        if not self.env_config.multiple_stopping_environment or self.env_config.attacker_prevented_stops_remaining == 0:
            uncaught_intrusion_steps = max(0, self.env_state.defender_obs_state.step
                                           - self.env_state.attacker_obs_state.intrusion_step)
        else:
            if self.env_config.attacker_prevented_stops_remaining == 1:
                uncaught_intrusion_steps = max(0, self.env_state.defender_obs_state.third_stop_step
                                               - self.env_state.attacker_obs_state.intrusion_step)
            elif self.env_config.attacker_prevented_stops_remaining == 2:
                uncaught_intrusion_steps = max(0, self.env_state.defender_obs_state.second_stop_step
                                               - self.env_state.attacker_obs_state.intrusion_step)
            elif self.env_config.attacker_prevented_stops_remaining == 3:
                uncaught_intrusion_steps = max(0, self.env_state.defender_obs_state.first_stop_step
                                               - self.env_state.attacker_obs_state.intrusion_step)
        info[constants.INFO_DICT.UNCAUGHT_INTRUSION_STEPS] = uncaught_intrusion_steps

        self.env_state = s_prime

        if self.env_state.defender_obs_state.caught_attacker:
            attacker_reward = self.env_config.attacker_detection_reward
            self.attacker_agent_state.num_detections += 1
        elif self.env_state.defender_obs_state.stopped:
            attacker_reward = self.env_config.attacker_early_stopping_reward

        if self.env_config.stop_after_failed_detection and not done and \
                self.env_state.attacker_obs_state.ongoing_intrusion():
            done = True

        optimal_defender_reward, optimal_stopping_indexes, optimal_stops_remaining, optimal_episode_steps = \
            StoppingBaselinesUtil.simulate_end_of_episode_performance(
            s_prime=s_prime, env_config=self.env_config, done=done, env=self, s=self.env_state,
            attacker_opponent=self.env_config.attacker_static_opponent)

        info[constants.INFO_DICT.OPTIMAL_DEFENDER_REWARD] = optimal_defender_reward
        info[constants.INFO_DICT.OPTIMAL_FIRST_STOP_STEP] = optimal_stopping_indexes[0]
        info[constants.INFO_DICT.OPTIMAL_SECOND_STOP_STEP] = optimal_stopping_indexes[1]
        info[constants.INFO_DICT.OPTIMAL_THIRD_STOP_STEP] = optimal_stopping_indexes[2]
        info[constants.INFO_DICT.OPTIMAL_FOURTH_STOP_STEP] = optimal_stopping_indexes[3]
        info[constants.INFO_DICT.OPTIMAL_STOPS_REMAINING] = optimal_stops_remaining
        info[constants.INFO_DICT.OPTIMAL_DEFENDER_EPISODE_STEPS] = optimal_episode_steps


        info = self.env_state.defender_obs_state.update_info_dict(info)
        return defender_reward, attacker_reward, done, info


    def reset(self, soft : bool = False) -> Tuple[np.ndarray, np.ndarray]:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :return: initial observation
        """
        if self.env_config.attacker_static_opponent is not None:
            self.env_config.attacker_static_opponent.reset()

        if not soft and self.env_config.env_mode == EnvMode.SIMULATION \
                and self.env_config.domain_randomization and self.randomization_space is not None:
            randomized_network_conf, env_config = DomainRandomizer.randomize(subnet_prefix="172.18.",
                                                                             network_ids=list(range(1, 254)),
                                                                             r_space=self.randomization_space,
                                                                             env_config=self.env_config)
            self.env_config = env_config
            if self.env_config.compute_pi_star_attacker:
                if not self.env_config.use_upper_bound_pi_star_attacker:
                    attacker_pi_star_tau, attacker_pi_star_rew = FindPiStarAttacker.brute_force(self.env_config, self)
                else:
                    attacker_pi_star_rew = FindPiStarAttacker.upper_bound_pi(self.env_config)
                    attacker_pi_star_tau = None
                self.env_config.pi_star_tau_attacker = attacker_pi_star_tau
                self.env_config.pi_star_rew_attacker = attacker_pi_star_rew
                self.env_config.pi_star_rew_list_attacker.append(attacker_pi_star_rew)

            self.env_config = FindPiStarDefender.update_pi_star(self.env_config)


        self.reset_metrics()

        if self.env_config.defender_update_state:
            # Initialize Defender's state
            defender_init_action = self.env_config.defender_action_conf.state_init_action
            s_prime, _, _ = TransitionOperator.defender_transition(
                s=self.env_state, defender_action=defender_init_action, env_config=self.env_config)
            self.env_state = s_prime

        # Randomize the starting state
        if self.env_config.randomize_attacker_starting_state:
            if self.env_config.randomize_state_steps_list is None:
                max_steps = np.random.randint(self.env_config.randomize_state_min_steps,
                                              self.env_config.randomize_state_max_steps)
            else:
                max_steps = np.random.choice(np.array(self.env_config.randomize_state_steps_list))
            exp_policy = self.env_config.attacker_exploration_policy
            if self.env_config.randomize_starting_state_policy is not None:
                exp_policy = self.env_config.randomize_starting_state_policy
            d = True
            while d:
                d2 = InitialStateRandomizer.randomize_starting_state(
                    exp_policy=exp_policy,
                    env_config=self.env_config, env=self, max_steps=max_steps)
                d = d2
                if d:
                    d = d2
                    self.reset_metrics()

        if self.env_config.randomize_defender_starting_state:
            self.env_state.defender_obs_state.stops_remaining = random.randint(1,4)
            if self.env_state.defender_obs_state.stops_remaining <= 3:
                self.env_state.defender_obs_state.first_stop_step = 1
            if self.env_state.defender_obs_state.stops_remaining <= 2:
                self.env_state.defender_obs_state.second_stop_step = 1
            if self.env_state.defender_obs_state.stops_remaining <= 1:
                self.env_state.defender_obs_state.third_stop_step = 1


        #self.viewer.mainframe.set_state(self.agent_state)
        if self.viewer is not None and self.viewer.mainframe is not None:
            self.viewer.mainframe.reset_state()
        if self.env_config.env_mode == EnvMode.SIMULATION:
            self.env_state.attacker_obs_state.agent_reachable = self.env_config.network_conf.agent_reachable
        self.env_config.cache_misses = 0
        sys.stdout.flush()

        total_attacker_actions = list(range(self.attacker_num_actions))
        self.attacker_initial_illegal_actions = list(filter(lambda attack_action: not PyCRCTFEnv.is_attack_action_legal(
            attack_action, env_config=self.env_config,
            env_state=self.env_state), total_attacker_actions))

        attacker_m_obs, attacker_p_obs = self.env_state.get_attacker_observation()
        attacker_m_obs = np.append(np.array([self.env_state.attacker_obs_state.step]), attacker_m_obs.flatten())
        defender_m_obs, defender_network_obs = self.env_state.get_defender_observation()
        defender_obs = np.append(defender_network_obs, defender_m_obs.flatten())
        self.attacker_last_obs = attacker_m_obs
        self.attacker_agent_state.attacker_obs_state = self.env_state.attacker_obs_state

        return attacker_m_obs, defender_obs

    def reset_metrics(self):
        self.__checkpoint_log()
        self.__checkpoint_trajectories()
        if self.env_state.attacker_obs_state.detected:
            self.attacker_agent_state.num_detections += 1
        elif self.env_state.attacker_obs_state.all_flags:
            self.attacker_agent_state.num_all_flags += 1

        self.reset_state()
        self.attacker_agent_state.num_episodes += 1
        self.attacker_agent_state.cumulative_reward += self.attacker_agent_state.episode_reward
        self.attacker_agent_state.time_step = 0
        self.attacker_agent_state.episode_reward = 0
        self.defender_time_step = 0
        self.attacker_agent_state.env_log.reset()


    def render(self, mode: str = 'human'):
        """
        Renders the environment
        Supported rendering modes:
          -human: render to the current display or terminal and return nothing. Usually for human consumption.
          -rgb_array: Return an numpy.ndarray with shape (x, y, 3),
                      representing RGB values for an x-by-y pixel image, suitable
                      for turning into a video.
        :param mode: the rendering mode
        :return: True (if human mode) otherwise an rgb array
        """
        #self.agent_state.attacker_obs_state = self.env_state.attacker_obs_state.copy()
        self.attacker_agent_state.attacker_obs_state = self.env_state.attacker_obs_state
        if mode not in self.metadata["render.modes"]:
            raise NotImplemented("mode: {} is not supported".format(mode))
        if self.viewer is None:
            self.__setup_viewer()
        self.viewer.mainframe.set_state(self.attacker_agent_state)
        arr = self.viewer.render(return_rgb_array=mode == 'rgb_array')
        return arr

    def randomize(self):
        randomized_network_conf, env_config = DomainRandomizer.randomize(subnet_prefix="172.18.",
                                                                         network_ids=list(range(1, 254)),
                                                                         r_space=self.randomization_space,
                                                                         env_config=self.env_config)
        self.env_config = env_config
        attacker_total_actions = list(range(self.attacker_num_actions))
        self.attacker_initial_illegal_actions = list(filter(lambda action: not PyCRCTFEnv.is_attack_action_legal(
            action, env_config=self.env_config, env_state=self.env_state), attacker_total_actions))

    @staticmethod
    def is_defense_action_legal(defense_action_id: int, env_config: EnvConfig, env_state: EnvState) -> bool:
        """
        Checks if a given defense action is legal in the current state of the environment

        :param defense_action_id: the id of the action to check
        :param env_config: the environment config
        :param env_state: the environment state
        :param attacker_action: the id of the previous attack action
        :return: True if legal, else false
        """
        return EnvUtil.is_defense_action_legal(defense_action_id=defense_action_id, env_config=env_config,
                                               env_state=env_state)

    @staticmethod
    def is_attack_action_legal(attack_action_id : int, env_config: EnvConfig, env_state: EnvState, m_selection: bool = False,
                               m_action: bool = False, m_index : int = None) -> bool:
        """
        Checks if a given attack action is legal in the current state of the environment

        :param attack_action_id: the id of the action to check
        :param env_config: the environment config
        :param env_state: the environment state
        :param m_selection: boolean flag whether using AR policy m_selection or not
        :param m_action: boolean flag whether using AR policy m_action or not
        :param m_index: index of machine in case using AR policy
        :return: True if legal, else false
        """
        return EnvUtil.is_attack_action_legal(attack_action_id=attack_action_id, env_config=env_config,
                                              env_state=env_state, m_selection=m_selection, m_action=m_action,
                                              m_index=m_index)

    def close(self) -> None:
        """
        Closes the viewer (cleanup)
        :return: None
        """
        if self.viewer:
            self.viewer.close()
            self.viewer = None

    def cleanup(self) -> None:
        """
        Cleans up environment state. This method is particularly useful in emulation mode where there are
        SSH/Telnet/FTP... connections that should be cleaned up, as well as background threads.

        :return: None
        """
        self.env_state.cleanup()
        if self.env_config.emulation_config is not None:
            self.env_config.emulation_config.close()

    def attacker_convert_ar_action(self, machine_idx, action_idx):
        """
        Converts an AR action id into a global action id

        :param machine_idx: the machine id
        :param action_idx: the action id
        :return: the global action id
        """
        key = (machine_idx, action_idx)
        print(self.env_config.attacker_action_conf.ar_action_converter)
        return self.env_config.attacker_action_conf.ar_action_converter[key]

    # -------- Private methods ------------

    def __update_log(self, action : AttackerAction) -> None:
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
        self.attacker_agent_state.env_log.add_entry(action.name + "[." + tag + "]" + " c:" + str(action.cost))

    def __setup_viewer(self):
        """
        Setup for the viewer to use for rendering

        :return: None
        """
        from pycr_common import Viewer
        script_dir = os.path.dirname(__file__)
        resource_path = os.path.join(script_dir, './rendering/frames/', constants.RENDERING.RESOURCES_DIR)
        self.env_config.render_config.resources_dir = resource_path
        self.viewer = Viewer(env_config=self.env_config, init_state=self.attacker_agent_state)
        self.viewer.start()

    def __checkpoint_log(self) -> None:
        """
        Checkpoints the agent log for an episode

        :return: None
        """
        if not self.env_config.checkpoint_dir == None \
                and self.attacker_agent_state.num_episodes % self.env_config.checkpoint_freq == 0:
            file_path = self.env_config.checkpoint_dir + "/ep_" + str(self.attacker_agent_state.num_episodes) + "_agent.log"
            with open(file_path, "w") as outfile:
                outfile.write("\n".join(self.attacker_agent_state.env_log.log))

    def __checkpoint_trajectories(self) -> None:
        """
        Checkpoints agent trajectories

        :return: None
        """
        if self.env_config.save_trajectories and not self.env_config.checkpoint_dir == None \
                and self.attacker_agent_state.num_episodes % self.env_config.checkpoint_freq == 0:
            file_path = self.env_config.checkpoint_dir + "/ep_" + str(self.attacker_agent_state.num_episodes) + "_trajectories.pickle"
            with open(file_path, "wb") as outfile:
                pickle.dump(self.attacker_trajectories, outfile, protocol=pickle.HIGHEST_PROTOCOL)
                self.attacker_trajectories = []

    def reset_state(self) -> None:
        """
        Resets the environment state

        :return: None
        """
        self.env_state.reset_state()
        defender_reset_action = self.env_config.defender_action_conf.state_reset_action
        s_prime, _, _ = TransitionOperator.defender_transition(s=self.env_state, defender_action=defender_reset_action,
                                               env_config=self.env_config)
        self.env_state = s_prime

    def warmup(self) -> None:
        """
        Warmup in the emulation

        :return: None
        """
        EmulationWarmup.warmup(exp_policy=RandomExplorationPolicy(
            num_actions=self.env_config.attacker_action_conf.num_actions),
            num_warmup_steps=self.env_config.emulation_config.warmup_iterations,
            env=self, render = False)
        print("[Warmup complete], nmap_cache_size:{}, fs_cache_size:{}, user_command_cache:{}, nikto_scan_cache:{},"
              "cache_misses:{}".format(
            len(self.env_config.attacker_nmap_scan_cache.cache),
            len(self.env_config.attacker_filesystem_scan_cache.cache),
            len(self.env_config.attacker_user_command_cache.cache),
            len(self.env_config.attacker_nikto_scan_cache.cache),
            self.env_config.cache_misses))


    def system_identification(self) -> None:
        """
        Performs system identification to estimate a dynamics model

        :return: None
        """
        self.env_config.network_conf, obs_state = SimulationGenerator.build_model(
            exp_policy=self.env_config.attacker_exploration_policy, env_config=self.env_config, env=self,
        )
        self.env_state.attacker_obs_state = obs_state
        self.env_config.env_mode = EnvMode.SIMULATION
        self.randomization_space = DomainRandomizer.generate_randomization_space([self.env_config.network_conf])
        self.env_config.emulation_config.connect_agent()

        if self.env_config.defender_update_state:
            # Initialize Defender's state
            defender_init_action = self.env_config.defender_action_conf.state_init_action
            s_prime, _, _ = TransitionOperator.defender_transition(
                s=self.env_state, defender_action=defender_init_action, env_config=self.env_config)
            self.env_state = s_prime
            self.env_config.network_conf.defender_dynamics_model.normalize()
        self.reset()

    def load_dynamics_model(self) -> None:
        """
        Loads a pre-defined dynamics model

        :return: None
        """
        defender_dynamics_model = SimulationGenerator.initialize_defender_dynamics_model()
        if self.env_config.emulation_config.save_dynamics_model_dir is not None:
            print('Loading Dynamics Model..')
            defender_dynamics_model.read_model(
                dir_path=self.env_config.emulation_config.save_dynamics_model_dir,
                model_name=self.env_config.emulation_config.save_dynamics_model_file
            )
            loaded_netconf = self.env_config.network_conf.load(
                dir_path=self.env_config.emulation_config.save_dynamics_model_dir,
                file_name=self.env_config.emulation_config.save_netconf_file
            )
            if loaded_netconf is not None:
                self.env_config.network_conf = loaded_netconf
            self.env_config.network_conf.defender_dynamics_model = defender_dynamics_model
            self.env_config.network_conf.defender_dynamics_model.normalize()
            print('Dynamics Model Loaded Successfully')

        self.env_config.env_mode = EnvMode.SIMULATION


    @staticmethod
    def initialize_info_dict() -> dict:
        """
        Initialize the info dict

        :return: the dict with the initialized values
        """
        info = {}
        info[constants.INFO_DICT.CAUGHT_ATTACKER] = 0
        info[constants.INFO_DICT.EARLY_STOPPED] = 0
        info[constants.INFO_DICT.OPTIMAL_DEFENDER_REWARD] = 0
        info[constants.INFO_DICT.UNCAUGHT_INTRUSION_STEPS] = 0
        info[constants.INFO_DICT.SNORT_SEVERE_BASELINE_REWARD] = 0
        info[constants.INFO_DICT.SNORT_WARNING_BASELINE_REWARD] = 0
        info[constants.INFO_DICT.SNORT_CRITICAL_BASELINE_REWARD] = 0
        info[constants.INFO_DICT.VAR_LOG_BASELINE_REWARD] = 0
        info[constants.INFO_DICT.STEP_BASELINE_REWARD] = 0
        info[constants.INFO_DICT.SNORT_SEVERE_BASELINE_STEP] = 1
        info[constants.INFO_DICT.SNORT_WARNING_BASELINE_STEP] = 1
        info[constants.INFO_DICT.SNORT_CRITICAL_BASELINE_STEP] = 1
        info[constants.INFO_DICT.VAR_LOG_BASELINE_STEP] = 1
        info[constants.INFO_DICT.STEP_BASELINE_STEP] = 1
        info[constants.INFO_DICT.SNORT_SEVERE_BASELINE_CAUGHT_ATTACKER] = False
        info[constants.INFO_DICT.SNORT_WARNING_BASELINE_CAUGHT_ATTACKER] = False
        info[constants.INFO_DICT.SNORT_CRITICAL_BASELINE_CAUGHT_ATTACKER] = False
        info[constants.INFO_DICT.VAR_LOG_BASELINE_CAUGHT_ATTACKER] = False
        info[constants.INFO_DICT.STEP_BASELINE_CAUGHT_ATTACKER] = False
        info[constants.INFO_DICT.SNORT_SEVERE_BASELINE_EARLY_STOPPING] = False
        info[constants.INFO_DICT.SNORT_WARNING_BASELINE_EARLY_STOPPING] = False
        info[constants.INFO_DICT.SNORT_CRITICAL_BASELINE_EARLY_STOPPING] = False
        info[constants.INFO_DICT.VAR_LOG_BASELINE_EARLY_STOPPING] = False
        info[constants.INFO_DICT.STEP_BASELINE_EARLY_STOPPING] = False
        info[constants.INFO_DICT.SNORT_SEVERE_BASELINE_UNCAUGHT_INTRUSION_STEPS] = 0
        info[constants.INFO_DICT.SNORT_WARNING_BASELINE_UNCAUGHT_INTRUSION_STEPS] = 0
        info[constants.INFO_DICT.SNORT_CRITICAL_BASELINE_UNCAUGHT_INTRUSION_STEPS] = 0
        info[constants.INFO_DICT.VAR_LOG_BASELINE_UNCAUGHT_INTRUSION_STEPS] = 0
        info[constants.INFO_DICT.STEP_BASELINE_UNCAUGHT_INTRUSION_STEPS] = 0
        info[constants.INFO_DICT.DEFENDER_STOPS_REMAINING] = 1
        info[constants.INFO_DICT.INTRUSION_STEP] = 1
        info[constants.INFO_DICT.DEFENDER_FIRST_STOP_STEP] = -1
        info[constants.INFO_DICT.DEFENDER_SECOND_STOP_STEP] = -1
        info[constants.INFO_DICT.DEFENDER_THIRD_STOP_STEP] = -1
        info[constants.INFO_DICT.DEFENDER_FOURTH_STOP_STEP] = -1
        return info