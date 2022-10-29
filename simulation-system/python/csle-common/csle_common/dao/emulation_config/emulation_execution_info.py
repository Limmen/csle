from typing import Dict, Any
from csle_common.dao.emulation_config.snort_managers_info import SnortManagersInfo
from csle_common.dao.emulation_config.ossec_managers_info import OSSECIDSManagersInfo
from csle_common.dao.emulation_config.kafka_managers_info import KafkaManagersInfo


class EmulationExecutionInfo:
    """
    DTO containing the runtime status of an emulation execution
    """

    def __init__(self, emulation_name: str, execution_id: int, snort_managers_info: SnortManagersInfo,
                 ossec_managers_info: OSSECIDSManagersInfo, kafka_managers_info: KafkaManagersInfo):
        self.emulation_name = emulation_name
        self.execution_id = execution_id
        self.snort_managers_info = snort_managers_info
        self.ossec_managers_info = ossec_managers_info
        self.kafka_managers_info = kafka_managers_info

    def __str__(self):
        """
        :return: a string representation of the DTO
        """
        return f"emulation_name: {self.emulation_name}, execution id: {self.execution_id}, " \
               f"snort_managers_info: {self.snort_managers_info}, ossec_managers_info: {self.ossec_managers_info}," \
               f"kafka_managers_info: {self.kafka_managers_info}"

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["emulation_name"] = self.emulation_name
        d["execution_id"] = self.execution_id
        d["snort_managers_info"] = self.snort_managers_info.to_dict()
        d["ossec_managers_info"] = self.ossec_managers_info.to_dict()
        d["kafka_managers_info"] = self.kafka_managers_info.to_dict()
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EmulationExecutionInfo":
        """
        Convert a dict representation to a DTO representation

        :return: a dto representation of the object
        """
        dto = EmulationExecutionInfo(emulation_name=d["emulation_name"], execution_id=d["execution_id"],
                                     snort_managers_info=SnortManagersInfo.from_dict(d["snort_managers_info"]),
                                     ossec_managers_info=OSSECIDSManagersInfo.from_dict(d["ossec_managers_info"]),
                                     kafka_managers_info=d["kafka_managers_info"])
        return dto