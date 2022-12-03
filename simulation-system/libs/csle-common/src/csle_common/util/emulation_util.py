from typing import Tuple, List, Union
import time
import paramiko
import psutil
import csle_collector.constants.constants as collector_constants
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_observation.common.emulation_connection_observation_state \
    import EmulationConnectionObservationState
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.util.env_dynamics_util import EnvDynamicsUtil
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_outcome import EmulationAttackerActionOutcome
from csle_common.dao.emulation_config.credential import Credential
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_common.util.ssh_util import SSHUtil
from csle_common.logging.log import Logger


class EmulationUtil:
    """
    Class containing utility functions for the emulation-middleware
    """

    @staticmethod
    def execute_ssh_cmds(cmds: List[str], conn, wait_for_completion: bool = True) -> List[Tuple[bytes, bytes, float]]:
        """
        Executes a list of commands over an ssh connection to the emulation

        :param cmds: the list of commands
        :param conn: the ssh connection
        :param wait_for_completion: whether to wait for completion of the commands or not
        :return: List of tuples (outdata, errdata, total_time)
        """
        return SSHUtil.execute_ssh_cmds(cmds=cmds, conn=conn, wait_for_completion=wait_for_completion)

    @staticmethod
    def execute_ssh_cmd(cmd: str, conn, wait_for_completion: bool = True) -> Tuple[bytes, bytes, float]:
        """
        Executes an action on the emulation over a ssh connection,
        this is a synchronous operation that waits for the completion of the action before returning

        :param cmd: the command to execute
        :param conn: the ssh connection
        :param wait_for_completion: boolean flag whether to wait for completion or not
        :return: outdata, errdata, total_time
        """
        return SSHUtil.execute_ssh_cmd(cmd=cmd, conn=conn, wait_for_completion=wait_for_completion)

    @staticmethod
    def log_measured_action_time(total_time, action: EmulationAttackerAction,
                                 emulation_env_config: EmulationEnvConfig, create_producer: bool = False) -> None:
        """
        Logs the measured time of an action to Kafka

        :param total_time: the total time of executing the action
        :param action: the action
        :param emulation_env_config: the environment config
        :param create_producer: boolean flag whether to create a producer from the csle-admin
        :return: None
        """
        action.execution_time = total_time
        record = action.to_kafka_record()
        if emulation_env_config.producer is None and create_producer:
            emulation_env_config.create_producer()
        emulation_env_config.producer.produce(collector_constants.KAFKA_CONFIG.ATTACKER_ACTIONS_TOPIC_NAME, record)
        emulation_env_config.producer.poll(0)
        emulation_env_config.producer.flush()

    @staticmethod
    def _check_if_ssh_server_is_running(conn, telnet: bool = False) -> bool:
        """
        Checks if an ssh server is running on the machine

        :param conn: the connection to use for the command
        :param telnet: whether the connection is a telnet connection
        :return: True if server is running, else false
        """
        cmd = "service ssh status"
        if not telnet:
            outdata, errdata, total_time = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=conn)
            return "is running" in outdata.decode() or "is running" in errdata.decode()
        else:
            cmd = cmd + "\n"
            conn.write(cmd.encode())
            response = conn.read_until(constants.TELNET.PROMPT, timeout=5)
            return "is running" in response.decode()

    @staticmethod
    def _list_all_users(c: EmulationConnectionObservationState, emulation_env_config: EmulationEnvConfig,
                        telnet: bool = False) -> List:
        """
        List all users on a machine

        :param c: the connection to user for the command
        :param telnet: whether it is a telnet connection
        :param emulation_env_config: emulation env config
        :return: list of users
        """
        cmd = constants.SHELL.LIST_ALL_USERS
        users = []
        for i in range(constants.ENV_CONSTANTS.ATTACKER_RETRY_FIND_USERS):
            if not telnet:
                outdata, errdata, total_time = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=c.conn)
                outdata = outdata.decode()
                errdata = errdata.decode()
                users = outdata.split("\n")
                users = list(filter(lambda x: x != '', users))
            else:
                cmd = cmd + "\n"
                c.conn.write(cmd.encode())
                response = c.conn.read_until(constants.TELNET.PROMPT, timeout=5)
                response = response.decode()
                users = response.split("\n")
                users = list(map(lambda x: x.replace("\r", ""), users))
                users = list(filter(lambda x: x != '', users))
            if len(users) == 0:
                continue
            else:
                break
        if len(users) == 0:
            raise ValueError("users empty, ip:{}, telnet:{}, root:{}, username:{}".format(c.ip, telnet, c.root,
                                                                                          c.username))
        return users

    @staticmethod
    def is_connection_active(conn):
        """
        Checks if a given connection is active or not

        :param conn: the connection to check
        :return: True if active, otherwise False
        """
        if conn is not None and conn.get_transport() is not None:
            return conn.get_transport().is_active()
        else:
            return False

    @staticmethod
    def setup_custom_connection(user: str, pw: str, source_ip: str, port: int, target_ip: str, proxy_conn,
                                root: bool) \
            -> Union[EmulationConnectionObservationState, None]:
        """
        Utility function for setting up a custom SSH connection given credentials and a proxy connection
        :param user: the username of the new connection
        :param pw: the pw of the new connection
        :param source_ip: the ip of the proxy
        :param port: the port of the new connection
        :param target_ip: the ip to connect to
        :param proxy_conn: the proxy connection
        :param root: whether it is a root connection or not
        :return: the new connection
        """
        cr = Credential(username=user, pw=pw, root=root, protocol=TransportProtocol.TCP,
                        service=constants.SSH.SERVICE_NAME, port=constants.SSH.DEFAULT_PORT)
        agent_addr = (source_ip, port)
        target_addr = (target_ip, port)
        agent_transport = proxy_conn.conn.get_transport()
        try:
            relay_channel = agent_transport.open_channel(constants.SSH.DIRECT_CHANNEL, target_addr, agent_addr,
                                                         timeout=3)
            target_conn = paramiko.SSHClient()
            target_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            target_conn.connect(target_ip, username=user, password=pw, sock=relay_channel)
            target_conn.get_transport().set_keepalive(5)
            connection_dto = EmulationConnectionObservationState(
                conn=target_conn, credential=cr, root=root, service=constants.SSH.SERVICE_NAME,
                port=constants.SSH.DEFAULT_PORT, proxy=proxy_conn, ip=target_ip)
            return connection_dto
        except Exception as e:
            Logger.__call__().get_logger().warning(f"Custom connection setup failed: {str(e)}, {repr(e)}")
            return None

    @staticmethod
    def write_remote_file(conn, file_name: str, contents: str, write_mode: str = "w") -> None:
        """
        Utility function for writing contents to a file

        :param conn: the SSH connection to use for writing
        :param file_name: the file name
        :param contents: the contents of the file
        :param write_mode: the write mode
        :return: None
        """
        sftp_client = conn.open_sftp()
        remote_file = sftp_client.file(file_name, mode=write_mode)
        try:
            remote_file.write(contents)
        except Exception as e:
            Logger.__call__().get_logger().warning(f"Exception writing file: {str(e)}, {repr(e)}")
        finally:
            remote_file.close()

    @staticmethod
    def connect_admin(emulation_env_config: EmulationEnvConfig, ip: str,
                      create_producer: bool = False) -> None:
        """
        Connects the admin agent

        :param emulation_env_config: the configuration of the emulation to connect to
        :param ip: the ip of the container to connect to
        :param create_producer: boolean flag whether the producer thread to Kafka should be created also
        :return: None
        """
        emulation_env_config.agent_ip = ip
        emulation_env_config.connect(ip=ip, username=constants.CSLE_ADMIN.SSH_USER, pw=constants.CSLE_ADMIN.SSH_PW,
                                     create_producer=create_producer)

    @staticmethod
    def disconnect_admin(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Disconnects the admin agent

        :param emulation_env_config: the configuration of the emulation to disconnect the admin of
        :return: None
        """
        emulation_env_config.close_all_connections()

    @staticmethod
    def execute_cmd_interactive_channel(cmd: str, channel) -> None:
        """
        Executes an action on the emulation using an interactive shell (non synchronous)
        :param a: action to execute
        :param env_config: environment config
        :param channel: the channel to use
        :return: None
        """
        channel.send(cmd + "\n")

    @staticmethod
    def read_result_interactive(emulation_env_config: EmulationEnvConfig, channel) -> str:
        """
        Reads the result of an action executed in interactive mode

        :param emulation_env_config: the emulation environment config
        :param the channel
        :return: the result
        """
        return EmulationUtil.read_result_interactive_channel(
            emulation_env_config=emulation_env_config,
            channel=channel)

    @staticmethod
    def read_result_interactive_channel(emulation_env_config: EmulationEnvConfig, channel) -> str:
        """
        Reads the result of an action executed in interactive mode
        :param emulation_env_config: the emulation environment config
        :param channel: the channel to use
        :return: the result
        """
        while not channel.recv_ready():
            time.sleep(constants.ENV_CONSTANTS.SHELL_READ_WAIT)
        output = channel.recv(constants.COMMON.LARGE_RECV_SIZE)
        output_str = output.decode("utf-8")
        output_str = constants.NMAP.SHELL_ESCAPE.sub("", output_str)
        return output_str

    @staticmethod
    def is_emulation_defense_action_legal(defense_action_id: int, env_config: EmulationEnvConfig,
                                          env_state: EmulationEnvState) -> bool:
        """
        Checks if a given defense action is legal in the current state of the environment

        :param defense_action_id: the id of the action to check
        :param env_config: the environment config
        :param env_state: the environment state
        :param attacker_action: the id of the previous attack action
        :return: True if legal, else false
        """
        return True

    @staticmethod
    def is_emulation_attack_action_legal(attack_action_id: int, env_config: EmulationEnvConfig,
                                         env_state: EmulationEnvState) -> bool:
        """
        Checks if a given attack action is legal in the current state of the environment

        :param attack_action_id: the id of the action to check
        :param env_config: the environment config
        :param env_state: the environment state
        :return: True if legal, else false
        """
        if attack_action_id > len(env_state.attacker_action_config.actions) - 1:
            return False

        action = env_state.attacker_action_config.actions[attack_action_id]
        ip = env_state.attacker_obs_state.get_action_ips(action, emulation_env_config=env_config)

        logged_in_ips_str = EnvDynamicsUtil.logged_in_ips_str(emulation_env_config=env_config, s=env_state)
        if (action.id, action.index, logged_in_ips_str) in env_state.attacker_obs_state.actions_tried:
            return False

        # Recon on subnet is always possible
        if action.type == EmulationAttackerActionType.RECON and action.index == -1:
            return True

        # Recon on set of all found machines is always possible if there exists such machiens
        if action.type == EmulationAttackerActionType.RECON and action.index == -1 and len(
                env_state.attacker_obs_state.machines) > 0:
            return True

        # Optimal Stopping actions are always possible
        if action.type == EmulationAttackerActionType.STOP or action.type == EmulationAttackerActionType.CONTINUE:
            return True

        machine_discovered = False
        target_machine = None
        logged_in = False
        unscanned_filesystems = False
        untried_credentials = False
        root_login = False
        machine_root_login = False
        machine_logged_in = False
        uninstalled_tools = False
        machine_w_tools = False
        uninstalled_backdoor = False
        target_untried_credentials = False

        for m in env_state.attacker_obs_state.machines:
            if m.logged_in:
                logged_in = True
                if not m.filesystem_searched:
                    unscanned_filesystems = True
                if m.root:
                    root_login = True
                    if not m.tools_installed and not m.install_tools_tried:
                        uninstalled_tools = True
                    else:
                        machine_w_tools = True
                    if m.tools_installed and not m.backdoor_installed and not m.backdoor_tried:
                        uninstalled_backdoor = True
            if m.ips == ip:
                machine_discovered = True
                target_machine = m
                if m.logged_in:
                    machine_logged_in = True
                    if m.root:
                        machine_root_login = True
                if m.untried_credentials:
                    target_untried_credentials = m.untried_credentials
            # if m.shell_access and not m.logged_in:
            #     untried_credentials = True
            if m.untried_credentials:
                untried_credentials = m.untried_credentials

        if action.index == -1 or action.id == EmulationAttackerActionId.NETWORK_SERVICE_LOGIN:
            machine_discovered = True

        # Privilege escalation only legal if machine discovered and logged in and not root
        if (action.type == EmulationAttackerActionType.PRIVILEGE_ESCALATION and
                (not machine_discovered or not machine_logged_in or machine_root_login)):
            return False

        # Exploit only legal if we have not already compromised the node
        if action.type == EmulationAttackerActionType.EXPLOIT and machine_logged_in and root_login:
            return False

        # Shell-access Exploit only legal if we do not already have untried credentials
        if (action.type == EmulationAttackerActionType.EXPLOIT
                and action.action_outcome == EmulationAttackerActionOutcome.SHELL_ACCESS
                and target_untried_credentials):
            return False

        # Priv-Esc Exploit only legal if we are already logged in and do not have root
        if action.type == EmulationAttackerActionType.EXPLOIT \
                and action.action_outcome == EmulationAttackerActionOutcome.PRIVILEGE_ESCALATION_ROOT \
                and (not machine_logged_in or root_login):
            return False

        # If IP is discovered, then IP specific action without other prerequisites is legal
        if (machine_discovered and (action.type == EmulationAttackerActionType.RECON or
                                    action.type == EmulationAttackerActionType.EXPLOIT or
                                    action.type == EmulationAttackerActionType.PRIVILEGE_ESCALATION)):
            if action.index == -1 and target_machine is None:
                return True
            else:
                exploit_tried = env_state.attacker_obs_state.exploit_tried(a=action, m=target_machine)
            if exploit_tried:
                return False
            return True

        # If nothing new to scan, find-flag is illegal
        if action.id == EmulationAttackerActionId.FIND_FLAG and not unscanned_filesystems:
            return False

        # If nothing new to backdoor, install backdoor is illegal
        if action.id == EmulationAttackerActionId.SSH_BACKDOOR and not uninstalled_backdoor:
            return False

        # If no new credentials, login to service is illegal
        if action.id == EmulationAttackerActionId.NETWORK_SERVICE_LOGIN and not untried_credentials:
            return False

        # Pivot recon possible if logged in on pivot machine with tools installed
        if (machine_discovered and action.type == EmulationAttackerActionType.POST_EXPLOIT and
                logged_in and machine_w_tools):
            return True

        # If IP is discovered, and credentials are found and shell access, then post-exploit actions are legal
        if machine_discovered and action.type == EmulationAttackerActionType.POST_EXPLOIT \
                and ((target_machine is not None and target_machine.shell_access
                      and len(target_machine.shell_access_credentials) > 0)
                     or action.index == -1 or action.id == EmulationAttackerActionId.NETWORK_SERVICE_LOGIN):
            return True

        # Bash action not tied to specific IP only possible when having shell access and being logged in
        if action.id == EmulationAttackerActionId.FIND_FLAG and logged_in and unscanned_filesystems:
            return True

        # Bash action not tied to specific IP only possible when having shell access and being logged in and root
        if action.id == EmulationAttackerActionId.INSTALL_TOOLS and logged_in and root_login and uninstalled_tools:
            return True

        # Bash action not tied to specific IP only possible when having shell access and being logged in and root
        if action.id == EmulationAttackerActionId.SSH_BACKDOOR and logged_in and root_login \
                and machine_w_tools and uninstalled_backdoor:
            return True

        return False

    @staticmethod
    def check_pid(pid: int) -> bool:
        """
        Check if a given pid is running on the host

        :param pid: the pid to check
        :return: True if it is running otherwise false.
        """
        try:
            return psutil.Process(pid).is_running()
        except Exception:
            return False
