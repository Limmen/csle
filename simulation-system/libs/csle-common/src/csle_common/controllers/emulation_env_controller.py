from typing import List, Tuple, Dict, Any
import time
import subprocess
import random
import paramiko
import csle_collector.constants.constants as collector_constants
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.kafka_config import KafkaConfig
from csle_common.dao.emulation_config.node_resources_config import NodeResourcesConfig
from csle_common.controllers.container_controller import ContainerController
from csle_common.controllers.snort_ids_controller import SnortIDSController
from csle_common.controllers.ossec_ids_controller import OSSECIDSController
from csle_common.controllers.host_controller import HostController
from csle_common.controllers.kafka_controller import KafkaController
from csle_common.controllers.elk_controller import ELKController
from csle_common.controllers.sdn_controller_manager import SDNControllerManager
from csle_common.controllers.users_controller import UsersController
from csle_common.controllers.vulnerabilities_controller import VulnerabilitiesController
from csle_common.controllers.flags_controller import FlagsController
from csle_common.controllers.traffic_controller import TrafficController
from csle_common.controllers.topology_controller import TopologyController
from csle_common.controllers.ovs_controller import OVSController
from csle_common.controllers.management_system_controller import ManagementSystemController
from csle_common.controllers.resource_constraints_controller import ResourceConstraintsController
from csle_common.util.emulation_util import EmulationUtil
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.logging.log import Logger
from csle_common.dao.emulation_config.emulation_execution import EmulationExecution
from csle_common.dao.emulation_config.emulation_execution_info import EmulationExecutionInfo
from csle_common.dao.emulation_config.config import Config
from csle_common.tunneling.forward_tunnel_thread import ForwardTunnelThread


class EmulationEnvController:
    """
    Class managing emulation environments
    """

    @staticmethod
    def stop_all_executions_of_emulation(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Stops all executions of a given emulation

        :param emulation_env_config: the emulation for which executions should be stopped
        :return: None
        """
        executions = MetastoreFacade.list_emulation_executions_for_a_given_emulation(
            emulation_name=emulation_env_config.name)
        for exec in executions:
            EmulationEnvController.stop_containers(execution=exec)
            ContainerController.stop_docker_stats_thread(execution=exec)

    @staticmethod
    def stop_execution_of_emulation(emulation_env_config: EmulationEnvConfig, execution_id: int) -> None:
        """
        Stops an execution of a given emulation

        :param emulation_env_config: the emulation for which executions should be stopped
        :param execution_id: the id of the execution to stop
        :return: None
        """
        execution = MetastoreFacade.get_emulation_execution(emulation_name=emulation_env_config.name,
                                                            ip_first_octet=execution_id)
        EmulationEnvController.stop_containers(execution=execution)
        ContainerController.stop_docker_stats_thread(execution=execution)

    @staticmethod
    def stop_all_executions() -> None:
        """
        Stops all emulation executions

        :return: None
        """
        executions = MetastoreFacade.list_emulation_executions()
        for exec in executions:
            EmulationEnvController.stop_containers(execution=exec)
            ContainerController.stop_docker_stats_thread(execution=exec)

    @staticmethod
    def install_csle_collector_library(emulation_env_config: EmulationEnvConfig):
        """
        Installs the latest csle-collector library on all nodes

        :return:
        """
        ips = list(map(lambda x: x.get_ips()[0], emulation_env_config.containers_config.containers))
        ips.append(emulation_env_config.kafka_config.container.get_ips()[0])
        ips.append(emulation_env_config.elk_config.container.get_ips()[0])
        for ip in ips:
            Logger.__call__().get_logger().info(f"Installing csle-collector version "
                                                f"{emulation_env_config.csle_collector_version} on node: {ip}")
            EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=ip)
            cmd = collector_constants.INSTALL
            if emulation_env_config.csle_collector_version != collector_constants.LATEST_VERSION:
                cmd = cmd + f"=={emulation_env_config.csle_collector_version}"
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))
            time.sleep(2)
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))
            EmulationUtil.disconnect_admin(emulation_env_config=emulation_env_config)

    @staticmethod
    def apply_emulation_env_config(emulation_execution: EmulationExecution, no_traffic: bool = False,
                                   no_clients: bool = False) -> None:
        """
        Applies the emulation env config

        :param emulation_execution: the emulation execution
        :param no_traffic: a boolean parameter that is True if the traffic generators should be skipped
        :param no_clients: a boolean parameter that is True if the client population should be skipped
        :return: None
        """
        steps = 37
        if no_traffic:
            steps = steps - 1
        if no_clients:
            emulation_execution.emulation_env_config.traffic_config.client_population_config = \
                emulation_execution.emulation_env_config.traffic_config.client_population_config.no_clients()

        current_step = 1
        emulation_env_config = emulation_execution.emulation_env_config

        Logger.__call__().get_logger().info(f"-- Configuring the emulation: {emulation_env_config.name} --")
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Creating networks --")
        ContainerController.create_networks(containers_config=emulation_env_config.containers_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Connect containers to networks --")
        ContainerController.connect_containers_to_networks(emulation_env_config=emulation_env_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Install csle-collector --")
        EmulationEnvController.install_csle_collector_library(emulation_env_config=emulation_env_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Apply kafka config --")
        EmulationEnvController.apply_kafka_config(emulation_env_config=emulation_env_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Connect SDN controller to  network --")
        SDNControllerManager.connect_sdn_controller_to_network(
            sdn_controller_config=emulation_env_config.sdn_controller_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Start SDN controller --")
        SDNControllerManager.start_controller(emulation_env_config=emulation_env_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Creating resource constraints --")
        ResourceConstraintsController.apply_resource_constraints(emulation_env_config=emulation_env_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Create OVS switches --")
        OVSController.create_virtual_switches_on_container(containers_config=emulation_env_config.containers_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Tests connections with Ping --")
        EmulationEnvController.ping_all(emulation_env_config=emulation_env_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Configure OVS switches --")
        OVSController.apply_ovs_config(emulation_env_config=emulation_env_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Tests connections with Ping --")
        EmulationEnvController.ping_all(emulation_env_config=emulation_env_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Start Kafka producer at "
                                            f"SDN controller --")
        SDNControllerManager.start_controller_producer(emulation_env_config=emulation_env_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Creating users --")
        UsersController.create_users(emulation_env_config=emulation_env_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Creating vulnerabilities --")
        VulnerabilitiesController.create_vulns(emulation_env_config=emulation_env_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Creating flags --")
        FlagsController.create_flags(emulation_env_config=emulation_env_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Creating topology --")
        TopologyController.create_topology(emulation_env_config=emulation_env_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting traffic managers --")
        TrafficController.start_traffic_managers(emulation_env_config=emulation_env_config)

        if not no_traffic:
            current_step += 1
            Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting traffic generators "
                                                f"on internal nodes --")
            TrafficController.start_internal_traffic_generators(emulation_env_config=emulation_env_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting client population --")
        TrafficController.stop_client_producer(emulation_env_config=emulation_env_config)
        TrafficController.start_client_population(emulation_env_config=emulation_env_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting client Kafka producer --")
        TrafficController.start_client_producer(emulation_env_config=emulation_env_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step "
                                            f"{current_step}/{steps}: Starting the Snort Intrusion Detection System --")
        SnortIDSController.start_snort_idses(emulation_env_config=emulation_env_config)
        time.sleep(10)
        SnortIDSController.start_snort_idses_monitor_threads(emulation_env_config=emulation_env_config)
        time.sleep(10)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step "
                                            f"{current_step}/{steps}: Starting the OSSEC Intrusion Detection System --")
        OSSECIDSController.start_ossec_idses(emulation_env_config=emulation_env_config)
        time.sleep(10)
        OSSECIDSController.start_ossec_idses_monitor_threads(emulation_env_config=emulation_env_config)
        time.sleep(10)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting the ELK stack --")
        EmulationEnvController.apply_elk_config(emulation_env_config=emulation_env_config)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting the Host managers "
                                            f"and host monitors --")
        HostController.start_host_monitor_threads(emulation_env_config=emulation_env_config)
        time.sleep(10)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Applying filebeats configurations --")
        HostController.config_filebeats(emulation_env_config=emulation_env_config)
        time.sleep(10)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Applying packetbeats configurations --")
        HostController.config_packetbeats(emulation_env_config=emulation_env_config)
        time.sleep(10)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Applying metricbeats configurations --")
        HostController.config_metricbeats(emulation_env_config=emulation_env_config)
        time.sleep(10)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Applying heartbeats configurations --")
        HostController.config_heartbeats(emulation_env_config=emulation_env_config)
        time.sleep(10)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting filebeats --")
        HostController.start_filebeats(emulation_env_config=emulation_env_config, initial_start=True)
        time.sleep(10)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting packetbeats --")
        HostController.start_packetbeats(emulation_env_config=emulation_env_config, initial_start=True)
        time.sleep(10)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting metricbeats --")
        HostController.start_metricbeats(emulation_env_config=emulation_env_config, initial_start=True)
        time.sleep(10)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting heartbeats --")
        HostController.start_heartbeats(emulation_env_config=emulation_env_config, initial_start=True)
        time.sleep(10)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting the Docker stats monitor --")
        ManagementSystemController.start_docker_stats_manager(
            port=emulation_env_config.docker_stats_manager_config.docker_stats_manager_port,
            log_file=emulation_env_config.docker_stats_manager_config.docker_stats_manager_log_file,
            log_dir=emulation_env_config.docker_stats_manager_config.docker_stats_manager_log_dir,
            max_workers=emulation_env_config.docker_stats_manager_config.docker_stats_manager_max_workers
        )
        time.sleep(15)
        ContainerController.start_docker_stats_thread(execution=emulation_execution)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting Cadvisor --")
        ManagementSystemController.start_cadvisor()
        time.sleep(2)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting Grafana --")
        ManagementSystemController.start_grafana()
        time.sleep(2)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting Node_exporter --")
        ManagementSystemController.start_node_exporter()
        time.sleep(2)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Step {current_step}/{steps}: Starting Prometheus --")
        ManagementSystemController.start_prometheus()
        time.sleep(2)

    @staticmethod
    def apply_kafka_config(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Applies the kafka config

        :param emulation_env_config: the emulation env config
        :return: None
        """
        steps = 2
        current_step = 1
        Logger.__call__().get_logger().info("-- Configuring the kafka container --")

        Logger.__call__().get_logger().info(
            f"-- Kafka configuration step {current_step}/{steps}: Restarting the Kafka server --")
        KafkaController.stop_kafka_server(emulation_env_config=emulation_env_config)
        time.sleep(20)
        KafkaController.start_kafka_server(emulation_env_config=emulation_env_config)
        time.sleep(20)

        current_step += 1
        Logger.__call__().get_logger().info(f"-- Kafka configuration step {current_step}/{steps}: Create topics --")
        KafkaController.create_topics(emulation_env_config=emulation_env_config)

    @staticmethod
    def apply_elk_config(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Applies the ELK config

        :param emulation_env_config: the emulation env config
        :return: None
        """
        steps = 1
        current_step = 1
        Logger.__call__().get_logger().info(
            f"-- ELK configuration step {current_step}/{steps}: Start the ELK stack  --")
        ELKController.start_elk_stack(emulation_env_config=emulation_env_config)
        time.sleep(30)

    @staticmethod
    def start_custom_traffic(emulation_env_config: EmulationEnvConfig, no_traffic: bool = True) -> None:
        """
        Utility function for starting traffic generators and client population on a given emulation

        :param emulation_env_config: the configuration of the emulation
        :param no_traffic boolean flag whether the internal traffic generators should be skipped.
        :return: None
        """
        if not no_traffic:
            TrafficController.start_internal_traffic_generators(emulation_env_config=emulation_env_config)
        TrafficController.stop_client_producer(emulation_env_config=emulation_env_config)
        TrafficController.start_client_population(emulation_env_config=emulation_env_config)
        TrafficController.start_client_producer(emulation_env_config=emulation_env_config)

    @staticmethod
    def stop_custom_traffic(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Stops the traffic generators on all internal nodes and stops the arrival process of clients

        :param emulation_env_config: the configuration for connecting to the emulation
        :return: None
        """
        TrafficController.stop_internal_traffic_generators(emulation_env_config=emulation_env_config)
        TrafficController.stop_client_population(emulation_env_config=emulation_env_config)

    @staticmethod
    def delete_networks_of_kafka_container(kafka_config: KafkaConfig) -> None:
        """
        Deletes the docker networks of a kafka container

        :param kafka_config: the kafka config
        :return: None
        """
        c = kafka_config.container
        for ip_net in c.ips_and_networks:
            ip, net = ip_net
            ContainerController.remove_network(name=net.name)

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
                ContainerController.remove_network(name=net.name)

        c = emulation_env_config.kafka_config.container
        for ip_net in c.ips_and_networks:
            ip, net = ip_net
            ContainerController.remove_network(name=net.name)

    @staticmethod
    def create_execution(emulation_env_config: EmulationEnvConfig) -> EmulationExecution:
        """
        Creates a new emulation execution
        :param emulation_env_config: the emulation configuration
        :return: a DTO representing the execution
        """
        timestamp = float(time.time())
        total_subnets = constants.CSLE.LIST_OF_IP_SUBNETS
        used_subnets = list(map(lambda x: x.ip_first_octet,
                                MetastoreFacade.list_emulation_executions_for_a_given_emulation(
                                    emulation_name=emulation_env_config.name)))
        available_sunets = list(filter(lambda x: x not in used_subnets, total_subnets))
        ip_first_octet = available_sunets[0]
        em_config = emulation_env_config.create_execution_config(ip_first_octet=ip_first_octet)
        emulation_execution = EmulationExecution(emulation_name=emulation_env_config.name,
                                                 timestamp=timestamp, ip_first_octet=ip_first_octet,
                                                 emulation_env_config=em_config)
        MetastoreFacade.save_emulation_execution(emulation_execution=emulation_execution)
        return emulation_execution

    @staticmethod
    def run_containers(emulation_execution: EmulationExecution) -> None:
        """
        Run containers in the emulation env config

        :param emulation_execution: the execution DTO
        :return: None
        """
        path = ExperimentUtil.default_output_dir()
        emulation_env_config = emulation_execution.emulation_env_config

        # Start regular containers
        for c in emulation_env_config.containers_config.containers:
            ips = c.get_ips()
            container_resources: NodeResourcesConfig = None
            for r in emulation_env_config.resources_config.node_resources_configurations:
                for ip_net_resources in r.ips_and_network_configs:
                    ip, net_resources = ip_net_resources
                    if ip in ips:
                        container_resources: NodeResourcesConfig = r
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
                  f"--restart={c.restart_policy} --cap-add NET_ADMIN --cap-add=SYS_NICE " \
                  f"{constants.CONTAINER_IMAGES.DOCKERHUB_USERNAME}/{c.name}:{c.version}"
            subprocess.call(cmd, shell=True)

        # Start the kafka container
        c = emulation_env_config.kafka_config.container
        container_resources: NodeResourcesConfig = emulation_env_config.kafka_config.resources
        name = c.get_full_name()
        Logger.__call__().get_logger().info(f"Starting container:{name}")
        cmd = f"docker container run -dt --name {name} " \
              f"--hostname={c.name}{c.suffix} --label dir={path} " \
              f"--label cfg={path + constants.DOCKER.EMULATION_ENV_CFG_PATH} " \
              f"-e TZ=Europe/Stockholm " \
              f"--label emulation={emulation_env_config.name} --network=none --publish-all=true " \
              f"--memory={container_resources.available_memory_gb}G --cpus={container_resources.num_cpus} " \
              f"--restart={c.restart_policy} --cap-add NET_ADMIN --cap-add=SYS_NICE " \
              f"{constants.CONTAINER_IMAGES.DOCKERHUB_USERNAME}/{c.name}:{c.version}"
        subprocess.call(cmd, shell=True)

        # Start the ELK container
        c = emulation_env_config.elk_config.container
        container_resources: NodeResourcesConfig = emulation_env_config.elk_config.resources
        name = c.get_full_name()
        Logger.__call__().get_logger().info(f"Starting container:{name}")
        cmd = f"docker container run -dt --name {name} " \
              f"--hostname={c.name}{c.suffix} --label dir={path} " \
              f"--label cfg={path + constants.DOCKER.EMULATION_ENV_CFG_PATH} " \
              f"-e TZ=Europe/Stockholm " \
              f"--label emulation={emulation_env_config.name} --network=none --publish-all=true " \
              f"--memory={container_resources.available_memory_gb}G --cpus={container_resources.num_cpus} " \
              f"--restart={c.restart_policy} --cap-add NET_ADMIN --cap-add=SYS_NICE " \
              f"{constants.CONTAINER_IMAGES.DOCKERHUB_USERNAME}/{c.name}:{c.version}"
        subprocess.call(cmd, shell=True)

        if emulation_env_config.sdn_controller_config is not None:
            # Start the SDN controller container
            c = emulation_env_config.sdn_controller_config.container
            container_resources: NodeResourcesConfig = emulation_env_config.sdn_controller_config.resources
            name = f"{constants.CSLE.NAME}-{c.name}{c.suffix}-level{c.level}-{c.execution_ip_first_octet}"
            Logger.__call__().get_logger().info(f"Starting container:{name}")
            cmd = f"docker container run -dt --name {name} " \
                  f"--hostname={c.name}{c.suffix} --label dir={path} " \
                  f"--label cfg={path + constants.DOCKER.EMULATION_ENV_CFG_PATH} " \
                  f"-e TZ=Europe/Stockholm " \
                  f"--label emulation={emulation_env_config.name} --network=none --publish-all=true " \
                  f"--memory={container_resources.available_memory_gb}G --cpus={container_resources.num_cpus} " \
                  f"--restart={c.restart_policy} --cap-add NET_ADMIN --cap-add=SYS_NICE " \
                  f"{constants.CONTAINER_IMAGES.DOCKERHUB_USERNAME}/{c.name}:{c.version}"
            subprocess.call(cmd, shell=True)

    @staticmethod
    def start_containers(emulation_execution: EmulationExecution) -> None:
        """
        Starts stopped containers in a given emulation execution

        :param emulation_execution: the execution DTO
        :return: None
        """
        emulation_env_config = emulation_execution.emulation_env_config

        # Start regular containers
        for c in emulation_env_config.containers_config.containers:
            ContainerController.start_container(name=c.get_full_name())

        # Start the kafka container
        c = emulation_env_config.kafka_config.container
        ContainerController.start_container(name=c.get_full_name())

        # Start the ELK container
        c = emulation_env_config.elk_config.container
        ContainerController.start_container(name=c.get_full_name())

        if emulation_env_config.sdn_controller_config is not None:
            # Start the SDN controller container
            c = emulation_env_config.sdn_controller_config.container
            ContainerController.start_container(name=c.get_full_name())

    @staticmethod
    def run_container(image: str, name: str, memory: int = 4, num_cpus: int = 1, create_network: bool = True,
                      version: str = "0.0.1") -> None:
        """
        Runs a given container

        :param image: image of the container
        :param name: name of the container
        :param memory: memory in GB
        :param num_cpus: number of CPUs to allocate
        :param create_network: whether to create a virtual network or not
        :param version: the version tag
        :return: None
        """
        Logger.__call__().get_logger().info(f"Starting container with image:{image} and name:csle_{name}-"
                                            f"{version.replace('.','')}")
        if create_network:
            net_id = random.randint(128, 254)
            sub_net_id = random.randint(2, 254)
            host_id = random.randint(2, 254)
            net_name = f"csle_custom_net_{name}_{net_id}"
            ip = f"55.{net_id}.{sub_net_id}.{host_id}"
            ContainerController.create_network(name=net_name,
                                               subnetmask=f"55.{net_id}.0.0/16",
                                               existing_network_names=[])
            cmd = f"docker container run -dt --name csle_{name}-{version.replace('.','')} " \
                  f"--hostname={name} " \
                  f"-e TZ=Europe/Stockholm " \
                  f"--network={net_name} --ip {ip} --publish-all=true " \
                  f"--memory={memory}G --cpus={num_cpus} " \
                  f"--restart={constants.DOCKER.ON_FAILURE_3} --cap-add NET_ADMIN --cap-add=SYS_NICE {image}"
        else:
            cmd = f"docker container run -dt --name csle-{name}-{version.replace('.','')} " \
                  f"--hostname={name} " \
                  f"-e TZ=Europe/Stockholm --net=none " \
                  f"--publish-all=true " \
                  f"--memory={memory}G --cpus={num_cpus} " \
                  f"--restart={constants.DOCKER.ON_FAILURE_3} --cap-add NET_ADMIN --cap-add=SYS_NICE {image}"
        subprocess.call(cmd, shell=True)

    @staticmethod
    def stop_containers(execution: EmulationExecution) -> None:
        """
        Stop containers in the emulation env config

        :param execution: the execution to stop
        :return: None
        """
        emulation_env_config = execution.emulation_env_config

        # Stop regular containers
        for c in emulation_env_config.containers_config.containers:
            name = c.get_full_name()
            Logger.__call__().get_logger().info(f"Stopping container:{name}")
            cmd = f"docker stop {name}"
            subprocess.call(cmd, shell=True)

        # Stop the Kafka container
        c = emulation_env_config.kafka_config.container
        name = c.get_full_name()
        Logger.__call__().get_logger().info(f"Stopping container:{name}")
        cmd = f"docker stop {name}"
        subprocess.call(cmd, shell=True)

        # Stop the ELK container
        c = emulation_env_config.elk_config.container
        name = c.get_full_name()
        Logger.__call__().get_logger().info(f"Stopping container:{name}")
        cmd = f"docker stop {name}"
        subprocess.call(cmd, shell=True)

        if emulation_env_config.sdn_controller_config is not None:
            # Stop the SDN controller container
            c = emulation_env_config.sdn_controller_config.container
            name = c.get_full_name()
            Logger.__call__().get_logger().info(f"Stopping container:{name}")
            cmd = f"docker stop {name}"
            subprocess.call(cmd, shell=True)

    @staticmethod
    def clean_all_emulation_executions(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Cleans an emulation

        :param emulation_env_config: the config of the emulation to clean
        :return: None
        """
        executions = MetastoreFacade.list_emulation_executions_for_a_given_emulation(
            emulation_name=emulation_env_config.name)
        for exec in executions:
            EmulationEnvController.stop_containers(execution=exec)
            EmulationEnvController.rm_containers(execution=exec)
            try:
                ContainerController.stop_docker_stats_thread(execution=exec)
            except Exception:
                pass
            EmulationEnvController.delete_networks_of_emulation_env_config(
                emulation_env_config=exec.emulation_env_config)
            MetastoreFacade.remove_emulation_execution(emulation_execution=exec)

    @staticmethod
    def clean_emulation_execution(emulation_env_config: EmulationEnvConfig, execution_id: int) -> None:
        """
        Cleans an emulation

        :param execution_id: the id of the execution to clean
        :param emulation_env_config: the config of the emulation to clean
        :return: None
        """
        execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id,
                                                            emulation_name=emulation_env_config.name)
        EmulationEnvController.stop_containers(execution=execution)
        EmulationEnvController.rm_containers(execution=execution)
        try:
            ContainerController.stop_docker_stats_thread(execution=execution)
        except Exception:
            pass
        EmulationEnvController.delete_networks_of_emulation_env_config(
            emulation_env_config=execution.emulation_env_config)
        MetastoreFacade.remove_emulation_execution(emulation_execution=execution)

    @staticmethod
    def clean_all_executions() -> None:
        """
        Cleans an emulation

        :param emulation_env_config: the config of the emulation to clean
        :return: None
        """
        executions = MetastoreFacade.list_emulation_executions()
        for exec in executions:
            EmulationEnvController.stop_containers(execution=exec)
            EmulationEnvController.rm_containers(execution=exec)
            try:
                ContainerController.stop_docker_stats_thread(execution=exec)
            except Exception:
                pass
            EmulationEnvController.delete_networks_of_emulation_env_config(
                emulation_env_config=exec.emulation_env_config)
            MetastoreFacade.remove_emulation_execution(emulation_execution=exec)

    @staticmethod
    def rm_containers(execution: EmulationExecution) -> None:
        """
        Remove containers in the emulation env config for a given execution

        :param execution: the execution to remove
        :return: None
        """

        # Remove regular containers
        for c in execution.emulation_env_config.containers_config.containers:
            name = c.get_full_name()
            Logger.__call__().get_logger().info(f"Removing container:{name}")
            cmd = f"docker rm {name}"
            subprocess.call(cmd, shell=True)

        # Remove the kafka container
        c = execution.emulation_env_config.kafka_config.container
        name = c.get_full_name()
        Logger.__call__().get_logger().info(f"Removing container:{name}")
        cmd = f"docker rm {name}"
        subprocess.call(cmd, shell=True)

        # Remove the elk container
        c = execution.emulation_env_config.elk_config.container
        name = c.get_full_name()
        Logger.__call__().get_logger().info(f"Removing container:{name}")
        cmd = f"docker rm {name}"
        subprocess.call(cmd, shell=True)

        if execution.emulation_env_config.sdn_controller_config is not None:
            # Remove the SDN controller container
            c = execution.emulation_env_config.sdn_controller_config.container
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
    def separate_running_and_stopped_emulations_dtos(emulations: List[EmulationEnvConfig]) \
            -> Tuple[List[EmulationEnvConfig], List[EmulationEnvConfig]]:
        """
        Partitions the set of emulations into a set of running emulations and a set of stopped emulations

        :param emulations: the list of emulations
        :return: running_emulations, stopped_emulations
        """
        rc_emulations = ContainerController.list_running_emulations()
        stopped_emulations = []
        running_emulations = []
        for em in emulations:
            if em.name in rc_emulations:
                running_emulations.append(em)
            else:
                stopped_emulations.append(em)
        return running_emulations, stopped_emulations

    @staticmethod
    def ping_all(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Tests the connections between all the containers using ping

        :param emulation_env_config: the emulation config
        :return: None
        """
        if emulation_env_config.sdn_controller_config is not None:

            # Ping controller-switches
            for ovs_sw in emulation_env_config.ovs_config.switch_configs:
                Logger.__call__().get_logger().info(f"Ping {ovs_sw.controller_ip} to {ovs_sw.ip}")
                cmd = f"{constants.COMMANDS.DOCKER_EXEC_COMMAND} " \
                      f"{emulation_env_config.sdn_controller_config.container.get_full_name()} " \
                      f"{constants.COMMANDS.PING} " \
                      f"{ovs_sw.ip} -c 5 &"
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

                Logger.__call__().get_logger().info(f"Ping {ovs_sw.ip} to {ovs_sw.controller_ip}")
                cmd = f"{constants.COMMANDS.DOCKER_EXEC_COMMAND} {ovs_sw.container_name} {constants.COMMANDS.PING} " \
                      f"{ovs_sw.controller_ip} -c 5 &"
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

        # Ping containers to switches
        for c1 in emulation_env_config.containers_config.containers:
            for c2 in emulation_env_config.containers_config.containers:
                for ip in c2.get_ips():
                    Logger.__call__().get_logger().info(f"Ping {c1.get_ips()[0]} to {ip}")
                    cmd = f"{constants.COMMANDS.DOCKER_EXEC_COMMAND} {c1.get_full_name()} {constants.COMMANDS.PING} " \
                          f"{ip} -c 5 &"
                    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

    @staticmethod
    def get_execution_info(execution: EmulationExecution) -> EmulationExecutionInfo:
        """
        Gets runtime information about an execution

        :param execution: the emulation execution to get the information for
        :return: execution information
        """
        running_containers, stopped_containers = ContainerController.list_all_running_containers_in_emulation(
            emulation_env_config=execution.emulation_env_config)
        active_ips = []
        for container in running_containers:
            active_ips = active_ips + container.get_ips()
        active_ips.append(constants.COMMON.LOCALHOST)
        active_ips.append(constants.COMMON.LOCALHOST_127_0_0_1)
        active_ips.append(constants.COMMON.LOCALHOST_127_0_1_1)
        config = Config.get_current_confg()
        for node in config.cluster_config.cluster_nodes:
            active_ips.append(node.ip)
        emulation_name = execution.emulation_name
        execution_id = execution.ip_first_octet
        snort_ids_managers_info = \
            SnortIDSController.get_snort_managers_info(emulation_env_config=execution.emulation_env_config,
                                                       active_ips=active_ips)
        ossec_ids_managers_info = \
            OSSECIDSController.get_ossec_managers_info(emulation_env_config=execution.emulation_env_config,
                                                       active_ips=active_ips)
        kafka_managers_info = \
            KafkaController.get_kafka_managers_info(emulation_env_config=execution.emulation_env_config,
                                                    active_ips=active_ips)
        host_managers_info = \
            HostController.get_host_managers_info(emulation_env_config=execution.emulation_env_config,
                                                  active_ips=active_ips)
        client_managers_info = \
            TrafficController.get_client_managers_info(emulation_env_config=execution.emulation_env_config,
                                                       active_ips=active_ips)
        traffic_managers_info = \
            TrafficController.get_traffic_managers_info(emulation_env_config=execution.emulation_env_config,
                                                        active_ips=active_ips)
        docker_stats_managers_info = \
            ContainerController.get_docker_stats_managers_info(emulation_env_config=execution.emulation_env_config,
                                                               active_ips=active_ips)
        elk_managers_info = \
            ELKController.get_elk_managers_info(emulation_env_config=execution.emulation_env_config,
                                                active_ips=active_ips)
        active_networks, inactive_networks = ContainerController.list_all_active_networks_for_emulation(
            emulation_env_config=execution.emulation_env_config)
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
                                                traffic_managers_info=traffic_managers_info)
        return execution_info

    @staticmethod
    def create_kibana_tunnel(execution: EmulationExecution, tunnels_dict: Dict[str, Any], local_port: int) -> None:
        """
        Creates an SSH tunnel to forward the Kibana port of a container

        :param execution: the emulation execution
        :param tunnels_dict: a dict with existing tunnels
        :param local_port: the local port to forward
        :return: None
        """
        config = Config.get_current_confg()
        if config is None:
            Config.set_config_parameters_from_config_file()
        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn.connect(execution.emulation_env_config.elk_config.container.get_ips()[0],
                     username=config.ssh_admin_username, password=config.ssh_admin_password)
        conn.get_transport().set_keepalive(5)
        agent_transport = conn.get_transport()
        tunnel_thread = ForwardTunnelThread(
            local_port=local_port,
            remote_host=execution.emulation_env_config.elk_config.container.get_ips()[0],
            remote_port=execution.emulation_env_config.elk_config.kibana_port, transport=agent_transport,
            tunnels_dict=tunnels_dict)
        tunnel_thread.start()
        tunnel_thread_dict = {}
        tunnel_thread_dict[api_constants.MGMT_WEBAPP.THREAD_PROPERTY] = tunnel_thread
        tunnel_thread_dict[api_constants.MGMT_WEBAPP.PORT_PROPERTY] = local_port
        tunnels_dict[execution.emulation_env_config.elk_config.container.get_ips()[0]] = tunnel_thread_dict
