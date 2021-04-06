from typing import List
from gym_pycr_ctf.dao.observation.attacker.attacker_machine_observation_state import AttackerMachineObservationState
from gym_pycr_ctf.dao.action.attacker.attacker_action import AttackerAction
from gym_pycr_ctf.dao.action.attacker.attacker_action_id import AttackerActionId

class AttackerObservationState:
    """
    Represents the attacker's agent's current belief state of the environment
    """

    def __init__(self, num_machines : int, num_ports : int, num_vuln : int, num_sh : int,
                 num_flags : int, catched_flags : int, agent_reachable = None):
        self.num_machines = num_machines
        self.num_ports = num_ports
        self.num_vuln = num_vuln
        self.machines : List[AttackerMachineObservationState] = []
        self.detected = False
        self.all_flags = False
        self.num_sh = num_sh
        self.num_flags = num_flags
        self.catched_flags = catched_flags
        self.actions_tried = set()
        self.agent_reachable = agent_reachable
        if agent_reachable is None:
            self.agent_reachable = set()
        self.last_attacker_action : AttackerAction = None
        self.undetected_intrusions_steps = 0

    def ongoing_intrusion(self):
        if self.last_attacker_action is not None and self.last_attacker_action.id != AttackerActionId.CONTINUE:
            return True

        if self.catched_flags > 0:
            return True

        for m in self.machines:
            if m.shell_access:
                return True
            if self.exploit_executed(m):
                return True
            if m.logged_in:
                return True
        return False

    def sort_machines(self):
        self.machines = sorted(self.machines, key=lambda x: int(x.ip.rsplit(".", 1)[-1]), reverse=False)


    def cleanup(self):
        for m in self.machines:
            m.cleanup()


    def get_action_ip(self, a : AttackerAction):
        if a.index == -1:
            self.sort_machines()
            ips = list(map(lambda x: x.ip, self.machines))
            ips_str = "_".join(ips)
            return ips_str
        if a.index < len(self.machines) and a.index < self.num_machines:
            return self.machines[a.index].ip
        return a.ip

    def exploit_tried(self, a: AttackerAction, m: AttackerMachineObservationState):
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
        if (machine.telnet_brute_tried or machine.ssh_brute_tried
                or machine.ftp_brute_tried or machine.cassandra_brute_tried or machine.irc_brute_tried
            or machine.mongo_brute_tried or machine.mysql_brute_tried or machine.smtp_brute_tried or
            machine.postgres_brute_tried or machine.sambacry_tried or machine.shellshock_tried or
            machine.dvwa_sql_injection_tried or machine.cve_2015_3306_tried or machine.cve_2015_1427_tried
            or machine.cve_2016_10033_tried or machine.cve_2010_0426_tried or machine.cve_2015_5602_tried):
            return True
        return False

    def copy(self):
        c = AttackerObservationState(num_machines = self.num_machines, num_vuln = self.num_vuln, num_sh = self.num_sh,
                                     num_flags = self.num_flags, catched_flags = self.catched_flags,
                                     agent_reachable = self.agent_reachable.copy(), num_ports=self.num_ports)
        c.detected = self.detected
        c.undetected_intrusions_steps = self.undetected_intrusions_steps
        c.all_flags = self.all_flags
        c.last_attacker_action = self.last_attacker_action
        c.actions_tried = self.actions_tried.copy()
        for m in self.machines:
            c.machines.append(m.copy())
        return c


    def __str__(self):
        return  "Found flags:{}".format(self.catched_flags) + "\n" + \
                "\n".join([str(i) + ":" + str(self.machines[i]) for i in range(len(self.machines))])
