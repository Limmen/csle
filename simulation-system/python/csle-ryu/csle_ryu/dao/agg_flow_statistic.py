from typing import Dict, Any


class AggFlowStatistic:
    """
    DTO containing aggregated flow statistics of an OpenFlow switch
    """

    def __init__(self, timestamp: float, datapath_id: int, total_num_packets: int, total_num_bytes: int,
                 total_num_flows: int):
        """
        Initializes the DTO

        :param timestamp: the timestamp the data was received
        :param datapath_id: the datapath ID
        :param total_num_packets: the total number of packets
        :param total_num_bytes: the total number of bytes
        :param total_num_flows: the total number of flows
        :param avg_duration_nanoseconds: the avg duration of the flow in nanoseconds
        """
        self.timestamp = timestamp
        self.datapath_id = datapath_id
        self.total_num_packets = total_num_packets
        self.total_num_bytes = total_num_bytes
        self.total_num_flows = total_num_flows

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AggFlowStatistic":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = AggFlowStatistic(
            timestamp=d["timestamp"], datapath_id=d["datapath_id"], total_num_packets=d["total_num_packets"],
            total_num_flows=d["total_num_flows"], total_num_bytes=d["total_num_bytes"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["timestamp"] = self.timestamp
        d["datapath_id"] = self.datapath_id
        d["total_num_packets"] = self.total_num_packets
        d["total_num_bytes"] = self.total_num_bytes
        d["total_num_flows"] = self.total_num_flows
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"timestamp: {self.timestamp}, datapath_id: {self.datapath_id}, " \
               f"total_num_packets: {self.total_num_packets}," \
               f"total_num_bytes: {self.total_num_bytes}, total_num_flows: {self.total_num_flows}"

    def to_json_str(self) -> str:
        """
        Converts the DTO into a json string

        :return: the json string representation of the DTO
        """
        import json
        json_str = json.dumps(self.to_dict(), indent=4, sort_keys=True)
        return json_str

    def to_json_file(self, json_file_path: str) -> None:
        """
        Saves the DTO to a json file

        :param json_file_path: the json file path to save  the DTO to
        :return: None
        """
        import io
        json_str = self.to_json_str()
        with io.open(json_file_path, 'w', encoding='utf-8') as f:
            f.write(json_str)

    def copy(self) -> "AggFlowStatistic":
        """
        :return: a copy of the DTO
        """
        return AggFlowStatistic.from_dict(self.to_dict())

    @staticmethod
    def from_kafka_record(record: str) -> "AggFlowStatistic":
        """
        Converts a kafka record to a DTO

        :param record: the kafka record
        :return: the DTO
        """
        parts = record.split(",")
        obj = AggFlowStatistic(timestamp=float(parts[0]), datapath_id=int(parts[1]), total_num_packets=int(parts[2]),
                               total_num_bytes=int(parts[3]), total_num_flows=int(parts[4]))
        return obj

    def to_kafka_record(self) -> str:
        """
        Converts the DTO into a kafka record

        :return: the kafka record
        """
        return f"{self.timestamp},{self.datapath_id}," \
               f"{self.total_num_packets},{self.total_num_bytes},{self.total_num_flows}"

    def update_with_kafka_record(self, record: str) -> None:
        """
        Updates the DTO with a new kafka record

        :param record: the kafka record
        :return: None
        """
        parts = record.split(",")
        self.timestamp = float(parts[0])
        self.datapath_id = int(parts[1])
        self.total_num_packets = int(parts[2])
        self.total_num_bytes = int(parts[3])
        self.total_num_flows = int(parts[4])
