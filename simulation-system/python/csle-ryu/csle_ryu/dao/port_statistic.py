from typing import Dict, Any


class PortStatistic:
    """
    DTO containing data with port statistics from an OpenFlow switch
    """

    def __init__(self, timestamp: float, datapath_id: int, port: int, num_received_packets: int,
                 num_received_bytes: int, num_received_errors: int, num_transmitted_packets: int,
                 num_transmitted_bytes: int, num_transmitted_errors: int, num_received_dropped: int,
                 num_transmitted_dropped, num_received_frame_errors, num_received_overrun_errors,
                 num_received_crc_errors, num_collisions, duration_nanoseconds, duration_seconds):
        """
        Initializes the DTO

        :param timestamp: the timestamp the statistic was received
        :param datapath_id: the datapath id
        :param port: the port
        :param num_received_packets: the number of received packets on the port
        :param num_received_bytes: the number of received bytes on the port
        :param num_received_errors: the number of received errors on the port
        :param num_transmitted_packets: the number of transmitted packets on the port
        :param num_transmitted_bytes: the nubmer of transmitted bytes on the port
        :param num_transmitted_errors: the number of transmitted errors on the port
        :param num_received_dropped: the number of received packets dropped on the port
        :param num_transmitted_dropped: the number of transmitted packets dropped on the port
        :param num_received_frame_errors: the number of received frame errors on the port
        :param num_received_overrun_errors: the number of overrun errors on the port
        :param num_received_crc_errors: the number of received crc errors on the port
        :param num_collisions: the number of collisions on the port
        :param duration_nanoseconds: the duration the port has been up in nanoseconds
        :param duration_seconds: the duration the port has been up in seconds
        """
        self.timestamp = timestamp
        self.datapath_id = datapath_id
        self.port = port
        self.num_received_packets = num_received_packets
        self.num_received_bytes = num_received_bytes
        self.num_received_errors = num_received_errors
        self.num_transmitted_packets = num_transmitted_packets
        self.num_transmitted_bytes = num_transmitted_bytes
        self.num_transmitted_errors = num_transmitted_errors
        self.num_received_dropped = num_received_dropped
        self.num_transmitted_dropped = num_transmitted_dropped
        self.num_received_frame_errors = num_received_frame_errors
        self.num_received_overrun_errors = num_received_overrun_errors
        self.num_received_crc_errors = num_received_crc_errors
        self.num_collisions = num_collisions
        self.duration_nanoseconds = duration_nanoseconds
        self.duration_seconds = duration_seconds

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "PortStatistic":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = PortStatistic(
            timestamp=d["timestamp"], datapath_id=d["datapath_id"],
            port=d["port"], num_received_packets=d["num_received_packets"], num_received_bytes=d["num_received_bytes"],
            num_received_errors=d["num_received_errors"], num_transmitted_packets=d["num_transmitted_packets"],
            num_transmitted_bytes=d["num_transmitted_bytes"], num_transmitted_errors=d["num_transmitted_errors"],
            num_received_dropped=d["num_received_dropped"], num_transmitted_dropped=d["num_transmitted_dropped"],
            num_received_frame_errors=d["num_received_frame_errors"],
            num_received_overrun_errors=d["num_received_overrun_errors"],
            num_received_crc_errors=d["num_received_crc_errors"],
            num_collisions=d["num_collisions"], duration_nanoseconds=d["duration_nanoseconds"],
            duration_seconds=d["duration_seconds"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["timestamp"] = self.timestamp
        d["datapath_id"] = self.datapath_id
        d["port"] = self.port
        d["num_received_packets"] = self.num_received_packets
        d["num_received_bytes"] = self.num_received_bytes
        d["num_received_errors"] = self.num_received_errors
        d["num_transmitted_packets"] = self.num_transmitted_packets
        d["num_transmitted_bytes"] = self.num_transmitted_bytes
        d["num_transmitted_errors"] = self.num_transmitted_errors
        d["num_received_dropped"] = self.num_received_dropped
        d["num_transmitted_dropped"] = self.num_transmitted_dropped
        d["num_received_frame_errors"] = self.num_received_frame_errors
        d["num_received_overrun_errors"] = self.num_received_overrun_errors
        d["num_received_crc_errors"] = self.num_received_crc_errors
        d["num_collisions"] = self.num_collisions
        d["duration_nanoseconds"] = self.duration_nanoseconds
        d["duration_seconds"] = self.duration_seconds
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"timestamp: {self.timestamp}, datapath_id: {self.datapath_id}, " \
               f"port: {self.port}, num_received_packets: {self.num_received_packets}, " \
               f"num_received_bytes: {self.num_received_bytes}," \
               f" num_received_errors: {self.num_received_errors}, " \
               f"num_transmitted_packets: {self.num_transmitted_packets}, " \
               f"num_transmitted_bytes: {self.num_transmitted_bytes}," \
               f" num_transmitted_errors: {self.num_transmitted_errors}, " \
               f"num_received_dropped: {self.num_received_dropped}, " \
               f"num_transmitted_dropped: {self.num_transmitted_dropped}, " \
               f"num_received_frame_errors: {self.num_received_frame_errors}, " \
               f"num_received_overrun_errors: {self.num_received_overrun_errors}, " \
               f"num_received_crc_errors: {self.num_received_crc_errors}, " \
               f"num_collisions: {self.num_collisions}, duration_nanoseconds: {self.duration_nanoseconds}, " \
               f"duration_seconds: {self.duration_seconds}"

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

    def copy(self) -> "PortStatistic":
        """
        :return: a copy of the DTO
        """
        return PortStatistic.from_dict(self.to_dict())

    @staticmethod
    def from_kafka_record(record: str) -> "PortStatistic":
        """
        Converts a kafka record to a DTO

        :param record: the kafka record
        :return: the DTO
        """
        parts = record.split(",")
        obj = PortStatistic(timestamp=float(parts[0]), datapath_id=int(parts[1]), port=int(parts[2]),
                            num_received_packets=int(parts[3]),
                            num_received_bytes=int(parts[4]), num_received_errors=int(parts[5]),
                            num_transmitted_packets=int(parts[6]), num_transmitted_bytes=int(parts[7]),
                            num_transmitted_errors=int(parts[8]), num_received_dropped=int(parts[9]),
                            num_transmitted_dropped=int(parts[10]), num_received_frame_errors=int(parts[11]),
                            num_received_overrun_errors=int(parts[12]), num_received_crc_errors=int(parts[13]),
                            num_collisions=int(parts[14]), duration_nanoseconds=int(parts[15]),
                            duration_seconds=int(parts[16]))
        return obj

    def to_kafka_record(self) -> str:
        """
        Converts the DTO into a kafka record

        :return: the kafka record
        """
        return f"{self.timestamp},{self.datapath_id},{self.port},{self.num_received_packets}," \
               f"{self.num_received_bytes}," \
               f"{self.num_received_errors},{self.num_transmitted_packets},{self.num_transmitted_bytes}," \
               f"{self.num_transmitted_errors},{self.num_received_dropped},{self.num_transmitted_dropped}," \
               f"{self.num_received_frame_errors},{self.num_received_overrun_errors}," \
               f"{self.num_received_crc_errors}," \
               f"{self.num_collisions},{self.duration_nanoseconds},{self.duration_seconds}"

    def update_with_kafka_record(self, record: str) -> None:
        """
        Updates the DTO with a new kafka record

        :param record: the kafka record
        :return: None
        """
        parts = record.split(",")
        self.timestamp = float(parts[0])
        self.datapath_id = int(parts[1])
        self.port = int(parts[2])
        self.num_received_packets = int(parts[3])
        self.num_received_bytes = int(parts[4])
        self.num_received_errors = int(parts[5])
        self.num_transmitted_packets = int(parts[6])
        self.num_transmitted_bytes = int(parts[7])
        self.num_transmitted_errors = int(parts[8])
        self.num_received_dropped = int(parts[9])
        self.num_transmitted_dropped = int(parts[10])
        self.num_received_frame_errors = int(parts[11])
        self.num_received_overrun_errors = int(parts[12])
        self.num_received_crc_errors = int(parts[13])
        self.num_collisions = int(parts[14])
        self.duration_nanoseconds = int(parts[15])
        self.duration_seconds = int(parts[16])
