import os
import argparse
import csle_common.constants.constants as constants
from csle_common.util.experiments_util import util
from csle_common.dao.container_config.log_sink_config import LogSinkConfig
from csle_common.dao.container_config.container_network import ContainerNetwork
from csle_common.envs_model.config.generator.env_config_generator import EnvConfigGenerator
from csle_common.dao.container_config.node_container_config import NodeContainerConfig


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
            (f"{constants.CSLE.CSLE_NETWORK_PREFIX}{constants.LOG_SINK.NETWORK_ID_FIRST_OCTET}."
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

    config = LogSinkConfig(
        container=container,
        name=name, version=version, port=9092,
    )
    return config


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--install", help="Boolean parameter, if true, install config",
                        action="store_true")
    parser.add_argument("-u", "--uninstall", help="Boolean parameter, if true, uninstall config",
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
