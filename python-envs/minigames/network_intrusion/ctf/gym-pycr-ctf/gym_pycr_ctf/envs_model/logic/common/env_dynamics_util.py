from typing import List, Tuple
import numpy as np
from gym_pycr_ctf.dao.observation.attacker.attacker_machine_observation_state import AttackerMachineObservationState
from gym_pycr_ctf.dao.observation.common.port_observation_state import PortObservationState
from gym_pycr_ctf.dao.observation.common.vulnerability_observation_state import VulnerabilityObservationState
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.network.env_state import EnvState
from gym_pycr_ctf.dao.action.attacker.attacker_action import AttackerAction
from gym_pycr_ctf.dao.action.attacker.attacker_action_id import AttackerActionId
from gym_pycr_ctf.dao.observation.attacker.attacker_observation_state import AttackerObservationState
import gym_pycr_ctf.constants.constants as constants
from gym_pycr_ctf.dao.action.attacker.attacker_action_config import AttackerActionConfig
from gym_pycr_ctf.dao.network.network_outcome import NetworkOutcome


class EnvDynamicsUtil:
    """
    Class containing common utilities that are used both in simulation-mode and in emulation-mode.
    """

    @staticmethod
    def merge_complete_obs_state(old_obs_state: AttackerObservationState, new_obs_state : AttackerObservationState,
                                 env_config: EnvConfig) -> AttackerObservationState:
        """
        Merges an old observation state with a new one

        :param old_obs_state: the old observation state
        :param new_obs_state: the new observation state
        :param env_config: the environment configuration
        :return: the merged observation state
        """
        merged_obs_state = old_obs_state.copy()
        merged_obs_state.num_machines = max(old_obs_state.num_machines, new_obs_state.num_machines)
        merged_obs_state.num_ports = max(old_obs_state.num_ports, new_obs_state.num_ports)
        merged_obs_state.num_vuln = max(old_obs_state.num_vuln, new_obs_state.num_vuln)
        merged_obs_state.num_flags = max(old_obs_state.num_flags, new_obs_state.num_flags)
        merged_obs_state.catched_flags = max(old_obs_state.catched_flags, new_obs_state.catched_flags)
        net_outcome = EnvDynamicsUtil.merge_new_obs_with_old(old_obs_state.machines, new_obs_state.machines,
                                                                           env_config=env_config, action=None)
        merged_obs_state.machines = net_outcome.attacker_machine_observations
        merged_obs_state.num_sh = max(old_obs_state.num_sh, new_obs_state.num_sh)
        merged_obs_state.agent_reachable = old_obs_state.agent_reachable.union(new_obs_state.agent_reachable)
        return merged_obs_state

    @staticmethod
    def merge_new_obs_with_old(old_machines_obs: List[AttackerMachineObservationState],
                               new_machines_obs: List[AttackerMachineObservationState], env_config: EnvConfig,
                               action : AttackerAction) -> NetworkOutcome:
        """
        Helper function for merging an old network observation with new information collected

        :param old_machines_obs: the list of old machine observations
        :param new_machines_obs: the list of newly collected information
        :param env_config: environment config
        :param action: the action
        :return: the merged network outcome
        """
        net_outcome = NetworkOutcome()
        new_machines_obs = EnvDynamicsUtil.merge_duplicate_machines(machines=new_machines_obs, action=action)

        # Add updated machines to merged state
        for n_m in new_machines_obs:
            if n_m.ip == env_config.hacker_ip or n_m.ip in env_config.blacklist_ips:
                continue
            exists = False
            merged_m = n_m
            for i, o_m in enumerate(old_machines_obs):
                if n_m.ip == o_m.ip:
                    new_net_outcome = EnvDynamicsUtil.merge_new_machine_obs_with_old_machine_obs(o_m, n_m, action)
                    net_outcome.update_counts(new_net_outcome)
                    merged_m = new_net_outcome.attacker_machine_observation
                    exists = True
            net_outcome.attacker_machine_observations.append(merged_m)
            if not exists:
                net_outcome.update_counts_machine(merged_m)

        # Add old machines to merged state
        for o_m in old_machines_obs:
            exists = False
            for m_m in net_outcome.attacker_machine_observations:
                if o_m.ip == m_m.ip:
                    exists = True
            if not exists:
                net_outcome.attacker_machine_observations.append(o_m)

        return net_outcome

    @staticmethod
    def merge_new_machine_obs_with_old_machine_obs(o_m: AttackerMachineObservationState,
                                                   n_m: AttackerMachineObservationState,
                                                   action: AttackerAction) -> NetworkOutcome:
        """
        Helper function for merging an old machine observation with new information collected

        :param o_m: old machine observation
        :param n_m: newly collected machine information
        :return: the merged network outcome
        """

        net_outcome = NetworkOutcome()
        if n_m == None:
            net_outcome.attacker_machine_observation = o_m
            return net_outcome

        merged_ports, num_new_ports_found = EnvDynamicsUtil.merge_ports(o_m.ports, n_m.ports)
        n_m.ports = merged_ports
        merged_os, num_new_os_found = EnvDynamicsUtil.merge_os(o_m.os, n_m.os)
        n_m.os = merged_os
        merged_cve_vulnerabilities, num_new_cve_vuln_found = EnvDynamicsUtil.merge_vulnerabilities(o_m.cve_vulns,
                                                                                                   n_m.cve_vulns)
        n_m.cve_vulns = merged_cve_vulnerabilities
        merged_osvdb_vulnerabilities, num_new_osvdb_vuln_found = EnvDynamicsUtil.merge_vulnerabilities(o_m.osvdb_vulns,
                                                                                                   n_m.osvdb_vulns)
        n_m.osvdb_vulns = merged_osvdb_vulnerabilities
        n_m, new_shell_access = EnvDynamicsUtil.merge_shell_access(o_m, n_m)
        n_m, num_new_logged_in = EnvDynamicsUtil.merge_logged_in(o_m, n_m)
        n_m, new_root = EnvDynamicsUtil.merge_root(o_m, n_m)
        n_m, new_flag_pts = EnvDynamicsUtil.merge_flags(o_m, n_m)
        n_m = EnvDynamicsUtil.merge_connections(o_m, n_m)
        n_m = EnvDynamicsUtil.merge_filesystem_scanned(o_m, n_m, new_root)
        n_m = EnvDynamicsUtil.merge_untried_credentials(o_m, n_m, action)
        n_m = EnvDynamicsUtil.merge_trace(o_m, n_m)
        n_m = EnvDynamicsUtil.merge_exploit_tried(o_m, n_m)
        n_m = EnvDynamicsUtil.merge_backdoor_tried(o_m, n_m)
        n_m = EnvDynamicsUtil.merge_tools_tried(o_m, n_m)
        n_m, num_new_tools_installed = EnvDynamicsUtil.merge_tools_installed(o_m, n_m)
        n_m, num_new_backdoors_installed = EnvDynamicsUtil.merge_backdoor_installed(o_m, n_m)
        n_m = EnvDynamicsUtil.merge_reachable(o_m=o_m, n_m=n_m)
        n_m = EnvDynamicsUtil.merge_backdoor_credentials(o_m=o_m, n_m=n_m)

        net_outcome.attacker_machine_observation = n_m
        net_outcome.total_new_ports_found = num_new_ports_found
        net_outcome.total_new_os_found = num_new_os_found
        net_outcome.total_new_cve_vuln_found = num_new_cve_vuln_found
        net_outcome.total_new_shell_access = new_shell_access
        net_outcome.total_new_flag_pts = new_flag_pts
        net_outcome.total_new_root = new_root
        net_outcome.total_new_osvdb_vuln_found = num_new_osvdb_vuln_found
        net_outcome.total_new_logged_in = num_new_logged_in
        net_outcome.total_new_tools_installed = num_new_tools_installed
        net_outcome.total_new_backdoors_installed = num_new_backdoors_installed

        return net_outcome

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
    def merge_shell_access(o_m: AttackerMachineObservationState, n_m: AttackerMachineObservationState) -> \
            Tuple[AttackerMachineObservationState, int]:
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
    def merge_reachable(o_m: AttackerMachineObservationState, n_m: AttackerMachineObservationState) \
            -> AttackerMachineObservationState:
        """
        Helper function for merging an old machine observation reachable nodes with new information collected

        :param o_os: the old machine observation
        :param n_os: the new machine observation
        :return: the merged machine observation with updated reachable nodes
        """
        n_m.reachable = n_m.reachable.union(o_m.reachable)
        return n_m

    @staticmethod
    def merge_backdoor_credentials(o_m: AttackerMachineObservationState, n_m: AttackerMachineObservationState) \
            -> AttackerMachineObservationState:
        """
        Helper function for merging an old machine observation backdoor credentials nodes with new information collected

        :param o_os: the old machine observation
        :param n_os: the new machine observation
        :return: the merged machine observation with updated backdoor credentials nodes
        """
        n_m.backdoor_credentials = list(set(n_m.backdoor_credentials + o_m.backdoor_credentials))
        return n_m

    @staticmethod
    def merge_logged_in(o_m: AttackerMachineObservationState, n_m: AttackerMachineObservationState) \
            -> Tuple[AttackerMachineObservationState, int]:
        """
        Helper function for merging an old machine observation logged in with new information collected

        :param o_os: the old machine observation
        :param n_os: the new machine observation
        :return: the merged machine observation with updated logged-in flag, num_new_login
        """
        num_new_logged_in = 0
        if not o_m.logged_in and n_m.logged_in:
            num_new_logged_in = 1
        if not n_m.logged_in:
            n_m.logged_in = o_m.logged_in
        return n_m, num_new_logged_in

    @staticmethod
    def merge_tools_installed(o_m: AttackerMachineObservationState, n_m: AttackerMachineObservationState) \
            -> Tuple[AttackerMachineObservationState, int]:
        """
        Helper function for merging an old machine observation "tools installed flag" with new information collected

        :param o_os: the old machine observation
        :param n_os: the new machine observation
        :return: the merged machine observation with updated tools_installed flag, num_new_tools_installed
        """
        num_new_tools_installed = 0
        if not o_m.tools_installed and n_m.tools_installed:
            num_new_tools_installed = 1
        if not n_m.tools_installed:
            n_m.tools_installed = o_m.tools_installed
        return n_m, num_new_tools_installed

    @staticmethod
    def merge_backdoor_installed(o_m: AttackerMachineObservationState, n_m: AttackerMachineObservationState) \
            -> Tuple[AttackerMachineObservationState, int]:
        """
        Helper function for merging an old machine observation "backdoor installed" flag with new information collected

        :param o_os: the old machine observation
        :param n_os: the new machine observation
        :return: the merged machine observation with updated backdoor_installed flag, num_new_backdoor_installed
        """
        num_new_backdoor_installed = 0
        if not o_m.backdoor_installed and n_m.backdoor_installed:
            num_new_backdoor_installed = 1
        if not n_m.backdoor_installed:
            n_m.backdoor_installed = o_m.backdoor_installed
        return n_m, num_new_backdoor_installed

    @staticmethod
    def merge_backdoor_tried(o_m: AttackerMachineObservationState, n_m: AttackerMachineObservationState) \
            -> AttackerMachineObservationState:
        """
        Helper function for merging an old machine observation "backdoor tried" flag with new information collected

        :param o_os: the old machine observation
        :param n_os: the new machine observation
        :return: the merged machine observation with updated backdoor-tried flag
        """
        if not n_m.backdoor_tried:
            n_m.backdoor_tried = o_m.backdoor_tried
        return n_m

    @staticmethod
    def merge_tools_tried(o_m: AttackerMachineObservationState, n_m: AttackerMachineObservationState) \
            -> AttackerMachineObservationState:
        """
        Helper function for merging an old machine observation "tools tried" flag with new information collected

        :param o_os: the old machine observation
        :param n_os: the new machine observation
        :return: the merged machine observation with updated tools-installed-tried flag
        """
        if not n_m.install_tools_tried:
            n_m.install_tools_tried = o_m.install_tools_tried
        return n_m

    @staticmethod
    def merge_root(o_m: AttackerMachineObservationState, n_m: AttackerMachineObservationState) \
            -> Tuple[AttackerMachineObservationState, int]:
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
    def merge_flags(o_m: AttackerMachineObservationState, n_m: AttackerMachineObservationState) \
            -> Tuple[AttackerMachineObservationState, int]:
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
    def merge_connections(o_m: AttackerMachineObservationState, n_m: AttackerMachineObservationState) \
            -> AttackerMachineObservationState:
        """
        Helper function for merging an old machine observation shell-connections with new information collected

        :param o_os: the old machine observation
        :param n_os: the new machine observation
        :return: the merged machine observation with updated connections
        """
        n_m.ssh_connections = list(set(n_m.ssh_connections + o_m.ssh_connections))
        n_m.telnet_connections = list(set(n_m.telnet_connections + o_m.telnet_connections))
        n_m.ftp_connections = list(set(n_m.ftp_connections + o_m.ftp_connections))
        return n_m

    @staticmethod
    def merge_filesystem_scanned(o_m: AttackerMachineObservationState, n_m: AttackerMachineObservationState,
                                 new_root: int) -> AttackerMachineObservationState:
        """
        Helper function for merging an old machine observation file-system-scanned-flag with new information collected

        :param o_os: the old machine observation
        :param n_os: the new machine observation
        :param new_root: number of new root connections
        :return: the merged machine observation with updated filesystem-scanned flag
        """
        if not n_m.filesystem_searched:
            n_m.filesystem_searched = o_m.filesystem_searched
        if new_root > 0:
            n_m.filesystem_searched = False
        return n_m

    @staticmethod
    def merge_untried_credentials(o_m: AttackerMachineObservationState, n_m: AttackerMachineObservationState,
                                  action: AttackerAction) -> AttackerMachineObservationState:
        """
        Helper function for merging an old machine observation untried-credentials-flag with new information collected

        :param o_m: the old machine observation
        :param n_m: the new machine observation
        :param action: the action that was done to get n_m
        :return: the merged machine observation with updated untried-credentials flag
        """
        if action is not None and action.id == AttackerActionId.NETWORK_SERVICE_LOGIN and n_m.shell_access:
            return n_m
        else:
            if not n_m.untried_credentials:
                n_m.untried_credentials = o_m.untried_credentials
        return n_m

    @staticmethod
    def merge_exploit_tried(o_m: AttackerMachineObservationState,
                            n_m: AttackerMachineObservationState) -> AttackerMachineObservationState:
        """
        Helper function for merging an old machine observation tried_brute_flags with new information collected

        :param o_os: the old machine observation
        :param n_os: the new machine observation
        :return: the merged machine observation with updated brute-tried flags
        """
        if not n_m.telnet_brute_tried:
            n_m.telnet_brute_tried = o_m.telnet_brute_tried
        if not n_m.ssh_brute_tried:
            n_m.ssh_brute_tried = o_m.ssh_brute_tried
        if not n_m.ftp_brute_tried:
            n_m.ftp_brute_tried = o_m.ftp_brute_tried
        if not n_m.cassandra_brute_tried:
            n_m.cassandra_brute_tried = o_m.cassandra_brute_tried
        if not n_m.irc_brute_tried:
            n_m.irc_brute_tried = o_m.irc_brute_tried
        if not n_m.mongo_brute_tried:
            n_m.mongo_brute_tried = o_m.mongo_brute_tried
        if not n_m.mysql_brute_tried:
            n_m.mysql_brute_tried = o_m.mysql_brute_tried
        if not n_m.smtp_brute_tried:
            n_m.smtp_brute_tried = o_m.smtp_brute_tried
        if not n_m.postgres_brute_tried:
            n_m.postgres_brute_tried = o_m.postgres_brute_tried
        if not n_m.sambacry_tried:
            n_m.sambacry_tried = o_m.sambacry_tried
        if not n_m.shellshock_tried:
            n_m.shellshock_tried = o_m.shellshock_tried
        if not n_m.dvwa_sql_injection_tried:
            n_m.dvwa_sql_injection_tried = o_m.dvwa_sql_injection_tried
        if not n_m.cve_2015_3306_tried:
            n_m.cve_2015_3306_tried = o_m.cve_2015_3306_tried
        if not n_m.cve_2015_1427_tried:
            n_m.cve_2015_1427_tried = o_m.cve_2015_1427_tried
        if not n_m.cve_2016_10033_tried:
            n_m.cve_2016_10033_tried = o_m.cve_2016_10033_tried
        if not n_m.cve_2010_0426_tried:
            n_m.cve_2010_0426_tried = o_m.cve_2010_0426_tried
        if not n_m.cve_2015_5602_tried:
            n_m.cve_2015_5602_tried = o_m.cve_2015_5602_tried
        return n_m

    @staticmethod
    def merge_trace(o_m: AttackerMachineObservationState, n_m: AttackerMachineObservationState) -> AttackerMachineObservationState:
        """
        Helper function for merging an old machine observation trace with new information collected

        :param o_os: the old machine observation
        :param n_os: the new machine observation
        :return: the merged machine observation with updated trace
        """
        if n_m.trace == None:
            n_m.trace = o_m.trace
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
    def reward_function(net_outcome: NetworkOutcome, env_config: EnvConfig  = None,
                        action: AttackerAction = None) -> float:
        """
        Implements the reward function

        :param net_outcome: the outcome statistics
        :param env_config: the environment configuration
        :param action: the action
        :return: reward
        """
        reward = env_config.attacker_port_found_reward_mult * net_outcome.total_new_ports_found + \
                 env_config.attacker_os_found_reward_mult * net_outcome.total_new_os_found + \
                 env_config.attacker_cve_vuln_found_reward_mult * net_outcome.total_new_cve_vuln_found + \
                 env_config.attacker_machine_found_reward_mult * net_outcome.total_new_machines_found + \
                 env_config.attacker_shell_access_found_reward_mult * net_outcome.total_new_shell_access + \
                 env_config.attacker_root_found_reward_mult * net_outcome.total_new_root + \
                 env_config.attacker_flag_found_reward_mult * net_outcome.total_new_flag_pts + \
                 env_config.attacker_osvdb_vuln_found_reward_mult * net_outcome.total_new_osvdb_vuln_found + \
                 env_config.attacker_new_login_reward_mult * net_outcome.total_new_logged_in+ \
                 env_config.attacker_new_tools_installed_reward_mult * net_outcome.total_new_tools_installed + \
                 env_config.attacker_new_backdoors_installed_reward_mult * net_outcome.total_new_backdoors_installed

        new_info = [net_outcome.total_new_ports_found, net_outcome.total_new_os_found,
                    net_outcome.total_new_cve_vuln_found, net_outcome.total_new_machines_found,
                    net_outcome.total_new_shell_access, net_outcome.total_new_root, net_outcome.total_new_flag_pts,
                    net_outcome.total_new_osvdb_vuln_found,
                    net_outcome.total_new_logged_in, net_outcome.total_new_tools_installed,
                    net_outcome.total_new_tools_installed]

        cost = EnvDynamicsUtil.normalize_action_costs(action=action, env_config=env_config)*env_config.attacker_cost_coefficient

        alerts_pts = 0
        if env_config.ids_router and action.alerts is not None:
            alerts_pts = EnvDynamicsUtil.normalize_action_alerts(action=action, env_config=env_config)*env_config.attacker_alerts_coefficient

        reward = float(reward) + float(env_config.attacker_base_step_reward) - float(cost) - float(alerts_pts)
        return reward

    @staticmethod
    def emulate_detection(net_outcome: NetworkOutcome, env_config: EnvConfig = None,
                          action: AttackerAction = None) -> Tuple[bool, int]:
        """
        Emulates a detection by the IDS by implementing a threshold policy

        :param net_outcome: the observed network outcome
        :param env_config: the environment configuration
        :param action: the action
        :return: detected, reward
        """
        if env_config.emulate_detection:
            detected = False
            if action.alerts is not None:
                num_alerts = action.alerts[0]
            else:
                num_alerts = 0

            if num_alerts > env_config.detection_alerts_threshold:
                det_p = (num_alerts / env_config.attacker_max_alerts) * env_config.detection_prob_factor
                detected = np.random.rand() < det_p
                # print("detection prob:{}, detected:{}, max_alets:{}, num_alerts:{}".format(
                #     det_p, detected, env_config.attacker_max_alerts, num_alerts))

            r = env_config.attacker_detection_reward

            if not detected:
                r = 0

            return detected, r
        else:
            return False, 0

    @staticmethod
    def is_all_flags_collected(s: EnvState, env_config: EnvConfig) -> bool:
        """
        Checks if all flags are collected (then episode is done)

        :param s: current state
        :param env_config: environment config
        :return: True if all flags are collected otherwise false
        """
        total_flags = set()
        for key, flag in env_config.network_conf.flags_lookup.items():
            total_flags.add(flag)
        found_flags = set()
        for node in s.attacker_obs_state.machines:
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

    @staticmethod
    def exploit_tried_flags(a: AttackerAction, m_obs: AttackerMachineObservationState):
        """
        Utility function for updating exploit-tried flags

        :param a: the action
        :param m_obs: the observation to update
        :return: the updated observation
        """
        # Subnet scans sometimes fail due to stagnation, https://github.com/nmap/nmap/issues/1321
        if (a.id == AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_SUBNET and m_obs.untried_credentials) \
                or a.id == AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST:
            m_obs.ftp_brute_tried = True
        elif (a.id == AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_SUBNET and m_obs.untried_credentials) \
                or a.id == AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST:
            m_obs.ssh_brute_tried = True
        elif (a.id == AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_SUBNET and m_obs.untried_credentials) \
                or a.id == AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST:
            m_obs.telnet_brute_tried = True
        elif (a.id == AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_SUBNET and m_obs.untried_credentials) \
                or a.id == AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST:
            m_obs.irc_brute_tried = True
        elif (a.id == AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_SUBNET and m_obs.untried_credentials) \
                or a.id == AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST:
            m_obs.postgres_brute_tried = True
        elif (a.id == AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_SUBNET and m_obs.untried_credentials) \
                or a.id == AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST:
            m_obs.smtp_brute_tried = True
        elif (a.id == AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_SUBNET and m_obs.untried_credentials) \
                or a.id == AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST:
            m_obs.mysql_brute_tried = True
        elif (a.id == AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_SUBNET and m_obs.untried_credentials)\
                or a.id == AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST:
            m_obs.mongo_brute_tried = True
        elif (a.id == AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_SUBNET and m_obs.untried_credentials) \
                or a.id == AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST:
            m_obs.cassandra_brute_tried = True
        elif a.id == AttackerActionId.SAMBACRY_EXPLOIT:
            m_obs.sambacry_tried = True
        elif a.id == AttackerActionId.SHELLSHOCK_EXPLOIT:
            m_obs.shellshock_tried = True
        elif a.id == AttackerActionId.DVWA_SQL_INJECTION:
            m_obs.dvwa_sql_injection_tried = True
        elif a.id == AttackerActionId.CVE_2015_3306_EXPLOIT:
            m_obs.cve_2015_3306_tried = True
        elif a.id == AttackerActionId.CVE_2015_1427_EXPLOIT:
            m_obs.cve_2015_1427_tried = True
        elif a.id == AttackerActionId.CVE_2016_10033_EXPLOIT:
            m_obs.cve_2016_10033_tried = True
        elif a.id == AttackerActionId.CVE_2010_0426_PRIV_ESC:
            m_obs.cve_2010_0426_tried = True
        elif a.id == AttackerActionId.CVE_2015_5602_PRIV_ESC:
            m_obs.cve_2015_5602_tried = True
        return m_obs

    @staticmethod
    def ssh_backdoor_tried_flags(a: AttackerAction, m_obs: AttackerMachineObservationState):
        """
        Utility function for updating install-backdoor flag

        :param a: the action
        :param m_obs: the observation to update
        :return: the updated observation
        """
        if a.id == AttackerActionId.SSH_BACKDOOR:
            m_obs.backdoor_tried = True
        return m_obs

    @staticmethod
    def install_tools_tried(a: AttackerAction, m_obs: AttackerMachineObservationState):
        """
        Utility function for updating install-tools flag

        :param a: the action
        :param m_obs: the observation to update
        :return: the updated observation
        """
        if a.id == AttackerActionId.INSTALL_TOOLS:
            m_obs.install_tools_tried = True
        return m_obs

    @staticmethod
    def cache_action(env_config: EnvConfig, a: AttackerAction, s: EnvState) -> None:
        """
        Utility function for caching an action

        :param env_config: the environment configuration
        :param a: the action to cache
        :param s: the current state
        :return: None
        """
        logged_in_ips_str = EnvDynamicsUtil.logged_in_ips_str(env_config=env_config, a=a, s=s)
        s.attacker_obs_state.actions_tried.add((a.id, a.index, logged_in_ips_str))

    @staticmethod
    def logged_in_ips_str(env_config: EnvConfig, a: AttackerAction, s: EnvState) -> str:
        """
        Utility function to getting a string-id of the attacker state (Q) of logged in machines

        :param env_config: the environment config
        :param a: the action
        :param s: the current state
        :return: the string id
        """
        hacker_ip = env_config.hacker_ip
        logged_in_ips = list(map(lambda x: x.ip + "_tools=" + str(int(x.tools_installed)) + "_backdoor="
                                           + str(int(x.backdoor_installed)) + "_root=" + str(int(x.root)),
                                 filter(lambda x: x.logged_in, s.attacker_obs_state.machines)))
        logged_in_ips.append(hacker_ip)
        logged_in_ips = sorted(logged_in_ips, key=lambda x: x)
        logged_in_ips_str = "_".join(logged_in_ips)
        return logged_in_ips_str

    @staticmethod
    def exploit_get_vuln_name(a: AttackerAction) -> str:
        """
        Utiltiy function to get the vulnerability name of a particular exploit action

        :param a: the action
        :return: the name of hte corresponding vulnerability
        """
        if a.id == AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.EXPLOIT_VULNERABILITES.FTP_DICT_SAME_USER_PASS
        elif a.id == AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.EXPLOIT_VULNERABILITES.SSH_DICT_SAME_USER_PASS
        elif a.id == AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.EXPLOIT_VULNERABILITES.TELNET_DICTS_SAME_USER_PASS
        elif a.id == AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_SUBNET:
            return constants.EXPLOIT_VULNERABILITES.IRC_DICTS_SAME_USER_PASS
        elif a.id == AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.EXPLOIT_VULNERABILITES.POSTGRES_DICTS_SAME_USER_PASS
        elif a.id == AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.EXPLOIT_VULNERABILITES.SMTP_DICTS_SAME_USER_PASS
        elif a.id == AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.EXPLOIT_VULNERABILITES.MYSQL_DICTS_SAME_USER_PASS
        elif a.id == AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.EXPLOIT_VULNERABILITES.MONGO_DICTS_SAME_USER_PASS
        elif a.id == AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.EXPLOIT_VULNERABILITES.CASSANDRA_DICTS_SAME_USER_PASS
        return constants.EXPLOIT_VULNERABILITES.UNKNOWN

    @staticmethod
    def exploit_get_vuln_cvss(a: AttackerAction) -> float:
        """
        Utility function for getting the CVSS of an exploit action

        :param a: the action
        :return: the CVSS
        """
        if a.id in AttackerActionConfig.dict_brute_same_user_ids():
            return constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS
        return 0.0

    @staticmethod
    def exploit_get_service_name(a: AttackerAction) -> str:
        """
        Utility function to get the name of the exploited service of a particular exploit action

        :param a: the action
        :return: the name of the service
        """
        if a.id == AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.FTP.SERVICE_NAME
        elif a.id == AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.SSH.SERVICE_NAME
        elif a.id == AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.TELNET.SERVICE_NAME
        elif a.id == AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_SUBNET:
            return constants.IRC.SERVICE_NAME
        elif a.id == AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.POSTGRES.SERVICE_NAME
        elif a.id == AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.SMTP.SERVICE_NAME
        elif a.id == AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.MYSQL.SERVICE_NAME
        elif a.id == AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.MONGO.SERVICE_NAME
        elif a.id == AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.CASSANDRA.SERVICE_NAME
        return constants.EXPLOIT_VULNERABILITES.UNKNOWN


    @staticmethod
    def merge_duplicate_machines(machines : List[AttackerMachineObservationState], action: AttackerAction) \
            -> List[AttackerMachineObservationState]:
        """
        Utility function for merging machines that are duplicates

        :param machines: list of machines (possibly with duplicates)
        :param action: the action that generated the new machines
        :return: the merged set of machines
        """
        merged_machines = []
        ips = set()
        for m in machines:
            if m.ip not in ips:
                merged_m = m
                for m2 in machines:
                    if m2.ip == merged_m.ip:
                        net_out = EnvDynamicsUtil.merge_new_machine_obs_with_old_machine_obs(merged_m, m2, action)
                        merged_m = net_out.attacker_machine_observation
                merged_machines.append(merged_m)
                ips.add(m.ip)
        return merged_machines


    @staticmethod
    def normalize_action_costs(action : AttackerAction, env_config: EnvConfig) -> float:
        """
        Normalize action costs

        :param action: the attacker aciton
        :param env_config: the environment configuration
        :return: the normalized cost
        """
        return ((action.cost) / env_config.attacker_max_costs) \
        * env_config.normalize_costs_max

    @staticmethod
    def normalize_action_alerts(action : AttackerAction, env_config: EnvConfig) -> float:
        """
        Normalize action alerts

        :param action: the attacker action
        :param env_config: the environment configuration
        :return: the normalized alerts pts
        """
        return ((action.alerts[0]) / env_config.attacker_max_alerts) \
          * env_config.normalize_alerts_max
