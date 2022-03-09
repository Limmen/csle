from typing import List


class KafkaTopic:
    """
    DTO representing a kafka topic (Records are assumed to be comma-separated strings) where attributes define
    the list of columns in the csv.
    """

    def __init__(self, name: str, num_partitions: int, num_replicas: int, attributes: List[str]):
        self.name = name
        self.num_partitions = num_partitions
        self.num_replicas = num_replicas
        self.attributes = attributes

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