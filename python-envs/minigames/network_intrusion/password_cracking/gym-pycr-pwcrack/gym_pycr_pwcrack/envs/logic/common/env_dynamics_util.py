from typing import List, Tuple
from gym_pycr_pwcrack.dao.observation.machine_observation_state import MachineObservationState
from gym_pycr_pwcrack.dao.observation.port_observation_state import PortObservationState
from gym_pycr_pwcrack.dao.observation.vulnerability_observation_state import VulnerabilityObservationState
from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.dao.network.env_state import EnvState

class EnvDynamicsUtil:
    """
    Class containing common utilities that are used both in simulation-mode and in cluster-mode.
    """

    @staticmethod
    def merge_new_obs_with_old(old_machines_obs: List[MachineObservationState],
                               new_machines_obs: List[MachineObservationState], env_config: EnvConfig) -> \
            Tuple[List[MachineObservationState], int, int, int, int, int, int]:
        """
        Helper function for merging an old network observation with new information collected

        :param old_machines_obs: the list of old machine observations
        :param new_machines_obs: the list of newly collected information
        :param env_config: environment config
        :return: the merged machine information, n_new_ports, n_new_os, n_new_vuln, n_new_m, new_s_a
        """
        merged_machines = []
        total_new_ports_found, total_new_os_found, total_new_vuln_found, total_new_machines, total_new_shell_access, \
        total_new_root, total_new_flag_pts = 0, 0, 0, 0, 0, 0, 0

        # Add updated machines to merged state
        for n_m in new_machines_obs:
            if n_m.ip == env_config.hacker_ip:
                continue
            exists = False
            merged_m = n_m
            for i, o_m in enumerate(old_machines_obs):
                if n_m.ip == o_m.ip:
                    merged_m, num_new_ports_found, num_new_os_found, num_new_vuln_found, new_shell_access, new_root, \
                    new_flag_pts = EnvDynamicsUtil.merge_new_machine_obs_with_old_machine_obs(o_m, n_m)
                    total_new_ports_found += num_new_ports_found
                    total_new_os_found += num_new_os_found
                    total_new_vuln_found += num_new_vuln_found
                    total_new_shell_access += new_shell_access
                    total_new_root += new_root
                    total_new_flag_pts += new_flag_pts
                    exists = True
            merged_machines.append(merged_m)
            if not exists:
                total_new_ports_found += len(merged_m.ports)
                new_os = 0 if merged_m.os == "unknown" else 1
                total_new_os_found += new_os
                total_new_vuln_found += len(merged_m.vuln)
                total_new_machines += 1

        # Add old machines to merged state
        for o_m in old_machines_obs:
            exists = False
            for m_m in merged_machines:
                if o_m.ip == m_m.ip:
                    exists = True
            if not exists:
                merged_machines.append(o_m)

        return merged_machines, total_new_ports_found, total_new_os_found, total_new_vuln_found, total_new_machines, \
               total_new_shell_access, total_new_flag_pts, total_new_root

    @staticmethod
    def merge_new_machine_obs_with_old_machine_obs(o_m: MachineObservationState, n_m: MachineObservationState) \
            -> Tuple[MachineObservationState, int, int, int, int, int, int]:
        """
        Helper function for merging an old machine observation with new information collected

        :param o_m: old machine observation
        :param n_m: newly collected machine information
        :return: the merged machine observation state, n_new_ports, n_new_os, n_new_vuln, new_access, new_root, new_fl
        """
        if n_m == None:
            return o_m, 0, 0, 0, 0, 0, 0
        merged_ports, num_new_ports_found = EnvDynamicsUtil.merge_ports(o_m.ports, n_m.ports)
        n_m.ports = merged_ports
        merged_os, num_new_os_found = EnvDynamicsUtil.merge_os(o_m.os, n_m.os)
        n_m.os = merged_os
        merged_vulnerabilities, num_new_vuln_found = EnvDynamicsUtil.merge_vulnerabilities(o_m.vuln, n_m.vuln)
        n_m.vuln = merged_vulnerabilities
        n_m, new_shell_access = EnvDynamicsUtil.merge_shell_access(o_m, n_m)
        n_m = EnvDynamicsUtil.merge_logged_in(o_m, n_m)
        n_m, new_root = EnvDynamicsUtil.merge_root(o_m, n_m)
        n_m, new_flag_pts = EnvDynamicsUtil.merge_flags(o_m, n_m)
        n_m = EnvDynamicsUtil.merge_connections(o_m, n_m)
        return n_m, num_new_ports_found, num_new_os_found, num_new_vuln_found, new_shell_access, new_root, new_flag_pts

    @staticmethod
    def merge_os(o_os: str, n_os: str) -> Tuple[str, int]:
        """
        Helper function for merging an old machine observation OS with new information collected

        :param o_os: the old OS
        :param n_os: the newly observed OS
        :return: the merged os, 1 if it was a newly detected OS, otherwise 0
        """
        merged_os = n_os
        if n_os == "unknown" and o_os != "unknown":
            merged_os = o_os
        new_os = 0 if merged_os == o_os else 1
        return merged_os, new_os

    @staticmethod
    def merge_shell_access(o_m: MachineObservationState, n_m: MachineObservationState) -> \
            Tuple[MachineObservationState, int]:
        """
        Helper function for merging an old machine observation shell access with new information collected

        :param o_os: the old machine observation
        :param n_os: the new machine observation
        :return: the merged machine observation with update shell-access parameters, 1 if new access otherwise 0
        """
        new_access = 0
        if not o_m.shell_access and n_m.shell_access:
            new_access = 1
            merged_credentials = o_m.shell_access_credentials
            for cr in n_m.shell_access_credentials:
                duplicate = False
                for cr_2 in o_m.shell_access_credentials:
                    if cr == cr_2:
                        duplicate = True
                if not duplicate:
                    merged_credentials.append(cr)
            n_m.shell_access_credentials = merged_credentials
        if not n_m.shell_access:
            n_m.shell_access = o_m.shell_access
            n_m.shell_access_credentials = o_m.shell_access_credentials
        return n_m, new_access

    @staticmethod
    def merge_logged_in(o_m: MachineObservationState, n_m: MachineObservationState) -> MachineObservationState:
        """
        Helper function for merging an old machine observation logged in with new information collected

        :param o_os: the old machine observation
        :param n_os: the new machine observation
        :return: the merged machine observation with updated logged-in flag
        """
        if not n_m.logged_in:
            n_m.logged_in = o_m.logged_in
        return n_m

    @staticmethod
    def merge_root(o_m: MachineObservationState, n_m: MachineObservationState) -> MachineObservationState:
        """
        Helper function for merging an old machine observation root with new information collected

        :param o_os: the old machine observation
        :param n_os: the new machine observation
        :return: the merged machine observation with updated root flag, 1 if new root otherwise 0
        """
        new_root = 0
        if not o_m.root and n_m.root:
            new_root = 1
        if not n_m.root:
            n_m.root = o_m.root
        return n_m, new_root

    @staticmethod
    def merge_flags(o_m: MachineObservationState, n_m: MachineObservationState) -> MachineObservationState:
        """
        Helper function for merging an old machine observation flags with new information collected

        :param o_os: the old machine observation
        :param n_os: the new machine observation
        :return: the merged machine observation with updated flags, number of new flag points
        """
        new_flag_points = 0
        for flag in n_m.flags_found:
            if flag not in o_m.flags_found:
                new_flag_points += flag.score
        n_m.flags_found = n_m.flags_found.union(o_m.flags_found)
        return n_m, new_flag_points

    @staticmethod
    def merge_connections(o_m: MachineObservationState, n_m: MachineObservationState) -> MachineObservationState:
        """
        Helper function for merging an old machine observation shell-connections with new information collected

        :param o_os: the old machine observation
        :param n_os: the new machine observation
        :return: the merged machine observation with updated connections
        """
        # Stale connections are removed
        if len(n_m.ssh_connections) == 0:
            n_m.ssh_connections = o_m.ssh_connections
        if len(n_m.telnet_connections) == 0:
            n_m.telnet_connections = o_m.telnet_connections
        if len(n_m.ftp_connections) == 0:
            n_m.ftp_connections = o_m.ftp_connections
        return n_m

    @staticmethod
    def merge_ports(o_ports: List[PortObservationState], n_ports: List[PortObservationState], acc: bool = True) \
            -> Tuple[List[PortObservationState], int]:
        """
        Helper function for merging two port lists

        :param o_ports: old list of ports
        :param n_ports: new list of ports
        :param acc: if true, accumulate port observations rather than overwrite
        :return: the merged port list, number of new ports found
        """
        num_new_ports_found = 0
        if n_ports == None or len(n_ports) == 0:
            return o_ports, num_new_ports_found
        merged_ports = n_ports
        for m_p in merged_ports:
            exist = False
            for o_p in o_ports:
                if o_p.port == m_p.port and o_p.protocol == m_p.protocol and o_p.service == m_p.service \
                        and o_p.open == m_p.open:
                    exist = True
            if not exist:
                num_new_ports_found += 1
        if acc:
            for o_p in o_ports:
                exist = False
                for m_p in merged_ports:
                    if o_p.port == m_p.port and o_p.protocol == m_p.protocol:
                        exist = True
                if not exist:
                    merged_ports.append(o_p)
        return merged_ports, num_new_ports_found

    @staticmethod
    def merge_vulnerabilities(o_vuln: List[VulnerabilityObservationState], n_vuln: List[VulnerabilityObservationState],
                              acc: bool = True) -> Tuple[List[VulnerabilityObservationState], int]:
        """
        Helper function for merging two vulnerability lists lists

        :param o_vuln: old list of vulnerabilities
        :param n_vuln: new list of vulnerabilities
        :param acc: if true, accumulate vulnerability observations rather than overwrite
        :return: the merged vulnerability list, number of new vulnerabilities detected
        """
        num_new_vuln_found = 0
        if n_vuln == None or len(n_vuln) == 0:
            return o_vuln, num_new_vuln_found
        merged_vuln = n_vuln
        for m_v in merged_vuln:
            exist = False
            for o_v in o_vuln:
                if o_v.name == m_v.name:
                    exist = True
            if not exist:
                num_new_vuln_found += 1
        if acc:
            for o_v in o_vuln:
                exist = False
                for m_v in merged_vuln:
                    if o_v.name == m_v.name:
                        exist = True
                if not exist:
                    merged_vuln.append(o_v)
        return merged_vuln, num_new_vuln_found

    @staticmethod
    def reward_function(num_new_ports_found: int = 0, num_new_os_found: int = 0, num_new_vuln_found: int = 0,
                        num_new_machines: int = 0, num_new_shell_access: int = 0, num_new_root: int = 0,
                        num_new_flag_pts: int = 0, cost: float = 0.0, env_config: EnvConfig  = None) -> int:
        """
        Implements the reward function

        :param num_new_ports_found: number of new ports detected
        :param num_new_os_found: number of new operating systems detected
        :param num_new_vuln_found: number of new vulnerabilities detected
        :param num_new_machines: number of new machines
        :param num_new_shell_access: number of new shell access to different machines
        :param num_new_root: number of new root access to different machines
        :param cost: cost of the action that was performed
        :param env_config: env config
        :return: reward
        """
        reward = env_config.port_found_reward_mult*num_new_ports_found + \
                 env_config.os_found_reward_mult*num_new_os_found + \
                 env_config.vuln_found_reward_mult*num_new_vuln_found + \
                 env_config.machine_found_reward_mult*num_new_machines + \
                 env_config.shell_access_found_reward_mult*num_new_shell_access + \
                 env_config.root_found_reward_mult*num_new_root + \
                 env_config.flag_found_reward_mult* num_new_flag_pts
        cost = cost*env_config.cost_coefficient
        reward = int((reward - cost))
        return reward

    @staticmethod
    def is_all_flags_collected(s: EnvState, env_config: EnvConfig) -> bool:
        """
        Checks if all flags are collected (then episode is done)

        :param s: current state
        :param env_config: environment config
        :return: True if all flags are collected otherwise false
        """
        total_flags = set()
        for node in env_config.network_conf.nodes:
            for flag in node.flags:
                total_flags.add(flag)
        found_flags = set()
        for node in s.obs_state.machines:
            found_flags = found_flags.union(node.flags_found)

        return total_flags == found_flags


    @staticmethod
    def check_if_ssh_connection_is_alive(conn) -> bool:
        """
        Utility function to check whether a SSH connection is alive or not
        :param conn: the connection to check
        :return: true or false
        """
        alive = False
        if conn.get_transport() is not None:
            alive = conn.get_transport().is_active()
        return alive

    @staticmethod
    def check_if_telnet_connection_is_alive(conn) -> bool:
        """
        Utility function to check whether a Telnet connection is alive or not

        :param conn: the connection to check
        :return: true or false
        """
        return True

    @staticmethod
    def check_if_ftp_connection_is_alive(conn) -> bool:
        """
        Utilitty function to check whether a FTP connection is alive or not

        :param conn: the connection to check
        :return: true or false
        """
        return True

