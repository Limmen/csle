from typing import Dict, Any
import csle_collector.elk_manager.elk_manager_pb2


class ElkManagerUtil:
    """
    Class with utility functions related to the Elk Manager
    """

    @staticmethod
    def elk_dto_to_dict(elk_dto: csle_collector.elk_manager.elk_manager_pb2.ElkDTO) -> Dict[str, Any]:
        """
        Converts an ElkDTO to a dict

        :param elk_dto: the dto to convert
        :return: a dict frepresentation of the DTO
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
