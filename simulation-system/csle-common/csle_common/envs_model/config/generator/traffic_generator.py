import time
from typing import List
import grpc
import csle_collector.client_manager.client_manager_pb2_grpc
import csle_collector.client_manager.client_manager_pb2
import csle_collector.client_manager.query_clients
import csle_common.constants.constants as constants
from csle_common.dao.container_config.topology import Topology
from csle_common.dao.container_config.containers_config import ContainersConfig
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.logic.emulation.util.common.emulation_util import EmulationUtil
from csle_common.envs_model.config.generator.generator_util import GeneratorUtil
from csle_common.dao.container_config.traffic_config import TrafficConfig
from csle_common.dao.container_config.node_traffic_config import NodeTrafficConfig
from csle_common.util.experiments_util import util


class TrafficGenerator:
    """
    A Utility Class for generating traffic generation configuration files
    """

    @staticmethod
    def generate(topology: Topology, containers_config: ContainersConfig, agent_container_names : List[str],
                 router_container_names : List[str]) \
            -> TrafficConfig:
        """
        Generates a traffic configuration

        :param topology: topology of the environment
        :param containers_config: container configuration of the envirinment
        :param agent_container_names: list of agent container names
        :param router_container_names: list of router container names
        :return: the created traffic configuration
        """
        # jumphosts_dict = {}
        # targethosts_dict = {}
        # containers_dict = {}
        #
        # for node in topology.node_configs:
        #     ip = node.get_ips()[0]
        #     jumphosts = TrafficGenerator._find_jumphosts(topology=topology, ip=ip)
        #     jumphosts_dict[ip] = jumphosts
        #     targethosts_dict[ip] = []
        #
        # for node in topology.node_configs:
        #     for k,v in jumphosts_dict.items():
        #         if node.ip in v:
        #             targethosts_dict[node.ip].append(k)
        #
        # for container in containers_config.containers:
        #     containers_dict[container.internal_ip] = container.name

        node_traffic_configs = []
        for node in topology.node_configs:
            commands = []
            # for target in targethosts_dict[node.ip]:
            #     if containers_dict[target] not in agent_container_names \
            #             and containers_dict[target] not in router_container_names:
            #         template_commands = constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[containers_dict[target]]
            #         for tc in template_commands:
            #             commands.append(tc.format(target))

            node_traffic_config = NodeTrafficConfig(ip=node.get_ips()[0],
                                                    jumphosts=[], target_hosts=[], commands=commands)
            node_traffic_configs.append(node_traffic_config)

        traffic_config = TrafficConfig(node_traffic_configs = node_traffic_configs)
        return traffic_config

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
    def stop_client_population(traffic_config: TrafficConfig, emulation_config: EmulationConfig) -> None:
        """
        Function for stopping the client arrival process of an emulation

        :param traffic_config: the configuration of the client population
        :param emulation_config: the configuration to connect to the emulation
        :return: None
        """
        print(f"stopping client population on container: {traffic_config.client_population_config.ip}")

        # Connect
        GeneratorUtil.connect_admin(emulation_config=emulation_config, ip=traffic_config.client_population_config.ip)

        # Check if client_manager is already running
        cmd = constants.COMMANDS.PS_AUX + " | " + constants.COMMANDS.GREP \
              + constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.CLIENT_MANAGER_FILE_NAME
        o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
        t = constants.COMMANDS.SEARCH_CLIENT_MANAGER

        if not constants.COMMANDS.SEARCH_CLIENT_MANAGER in str(o):

            # Stop old background job if running
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL + \
                  constants.COMMANDS.SPACE_DELIM \
                  + constants.TRAFFIC_COMMANDS.CLIENT_MANAGER_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            # Start the client_manager
            cmd = constants.COMMANDS.START_CLIENT_MANAGER.format(
                traffic_config.client_population_config.client_manager_port)
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
            time.sleep(5)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{traffic_config.client_population_config.ip}:'
                f'{traffic_config.client_population_config.client_manager_port}') as channel:
            stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)
            client_dto = csle_collector.client_manager.query_clients.get_clients(stub)

            # Stop the client population
            if client_dto.client_process_active:
                csle_collector.client_manager.query_clients.stop_clients(stub)


    @staticmethod
    def start_client_population(traffic_config: TrafficConfig, containers_config: ContainersConfig,
                                emulation_config: EmulationConfig) -> None:
        """
        Starts the arrival process of clients

        :param traffic_config: the configuration of the client population
        :param containers_config: the container configurations
        :param emulation_config: the configuration to connect to the emulation
        :return: None
        """
        print(f"starting client population on container: {traffic_config.client_population_config.ip}")
        commands = []
        reachable_containers = []

        # Collect commands and reachable containers
        for container in containers_config.containers:
            match = False
            for ip,net in container.ips_and_networks:
                for net2 in traffic_config.client_population_config.networks:
                    if net.name == net2.name:
                        match = True
                        break
            if match:
                for ip2 in container.get_ips():
                    reachable_containers.append(ip2)

        for node_traffic_cfg in traffic_config.node_traffic_configs:
            if node_traffic_cfg.ip in reachable_containers:
                for cmd in node_traffic_cfg.commands:
                    commands.append(cmd.format(node_traffic_cfg.ip))

        for net in traffic_config.client_population_config.networks:
            for cmd in constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS["client_1_subnet"]:
                commands.append(cmd.format(net.subnet_mask))

        # Connect
        GeneratorUtil.connect_admin(emulation_config=emulation_config, ip=traffic_config.client_population_config.ip)

        # Check if client_manager is already running
        cmd = constants.COMMANDS.PS_AUX + " | " + constants.COMMANDS.GREP \
              + constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.CLIENT_MANAGER_FILE_NAME
        o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
        t = constants.COMMANDS.SEARCH_CLIENT_MANAGER

        if not constants.COMMANDS.SEARCH_CLIENT_MANAGER in str(o):

            # Stop old background job if running
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL + \
                  constants.COMMANDS.SPACE_DELIM \
                  + constants.TRAFFIC_COMMANDS.CLIENT_MANAGER_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            # Start the client_manager
            cmd = constants.COMMANDS.START_CLIENT_MANAGER.format(
                traffic_config.client_population_config.client_manager_port)
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
            time.sleep(5)

        # Open a gRPC session
        with grpc.insecure_channel(
                f'{traffic_config.client_population_config.ip}:'
                f'{traffic_config.client_population_config.client_manager_port}') as channel:
            stub = csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerStub(channel)
            client_dto = csle_collector.client_manager.query_clients.get_clients(stub)

            # Stop the client population if it is already running
            if client_dto.client_process_active:
                csle_collector.client_manager.query_clients.stop_clients(stub)
                time.sleep(5)


            # Start the client population
            csle_collector.client_manager.query_clients.start_clients(
                stub=stub, mu=traffic_config.client_population_config.mu,
                lamb=traffic_config.client_population_config.lamb, time_step_len_seconds=1, commands=commands,
                num_commands=traffic_config.client_population_config.num_commands)


    @staticmethod
    def stop_internal_traffic_generators(traffic_config: TrafficConfig,
                                                     emulation_config: EmulationConfig) -> None:
        """
        Utility function for stopping and deleting internal traffic generators

        :param traffic_config: the configuration of the traffic generators
        :param emulation_config: the configuration to connect to the emulation
        :return: None
        """
        for node in traffic_config.node_traffic_configs:
            print("stopping traffic generator script, node ip:{}".format(node.ip))

            # Connect
            GeneratorUtil.connect_admin(emulation_config=emulation_config, ip=node.ip)

            # Stop old background job if running
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL + \
                  constants.COMMANDS.SPACE_DELIM \
                  + constants.TRAFFIC_COMMANDS.TRAFFIC_GENERATOR_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            # Remove old file if exists
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.RM_F + \
                  constants.COMMANDS.SPACE_DELIM + \
                  constants.COMMANDS.SLASH_DELIM + constants.TRAFFIC_COMMANDS.TRAFFIC_GENERATOR_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            # Disconnect
            GeneratorUtil.disconnect_admin(emulation_config=emulation_config)


    @staticmethod
    def create_and_start_internal_traffic_generators(traffic_config: TrafficConfig, containers_config: ContainersConfig,
                                                     emulation_config: EmulationConfig, sleep_time : int = 2) -> None:
        """
        Installs the traffic generation scripts at each node

        :param traffic_config: the traffic configuration
        :param containers_config: the containers configuration
        :param emulation_config: the emulation configuration
        :param sleep_time: the time to sleep between commands
        :return: None
        """
        for node in traffic_config.node_traffic_configs:
            container = None
            for c in containers_config.containers:
                if node.ip in c.get_ips():
                    container = c
                    break

            commands = []
            subnet_masks = []
            reachable_containers = []
            for ip_net1 in container.ips_and_networks:
                ip,net1 = ip_net1
                subnet_masks.append(net1.subnet_mask)
            for c in containers_config.containers:
                for ip_net1 in c.ips_and_networks:
                    ip,net1 = ip_net1
                    if net1.subnet_mask in subnet_masks and ip not in container.get_ips():
                        reachable_containers.append((ip, c.get_ips()))

            for node2 in traffic_config.node_traffic_configs:
                for rc in reachable_containers:
                    ip, ips = rc
                    if node2.ip in ips:
                        for cmd in node2.commands:
                            commands.append(cmd.format(ip))

            print("creating traffic generator script, node ip:{}".format(node.ip))

            # Connect
            GeneratorUtil.connect_admin(emulation_config=emulation_config, ip=node.ip)

            # Stop old background job if running
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL + \
                  constants.COMMANDS.SPACE_DELIM \
                  + constants.TRAFFIC_COMMANDS.TRAFFIC_GENERATOR_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
            
            # Remove old file if exists
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.RM_F + \
                  constants.COMMANDS.SPACE_DELIM + \
                  constants.COMMANDS.SLASH_DELIM + constants.TRAFFIC_COMMANDS.TRAFFIC_GENERATOR_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

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
            sftp_client = emulation_config.agent_conn.open_sftp()
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM \
                  + constants.COMMANDS.TOUCH + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.SLASH_DELIM \
                  + constants.TRAFFIC_COMMANDS.TRAFFIC_GENERATOR_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            # Make executable
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.CHMOD_777 + \
                  constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.SLASH_DELIM \
                  + constants.TRAFFIC_COMMANDS.TRAFFIC_GENERATOR_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            # Write traffic generation script file
            remote_file = sftp_client.open(constants.COMMANDS.SLASH_DELIM
                                           + constants.TRAFFIC_COMMANDS.TRAFFIC_GENERATOR_FILE_NAME, mode="w")
            try:
                remote_file.write(script_file)
            except Exception as e:
                print("exception writing traffic generation file:{}".format(str(e)))
            finally:
                remote_file.close()

            # Start background job
            cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM \
                  + constants.COMMANDS.NOHUP + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.SLASH_DELIM \
                  + constants.TRAFFIC_COMMANDS.TRAFFIC_GENERATOR_FILE_NAME + constants.COMMANDS.SPACE_DELIM \
                  + constants.COMMANDS.AMP
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            # Disconnect
            GeneratorUtil.disconnect_admin(emulation_config=emulation_config)

    @staticmethod
    def stop_traffic_generators(traffic_config: TrafficConfig, emulation_config: EmulationConfig) -> None:
        """
        Stops running traffic generators at each node

        :param traffic_config: the traffic configuration
        :param emulation_config: the emulation configuration
        :return: None
        """
        for node in traffic_config.node_traffic_configs:

            # Connect
            GeneratorUtil.connect_admin(emulation_config=emulation_config, ip=node.ip)

            # Stop old background job if running
            cmd = constants.COMMANDS.SUDO + " " + constants.COMMANDS.PKILL + " " \
                  + constants.TRAFFIC_COMMANDS.TRAFFIC_GENERATOR_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            # Disconnect
            GeneratorUtil.disconnect_admin(emulation_config=emulation_config)


    @staticmethod
    def write_traffic_config(traffic_config: TrafficConfig, path: str = None) -> None:
        """
        Writes the default configuration to a json file

        :param traffic_config: the traffic config to write
        :param path: the path to write the configuration to
        :return: None
        """
        path = util.default_traffic_path(out_dir=path)
        util.write_traffic_config_file(traffic_config, path)


    @staticmethod
    def _find_jumphosts(topology: Topology, ip: str) -> List[str]:
        """
        Utility method to find Ips in a topology that can reach a specific ip

        :param topology: the topology
        :param ip: the ip to test
        :return: a list of ips that can reach the target ip
        """
        jumphosts = []
        for node in topology.node_configs:
            if ip in node.output_accept and ip in node.input_accept:
                jumphosts.append(node.ip)
        return jumphosts

