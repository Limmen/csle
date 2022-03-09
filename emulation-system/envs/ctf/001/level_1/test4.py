import grpc
import csle_collector.docker_stats_manager.query_docker_stats_manager as query_docker_stats_manager
import csle_collector.docker_stats_manager.docker_stats_manager_pb2_grpc
import csle_collector.docker_stats_manager.docker_stats_manager_pb2

if __name__ == '__main__':
    with grpc.insecure_channel('172.31.212.92:50051') as channel:
        stub = csle_collector.docker_stats_manager.docker_stats_manager_pb2_grpc.DockerStatsManagerStub(channel)
        query_docker_stats_manager.start_docker_stats_monitor(
            stub=stub,
            emulation="csle-ctf-level1-001", sink_ip="55.1.253.253", stats_queue_maxsize=1000,
            time_step_len_seconds=15, sink_port=9092, containers=[
                "csle-ctf-kafka_1_1-level1",
                "csle-ctf-telnet_1_1-level1",
                "csle-ctf-ssh_1_1-level1",
                "csle-ctf-router_1_1-level1",
                "csle-ctf-honeypot_1_1-level1",
                "csle-ctf-hacker_kali_1_1-level1",
                "csle-ctf-ftp_1_1-level1",
                "csle-ctf-client_1_1-level1"
            ])