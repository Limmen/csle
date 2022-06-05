import time
import grpc
import csle_collector.client_manager.client_manager_pb2_grpc
import csle_collector.client_manager.client_manager_pb2
import csle_collector.client_manager.query_clients
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.util.emulation_util import EmulationUtil
from csle_common.dao.emulation_config.client_population_process_type import ClientPopulationProcessType
from csle_common.logging.log import Logger


class TrafficManager:
    """
    Class managing traffic generators in the emulation environments
    """

    @staticmethod
    def grpc_server_on(channel) -> bool:
        """
        Utility function to test if a given gRPC channel is working or not

        :param channel: the channel to test
        :return: True if working, False if timeout
        """
        try:
            grpc.channel_ready_future(channel).result(timeout=15)
            return True
        except grpc.FutureTimeoutError:
            return False

    @staticmethod
    def stop_client_population(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Function for stopping the client arrival process of an emulation

        :param emulation_env_config: the emulation env config
        :return: None
        """
        Logger.__call__().get_logger().info(f"stopping client population on container: "
              f"{emulation_env_config.traffic_config.client_population_config.ip}")

        # Connect
        EmulationUtil.connect_admin(emulation_env_config=emulation_env_config,
                                    ip=emulation_env_config.traffic_config.client_population_config.ip)

        # Check if client_manager is already running
        cmd = constants.COMMANDS.PS_AUX + " | " + constants.COMMANDS.GREP \
              + constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.CLIENT_MANAGER_FILE_NAME
        o, e, _ = EmulationUtil.execute_ssh_cmd(
            cmd=cmd,
            conn=emulation_env_config.get_connection(
                ip=emulation_env_config.traffic_config.client_population_config.ip))
        t = constants.COMMANDS.SEARCH_CLIENT_MANAGER

        if not constants.COMMANDS.SEARCH_CLIENT_MANAGER in str(o):

            # Stop old background job if running
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL + \
                  constants.COMMANDS.SPACE_DELIM \
                  + constants.TRAFFIC_COMMANDS.CLIENT_MANAGER_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(
                ip=emulation_env_config.traffic_config.client_population_config.ip))

            # Start the client_manager
            cmd = constants.COMMANDS.START_CLIENT_MANAGER.format(
                emulation_env_config.traffic_config.client_population_config.client_manager_port)
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(
                ip=emulation_env_config.traffic_config.client_population_config.ip))
            time.sleep(5)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{emulation_env_config.traffic_config.client_population_config.ip}:'
                f'{emulation_env_config.traffic_config.client_population_config.client_manager_port}') as channel:
            stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)
            client_dto = csle_collector.client_manager.query_clients.get_clients(stub)

            # Stop the producer
            if client_dto.client_process_active:
                csle_collector.client_manager.query_clients.stop_producer(stub)

            # Stop the client population
            if client_dto.client_process_active:
                csle_collector.client_manager.query_clients.stop_clients(stub)

    @staticmethod
    def start_client_population(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Starts the arrival process of clients

        :param emulation_env_config: the emulation environment configuration
        :return: None
        """
        Logger.__call__().get_logger().info(f"Starting client population on container:"
              f" {emulation_env_config.traffic_config.client_population_config.ip}")
        commands = []
        reachable_containers = []

        # Collect commands and reachable containers
        for container in emulation_env_config.containers_config.containers:
            match = False
            for ip,net in container.ips_and_networks:
                for net2 in emulation_env_config.traffic_config.client_population_config.networks:
                    if net.name == net2.name:
                        match = True
                        break
            if match:
                for ip2 in container.get_ips():
                    reachable_containers.append(ip2)

        for node_traffic_cfg in emulation_env_config.traffic_config.node_traffic_configs:
            if node_traffic_cfg.ip in reachable_containers:
                for cmd in node_traffic_cfg.commands:
                    commands.append(cmd.format(node_traffic_cfg.ip))

        for net in emulation_env_config.traffic_config.client_population_config.networks:
            for cmd in constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[constants.TRAFFIC_COMMANDS.CLIENT_1_SUBNET]:
                commands.append(cmd.format(net.subnet_mask))

        # Connect
        EmulationUtil.connect_admin(emulation_env_config=emulation_env_config,
                                    ip=emulation_env_config.traffic_config.client_population_config.ip)

        # Check if client_manager is already running
        cmd = constants.COMMANDS.PS_AUX + " | " + constants.COMMANDS.GREP \
              + constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.CLIENT_MANAGER_FILE_NAME
        o, e, _ = EmulationUtil.execute_ssh_cmd(
            cmd=cmd,
            conn=emulation_env_config.get_connection(
                ip=emulation_env_config.traffic_config.client_population_config.ip))
        t = constants.COMMANDS.SEARCH_CLIENT_MANAGER

        if not constants.COMMANDS.SEARCH_CLIENT_MANAGER in str(o):

            # Stop old background job if running
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL + \
                  constants.COMMANDS.SPACE_DELIM \
                  + constants.TRAFFIC_COMMANDS.CLIENT_MANAGER_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(
                ip=emulation_env_config.traffic_config.client_population_config.ip))

            # Start the client_manager
            cmd = constants.COMMANDS.START_CLIENT_MANAGER.format(
                emulation_env_config.traffic_config.client_population_config.client_manager_port)
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(
                ip=emulation_env_config.traffic_config.client_population_config.ip))
            time.sleep(5)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{emulation_env_config.traffic_config.client_population_config.ip}:'
                f'{emulation_env_config.traffic_config.client_population_config.client_manager_port}') as channel:
            stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)
            client_dto = csle_collector.client_manager.query_clients.get_clients(stub)

            # Stop the client population if it is already running
            if client_dto.client_process_active:
                csle_collector.client_manager.query_clients.stop_clients(stub)
                time.sleep(5)

            # Stop the producer thread if it is already running
            if client_dto.client_process_active:
                csle_collector.client_manager.query_clients.stop_producer(stub)
                time.sleep(5)

            # Start the client population
            sine_modulated = False
            if (emulation_env_config.traffic_config.client_population_config.client_process_type ==
                    ClientPopulationProcessType.SINE_MODULATED_POISSON):
                sine_modulated = True
            csle_collector.client_manager.query_clients.start_clients(
                stub=stub, mu=emulation_env_config.traffic_config.client_population_config.mu,
                lamb=emulation_env_config.traffic_config.client_population_config.lamb,
                time_step_len_seconds=
                emulation_env_config.traffic_config.client_population_config.client_time_step_len_seconds,
                commands=commands,
                num_commands=emulation_env_config.traffic_config.client_population_config.num_commands,
                sine_modulated=sine_modulated,
                time_scaling_factor=emulation_env_config.traffic_config.client_population_config.time_scaling_factor,
                period_scaling_factor=emulation_env_config.traffic_config.client_population_config.period_scaling_factor
            )

            time.sleep(5)

            # Start the producer thread
            csle_collector.client_manager.query_clients.start_producer(
                stub=stub, ip=emulation_env_config.log_sink_config.container.get_ips()[0],
                port=emulation_env_config.log_sink_config.kafka_port,
                time_step_len_seconds=emulation_env_config.log_sink_config.time_step_len_seconds)

    @staticmethod
    def get_num_active_clients(emulation_env_config : EmulationEnvConfig) \
            -> csle_collector.client_manager.client_manager_pb2.ClientsDTO:
        # Connect
        EmulationUtil.connect_admin(emulation_env_config=emulation_env_config,
                                    ip=emulation_env_config.traffic_config.client_population_config.ip)

        # Check if client_manager is already running
        cmd = constants.COMMANDS.PS_AUX + " | " + constants.COMMANDS.GREP \
              + constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.CLIENT_MANAGER_FILE_NAME
        o, e, _ = EmulationUtil.execute_ssh_cmd(
            cmd=cmd, conn=emulation_env_config.get_connection(
                ip=emulation_env_config.traffic_config.client_population_config.ip))
        t = constants.COMMANDS.SEARCH_CLIENT_MANAGER

        if not constants.COMMANDS.SEARCH_CLIENT_MANAGER in str(o):

            # Stop old background job if running
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL + \
                  constants.COMMANDS.SPACE_DELIM \
                  + constants.TRAFFIC_COMMANDS.CLIENT_MANAGER_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(
                ip=emulation_env_config.traffic_config.client_population_config.ip))

            # Start the client_manager
            cmd = constants.COMMANDS.START_CLIENT_MANAGER.format(
                emulation_env_config.traffic_config.client_population_config.client_manager_port)
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(
                ip=emulation_env_config.traffic_config.client_population_config.ip))
            time.sleep(5)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{emulation_env_config.traffic_config.client_population_config.ip}:'
                f'{emulation_env_config.traffic_config.client_population_config.client_manager_port}') as channel:
            stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)
            client_dto = csle_collector.client_manager.query_clients.get_clients(stub)
            return client_dto

    @staticmethod
    def stop_internal_traffic_generators(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Utility function for stopping and deleting internal traffic generators

        :param emulation_env_config: the configuration of the meulatio nenv
        :return: None
        """
        for node in emulation_env_config.traffic_config.node_traffic_configs:
            Logger.__call__().get_logger().info("stopping traffic generator script, node ip:{}".format(node.ip))

            # Connect
            EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=node.ip)

            # Stop old background job if running
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL + \
                  constants.COMMANDS.SPACE_DELIM \
                  + constants.TRAFFIC_COMMANDS.TRAFFIC_GENERATOR_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=node.ip))

            # Remove old file if exists
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.RM_F + \
                  constants.COMMANDS.SPACE_DELIM + \
                  constants.COMMANDS.SLASH_DELIM + constants.TRAFFIC_COMMANDS.TRAFFIC_GENERATOR_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=node.ip))

            # Disconnect
            EmulationUtil.disconnect_admin(emulation_env_config=emulation_env_config)

    @staticmethod
    def create_and_start_internal_traffic_generators(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Installs the traffic generation scripts at each node

        :param emulation_env_config: the emulation env configuration
        :return: None
        """
        sleep_time = emulation_env_config.traffic_config.client_population_config.client_time_step_len_seconds
        for node in emulation_env_config.traffic_config.node_traffic_configs:
            container = None
            for c in emulation_env_config.containers_config.containers:
                if node.ip in c.get_ips():
                    container = c
                    break

            commands = []
            subnet_masks = []
            reachable_containers = []
            for ip_net1 in container.ips_and_networks:
                ip,net1 = ip_net1
                subnet_masks.append(net1.subnet_mask)
            for c in emulation_env_config.containers_config.containers:
                for ip_net1 in c.ips_and_networks:
                    ip,net1 = ip_net1
                    if net1.subnet_mask in subnet_masks and ip not in container.get_ips():
                        reachable_containers.append((ip, c.get_ips()))

            for node2 in emulation_env_config.traffic_config.node_traffic_configs:
                for rc in reachable_containers:
                    ip, ips = rc
                    if node2.ip in ips:
                        for cmd in node2.commands:
                            commands.append(cmd.format(ip))

            Logger.__call__().get_logger().info("Creating traffic generator script, node ip:{}".format(node.ip))

            # Connect
            EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=node.ip)

            # Stop old background job if running
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL + \
                  constants.COMMANDS.SPACE_DELIM \
                  + constants.TRAFFIC_COMMANDS.TRAFFIC_GENERATOR_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=node.ip))

            # Remove old file if exists
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.RM_F + \
                  constants.COMMANDS.SPACE_DELIM + \
                  constants.COMMANDS.SLASH_DELIM + constants.TRAFFIC_COMMANDS.TRAFFIC_GENERATOR_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=node.ip))

            # File contents
            script_file = ""
            script_file = script_file + "#!/bin/bash\n"
            script_file = script_file + "while [ 1 ]\n"
            script_file = script_file + "do\n"
            script_file = script_file + "    sleep {}\n".format(sleep_time)
            for cmd in commands:
                script_file = script_file + "    " + cmd + "\n"
                script_file = script_file + "    sleep {}\n".format(sleep_time)
            script_file = script_file + "done\n"

            # Create file
            sftp_client = emulation_env_config.get_connection(ip=node.ip).open_sftp()
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM \
                  + constants.COMMANDS.TOUCH + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.SLASH_DELIM \
                  + constants.TRAFFIC_COMMANDS.TRAFFIC_GENERATOR_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=node.ip))

            # Make executable
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.CHMOD_777 + \
                  constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.SLASH_DELIM \
                  + constants.TRAFFIC_COMMANDS.TRAFFIC_GENERATOR_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=node.ip))

            # Write traffic generation script file
            remote_file = sftp_client.open(constants.COMMANDS.SLASH_DELIM
                                           + constants.TRAFFIC_COMMANDS.TRAFFIC_GENERATOR_FILE_NAME, mode="w")
            try:
                remote_file.write(script_file)
            except Exception as e:
                Logger.__call__().get_logger().warning("exception writing traffic generation file:{}".format(str(e)))
            finally:
                remote_file.close()

            # Start background job
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM \
                  + constants.COMMANDS.NOHUP + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.SLASH_DELIM \
                  + constants.TRAFFIC_COMMANDS.TRAFFIC_GENERATOR_FILE_NAME + constants.COMMANDS.SPACE_DELIM \
                  + constants.COMMANDS.AMP
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=node.ip))

            # Disconnect
            EmulationUtil.disconnect_admin(emulation_env_config=emulation_env_config)

    @staticmethod
    def stop_traffic_generators(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Stops running traffic generators at each node

        :param emulation_env_config: the emulation environment configuration
        :return: None
        """
        for node in emulation_env_config.traffic_config.node_traffic_configs:

            # Connect
            EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=node.ip)

            # Stop old background job if running
            cmd = constants.COMMANDS.SUDO + " " + constants.COMMANDS.PKILL + " " \
                  + constants.TRAFFIC_COMMANDS.TRAFFIC_GENERATOR_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=node.ip))

            # Disconnect
            EmulationUtil.disconnect_admin(emulation_env_config=emulation_env_config)