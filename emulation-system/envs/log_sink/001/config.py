import os
import argparse
import csle_common.constants.constants as constants
from csle_common.util.experiments_util import util
from csle_common.dao.container_config.log_sink_config import LogSinkConfig
from csle_common.dao.container_config.container_network import ContainerNetwork
from csle_common.envs_model.config.generator.env_config_generator import EnvConfigGenerator
from csle_common.dao.container_config.node_container_config import NodeContainerConfig
from csle_common.dao.container_config.node_resources_config import NodeResourcesConfig
from csle_common.dao.container_config.kafka_topic import KafkaTopic


def default_config(name: str, version: str = "0.0.1") -> LogSinkConfig:
    """
    The default configuration of the log sink

    :param name: the name of the log sink
    :param version: the version
    :return: The configuration
    """
    container = NodeContainerConfig(
        name=f"{constants.CONTAINER_IMAGES.KAFKA_1}",
        ips_and_networks=[
            (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{constants.LOG_SINK.NETWORK_ID_FIRST_OCTET}."
             f"{constants.LOG_SINK.NETWORK_ID_SECOND_OCTET}.{constants.LOG_SINK.NETWORK_ID_THIRD_OCTET}",
             ContainerNetwork(
                 name=f"{constants.CSLE.CSLE_NETWORK_PREFIX}{constants.LOG_SINK.NETWORK_ID_FIRST_OCTET}_1",
                 subnet_mask=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}"
                             f"{constants.LOG_SINK.NETWORK_ID_FIRST_OCTET}.{constants.LOG_SINK.NETWORK_ID_SECOND_OCTET}"
                             f"{constants.CSLE.CSLE_EDGE_SUBNETMASK_SUFFIX}",
                 subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{constants.LOG_SINK.NETWORK_ID_FIRST_OCTET}"
             )),
        ],
        minigame=constants.CSLE.CTF_MINIGAME,
        version=version, level=constants.LOG_SINK.LEVEL,
        restart_policy=constants.DOCKER.ON_FAILURE_3, suffix=constants.LOG_SINK.SUFFIX)

    resources = NodeResourcesConfig(
        container_name=f"{constants.CSLE.NAME}-{constants.LOG_SINK.MINIGAME}-"
                       f"{constants.CONTAINER_IMAGES.KAFKA_1}_1-{constants.CSLE.LEVEL}{constants.LOG_SINK.LEVEL}",
        num_cpus=1, available_memory_gb=4,
        ips_and_network_configs=[
            (f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}{constants.LOG_SINK.NETWORK_ID_FIRST_OCTET}."
             f"{constants.LOG_SINK.NETWORK_ID_SECOND_OCTET}.{constants.LOG_SINK.NETWORK_ID_THIRD_OCTET}",
             None)])

    topics = [
        KafkaTopic(
            name=constants.LOG_SINK.CLIENT_POPULATION_TOPIC_NAME,
            num_replicas=1,
            num_partitions=1,
            attributes=constants.LOG_SINK.CLIENT_POPULATION_TOPIC_ATTRIBUTES
        ),
        KafkaTopic(
            name=constants.LOG_SINK.IDS_LOG_TOPIC_NAME,
            num_replicas=1,
            num_partitions=1,
            attributes= constants.LOG_SINK.IDS_LOG_TOPIC_ATTRIBUTES
        ),
        KafkaTopic(
            name=constants.LOG_SINK.LOGIN_ATTEMPTS_TOPIC_NAME,
            num_replicas=1,
            num_partitions=1,
            attributes=constants.LOG_SINK.LOGIN_ATTEMPTS_TOPIC_ATTRIBUTES
        ),
        KafkaTopic(
            name=constants.LOG_SINK.TCP_CONNECTIONS_TOPIC_NAME,
            num_replicas=1,
            num_partitions=1,
            attributes=constants.LOG_SINK.TCP_CONNECTIONS_TOPIC_ATTRIBUTES
        ),
        KafkaTopic(
            name=constants.LOG_SINK.PROCESSES_TOPIC_NAME,
            num_replicas=1,
            num_partitions=1,
            attributes=constants.LOG_SINK.PROCESSES_TOPIC_ATTRIBUTES
        ),
        KafkaTopic(
            name=constants.LOG_SINK.DOCKER_STATS_TOPIC_NAME,
            num_replicas=1,
            num_partitions=1,
            attributes=constants.LOG_SINK.DOCKER_STATS_TOPIC_ATTRIBUTES
        )
    ]

    config = LogSinkConfig(container=container, resources=resources, topics=topics,
                           name=name, version=version, kafka_port=9092, kafka_manager_port=50051)
    return config


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--install", help="Boolean parameter, if true, install config",
                        action="store_true")
    parser.add_argument("-u", "--uninstall", help="Boolean parameter, if true, uninstall config",
                        action="store_true")
    parser.add_argument("-r", "--run", help="Boolean parameter, if true, run containers",
                        action="store_true")
    parser.add_argument("-s", "--stop", help="Boolean parameter, if true, stop containers",
                        action="store_true")
    parser.add_argument("-c", "--clean", help="Boolean parameter, if true, remove containers",
                        action="store_true")
    parser.add_argument("-a", "--apply", help="Boolean parameter, if true, apply config",
                        action="store_true")

    args = parser.parse_args()
    if not os.path.exists(util.default_log_sink_config_path()):
        config = default_config(name="csle-logsink-001", version="0.0.1")
        util.write_log_sink_config_file(config, util.default_log_sink_config_path())
    config = util.read_log_sink_config(util.default_log_sink_config_path())
    if args.install:
        EnvConfigGenerator.install_logsink(config=config)
    if args.uninstall:
        EnvConfigGenerator.uninstall_logsink(config=config)
    if args.run:
        EnvConfigGenerator.run_log_sink(log_sink_config=config)
    if args.stop:
        EnvConfigGenerator.stop_log_sink(log_sink_config=config)
    if args.clean:
        EnvConfigGenerator.stop_log_sink(log_sink_config=config)
        EnvConfigGenerator.rm_log_sink(log_sink_config=config)
        EnvConfigGenerator.delete_networks_of_log_sink(log_sink_config=config)
    if args.apply:
        EnvConfigGenerator.apply_log_sink_config(log_sink_config=config)
