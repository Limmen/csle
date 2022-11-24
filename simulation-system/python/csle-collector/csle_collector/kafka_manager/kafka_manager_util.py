from typing import Dict, Any
import csle_collector.kafka_manager.kafka_manager_pb2


class KafkaManagerUtil:
    """
    Class with utility functions related to the Kafka Manager
    """

    @staticmethod
    def kafka_dto_to_dict(kafka_dto: csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO) -> Dict[str, Any]:
        """
        Converts a KafkaDTO to a dict

        :param kafka_dto: the dto to convert
        :return: a dict representation of the DTO
        """
        d = {}
        d["running"] = kafka_dto.running
        topics = []
        for top in kafka_dto.topics:
            topics.append(str(top))
        d["topics"] = topics
        return d

    @staticmethod
    def kafka_dto_from_dict(d: Dict[str, Any]) -> csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO:
        """
        Converts a dict representation of a KafkaDTO to a DTO

        :param d: the dict to convert
        :return: the converted DTO
        """
        kafka_dto = csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO()
        kafka_dto.running = d["running"]
        kafka_dto.topics = d["topics"]
        return kafka_dto

    @staticmethod
    def kafka_dto_empty() -> csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO:
        """
        :return: an empty KafkaDTO
        """
        kafka_dto = csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO()
        kafka_dto.running = False
        return kafka_dto
