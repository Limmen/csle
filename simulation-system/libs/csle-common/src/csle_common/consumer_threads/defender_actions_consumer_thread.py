from typing import List
import threading
import time
from confluent_kafka import Consumer, KafkaError, KafkaException
from csle_common.logging.log import Logger
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
import csle_collector.constants.constants as collector_constants


class DefenderActionsConsumerThread(threading.Thread):
    """
    Thread that polls the kafka to get the latest defender actions
    """

    def __init__(self, kafka_server_ip: str, kafka_port: int,
                 defender_actions: List[EmulationDefenderAction], auto_offset_reset: str = "latest") -> None:
        """
        Initializes the thread

        :param kafka_server_ip: the ip of the kafka server
        :param kafka_port: the port of the kafka server
        :param defender_actions: the defender actions to update
        :param auto_offset_reset: the offset for kafka to start reading from
        """
        threading.Thread.__init__(self)
        self.running = True
        self.kafka_server_ip = kafka_server_ip
        self.kafka_port = kafka_port
        self.ts = time.time()
        self.auto_offset_reset = auto_offset_reset
        self.kafka_conf = {
            collector_constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{self.kafka_server_ip}:{self.kafka_port}",
            collector_constants.KAFKA.GROUP_ID_PROPERTY: f"defender_actions_consumer_thread_{self.ts}",
            collector_constants.KAFKA.AUTO_OFFSET_RESET_PROPERTY: auto_offset_reset
        }
        self.consumer = Consumer(**self.kafka_conf)
        self.consumer.subscribe([collector_constants.KAFKA_CONFIG.DEFENDER_ACTIONS_TOPIC_NAME])
        self.defender_actions = defender_actions

    def run(self) -> None:
        """
        Runs the thread

        :return: None
        """
        while self.running:
            msg = self.consumer.poll(timeout=5.0)
            if msg is not None:
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        Logger.__call__().get_logger.warning(
                            f"reached end of partition: {msg.topic(), msg.partition(), msg.offset()}")
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    self.defender_actions.append(EmulationDefenderAction.from_kafka_record(
                        record=msg.value().decode()))
        self.consumer.close()
