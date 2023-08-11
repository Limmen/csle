from typing import Dict, Any
import csle_collector.ryu_manager.ryu_manager_pb2


class RyuManagerUtil:
    """
    Class with utility functions related to the Ryu Manager
    """

    @staticmethod
    def ryu_dto_to_dict(ryu_dto: csle_collector.ryu_manager.ryu_manager_pb2.RyuDTO) -> Dict[str, Any]:
        """
        Converts a RyuDTO to a dict

        :param ryu_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["ryu_running"] = ryu_dto.ryu_running
        d["monitor_running"] = ryu_dto.monitor_running
        d["port"] = ryu_dto.port
        d["web_port"] = ryu_dto.web_port
        d["controller"] = ryu_dto.controller
        d["kafka_ip"] = ryu_dto.kafka_ip
        d["kafka_port"] = ryu_dto.kafka_port
        d["time_step_len"] = ryu_dto.time_step_len
        return d

    @staticmethod
    def ryu_dto_from_dict(d: Dict[str, Any]) -> csle_collector.ryu_manager.ryu_manager_pb2.RyuDTO:
        """
        Converts a dict representation of a RyuDTO to a DTO

        :param d: the dict to convert
        :return: the converted DTO
        """
        ryu_dto = csle_collector.ryu_manager.ryu_manager_pb2.RyuDTO()
        ryu_dto.ryu_running = d["ryu_running"]
        ryu_dto.monitor_running = d["monitor_running"]
        ryu_dto.port = d["port"]
        ryu_dto.web_port = d["web_port"]
        ryu_dto.controller = d["controller"]
        ryu_dto.kafka_ip = d["kafka_ip"]
        ryu_dto.kafka_port = d["kafka_port"]
        ryu_dto.time_step_len = d["time_step_len"]
        return ryu_dto

    @staticmethod
    def ryu_dto_empty() -> csle_collector.ryu_manager.ryu_manager_pb2.RyuDTO:
        """
        :return: an empty RyuDTO
        """
        ryu_dto = csle_collector.ryu_manager.ryu_manager_pb2.RyuDTO()
        ryu_dto.ryu_running = False
        ryu_dto.monitor_running = False
        ryu_dto.port = 6633
        ryu_dto.web_port = 8080
        ryu_dto.kafka_ip = ""
        ryu_dto.kafka_port = 9092
        ryu_dto.controller = ""
        ryu_dto.time_step_len = 30
        return ryu_dto
