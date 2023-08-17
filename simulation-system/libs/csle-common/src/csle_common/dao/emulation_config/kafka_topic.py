from typing import List, Dict, Any, Union
from csle_base.json_serializable import JSONSerializable


class KafkaTopic(JSONSerializable):
    """
    DTO representing a kafka topic (Records are assumed to be comma-separated strings) where attributes define
    the list of columns in the csv.
    """

    def __init__(self, name: str, num_partitions: int, num_replicas: int, attributes: List[str],
                 retention_time_hours: int):
        """
        Initializes the DTO

        :param name: the name of the topic
        :param num_partitions: the number of partitions
        :param num_replicas: the number of replicas
        :param attributes: the attributes of the topic
        :param retention_time_hours: the retention time of the topic (how long to store the data)
        """
        self.name = name
        self.num_partitions = num_partitions
        self.num_replicas = num_replicas
        self.attributes = attributes
        self.retention_time_hours = retention_time_hours

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "KafkaTopic":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = KafkaTopic(name=d["name"], num_replicas=d["num_replicas"], num_partitions=d["num_partitions"],
                         attributes=d["attributes"], retention_time_hours=d["retention_time_hours"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Union[str, int, List[str]]] = {}
        d["name"] = self.name
        d["num_partitions"] = self.num_partitions
        d["num_replicas"] = self.num_replicas
        d["attributes"] = self.attributes
        d["retention_time_hours"] = self.retention_time_hours
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"name:{self.name}, num_partitions: {self.num_partitions}, " \
               f"num_replicas:{self.num_replicas}, attributes: {','.join(self.attributes)}, " \
               f"retention_time_hours:{self.retention_time_hours}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "KafkaTopic":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return KafkaTopic.from_dict(json.loads(json_str))

    def copy(self) -> "KafkaTopic":
        """
        :return: a copy of the DTO
        """
        return KafkaTopic.from_dict(self.to_dict())

    @staticmethod
    def schema() -> "KafkaTopic":
        """
        :return: get the schema of the DTO
        """
        return KafkaTopic(name="", num_partitions=1, num_replicas=1, attributes=[""], retention_time_hours=1)
