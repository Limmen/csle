from typing import List


class KafkaTopic:
    """
    DTO representing a kafka topic (Records are assumed to be comma-separated strings) where attributes define
    the list of columns in the csv.
    """

    def __init__(self, name: str, num_partitions: int, num_replicas: int, attributes: List[str]):
        """
        Initializes the DTO

        :param name: the name of the topic
        :param num_partitions: the number of partitions
        :param num_replicas: the number of replicas
        :param attributes: the attributes of the topic
        """
        self.name = name
        self.num_partitions = num_partitions
        self.num_replicas = num_replicas
        self.attributes = attributes


    @staticmethod
    def from_dict(d: dict) -> "KafkaTopic":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj= KafkaTopic(
            name=d["name"], num_replicas=d["num_replicas"], num_partitions=d["num_partitions"],
            attributes=d["attributes"]
        )
        return obj

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["name"] = self.name
        d["num_partitions"] = self.num_partitions
        d["num_replicas"] = self.num_replicas
        d["attributes"] = self.attributes
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"name:{self.name}, num_partitions: {self.num_partitions}, " \
               f"num_replicas:{self.num_replicas}, attributes: {','.join(self.attributes)}"