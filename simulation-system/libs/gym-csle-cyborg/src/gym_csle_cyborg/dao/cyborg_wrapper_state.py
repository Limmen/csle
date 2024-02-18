from typing import List, Dict, Any, Union
from csle_base.json_serializable import JSONSerializable


class CyborgWrapperState(JSONSerializable):
    """
    A DAO for managing the state in the  cyborg wrapper
    """

    def __init__(self, s: List[List[int]], scan_state: List[int], op_server_restored: bool, obs: List[List[int]],
                 red_action_targets: Dict[int, int], privilege_escalation_detected: Union[int, None],
                 red_agent_state: int, red_agent_target: int, attacker_observed_decoy: List[int],
                 detected: List[int], malware_state: List[int], ssh_access: List[int],
                 escalated: List[int], exploited: List[int], bline_base_jump: bool,
                 scanned_subnets: List[int]) -> None:
        """
        Initializes the DAO

        :param s: the vectorized state
        :param scan_state: the scan state
        :param op_server_restored: boolean flag inidicating whether the op server has been restored or not
        :param obs: the defender observation
        :param red_action_targets: the history of red agent targets
        :param privilege_escalation_detected: a boolean flag indicating whether a privilege escalation
                                             has been detected
        :param red_agent_state: the state of the red agent
        :param red_agent_target: the target of the red agent
        :param attacker_observed_decoy: a list of observed decoys of the attacker
        :param detected: a list of detected states for the hosts
        :param malware_state: a list of malware states for the hosts
        :param ssh_access: a list of ssh access states for the hosts
        :param escalated: a list of escalated statuses for the hosts
        :param exploited: a list of exploited statuses for the hosts
        :param scanned_subnets: a list of scanned subnetworks
        :param bline_base_jump: boolean flag indicating whether the bline agent should jump
        """
        self.s = s
        self.scan_state = scan_state
        self.op_server_restored = op_server_restored
        self.obs = obs
        self.red_action_targets = red_action_targets
        self.privilege_escalation_detected = privilege_escalation_detected
        self.red_agent_state = red_agent_state
        self.red_agent_target = red_agent_target
        self.attacker_observed_decoy = attacker_observed_decoy
        self.detected = detected
        self.malware_state = malware_state
        self.ssh_access = ssh_access
        self.escalated = escalated
        self.exploited = exploited
        self.bline_base_jump = bline_base_jump
        self.scanned_subnets = scanned_subnets

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return (f"s={self.s}, scan_state={self.scan_state}, op_server_restored={self.op_server_restored}, "
                f"obs={self.obs}, red_action_targets={self.red_action_targets}, "
                f"privilege_escalation_detected={self.privilege_escalation_detected}, "
                f"red_agent_state={self.red_agent_state}, red_agent_target={self.red_agent_target}, "
                f"attacker_observed_decoy={self.attacker_observed_decoy}, detected={self.detected}, "
                f"malware_state={self.malware_state}, ssh_access={self.ssh_access}, escalated={self.escalated}, "
                f"exploited={self.exploited}, bline_base_jump={self.bline_base_jump}, "
                f"scanned_subnets={self.scanned_subnets}")

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CyborgWrapperState":
        """
        Converts a dict representation into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = CyborgWrapperState(
            s=d["s"], scan_state=d["scan_state"], op_server_restored=d["op_server_restored"], obs=d["obs"],
            red_action_targets=d["red_action_targets"],
            privilege_escalation_detected=d["privilege_escalation_deteceted"], red_agent_state=d["red_agent_state"],
            red_agent_target=d["red_agent_target"], attacker_observed_decoy=d["attacker_observed_decoy"],
            detected=d["detected"], malware_state=d["malware_state"], ssh_access=d["ssh_access"],
            escalated=d["escalated"], exploited=d["exploited"], bline_base_jump=d["bline_base_jump"],
            scanned_subnets=d["scanned_subnets"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["s"] = self.s
        d["scan_state"] = self.scan_state
        d["op_server_restored"] = self.op_server_restored
        d["obs"] = self.obs
        d["red_action_targets"] = self.red_action_targets
        d["privilege_escalation_detected"] = self.privilege_escalation_detected
        d["red_agent_state"] = self.red_agent_state
        d["red_agent_target"] = self.red_agent_target
        d["attacker_observed_decoy"] = self.attacker_observed_decoy
        d["detected"] = self.detected
        d["malware_state"] = self.malware_state
        d["ssh_access"] = self.ssh_access
        d["escalated"] = self.escalated
        d["exploited"] = self.exploited
        d["bline_base_jump"] = self.bline_base_jump
        d["scanned_subnets"] = self.scanned_subnets
        return d

    @staticmethod
    def from_json_str(json_str: str) -> "CyborgWrapperState":
        """
        Converts json string into a DTO

        :param json_str: the json string representation
        :return: the DTO instance
        """
        import json
        dto: CyborgWrapperState = CyborgWrapperState.from_dict(json.loads(json_str))
        return dto

    @staticmethod
    def from_json_file(json_file_path: str) -> "CyborgWrapperState":
        """
        Reads a json file and converts it into a dto

        :param json_file_path: the json file path to save  the DTO to
        :return: None
        """
        import io
        with io.open(json_file_path, 'r', encoding='utf-8') as f:
            json_str = f.read()
            dto = CyborgWrapperState.from_json_str(json_str=json_str)
            return dto
