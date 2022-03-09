import socket
import sys
import time

import confluent_kafka.admin
from confluent_kafka import Producer


def test():
    conf = {'bootstrap.servers': "55.254.1.72:9092",
            'client.id': socket.gethostname()}
    print(socket.gethostname())
    print(socket.gethostbyname(socket.gethostname()))
    client = confluent_kafka.admin.AdminClient(conf)
    cluster_metadata = client.list_topics()
    print(cluster_metadata.cluster_id)
    print(cluster_metadata.controller_id)
    print(cluster_metadata.brokers)
    print(cluster_metadata.topics)
    topics = []
    for k,v in cluster_metadata.topics.items():
        topics.append(k)
    print(topics)

    num_partitions = 1
    num_replicas=1
    print("Creating topic?")
    new_topic  = confluent_kafka.admin.NewTopic('topic_test2', num_partitions, num_replicas)
    time.sleep(5)
    topics_created = client.create_topics([new_topic])
    time.sleep(5)
    print(topics_created)


def test_create_topics():
    conf = {'bootstrap.servers': "55.254.1.72:9092",
            'client.id': socket.gethostname()}
    client = confluent_kafka.admin.AdminClient(conf)
    num_partitions = 1
    num_replicas=1
    t_1  = confluent_kafka.admin.NewTopic('client_population', num_partitions, num_replicas)
    t_2  = confluent_kafka.admin.NewTopic('ids_log', num_partitions, num_replicas)
    t_3  = confluent_kafka.admin.NewTopic('login_attempts', num_partitions, num_replicas)
    t_4  = confluent_kafka.admin.NewTopic('tcp_connections', num_partitions, num_replicas)
    t_5  = confluent_kafka.admin.NewTopic('processes', num_partitions, num_replicas)
    t_6  = confluent_kafka.admin.NewTopic('docker_stats', num_partitions, num_replicas)
    client.create_topics([t_1, t_2, t_3, t_4, t_5, t_6,])
    time.sleep(5)


def test_read_topics():
    conf = {'bootstrap.servers': "55.254.1.72:9092",
            'client.id': socket.gethostname()}
    client = confluent_kafka.admin.AdminClient(conf)
    cluster_metadata = client.list_topics()
    topics = []
    for k,v in cluster_metadata.topics.items():
        topics.append(k)
    print(topics)

# Optional per-message delivery callback (triggered by poll() or flush())
# when a message has been successfully delivered or permanently
# failed delivery (after retries).
def delivery_callback(err, msg):
    if err:
        sys.stderr.write('%% Message failed delivery: %s\n' % err)
    else:
        sys.stderr.write('%% Message delivered to %s [%d] @ %d\n' %
                         (msg.topic(), msg.partition(), msg.offset()))


def test_produce_to_topic():
    conf = {'bootstrap.servers': "55.254.1.72:9092",
            'client.id': socket.gethostname()}
    p = Producer(**conf)
    p.produce("client_population", "timestamp,emulation_name,ip,5", callback=delivery_callback)
    p.produce("ids_log", "timestamp,emulation_name,ip,high,medium,low,very_low,attempted-admin,attempted-user,inappropriate-content,"
                         "policy-violation,shellcode-detect,successful-admin,successful-user,trojan-activity,"
                         "unsuccessful-user,web-application-attack,attempted-dos,attempted-recon,bad-unknown,"
                         "default-login-attempt,denial-of-service,misc-attack,non-standard-protocol,"
                         "rpc-portmap-decode,successful-dos,successful-recon-largescale,"
                         "successful-recon-limited,suspicious-filename-detect,suspicious-login,"
                         "system-call-detect,unusual-client-port-connection,web-application-activity,"
                         "icmp-event,misc-activity,network-scan,not-suspicious,protocol-command-decode,"
                         "string-detect,unknown,tcp-connection", callback=delivery_callback)
    p.produce("login_attempts", "timestamp,emulation_name,ip,num_login_attempts", callback=delivery_callback)
    p.produce("tcp_connections", "timestamp,emulation_name,ip,num_tcp_connections", callback=delivery_callback)
    p.produce("processes", "timestamp,emulation_name,ip,num_processes", callback=delivery_callback)
    p.produce("docker_stats", "timestamp,emulation_name,ip,cpu_percentage_change,new_mem_current,new_mem_total,"
                              "new_mem_percent,new_blk_read,new_blk_write,new_net_rx,new_net_tx", callback=delivery_callback)
    time.sleep(5)
    p.poll(0)


if __name__ == '__main__':
    # test()
    # test_create_topics()
    # test_read_topics()
    test_produce_to_topic()