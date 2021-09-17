from typing import List
import pycr_common.constants.constants as constants
from pycr_common.dao.container_config.topology import Topology
from pycr_common.dao.container_config.containers_config import ContainersConfig
from pycr_common.dao.network.emulation_config import EmulationConfig
from pycr_common.envs_model.logic.emulation.util.common.emulation_util import EmulationUtil
from pycr_common.envs_model.config.generator.generator_util import GeneratorUtil
from pycr_common.dao.container_config.traffic_config import TrafficConfig
from pycr_common.dao.container_config.node_traffic_config import NodeTrafficConfig
from pycr_common.util.experiments_util import util


class TrafficGenerator:

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
        jumphosts_dict = {}
        targethosts_dict = {}
        containers_dict = {}

        for node in topology.node_configs:
            ip = node.ip
            jumphosts = TrafficGenerator._find_jumphosts(topology=topology, ip=ip)
            jumphosts_dict[ip] = jumphosts
            targethosts_dict[ip] = []

        for node in topology.node_configs:
            for k,v in jumphosts_dict.items():
                if node.ip in v:
                    targethosts_dict[node.ip].append(k)

        for container in containers_config.containers:
            containers_dict[container.ip] = container.name

        node_traffic_configs = []
        for node in topology.node_configs:
            commands = []
            for target in targethosts_dict[node.ip]:
                if containers_dict[target] not in agent_container_names \
                        and containers_dict[target] not in router_container_names:
                    template_commands = constants.TRAFFIC_COMMANDS.DEFAULT_COMMANDS[containers_dict[target]]
                    for tc in template_commands:
                        commands.append(tc.format(target))

            node_traffic_config = NodeTrafficConfig(ip=node.ip, jumphosts=targethosts_dict[node.ip],
                                                    target_hosts=targethosts_dict[node.ip], commands=commands)
            node_traffic_configs.append(node_traffic_config)

        traffic_config = TrafficConfig(node_traffic_configs = node_traffic_configs)
        return traffic_config


    @staticmethod
    def create_traffic_scripts(traffic_config: TrafficConfig, emulation_config: EmulationConfig, sleep_time : int = 2,
                               only_clients : bool = False) -> None:
        """
        Installs the traffic generation scripts at each node

        :param traffic_config: the traffic configuration
        :param emulation_config: the emulation configuration
        :param sleep_time: the time to sleep between commands
        :param only_clients: whether to start only client traffic or also start internal traffic
        :return: None
        """
        for node in traffic_config.node_traffic_configs:
            if only_clients and not node.client:
                continue

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
            for cmd in node.commands:
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

