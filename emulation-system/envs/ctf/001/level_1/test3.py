import grpc
import csle_collector.kafka_manager.query_kafka_server as query_kafka_server
import csle_collector.kafka_manager.kafka_manager_pb2_grpc

if __name__ == '__main__':
    # Open a gRPC session
    with grpc.insecure_channel(f'55.254.1.72:50051') as channel:
        stub = csle_collector.kafka_manager.kafka_manager_pb2_grpc.KafkaManagerStub(channel)
        kafka_dto = query_kafka_server.get_kafka_status(stub)
        print(kafka_dto)