from typing import List, Dict, Any
import csle_collector.kafka_manager.kafka_manager_pb2_grpc
import csle_collector.kafka_manager.kafka_manager_pb2
import csle_collector.kafka_manager.kafka_manager_util as kafka_manager_util


class KafkaManagersInfo:
    """
    DTO containing the status of the Kafka managers for a given emulation execution
    """

    def __init__(self, ips: List[str], ports: List[int],
                 emulation_name: str, execution_id: int,
                 kafka_managers_statuses: List[csle_collector.kafka_manager.kafka_manager_pb2.KafkaDTO],
                 kafka_managers_running: List[bool]):
        """
        Initializes the DTO

        :param ips: the list of IPs of the running Kafka managers
        :param ports: the list of ports of the running Kafka managers
        :param emulation_name: the name of the corresponding emulation
        :param execution_id: the ID of the corresponding emulation execution
        :param kafka_managers_statuses: a list of statuses of the Kafka managers
        :param kafka_managers_running: a list of booleans indicating whether the Kafka managers are running or not
        """
        self.kafka_managers_running = kafka_managers_running
        self.ips = ips
        self.ports = ports
        self.emulation_name = emulation_name
        self.execution_id = execution_id
        self.kafka_managers_statuses = kafka_managers_statuses

    def __str__(self):
        """
        :return: a string representation of the DTO
        """
        return f"kafka_managers_running: {self.kafka_managers_running}, " \
               f"ips: {list(map(lambda x: str(x), self.ips))}, " \
               f"emulation_name: {self.emulation_name}, " \
               f"execution_id: {self.execution_id}, " \
               f"kafka_managers_statuses: {list(map(lambda x: str(x), self.kafka_managers_statuses))}, " \
               f"ports: {list(map(lambda x: str(x), self.ports))}"

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["kafka_managers_running"] = self.kafka_managers_running
        d["ips"] = self.ips
        d["ports"] = self.ports
        d["emulation_name"] = self.emulation_name
        d["execution_id"] = self.execution_id
        d["kafka_managers_statuses"] = list(map(
            lambda x: kafka_manager_util.KafkaManagerUtil.kafka_dto_to_dict(x),
            self.kafka_managers_statuses))
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "KafkaManagersInfo":
        """
        Convert a dict representation to a DTO representation

        :return: a dto representation of the object
        """
        dto = KafkaManagersInfo(
            kafka_managers_running=d["kafka_managers_running"], ips=d["ips"], ports=d["ports"],
            emulation_name=d["emulation_name"], execution_id=d["execution_id"],
            kafka_managers_statuses=list(map(
                lambda x: kafka_manager_util.KafkaManagerUtil.kafka_dto_from_dict(x), d["kafka_managers_statuses"])))
        return dto
