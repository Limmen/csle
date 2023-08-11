from typing import Dict, Any, Union
import csle_collector.traffic_manager.traffic_manager_pb2


class TrafficManagerUtil:
    """
    Class with utility functions related to the Traffic Manager
    """

    @staticmethod
    def traffic_dto_to_dict(traffic_dto: csle_collector.traffic_manager.traffic_manager_pb2.TrafficDTO) \
            -> Dict[str, Union[bool, str]]:
        """
        Converts a TrafficDTO to a dict

        :param traffic_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Union[bool, str]] = {}
        d["running"] = traffic_dto.running
        d["script"] = traffic_dto.script
        return d

    @staticmethod
    def traffic_dto_from_dict(d: Dict[str, Any]) -> csle_collector.traffic_manager.traffic_manager_pb2.TrafficDTO:
        """
        Converts a dict representation of a TrafficDTO to a DTO

        :param d: the dict to convert
        :return: the converted DTO
        """
        traffic_dto = csle_collector.traffic_manager.traffic_manager_pb2.TrafficDTO()
        traffic_dto.running = d["running"]
        traffic_dto.script = d["script"]
        return traffic_dto

    @staticmethod
    def traffic_dto_empty() -> csle_collector.traffic_manager.traffic_manager_pb2.TrafficDTO:
        """
        :return: an empty TrafficDTO
        """
        traffic_dto = csle_collector.traffic_manager.traffic_manager_pb2.TrafficDTO()
        traffic_dto.running = False
        traffic_dto.script = ""
        return traffic_dto
