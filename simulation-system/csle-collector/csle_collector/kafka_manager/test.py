import confluent_kafka.admin
import socket

if __name__ == '__main__':
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

    # num_partitions = 1
    # num_replicas=1
    # new_topic  = confluent_kafka.admin.NewTopic('topic_test2', num_partitions, num_replicas)
    # client.create_topics([new_topic,])