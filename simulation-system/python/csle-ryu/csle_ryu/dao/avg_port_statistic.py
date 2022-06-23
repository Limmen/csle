from typing import Dict, Any, List
from csle_ryu.dao.port_statistic import PortStatistic


class AvgPortStatistic:
    """
    DTO containing data with average port statistics from an OpenFlow switch
    """

    def __init__(self, timestamp: float, datapath_id: int, avg_num_received_packets: int,
                 avg_num_received_bytes: int, avg_num_received_errors: int, avg_num_transmitted_packets: int,
                 avg_num_transmitted_bytes: int, avg_num_transmitted_errors: int, avg_num_received_dropped: int,
                 avg_num_transmitted_dropped, avg_num_received_frame_errors, avg_num_received_overrun_errors,
                 avg_num_received_crc_errors, avg_num_collisions, avg_duration_nanoseconds, avg_duration_seconds):
        """
        Initializes the DTO

        :param timestamp: the timestamp the statistic was received
        :param datapath_id: the datapath id
        :param avg_num_received_packets: the avg number of received packets on the port
        :param avg_num_received_bytes: the avg number of received bytes on the port
        :param avg_num_received_errors: the avg number of received errors on the port
        :param avg_num_transmitted_packets: the avg number of transmitted packets on the port
        :param avg_num_transmitted_bytes: the avg number of transmitted bytes on the port
        :param avg_num_transmitted_errors: the avg number of transmitted errors on the port
        :param avg_num_received_dropped: the avg number of received packets dropped on the port
        :param avg_num_transmitted_dropped: the avg number of transmitted packets dropped on the port
        :param avg_num_received_frame_errors: the avg number of received frame errors on the port
        :param avg_num_received_overrun_errors: the avg number of overrun errors on the port
        :param avg_num_received_crc_errors: the avg number of received crc errors on the port
        :param avg_num_collisions: the avg number of collisions on the port
        :param avg_duration_nanoseconds: the avg duration the port has been up in nanoseconds
        :param avg_duration_seconds: the avg duration the port has been up in seconds
        """
        self.timestamp = timestamp
        self.datapath_id = datapath_id
        self.avg_num_received_packets = avg_num_received_packets
        self.avg_num_received_bytes = avg_num_received_bytes
        self.avg_num_received_errors = avg_num_received_errors
        self.avg_num_transmitted_packets = avg_num_transmitted_packets
        self.avg_num_transmitted_bytes = avg_num_transmitted_bytes
        self.avg_num_transmitted_errors = avg_num_transmitted_errors
        self.avg_num_received_dropped = avg_num_received_dropped
        self.avg_num_transmitted_dropped = avg_num_transmitted_dropped
        self.avg_num_received_frame_errors = avg_num_received_frame_errors
        self.avg_num_received_overrun_errors = avg_num_received_overrun_errors
        self.avg_num_received_crc_errors = avg_num_received_crc_errors
        self.avg_num_collisions = avg_num_collisions
        self.avg_duration_nanoseconds = avg_duration_nanoseconds
        self.avg_duration_seconds = avg_duration_seconds

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AvgPortStatistic":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = AvgPortStatistic(
            timestamp=d["timestamp"], datapath_id=d["datapath_id"],
            avg_num_received_packets=d["avg_num_received_packets"],
            avg_num_received_bytes=d["avg_num_received_bytes"],
            avg_num_received_errors=d["avg_num_received_errors"],
            avg_num_transmitted_packets=d["avg_num_transmitted_packets"],
            avg_num_transmitted_bytes=d["avg_num_transmitted_bytes"],
            avg_num_transmitted_errors=d["avg_num_transmitted_errors"],
            avg_num_received_dropped=d["avg_num_received_dropped"],
            avg_num_transmitted_dropped=d["avg_num_transmitted_dropped"],
            avg_num_received_frame_errors=d["avg_num_received_frame_errors"],
            avg_num_received_overrun_errors=d["avg_num_received_overrun_errors"],
            avg_num_received_crc_errors=d["avg_num_received_crc_errors"],
            avg_num_collisions=d["avg_num_collisions"], avg_duration_nanoseconds=d["avg_duration_nanoseconds"],
            avg_duration_seconds=d["avg_duration_seconds"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["timestamp"] = self.timestamp
        d["datapath_id"] = self.datapath_id
        d["avg_num_received_packets"] = self.avg_num_received_packets
        d["avg_num_received_bytes"] = self.avg_num_received_bytes
        d["avg_num_received_errors"] = self.avg_num_received_errors
        d["avg_num_transmitted_packets"] = self.avg_num_transmitted_packets
        d["avg_num_transmitted_bytes"] = self.avg_num_transmitted_bytes
        d["avg_num_transmitted_errors"] = self.avg_num_transmitted_errors
        d["avg_num_received_dropped"] = self.avg_num_received_dropped
        d["avg_num_transmitted_dropped"] = self.avg_num_transmitted_dropped
        d["avg_num_received_frame_errors"] = self.avg_num_received_frame_errors
        d["avg_num_received_overrun_errors"] = self.avg_num_received_overrun_errors
        d["avg_num_received_crc_errors"] = self.avg_num_received_crc_errors
        d["avg_num_collisions"] = self.avg_num_collisions
        d["avg_duration_nanoseconds"] = self.avg_duration_nanoseconds
        d["avg_duration_seconds"] = self.avg_duration_seconds
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"timestamp: {self.timestamp}, datapath_id: {self.datapath_id}, " \
               f"avg_num_received_packets: {self.avg_num_received_packets}, " \
               f"avg_num_received_bytes: {self.avg_num_received_bytes}," \
               f" avg_num_received_errors: {self.avg_num_received_errors}, " \
               f"avg_num_transmitted_packets: {self.avg_num_transmitted_packets}, " \
               f"avg_num_transmitted_bytes: {self.avg_num_transmitted_bytes}," \
               f" avg_num_transmitted_errors: {self.avg_num_transmitted_errors}, " \
               f"avg_num_received_dropped: {self.avg_num_received_dropped}, " \
               f"avg_num_transmitted_dropped: {self.avg_num_transmitted_dropped}, " \
               f"avg_num_received_frame_errors: {self.avg_num_received_frame_errors}, " \
               f"avg_num_received_overrun_errors: {self.avg_num_received_overrun_errors}, " \
               f"avg_num_received_crc_errors: {self.avg_num_received_crc_errors}, " \
               f"avg_num_collisions: {self.avg_num_collisions}, " \
               f"avg_duration_nanoseconds: {self.avg_duration_nanoseconds}, " \
               f"avg_duration_seconds: {self.avg_duration_seconds}"

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
    def from_kafka_record(record: str) -> "AvgPortStatistic":
        """
        Converts a kafka record to a DTO

        :param record: the kafka record
        :return: the DTO
        """
        parts = record.split(",")
        obj = AvgPortStatistic(timestamp = float(parts[0]), datapath_id=int(parts[1]),
                            avg_num_received_packets=int(parts[2]),
                            avg_num_received_bytes=int(parts[3]), avg_num_received_errors=int(parts[4]),
                            avg_num_transmitted_packets=int(parts[5]), avg_num_transmitted_bytes=int(parts[6]),
                            avg_num_transmitted_errors=int(parts[7]), avg_num_received_dropped=int(parts[8]),
                            avg_num_transmitted_dropped=int(parts[9]), avg_num_received_frame_errors=int(parts[10]),
                            avg_num_received_overrun_errors=int(parts[11]), avg_num_received_crc_errors=int(parts[12]),
                            avg_num_collisions=int(parts[13]), avg_duration_nanoseconds=int(parts[14]),
                            avg_duration_seconds=int(parts[15]))
        return obj

    def to_kafka_record(self) -> str:
        """
        Converts the DTO into a kafka record

        :return: the kafka record
        """
        return f"{self.timestamp},{self.datapath_id},{self.avg_num_received_packets},{self.avg_num_received_bytes}," \
               f"{self.avg_num_received_errors},{self.avg_num_transmitted_packets},{self.avg_num_transmitted_bytes}," \
               f"{self.avg_num_transmitted_errors},{self.avg_num_received_dropped},{self.avg_num_transmitted_dropped}," \
               f"{self.avg_num_received_frame_errors},{self.avg_num_received_overrun_errors},{self.avg_num_received_crc_errors}," \
               f"{self.avg_num_collisions},{self.avg_duration_nanoseconds},{self.avg_duration_seconds}"

    def update_with_kafka_record(self, record: str) -> None:
        """
        Updates the DTO with a new kafka record

        :param record: the kafka record
        :return: None
        """
        parts = record.split(",")
        self.timestamp = float(parts[0])
        self.datapath_id=int(parts[1])
        self.avg_num_received_packets=int(parts[2])
        self.avg_num_received_bytes=int(parts[3])
        self.avg_num_received_errors=int(parts[4])
        self.avg_num_transmitted_packets=int(parts[5])
        self.avg_num_transmitted_bytes=int(parts[6])
        self.avg_num_transmitted_errors=int(parts[7])
        self.avg_num_received_dropped=int(parts[8])
        self.avg_num_transmitted_dropped=int(parts[9])
        self.avg_num_received_frame_errors=int(parts[10])
        self.avg_num_received_overrun_errors=int(parts[11])
        self.avg_num_received_crc_errors=int(parts[12])
        self.avg_num_collisions=int(parts[13])
        self.avg_duration_nanoseconds=int(parts[14])
        self.avg_duration_seconds=int(parts[15])



    @staticmethod
    def average_port_statistics(timestamp: float, datapath_id: int,
                                port_statistics: List[PortStatistic]) -> "AvgPortStatistic":
        """
        Computes the average metrics from a list of flow statistics

        :param port_statistics: the list of flow statistics to average
        :return: the computed averages
        """
        total_num_received_packets = 0
        total_num_received_bytes = 0
        total_num_received_errors = 0
        total_num_transmitted_packets = 0
        total_num_transmitted_bytes = 0
        total_num_transmitted_errors = 0
        total_num_received_dropped = 0
        total_num_transmitted_dropped = 0
        total_num_received_frame_errors = 0
        total_num_received_overrun_errors = 0
        total_num_received_crc_errors = 0
        total_num_collisions = 0
        total_num_duration_nanoseconds = 0
        total_num_duration_seconds = 0

        for port in port_statistics:
            total_num_received_packets += port.num_received_packets
            total_num_received_bytes += port.num_received_bytes
            total_num_received_errors += port.num_received_errors
            total_num_transmitted_packets += port.num_transmitted_packets
            total_num_transmitted_bytes += port.num_transmitted_bytes
            total_num_transmitted_errors += port.num_transmitted_errors
            total_num_received_dropped += port.num_received_dropped
            total_num_transmitted_dropped += port.num_transmitted_dropped
            total_num_received_frame_errors += port.num_received_frame_errors
            total_num_received_overrun_errors += port.num_received_overrun_errors
            total_num_received_crc_errors += port.num_received_crc_errors
            total_num_collisions += port.num_collisions
            total_num_duration_nanoseconds += port.duration_nanoseconds
            total_num_duration_seconds += port.duration_seconds

        num_ports = len(port_statistics)
        aggregated_flow_statistics_dto = AvgPortStatistic(
            timestamp=timestamp, datapath_id=datapath_id,
            avg_num_received_packets=int(total_num_received_packets/num_ports),
            avg_num_received_bytes=int(total_num_received_bytes/num_ports),
            avg_num_received_errors=int(total_num_received_errors/num_ports),
            avg_num_transmitted_packets=int(total_num_transmitted_packets/num_ports),
            avg_num_transmitted_bytes=int(total_num_transmitted_bytes/num_ports),
            avg_num_transmitted_errors=int(total_num_transmitted_errors/num_ports),
            avg_num_received_dropped=int(total_num_received_dropped/num_ports),
            avg_num_transmitted_dropped=int(total_num_transmitted_dropped/num_ports),
            avg_num_received_frame_errors=int(total_num_received_frame_errors/num_ports),
            avg_num_received_overrun_errors=int(total_num_received_overrun_errors/num_ports),
            avg_num_received_crc_errors=int(total_num_received_crc_errors/num_ports),
            avg_num_collisions=int(total_num_collisions/num_ports),
            avg_duration_nanoseconds=int(total_num_duration_nanoseconds/num_ports),
            avg_duration_seconds=int(total_num_duration_seconds/num_ports)
        )
        return aggregated_flow_statistics_dto