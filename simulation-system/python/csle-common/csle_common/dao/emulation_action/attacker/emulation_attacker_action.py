from typing import List, Tuple, Dict, Any
import time
import csle_common.constants.constants as constants
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_outcome import EmulationAttackerActionOutcome
from csle_common.util.general_util import GeneralUtil


class EmulationAttackerAction:
    """
    Class representing an action of the attacker in the emulation
    """
    def __init__(self, id: EmulationAttackerActionId, name: str, cmds: List[str],
                 type: EmulationAttackerActionType, descr: str, ips: List[str], index: int,
                 action_outcome: EmulationAttackerActionOutcome = EmulationAttackerActionOutcome.INFORMATION_GATHERING,
                 vulnerability: str = None, alt_cmds: List[str] = None, backdoor: bool = False,
                 execution_time: float = 0, ts: float = None):
        """
        Class constructor

        :param id: id of the action
        :param name: name of the action
        :param cmds: command-line commands to apply the action on the emulation
        :param type: type of the action
        :param descr: description of the action (documentation)
        :param ips: ips of the machines to apply the action to
        :param index: index of the machien to apply the action to
        :param action_outcome: type of the outcome of the action
        :param vulnerability: type of vulnerability that the action exploits (in case an exploit)
        :param alt_cmds: alternative command if the first command does not work
        :param backdoor: if the action also installs a backdoor (some exploits does this)
        :param execution_time: the time it took to run the action
        :param ts: the timestep the action was completed
        """
        self.type = type
        self.id = id
        self.name = name
        self.cmds = cmds
        if self.cmds is None:
            self.cmds = []
        self.descr = descr
        self.index = index
        self.ips = ips
        if self.ips is None:
            self.ips = []
        self.vulnerability = vulnerability
        self.action_outcome = action_outcome
        self.backdoor = backdoor
        self.alt_cmds = alt_cmds
        if self.alt_cmds is None:
            self.alt_cmds = []
        self.index = index
        self.backdoor = backdoor
        self.execution_time = execution_time
        self.ts = ts

    def nmap_cmds(self, machine_ips: List[str] = None) -> Tuple[List[str], List[str]]:
        """
        Augments the original command of the action with extra flags for NMAP

        :param machine_ips: list of ips
        :return: the new command
        """
        commands = []
        file_names = []
        for ip in self.ips:
            file_name = str(self.id) + "_" + str(self.index) + "_" + ip.replace("/", "_")
            file_name = file_name + ".xml "
            commands.append(self.cmds[0] + constants.NMAP.FILE_ARGS + " " + file_name + ip)
            file_names.append(file_name)
        if machine_ips is None:
            machine_ips = []
        for ip in machine_ips:
            file_name = str(self.id) + "_" + str(self.index) + "_" + ip.replace("/", "_")
            file_name = file_name + ".xml "
            commands.append(self.cmds[0] + constants.NMAP.FILE_ARGS + " " + file_name + ip)
            file_names.append(file_name)
        return commands, file_names

    def nikto_cmds(self) -> Tuple[List[str], List[str]]:
        """
        Augments the original command of the action with extra flags for Nikto

        :return: the new command
        """
        file_names = []
        commands = []
        for ip in self.ips:
            file_name = str(self.id) + "_" + str(self.index) + "_" + ip + ".xml "
            commands.append(self.cmds[0] + constants.NIKTO.HOST_ARG + ip + " " + constants.NIKTO.OUTPUT_ARG + file_name)
            file_names.append(file_name)
        return commands, file_names

    def masscan_cmds(self) -> Tuple[List[str], List[str]]:
        """
        Augments the original command of the action with extra flags for massscan

        :return: the new command
        """
        commands = []
        file_names = []
        for ip in self.ips:
            file_name = str(self.id) + "_" + str(self.index) + "_" + ip + ".xml "
            if self.index == -1:
                file_name = str(self.id) + "_" + str(self.index) + ".xml "
            commands.append(self.cmds[0] + constants.MASSCAN.OUTPUT_ARG + " " + file_name + ip)
            file_names.append(file_name)
        return commands, file_names

    def __str__(self):
        """
        :return: a string representation of the object
        """
        return "id:{},name:{},ips:{},index:{}".format(self.id, self.name, self.ips, self.index)

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EmulationAttackerAction":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = EmulationAttackerAction(
            type=d["type"], id=d["id"], name=d["name"], cmds=d["cmds"], descr=d["descr"], index=d["index"],
            ips=d["ips"], vulnerability=d["vulnerability"], action_outcome=d["action_outcome"],
            backdoor=d["backdoor"], alt_cmds=d["alt_cmds"], execution_time=d["execution_time"], ts=d["ts"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["id"] = self.id
        d["name"] = self.name
        d["cmds"] = self.cmds
        d["type"] = self.type
        d["descr"] = self.descr
        d["ips"] = self.ips
        d["index"] = self.index
        d["action_outcome"] = self.action_outcome
        d["vulnerability"] = self.vulnerability
        d["alt_cmds"] = self.alt_cmds
        d["backdoor"] = self.backdoor
        d["execution_time"] = self.execution_time
        d["ts"] = self.ts
        return d

    def ips_match(self, ips: List[str]) -> bool:
        """
        Checks if a list of ips overlap with the ips of this host

        :param ips: the list of ips to check
        :return:  True if they match, False otherwise
        """
        for ip in self.ips:
            if ip in ips:
                return True
        return False

    def to_kafka_record(self) -> str:
        """
        Converts the instance into a kafka record format

        :param total_time: the total time of execution
        :return: the kafka record
        """
        if self.vulnerability is None:
            vuln = ""
        else:
            vuln = self.vulnerability
        if self.alt_cmds is None:
            alt_cmds = []
        else:
            alt_cmds = self.alt_cmds
        ts = time.time()
        if self.alt_cmds is None or len(self.alt_cmds) == 0:
            self.alt_cmds = ["-"]
        if self.cmds is None or len(self.cmds) == 0:
            self.cmds = ["-"]
        alt_cmds = list(map(lambda x: x.replace(",", "-"), alt_cmds))
        vuln = vuln.replace(",", "-")
        cmds = list(map(lambda x: x.replace(",", "-"), self.cmds))
        record = f"{ts},{self.id},{self.descr.replace(',', '')},{self.index},{self.name.replace(',', '-')}," \
                 f"{self.execution_time},{'_'.join(self.ips)},{'_'.join(cmds)},{self.type}," \
                 f"{self.action_outcome},{vuln}," \
                 f"{'_'.join(alt_cmds)},{self.backdoor}"
        return record

    @staticmethod
    def from_kafka_record(record: str) -> "EmulationAttackerAction":
        """
        Converts a kafka record into an instance

        :param record: the record to convert
        :return: the created instance
        """
        parts = record.split(",")
        obj = EmulationAttackerAction(id=EmulationAttackerActionId(int(parts[1])), ts=float(parts[0]),
                                      descr=parts[2], index=int(parts[3]),
                                      name=parts[4],
                                      execution_time=float(parts[5]), ips=parts[6].split("_"),
                                      cmds=parts[7].split("_"),
                                      type=EmulationAttackerActionType(int(parts[8])),
                                      action_outcome=EmulationAttackerActionOutcome(int(parts[9])),
                                      vulnerability=parts[10], alt_cmds=parts[11].split("_"),
                                      backdoor=parts[12] == "True")
        return obj

    def to_json_str(self) -> str:
        """
        Converts the DTO into a json string

        :return: the json string representation of the DTO
        """
        import json
        json_str = json.dumps(self.to_dict(), indent=4, sort_keys=True)
        return json_str

    def to_json_file(self, json_file_path: str) -> None:
        """
        Saves the DTO to a json file

        :param json_file_path: the json file path to save  the DTO to
        :return: None
        """
        import io
        json_str = self.to_json_str()
        with io.open(json_file_path, 'w', encoding='utf-8') as f:
            f.write(json_str)

    def copy(self) -> "EmulationAttackerAction":
        """
        :return: a copy of the DTO
        """
        return EmulationAttackerAction.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "EmulationAttackerAction":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.ips = list(map(lambda x: GeneralUtil.replace_first_octet_of_ip(ip=x, ip_first_octet=ip_first_octet),
                              config.ips))
        return config

    def num_attributes(self) -> int:
        """
        :return: The number of attributes of the DTO
        """
        return 13

    @staticmethod
    def schema() -> "EmulationAttackerAction":
        """
        :return: get the schema of the DTO
        """
        return EmulationAttackerAction(id=EmulationAttackerActionId.STOP, name="", cmds=[""],
                                       type=EmulationAttackerActionType.STOP, descr="", ips=[""], index=-1,
                                       action_outcome=EmulationAttackerActionOutcome.INFORMATION_GATHERING,
                                       vulnerability="", alt_cmds=[""], backdoor=False, execution_time=0.0, ts=0.0)
