from typing import Tuple
import numpy as np
import gym
from gym_pycr_ctf.dao.observation.defender.defender_observation_state import DefenderObservationState

class DefenderStateRepresentation:
    """
    Utility class for configuring state and observation representations for the pycr-ctf env
    """

    @staticmethod
    def base_representation_spaces(obs_state: DefenderObservationState)-> Tuple:
        """
        Configures observation spaces for the base representation

        :param obs_state: the observation state
        :return: m_selection_obs_space (for AR), network_orig_shape, machine_orig_shape, m_action_obs_space (for AR)
        """
        num_network_features = 8
        num_m_features = 11
        observation_space = gym.spaces.Box(low=0, high=1000, dtype=np.float32, shape=(
            obs_state.num_machines * num_m_features + num_network_features,))
        return observation_space

    @staticmethod
    def base_representation(num_machines : int, obs_state :DefenderObservationState,
                            os_lookup: dict,
                            ids: bool = False) \
            -> Tuple[np.ndarray, np.ndarray]:
        """
        Base observation representation, includes all available information. E.g. for each machine: ports, ip, os,
        vulnerabilities, services, cvss, shell, root, flags, etc.

        :param num_machines: max number of machines in the obs
        :param obs_state: current observation state to turn into a numeratical representation
        :param os_lookup: lookup dict for converting categorical os into numerical
        :param ids: whether ids is enabled or not
        :return: Machines obs, ports obs, obs_space, m_selection_obs_space (for AR), network_orig_shape,
                 machine_orig_shape, m_action_obs_space (for AR)
        """
        obs_state.sort_machines()
        num_m_features = 11
        num_network_features = 8
        machines_obs = np.zeros((num_machines, num_m_features))
        if ids:
            network_obs = np.zeros(num_network_features)
            network_obs[0] = obs_state.num_alerts_recent
            network_obs[1] = obs_state.num_severe_alerts_recent
            network_obs[2] = obs_state.num_warning_alerts_recent
            network_obs[3] = obs_state.sum_priority_alerts_recent
            network_obs[4] = obs_state.num_alerts_total
            network_obs[5] = obs_state.sum_priority_alerts_total
            network_obs[6] = obs_state.num_severe_alerts_total
            network_obs[7] = obs_state.num_warning_alerts_total
        else:
            network_obs = np.zeros(0)
        for i in range(num_machines):

            if len(obs_state.machines) > i:
                machines_obs[i][0] = i + 1
                obs_state.machines[i].sort_ports()

                # IP
                host_ip = int(obs_state.machines[i].ip.rsplit(".", 1)[-1])
                machines_obs[i][1] = host_ip

                # OS
                os_id = os_lookup[obs_state.machines[i].os]
                machines_obs[i][2] = os_id

                # Num Open Ports
                machines_obs[i][3] = len(obs_state.machines[i].ports)

                # Num flags
                machines_obs[i][4] = obs_state.machines[i].num_flags

                # Num open connections
                machines_obs[i][5] = obs_state.machines[i].num_open_connections

                # Num failed login attempts
                machines_obs[i][6] = obs_state.machines[i].num_failed_login_attempts

                # Num users
                machines_obs[i][7] = obs_state.machines[i].num_users

                # Num logged in users
                machines_obs[i][8] = obs_state.machines[i].num_logged_in_users

                # Num login events
                machines_obs[i][9] = obs_state.machines[i].num_login_events

                # Num processes
                machines_obs[i][10] = obs_state.machines[i].num_processes

        return machines_obs, network_obs

    @staticmethod
    def essential_representation_spaces(obs_state: DefenderObservationState) -> Tuple:
        """
        Configures observation spaces for the essential representation

        :param obs_state: the observation state
        :return: m_selection_obs_space (for AR), network_orig_shape, machine_orig_shape, m_action_obs_space (for AR)
        """
        num_network_features = 4
        num_m_features = 7
        observation_space = gym.spaces.Box(low=0, high=1000, dtype=np.float32, shape=(
            obs_state.num_machines * num_m_features + num_network_features,))
        return observation_space

    @staticmethod
    def essential_representation(num_machines: int, obs_state: DefenderObservationState,
                            os_lookup: dict,
                            ids: bool = False) \
            -> Tuple[np.ndarray, np.ndarray]:
        """
        Base observation representation, includes all available information. E.g. for each machine: ports, ip, os,
        vulnerabilities, services, cvss, shell, root, flags, etc.

        :param num_machines: max number of machines in the obs
        :param obs_state: current observation state to turn into a numeratical representation
        :param os_lookup: lookup dict for converting categorical os into numerical
        :param ids: whether ids is enabled or not
        :return: Machines obs, ports obs, obs_space, m_selection_obs_space (for AR), network_orig_shape,
                 machine_orig_shape, m_action_obs_space (for AR)
        """
        obs_state.sort_machines()
        num_m_features = 7
        num_network_features = 4
        machines_obs = np.zeros((num_machines, num_m_features))
        if ids:
            network_obs = np.zeros(num_network_features)
            network_obs[0] = obs_state.num_alerts_recent
            network_obs[1] = obs_state.num_severe_alerts_recent
            network_obs[2] = obs_state.num_warning_alerts_recent
            network_obs[3] = obs_state.sum_priority_alerts_recent
        else:
            network_obs = np.zeros(0)
        for i in range(num_machines):

            if len(obs_state.machines) > i:
                machines_obs[i][0] = i + 1
                obs_state.machines[i].sort_ports()

                # IP
                host_ip = int(obs_state.machines[i].ip.rsplit(".", 1)[-1])
                machines_obs[i][1] = host_ip

                # Num Open Ports
                machines_obs[i][2] = len(obs_state.machines[i].ports)

                # Num open connections
                machines_obs[i][3] = obs_state.machines[i].num_open_connections

                # Num failed login attempts
                machines_obs[i][4] = obs_state.machines[i].num_failed_login_attempts

                # Num logged in users
                machines_obs[i][5] = obs_state.machines[i].num_logged_in_users

                # Num login events
                machines_obs[i][6] = obs_state.machines[i].num_login_events


        return machines_obs, network_obs
