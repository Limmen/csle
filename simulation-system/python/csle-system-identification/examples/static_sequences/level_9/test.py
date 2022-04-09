from csle_collector.docker_stats_manager.docker_stats_manager import DockerStatsThread
from csle_common.metastore.metastore_facade import MetastoreFacade
import csle_collector.docker_stats_manager.docker_stats_manager_pb2_grpc
import csle_collector.docker_stats_manager.docker_stats_manager_pb2
import csle_collector.docker_stats_manager.query_docker_stats_manager

if __name__ == '__main__':
    emulation_env_config = MetastoreFacade.get_emulation("csle-level9-001")

    container_ip_dtos = []
    for c in emulation_env_config.containers_config.containers:
        name = c.get_full_name()
        ip = c.get_ips()[0]
        container_ip_dtos.append(csle_collector.docker_stats_manager.docker_stats_manager_pb2.ContainerIp(
            ip=ip, container=name))

    docker_stats_monitor_thread = DockerStatsThread(
        container_ip_dtos, emulation_env_config.name, emulation_env_config.log_sink_config.container.get_ips()[0],
        1000, emulation_env_config.log_sink_config.time_step_len_seconds,
        emulation_env_config.log_sink_config.kafka_port)
    docker_stats_monitor_thread.start()
    docker_stats_monitor_thread.join()