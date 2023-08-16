from typing import List, Dict, Any, Union
import logging
import time
import subprocess
import random
import paramiko
import csle_collector.constants.constants as collector_constants
import csle_ryu.constants.constants as ryu_constants
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.node_resources_config import NodeResourcesConfig
from csle_common.controllers.container_controller import ContainerController
from csle_common.controllers.snort_ids_controller import SnortIDSController
from csle_common.controllers.ossec_ids_controller import OSSECIDSController
from csle_common.controllers.host_controller import HostController
from csle_common.controllers.kafka_controller import KafkaController
from csle_common.controllers.elk_controller import ELKController
from csle_common.controllers.sdn_controller_manager import SDNControllerManager
from csle_common.controllers.traffic_controller import TrafficController
from csle_common.util.emulation_util import EmulationUtil
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.logging.log import Logger
from csle_common.dao.emulation_config.emulation_execution import EmulationExecution
from csle_common.dao.emulation_config.emulation_execution_info import EmulationExecutionInfo
from csle_common.dao.emulation_config.config import Config
from csle_common.tunneling.forward_tunnel_thread import ForwardTunnelThread
from csle_common.util.cluster_util import ClusterUtil


class EmulationEnvController:
    """
    Class managing emulation environments
    """

    @staticmethod
    def stop_all_executions_of_emulation(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                                         logger: logging.Logger) -> None:
        """
        Stops all executions of a given emulation

        :param emulation_env_config: the emulation for which executions should be stopped
        :param physical_server_ip: ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        executions = MetastoreFacade.list_emulation_executions_for_a_given_emulation(
            emulation_name=emulation_env_config.name)
        for exec in executions:
            EmulationEnvController.stop_containers(execution=exec, physical_server_ip=physical_server_ip,
                                                   logger=logger)
            ContainerController.stop_docker_stats_thread(execution=exec, physical_server_ip=physical_server_ip,
                                                         logger=logger)

    @staticmethod
    def stop_execution_of_emulation(emulation_env_config: EmulationEnvConfig, execution_id: int,
                                    physical_server_ip: str, logger: logging.Logger) -> None:
        """
        Stops an execution of a given emulation

        :param emulation_env_config: the emulation for which executions should be stopped
        :param execution_id: the id of the execution to stop
        :param physical_server_ip: ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        execution = MetastoreFacade.get_emulation_execution(emulation_name=emulation_env_config.name,
                                                            ip_first_octet=execution_id)
        if execution is None:
            raise ValueError(f"Could not find any execution with id: {execution_id}, "
                             f"emulation: {emulation_env_config.name}")
        EmulationEnvController.stop_containers(execution=execution, physical_server_ip=physical_server_ip,
                                               logger=logger)
        ContainerController.stop_docker_stats_thread(execution=execution, physical_server_ip=physical_server_ip,
                                                     logger=logger)

    @staticmethod
    def stop_all_executions(physical_server_ip: str, logger: logging.Logger) -> None:
        """
        Stops all emulation executions

        :param physical_server_ip: ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        executions = MetastoreFacade.list_emulation_executions()
        for exec in executions:
            EmulationEnvController.stop_containers(execution=exec, physical_server_ip=physical_server_ip,
                                                   logger=logger)
            ContainerController.stop_docker_stats_thread(execution=exec, physical_server_ip=physical_server_ip,
                                                         logger=logger)

    @staticmethod
    def install_csle_collector_and_ryu_libraries(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                                                 logger: logging.Logger) \
            -> None:
        """
        Installs the latest csle-collector and csle-ryu libraries on all nodes of a given emulation

        :param emulation_env_config: the emulation configuration
        :param physical_server_ip: the IP of the physical servers where the containers are
        :param logger: the logger to use for logging
        :return: None
        """
        containers = list(filter(lambda x: x.physical_host_ip == physical_server_ip,
                                 emulation_env_config.containers_config.containers))
        ips = list(map(lambda x: x.docker_gw_bridge_ip, containers))
        if emulation_env_config.kafka_config.container.physical_host_ip == physical_server_ip:
            ips.append(emulation_env_config.kafka_config.container.docker_gw_bridge_ip)
        if emulation_env_config.elk_config.container.physical_host_ip == physical_server_ip:
            ips.append(emulation_env_config.elk_config.container.docker_gw_bridge_ip)
        if emulation_env_config.sdn_controller_config is not None:
            ips.append(emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip)
        for ip in ips:
            logger.info(f"Installing csle-collector version "
                        f"{emulation_env_config.csle_collector_version} on node: {ip}")
            EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=ip)
            cmd = collector_constants.INSTALL
            if emulation_env_config.csle_collector_version != collector_constants.LATEST_VERSION:
                cmd = cmd + f"=={emulation_env_config.csle_collector_version}"
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))
            time.sleep(2)
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))
            time.sleep(2)
            logger.info(f"Installing csle-ryu version "
                        f"{emulation_env_config.csle_ryu_version} on node: {ip}")
            EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=ip)
            cmd = ryu_constants.INSTALL
            if emulation_env_config.csle_ryu_version != ryu_constants.LATEST_VERSION:
                cmd = cmd + f"=={emulation_env_config.csle_ryu_version}"
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))
            time.sleep(2)
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))

            EmulationUtil.disconnect_admin(emulation_env_config=emulation_env_config)

    @staticmethod
    def update_execution_config_w_docker_gw_bridge_ip(execution: EmulationExecution) -> EmulationExecution:
        """
        Updates the execution configuration with the IP of the docker gw of the docker swarm

        :param execution: the execution to update
        :return: the updated execution
        """
        emulation_env_config = execution.emulation_env_config
        emulation_env_config.kafka_config.resources.docker_gw_bridge_ip = \
            emulation_env_config.kafka_config.container.docker_gw_bridge_ip
        emulation_env_config.kafka_config.resources.physical_host_ip = \
            emulation_env_config.kafka_config.container.physical_host_ip
        emulation_env_config.elk_config.resources.docker_gw_bridge_ip = \
            emulation_env_config.elk_config.container.docker_gw_bridge_ip
        emulation_env_config.elk_config.resources.physical_host_ip = \
            emulation_env_config.elk_config.container.physical_host_ip
        if emulation_env_config.sdn_controller_config is not None:
            emulation_env_config.sdn_controller_config.resources.docker_gw_bridge_ip = \
                emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip
            emulation_env_config.sdn_controller_config.resources.physical_host_ip = \
                emulation_env_config.sdn_controller_config.container.physical_host_ip
        for resource_config in emulation_env_config.resources_config.node_resources_configurations:
            for container in emulation_env_config.containers_config.containers:
                if container.get_readable_name() == resource_config.container_name:
                    resource_config.docker_gw_bridge_ip = container.docker_gw_bridge_ip
                    resource_config.physical_host_ip = container.physical_host_ip
        for ovs_switch in emulation_env_config.ovs_config.switch_configs:
            for container in emulation_env_config.containers_config.containers:
                if container.get_readable_name() == ovs_switch.container_name:
                    ovs_switch.docker_gw_bridge_ip = container.docker_gw_bridge_ip
                    ovs_switch.physical_host_ip = container.physical_host_ip
        for user_config in emulation_env_config.users_config.users_configs:
            for container in emulation_env_config.containers_config.containers:
                if user_config.ip in container.get_ips():
                    user_config.docker_gw_bridge_ip = container.docker_gw_bridge_ip
                    user_config.physical_host_ip = container.physical_host_ip
        for vuln_config in emulation_env_config.vuln_config.node_vulnerability_configs:
            for container in emulation_env_config.containers_config.containers:
                if vuln_config.ip in container.get_ips():
                    vuln_config.docker_gw_bridge_ip = container.docker_gw_bridge_ip
                    vuln_config.physical_host_ip = container.physical_host_ip
        for flags_config in emulation_env_config.flags_config.node_flag_configs:
            for container in emulation_env_config.containers_config.containers:
                if flags_config.ip in container.get_ips():
                    flags_config.docker_gw_bridge_ip = container.docker_gw_bridge_ip
                    flags_config.physical_host_ip = container.physical_host_ip
        for node_fw_config in emulation_env_config.topology_config.node_configs:
            for container in emulation_env_config.containers_config.containers:
                for ip in container.get_ips():
                    if ip in node_fw_config.get_ips():
                        node_fw_config.docker_gw_bridge_ip = container.docker_gw_bridge_ip
                        node_fw_config.physical_host_ip = container.physical_host_ip
                        break
        emulation_env_config.kafka_config.firewall_config.docker_gw_bridge_ip = \
            emulation_env_config.kafka_config.container.docker_gw_bridge_ip
        emulation_env_config.kafka_config.firewall_config.physical_host_ip = \
            emulation_env_config.kafka_config.container.physical_host_ip
        emulation_env_config.elk_config.firewall_config.docker_gw_bridge_ip = \
            emulation_env_config.elk_config.container.docker_gw_bridge_ip
        emulation_env_config.elk_config.firewall_config.physical_host_ip = \
            emulation_env_config.elk_config.container.physical_host_ip
        if emulation_env_config.sdn_controller_config is not None:
            emulation_env_config.sdn_controller_config.firewall_config.docker_gw_bridge_ip = \
                emulation_env_config.sdn_controller_config.container.docker_gw_bridge_ip
            emulation_env_config.sdn_controller_config.firewall_config.physical_host_ip = \
                emulation_env_config.sdn_controller_config.container.physical_host_ip
        for node_traffic_config in emulation_env_config.traffic_config.node_traffic_configs:
            for container in emulation_env_config.containers_config.containers:
                if node_traffic_config.ip in container.get_ips():
                    node_traffic_config.docker_gw_bridge_ip = container.docker_gw_bridge_ip
                    node_traffic_config.physical_host_ip = container.physical_host_ip
        for container in emulation_env_config.containers_config.containers:
            if emulation_env_config.traffic_config.client_population_config.ip in container.get_ips():
                emulation_env_config.traffic_config.client_population_config.docker_gw_bridge_ip = \
                    container.docker_gw_bridge_ip
                emulation_env_config.traffic_config.client_population_config.physical_host_ip = \
                    container.physical_host_ip
        execution.emulation_env_config = emulation_env_config
        MetastoreFacade.update_emulation_execution(emulation_execution=execution,
                                                   ip_first_octet=execution.ip_first_octet,
                                                   emulation=execution.emulation_name)
        return execution

    @staticmethod
    def apply_kafka_config(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                           logger: logging.Logger) -> None:
        """
        Applies the kafka config

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        if emulation_env_config.kafka_config.container.physical_host_ip != physical_server_ip:
            return
        steps = 3
        current_step = 1
        logger.info("-- Configuring the kafka container --")

        logger.info(
            f"-- Kafka configuration step {current_step}/{steps}: Configuring the IP addresses of the kafka brokers --")
        KafkaController.configure_broker_ips(emulation_env_config=emulation_env_config, logger=logger)
        current_step += 1

        logger.info(
            f"-- Kafka configuration step {current_step}/{steps}: Restarting the Kafka server --")
        KafkaController.stop_kafka_server(emulation_env_config=emulation_env_config, logger=logger)
        time.sleep(20)
        KafkaController.start_kafka_server(emulation_env_config=emulation_env_config, logger=logger)
        time.sleep(20)

        current_step += 1
        logger.info(f"-- Kafka configuration step {current_step}/{steps}: Create topics --")
        KafkaController.create_topics(emulation_env_config=emulation_env_config, logger=logger)

    @staticmethod
    def start_custom_traffic(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                             no_traffic: bool = True) -> None:
        """
        Utility function for starting traffic generators and client population on a given emulation

        :param emulation_env_config: the configuration of the emulation
        :param no_traffic boolean flag whether the internal traffic generators should be skipped.
        :param physical_server_ip: ip of the physical servern
        :return: None
        """
        if not no_traffic:
            TrafficController.start_internal_traffic_generators(emulation_env_config=emulation_env_config,
                                                                physical_server_ip=physical_server_ip,
                                                                logger=Logger.__call__().get_logger())
        TrafficController.stop_client_producer(emulation_env_config=emulation_env_config,
                                               physical_server_ip=physical_server_ip,
                                               logger=Logger.__call__().get_logger())
        TrafficController.start_client_population(emulation_env_config=emulation_env_config,
                                                  physical_server_ip=physical_server_ip,
                                                  logger=Logger.__call__().get_logger())
        TrafficController.start_client_producer(emulation_env_config=emulation_env_config,
                                                physical_server_ip=physical_server_ip,
                                                logger=Logger.__call__().get_logger())

    @staticmethod
    def delete_networks_of_emulation_env_config(emulation_env_config: EmulationEnvConfig,
                                                physical_server_ip: str, logger: logging.Logger,
                                                leader: bool = False) -> None:
        """
        Deletes the docker networks

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server to remove the networks
        :param leader: boolean flag indicating whether this node is the leader in the Swarm cluster
        :param logger: the logger to use for logging
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip == physical_server_ip or leader:
                for ip_net in c.ips_and_networks:
                    ip, net = ip_net
                    ContainerController.remove_network(name=net.name, logger=logger)

        c = emulation_env_config.kafka_config.container
        if c.physical_host_ip == physical_server_ip or leader:
            for ip_net in c.ips_and_networks:
                ip, net = ip_net
                ContainerController.remove_network(name=net.name, logger=logger)

    @staticmethod
    def create_execution(emulation_env_config: EmulationEnvConfig, physical_servers: List[str], logger: logging.Logger,
                         id: int = -1) -> EmulationExecution:
        """
        Creates a new emulation execution

        :param emulation_env_config: the emulation configuration
        :param physical_servers: the physical servers to deploy the containers on
        :param id: the id of the execution (if not specified the next available id will be used)
        :param logger: the logger to use for logging
        :return: a DTO representing the execution
        """
        timestamp = float(time.time())
        total_subnets = constants.CSLE.LIST_OF_IP_SUBNETS
        used_subnets = list(map(lambda x: x.ip_first_octet,
                                MetastoreFacade.list_emulation_executions_for_a_given_emulation(
                                    emulation_name=emulation_env_config.name)))
        available_subnets = list(filter(lambda x: x not in used_subnets, total_subnets))
        ip_first_octet = available_subnets[0]
        if id != -1 and id not in available_subnets:
            logger.warning(f"The specified execution ID: {id} is not valid or is already taken. "
                           f"Using ID: {ip_first_octet} instead")
        elif id != -1 and id in available_subnets:
            ip_first_octet = id

        em_config = emulation_env_config.create_execution_config(ip_first_octet=ip_first_octet,
                                                                 physical_servers=physical_servers)
        emulation_execution = EmulationExecution(emulation_name=emulation_env_config.name,
                                                 timestamp=timestamp, ip_first_octet=ip_first_octet,
                                                 emulation_env_config=em_config, physical_servers=physical_servers)
        MetastoreFacade.save_emulation_execution(emulation_execution=emulation_execution)
        return emulation_execution

    @staticmethod
    def run_containers(emulation_execution: EmulationExecution, physical_host_ip: str, logger: logging.Logger) -> None:
        """
        Run containers in the emulation env config

        :param emulation_execution: the execution DTO
        :param physical_host_ip: the ip of the physical host where the containers should be started
        :param logger: the logger to use for logging
        :return: None
        """
        path = ExperimentUtil.default_output_dir()
        emulation_env_config = emulation_execution.emulation_env_config

        # Start regular containers
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_host_ip:
                continue
            ips = c.get_ips()
            container_resources: Union[None, NodeResourcesConfig] = None
            for r in emulation_env_config.resources_config.node_resources_configurations:
                for ip_net_resources in r.ips_and_network_configs:
                    ip, net_resources = ip_net_resources
                    if ip in ips:
                        container_resources = r
                        break
            if container_resources is None:
                raise ValueError(f"Container resources not found for container with ips:{ips}, "
                                 f"resources:{emulation_env_config.resources_config}")
            name = c.get_full_name()
            cmd = f"docker container run -dt --name {name} " \
                  f"--hostname={c.name}{c.suffix} --label dir={path} " \
                  f"--label cfg={path + constants.DOCKER.EMULATION_ENV_CFG_PATH} " \
                  f"-e TZ=Europe/Stockholm " \
                  f"--label emulation={emulation_env_config.name} --network=none --publish-all=true " \
                  f"--memory={container_resources.available_memory_gb}G --cpus={container_resources.num_cpus} " \
                  f"--restart={c.restart_policy} --cap-add NET_ADMIN --cap-add=SYS_NICE --privileged " \
                  f"{constants.CONTAINER_IMAGES.DOCKERHUB_USERNAME}/{c.name}:{c.version}"
            logger.info(f"Starting container:{name} with cmd: {cmd}")
            subprocess.call(cmd, shell=True)

        if emulation_env_config.kafka_config.container.physical_host_ip == physical_host_ip:
            # Start the kafka container
            c = emulation_env_config.kafka_config.container
            container_resources = emulation_env_config.kafka_config.resources
            name = c.get_full_name()
            cmd = f"docker container run -dt --name {name} " \
                  f"--hostname={c.name}{c.suffix} --label dir={path} " \
                  f"--label cfg={path + constants.DOCKER.EMULATION_ENV_CFG_PATH} " \
                  f"-e TZ=Europe/Stockholm " \
                  f"--label emulation={emulation_env_config.name} --network=none --publish-all=true " \
                  f"--memory={container_resources.available_memory_gb}G --cpus={container_resources.num_cpus} " \
                  f"--restart={c.restart_policy} --cap-add NET_ADMIN --cap-add=SYS_NICE --privileged " \
                  f"{constants.CONTAINER_IMAGES.DOCKERHUB_USERNAME}/{c.name}:{c.version}"
            logger.info(f"Starting container:{name}, cmd: {cmd}")
            subprocess.call(cmd, shell=True)

        if emulation_env_config.elk_config.container.physical_host_ip == physical_host_ip:
            # Start the ELK container
            c = emulation_env_config.elk_config.container
            container_resources = emulation_env_config.elk_config.resources
            name = c.get_full_name()
            cmd = f"docker container run -dt --name {name} " \
                  f"--hostname={c.name}{c.suffix} --label dir={path} " \
                  f"--label cfg={path + constants.DOCKER.EMULATION_ENV_CFG_PATH} " \
                  f"-e TZ=Europe/Stockholm " \
                  f"--label emulation={emulation_env_config.name} --network=none --publish-all=true " \
                  f"--memory={container_resources.available_memory_gb}G --cpus={container_resources.num_cpus} " \
                  f"--restart={c.restart_policy} --cap-add NET_ADMIN --cap-add=SYS_NICE --privileged " \
                  f"{constants.CONTAINER_IMAGES.DOCKERHUB_USERNAME}/{c.name}:{c.version}"
            logger.info(f"Starting container:{name}, cmd: {cmd}")
            subprocess.call(cmd, shell=True)

        if emulation_env_config.sdn_controller_config is not None \
                and emulation_env_config.sdn_controller_config.container.physical_host_ip == physical_host_ip:
            # Start the SDN controller container
            c = emulation_env_config.sdn_controller_config.container
            container_resources = emulation_env_config.sdn_controller_config.resources
            name = c.get_full_name()
            cmd = f"docker container run -dt --name {name} " \
                  f"--hostname={c.name}{c.suffix} --label dir={path} " \
                  f"--label cfg={path + constants.DOCKER.EMULATION_ENV_CFG_PATH} " \
                  f"-e TZ=Europe/Stockholm " \
                  f"--label emulation={emulation_env_config.name} --network=none --publish-all=true " \
                  f"--memory={container_resources.available_memory_gb}G --cpus={container_resources.num_cpus} " \
                  f"--restart={c.restart_policy} --cap-add NET_ADMIN --cap-add=SYS_NICE --privileged " \
                  f"{constants.CONTAINER_IMAGES.DOCKERHUB_USERNAME}/{c.name}:{c.version}"
            logger.info(f"Starting container:{name}, cmd: {cmd}")
            subprocess.call(cmd, shell=True)

    @staticmethod
    def start_containers_of_execution(emulation_execution: EmulationExecution, physical_host_ip: str) -> None:
        """
        Starts stopped containers in a given emulation execution

        :param emulation_execution: the execution DTO
        :param physical_host_ip: the ip of the physical host
        :return: None
        """
        emulation_env_config = emulation_execution.emulation_env_config

        # Start regular containers
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip == physical_host_ip:
                ContainerController.start_container(name=c.get_full_name())

        # Start the kafka container
        c = emulation_env_config.kafka_config.container
        if c.physical_host_ip == physical_host_ip:
            ContainerController.start_container(name=c.get_full_name())

        # Start the ELK container
        c = emulation_env_config.elk_config.container
        if c.physical_host_ip == physical_host_ip:
            ContainerController.start_container(name=c.get_full_name())

        if emulation_env_config.sdn_controller_config is not None:
            # Start the SDN controller container
            c = emulation_env_config.sdn_controller_config.container
            if c.physical_host_ip == physical_host_ip:
                ContainerController.start_container(name=c.get_full_name())

    @staticmethod
    def run_container(image: str, name: str, logger: logging.Logger, memory: int = 4, num_cpus: int = 1,
                      create_network: bool = True, version: str = "0.0.1") -> None:
        """
        Runs a given container

        :param image: image of the container
        :param name: name of the container
        :param memory: memory in GB
        :param num_cpus: number of CPUs to allocate
        :param create_network: whether to create a virtual network or not
        :param version: the version tag
        :param logger: the logger to use for logging
        :return: None
        """
        logger.info(f"Starting container with image:{image} and name:csle_{name}-{version.replace('.', '')}")
        if create_network:
            net_id = random.randint(128, 254)
            sub_net_id = random.randint(2, 254)
            host_id = random.randint(2, 254)
            net_name = f"csle_custom_net_{name}_{net_id}"
            ip = f"55.{net_id}.{sub_net_id}.{host_id}"
            ContainerController.create_network(
                name=net_name, subnetmask=f"55.{net_id}.0.0/16", existing_network_names=[], logger=logger)
            cmd = f"docker container run -dt --name csle_{name}-{version.replace('.', '')} " \
                  f"--hostname={name} " \
                  f"-e TZ=Europe/Stockholm " \
                  f"--network={net_name} --ip {ip} --publish-all=true " \
                  f"--memory={memory}G --cpus={num_cpus} " \
                  f"--restart={constants.DOCKER.ON_FAILURE_3} --cap-add NET_ADMIN --privileged " \
                  f"--cap-add=SYS_NICE {image}"
        else:
            cmd = f"docker container run -dt --name csle-{name}-{version.replace('.', '')} " \
                  f"--hostname={name} " \
                  f"-e TZ=Europe/Stockholm --net=none " \
                  f"--publish-all=true " \
                  f"--memory={memory}G --cpus={num_cpus} " \
                  f"--restart={constants.DOCKER.ON_FAILURE_3} --cap-add NET_ADMIN --privileged " \
                  f"--cap-add=SYS_NICE {image}"
        subprocess.call(cmd, shell=True)

    @staticmethod
    def stop_containers(execution: EmulationExecution, physical_server_ip: str, logger: logging.Logger) -> None:
        """
        Stop containers in the emulation env config

        :param execution: the execution to stop
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        emulation_env_config = execution.emulation_env_config

        # Stop regular containers
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            name = c.get_full_name()
            logger.info(f"Stopping container:{name}")
            cmd = f"docker stop {name}"
            subprocess.call(cmd, shell=True)

        # Stop the Kafka container
        c = emulation_env_config.kafka_config.container
        if c.physical_host_ip == physical_server_ip:
            name = c.get_full_name()
            logger.info(f"Stopping container:{name}")
            cmd = f"docker stop {name}"
            subprocess.call(cmd, shell=True)

        # Stop the ELK container
        c = emulation_env_config.elk_config.container
        if c.physical_host_ip == physical_server_ip:
            name = c.get_full_name()
            logger.info(f"Stopping container:{name}")
            cmd = f"docker stop {name}"
            subprocess.call(cmd, shell=True)

        if emulation_env_config.sdn_controller_config is not None:
            # Stop the SDN controller container
            c = emulation_env_config.sdn_controller_config.container
            if c.physical_host_ip == physical_server_ip:
                name = c.get_full_name()
                logger.info(f"Stopping container:{name}")
                cmd = f"docker stop {name}"
                subprocess.call(cmd, shell=True)

    @staticmethod
    def clean_all_emulation_executions(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                                       logger: logging.Logger, leader: bool = False) -> None:
        """
        Cleans an emulation

        :param emulation_env_config: the config of the emulation to clean
        :param physical_server_ip: the ip of the physical server to clean the emulation executions
        :param leader: boolean flag indicating whether this node is the leader in the Swarm cluster or not
        :param logger: the logger to use for logging
        :return: None
        """
        executions = MetastoreFacade.list_emulation_executions_for_a_given_emulation(
            emulation_name=emulation_env_config.name)
        for exec in executions:
            EmulationEnvController.stop_containers(execution=exec, physical_server_ip=physical_server_ip,
                                                   logger=logger)
            EmulationEnvController.rm_containers(execution=exec, physical_server_ip=physical_server_ip, logger=logger)
            try:
                ContainerController.stop_docker_stats_thread(execution=exec, physical_server_ip=physical_server_ip,
                                                             logger=logger)
            except Exception:
                pass
            EmulationEnvController.delete_networks_of_emulation_env_config(
                emulation_env_config=exec.emulation_env_config, physical_server_ip=physical_server_ip, logger=logger,
                leader=leader)

    @staticmethod
    def clean_emulation_execution(emulation_env_config: EmulationEnvConfig, execution_id: int,
                                  physical_server_ip: str, logger: logging.Logger, leader: bool = False) -> None:
        """
        Cleans an emulation execution

        :param execution_id: the id of the execution to clean
        :param emulation_env_config: the config of the emulation to clean
        :param physical_server_ip: the ip of the physical server to clean the execution
        :param leader: boolean flag indicating whether this node is the leader or not
        :param logger: the logger to use for logging
        :return: None
        """
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id,
                                                            emulation_name=emulation_env_config.name)
        if execution is None:
            raise ValueError(f"Could not find any execution with id: {execution_id}, "
                             f"emulation: {emulation_env_config.name}")
        EmulationEnvController.stop_containers(execution=execution, physical_server_ip=physical_server_ip,
                                               logger=logger)
        EmulationEnvController.rm_containers(execution=execution, physical_server_ip=physical_server_ip, logger=logger)
        try:
            ContainerController.stop_docker_stats_thread(execution=execution, physical_server_ip=physical_server_ip,
                                                         logger=logger)
        except Exception:
            pass
        EmulationEnvController.delete_networks_of_emulation_env_config(
            emulation_env_config=execution.emulation_env_config, physical_server_ip=physical_server_ip, logger=logger,
            leader=leader)

    @staticmethod
    def clean_all_executions(physical_server_ip: str, logger: logging.Logger, leader: bool = False) -> None:
        """
        Cleans all executions of a given emulation on a given physical server

        :param physical_server_ip: the ip of the physical server to clean the executions
        :param logger: the logger to use for logging
        :param leader: boolean flag indicating whether this node is the leader or not
        :return: None
        """
        executions = MetastoreFacade.list_emulation_executions()
        for exec in executions:
            EmulationEnvController.stop_containers(execution=exec, physical_server_ip=physical_server_ip,
                                                   logger=logger)
            EmulationEnvController.rm_containers(execution=exec, physical_server_ip=physical_server_ip, logger=logger)
            try:
                ContainerController.stop_docker_stats_thread(execution=exec, physical_server_ip=physical_server_ip,
                                                             logger=logger)
            except Exception:
                pass
            EmulationEnvController.delete_networks_of_emulation_env_config(
                emulation_env_config=exec.emulation_env_config, physical_server_ip=physical_server_ip, logger=logger,
                leader=leader)
            MetastoreFacade.remove_emulation_execution(emulation_execution=exec)

    @staticmethod
    def rm_containers(execution: EmulationExecution, physical_server_ip: str, logger: logging.Logger) -> None:
        """
        Remove containers in the emulation env config for a given execution

        :param execution: the execution to remove
        :param physical_server_ip: the ip of the physical server to remove the containers
        :param logger: the logger to use for logging
        :return: None
        """

        # Remove regular containers
        for c in execution.emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            name = c.get_full_name()
            logger.info(f"Removing container:{name}")
            cmd = f"docker rm {name}"
            subprocess.call(cmd, shell=True)

        # Remove the kafka container
        c = execution.emulation_env_config.kafka_config.container
        if c.physical_host_ip == physical_server_ip:
            name = c.get_full_name()
            logger.info(f"Removing container:{name}")
            cmd = f"docker rm {name}"
            subprocess.call(cmd, shell=True)

        # Remove the elk container
        c = execution.emulation_env_config.elk_config.container
        if c.physical_host_ip == physical_server_ip:
            name = c.get_full_name()
            logger.info(f"Removing container:{name}")
            cmd = f"docker rm {name}"
            subprocess.call(cmd, shell=True)

        if execution.emulation_env_config.sdn_controller_config is not None:
            # Remove the SDN controller container
            c = execution.emulation_env_config.sdn_controller_config.container
            if c.physical_host_ip == physical_server_ip:
                name = c.get_full_name()
                logger.info(f"Removing container:{name}")
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
    def ping_all(emulation_env_config: EmulationEnvConfig, physical_server_ip: str, logger: logging.Logger) -> None:
        """
        Tests the connections between all the containers using ping

        :param emulation_env_config: the emulation config
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        if emulation_env_config.sdn_controller_config is not None \
                and emulation_env_config.sdn_controller_config.container.physical_host_ip == physical_server_ip:

            # Ping controller-switches
            for ovs_sw in emulation_env_config.ovs_config.switch_configs:
                logger.info(f"Ping {ovs_sw.controller_ip} to {ovs_sw.ip}")
                cmd = f"{constants.COMMANDS.DOCKER_EXEC_COMMAND} " \
                      f"{emulation_env_config.sdn_controller_config.container.get_full_name()} " \
                      f"{constants.COMMANDS.PING} " \
                      f"{ovs_sw.ip} -c 5 &"
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

                logger.info(f"Ping {ovs_sw.ip} to {ovs_sw.controller_ip}")
                cmd = f"{constants.COMMANDS.DOCKER_EXEC_COMMAND} {ovs_sw.container_name} {constants.COMMANDS.PING} " \
                      f"{ovs_sw.controller_ip} -c 5 &"
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

        # Ping containers to switches
        for c1 in emulation_env_config.containers_config.containers:
            if c1.physical_host_ip != physical_server_ip:
                continue
            for c2 in emulation_env_config.containers_config.containers:
                for ip in c2.get_ips():
                    logger.info(f"Ping {c1.get_ips()[0]} to {ip}")
                    cmd = f"{constants.COMMANDS.DOCKER_EXEC_COMMAND} {c1.get_full_name()} {constants.COMMANDS.PING} " \
                          f"{ip} -c 5 &"
                    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

    @staticmethod
    def get_execution_info(execution: EmulationExecution, logger: logging.Logger, physical_server_ip: str) \
            -> EmulationExecutionInfo:
        """
        Gets runtime information about an execution

        :param execution: the emulation execution to get the information for
        :param logger: the logger to use for logging
        :param physical_server_ip: the IP of the physical server
        :return: execution information
        """
        running_containers, stopped_containers = ContainerController.list_all_running_containers_in_emulation(
            emulation_env_config=execution.emulation_env_config)
        active_ips: List[str] = []
        for container in running_containers:
            active_ips = active_ips + container.get_ips()
            active_ips.append(container.docker_gw_bridge_ip)
        active_ips.append(constants.COMMON.LOCALHOST)
        active_ips.append(constants.COMMON.LOCALHOST_127_0_0_1)
        active_ips.append(constants.COMMON.LOCALHOST_127_0_1_1)
        config = Config.get_current_config()
        if config is None:
            raise ValueError("Could not cluster read configuration")
        for node in config.cluster_config.cluster_nodes:
            active_ips.append(node.ip)
        emulation_name = execution.emulation_name
        execution_id = execution.ip_first_octet
        logger.info("Getting the Snort IDS Managers info")
        snort_ids_managers_info = \
            SnortIDSController.get_snort_managers_info(emulation_env_config=execution.emulation_env_config,
                                                       active_ips=active_ips, logger=logger,
                                                       physical_server_ip=physical_server_ip)
        logger.info("Getting the OSSEC IDS Managers info")
        ossec_ids_managers_info = \
            OSSECIDSController.get_ossec_managers_info(emulation_env_config=execution.emulation_env_config,
                                                       active_ips=active_ips, logger=logger,
                                                       physical_host_ip=physical_server_ip)
        logger.info("Getting the Kafka Managers info")
        kafka_managers_info = \
            KafkaController.get_kafka_managers_info(emulation_env_config=execution.emulation_env_config,
                                                    active_ips=active_ips, logger=logger,
                                                    physical_host_ip=physical_server_ip)
        logger.info("Getting the Host Managers info")
        host_managers_info = \
            HostController.get_host_managers_info(emulation_env_config=execution.emulation_env_config,
                                                  active_ips=active_ips, logger=logger,
                                                  physical_host_ip=physical_server_ip)
        logger.info("Getting the Client Managers info")
        client_managers_info = \
            TrafficController.get_client_managers_info(emulation_env_config=execution.emulation_env_config,
                                                       active_ips=active_ips, logger=logger)
        logger.info("Getting the Traffic Managers info")
        traffic_managers_info = \
            TrafficController.get_traffic_managers_info(emulation_env_config=execution.emulation_env_config,
                                                        active_ips=active_ips, logger=logger,
                                                        physical_host_ip=physical_server_ip)
        logger.info("Getting the Docker Stats Managers info")
        docker_stats_managers_info = \
            ContainerController.get_docker_stats_managers_info(emulation_env_config=execution.emulation_env_config,
                                                               active_ips=active_ips, logger=logger,
                                                               physical_host_ip=physical_server_ip)
        logger.info("Getting the Elk Managers info")
        elk_managers_info = \
            ELKController.get_elk_managers_info(emulation_env_config=execution.emulation_env_config,
                                                active_ips=active_ips, logger=logger,
                                                physical_host_ip=physical_server_ip)
        active_networks, inactive_networks = ContainerController.list_all_active_networks_for_emulation(
            emulation_env_config=execution.emulation_env_config)
        ryu_managers_info = None
        if execution.emulation_env_config.sdn_controller_config is not None:
            ryu_managers_info = SDNControllerManager.get_ryu_managers_info(
                emulation_env_config=execution.emulation_env_config, active_ips=active_ips,
                logger=logger, physical_server_ip=physical_server_ip)
        execution_info = EmulationExecutionInfo(emulation_name=emulation_name, execution_id=execution_id,
                                                snort_ids_managers_info=snort_ids_managers_info,
                                                ossec_ids_managers_info=ossec_ids_managers_info,
                                                kafka_managers_info=kafka_managers_info,
                                                host_managers_info=host_managers_info,
                                                client_managers_info=client_managers_info,
                                                docker_stats_managers_info=docker_stats_managers_info,
                                                running_containers=running_containers,
                                                stopped_containers=stopped_containers,
                                                active_networks=active_networks,
                                                inactive_networks=inactive_networks,
                                                elk_managers_info=elk_managers_info,
                                                traffic_managers_info=traffic_managers_info,
                                                ryu_managers_info=ryu_managers_info)
        return execution_info

    @staticmethod
    def create_ssh_tunnel(tunnels_dict: Dict[str, Any], local_port: int,
                          remote_port: int, remote_ip: str, emulation: str, execution_id: int) -> None:
        """
        Creates an SSH tunnel to forward the port of a container

        :param execution: the emulation execution
        :param tunnels_dict: a dict with existing tunnels
        :param local_port: the local port to forward
        :param remote_port: the remote port to forward
        :param remote_ip: the remote ip to forward
        :param emulation: the name of the emulation
        :param execution_id: the id of the execution
        :return: None
        """
        config = Config.get_current_config()
        if config is None:
            ClusterUtil.set_config_parameters_from_config_file()
        config = Config.get_current_config()
        if config is None:
            raise ValueError("Could not read the CSLE configuration")
        conn = paramiko.SSHClient()
        if conn is None:
            raise ValueError("Could not create paramiko SSH client")
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn.connect(remote_ip, username=config.ssh_admin_username, password=config.ssh_admin_password)
        agent_transport = conn.get_transport()
        if agent_transport is None:
            raise ValueError(f"Error opening SSH connection to {remote_ip}")
        agent_transport.set_keepalive(5)
        tunnel_thread = ForwardTunnelThread(
            local_port=local_port,
            remote_host=remote_ip,
            remote_port=remote_port, transport=agent_transport,
            tunnels_dict=tunnels_dict)
        tunnel_thread.start()
        tunnel_thread_dict: Dict[str, Union[ForwardTunnelThread, int, str]] = {}
        tunnel_thread_dict[constants.GENERAL.THREAD_PROPERTY] = tunnel_thread
        tunnel_thread_dict[constants.GENERAL.PORT_PROPERTY] = local_port
        tunnel_thread_dict[constants.GENERAL.EMULATION_PROPERTY] = emulation
        tunnel_thread_dict[constants.GENERAL.EXECUTION_ID_PROPERTY] = execution_id
        tunnels_dict[remote_ip] = tunnel_thread_dict
