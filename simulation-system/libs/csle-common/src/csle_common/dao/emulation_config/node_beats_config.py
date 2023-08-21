from typing import List, Dict, Any
from csle_common.util.general_util import GeneralUtil
from csle_base.json_serializable import JSONSerializable


class NodeBeatsConfig(JSONSerializable):
    """
    A DTO object representing the beats configuration of an individual container in an emulation
    """

    def __init__(self, ip: str, log_files_paths: List[str], filebeat_modules: List[str],
                 metricbeat_modules: List[str], heartbeat_hosts_to_monitor: List[str],
                 kafka_input: bool = False,
                 start_filebeat_automatically: bool = False, start_packetbeat_automatically: bool = False,
                 start_metricbeat_automatically: bool = False, start_heartbeat_automatically: bool = False):
        """
        Initializes the DTO

        :param ip: the ip of the nod
        :param log_files_paths: list of log files to ingest to elastic through filebeat
        :param filebeat_modules: list of filebeat modules to enable
        :param metricbeat_modules: list of metricbeat modules to enable
        :param heartbeat_hosts_to_monitor: list of hosts to monitor with heartbeat
        :param kafka_input: boolean indicating whether the kafka log should be ingested from this node or not
        :param start_filebeat_automatically: boolean indicating whether filebeat should be started automatically
                                             when the emulation is started
        :param start_packetbeat_automatically: boolean indicating whether packetbeat should be started automatically
                                               when the emulation is started
        :param start_metricbeat_automatically: boolean indicating whether metricbeat should be started automatically
                                               when the emulation is started
        :param start_heartbeat_automatically: boolean indicating whether heartbeat should be started automatically
                                               when the emulation is started
        """
        self.ip = ip
        self.log_files_paths = log_files_paths
        self.filebeat_modules = filebeat_modules
        self.kafka_input = kafka_input
        self.start_filebeat_automatically = start_filebeat_automatically
        self.start_packetbeat_automatically = start_packetbeat_automatically
        self.metricbeat_modules = metricbeat_modules
        self.start_metricbeat_automatically = start_metricbeat_automatically
        self.start_heartbeat_automatically = start_heartbeat_automatically
        self.heartbeat_hosts_to_monitor = heartbeat_hosts_to_monitor

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NodeBeatsConfig":
        """
        Converts a dict representation into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = NodeBeatsConfig(
            ip=d["ip"], log_files_paths=d["log_files_paths"], filebeat_modules=d["filebeat_modules"],
            kafka_input=d["kafka_input"], start_filebeat_automatically=d["start_filebeat_automatically"],
            start_packetbeat_automatically=d["start_packetbeat_automatically"],
            metricbeat_modules=d["metricbeat_modules"],
            start_metricbeat_automatically=d["start_metricbeat_automatically"],
            start_heartbeat_automatically=d["start_heartbeat_automatically"],
            heartbeat_hosts_to_monitor=d["heartbeat_hosts_to_monitor"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["ip"] = self.ip
        d["log_files_paths"] = self.log_files_paths
        d["filebeat_modules"] = self.filebeat_modules
        d["kafka_input"] = self.kafka_input
        d["start_filebeat_automatically"] = self.start_filebeat_automatically
        d["start_packetbeat_automatically"] = self.start_packetbeat_automatically
        d["metricbeat_modules"] = self.metricbeat_modules
        d["start_metricbeat_automatically"] = self.start_metricbeat_automatically
        d["start_heartbeat_automatically"] = self.start_heartbeat_automatically
        d["heartbeat_hosts_to_monitor"] = self.heartbeat_hosts_to_monitor
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ip:{self.ip}, log_files_paths: {self.log_files_paths}, filebeat_modules: {self.filebeat_modules}, " \
               f"kafka_input: {self.kafka_input}, start_filebeat_automatically: {self.start_filebeat_automatically}, " \
               f"start_packetbeat_automatically: {self.start_packetbeat_automatically}, " \
               f"metricbeat_modules: {self.metricbeat_modules}, " \
               f"start_metricbeat_automatically: {self.start_metricbeat_automatically}," \
               f"start_heartbeat_automatically: {self.start_heartbeat_automatically}," \
               f"heartbeat_hosts_to_monitor: {self.heartbeat_hosts_to_monitor}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "NodeBeatsConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return NodeBeatsConfig.from_dict(json.loads(json_str))

    def copy(self) -> "NodeBeatsConfig":
        """
        :return: a copy of the DTO
        """
        return NodeBeatsConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "NodeBeatsConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.ip = GeneralUtil.replace_first_octet_of_ip(ip=config.ip, ip_first_octet=ip_first_octet)
        heartbeat_hosts_to_monitor = []
        for host in self.heartbeat_hosts_to_monitor:
            heartbeat_hosts_to_monitor.append(GeneralUtil.replace_first_octet_of_ip(ip=host,
                                                                                    ip_first_octet=ip_first_octet))
        config.heartbeat_hosts_to_monitor = heartbeat_hosts_to_monitor
        return config
