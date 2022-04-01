import threading
import time
from confluent_kafka import Consumer, KafkaError, KafkaException
from csle_common.dao.emulation_observation.defender.emulation_defender_machine_observation_state \
    import EmulationDefenderMachineObservationState
import csle_collector.constants.constants as collector_constants
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_collector.host_manager.host_metrics import HostMetrics
from csle_common.logging.log import Logger


class HostMetricsConsumerThread(threading.Thread):
    """
    Thread that polls Kafka to get the latest metrics for a specific host
    """

    def __init__(self, host_ip: str, kafka_server_ip: str, kafka_port: int,
                 machine: EmulationDefenderMachineObservationState) -> None:
        """
        Initializes the thread

        :param host_ip: the ip of the host
        :param kafka_server_ip: the ip of the kafka server
        :param kafka_port: the port of the kafka server
        :param machine: the machine state to update
        """
        threading.Thread.__init__(self)
        self.running =True
        self.host_ip = host_ip
        self.kafka_server_ip = kafka_server_ip
        self.kafka_port = kafka_port
        self.machine = machine
        self.ts = time.time()
        self.kafka_conf = {'bootstrap.servers': f"{self.kafka_server_ip}:{self.kafka_port}",
                           'group.id':  f"host_metrics_consumer_thread_{self.host_ip}_{self.ts}",
                           'auto.offset.reset': 'latest'}
        self.consumer = Consumer(**self.kafka_conf)
        self.consumer.subscribe([collector_constants.LOG_SINK.HOST_METRICS_TOPIC_NAME])

    def run(self) -> None:
        """
        Runs the thread

        :return: None
        """
        while True:
            msg = self.consumer.poll(timeout=5.0)
            if msg is not None:
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        Logger.__call__().get_logger.warning(
                            f"reached end of partition: {msg.topic(), msg.partition(), msg.offset()}")
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    self.machine.host_metrics = HostMetrics.from_kafka_record(
                        record=msg.value().decode())
                    print(self.machine.host_metrics)


if __name__ == '__main__':
    emulation_env_config = MetastoreFacade.get_emulation("csle-level9-001")
    # s = EmulationEnvState(emulation_env_config=emulation_env_config)
    # thread = HostMetricsConsumerThread(
    #     kafka_server_ip=emulation_env_config.log_sink_config.container.get_ips()[0],
    #     kafka_port=emulation_env_config.log_sink_config.kafka_port, s=s)
    # thread.start()
    # thread.join()