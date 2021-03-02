from typing import List
from gym_pycr_pwcrack.dao.observation.machine_observation_state import MachineObservationState
from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.dao.action.action_id import ActionId

class ObservationState:

    def __init__(self, num_machines : int, num_ports : int, num_vuln : int, num_sh : int,
                 num_flags : int, catched_flags : int, agent_reachable = None):
        self.num_machines = num_machines
        self.num_ports = num_ports
        self.num_vuln = num_vuln
        self.machines : List[MachineObservationState] = []
        self.detected = False
        self.all_flags = False
        self.num_sh = num_sh
        self.num_flags = num_flags
        self.catched_flags = catched_flags
        self.actions_tried = set()
        self.agent_reachable = agent_reachable
        if agent_reachable is None:
            self.agent_reachable = set()


    def sort_machines(self):
        self.machines = sorted(self.machines, key=lambda x: int(x.ip.rsplit(".", 1)[-1]), reverse=False)


    def cleanup(self):
        for m in self.machines:
            m.cleanup()


    def get_action_ip(self, a : Action):
        if a.index == -1:
            self.sort_machines()
            ips = list(map(lambda x: x.ip, self.machines))
            ips_str = "_".join(ips)
            return ips_str
        if a.index < len(self.machines) and a.index < self.num_machines:
            return self.machines[a.index].ip
        return a.ip

    def exploit_tried(self, a: Action, m: MachineObservationState):
        # Known issue with subnet attacks and NMAP: https://github.com/nmap/nmap/issues/1321
        if m is not None:
            if (a.id == ActionId.SSH_SAME_USER_PASS_DICTIONARY_ALL
                or a.id == ActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST):
                return m.ssh_brute_tried

            if (a.id == ActionId.TELNET_SAME_USER_PASS_DICTIONARY_ALL
                or a.id == ActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST):
                return m.telnet_brute_tried

            if (a.id == ActionId.FTP_SAME_USER_PASS_DICTIONARY_ALL
                or a.id == ActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST):
                return m.ftp_brute_tried

            if (a.id == ActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_ALL
                or a.id == ActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST):
                return m.cassandra_brute_tried

            if (a.id == ActionId.IRC_SAME_USER_PASS_DICTIONARY_ALL
                or a.id == ActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST):
                return m.irc_brute_tried

            if (a.id == ActionId.MONGO_SAME_USER_PASS_DICTIONARY_ALL
                or a.id == ActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST):
                return m.mongo_brute_tried

            if (a.id == ActionId.MYSQL_SAME_USER_PASS_DICTIONARY_ALL
                or a.id == ActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST):
                return m.mysql_brute_tried

            if (a.id == ActionId.SMTP_SAME_USER_PASS_DICTIONARY_ALL
                or a.id == ActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST):
                return m.smtp_brute_tried

            if (a.id == ActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_ALL
                or a.id == ActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST):
                return m.postgres_brute_tried

            if a.id == ActionId.SAMBACRY_EXPLOIT:
                return m.sambacry_tried

            if a.id == ActionId.SHELLSHOCK_EXPLOIT:
                return m.shellshock_tried

            if a.id == ActionId.DVWA_SQL_INJECTION:
                return m.dvwa_sql_injection_tried

            if a.id == ActionId.CVE_2015_3306_EXPLOIT:
                return m.cve_2015_3306_tried

            if a.id == ActionId.CVE_2015_1427_EXPLOIT:
                return m.cve_2015_1427_tried

            if a.id == ActionId.CVE_2016_10033_EXPLOIT:
                return m.cve_2016_10033_tried

            if a.id == ActionId.CVE_2010_0426_EXPLOIT:
                return m.cve_2010_0426_tried

            if a.id == ActionId.CVE_2015_5602_EXPLOIT:
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

    def copy(self):
        c = ObservationState(num_machines = self.num_machines, num_vuln = self.num_vuln, num_sh = self.num_sh,
                                    num_flags = self.num_flags, catched_flags = self.catched_flags,
                                    agent_reachable = self.agent_reachable.copy(), num_ports=self.num_ports)
        c.detected = self.detected
        c.all_flags = self.all_flags
        c.actions_tried = self.actions_tried.copy()
        for m in self.machines:
            c.machines.append(m.copy())
        return c
