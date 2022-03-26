from typing import List, Tuple
import copy
from csle_common.dao.observation.attacker import AttackerMachineObservationState


class NetworkOutcome:
    """
    DTO that represents the observed outcome of an action for the attacker in the environment
    """

    def __init__(self, attacker_machine_observations: List[AttackerMachineObservationState] = None,
                 attacker_machine_observation: AttackerMachineObservationState = None,
                 total_new_ports_found : int = 0, total_new_os_found: int = 0,
                 total_new_cve_vuln_found : int = 0, total_new_machines_found : int = 0,
                 total_new_shell_access : int = 0, total_new_flag_pts : int = 0, total_new_root : int = 0,
                 total_new_osvdb_vuln_found : int = 0, total_new_logged_in : int = 0,
                 total_new_tools_installed : int = 0, total_new_backdoors_installed : int = 0,
                 cost: float = 0.0, alerts: Tuple = (0,0)):
        """
        Initializes the DTO

        :param attacker_machine_observations: the list of attacker machine observations
        :param attacker_machine_observation: the specific attacker machine observation
        :param total_new_ports_found: the total number of new ports found
        :param total_new_os_found: the total number of new operating systems found
        :param total_new_cve_vuln_found: the total number of new CVE vulnerabilities found
        :param total_new_machines_found: the total number of new machines found
        :param total_new_shell_access: the total number of new shell access found
        :param total_new_flag_pts: the total number of new flag points found
        :param total_new_root: the total number of new root logins found
        :param total_new_osvdb_vuln_found: the total number of OSVDB vulnerabilities found
        :param total_new_logged_in: the total number of new logins found
        :param total_new_tools_installed: the total number of new tools installed
        :param total_new_backdoors_installed: the total number of new backdoors installed
        :param cost: the total cost of the operation
        :param alerts: the total alerts of the operation
        """
        if attacker_machine_observations is None:
            self.attacker_machine_observations = []
        else:
            self.attacker_machine_observations = attacker_machine_observations
        self.attacker_machine_observation = attacker_machine_observation
        self.total_new_ports_found = total_new_ports_found
        self.total_new_os_found  =total_new_os_found
        self.total_new_cve_vuln_found = total_new_cve_vuln_found
        self.total_new_machines_found = total_new_machines_found
        self.total_new_shell_access = total_new_shell_access
        self.total_new_flag_pts = total_new_flag_pts
        self.total_new_root = total_new_root
        self.total_new_osvdb_vuln_found = total_new_osvdb_vuln_found
        self.total_new_logged_in = total_new_logged_in
        self.total_new_tools_installed = total_new_tools_installed
        self.total_new_backdoors_installed = total_new_backdoors_installed
        self.cost = cost
        self.alerts = alerts

    def copy(self):
        """
        :return: a copy of the object
        """
        net_outcome = NetworkOutcome(
            attacker_machine_observations=copy.deepcopy(self.attacker_machine_observations),
            attacker_machine_observation=self.attacker_machine_observation.copy(),
            total_new_ports_found=self.total_new_ports_found,
            total_new_os_found=self.total_new_os_found,
            total_new_cve_vuln_found=self.total_new_cve_vuln_found,
            total_new_machines_found=self.total_new_machines_found,
            total_new_shell_access=self.total_new_shell_access,
            total_new_flag_pts=self.total_new_flag_pts,
            total_new_root=self.total_new_root,
            total_new_osvdb_vuln_found=self.total_new_osvdb_vuln_found,
            total_new_logged_in=self.total_new_logged_in,
            total_new_tools_installed=self.total_new_tools_installed,
            total_new_backdoors_installed=self.total_new_backdoors_installed,
            cost=self.cost, alerts=self.alerts
        )
        return net_outcome

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "attacker_machine_observations:{},attacker_machine_observation:{}" \
               "total_new_ports_found:{},total_new_os_found:{}," \
               "total_new_cve_vuln_found:{},total_new_machines_found:{},total_new_shell_access:{}," \
               "total_new_flag_pts:{},total_new_root:{},total_new_osvdb_vuln_found:{}," \
               "total_new_logged_in:{},total_new_tools_installed:{},total_new_backdoors_installed:{}," \
               "cost:{}, alerts:{}".format(
            list(map(lambda x: str(x), self.attacker_machine_observations)),
            str(self.attacker_machine_observation),
            self.total_new_ports_found, self.total_new_os_found, self.total_new_cve_vuln_found,
            self.total_new_machines_found, self.total_new_shell_access, self.total_new_flag_pts,
            self.total_new_root, self.total_new_osvdb_vuln_found, self.total_new_logged_in,
            self.total_new_tools_installed, self.total_new_backdoors_installed, self.cost,
            self.alerts)

    def update_counts(self, net_outcome) -> None:
        """
        Utility function for merging the net outcome with another outcome.

        :param net_outcome: the outcome to merge with
        :return: None
        """
        self.total_new_ports_found += net_outcome.total_new_ports_found
        self.total_new_os_found += net_outcome.total_new_os_found
        self.total_new_cve_vuln_found += net_outcome.total_new_cve_vuln_found
        self.total_new_machines_found += net_outcome.total_new_machines_found
        self.total_new_shell_access += net_outcome.total_new_shell_access
        self.total_new_flag_pts += net_outcome.total_new_flag_pts
        self.total_new_root += net_outcome.total_new_root
        self.total_new_osvdb_vuln_found += net_outcome.total_new_osvdb_vuln_found
        self.total_new_logged_in += net_outcome.total_new_logged_in
        self.total_new_tools_installed += net_outcome.total_new_tools_installed
        self.total_new_backdoors_installed += net_outcome.total_new_backdoors_installed

    def update_counts_machine(self, machine: AttackerMachineObservationState) -> None:
        """
        Utility function for updating the counts based on a newly observed machine

        :param machine: the newly observed machine
        :return: None
        """
        self.total_new_ports_found += len(machine.ports)
        new_os = 0 if machine.os == "unknown" else 1
        self.total_new_os_found += new_os
        self.total_new_cve_vuln_found += len(machine.cve_vulns)
        self.total_new_shell_access += 1 if machine.shell_access else 0
        self.total_new_flag_pts += len(machine.flags_found)
        self.total_new_root += 1 if machine.root else 0
        self.total_new_osvdb_vuln_found += len(machine.osvdb_vulns)
        self.total_new_logged_in += 1 if machine.logged_in else 0
        self.total_new_tools_installed += 1 if machine.tools_installed else 0
        self.total_new_backdoors_installed += 1 if machine.backdoor_installed else 0
        self.total_new_machines_found += 1