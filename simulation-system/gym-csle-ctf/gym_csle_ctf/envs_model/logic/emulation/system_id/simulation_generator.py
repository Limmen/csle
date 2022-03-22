from typing import Tuple, List
import numpy as np
import sys
import os
import csv
from torch.utils.tensorboard import SummaryWriter
from gym_csle_ctf.dao.network.env_config import CSLEEnvConfig
from gym_csle_ctf.envs_model.logic.common.env_dynamics_util import EnvDynamicsUtil
from gym_csle_ctf.envs_model.logic.transition_operator import TransitionOperator
import csle_common.constants.constants as constants
from csle_common.dao.network.network_config import NetworkConfig
from csle_common.envs_model.logic.exploration.exploration_policy import ExplorationPolicy
from csle_common.dao.defender_dynamics.defender_dynamics_model import DefenderDynamicsModel
from csle_common.dao.network.trajectory import Trajectory
from csle_common.dao.defender_dynamics.defender_dynamics_tensorboard_dto import DefenderDynamicsTensorboardDTO


class SimulationGenerator:
    """
    Class with functions for running an exploration policy in an environment to build a model
    that later can be used for simulations
    """

    @staticmethod
    def explore(attacker_exp_policy: ExplorationPolicy, env_config: CSLEEnvConfig, env,
                render: bool = False, defender_dynamics_model: DefenderDynamicsModel = None,
                tensorboard_writer : SummaryWriter = None, tau_index :int = 0
                ) -> Tuple[np.ndarray, Trajectory, List[DefenderDynamicsTensorboardDTO]]:
        """
        Explores the environment to generate trajectories that can be used to learn a dynamics model

        :param attacker_exp_policy: the exploration policy to use
        :param env_config: the env config
        :param env: the env to explore
        :param render: whether to render the env or not
        :param explore_defense_states: boolean flag whether to explore defensive states or not
        :return: The final observation, the collected trajectory, the log
        """
        obs = env.reset()
        init_state = env.env_state.copy()
        done = False
        step = 0
        log = []
        trajectory = SimulationGenerator.reset_trajectory(obs)
        if not env_config.explore_defense_states:
            defender_action = None
            old_env_config = env_config.copy()
            env_config.simulate_detection = False
            env_config.emulate_detection = False
            env_config.max_episode_length = env_config.attacker_max_exploration_steps
            env.env_config = env_config
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

            # Sample action
            attacker_action = attacker_exp_policy.action(
                env=env, filter_illegal=env_config.attacker_exploration_filter_illegal, step=step)

            # Step in the environment
            action = (attacker_action, defender_action)
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
                tb_dto = defender_dynamics_model.update_model(
                    s=s, s_prime=s_prime, attacker_action_id=attack_action_dto.id,
                    attacker_action_name= attack_action_dto.name,
                    attacker_action_idx = action[0],
                    logged_in_ips=logged_in_ips_str, t=step, idx=tau_index)
                tb_dto.log_tensorboard(tensorboard_writer=tensorboard_writer)
                log.append(tb_dto)
                print(str(tb_dto))


            step +=1
            if render:
                env.render()
        if step >= env_config.attacker_max_exploration_steps:
            print("maximum exploration steps reached")
        env.env_config = old_env_config
        return defender_dynamics_model, trajectory, log

    @staticmethod
    def build_model(exp_policy: ExplorationPolicy, env_config: CSLEEnvConfig, env, render: bool = False) \
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

        # Setup TensorBoard
        tensorboard_writer = SummaryWriter(env.env_config.emulation_config.save_dynamics_model_dir + "/tensorboard")

        # Initialize model
        aggregated_observation = env.env_state.attacker_obs_state.copy()
        defender_dynamics_model = SimulationGenerator.initialize_defender_dynamics_model()
        trajectories = []
        logs = []
        if env_config.emulation_config.save_dynamics_model_dir is not None:
            defender_dynamics_model.read_model(
                dir_path=env.env_config.emulation_config.save_dynamics_model_dir,
                model_name=env.env_config.emulation_config.save_dynamics_model_file
            )
            trajectories = Trajectory.load_trajectories(
                env_config.emulation_config.save_dynamics_model_dir,
                trajectories_file=env_config.emulation_config.save_trajectories_file)

            loaded_netconf = env_config.network_conf.load(
                dir_path=env_config.emulation_config.save_dynamics_model_dir,
                file_name=env_config.emulation_config.save_netconf_file
            )
            if loaded_netconf is not None:
                env_config.network_conf = loaded_netconf

        for i in range(env_config.attacker_max_exploration_trajectories):

            print("Collecting trajectory {}/{}".format(i, env_config.attacker_max_exploration_trajectories))

            if env.env_config.defender_update_state:
                # Initialize Defender's state
                defender_init_action = env_config.defender_action_conf.state_init_action
                TransitionOperator.defender_transition(s=env.env_state, defender_action=defender_init_action,
                                                       env_config=env_config)

            # Collect trajectory
            defender_dynamics_model, trajectory, log = \
                SimulationGenerator.explore(attacker_exp_policy= exp_policy, env_config=env_config,
                                            env=env, render=render, defender_dynamics_model=defender_dynamics_model,
                                            tensorboard_writer=tensorboard_writer, tau_index=i)
            trajectories.append(trajectory)
            logs = logs + log

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
            num_flags = aggregated_observation.num_flags
            print("Exploration completed, found {} machines, {} vulnerabilities, {} credentials, {} flags".format(
                num_machines, num_vulnerabilities, num_credentials, num_flags))

            nodes = list(map(lambda x: x.to_node(), aggregated_observation.machines))
            new_net_conf = NetworkConfig(subnet_mask=env_config.network_conf.subnet_mask, nodes=nodes,
                                         adj_matrix=env_config.network_conf.adj_matrix,
                                         flags_lookup=env_config.network_conf.flags_lookup,
                                         agent_reachable=env_config.network_conf.agent_reachable)
            env_config.network_conf.merge(new_net_conf)
            # for n2 in env_config.network_conf.nodes:
            #     print("node:{}, flags:{}".format(n2.ip, list(map(lambda x: str(x), n2.flags))))
            env_config.network_conf.defender_dynamics_model = defender_dynamics_model
            env_config.network_conf.agent_reachable = aggregated_observation.agent_reachable

            # Save Models
            print("Checkpointing models")
            defender_dynamics_model.save_model(
                dir_path=env_config.emulation_config.save_dynamics_model_dir,
                model_name=env_config.emulation_config.save_dynamics_model_file)
            Trajectory.save_trajectories(env_config.emulation_config.save_dynamics_model_dir, trajectories,
                                         trajectories_file=env_config.emulation_config.save_trajectories_file)
            SimulationGenerator.save_logs_to_csv(logs, dir=env_config.emulation_config.save_dynamics_model_dir,
                                                 filename=env_config.emulation_config.save_system_id_logs_file)

            env_config.network_conf.save(
                dir_path=env_config.emulation_config.save_dynamics_model_dir,
                file_name=env_config.emulation_config.save_netconf_file
            )

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
        if attacker_action is None:
            attacker_action = -1
        if defender_action is None:
            defender_action = -1
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

    @staticmethod
    def save_logs_to_csv(logs: List[DefenderDynamicsTensorboardDTO], dir: str, filename: str):
        if dir is None or dir == "":
            dir = os.getcwd()
        if filename is None or filename == "":
            filename = constants.SYSTEM_IDENTIFICATION.SYSTEM_ID_LOGS_FILE

        metrics = [
            list(map(lambda x: x.t, logs)), list(map(lambda x: x.num_new_alerts, logs)),
            list(map(lambda x: x.num_new_priority, logs)), list(map(lambda x: x.num_new_severe_alerts, logs)),
            list(map(lambda x: x.num_new_warning_alerts, logs)), list(map(lambda x: x.num_new_open_connections, logs)),
            list(map(lambda x: x.num_new_failed_login_attempts, logs)),
            list(map(lambda x: x.num_new_login_events, logs)), list(map(lambda x: x.num_new_processes, logs)),
            list(map(lambda x: x.index, logs)), list(map(lambda x: x.attacker_action_id, logs)),
            list(map(lambda x: x.attacker_action_idx, logs)), list(map(lambda x: x.attacker_action_name, logs))
        ]
        labels = [
            "t", "num_new_alerts", "num_new_priority", "num_new_severe_alerts", "num_new_warning_alerts",
            "num_new_open_connections", "num_new_failed_login_attempts", "num_new_login_events", "num_new_processes",
            "index", "attacker_action_id", "attacker_action_idx", "attacker_action_name"
        ]

        rows = zip(*metrics)
        with open(dir + "/" + filename, "w") as f:
            writer = csv.writer(f)
            writer.writerow(labels)
            for row in rows:
                writer.writerow(row)
