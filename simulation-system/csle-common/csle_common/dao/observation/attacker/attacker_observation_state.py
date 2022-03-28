from typing import List
from csle_common.dao.observation.attacker.attacker_machine_observation_state import AttackerMachineObservationState
from csle_common.dao.action.attacker.attacker_action import AttackerAction
from csle_common.dao.action.attacker.attacker_action_id import AttackerActionId


class AttackerObservationState:
    """
    Represents the attacker's agent's current belief state of the environment
    """

    def __init__(self, catched_flags : int, agent_reachable = None):
        """
        Initializes the state

        :param num_flags: the number of flags
        :param catched_flags: the number of catched flags
        :param agent_reachable: whether this node is reachable from the agent
        """
        self.machines : List[AttackerMachineObservationState] = []
        self.catched_flags = catched_flags
        self.actions_tried = set()
        self.agent_reachable = agent_reachable
        if agent_reachable is None:
            self.agent_reachable = set()

    def sort_machines(self) -> None:
        """
        Sorts the machines in the observation

        :return: None
        """
        self.machines = sorted(self.machines, key=lambda x: int(x.internal_ip.rsplit(".", 1)[-1]), reverse=False)

    def cleanup(self) -> None:
        """
        Cleanup machine states

        :return: None
        """
        for m in self.machines:
            m.cleanup()

    def get_action_ips(self, a : AttackerAction) -> List[str]:
        """
        Returns the ip of the machine that the action targets

        :param a: the action
        :return: the ip of the target
        """
        if a.index == -1:
            self.sort_machines()
            ips = list(map(lambda x: x.internal_ip, self.machines))
            return ips
        if a.index < len(self.machines):
            return self.machines[a.index].ips
        return a.ips

    def exploit_tried(self, a: AttackerAction, m: AttackerMachineObservationState) -> bool:
        """
        Checks if a given exploit have been tried on a given machine or not

        :param a: the exploit action
        :param m: the machine
        :return: true if it has already been tried, otherwise false
        """
        # Known issue with subnet attacks and NMAP: https://github.com/nmap/nmap/issues/1321
        if m is not None:
            if (a.id == AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_ALL
                or a.id == AttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST):
                return m.ssh_brute_tried

            if (a.id == AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_ALL
                or a.id == AttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST):
                return m.telnet_brute_tried

            if (a.id == AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_ALL
                or a.id == AttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST):
                return m.ftp_brute_tried

            if (a.id == AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_ALL
                or a.id == AttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST):
                return m.cassandra_brute_tried

            if (a.id == AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_ALL
                or a.id == AttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST):
                return m.irc_brute_tried

            if (a.id == AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_ALL
                or a.id == AttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST):
                return m.mongo_brute_tried

            if (a.id == AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_ALL
                or a.id == AttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST):
                return m.mysql_brute_tried

            if (a.id == AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_ALL
                or a.id == AttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST):
                return m.smtp_brute_tried

            if (a.id == AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_ALL
                or a.id == AttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST):
                return m.postgres_brute_tried

            if a.id == AttackerActionId.SAMBACRY_EXPLOIT:
                return m.sambacry_tried

            if a.id == AttackerActionId.SHELLSHOCK_EXPLOIT:
                return m.shellshock_tried

            if a.id == AttackerActionId.DVWA_SQL_INJECTION:
                return m.dvwa_sql_injection_tried

            if a.id == AttackerActionId.CVE_2015_3306_EXPLOIT:
                return m.cve_2015_3306_tried

            if a.id == AttackerActionId.CVE_2015_1427_EXPLOIT:
                return m.cve_2015_1427_tried

            if a.id == AttackerActionId.CVE_2016_10033_EXPLOIT:
                return m.cve_2016_10033_tried

            if a.id == AttackerActionId.CVE_2010_0426_PRIV_ESC:
                return m.cve_2010_0426_tried

            if a.id == AttackerActionId.CVE_2015_5602_PRIV_ESC:
                return m.cve_2015_5602_tried

            return False
        else:
            exploit_tried = True
            for m2 in self.machines:
                res = self.exploit_tried(a=a, m=m2)
                if not res:
                    exploit_tried = res
                    break
            return exploit_tried

    def exploit_executed(self, machine: AttackerMachineObservationState) -> bool:
        """
        Check if exploit have been tried on a particular machine

        :param machine: the machine
        :return: true if some exploit have been launched, false otherwise
        """
        if (machine.telnet_brute_tried or machine.ssh_brute_tried
                or machine.ftp_brute_tried or machine.cassandra_brute_tried or machine.irc_brute_tried
            or machine.mongo_brute_tried or machine.mysql_brute_tried or machine.smtp_brute_tried or
            machine.postgres_brute_tried or machine.sambacry_tried or machine.shellshock_tried or
            machine.dvwa_sql_injection_tried or machine.cve_2015_3306_tried or machine.cve_2015_1427_tried
            or machine.cve_2016_10033_tried or machine.cve_2010_0426_tried or machine.cve_2015_5602_tried):
            return True
        return False

    def copy(self) -> "AttackerObservationState":
        """
        :return: a copy of the state
        """
        c = AttackerObservationState(catched_flags = self.catched_flags,
                                     agent_reachable = self.agent_reachable.copy())
        c.actions_tried = self.actions_tried.copy()
        for m in self.machines:
            c.machines.append(m.copy())
        return c

    def __str__(self) -> str:
        """
        :return: a string representation of the state
        """
        return  "Found flags:{},".format(self.catched_flags) \
                + "\n" + "\n".join([str(i) + ":" + str(self.machines[i]) for i in range(len(self.machines))])
