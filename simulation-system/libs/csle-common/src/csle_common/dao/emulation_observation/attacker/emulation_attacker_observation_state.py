from typing import Optional, List, Set, Dict, Any, Tuple
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_observation.attacker.emulation_attacker_machine_observation_state \
    import EmulationAttackerMachineObservationState
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_base.json_serializable import JSONSerializable


class EmulationAttackerObservationState(JSONSerializable):
    """
    Represents the attacker's agent's current belief state of the emulation
    """

    def __init__(self, catched_flags: int, agent_reachable: Set[str]):
        """
        Initializes the state

        :param num_flags: the number of flags
        :param catched_flags: the number of catched flags
        :param agent_reachable: whether this node is reachable from the agent
        """
        self.machines: List[EmulationAttackerMachineObservationState] = []
        self.catched_flags = catched_flags
        self.actions_tried: Set[Tuple[int, int, str]] = set()
        self.agent_reachable = agent_reachable

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EmulationAttackerObservationState":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the instance
        """
        obj = EmulationAttackerObservationState(catched_flags=d["catched_flags"],
                                                agent_reachable=set(d["agent_reachable"]))
        obj.machines = list(map(lambda x: EmulationAttackerMachineObservationState.from_dict(x), d["machines"]))
        actions_tried = set()
        for i in range(len(d["actions_tried"])):
            actions_tried.add((int(d["actions_tried"][i][0]), int(d["actions_tried"][i][1]),
                               str(d["actions_tried"][i][2])))
        obj.actions_tried = actions_tried
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["machines"] = list(map(lambda x: x.to_dict(), self.machines))
        d["catched_flags"] = self.catched_flags
        d["actions_tried"] = sorted(list(self.actions_tried))
        d["agent_reachable"] = sorted(list(self.agent_reachable))
        return d

    def sort_machines(self) -> None:
        """
        Sorts the machines in the observation

        :return: None
        """
        self.machines = sorted(self.machines, key=lambda x: int(x.ips[0].rsplit(".", 1)[-1]), reverse=False)

    def cleanup(self) -> None:
        """
        Cleanup machine states

        :return: None
        """
        for m in self.machines:
            m.cleanup()

    def get_action_ips(self, a: EmulationAttackerAction, emulation_env_config: EmulationEnvConfig) -> List[str]:
        """
        Returns the ip of the machine that the action targets

        :param a: the action
        :param emulation_env_config: the emulation env config
        :return: the ip of the target
        """
        if a.index == -1 or a.index == len(self.machines):
            return emulation_env_config.topology_config.subnetwork_masks
        elif a.index < len(self.machines):
            return self.machines[a.index].ips
        elif a.index > len(self.machines):
            raise ValueError(f"invalid index: {a.index}, num machines: {len(self.machines)}")
        else:
            return a.ips

    def exploit_tried(self, a: EmulationAttackerAction, m: Optional[EmulationAttackerMachineObservationState]) -> bool:
        """
        Checks if a given exploit have been tried on a given machine or not

        :param a: the exploit action
        :param m: the machine
        :return: true if it has already been tried, otherwise false
        """
        # Known issue with subnet attacks and NMAP: https://github.com/nmap/nmap/issues/1321
        if m is not None:
            if (a.id == EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_ALL
                    or a.id == EmulationAttackerActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST):
                return m.ssh_brute_tried

            if (a.id == EmulationAttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_ALL
                    or a.id == EmulationAttackerActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST):
                return m.telnet_brute_tried

            if (a.id == EmulationAttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_ALL
                    or a.id == EmulationAttackerActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST):
                return m.ftp_brute_tried

            if (a.id == EmulationAttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_ALL
                    or a.id == EmulationAttackerActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST):
                return m.cassandra_brute_tried

            if (a.id == EmulationAttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_ALL
                    or a.id == EmulationAttackerActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST):
                return m.irc_brute_tried

            if (a.id == EmulationAttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_ALL
                    or a.id == EmulationAttackerActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST):
                return m.mongo_brute_tried

            if (a.id == EmulationAttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_ALL
                    or a.id == EmulationAttackerActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST):
                return m.mysql_brute_tried

            if (a.id == EmulationAttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_ALL or
                    a.id == EmulationAttackerActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST):
                return m.smtp_brute_tried

            if (a.id == EmulationAttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_ALL or
                    a.id == EmulationAttackerActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST):
                return m.postgres_brute_tried

            if a.id == EmulationAttackerActionId.SAMBACRY_EXPLOIT:
                return m.sambacry_tried

            if a.id == EmulationAttackerActionId.SHELLSHOCK_EXPLOIT:
                return m.shellshock_tried

            if a.id == EmulationAttackerActionId.DVWA_SQL_INJECTION:
                return m.dvwa_sql_injection_tried

            if a.id == EmulationAttackerActionId.CVE_2015_3306_EXPLOIT:
                return m.cve_2015_3306_tried

            if a.id == EmulationAttackerActionId.CVE_2015_1427_EXPLOIT:
                return m.cve_2015_1427_tried

            if a.id == EmulationAttackerActionId.CVE_2016_10033_EXPLOIT:
                return m.cve_2016_10033_tried

            if a.id == EmulationAttackerActionId.CVE_2010_0426_PRIV_ESC:
                return m.cve_2010_0426_tried

            if a.id == EmulationAttackerActionId.CVE_2015_5602_PRIV_ESC:
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

    def exploit_executed(self, machine: EmulationAttackerMachineObservationState) -> bool:
        """
        Check if exploit have been tried on a particular machine

        :param machine: the machine
        :return: true if some exploit have been launched, false otherwise
        """
        if (machine.telnet_brute_tried or machine.ssh_brute_tried or machine.ftp_brute_tried or
                machine.cassandra_brute_tried or machine.irc_brute_tried or machine.mongo_brute_tried or
                machine.mysql_brute_tried or machine.smtp_brute_tried or machine.postgres_brute_tried or
                machine.sambacry_tried or machine.shellshock_tried or machine.dvwa_sql_injection_tried or
                machine.cve_2015_3306_tried or machine.cve_2015_1427_tried or
                machine.cve_2016_10033_tried or machine.cve_2010_0426_tried or machine.cve_2015_5602_tried):
            return True
        return False

    def copy(self) -> "EmulationAttackerObservationState":
        """
        :return: a copy of the state
        """
        c = EmulationAttackerObservationState(catched_flags=self.catched_flags,
                                              agent_reachable=self.agent_reachable)
        c.actions_tried = self.actions_tried
        for m in self.machines:
            c.machines.append(m.copy())
        return c

    def __str__(self) -> str:
        """
        :return: a string representation of the state
        """
        return f"Found flags:{self.catched_flags}," + "\n" + "\n".join(
            [str(i) + ":" + str(self.machines[i]) for i in range(len(self.machines))])

    @staticmethod
    def from_json_file(json_file_path: str) -> "EmulationAttackerObservationState":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return EmulationAttackerObservationState.from_dict(json.loads(json_str))

    def num_attributes(self):
        """
        :return: number of attributes of the DTO
        """
        num_attributes = 3
        if len(self.machines) > 0:
            num_attributes = num_attributes + len(self.machines) * self.machines[0].num_attributes()
        return num_attributes

    @staticmethod
    def schema() -> "EmulationAttackerObservationState":
        """
        :return: get the schema of the DTO
        """
        dto = EmulationAttackerObservationState(catched_flags=0, agent_reachable=set())
        dto.agent_reachable.add("")
        dto.actions_tried.add((-1, -1, ""))
        dto.machines = [EmulationAttackerMachineObservationState.schema()]
        return dto
