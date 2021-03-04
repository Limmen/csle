from typing import Tuple, List
import time
import paramiko
from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.dao.action.action import Action
import gym_pycr_pwcrack.constants.constants as constants
from gym_pycr_pwcrack.dao.observation.connection_observation_state import ConnectionObservationState
from gym_pycr_pwcrack.dao.action_results.ids_alert import IdsAlert


class ClusterUtil:
    """
    Class containing utility functions for the cluster-middleware
    """

    @staticmethod
    def execute_ssh_cmd(cmd: str, conn) -> Tuple[bytes, bytes, float]:
        """
        Executes an action on the cluster over a ssh connection,
        this is a synchronous operation that waits for the completion of the action before returning

        :param cmd: the command to execute
        :param conn: the ssh connection
        :return: outdata, errdata, total_time
        """
        transport_conn = conn.get_transport()
        session = transport_conn.open_session()
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
            if session.exit_status_ready():
                break
        end = time.time()
        total_time = end - start
        return outdata, errdata, total_time

    @staticmethod
    def write_estimated_cost(total_time, action: Action, env_config: EnvConfig, ip: str = None,
                             user: str = None, service: str = None, conn=None, dir: str = None,
                             machine_ip: str = None) -> None:
        """
        Caches the estimated cost of an action by writing it to a file

        :param total_time: the total time of executing the action
        :param action: the action
        :param env_config: the environment config
        :param ip: ip
        :param user: user
        :param service: service
        :param conn: conn
        :param dir: dir
        :param machine_ip: machine_ip
        :return: None
        """
        if conn is None:
            conn = env_config.cluster_config.agent_conn
        if dir is None or dir == "":
            dir = env_config.nmap_cache_dir

        sftp_client = conn.open_sftp()
        file_name = dir + str(action.id.value) + "_" + str(action.index)
        if not action.subnet and action.ip is not None:
            file_name = file_name + "_" + action.ip
        elif ip is not None:
            file_name = file_name + "_" + ip
        if service is not None:
            file_name = file_name + "_" + service
        if user is not None:
            file_name = file_name + "_" + user
        if machine_ip is not None:
            file_name = file_name + "_" + machine_ip
        file_name = file_name + constants.FILE_PATTERNS.COST_FILE_SUFFIX
        remote_file = sftp_client.file(file_name, mode="w")
        try:
            remote_file.write(str(round(total_time, 1)) + "\n")
        except Exception as e:
            print("exception writing cost file:{}".format(str(e)))
        finally:
            remote_file.close()

    @staticmethod
    def write_alerts_response(sum_priorities, num_alerts, action: Action, env_config: EnvConfig, ip: str = None,
                              user: str = None, service: str = None, conn=None, dir: str = None,
                              machine_ip: str = None) -> None:
        """
        Caches the number of triggered IDS alerts of an action by writing it to a file

        :param sum_priorities: the sum of the "priority" field of the alerts
        :param num_alerts: the number of different alerts that were triggered
        :param action: the action
        :param env_config: the environment config
        :param ip: ip
        :param user: user
        :param service: service
        :param conn: conn
        :param dir: dir
        :param machine_ip: machine_ip
        :return: None
        """
        if conn is None:
            conn = env_config.cluster_config.agent_conn
        if dir is None or dir == "":
            dir = env_config.nmap_cache_dir

        sftp_client = conn.open_sftp()
        file_name = dir + str(action.id.value) + "_" + str(action.index)
        if not action.subnet and action.ip is not None:
            file_name = file_name + "_" + action.ip
        elif ip is not None:
            file_name = file_name + "_" + ip
        if service is not None:
            file_name = file_name + "_" + service
        if user is not None:
            file_name = file_name + "_" + user
        if machine_ip is not None:
            file_name = file_name + "_" + machine_ip
        file_name = file_name + constants.FILE_PATTERNS.ALERTS_FILE_SUFFIX
        remote_file = sftp_client.file(file_name, mode="w")
        try:
            remote_file.write(str(sum_priorities) + "," + str(num_alerts) + "\n")
        except Exception as e:
            print("exception writing alerts file:{}".format(str(e)))
        finally:
            remote_file.close()

    @staticmethod
    def write_file_system_scan_cache(action: Action, env_config: EnvConfig, service: str, user: str, files: List[str],
                                     ip: str) \
            -> None:
        """
        Caches the result of a file system scan
        :param action: the action
        :param env_config: the env config
        :param service: the service used to connect to the file system
        :param user: the user
        :param files: the result to cache
        :param ip: the ip
        :return: None
        """
        sftp_client = env_config.cluster_config.agent_conn.open_sftp()
        file_name = env_config.nmap_cache_dir + str(action.id.value) + "_" + str(
            action.index) + "_" + ip + "_" + service \
                    + "_" + user + ".txt"
        remote_file = sftp_client.file(file_name, mode="a")
        try:
            for file in files:
                remote_file.write(file + "\n")
        except Exception as e:
            print("exception writing cache:{}".format(str(e)))
        finally:
            remote_file.close()

    @staticmethod
    def write_user_command_cache(action: Action, env_config: EnvConfig, user: str, result: str,
                                 ip: str) \
            -> None:
        """
        Caches the result of a user command action

        :param action: the action
        :param env_config: the env config
        :param user: the user
        :param result: the result to cache
        :param ip: the ip
        :return: None
        """
        sftp_client = env_config.cluster_config.agent_conn.open_sftp()
        file_name = env_config.nmap_cache_dir + str(action.id.value) + "_" + str(
            action.index) + "_" + ip + \
                    "_" + user + ".txt"
        print("writing cache file:{}".format(file_name))
        remote_file = sftp_client.file(file_name, mode="w")
        try:
            remote_file.write(result)
        finally:
            remote_file.close()

    @staticmethod
    def execute_cmd_interactive(a: Action, env_config: EnvConfig) -> None:
        """
        Executes an action on the cluster using an interactive shell (non synchronous)

        :param a: action to execute
        :param env_config: environment config
        :return: None
        """
        ClusterUtil.execute_cmd_interactive_channel(cmd=a.cmd[0], channel=env_config.cluster_config.agent_channel)
        env_config.cluster_config.agent_channel.send(a.cmd[0] + "\n")

    @staticmethod
    def execute_cmd_interactive_channel(cmd: str, channel) -> None:
        """
        Executes an action on the cluster using an interactive shell (non synchronous)

        :param a: action to execute
        :param env_config: environment config
        :param channel: the channel to use
        :return: None
        """
        channel.send(cmd + "\n")

    @staticmethod
    def read_result_interactive(env_config: EnvConfig) -> str:
        """
        Reads the result of an action executed in interactive mode

        :param env_config: the environment config
        :return: the result
        """
        return ClusterUtil.read_result_interactive_channel(env_config=env_config, channel=env_config.cluster_config.agent_channel)

    @staticmethod
    def read_result_interactive_channel(env_config: EnvConfig, channel) -> str:
        """
        Reads the result of an action executed in interactive mode

        :param env_config: the environment config
        :param channel: the channel to use
        :return: the result
        """
        while not channel.recv_ready():
             time.sleep(env_config.shell_read_wait)
        output = channel.recv(constants.COMMON.LARGE_RECV_SIZE)
        output_str = output.decode("utf-8")
        output_str = env_config.shell_escape.sub("", output_str)
        return output_str

    @staticmethod
    def check_filesystem_action_cache(a: Action, env_config: EnvConfig, ip: str, service: str, user: str):
        """
        Checks if a filesystem action is cached or not

        :param a: the action
        :param env_config: the environment configuration
        :return: None or the name of the file where the result is cached
        """
        query = str(a.id.value) + "_" + str(a.index) + "_" + ip + "_" + service + "_" + user + ".txt"

        # Search through cache
        if query in env_config.filesystem_file_cache:
            return query

        stdin, stdout, stderr = env_config.cluster_config.agent_conn.exec_command(constants.COMMANDS.LIST_CACHE
                                                                                  + env_config.nmap_cache_dir)
        cache_list = []
        for line in stdout:
            cache_list.append(line.replace("\n", ""))
        env_config.filesystem_file_cache = cache_list

        # Search through updated cache
        if query in env_config.filesystem_file_cache:
            return query

        env_config.cache_misses += 1

        return None

    @staticmethod
    def check_user_action_cache(a: Action, env_config: EnvConfig, ip: str, user: str):
        """
        Checks if a user-specific action is cached or not

        :param a: the action
        :param env_config: the environment configuration
        :return: None or the name of the file where the result is cached
        """
        query = str(a.id.value) + "_" + str(a.index) + "_" + ip + "_" + user + ".txt"

        # Search through cache
        if query in env_config.user_command_cache_files_cache:
            return query

        stdin, stdout, stderr = env_config.cluster_config.agent_conn.exec_command(constants.COMMANDS.LIST_CACHE
                                                                                  + env_config.nmap_cache_dir)
        cache_list = []
        for line in stdout:
            cache_list.append(line.replace("\n", ""))
        env_config.user_command_cache_files_cache = cache_list

        # Search through updated cache
        if query in env_config.user_command_cache_files_cache:
            return query

        env_config.cache_misses += 1

        return None

    @staticmethod
    def parse_file_scan_file(file_name: str, env_config: EnvConfig) -> List[str]:
        """
        Parses a file containing cached results of a file scan on a server

        :param file_name: name of the file to parse
        :param env_config: environment config
        :return: a list of files
        """
        sftp_client = env_config.cluster_config.agent_conn.open_sftp()
        remote_file = sftp_client.open(env_config.nmap_cache_dir + file_name)
        files = []
        try:
            data = remote_file.read()
            data = data.decode()
            files = data.split("\n")
        finally:
            remote_file.close()
        return files

    @staticmethod
    def parse_user_command_file(file_name: str, env_config: EnvConfig, conn) -> List[str]:
        """
        Parses a file containing cached results of a user command file on a server

        :param file_name: name of the file to parse
        :param env_config: environment config
        :return: a list of files
        """
        sftp_client = conn.open_sftp()
        remote_file = sftp_client.open(env_config.nmap_cache_dir + file_name)
        result = "0"
        try:
            data = remote_file.read()
            result = data.decode()
        finally:
            remote_file.close()
        return result

    @staticmethod
    def delete_cache_file(file_name: str, env_config: EnvConfig) -> Tuple[bytes, bytes, float]:
        """
        Deletes the file that contains the cached result of some operation

        :param file_name: name of the file to delete
        :param env_config: the environment config
        :return: outdata, errdata, total_time
        """
        cmd = "rm -f " + env_config.nmap_cache_dir + file_name
        return ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=env_config.cluster_config.agent_conn)

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
            outdata, errdata, total_time = ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=conn)
            return "is running" in outdata.decode() or "is running" in errdata.decode()
        else:
            cmd = cmd + "\n"
            conn.write(cmd.encode())
            response = conn.read_until(constants.TELNET.PROMPT, timeout=5)
            return "is running" in response.decode()

    @staticmethod
    def _list_all_users(c: ConnectionObservationState, env_config: EnvConfig, telnet: bool = False) \
            -> List:
        """
        List all users on a machine

        :param c: the connection to user for the command
        :param telnet: whether it is a telnet connection
        :param env_config: env config
        :return: list of users
        """
        cache_id = ("list_users", c.ip, c.root)
        cache_file_name = "list_users_" + c.ip + "_" + str(c.root)

        # check in-memory cache
        if env_config.filesystem_scan_cache.get(cache_id) is not None:
            return env_config.filesystem_scan_cache.get(cache_id)

        if not telnet:
            # check file cache
            sftp_client = c.conn.open_sftp()
            cwd = "/home/" + c.username + "/"
            remote_file = None
            try:
                remote_file = sftp_client.open(cwd + cache_file_name, mode="r")
                users = []
                data = remote_file.read()
                data = data.decode()
                users = data.split("\n")
                users = list(filter(lambda x: x != '', users))
                if len(users) > 0:
                    # cache result
                    env_config.filesystem_scan_cache.add(cache_id, users)
                    return users
            except Exception as e:
                pass
            finally:
                if remote_file is not None:
                    remote_file.close()

        cmd = constants.SHELL.LIST_ALL_USERS
        for i in range(env_config.retry_find_users):
            if not telnet:
                outdata, errdata, total_time = ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=c.conn)
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

        backdoor_exists = False
        for user in users:
            if constants.SSH_BACKDOOR.BACKDOOR_PREFIX in user:
                backdoor_exists = True

        if backdoor_exists:
            # cache result in-memory
            env_config.filesystem_scan_cache.add(cache_id, users)

        if not telnet and backdoor_exists:
            # cache result on-disk
            sftp_client = c.conn.open_sftp()
            remote_file = None
            try:
                remote_file = sftp_client.file(cwd + cache_file_name, mode="a")
                for user in users:
                    remote_file.write(user + "\n")
            except Exception as e:
                print(
                    "Error writing list of users cache: {}, file:{}, ip:{}".format(str(e), cwd + cache_file_name, c.ip))
            finally:
                if remote_file is not None:
                    remote_file.close()
        return users

    @staticmethod
    def get_latest_alert_ts(env_config: EnvConfig) -> float:
        """
        Gets the latest timestamp in the snort alerts log

        :param env_config: the environment config
        :return: the latest timestamp
        """
        if not env_config.ids_router:
            raise AssertionError("Can only read alert files if IDS router is enabled")
        stdin, stdout, stderr = env_config.cluster_config.router_conn.exec_command(
            constants.IDS_ROUTER.TAIL_ALERTS_LATEST_COMMAND + " " + constants.IDS_ROUTER.ALERTS_FILE)
        alerts = []
        for line in stdout:
            a_str = line.replace("\n", "")
            alerts.append(IdsAlert.parse_from_str(a_str))
        if len(alerts) == 0:
            # retry once
            stdin, stdout, stderr = env_config.cluster_config.router_conn.exec_command(
                constants.IDS_ROUTER.TAIL_ALERTS_LATEST_COMMAND + " " + constants.IDS_ROUTER.ALERTS_FILE)
            alerts = []
            for line in stdout:
                a_str = line.replace("\n", "")
                alerts.append(IdsAlert.parse_from_str(a_str))
            if len(alerts) == 0:
                return None
            else:
                return alerts[0].timestamp
        else:
            return alerts[0].timestamp

    @staticmethod
    def check_ids_alerts(env_config: EnvConfig) -> List[IdsAlert]:
        """
        Reads alerts from the IDS alerts log

        :param env_config: the environment config
        :return: a list of alerts
        """
        if not env_config.ids_router:
            raise AssertionError("Can only read alert files if IDS router is enabled")
        stdin, stdout, stderr = env_config.cluster_config.router_conn.exec_command(
            constants.IDS_ROUTER.TAIL_ALERTS_COMMAND + " " + constants.IDS_ROUTER.ALERTS_FILE)
        alerts = []
        for line in stdout:
            a_str = line.replace("\n", "")
            alerts.append(IdsAlert.parse_from_str(a_str))
        return alerts

    @staticmethod
    def check_ids_fast_log(env_config: EnvConfig) -> List[IdsAlert]:
        """
        Reads alerts from the IDS fast-log

        :param env_config: the environment config
        :return: a list of alerts
        """
        if not env_config.ids_router:
            raise AssertionError("Can only read alert files if IDS router is enabled")
        stdin, stdout, stderr = env_config.cluster_config.router_conn.exec_command(
            constants.IDS_ROUTER.TAIL_FAST_LOG_COMMAND + " " + constants.IDS_ROUTER.FAST_LOG_FILE)
        fast_logs = []
        for line in stdout:
            a_str = line.replace("\n", "")
            priority, ts = IdsAlert.fast_log_parse(a_str)
            fast_logs.append((priority, ts))
        return fast_logs

    @staticmethod
    def setup_custom_connection(user: str, pw: str, source_ip: str, port: int, target_ip: str, proxy_conn,
                                root: bool) \
            -> ConnectionObservationState:
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