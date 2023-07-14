from typing import Dict, Any, List
from csle_ryu.dao.flow_statistic import FlowStatistic
from csle_base.json_serializable import JSONSerializable


class AvgFlowStatistic(JSONSerializable):
    """
    DTO containing avg data of a flow statistics returned by an OpenFlow switch
    """

    def __init__(self, timestamp: float, datapath_id: str,
                 total_num_packets: int, total_num_bytes: int, avg_duration_nanoseconds: int, avg_duration_seconds: int,
                 avg_hard_timeout: int, avg_idle_timeout: int, avg_priority: int, avg_cookie: int):
        """
        Initializes the DTO

        :param timestamp: the timestamp the data was received
        :param datapath_id: the datapath ID
        :param total_num_packets: the total number of packets of the flow
        :param total_num_bytes: the total number of bytes of the flow
        :param avg_duration_nanoseconds: the avg duration of the flow in nanoseconds
        :param avg_duration_seconds: the avg duration of the flow in seconds
        :param avg_hard_timeout: the avg hard timeout of the flow
        :param avg_idle_timeout: the avg idle timeout of the flow
        :param avg_priority: the avg priority of the flow
        :param avg_cookie: the avg cookie of the flow
        """
        self.timestamp = timestamp
        self.datapath_id = datapath_id
        self.total_num_packets = total_num_packets
        self.total_num_bytes = total_num_bytes
        self.avg_duration_nanoseconds = avg_duration_nanoseconds
        self.avg_duration_seconds = avg_duration_seconds
        self.avg_hard_timeout = avg_hard_timeout
        self.avg_idle_timeout = avg_idle_timeout
        self.avg_priority = avg_priority
        self.avg_cookie = avg_cookie

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AvgFlowStatistic":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = AvgFlowStatistic(
            timestamp=d["timestamp"], datapath_id=d["datapath_id"], total_num_packets=d["total_num_packets"],
            total_num_bytes=d["total_num_bytes"],
            avg_duration_nanoseconds=d["avg_duration_nanoseconds"],
            avg_duration_seconds=d["avg_duration_seconds"],
            avg_hard_timeout=d["avg_hard_timeout"], avg_idle_timeout=d["avg_idle_timeout"],
            avg_priority=d["avg_priority"],
            avg_cookie=d["avg_cookie"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["timestamp"] = self.timestamp
        d["datapath_id"] = self.datapath_id
        d["total_num_packets"] = self.total_num_packets
        d["total_num_bytes"] = self.total_num_bytes
        d["avg_duration_nanoseconds"] = self.avg_duration_nanoseconds
        d["avg_duration_seconds"] = self.avg_duration_seconds
        d["avg_hard_timeout"] = self.avg_hard_timeout
        d["avg_idle_timeout"] = self.avg_idle_timeout
        d["avg_priority"] = self.avg_priority
        d["avg_cookie"] = self.avg_cookie
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"timestamp: {self.timestamp}, datapath_id: {self.datapath_id}, " \
               f"total_num_packets: {self.total_num_packets}," \
               f"total_num_bytes: {self.total_num_bytes}, avg_duration_nanoseconds: {self.avg_duration_nanoseconds}, " \
               f"avg_hard_timeout: {self.avg_hard_timeout}, avg_idle_timeout: {self.avg_idle_timeout}, " \
               f"avg_priority: {self.avg_priority}," \
               f"avg_cookie: {self.avg_cookie}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "AvgFlowStatistic":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return AvgFlowStatistic.from_dict(json.loads(json_str))

    def copy(self) -> "AvgFlowStatistic":
        """
        :return: a copy of the DTO
        """
        return AvgFlowStatistic.from_dict(self.to_dict())

    @staticmethod
    def from_kafka_record(record: str) -> "AvgFlowStatistic":
        """
        Converts a kafka record to a DTO

        :param record: the kafka record
        :return: the DTO
        """
        parts = record.split(",")
        obj = AvgFlowStatistic(timestamp=float(parts[0]), datapath_id=parts[1],
                               total_num_packets=int(parts[2]),
                               total_num_bytes=int(parts[3]), avg_duration_nanoseconds=int(parts[4]),
                               avg_duration_seconds=int(parts[5]),
                               avg_hard_timeout=int(parts[6]), avg_idle_timeout=int(parts[7]),
                               avg_priority=int(parts[8]),
                               avg_cookie=int(parts[9]))
        return obj

    def to_kafka_record(self) -> str:
        """
        Converts the DTO into a kafka record

        :return: the kafka record
        """
        return f"{self.timestamp},{self.datapath_id}," \
               f"{self.total_num_packets},{self.total_num_bytes},{self.avg_duration_nanoseconds}," \
               f"{self.avg_duration_seconds}," \
               f"{self.avg_hard_timeout},{self.avg_idle_timeout},{self.avg_priority},{self.avg_cookie}"

    def update_with_kafka_record(self, record: str) -> None:
        """
        Updates the DTO with a new kafka record

        :param record: the kafka record
        :return: None
        """
        parts = record.split(",")
        self.timestamp = float(parts[0])
        self.datapath_id = parts[1]
        self.total_num_packets = int(parts[2])
        self.total_num_bytes = int(parts[3])
        self.avg_duration_nanoseconds = int(parts[4])
        self.avg_duration_seconds = int(parts[5])
        self.avg_hard_timeout = int(parts[6])
        self.avg_idle_timeout = int(parts[7])
        self.avg_priority = int(parts[8])
        self.avg_cookie = int(parts[9])

    @staticmethod
    def average_flow_statistics(timestamp: float, datapath_id: str,
                                flow_statistics: List[FlowStatistic]) -> "AvgFlowStatistic":
        """
        Computes the average metrics from a list of flow statistics

        :param flow_statistics: the list of flow statistics to average
        :return: the computed averages
        """
        total_num_packets = 0
        total_num_bytes = 0
        total_duration_nanoseconds = 0
        total_duration_seconds = 0
        total_hard_timeout = 0
        total_idle_timeout = 0
        total_priority = 0
        total_cookie = 0

        for flow in flow_statistics:
            total_num_packets += flow.num_packets
            total_num_bytes += flow.num_bytes
            total_duration_nanoseconds += flow.duration_nanoseconds
            total_duration_seconds += flow.duration_seconds
            total_hard_timeout += flow.hard_timeout
            total_idle_timeout += flow.idle_timeout
            total_priority += flow.priority
            total_cookie += flow.cookie

        num_flows = len(flow_statistics)
        aggregated_flow_statistics_dto = AvgFlowStatistic(
            timestamp=timestamp, datapath_id=datapath_id,
            total_num_packets=total_num_packets,
            total_num_bytes=total_num_bytes,
            avg_duration_nanoseconds=int(total_duration_nanoseconds / num_flows),
            avg_duration_seconds=int(total_duration_seconds / num_flows),
            avg_hard_timeout=int(total_hard_timeout / num_flows),
            avg_idle_timeout=int(total_idle_timeout / num_flows),
            avg_priority=int(total_priority / num_flows),
            avg_cookie=int(total_cookie / num_flows)
        )
        return aggregated_flow_statistics_dto
