from typing import List, Tuple
import time
import subprocess
import random
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.log_sink_config import LogSinkConfig
from csle_common.dao.emulation_config.node_resources_config import NodeResourcesConfig
from csle_common.controllers.container_manager import ContainerManager
from csle_common.controllers.ids_manager import IDSManager
from csle_common.controllers.host_manager import HostManager
from csle_common.controllers.log_sink_manager import LogSinkManager
from csle_common.controllers.users_manager import UsersManager
from csle_common.controllers.vulnerabilities_manager import VulnerabilitiesManager
from csle_common.controllers.flags_manager import FlagsManager
from csle_common.controllers.traffic_manager import TrafficManager
from csle_common.controllers.topology_manager import TopologyManager
from csle_common.controllers.monitor_tools_controller import MonitorToolsController
from csle_common.controllers.resource_constraints_manager import ResourceConstraintsManager
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.logging.log import Logger


class EmulationEnvManager:
    """
    Class managing emulation environments
    """

    @staticmethod
    def apply_emulation_env_config(emulation_env_config: EmulationEnvConfig, no_traffic: bool = False) -> None:
        """
        Applies the emulation env config

        :param emulation_env_config: the config to apply
        :param no_traffic: a boolean parameter that is True if the traffic generators should be skipped
        :return: None
        """
        steps = 17
        if no_traffic:
            steps = steps-1
        current_step = 1
        Logger.__call__().get_logger().info(f"-- Configuring the emulation: {emulation_env_config.name} --")
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Creating networks --")
        ContainerManager.create_networks(containers_config=emulation_env_config.containers_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Connect containers to networks --")
        ContainerManager.connect_containers_to_networks(containers_config=emulation_env_config.containers_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Apply log sink config --")
        EmulationEnvManager.apply_log_sink_config(emulation_env_config=emulation_env_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Connect containers to log sink --")
        ContainerManager.connect_containers_to_logsink(containers_config=emulation_env_config.containers_config,
                                                       log_sink_config=emulation_env_config.log_sink_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Creating users --")
        UsersManager.create_users(emulation_env_config=emulation_env_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Creating vulnerabilities --")
        VulnerabilitiesManager.create_vulns(emulation_env_config=emulation_env_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Creating flags --")
        FlagsManager.create_flags(emulation_env_config=emulation_env_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Creating topology --")
        TopologyManager.create_topology(emulation_env_config=emulation_env_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Creating resource constraints --")
        ResourceConstraintsManager.apply_resource_constraints(emulation_env_config=emulation_env_config)

        if not no_traffic:
            current_step += 1
            Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Creating traffic generators --")
            TrafficManager.create_and_start_internal_traffic_generators(emulation_env_config=emulation_env_config)
            TrafficManager.start_client_population(emulation_env_config=emulation_env_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step "
                                            f"{current_step}/{steps}: Starting the Intrusion Detection System --")
        IDSManager.start_ids(emulation_env_config=emulation_env_config)
        time.sleep(10)
        IDSManager.start_ids_monitor_thread(emulation_env_config=emulation_env_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting the Host managers --")
        HostManager.start_host_monitor_thread(emulation_env_config=emulation_env_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting the Docker stats monitor --")
        MonitorToolsController.start_docker_stats_manager(port=50051)
        time.sleep(10)
        ContainerManager.start_docker_stats_thread(
            log_sink_config=emulation_env_config.log_sink_config,
            containers_config=emulation_env_config.containers_config,
            emulation_name=emulation_env_config.name)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting Cadvisor --")
        MonitorToolsController.start_cadvisor()
        time.sleep(2)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting Grafana --")
        MonitorToolsController.start_grafana()
        time.sleep(2)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting Node_exporter --")
        MonitorToolsController.start_node_exporter()
        time.sleep(2)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting Prometheus --")
        MonitorToolsController.start_prometheus()
        time.sleep(2)

    @staticmethod
    def apply_log_sink_config(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Applies the log sink config

        :param emulation_env_config: the emulation env config
        :return: None
        """
        steps = 4
        current_step = 1
        Logger.__call__().get_logger().info(f"-- Configuring the logsink --")

        Logger.__call__().get_logger().info(f"-- Log sink configuration step {current_step}/{steps}: Creating networks --")
        networks = ContainerManager.get_network_references()
        networks = list(map(lambda x: x.name, networks))
        ip, net = emulation_env_config.log_sink_config.container.ips_and_networks[0]
        ContainerManager.create_network_from_dto(network_dto=net, existing_network_names=networks)

        current_step += 1
        Logger.__call__().get_logger().info(
            f"-- Log sink configuration step {current_step}/{steps}: Connect log sink container to network --")
        ContainerManager.connect_logsink_to_network(log_sink_config=emulation_env_config.log_sink_config)

        Logger.__call__().get_logger().info(
            f"-- Log sink configuration step {current_step}/{steps}: Restarting the Kafka server --")
        LogSinkManager.stop_kafka_server(emulation_env_config=emulation_env_config)
        time.sleep(20)
        LogSinkManager.start_kafka_server(emulation_env_config=emulation_env_config)
        time.sleep(20)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Log sink configuration step {current_step}/{steps}: Create topics --")
        LogSinkManager.create_topics(emulation_env_config=emulation_env_config)

    @staticmethod
    def start_custom_traffic(emulation_env_config : EmulationEnvConfig) -> None:
        """
        Utility function for starting traffic generators and client population on a given emulation

        :param emulation_env_config: the configuration of the emulation
        :return: None
        """
        TrafficManager.create_and_start_internal_traffic_generators(emulation_env_config=emulation_env_config)
        TrafficManager.start_client_population(emulation_env_config=emulation_env_config)

    @staticmethod
    def stop_custom_traffic(emulation_env_config : EmulationEnvConfig) -> None:
        """
        Stops the traffic generators on all internal nodes and stops the arrival process of clients

        :param emulation_env_config: the configuration for connecting to the emulation
        :return: None
        """
        TrafficManager.stop_internal_traffic_generators(emulation_env_config=emulation_env_config)
        TrafficManager.stop_client_population(emulation_env_config=emulation_env_config)

    @staticmethod
    def delete_networks_of_log_sink(log_sink_config: LogSinkConfig) -> None:
        """
        Deletes the docker networks of a log sink

        :param log_sink_config: the log sink config
        :return: None
        """
        c = log_sink_config.container
        for ip_net in c.ips_and_networks:
            ip, net = ip_net
            ContainerManager.remove_network(name=net.name)

    @staticmethod
    def delete_networks_of_emulation_env_config(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Deletes the docker networks

        :param emulation_env_config: the emulation env config
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            for ip_net in c.ips_and_networks:
                ip, net = ip_net
                ContainerManager.remove_network(name=net.name)

        c = emulation_env_config.log_sink_config.container
        for ip_net in c.ips_and_networks:
            ip, net = ip_net
            ContainerManager.remove_network(name=net.name)


    @staticmethod
    def run_containers(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Run containers in the emulation env config

        :param emulation_env_config: the config
        :return: None
        """
        path = ExperimentUtil.default_output_dir()
        for c in emulation_env_config.containers_config.containers:
            ips = c.get_ips()
            container_resources : NodeResourcesConfig = None
            for r in emulation_env_config.resources_config.node_resources_configurations:
                for ip_net_resources in r.ips_and_network_configs:
                    ip, net_resources = ip_net_resources
                    if ip in ips:
                        container_resources : NodeResourcesConfig = r
                        break
            if container_resources is None:
                raise ValueError(f"Container resources not found for container with ips:{ips}, "
                                 f"resources:{emulation_env_config.resources_config}")

            name = c.get_full_name()
            Logger.__call__().get_logger().info(f"Starting container:{name}")
            cmd = f"docker container run -dt --name {name} " \
                  f"--hostname={c.name}{c.suffix} --label dir={path} " \
                  f"--label cfg={path + constants.DOCKER.EMULATION_ENV_CFG_PATH} " \
                  f"-e TZ=Europe/Stockholm " \
                  f"--label emulation={emulation_env_config.name} --network=none --publish-all=true " \
                  f"--memory={container_resources.available_memory_gb}G --cpus={container_resources.num_cpus} " \
                  f"--restart={c.restart_policy} --cap-add NET_ADMIN csle/{c.name}:{c.version}"
            subprocess.call(cmd, shell=True)

        c = emulation_env_config.log_sink_config.container
        container_resources : NodeResourcesConfig = emulation_env_config.log_sink_config.resources

        name = f"{constants.CSLE.NAME}-{c.name}{c.suffix}-level{c.level}"
        Logger.__call__().get_logger().info(f"Starting container:{name}")
        cmd = f"docker container run -dt --name {name} " \
              f"--hostname={c.name}{c.suffix} --label dir={path} " \
              f"--label cfg={path + constants.DOCKER.EMULATION_ENV_CFG_PATH} " \
              f"-e TZ=Europe/Stockholm " \
              f"--label emulation={emulation_env_config.name} --network=none --publish-all=true " \
              f"--memory={container_resources.available_memory_gb}G --cpus={container_resources.num_cpus} " \
              f"--restart={c.restart_policy} --cap-add NET_ADMIN csle/{c.name}:{c.version}"
        subprocess.call(cmd, shell=True)


    @staticmethod
    def run_container(image: str, name: str, memory : int = 4, num_cpus: int = 1) -> None:
        """
        Runs a given container

        :param image: image of the container
        :param name: name of the container
        :param memory: memory in GB
        :param num_cpus: number of CPUs to allocate
        :return: None
        """
        net_id = random.randint(128, 254)
        sub_net_id= random.randint(2, 254)
        host_id= random.randint(2, 254)
        net_name = f"csle_custom_net_{name}_{net_id}"
        ip = f"55.{net_id}.{sub_net_id}.{host_id}"
        ContainerManager.create_network(name=net_name,
                                        subnetmask=f"55.{net_id}.0.0/16",
                                        existing_network_names=[])
        Logger.__call__().get_logger().info(f"Starting container with image:{image} and name:csle-{name}-001")
        cmd = f"docker container run -dt --name csle-{name}-001 " \
              f"--hostname={name} " \
              f"-e TZ=Europe/Stockholm " \
              f"--network={net_name} --ip {ip} --publish-all=true " \
              f"--memory={memory}G --cpus={num_cpus} " \
              f"--restart={constants.DOCKER.ON_FAILURE_3} --cap-add NET_ADMIN {image}"
        subprocess.call(cmd, shell=True)

    @staticmethod
    def stop_containers(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Stop containers in the emulation env config

        :param emulation_env_config: the config
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            name = c.get_full_name()
            Logger.__call__().get_logger().info(f"Stopping container:{name}")
            cmd = f"docker stop {name}"
            subprocess.call(cmd, shell=True)

        c = emulation_env_config.log_sink_config.container
        name = c.get_full_name()
        Logger.__call__().get_logger().info(f"Stopping container:{name}")
        cmd = f"docker stop {name}"
        subprocess.call(cmd, shell=True)

    @staticmethod
    def rm_containers(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Remove containers in the emulation env config

        :param emulation_env_config: the config
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            name = f"{constants.CSLE.NAME}-{c.name}{c.suffix}-level{c.level}"
            Logger.__call__().get_logger().info(f"Removing container:{name}")
            cmd = f"docker rm {name}"
            subprocess.call(cmd, shell=True)

        c = emulation_env_config.log_sink_config.container
        name = c.get_full_name()
        Logger.__call__().get_logger().info(f"Removing container:{name}")
        cmd = f"docker rm {name}"
        subprocess.call(cmd, shell=True)

    @staticmethod
    def install_emulation(config: EmulationEnvConfig) -> None:
        """
        Installs the emulation configuration in the metastore

        :param config: the config to install
        :return: None
        """
        MetastoreFacade.install_emulation(config=config)

    @staticmethod
    def save_emulation_image(img: bytes, emulation_name: str) -> None:
        """
        Saves the emulation image

        :param image: the image data
        :param emulation_name: the name of the emulation
        :return: None
        """
        MetastoreFacade.save_emulation_image(img=img, emulation_name=emulation_name)

    @staticmethod
    def uninstall_emulation(config: EmulationEnvConfig) -> None:
        """
        Uninstalls the emulation configuration in the metastore

        :param config: the config to uninstall
        :return: None
        """
        MetastoreFacade.uninstall_emulation(config=config)

    @staticmethod
    def separate_running_and_stopped_emulations_dtos(emulations : List[EmulationEnvConfig]) \
            -> Tuple[List[EmulationEnvConfig], List[EmulationEnvConfig]]:
        """
        Partitions the set of emulations into a set of running emulations and a set of stopped emulations

        :param emulations: the list of emulations
        :return: running_emulations, stopped_emulations
        """
        rc_emulations = ContainerManager.list_running_emulations()
        stopped_emulations = []
        running_emulations = []
        for em in emulations:
            if em.name in rc_emulations:
                running_emulations.append(em)
            else:
                stopped_emulations.append(em)
        return running_emulations, stopped_emulations

