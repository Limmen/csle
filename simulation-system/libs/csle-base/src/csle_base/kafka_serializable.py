from abc import abstractmethod, ABC


class KafkaSerializable(ABC):
    """
    Abstract class representing objects that are Kafka serializable
    """

    @abstractmethod
    def to_kafka_record(self, ip: str) -> str:
        """
        Converts the DTO into a kafka record

        :param ip: the ip to add to the record in addition to the IDS statistics
        :return: a comma-separated string representing the kafka record
        """
        pass

    @staticmethod
    @abstractmethod
    def from_kafka_record(record: str) -> "KafkaSerializable":
        """
        Converts a kafka record to a DTO

        :param record: the kafka record to convert
        :return: the DTO
        """
        pass
