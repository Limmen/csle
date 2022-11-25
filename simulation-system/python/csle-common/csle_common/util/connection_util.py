from typing import Tuple, List
import time
import paramiko
import telnetlib
from ftplib import FTP
import csle_common.constants.constants as constants
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.util.env_dynamics_util import EnvDynamicsUtil
from csle_common.dao.emulation_observation.common.emulation_connection_observation_state \
    import EmulationConnectionObservationState
from csle_common.dao.emulation_observation.attacker.emulation_attacker_machine_observation_state \
    import EmulationAttackerMachineObservationState
from csle_common.tunneling.forward_tunnel_thread import ForwardTunnelThread
from csle_common.dao.emulation_config.credential import Credential
from csle_common.util.emulation_util import EmulationUtil
from csle_common.dao.emulation_config.connection_setup_dto import ConnectionSetupDTO
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_common.logging.log import Logger


class ConnectionUtil:
    """
    Class containing utility functions for the connection-related functionality to the emulation
    """

    @staticmethod
    def login_service_helper(s: EmulationEnvState, a: EmulationAttackerAction, alive_check,
                             service_name: str) -> Tuple[EmulationEnvState, bool]:
        """
        Helper function for logging in to a network service in the emulation

        :param s: the current state
        :param a: the action of the login
        :param alive_check:  the function to check whether current connections are alive or not
        :param service_name: name of the service to login to
        :return: s_prime, new connection (bool)
        """
        total_cost = 0
        target_machine = None
        non_used_credentials = []
        root = False
        non_failed_credentials = []
        for m in s.attacker_obs_state.machines:
            if m.ips == a.ips:
                target_machine = m
                target_machine = target_machine.copy()
                break

        # Check if already logged in
        if target_machine is not None:
            alive_connections = []
            root = False
            connected = False
            connections = []
            if service_name == constants.TELNET.SERVICE_NAME:
                connections = target_machine.telnet_connections
            elif service_name == constants.SSH.SERVICE_NAME:
                connections = target_machine.ssh_connections
            elif service_name == constants.FTP.SERVICE_NAME:
                connections = target_machine.ftp_connections
            for c in connections:
                if alive_check(c.conn):
                    connected = True
                    alive_connections.append(c)
                    if c.root:
                        root = c.root
                else:
                    if c.tunnel_thread is not None:
                        # stop the tunnel thread that does port forwarding
                        c.tunnel_thread.forward_server.shutdown()
            if len(target_machine.logged_in_services) == 1 and target_machine.logged_in_services[0] == service_name:
                target_machine.logged_in = connected
            if len(target_machine.root_services) == 1 and target_machine.root_services[0] == service_name:
                target_machine.root = root
            if not connected and service_name in target_machine.logged_in_services:
                target_machine.logged_in_services.remove(service_name)
            if not root and service_name in target_machine.root_services:
                target_machine.root_services.remove(service_name)
            non_used_credentials = []
            root = False
            for cr in target_machine.shell_access_credentials:
                if cr.service == service_name:
                    already_logged_in = False
                    for c in alive_connections:
                        if not root and c.root:
                            root = True
                        if c.credential.username == cr.username:
                            already_logged_in = True
                    if not already_logged_in:
                        non_used_credentials.append(cr)

            if service_name == constants.TELNET.SERVICE_NAME:
                target_machine.telnet_connections = alive_connections
            elif service_name == constants.SSH.SERVICE_NAME:
                target_machine.ssh_connections = alive_connections
            elif service_name == constants.FTP.SERVICE_NAME:
                target_machine.ftp_connections = alive_connections

        # Check cached connections
        non_used_nor_cached_credentials = []
        for cr in non_used_credentials:
            if cr.service == constants.SSH.SERVICE_NAME:
                for ip in target_machine.ips:
                    key = (ip, cr.username, cr.port)
                    if key in s.attacker_cached_ssh_connections:
                        c = s.attacker_cached_ssh_connections[key]
                        target_machine.ssh_connections.append(c)
                        target_machine.logged_in = True
                        target_machine.root = c.root
                        if cr.service not in target_machine.logged_in_services:
                            target_machine.logged_in_services.append(cr.service)
                        if cr.service not in target_machine.root_services:
                            target_machine.root_services.append(cr.service)
                        break
                    else:
                        non_used_nor_cached_credentials.append(cr)
            elif cr.service == constants.TELNET.SERVICE_NAME:
                for ip in target_machine.ips:
                    key = (ip, cr.username, cr.port)
                    if key in s.attacker_cached_telnet_connections:
                        c = s.attacker_cached_telnet_connections[key]
                        target_machine.telnet_connections.append(c)
                        target_machine.logged_in = True
                        target_machine.root = c.root
                        if cr.service not in target_machine.logged_in_services:
                            target_machine.logged_in_services.append(cr.service)
                        if cr.service not in target_machine.root_services:
                            target_machine.root_services.append(cr.service)
                        break
                    else:
                        non_used_nor_cached_credentials.append(cr)
            elif cr.service == constants.FTP.SERVICE_NAME:
                for ip in target_machine.ips:
                    key = (ip, cr.username, cr.port)
                    if key in s.attacker_cached_ftp_connections:
                        c = s.attacker_cached_ftp_connections[key]
                        target_machine.ftp_connections.append(c)
                        target_machine.logged_in = True
                        target_machine.root = c.root
                        if cr.service not in target_machine.logged_in_services:
                            target_machine.logged_in_services.append(cr.service)
                        if cr.service not in target_machine.root_services:
                            target_machine.root_services.append(cr.service)
                        break
                    else:
                        non_used_nor_cached_credentials.append(cr)

        if target_machine is None or root or len(non_used_nor_cached_credentials) == 0:
            s_prime = s
            if target_machine is not None:
                attacker_machine_observations = EnvDynamicsUtil.merge_new_obs_with_old(
                    s.attacker_obs_state.machines, [target_machine],
                    emulation_env_config=s.emulation_env_config, action=a)
                s_prime.attacker_obs_state.machines = attacker_machine_observations

            return s_prime, False

        # If not logged in and there are credentials, setup a new connection
        agent_cr = Credential(
            username=constants.AGENT.USER, pw=constants.AGENT.PW, root=True,
            protocol=TransportProtocol.TCP, service=constants.SSH.SERVICE_NAME, port=constants.SSH.DEFAULT_PORT)
        proxy_connections = [EmulationConnectionObservationState(
            conn=s.emulation_env_config.get_hacker_connection(), credential=agent_cr,
            root=True, port=22, service=constants.SSH.SERVICE_NAME, proxy=None,
            ip=s.emulation_env_config.containers_config.agent_ip)]
        for m in s.attacker_obs_state.machines:
            ssh_connections_sorted_by_root = sorted(
                m.ssh_connections,
                key=lambda x: (constants.SSH_BACKDOOR.BACKDOOR_PREFIX in x.credential.username, x.root,
                               x.credential.username),
                reverse=True)
            if len(ssh_connections_sorted_by_root) > 0:
                proxy_connections.append(ssh_connections_sorted_by_root[0])

        connection_setup_dto = ConnectionSetupDTO()
        if service_name == constants.SSH.SERVICE_NAME:
            connection_setup_dto = ConnectionUtil._ssh_setup_connection(
                a=a,
                credentials=non_used_nor_cached_credentials,
                proxy_connections=proxy_connections, s=s)
        elif service_name == constants.TELNET.SERVICE_NAME:
            connection_setup_dto = ConnectionUtil._telnet_setup_connection(
                a=a,
                credentials=non_used_nor_cached_credentials,
                proxy_connections=proxy_connections, s=s)
        elif service_name == constants.FTP.SERVICE_NAME:
            connection_setup_dto = ConnectionUtil._ftp_setup_connection(
                a=a,
                credentials=non_used_nor_cached_credentials,
                proxy_connections=proxy_connections, s=s)

        s_prime = s
        if len(connection_setup_dto.non_failed_credentials) > 0:
            total_cost += connection_setup_dto.total_time
            if connection_setup_dto.connected:
                root = False
                target_machine.logged_in = True
                target_machine.shell_access_credentials = non_failed_credentials
                if service_name not in target_machine.logged_in_services:
                    target_machine.logged_in_services.append(service_name)
                if service_name not in target_machine.root_services:
                    target_machine.root_services.append(service_name)
                for i in range(len(connection_setup_dto.target_connections)):
                    # Check if root
                    c_root = False
                    cost = 0.0
                    if service_name == constants.SSH.SERVICE_NAME:
                        c_root, cost = ConnectionUtil._ssh_finalize_connection(
                            target_machine=target_machine, i=i,
                            connection_setup_dto=connection_setup_dto)
                    elif service_name == constants.TELNET.SERVICE_NAME:
                        c_root, cost = ConnectionUtil._telnet_finalize_connection(
                            target_machine=target_machine, i=i,
                            connection_setup_dto=connection_setup_dto)
                    elif service_name == constants.FTP.SERVICE_NAME:
                        c_root, cost = ConnectionUtil._ftp_finalize_connection(
                            target_machine=target_machine, i=i, connection_setup_dto=connection_setup_dto)
                    total_cost += cost
                    if c_root:
                        root = True
            target_machine.root = root
            attacker_machine_observations = EnvDynamicsUtil.merge_new_obs_with_old(
                s.attacker_obs_state.machines, [target_machine],
                emulation_env_config=s.emulation_env_config, action=a)
            s_prime.attacker_obs_state.machines = attacker_machine_observations
        else:
            target_machine.shell_access = False
            target_machine.shell_access_credentials = []

        return s_prime, False

    @staticmethod
    def _ssh_setup_connection(a: EmulationAttackerAction,
                              credentials: List[Credential],
                              proxy_connections: List[EmulationConnectionObservationState],
                              s: EmulationEnvState) -> ConnectionSetupDTO:
        """
        Helper function for setting up a SSH connection

        :param a: the action of the connection
        :param emulation_env_config: the emulation environment config
        :param credentials: list of credentials to try
        :param proxy_connections: list of proxy connections to try
        :param s: env state
        :return: a DTO with connection setup information
        """
        connection_setup_dto = ConnectionSetupDTO()
        start = time.time()
        for proxy_conn in proxy_connections:
            if proxy_conn.ip != s.emulation_env_config.containers_config.agent_ip:
                m = s.get_attacker_machine(proxy_conn.ip)
                if m is None or not a.ips_match(list(m.reachable)) or m.ips_match(a.ips):
                    continue
            else:
                if not a.ips_match(s.attacker_obs_state.agent_reachable):
                    continue
            for cr in credentials:
                for ip in a.ips:
                    if cr.service == constants.SSH.SERVICE_NAME:
                        try:
                            agent_addr = (proxy_conn.ip, cr.port)
                            target_addr = (ip, cr.port)
                            agent_transport = proxy_conn.conn.get_transport()
                            relay_channel = agent_transport.open_channel(constants.SSH.DIRECT_CHANNEL, target_addr,
                                                                         agent_addr)
                            target_conn = paramiko.SSHClient()
                            target_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            target_conn.connect(ip, username=cr.username, password=cr.pw, sock=relay_channel)
                            target_conn.get_transport().set_keepalive(5)
                            connection_setup_dto.connected = True
                            connection_setup_dto.credentials.append(cr)
                            connection_setup_dto.target_connections.append(target_conn)
                            connection_setup_dto.proxies.append(proxy_conn)
                            connection_setup_dto.ports.append(cr.port)
                            connection_setup_dto.non_failed_credentials.append(cr)
                            connection_setup_dto.ip = ip
                            break
                        except Exception as e:
                            Logger.__call__().get_logger().warning("SSH exception :{}".format(str(e)))
                            Logger.__call__().get_logger().warning("user:{}, pw:{}".format(cr.username, cr.pw))
                            Logger.__call__().get_logger().warning("Agent reachable:{}".format(
                                s.attacker_obs_state.agent_reachable))
                            Logger.__call__().get_logger().warning("Action:{}, {}, {}".format(a.id, a.ips, a.descr))
                    else:
                        connection_setup_dto.non_failed_credentials.append(cr)
            if connection_setup_dto.connected:
                break
        end = time.time()
        connection_setup_dto.total_time = end - start
        return connection_setup_dto

    @staticmethod
    def _ssh_finalize_connection(target_machine: EmulationAttackerMachineObservationState,
                                 connection_setup_dto: ConnectionSetupDTO, i: int) -> Tuple[bool, float]:
        """
        Helper function for finalizing a SSH connection and setting up the DTO

        :param target_machine: the target machine to connect to
        :param i: current index
        :param connection_setup_dto: DTO with connection setup information
        :return: boolean whether the connection has root privileges or not, cost
        """
        start = time.time()
        root = False
        for j in range(constants.ENV_CONSTANTS.ATTACKER_RETRY_CHECK_ROOT):
            outdata, errdata, total_time = EmulationUtil.execute_ssh_cmd(
                cmd="sudo -l", conn=connection_setup_dto.target_connections[i])
            root = False
            if f"{connection_setup_dto.credentials[i].username} may not run sudo" not in errdata.decode("utf-8") \
                    and ("(ALL) NOPASSWD: ALL" in outdata.decode("utf-8") or
                         "(ALL : ALL) ALL" in outdata.decode("utf-8")):
                root = True
                target_machine.root = True
                break
            else:
                time.sleep(constants.ENV_CONSTANTS.SLEEP_RETRY)
        connection_dto = EmulationConnectionObservationState(conn=connection_setup_dto.target_connections[i],
                                                             credential=connection_setup_dto.credentials[i],
                                                             root=root,
                                                             service=constants.SSH.SERVICE_NAME,
                                                             port=connection_setup_dto.ports[i],
                                                             proxy=connection_setup_dto.proxies[i],
                                                             ip=connection_setup_dto.ip)
        target_machine.ssh_connections.append(connection_dto)
        end = time.time()
        total_time = end - start
        return root, total_time

    @staticmethod
    def _telnet_setup_connection(a: EmulationAttackerAction,
                                 credentials: List[Credential], proxy_connections: List,
                                 s: EmulationEnvState) -> ConnectionSetupDTO:
        """
        Helper function for setting up a Telnet connection to a target machine

        :param a: the action of the connection
        :param credentials: list of credentials to try
        :param proxies: proxy connections
        :param s: env state
        :return: a DTO with the connection setup information
        """
        connection_setup_dto = ConnectionSetupDTO()
        start = time.time()
        for proxy_conn in proxy_connections:
            if proxy_conn.ip != s.emulation_env_config.containers_config.agent_ip:
                m = s.get_attacker_machine(proxy_conn.ip)
                if m is None or a.ips not in m.reachable or m.ips == a.ips:
                    continue
            else:
                if not a.ips_match(s.attacker_obs_state.agent_reachable):
                    continue
            for cr in credentials:
                for ip in a.ips:
                    if cr.service == constants.TELNET.SERVICE_NAME:
                        try:
                            forward_port = s.emulation_env_config.get_port_forward_port()
                            agent_transport = proxy_conn.conn.get_transport()
                            tunnel_thread = ForwardTunnelThread(local_port=forward_port,
                                                                remote_host=ip, remote_port=cr.port,
                                                                transport=agent_transport)
                            tunnel_thread.start()
                            target_conn = telnetlib.Telnet(host=constants.TELNET.LOCALHOST, port=forward_port,
                                                           timeout=3)
                            target_conn.read_until(constants.TELNET.LOGIN_PROMPT, timeout=3)
                            target_conn.write((cr.username + "\n").encode())
                            target_conn.read_until(constants.TELNET.PASSWORD_PROMPT, timeout=3)
                            target_conn.write((cr.pw + "\n").encode())
                            response = target_conn.read_until(constants.TELNET.PROMPT, timeout=3)
                            response = response.decode()
                            if constants.TELNET.INCORRECT_LOGIN not in response and response != "":
                                connection_setup_dto.connected = True
                                connection_setup_dto.credentials.append(cr)
                                connection_setup_dto.target_connections.append(target_conn)
                                connection_setup_dto.proxies.append(proxy_conn)
                                connection_setup_dto.tunnel_threads.append(tunnel_thread)
                                connection_setup_dto.forward_ports.append(forward_port)
                                connection_setup_dto.ports.append(cr.port)
                                connection_setup_dto.ip = ip
                            connection_setup_dto.non_failed_credentials.append(cr)
                            break
                        except Exception as e:
                            Logger.__call__().get_logger().warning(f"telnet exception:{str(e)}, {repr(e)}")
                            Logger.__call__().get_logger().warning(
                                f"Target ip in agent reachable: {s.attacker_obs_state.agent_reachable}")
                            Logger.__call__().get_logger().warning(
                                f"Agent reachable:{s.attacker_obs_state.agent_reachable}")
                    else:
                        connection_setup_dto.non_failed_credentials.append(cr)
                if connection_setup_dto.connected:
                    break
            if connection_setup_dto.connected:
                break
        end = time.time()
        connection_setup_dto.total_time = end - start
        return connection_setup_dto

    @staticmethod
    def _telnet_finalize_connection(target_machine: EmulationAttackerMachineObservationState, i: int,
                                    connection_setup_dto: ConnectionSetupDTO) -> Tuple[bool, float]:
        """
        Helper function for finalizing a Telnet connection to a target machine and creating the DTO

        :param target_machine: the target machine to connect to
        :param i: current index
        :param connection_setup_dto: DTO with information about the connection setup
        :return: boolean whether the connection has root privileges or not, cost
        """
        start = time.time()
        root = False
        for i in range(constants.ENV_CONSTANTS.ATTACKER_RETRY_CHECK_ROOT):
            connection_setup_dto.target_connections[i].write("sudo -l\n".encode())
            response = connection_setup_dto.target_connections[i].read_until(constants.TELNET.PROMPT, timeout=3)
            root = False
            if f"{connection_setup_dto.credentials[i].username} may not run sudo" not in response.decode("utf-8") \
                    and ("(ALL) NOPASSWD: ALL" in response.decode("utf-8") or
                         "(ALL : ALL) ALL" in response.decode("utf-8")):
                root = True
                break
            else:
                time.sleep(constants.ENV_CONSTANTS.SLEEP_RETRY)
        connection_dto = EmulationConnectionObservationState(conn=connection_setup_dto.target_connections[i],
                                                             credential=connection_setup_dto.credentials[i],
                                                             root=root,
                                                             service=constants.TELNET.SERVICE_NAME,
                                                             tunnel_thread=connection_setup_dto.tunnel_threads[i],
                                                             tunnel_port=connection_setup_dto.forward_ports[i],
                                                             port=connection_setup_dto.ports[i],
                                                             proxy=connection_setup_dto.proxies[i],
                                                             ip=connection_setup_dto.ip)
        target_machine.telnet_connections.append(connection_dto)
        end = time.time()
        total_time = end - start
        return root, total_time

    @staticmethod
    def _ftp_setup_connection(a: EmulationAttackerAction,
                              credentials: List[Credential], proxy_connections: List,
                              s: EmulationEnvState) -> ConnectionSetupDTO:
        """
        Helper function for setting up a FTP connection

        :param a: the action of the connection
        :param credentials: list of credentials to try
        :param proxy_connections: proxy connections
        :param env_state: env state
        :return: a DTO with connection setup information
        """
        connection_setup_dto = ConnectionSetupDTO()
        start = time.time()
        for proxy_conn in proxy_connections:
            if proxy_conn.ip != s.emulation_env_config.containers_config.agent_ip:
                m = s.get_attacker_machine(proxy_conn.ip)
                if m is None or a.ips not in m.reachable or m.ips == a.ips:
                    continue
            else:
                if not a.ips_match(s.attacker_obs_state.agent_reachable):
                    continue
            for cr in credentials:
                for ip in a.ips:
                    if cr.service == constants.FTP.SERVICE_NAME:
                        try:
                            forward_port = s.emulation_env_config.get_port_forward_port()
                            agent_transport = proxy_conn.conn.get_transport()
                            tunnel_thread = ForwardTunnelThread(local_port=forward_port,
                                                                remote_host=ip, remote_port=cr.port,
                                                                transport=agent_transport)
                            tunnel_thread.start()
                            target_conn = FTP()
                            target_conn.connect(host=constants.FTP.LOCALHOST, port=forward_port, timeout=5)
                            login_result = target_conn.login(cr.username, cr.pw)
                            if constants.FTP.INCORRECT_LOGIN not in login_result:
                                connection_setup_dto.connected = True
                                connection_setup_dto.credentials.append(cr)
                                connection_setup_dto.target_connections.append(target_conn)
                                connection_setup_dto.proxies.append(proxy_conn)
                                connection_setup_dto.tunnel_threads.append(tunnel_thread)
                                connection_setup_dto.forward_ports.append(forward_port)
                                connection_setup_dto.ports.append(cr.port)
                                connection_setup_dto.ip = ip
                                # Create LFTP connection too to be able to search file system
                                shell = proxy_conn.conn.invoke_shell()
                                # clear output
                                if shell.recv_ready():
                                    shell.recv(constants.COMMON.DEFAULT_RECV_SIZE)
                                shell.send(constants.FTP.LFTP_PREFIX + cr.username + ":" + cr.pw + "@" + ip + "\n")
                                time.sleep(0.5)
                                # clear output
                                if shell.recv_ready():
                                    shell.recv(constants.COMMON.DEFAULT_RECV_SIZE)
                                connection_setup_dto.interactive_shells.append(shell)
                                connection_setup_dto.non_failed_credentials.append(cr)
                                break
                        except Exception as e:
                            Logger.__call__().get_logger().warning(f"FTP exception: {str(e)}, {repr(e)}")
                            Logger.__call__().get_logger().warning(
                                f"Target ip in agent reacahble {a.ips_match(s.attacker_obs_state.agent_reachable)}")
                            Logger.__call__().get_logger().warning(f"Agent reachable: "
                                                                   f"{s.attacker_obs_state.agent_reachable}")
                    else:
                        connection_setup_dto.non_failed_credentials.append(cr)
                if connection_setup_dto.connected:
                    break
            if connection_setup_dto.connected:
                break
        end = time.time()
        connection_setup_dto.total_time = end - start
        return connection_setup_dto

    @staticmethod
    def _ftp_finalize_connection(target_machine: EmulationAttackerMachineObservationState, i: int,
                                 connection_setup_dto: ConnectionSetupDTO) -> Tuple[bool, float]:
        """
        Helper function for creating the connection DTO for FTP

        :param target_machine: the target machine to connect to
        :param users: list of users that are connected
        :param i: current index
        :param connection_setup_dto: DTO with information about the connection setup
        :return: boolean, whether the connection has root privileges, cost
        """
        root = False
        connection_dto = EmulationConnectionObservationState(
            conn=connection_setup_dto.target_connections[i], credential=connection_setup_dto.credentials[i],
            root=root,
            service=constants.FTP.SERVICE_NAME, tunnel_thread=connection_setup_dto.tunnel_threads[i],
            tunnel_port=connection_setup_dto.forward_ports[i], port=connection_setup_dto.ports[i],
            interactive_shell=connection_setup_dto.interactive_shells[i], ip=connection_setup_dto.ip,
            proxy=connection_setup_dto.proxies[i])
        target_machine.ftp_connections.append(connection_dto)
        return root, 0

    @staticmethod
    def find_jump_host_connection(ip, s: EmulationEnvState) -> EmulationConnectionObservationState:
        """
        Utility function for finding a jump-host from the set of compromised machines to reach a target IP

        :param ip: the ip to reach
        :param s: the current state
        :param emulation_env_config: the emulation environment configuration
        :return: a connection DTO
        """

        if ip in s.attacker_obs_state.agent_reachable:
            cr = Credential(
                username=constants.AGENT.USER, pw=constants.AGENT.PW, root=True,
                protocol=TransportProtocol.TCP, service=constants.SSH.SERVICE_NAME, port=constants.SSH.DEFAULT_PORT)
            c = EmulationConnectionObservationState(
                conn=s.emulation_env_config.get_hacker_connection(), credential=cr,
                root=True, port=constants.SSH.DEFAULT_PORT, service=constants.SSH.SERVICE_NAME,
                proxy=None, ip=s.emulation_env_config.containers_config.agent_ip)
            return c
        s.attacker_obs_state.sort_machines()

        for m in s.attacker_obs_state.machines:
            if m.logged_in and m.tools_installed and m.backdoor_installed and ip in m.reachable:

                # Start with ssh connections
                ssh_connections_sorted_by_root = sorted(
                    m.ssh_connections,
                    key=lambda x: (constants.SSH_BACKDOOR.BACKDOOR_PREFIX in x.credential.username, x.root,
                                   x.credential.username),
                    reverse=True)

                for c in ssh_connections_sorted_by_root:
                    alive = ConnectionUtil.test_connection(c)
                    if alive:
                        return c
        raise ValueError("No JumpHost found")

    @staticmethod
    def test_connection(c: EmulationConnectionObservationState) -> bool:
        """
        Utility function for testing if a connection is alive or not

        :param c: the connection to thest
        :return: True if the connection is alive, otherwise false
        """
        cmd = constants.AUXILLARY_COMMANDS.WHOAMI
        outdata, errdata, total_time = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=c.conn)
        if outdata is not None and outdata != "":
            return True
        else:
            return False

    @staticmethod
    def reconnect_ssh(c: EmulationConnectionObservationState) -> EmulationConnectionObservationState:
        """
        Reconnects the given SSH connection if it has died for some reason

        :param c: the connection to reconnect
        :return: the new connection
        """
        if c.proxy is None:
            c.conn = paramiko.SSHClient()
            c.conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            c.conn.connect(c.ip, username=c.credential.username, password=c.credential.pw)
            c.conn.get_transport().set_keepalive(5)
        else:
            proxy = c.proxy
            if proxy.conn.get_transport() is None or not proxy.conn.get_transport().is_active():
                proxy = ConnectionUtil.reconnect_ssh(c=proxy)

            agent_addr = (proxy.ip, c.credential.port)
            target_addr = (c.ip, c.credential.port)
            agent_transport = proxy.conn.get_transport()
            relay_channel = agent_transport.open_channel(constants.SSH.DIRECT_CHANNEL, target_addr,
                                                         agent_addr)
            c.conn = paramiko.SSHClient()
            c.conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            c.conn.connect(c.ip, username=c.credential.username, password=c.credential.pw, sock=relay_channel)
            c.conn.get_transport().set_keepalive(5)
            c.proxy = proxy
        return c

    @staticmethod
    def reconnect_telnet(c: EmulationConnectionObservationState, forward_port: int = 9000) \
            -> EmulationConnectionObservationState:
        """
        Reconnects the given Telnet connection if it has died for some reason

        :param c: the connection to reconnect
        :return: the new connection
        """
        if c.proxy.conn.get_transport() is None or not c.proxy.conn.get_transport().is_active():
            proxy = ConnectionUtil.reconnect_ssh(c=c.proxy)
            c.proxy = proxy
        for i in range(constants.ENV_CONSTANTS.NUM_RETRIES):
            try:
                agent_transport = c.proxy.conn.get_transport()
                tunnel_thread = ForwardTunnelThread(local_port=forward_port,
                                                    remote_host=c.ip, remote_port=constants.TELNET.DEFAULT_PORT,
                                                    transport=agent_transport)
                tunnel_thread.start()
                target_conn = telnetlib.Telnet(host=constants.TELNET.LOCALHOST, port=forward_port, timeout=3)
                target_conn.read_until(constants.TELNET.LOGIN_PROMPT, timeout=3)
                target_conn.write((c.credential.username + "\n").encode())
                target_conn.read_until(constants.TELNET.PASSWORD_PROMPT, timeout=3)
                target_conn.write((c.credential.pw + "\n").encode())
                response = target_conn.read_until(constants.TELNET.PROMPT, timeout=3)
                response = response.decode()
                if constants.TELNET.INCORRECT_LOGIN not in response and response != "":
                    c.conn = target_conn
            except Exception as e:
                Logger.__call__().get_logger().warning(f"telnet exception:{str(e)}, {repr(e)}")
        return c
