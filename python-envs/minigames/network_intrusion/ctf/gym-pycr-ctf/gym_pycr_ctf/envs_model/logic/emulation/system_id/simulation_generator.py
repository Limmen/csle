from typing import Tuple
import numpy as np
import os
import sys
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.network.network_config import NetworkConfig
from gym_pycr_ctf.envs_model.logic.exploration.exploration_policy import ExplorationPolicy
from gym_pycr_ctf.envs_model.logic.common.env_dynamics_util import EnvDynamicsUtil
from gym_pycr_ctf.dao.defender_dynamics.defender_dynamics_model import DefenderDynamicsModel
from gym_pycr_ctf.util.experiments_util import util
from gym_pycr_ctf.envs_model.logic.transition_operator import TransitionOperator
import gym_pycr_ctf.constants.constants as constants
from gym_pycr_ctf.dao.network.trajectory import Trajectory


class SimulationGenerator:
    """
    Class for with functions for running an exploration policy in an environment to build a level_1 model
    that later can be used for simulations
    """

    @staticmethod
    def explore(attacker_exp_policy: ExplorationPolicy, env_config: EnvConfig, env,
                render: bool = False, defender_dynamics_model: DefenderDynamicsModel = None
                ) -> np.ndarray:
        """
        Explores the environment to generate trajectories that can be used to learn a dynamics model

        :param attacker_exp_policy: the exploration policy to use
        :param env_config: the env config
        :param env: the env to explore
        :param render: whether to render the env or not
        :param explore_defense_states: boolean flag whether to explore defensive states or not
        :return: The final observation
        """
        obs = env.reset()
        init_state = env.env_state.copy()
        done = False
        step = 0
        trajectory = SimulationGenerator.reset_trajectory(obs)
        if not env_config.explore_defense_states:
            defender_action = None
            old_env_config = env_config
        else:
            # Setup config
            old_env_config = env_config.copy()
            env_config.attacker_use_nmap_cache = False
            env_config.attacker_nmap_scan_cache = False
            env_config.attacker_use_nikto_cache = False
            env_config.attacker_use_file_system_cache = False
            env_config.attacker_use_user_command_cache = False
            defender_action = env_config.defender_action_conf.get_continue_action_idx()
            defender_dynamics_model.update_init_state_distribution(init_state=init_state)

        while not done and step < env_config.attacker_max_exploration_steps:

            # Save previous state
            s = env.env_state.copy()

            if step == 0 and env_config.explore_defense_states:
                # Start with sleep action to observe background noise
                attacker_action = env_config.attacker_action_conf.get_continue_action_idx()
            else:
                # Sample action
                attacker_action = attacker_exp_policy.action(
                    env=env, filter_illegal=env_config.attacker_exploration_filter_illegal)

            # Step in the environment
            action = (attacker_action, defender_action)
            print("step, action:{}".format(attacker_action))
            obs, reward, done, info = env.step(action)
            trajectory = SimulationGenerator.update_trajectory(trajectory=trajectory, obs=obs, reward=reward, done=done,
                                                  info=info, action=action)
            s_prime = env.env_state
            sys.stdout.flush()

            # Update dynamics
            if env_config.explore_defense_states and defender_dynamics_model is not None:
                attack_action_dto = env_config.attacker_action_conf.actions[attacker_action]
                logged_in_ips_str = EnvDynamicsUtil.logged_in_ips_str(env_config=env_config, a=attack_action_dto,
                                                                      s=env.env_state)
                defender_dynamics_model.update_model(s=s, s_prime=s_prime,
                                                     attacker_action_id=attack_action_dto.id,
                                                     logged_in_ips=logged_in_ips_str)

            step +=1
            if render:
                env.render()
        if step >= env_config.attacker_max_exploration_steps:
            print("maximum exploration steps reached")
        env.env_config = old_env_config
        return defender_dynamics_model, trajectory

    @staticmethod
    def build_model(exp_policy: ExplorationPolicy, env_config: EnvConfig, env, render: bool = False) \
            -> Tuple[NetworkConfig, np.ndarray]:
        """
        Builds a Model of the environment using System Identification, Random Walks, ML-estimation

        :param exp_policy: the exploration policy for the random walks
        :param env_config: the environment configuration
        :param env: the environment
        :param render: whether to render or not
        :return: The learned model
        """
        print("Starting System Identification Process to Estimate Model")

        # Initialize model
        aggregated_observation = env.env_state.attacker_obs_state.copy()
        defender_dynamics_model = SimulationGenerator.initialize_defender_dynamics_model()
        trajectories = []
        if env_config.emulation_config.save_dynamics_model_dir is not None:
            defender_dynamics_model.read_model(env_config)
            trajectories = Trajectory.load_trajectories(env_config.emulation_config.save_dynamics_model_dir)
            load_dir = env_config.emulation_config.save_dynamics_model_dir + "/" \
                       + constants.SYSTEM_IDENTIFICATION.NETWORK_CONF_FILE
            if os.path.exists(load_dir):
                env_config.network_conf = \
                    env_config.network_conf.load(load_dir)

        for i in range(env_config.attacker_max_exploration_trajectories):

            print("Collecting trajectory {}/{}".format(i, env_config.attacker_max_exploration_trajectories))

            if env.env_config.defender_update_state:
                # Initialize Defender's state
                defender_init_action = env_config.defender_action_conf.state_init_action
                TransitionOperator.defender_transition(s=env.env_state, defender_action=defender_init_action,
                                                       env_config=env_config)

            # Collect trajectory
            defender_dynamics_model, trajectory = \
                SimulationGenerator.explore(attacker_exp_policy= exp_policy, env_config=env_config,
                                            env=env, render=render, defender_dynamics_model=defender_dynamics_model)
            trajectories.append(trajectory)

            # Aggregate attacker's state
            observation = env.env_state.attacker_obs_state
            aggregated_observation = EnvDynamicsUtil.merge_complete_obs_state(old_obs_state=aggregated_observation,
                                                                              new_obs_state=observation,
                                                                              env_config=env_config)

            # Update model
            num_machines = len(aggregated_observation.machines)
            num_vulnerabilities = sum(
                list(map(lambda x: len(x.cve_vulns) + len(x.osvdb_vulns), aggregated_observation.machines)))
            num_credentials = sum(list(map(lambda x: len(x.shell_access_credentials), aggregated_observation.machines)))
            print("Exploration completed, found {} machines, {} vulnerabilities, {} credentials".format(
                num_machines, num_vulnerabilities, num_credentials))
            print("Defender Dynamics Model:\n{}".format(defender_dynamics_model))
            nodes = list(map(lambda x: x.to_node(), aggregated_observation.machines))
            node_ips = list(map(lambda x: x.ip, env_config.network_conf.nodes))
            for n in nodes:
                if n.ip not in node_ips:
                    env_config.network_conf.nodes.append(n)
            #env_config.network_conf.nodes = nodes
            env_config.network_conf.defender_dynamics_model = defender_dynamics_model
            env_config.network_conf.agent_reachable = aggregated_observation.agent_reachable

            # Save Models
            print("Checkpointing models")
            defender_dynamics_model.save_model(env_config)
            Trajectory.save_trajectories(env_config.emulation_config.save_dynamics_model_dir, trajectories)
            if env_config.emulation_config.save_dynamics_model_dir is not None:
                save_path = env_config.emulation_config.save_dynamics_model_dir + "/" \
                            + constants.SYSTEM_IDENTIFICATION.NETWORK_CONF_FILE
            else:
                save_path = util.get_script_path() + "/" \
                            + constants.SYSTEM_IDENTIFICATION.NETWORK_CONF_FILE
            env_config.network_conf.save(save_path)

        env.cleanup()
        return env_config.network_conf, aggregated_observation

    @staticmethod
    def initialize_defender_dynamics_model() -> DefenderDynamicsModel:
        """
        Utiltiy function for initializing a defender dynamics model

        :return: the initialized defender dynamics model
        """
        defender_dynamics_model = DefenderDynamicsModel()
        return defender_dynamics_model

    @staticmethod
    def update_trajectory(trajectory: Trajectory, obs: Tuple[np.ndarray, np.ndarray],
                          reward: Tuple[float, float], done : bool, info : dict, action: Tuple[int,int]) -> Trajectory:
        """
        Utility function for updating a trajectory with new information from a step in the environment

        :param trajectory: the trajectory to update
        :param obs: the new observations
        :param reward: the new rewards
        :param done: the new done (bool)
        :param info: the new info
        :param action: the actions
        :return: the updated trajectory
        """
        attacker_obs, defender_obs = obs
        attacker_reward, defender_reward = reward
        attacker_action, defender_action = action
        trajectory.attacker_rewards.append(float(attacker_reward))
        trajectory.defender_rewards.append(float(defender_reward))
        trajectory.attacker_observations.append(attacker_obs.tolist())
        trajectory.defender_observations.append(defender_obs.tolist())
        trajectory.infos.append(info)
        trajectory.dones.append(done)
        trajectory.attacker_actions.append(int(attacker_action))
        trajectory.defender_actions.append(int(defender_action))
        return trajectory

    @staticmethod
    def reset_trajectory(obs) -> Trajectory:
        """
        Utility function for resetting a trajectory DTO

        :param obs: the reset observation
        :return: the reset trajectory
        """
        attacker_obs, defender_obs = obs
        trajectory = Trajectory()
        trajectory.attacker_rewards.append(0)
        trajectory.defender_rewards.append(0)
        trajectory.attacker_observations.append(attacker_obs.tolist())
        trajectory.defender_observations.append(defender_obs.tolist())
        trajectory.infos.append({})
        trajectory.dones.append(False)
        trajectory.attacker_actions.append(-1)
        trajectory.defender_actions.append(-1)
        return trajectory