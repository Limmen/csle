from typing import Dict, Any


class FlowStatistic:
    """
    DTO containing data of a flow statistic returned by an OpenFlow switch
    """

    def __init__(self, timestamp: float, datapath_id: int, in_port: int, out_port: int, dst_mac_address: str,
                 num_packets: int, num_bytes: int, duration_nanoseconds: int, duration_seconds: int, hard_timeout: int,
                 idle_timeout: int, priority: int, cookie: int):
        """
        Initializes the DTO

        :param timestamp: the timestamp the data was received
        :param datapath_id: the datapath ID
        :param in_port: the input port of the flow
        :param out_port: the output port of the flow
        :param dst_mac_address: the destination MAC address of the flow
        :param num_packets: the number of packets of the flow
        :param num_bytes: the number of bytes of the flow
        :param duration_nanoseconds: the duration of the flow in nanoseconds
        :param duration_seconds: the duration of the flow in seconds
        :param hard_timeout: the hard timeout of the flow
        :param idle_timeout: the idle timeout of the flow
        :param priority: the priority of the flow
        :param cookie: the cookie of the flow
        """
        self.timestamp = timestamp
        self.datapath_id = datapath_id
        self.in_port = in_port
        self.out_port = out_port
        self.dst_mac_address = dst_mac_address
        self.num_packets = num_packets
        self.num_bytes = num_bytes
        self.duration_nanoseconds = duration_nanoseconds
        self.duration_seconds = duration_seconds
        self.hard_timeout = hard_timeout
        self.idle_timeout = idle_timeout
        self.priority = priority
        self.cookie = cookie

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FlowStatistic":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = FlowStatistic(
            timestamp=d["timestamp"], datapath_id=d["datapath_id"], in_port=d["in_port"], out_port=d["out_port"],
            dst_mac_address=d["dst_mac_address"], num_packets=d["num_packets"], num_bytes=d["num_bytes"],
            duration_nanoseconds=d["duration_nanoseconds"], duration_seconds=d["duration_seconds"],
            hard_timeout=d["hard_timeout"], idle_timeout=d["idle_timeout"], priority=d["priority"], cookie=d["cookie"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["timestamp"] = self.timestamp
        d["datapath_id"] = self.datapath_id
        d["in_port"] = self.in_port
        d["out_port"] = self.out_port
        d["dst_mac_address"] = self.dst_mac_address
        d["num_packets"] = self.num_packets
        d["num_bytes"] = self.num_bytes
        d["duration_nanoseconds"] = self.duration_nanoseconds
        d["duration_seconds"] = self.duration_seconds
        d["hard_timeout"] = self.hard_timeout
        d["idle_timeout"] = self.idle_timeout
        d["priority"] = self.priority
        d["cookie"] = self.cookie
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"timestamp: {self.timestamp}, datapath_id: {self.datapath_id}, in_port: {self.in_port}, " \
               f"out_port: {self.out_port}, dst_mac_address: {self.dst_mac_address}, num_packets: {self.num_packets}," \
               f"num_bytes: {self.num_bytes}, duration_nanoseconds: {self.duration_nanoseconds}, " \
               f"hard_timeout: {self.hard_timeout}, idle_timeout: {self.idle_timeout}, priority: {self.priority}," \
               f"cookie: {self.cookie}"

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

    def copy(self) -> "FlowStatistic":
        """
        :return: a copy of the DTO
        """
        return FlowStatistic.from_dict(self.to_dict())

    @staticmethod
    def from_kafka_record(record: str) -> "FlowStatistic":
        """
        Converts a kafka record to a DTO

        :param record: the kafka record
        :return: the DTO
        """
        parts = record.split(",")
        obj = FlowStatistic(timestamp=float(parts[0]), datapath_id=int(parts[1]), in_port=int(parts[2]),
                            out_port=int(parts[3]), dst_mac_address=parts[4], num_packets=int(parts[5]),
                            num_bytes=int(parts[6]), duration_nanoseconds=int(parts[7]),
                            duration_seconds=int(parts[8]),
                            hard_timeout=int(parts[9]), idle_timeout=int(parts[10]), priority=int(parts[11]),
                            cookie=int(parts[12]))
        return obj

    def to_kafka_record(self) -> str:
        """
        Converts the DTO into a kafka record

        :return: the kafka record
        """
        return f"{self.timestamp},{self.datapath_id},{self.in_port},{self.out_port},{self.dst_mac_address}," \
               f"{self.num_packets},{self.num_bytes},{self.duration_nanoseconds},{self.duration_seconds}," \
               f"{self.hard_timeout},{self.idle_timeout},{self.priority},{self.cookie}"

    def update_with_kafka_record(self, record: str) -> None:
        """
        Updates the DTO with a new kafka record

        :param record: the kafka record
        :return: None
        """
        parts = record.split(",")
        self.timestamp = float(parts[0])
        self.datapath_id = int(parts[1])
        self.in_port = int(parts[2])
        self.out_port = int(parts[3])
        self.dst_mac_address = int(parts[4])
        self.num_packets = int(parts[5])
        self.num_bytes = int(parts[6])
        self.duration_nanoseconds = int(parts[7])
        self.duration_seconds = int(parts[8])
        self.hard_timeout = int(parts[9])
        self.idle_timeout = int(parts[10])
        self.priority = int(parts[11])
        self.cookie = int(parts[12])
