from typing import Dict, Any, List
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace
from csle_base.json_serializable import JSONSerializable


class DataCollectionJobConfig(JSONSerializable):
    """
    DTO representing the configuration of a data collection job
    """

    def __init__(self, emulation_env_name: str, num_collected_steps: int,
                 progress_percentage: float, attacker_sequence: List[EmulationAttackerAction], pid: int,
                 repeat_times: int, emulation_statistic_id: int, num_sequences_completed: int,
                 traces: List[EmulationTrace], save_emulation_traces_every: int, num_cached_traces: int,
                 defender_sequence: List[EmulationDefenderAction], log_file_path: str, physical_host_ip: str,
                 descr: str = ""):
        """
        Initializes the DTO

        :param emulation_env_name: the emulation environment name
        :param num_collected_steps: number of collected steps in the emulation
        :param num_sequences_completed: number of sequences completed
        :param progress_percentage: the progress of the data collection job in %
        :param attacker_sequence: the sequence of actions to emulate the attacker
        :param defender_sequence: the sequence of actions to emulate the defender
        :param repeat_times: the number of times to repeat the sequences
        :param traces: list of collected emulation traces
        :param descr: description of the job
        :param emulation_statistic_id: the id of the emulation statistic
        :param save_emulation_traces_every: the frequency to save emulation traces to the metastore
        :param num_cached_traces: the number of emulation traces to keep with the job metadata
        :param physical_host_ip: the IP of the physical host where the job is running
        """
        self.emulation_env_name = emulation_env_name
        self.progress_percentage = round(progress_percentage, 3)
        self.pid = pid
        self.num_collected_steps = num_collected_steps
        self.progress_percentage = self.progress_percentage
        self.attacker_sequence = attacker_sequence
        self.defender_sequence = defender_sequence
        self.id = -1
        self.running = False
        self.descr = descr
        self.repeat_times = repeat_times
        self.emulation_statistic_id = emulation_statistic_id
        self.num_sequences_completed = num_sequences_completed
        self.traces = traces
        self.save_emulation_traces_every = save_emulation_traces_every
        self.num_cached_traces = num_cached_traces
        self.log_file_path = log_file_path
        self.physical_host_ip = physical_host_ip

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["emulation_env_name"] = self.emulation_env_name
        d["progress_percentage"] = round(self.progress_percentage, 2)
        d["pid"] = self.pid
        d["num_collected_steps"] = self.num_collected_steps
        d["progress_percentage"] = self.progress_percentage
        d["attacker_sequence"] = list(map(lambda x: x.to_dict(), self.attacker_sequence))
        d["defender_sequence"] = list(map(lambda x: x.to_dict(), self.defender_sequence))
        d["id"] = self.id
        d["running"] = self.running
        d["descr"] = self.descr
        d["repeat_times"] = self.repeat_times
        d["emulation_statistic_id"] = self.emulation_statistic_id
        d["traces"] = list(map(lambda x: x.to_dict(), self.traces))
        d["num_sequences_completed"] = self.num_sequences_completed
        d["save_emulation_traces_every"] = self.save_emulation_traces_every
        d["num_cached_traces"] = self.num_cached_traces
        d["log_file_path"] = self.log_file_path
        d["physical_host_ip"] = self.physical_host_ip
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DataCollectionJobConfig":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = DataCollectionJobConfig(
            emulation_env_name=d["emulation_env_name"], pid=d["pid"], num_collected_steps=d["num_collected_steps"],
            progress_percentage=d["progress_percentage"],
            attacker_sequence=list(map(lambda x: EmulationAttackerAction.from_dict(x), d["attacker_sequence"])),
            defender_sequence=list(map(lambda x: EmulationDefenderAction.from_dict(x), d["defender_sequence"])),
            descr=d["descr"], repeat_times=d["repeat_times"], emulation_statistic_id=d["emulation_statistic_id"],
            traces=list(map(lambda x: EmulationTrace.from_dict(x), d["traces"])),
            num_sequences_completed=d["num_sequences_completed"],
            save_emulation_traces_every=d["save_emulation_traces_every"], num_cached_traces=d["num_cached_traces"],
            log_file_path=d["log_file_path"], physical_host_ip=d["physical_host_ip"])
        obj.id = d["id"]
        obj.running = d["running"]
        return obj

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"emulation_env_name: {self.emulation_env_name}, pid: {self.pid}, " \
               f"progress_percentage: {self.progress_percentage}, " \
               f"attacker_sequence={list(map(lambda x: str(x), self.attacker_sequence))}," \
               f"defender_sequence={list(map(lambda x: str(x), self.defender_sequence))}, id: {self.id}," \
               f"running:{self.running}, descr: {self.descr}, repeat_times: {self.repeat_times}," \
               f"emulation_statistic_id: {self.emulation_statistic_id}, " \
               f"num_sequences_completed: {self.num_sequences_completed}, " \
               f"traces: {list(map(lambda x: str(x), self.traces))}, " \
               f"save_emulation_traces_every: {self.save_emulation_traces_every}, " \
               f"num_cached_traces: {self.num_cached_traces}, log_file_path: {self.log_file_path}, " \
               f"physical_host_ip: {self.physical_host_ip}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "DataCollectionJobConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return DataCollectionJobConfig.from_dict(json.loads(json_str))
