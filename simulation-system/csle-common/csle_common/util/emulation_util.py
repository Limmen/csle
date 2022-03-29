from typing import Tuple, List, Union
import time
import paramiko
import csle_collector.constants.constants as collector_constants
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.action.attacker.attacker_action import AttackerAction
from csle_common.dao.observation.common.connection_observation_state import ConnectionObservationState


class EmulationUtil:
    """
    Class containing utility functions for the emulation-middleware
    """

    @staticmethod
    def execute_ssh_cmds(cmds: List[str], conn, wait_for_completion :bool = True) -> List[Tuple[bytes, bytes, float]]:
        """
        Executes a list of commands over an ssh connection to the emulation

        :param cmds: the list of commands
        :param conn: the ssh connection
        :param wait_for_completion: whether to wait for completion of the commands or not
        :return: List of tuples (outdata, errdata, total_time)
        """
        results = []
        for cmd in cmds:
            res = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=conn, wait_for_completion=wait_for_completion)
            results.append(res)
        return results

    @staticmethod
    def execute_ssh_cmd(cmd: str, conn, wait_for_completion :bool = True) -> Tuple[bytes, bytes, float]:
        """
        Executes an action on the emulation over a ssh connection,
        this is a synchronous operation that waits for the completion of the action before returning

        :param cmd: the command to execute
        :param conn: the ssh connection
        :param wait_for_completion: boolean flag whether to wait for completion or not
        :return: outdata, errdata, total_time
        """
        transport_conn = conn.get_transport()
        try:
            session = transport_conn.open_session(timeout=60)
        except Exception:
            raise IOError("Connection timed out")
        start = time.time()
        session.exec_command(cmd)
        outdata, errdata = b'', b''
        # Wait for completion
        while True:
            # Reading from output streams
            while session.recv_ready():
                outdata += session.recv(1000)
            while session.recv_stderr_ready():
                errdata += session.recv_stderr(1000)

            # Check for completion
            if session.exit_status_ready() or not wait_for_completion:
                break
        end = time.time()
        total_time = end - start
        return outdata, errdata, total_time

    @staticmethod
    def log_measured_action_time(total_time, action: AttackerAction, emulation_env_config: EmulationEnvConfig) -> None:
        """
        Logs the measured time of an action to Kafka

        :param total_time: the total time of executing the action
        :param action: the action
        :param emulation_env_config: the environment config
        :param ip: ip
        :param user: user
        :param service: service
        :param conn: conn
        :param dir: dir
        :param machine_ips: machine_ips
        :return: None
        """
        ts = time.time()
        record = f"{ts},{action.id.value},{action.descr},{action.index},{action.name}," \
                 f"{total_time},{'_'.join(action.ips)},{'_'.join(action.cmds)}"
        emulation_env_config.producer.produce(collector_constants.LOG_SINK.ATTACKER_ACTIONS_TOPIC_NAME, record)
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
    def _list_all_users(c: ConnectionObservationState, emulation_env_config: EmulationEnvConfig,
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
            -> Union[ConnectionObservationState, None]:
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
        agent_addr = (source_ip, port)
        target_addr = (target_ip, port)
        agent_transport = proxy_conn.conn.get_transport()
        try:
            relay_channel = agent_transport.open_channel(constants.SSH.DIRECT_CHANNEL, target_addr, agent_addr,
                                                         timeout=3)
            target_conn = paramiko.SSHClient()
            target_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            target_conn.connect(target_ip, username=user, password=pw, sock=relay_channel,
                                timeout=3)
            connection_dto = ConnectionObservationState(conn=target_conn, username=user, root=root,
                                                        service=constants.SSH.SERVICE_NAME,
                                                        port=constants.SSH.DEFAULT_PORT,
                                                        proxy=proxy_conn, ip=target_ip)
            return connection_dto
        except Exception as e:
            print("Custom connection setup failed:{}".format(str(e)))
            return None


    @staticmethod
    def write_remote_file(conn, file_name : str, contents : str , write_mode : str ="w") -> None:
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
            print("exception writing file:{}".format(str(e)))
        finally:
            remote_file.close()


    @staticmethod
    def connect_admin(emulation_env_config: EmulationEnvConfig, ip: str) -> None:
        """
        Connects the admin agent

        :param emulation_env_config: the configuration of the emulation to connect to
        :param ip: the ip of the container to connect to
        :return: None
        """
        emulation_env_config.agent_ip = ip
        emulation_env_config.connect(ip=ip, username=constants.CSLE_ADMIN.USER, pw=constants.CSLE_ADMIN.PW)

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
