from typing import Dict, Any
import csle_collector.elk_manager.elk_manager_pb2


class ElkManagerUtil:
    """
    Class with utility functions related to the ELK Manager
    """

    @staticmethod
    def elk_dto_to_dict(elk_dto: csle_collector.elk_manager.elk_manager_pb2.ElkDTO) -> Dict[str, Any]:
        """
        Converts an ElkDTO to a dict

        :param elk_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["kibanaRunning"] = elk_dto.kibanaRunning
        d["elasticRunning"] = elk_dto.elasticRunning
        d["logstashRunning"] = elk_dto.logstashRunning
        return d

    @staticmethod
    def elk_dto_from_dict(d: Dict[str, Any]) -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Converts a dict representation of an ElkDTO to a DTO

        :param d: the dict to convert
        :return: the converted DTO
        """
        elk_dto = csle_collector.elk_manager.elk_manager_pb2.ElkDTO()
        elk_dto.kibanaRunning = d["kibanaRunning"]
        elk_dto.elasticRunning = d["elasticRunning"]
        elk_dto.logstashRunning = d["logstashRunning"]
        return elk_dto

    @staticmethod
    def elk_dto_empty() -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        :return: an empty ElkDTO
        """
        elk_dto = csle_collector.elk_manager.elk_manager_pb2.ElkDTO()
        elk_dto.kibanaRunning = False
        elk_dto.elasticRunning = False
        elk_dto.logstashRunning = False
        return elk_dto
