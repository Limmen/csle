from typing import List, Tuple, Union, Set, Any
import csle_common.constants.constants as constants
from csle_common.dao.emulation_observation.attacker.emulation_attacker_machine_observation_state \
    import EmulationAttackerMachineObservationState
from csle_common.dao.emulation_observation.common.emulation_port_observation_state \
    import EmulationPortObservationState
from csle_common.dao.emulation_observation.common.emulation_vulnerability_observation_state \
    import EmulationVulnerabilityObservationState
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_observation.attacker.emulation_attacker_observation_state \
    import EmulationAttackerObservationState
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_config import EmulationAttackerActionConfig


class EnvDynamicsUtil:
    """
    Class containing common utilities that are used both in simulation-mode and in emulation-mode.
    """

    @staticmethod
    def merge_complete_obs_state(old_obs_state: EmulationAttackerObservationState,
                                 new_obs_state: EmulationAttackerObservationState,
                                 emulation_env_config: EmulationEnvConfig) -> EmulationAttackerObservationState:
        """
        Merges an old observation state with a new one

        :param old_obs_state: the old observation state
        :param new_obs_state: the new observation state
        :param emulation_env_config: the emulation environment configuration
        :return: the merged observation state
        """
        merged_obs_state = old_obs_state.copy()
        merged_obs_state.catched_flags = max(old_obs_state.catched_flags, new_obs_state.catched_flags)
        merged_obs_state.machines = EnvDynamicsUtil.merge_new_obs_with_old(
            old_obs_state.machines, new_obs_state.machines, emulation_env_config=emulation_env_config, action=None)
        merged_obs_state.agent_reachable = old_obs_state.agent_reachable.union(new_obs_state.agent_reachable)
        return merged_obs_state

    @staticmethod
    def merge_new_obs_with_old(old_machines_obs: List[EmulationAttackerMachineObservationState],
                               new_machines_obs: List[EmulationAttackerMachineObservationState],
                               emulation_env_config: EmulationEnvConfig,
                               action: Union[EmulationAttackerAction, None]) \
            -> List[EmulationAttackerMachineObservationState]:
        """
        Helper function for merging an old network observation with new information collected

        :param old_machines_obs: the list of old machine observations
        :param new_machines_obs: the list of newly collected information
        :param emulation_env_config: environment config
        :param action: the action
        :return: the merged machine observations
        """
        if action is None:
            raise ValueError("action is None")
        new_machines_obs = EnvDynamicsUtil.merge_duplicate_machines(machines=new_machines_obs, action=action)
        attacker_machine_observations = []
        # Add updated machines to merged state
        for n_m in new_machines_obs:
            if emulation_env_config.containers_config.agent_ip in n_m.ips:
                continue
            merged_m = n_m
            for i, o_m in enumerate(old_machines_obs):
                if n_m.ips_match(o_m.ips):
                    merged_m = EnvDynamicsUtil.merge_new_machine_obs_with_old_machine_obs(o_m, n_m, action)
            attacker_machine_observations.append(merged_m)

        # Add old machines to merged state
        for o_m in old_machines_obs:
            exists = False
            for m_m in attacker_machine_observations:
                if o_m.ips_match(m_m.ips):
                    exists = True
            if not exists:
                attacker_machine_observations.append(o_m)

        return attacker_machine_observations

    @staticmethod
    def merge_new_machine_obs_with_old_machine_obs(o_m: EmulationAttackerMachineObservationState,
                                                   n_m: EmulationAttackerMachineObservationState,
                                                   action: EmulationAttackerAction) \
            -> EmulationAttackerMachineObservationState:
        """
        Helper function for merging an old machine observation with new information collected

        :param o_m: old machine observation
        :param n_m: newly collected machine information
        :return: the merged attacker machine observation state
        """
        
        merged_ports, num_new_ports_found = EnvDynamicsUtil.merge_ports(o_m.ports, n_m.ports, acc=True)
        n_m.ports = merged_ports
        merged_os, num_new_os_found = EnvDynamicsUtil.merge_os(o_m.os, n_m.os)
        n_m.os = merged_os
        merged_cve_vulnerabilities, num_new_cve_vuln_found = EnvDynamicsUtil.merge_vulnerabilities(o_m.cve_vulns,
                                                                                                   n_m.cve_vulns)
        n_m.cve_vulns = merged_cve_vulnerabilities
        merged_osvdb_vulnerabilities, num_new_osvdb_vuln_found = EnvDynamicsUtil.merge_vulnerabilities(
            o_m.osvdb_vulns, n_m.osvdb_vulns)
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

        return n_m

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
    def merge_shell_access(o_m: EmulationAttackerMachineObservationState,
                           n_m: EmulationAttackerMachineObservationState) -> \
            Tuple[EmulationAttackerMachineObservationState, int]:
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
    def merge_reachable(o_m: EmulationAttackerMachineObservationState,
                        n_m: EmulationAttackerMachineObservationState) \
            -> EmulationAttackerMachineObservationState:
        """
        Helper function for merging an old machine observation reachable nodes with new information collected

        :param o_os: the old machine observation
        :param n_os: the new machine observation
        :return: the merged machine observation with updated reachable nodes
        """
        n_m.reachable = n_m.reachable.union(o_m.reachable)
        return n_m

    @staticmethod
    def merge_backdoor_credentials(o_m: EmulationAttackerMachineObservationState,
                                   n_m: EmulationAttackerMachineObservationState) \
            -> EmulationAttackerMachineObservationState:
        """
        Helper function for merging an old machine observation backdoor credentials nodes with new information collected

        :param o_os: the old machine observation
        :param n_os: the new machine observation
        :return: the merged machine observation with updated backdoor credentials nodes
        """
        n_m.backdoor_credentials = list(set(n_m.backdoor_credentials + o_m.backdoor_credentials))
        return n_m

    @staticmethod
    def merge_logged_in(o_m: EmulationAttackerMachineObservationState,
                        n_m: EmulationAttackerMachineObservationState) \
            -> Tuple[EmulationAttackerMachineObservationState, int]:
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
    def merge_tools_installed(o_m: EmulationAttackerMachineObservationState,
                              n_m: EmulationAttackerMachineObservationState) \
            -> Tuple[EmulationAttackerMachineObservationState, int]:
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
    def merge_backdoor_installed(o_m: EmulationAttackerMachineObservationState,
                                 n_m: EmulationAttackerMachineObservationState) \
            -> Tuple[EmulationAttackerMachineObservationState, int]:
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
    def merge_backdoor_tried(o_m: EmulationAttackerMachineObservationState,
                             n_m: EmulationAttackerMachineObservationState) \
            -> EmulationAttackerMachineObservationState:
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
    def merge_tools_tried(o_m: EmulationAttackerMachineObservationState,
                          n_m: EmulationAttackerMachineObservationState) -> EmulationAttackerMachineObservationState:
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
    def merge_root(o_m: EmulationAttackerMachineObservationState, n_m: EmulationAttackerMachineObservationState) \
            -> Tuple[EmulationAttackerMachineObservationState, int]:
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
    def merge_flags(o_m: EmulationAttackerMachineObservationState, n_m: EmulationAttackerMachineObservationState) \
            -> Tuple[EmulationAttackerMachineObservationState, int]:
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
    def merge_connections(o_m: EmulationAttackerMachineObservationState,
                          n_m: EmulationAttackerMachineObservationState) -> EmulationAttackerMachineObservationState:
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
    def merge_filesystem_scanned(o_m: EmulationAttackerMachineObservationState,
                                 n_m: EmulationAttackerMachineObservationState,
                                 new_root: int) -> EmulationAttackerMachineObservationState:
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
    def merge_untried_credentials(o_m: EmulationAttackerMachineObservationState,
                                  n_m: EmulationAttackerMachineObservationState,
                                  action: EmulationAttackerAction) -> EmulationAttackerMachineObservationState:
        """
        Helper function for merging an old machine observation untried-credentials-flag with new information collected

        :param o_m: the old machine observation
        :param n_m: the new machine observation
        :param action: the action that was done to get n_m
        :return: the merged machine observation with updated untried-credentials flag
        """
        if action is not None and action.id == EmulationAttackerActionId.NETWORK_SERVICE_LOGIN and n_m.shell_access:
            return n_m
        else:
            if not n_m.untried_credentials:
                n_m.untried_credentials = o_m.untried_credentials
        return n_m

    @staticmethod
    def merge_exploit_tried(o_m: EmulationAttackerMachineObservationState,
                            n_m: EmulationAttackerMachineObservationState) -> EmulationAttackerMachineObservationState:
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
    def merge_trace(o_m: EmulationAttackerMachineObservationState, n_m: EmulationAttackerMachineObservationState) \
            -> EmulationAttackerMachineObservationState:
        """
        Helper function for merging an old machine observation trace with new information collected

        :param o_os: the old machine observation
        :param n_os: the new machine observation
        :return: the merged machine observation with updated trace
        """
        if n_m.trace is None:
            n_m.trace = o_m.trace
        return n_m

    @staticmethod
    def merge_ports(o_ports: List[EmulationPortObservationState], n_ports: List[EmulationPortObservationState],
                    acc: bool = True) -> Tuple[List[EmulationPortObservationState], int]:
        """
        Helper function for merging two port lists

        :param o_ports: old list of ports
        :param n_ports: new list of ports
        :param acc: if true, accumulate port observations rather than overwrite
        :return: the merged port list, number of new ports found
        """
        num_new_ports_found = 0
        if n_ports is None or len(n_ports) == 0:
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
    def merge_vulnerabilities(o_vuln: List[EmulationVulnerabilityObservationState],
                              n_vuln: List[EmulationVulnerabilityObservationState],
                              acc: bool = True) -> Tuple[List[EmulationVulnerabilityObservationState], int]:
        """
        Helper function for merging two vulnerability lists lists

        :param o_vuln: old list of vulnerabilities
        :param n_vuln: new list of vulnerabilities
        :param acc: if true, accumulate vulnerability observations rather than overwrite
        :return: the merged vulnerability list, number of new vulnerabilities detected
        """
        num_new_vuln_found = 0
        if n_vuln is None or len(n_vuln) == 0:
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
    def is_all_flags_collected(s: EmulationEnvState, emulation_env_config: EmulationEnvConfig) -> bool:
        """
        Checks if all flags are collected (then episode is done)

        :param s: current state
        :param emulation_env_config: environment config
        :return: True if all flags are collected otherwise false
        """
        total_flags = set()
        for flag in emulation_env_config.flags_config.node_flag_configs:
            total_flags.add(flag)
        found_flags: Set[Any] = set()
        if s.attacker_obs_state is None:
            raise ValueError("EmlationAttackerObservationState is None")
        for node in s.attacker_obs_state.machines:
            found_flags = found_flags.union(node.flags_found)
        return total_flags == found_flags

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
    def exploit_tried_flags(a: EmulationAttackerAction, m_obs: EmulationAttackerMachineObservationState):
        """
        Utility function for updating exploit-tried flags

        :param a: the action
        :param m_obs: the observation to update
        :return: the updated observation
        """
        # Subnet scans sometimes fail due to stagnation, https://github.com/nmap/nmap/issues/1321
        if (a.id == EmulationAttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_ALL and m_obs.untried_credentials) \
                or a.id == EmulationAttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST:
            m_obs.ftp_brute_tried = True
        elif (a.id == EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_ALL and m_obs.untried_credentials) \
                or a.id == EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST:
            m_obs.ssh_brute_tried = True
        elif (a.id == EmulationAttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_ALL and m_obs.untried_credentials) \
                or a.id == EmulationAttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST:
            m_obs.telnet_brute_tried = True
        elif (a.id == EmulationAttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_ALL and m_obs.untried_credentials) \
                or a.id == EmulationAttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST:
            m_obs.irc_brute_tried = True
        elif (a.id == EmulationAttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_ALL and m_obs.untried_credentials) \
                or a.id == EmulationAttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST:
            m_obs.postgres_brute_tried = True
        elif (a.id == EmulationAttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_ALL and m_obs.untried_credentials) \
                or a.id == EmulationAttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST:
            m_obs.smtp_brute_tried = True
        elif (a.id == EmulationAttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_ALL and m_obs.untried_credentials) \
                or a.id == EmulationAttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST:
            m_obs.mysql_brute_tried = True
        elif (a.id == EmulationAttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_ALL and m_obs.untried_credentials)\
                or a.id == EmulationAttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST:
            m_obs.mongo_brute_tried = True
        elif (a.id == EmulationAttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_ALL and m_obs.untried_credentials) \
                or a.id == EmulationAttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST:
            m_obs.cassandra_brute_tried = True
        elif a.id == EmulationAttackerActionId.SAMBACRY_EXPLOIT:
            m_obs.sambacry_tried = True
        elif a.id == EmulationAttackerActionId.SHELLSHOCK_EXPLOIT:
            m_obs.shellshock_tried = True
        elif a.id == EmulationAttackerActionId.DVWA_SQL_INJECTION:
            m_obs.dvwa_sql_injection_tried = True
        elif a.id == EmulationAttackerActionId.CVE_2015_3306_EXPLOIT:
            m_obs.cve_2015_3306_tried = True
        elif a.id == EmulationAttackerActionId.CVE_2015_1427_EXPLOIT:
            m_obs.cve_2015_1427_tried = True
        elif a.id == EmulationAttackerActionId.CVE_2016_10033_EXPLOIT:
            m_obs.cve_2016_10033_tried = True
        elif a.id == EmulationAttackerActionId.CVE_2010_0426_PRIV_ESC:
            m_obs.cve_2010_0426_tried = True
        elif a.id == EmulationAttackerActionId.CVE_2015_5602_PRIV_ESC:
            m_obs.cve_2015_5602_tried = True
        return m_obs

    @staticmethod
    def ssh_backdoor_tried_flags(a: EmulationAttackerAction, m_obs: EmulationAttackerMachineObservationState):
        """
        Utility function for updating install-backdoor flag

        :param a: the action
        :param m_obs: the observation to update
        :return: the updated observation
        """
        if a.id == EmulationAttackerActionId.SSH_BACKDOOR:
            m_obs.backdoor_tried = True
        return m_obs

    @staticmethod
    def install_tools_tried(a: EmulationAttackerAction, m_obs: EmulationAttackerMachineObservationState):
        """
        Utility function for updating install-tools flag

        :param a: the action
        :param m_obs: the observation to update
        :return: the updated observation
        """
        if a.id == EmulationAttackerActionId.INSTALL_TOOLS:
            m_obs.install_tools_tried = True
        return m_obs

    @staticmethod
    def cache_attacker_action(a: EmulationAttackerAction, s: EmulationEnvState) \
            -> None:
        """
        Utility function for caching an attacker action

        :param a: the attacker action to cache
        :param s: the current state
        :return: None
        """
        if s.attacker_obs_state is None:
            raise ValueError("EmulationAttackerObservationState is None")
        logged_in_ips_str = EnvDynamicsUtil.logged_in_ips_str(emulation_env_config=s.emulation_env_config, s=s)
        s.attacker_obs_state.actions_tried.add((a.id, a.index, logged_in_ips_str))

    @staticmethod
    def cache_defender_action(a: EmulationDefenderAction, s: EmulationEnvState) \
            -> None:
        """
        Utility function for caching a defender action

        :param a: the defender action to cache
        :param s: the current state
        :return: None
        """
        if s.defender_obs_state is None:
            raise ValueError("EmulationAttackerObservationState is None")
        logged_in_ips_str = EnvDynamicsUtil.logged_in_ips_str(emulation_env_config=s.emulation_env_config, s=s)
        s.defender_obs_state.actions_tried.add((int(a.id.value), a.index, logged_in_ips_str))

    @staticmethod
    def logged_in_ips_str(emulation_env_config: EmulationEnvConfig, s: EmulationEnvState) -> str:
        """
        Utility function to getting a string-id of the attacker state (Q) of logged in machines

        :param emulation_env_config: the environment config
        :param s: the current state
        :return: the string id
        """
        hacker_ip = emulation_env_config.containers_config.agent_ip
        if s.attacker_obs_state is None:
            raise ValueError("EmultaionAttackerObservationState is None")
        machines = s.attacker_obs_state.machines
        logged_in_ips = list(map(lambda x: "_".join(x.ips) + "_tools=" + str(int(x.tools_installed)) + "_backdoor="
                                           + str(int(x.backdoor_installed)) + "_root=" + str(int(x.root)),
                                 filter(lambda x: x.logged_in, machines)))
        logged_in_ips.append(hacker_ip)
        logged_in_ips = sorted(logged_in_ips, key=lambda x: x)
        logged_in_ips_str = "_".join(logged_in_ips)
        return logged_in_ips_str

    @staticmethod
    def exploit_get_vuln_name(a: EmulationAttackerAction) -> str:
        """
        Utiltiy function to get the vulnerability name of a particular exploit action

        :param a: the action
        :return: the name of hte corresponding vulnerability
        """
        if a.id == EmulationAttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_ALL \
                or a.id == EmulationAttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.EXPLOIT_VULNERABILITES.FTP_DICT_SAME_USER_PASS
        elif a.id == EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_ALL \
                or a.id == EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.EXPLOIT_VULNERABILITES.SSH_DICT_SAME_USER_PASS
        elif a.id == EmulationAttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_ALL \
                or a.id == EmulationAttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.EXPLOIT_VULNERABILITES.TELNET_DICTS_SAME_USER_PASS
        elif a.id == EmulationAttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST \
                or a.id == EmulationAttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_ALL:
            return constants.EXPLOIT_VULNERABILITES.IRC_DICTS_SAME_USER_PASS
        elif a.id == EmulationAttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_ALL \
                or a.id == EmulationAttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.EXPLOIT_VULNERABILITES.POSTGRES_DICTS_SAME_USER_PASS
        elif a.id == EmulationAttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_ALL \
                or a.id == EmulationAttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.EXPLOIT_VULNERABILITES.SMTP_DICTS_SAME_USER_PASS
        elif a.id == EmulationAttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_ALL \
                or a.id == EmulationAttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.EXPLOIT_VULNERABILITES.MYSQL_DICTS_SAME_USER_PASS
        elif a.id == EmulationAttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_ALL \
                or a.id == EmulationAttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.EXPLOIT_VULNERABILITES.MONGO_DICTS_SAME_USER_PASS
        elif a.id == EmulationAttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_ALL \
                or a.id == EmulationAttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.EXPLOIT_VULNERABILITES.CASSANDRA_DICTS_SAME_USER_PASS
        return constants.EXPLOIT_VULNERABILITES.UNKNOWN

    @staticmethod
    def exploit_get_vuln_cvss(a: EmulationAttackerAction) -> float:
        """
        Utility function for getting the CVSS of an exploit action

        :param a: the action
        :return: the CVSS
        """
        if a.id in EmulationAttackerActionConfig.dict_brute_same_user_ids():
            return constants.EXPLOIT_VULNERABILITES.WEAK_PASSWORD_CVSS
        return 0.0

    @staticmethod
    def exploit_get_service_name(a: EmulationAttackerAction) -> str:
        """
        Utility function to get the name of the exploited service of a particular exploit action

        :param a: the action
        :return: the name of the service
        """
        if a.id == EmulationAttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_ALL \
                or a.id == EmulationAttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.FTP.SERVICE_NAME
        elif a.id == EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_ALL \
                or a.id == EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.SSH.SERVICE_NAME
        elif a.id == EmulationAttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_ALL \
                or a.id == EmulationAttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.TELNET.SERVICE_NAME
        elif a.id == EmulationAttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_ALL \
                or a.id == EmulationAttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.IRC.SERVICE_NAME
        elif a.id == EmulationAttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_ALL \
                or a.id == EmulationAttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.POSTGRES.SERVICE_NAME
        elif a.id == EmulationAttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_ALL \
                or a.id == EmulationAttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.SMTP.SERVICE_NAME
        elif a.id == EmulationAttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_ALL \
                or a.id == EmulationAttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.MYSQL.SERVICE_NAME
        elif a.id == EmulationAttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_ALL \
                or a.id == EmulationAttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.MONGO.SERVICE_NAME
        elif a.id == EmulationAttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_ALL \
                or a.id == EmulationAttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST:
            return constants.CASSANDRA.SERVICE_NAME
        return constants.EXPLOIT_VULNERABILITES.UNKNOWN

    @staticmethod
    def merge_duplicate_machines(machines: List[EmulationAttackerMachineObservationState],
                                 action: EmulationAttackerAction) -> List[EmulationAttackerMachineObservationState]:
        """
        Utility function for merging machines that are duplicates

        :param machines: list of machines (possibly with duplicates)
        :param action: the action that generated the new machines
        :return: the merged set of machines
        """
        merged_machines = []
        ips: Set[str] = set()
        for m in machines:
            ip_suffixes = list(map(lambda x: x.split(".")[-1], m.ips))
            for m1 in machines:
                for ip in m1.ips:
                    if ip.split(".")[-1] in ip_suffixes and ip not in m.ips:
                        m.ips = list(set(m.ips + m1.ips))
        for m in machines:
            if not m.ips_match(list(ips)):
                merged_m = m
                for m2 in machines:
                    if m2.ips == merged_m.ips:
                        merged_m = EnvDynamicsUtil.merge_new_machine_obs_with_old_machine_obs(merged_m, m2, action)
                merged_machines.append(merged_m)
                ips = ips.union(set(m.ips))
        return merged_machines
