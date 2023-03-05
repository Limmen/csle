import csle_collector.constants.constants as constants
import csle_collector.docker_stats_manager.docker_stats_manager
from csle_collector.docker_stats_manager.docker_stats import DockerStats
from csle_collector.docker_stats_manager.docker_stats_util import DockerStatsUtil
import socket
from collections import deque
from confluent_kafka import Producer
import time
import docker

def compute_averages(stats_queues):
    """
    Compute averages and aggregates of the list of metrics
    :return: the average and aggregate metrics
    """
    avg_stats = {}
    avg_stats_l = []
    for k, v in stats_queues.items():
        avg_stat = DockerStats.compute_averages(list(v))
        avg_stats[k] = avg_stat
        avg_stats_l.append(avg_stat)
    aggregated_stats = DockerStats.compute_averages(avg_stats_l)
    aggregated_stats.pids = float("{:.1f}".format(aggregated_stats.pids * len(avg_stats_l)))
    aggregated_stats.mem_current = float("{:.1f}".format(aggregated_stats.mem_current * len(avg_stats_l)))
    aggregated_stats.mem_total = float("{:.1f}".format(aggregated_stats.mem_total * len(avg_stats_l)))
    aggregated_stats.blk_read = float("{:.1f}".format(aggregated_stats.blk_read * len(avg_stats_l)))
    aggregated_stats.blk_write = float("{:.1f}".format(aggregated_stats.blk_write * len(avg_stats_l)))
    aggregated_stats.net_rx = float("{:.1f}".format(aggregated_stats.net_rx * len(avg_stats_l)))
    aggregated_stats.net_tx = float("{:.1f}".format(aggregated_stats.net_tx * len(avg_stats_l)))
    return aggregated_stats, avg_stats

if __name__ == '__main__':
    container_names_and_ips = [("15.4.1.254", "csle_client_1_1-level4-15")]
    container_names = ["csle_client_1_1-level4-15"]
    client_1 = docker.from_env()
    client_2 = docker.APIClient(base_url=constants.DOCKER_STATS.UNIX_DOCKER_SOCK_URL)
    containers = client_1.containers.list()
    containers = list(filter(lambda x: x.name in container_names, containers))
    print(f"containers len: {len(containers)}")
    stats_queues = {}
    streams = []
    for container in containers:
        stream = container.stats(decode=True, stream=True)
        streams.append((stream, container))
    stats_queue_maxsize = 10000
    emulation = "emulation:csle-level4-010"
    execution_first_ip_octet = 15
    kafka_ip="172.18.0.10"
    # kafka_port=9292
    # kafka_port=5000
    kafka_port=9292
    time_step_len_seconds=15
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    conf = {constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{kafka_ip}:{kafka_port}",
            constants.KAFKA.CLIENT_ID_PROPERTY: hostname}
    producer = Producer(**conf)
    time.sleep(10)
    for stream, container in streams:
        stats_dict = next(stream)
        parsed_stats = DockerStatsUtil.parse_stats(stats_dict, container.name)
        if parsed_stats.container_name not in stats_queues:
            stats_queues[parsed_stats.container_name] = deque([], maxlen=stats_queue_maxsize)
        stats_queues[parsed_stats.container_name].append(parsed_stats)
    print(f"stats queues:{stats_queues}")
    time.sleep(10)
    aggregated_stats, avg_stats_dict = compute_averages(stats_queues)
    record = aggregated_stats.to_kafka_record(ip=ip)
    print(f"PRODUCING to {constants.KAFKA_CONFIG.DOCKER_STATS_TOPIC_NAME}")
    producer.produce(constants.KAFKA_CONFIG.DOCKER_STATS_TOPIC_NAME, record)
    producer.poll(0)
    time.sleep(10)
    print("PRODUCED")
