from typing import List
import time
import datetime
from confluent_kafka import Consumer, KafkaError, KafkaException, TopicPartition
import csle_collector.constants.constants as collector_constants
from csle_collector.ids_manager.alert_counters import AlertCounters
from csle_collector.client_manager.client_population_metrics import ClientPopulationMetrics
from csle_collector.docker_stats_manager.docker_stats import DockerStats
from csle_collector.host_manager.host_metrics import HostMetrics
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_config.emulation_metrics_time_series import EmulationMetricsTimeSeries
from csle_common.logging.log import Logger


class ReadEmulationStatistics:


    @staticmethod
    def read_all(emulation_env_config: EmulationEnvConfig, time_window_minutes : int = 100) -> EmulationMetricsTimeSeries:
        """
        Reads all time series data from the kafka log

        :param emulation_env_config: the configuration of the emulation environment
        :param time_window_minutes : the length of the time window in minutes to consume (now-time_windows_minutes, now)
        :return: the collected time series data
        """
        client_metrics = []
        agg_docker_stats = []
        docker_host_stats = {}
        host_metrics = {}
        aggregated_host_metrics = []
        defender_actions = []
        attacker_actions = []
        ids_metrics = []
        total_host_metrics = []

        for c in emulation_env_config.containers_config.containers:
            docker_host_stats[c.get_full_name()] = []
            host_metrics[c.get_full_name()] = []

        topic_names = [collector_constants.LOG_SINK.ATTACKER_ACTIONS_TOPIC_NAME,
                       collector_constants.LOG_SINK.DOCKER_HOST_STATS_TOPIC_NAME,
                       collector_constants.LOG_SINK.DEFENDER_ACTIONS_TOPIC_NAME,
                       collector_constants.LOG_SINK.DOCKER_STATS_TOPIC_NAME,
                       collector_constants.LOG_SINK.IDS_LOG_TOPIC_NAME,
                       collector_constants.LOG_SINK.HOST_METRICS_TOPIC_NAME,
                       collector_constants.LOG_SINK.CLIENT_POPULATION_TOPIC_NAME
                       ]

        start_consume_ts = time.time()
        kafka_conf = {
            collector_constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY:
                f"{emulation_env_config.log_sink_config.container.get_ips()[0]}:"
                                           f"{emulation_env_config.log_sink_config.kafka_port}",
            collector_constants.KAFKA.GROUP_ID_PROPERTY:  f"attacker_actions_consumer_thread_{start_consume_ts}",
            collector_constants.KAFKA.AUTO_OFFSET_RESET_PROPERTY: collector_constants.KAFKA.EARLIEST_OFFSET}
        consumer = Consumer(**kafka_conf)
        print(f"consume: {datetime.datetime.now() - datetime.timedelta(minutes=time_window_minutes)}")
        start_consume_ts = int(datetime.datetime.timestamp(datetime.datetime.now()
                                                           - datetime.timedelta(minutes=time_window_minutes)))
        start_consume_ts=int(start_consume_ts*1e3) # convert to ms
        topic_partitions = list(map(lambda x: TopicPartition(topic=x, partition=0, offset=start_consume_ts), topic_names))
        time_offsets_partitions = consumer.offsets_for_times(partitions=topic_partitions, timeout=20)

        def on_assign(consumer, partitions):
            """
            Callback called when a Kafka consumer is assigned to a partition
            """
            consumer.assign(time_offsets_partitions)

        consumer.subscribe(topic_names, on_assign=on_assign)
        done = False
        num_msg = 0
        host_metrics_counter = 0
        while not done:
            msg = consumer.poll(timeout=1.0)
            if msg is not None:
                num_msg+= 1
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        Logger.__call__().get_logger.warning(
                            f"reached end of partition: {msg.topic(), msg.partition(), msg.offset()}")
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    topic = msg.topic()
                    if topic == collector_constants.LOG_SINK.DOCKER_STATS_TOPIC_NAME:
                        agg_docker_stats.append(DockerStats.from_kafka_record(record=msg.value().decode()))
                    elif topic == collector_constants.LOG_SINK.HOST_METRICS_TOPIC_NAME:
                        metrics = HostMetrics.from_kafka_record(record=msg.value().decode())
                        c = emulation_env_config.containers_config.get_container_from_ip(metrics.ip)
                        host_metrics[c.get_full_name()].append(metrics)
                        host_metrics_counter += 1
                        total_host_metrics.append(metrics)
                    elif topic == collector_constants.LOG_SINK.ATTACKER_ACTIONS_TOPIC_NAME:
                        attacker_actions.append(EmulationAttackerAction.from_kafka_record(record=msg.value().decode()))
                    elif topic == collector_constants.LOG_SINK.DEFENDER_ACTIONS_TOPIC_NAME:
                        defender_actions.append(EmulationDefenderAction.from_kafka_record(record=msg.value().decode()))
                    elif topic == collector_constants.LOG_SINK.DOCKER_HOST_STATS_TOPIC_NAME:
                        stats = DockerStats.from_kafka_record(record=msg.value().decode())
                        c = emulation_env_config.containers_config.get_container_from_ip(stats.ip)
                        docker_host_stats[c.get_full_name()].append(stats)
                    elif topic == collector_constants.LOG_SINK.IDS_LOG_TOPIC_NAME:
                        ids_metrics.append(AlertCounters.from_kafka_record(record=msg.value().decode()))
                    elif topic == collector_constants.LOG_SINK.CLIENT_POPULATION_TOPIC_NAME:
                        client_metrics.append(ClientPopulationMetrics.from_kafka_record(record=msg.value().decode()))
                    if host_metrics_counter >= len(emulation_env_config.containers_config.containers):
                        agg_host_metrics_dto = ReadEmulationStatistics.average_host_metrics(
                            host_metrics=total_host_metrics)
                        aggregated_host_metrics.append(agg_host_metrics_dto)
                        host_metrics_counter = 0
                        total_host_metrics = []
            else:
                done=True
        consumer.close()
        dto = EmulationMetricsTimeSeries(
            client_metrics=client_metrics, aggregated_docker_stats=agg_docker_stats, host_metrics=host_metrics,
            docker_host_stats=docker_host_stats, ids_metrics=ids_metrics, attacker_actions=attacker_actions,
            defender_actions=defender_actions, aggregated_host_metrics=aggregated_host_metrics,
            emulation_env_config=emulation_env_config)
        return dto


    @staticmethod
    def average_host_metrics(host_metrics: List[HostMetrics]) -> HostMetrics:
        total_num_logged_in_users = 0
        total_num_failed_login_attempts = 0
        total_num_open_connections = 0
        total_num_login_events = 0
        total_num_processes = 0
        total_num_users = 0
        for metric in host_metrics:
            total_num_logged_in_users += metric.num_logged_in_users
            total_num_failed_login_attempts += metric.num_failed_login_attempts
            total_num_open_connections += metric.num_open_connections
            total_num_login_events += metric.num_login_events
            total_num_processes += metric.num_processes
            total_num_users += metric.num_users
        aggregated_host_metrics_dto = HostMetrics()
        aggregated_host_metrics_dto.num_logged_in_users = total_num_logged_in_users
        aggregated_host_metrics_dto.num_failed_login_attempts = total_num_failed_login_attempts
        aggregated_host_metrics_dto.num_open_connections = total_num_open_connections
        aggregated_host_metrics_dto.num_login_events = total_num_login_events
        aggregated_host_metrics_dto.num_processes = total_num_processes
        aggregated_host_metrics_dto.num_users = total_num_users
        return aggregated_host_metrics_dto
