from typing import Tuple, List
import time
import paramiko
import telnetlib
from ftplib import FTP
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.action.attacker.attacker_action import AttackerAction
from gym_pycr_ctf.dao.network.env_state import EnvState
from gym_pycr_ctf.envs_model.logic.common.env_dynamics_util import EnvDynamicsUtil
import gym_pycr_ctf.constants.constants as constants
from gym_pycr_ctf.dao.observation.common.connection_observation_state import ConnectionObservationState
from gym_pycr_ctf.dao.observation.attacker.attacker_machine_observation_state import AttackerMachineObservationState
from gym_pycr_ctf.envs_model.logic.emulation.tunnel.forward_tunnel_thread import ForwardTunnelThread
from gym_pycr_ctf.dao.network.credential import Credential
from gym_pycr_ctf.envs_model.logic.emulation.util.common.emulation_util import EmulationUtil

class ConnectionUtil:
    """
    Class containing utility functions for the connection-related functionality to the emulation
    """

    @staticmethod
    def login_service_helper(s: EnvState, a: AttackerAction, alive_check, service_name: str,
                             env_config: EnvConfig) -> Tuple[EnvState, int, int, int, int, int, int, int,
                                                             int, float, bool]:
        """
        Helper function for logging in to a network service in the emulation

        :param s: the current state
        :param a: the action of the login
        :param alive_check:  the function to check whether current connections are alive or not
        :param service_name: name of the service to login to
        :param env_config: environment config
        :return: s_prime, total_new_ports, total_new_os, total_new_vuln, total_new_machines, \
                   total_new_shell_access, total_new_flag_pts, total_new_root, cost, new_conn, total_new_osvdb_found,
                   total_new_logged_in, total_new_tools_installed, total_new_backdoors_installed
        """
        total_new_ports, total_new_os, total_new_vuln, total_new_machines, total_new_shell_access, \
        total_new_root, total_new_flag_pts, total_new_osvdb_vuln_found, total_new_logged_in, \
        total_new_tools_installed, total_new_backdoors_installed = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        total_cost = 0
        target_machine = None
        non_used_credentials = []
        root = False
        for m in s.attacker_obs_state.machines:
            if m.ip == a.ip:
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
                        if c.username == cr.username:
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
                key = (target_machine.ip, cr.username, cr.port)
                if key in s.attacker_cached_ssh_connections:
                    c = s.attacker_cached_ssh_connections[key]
                    target_machine.ssh_connections.append(c)
                    target_machine.logged_in = True
                    target_machine.root = c.root
                    if cr.service not in target_machine.logged_in_services:
                        target_machine.logged_in_services.append(cr.service)
                    if cr.service not in target_machine.root_services:
                        target_machine.root_services.append(cr.service)
                else:
                    non_used_nor_cached_credentials.append(cr)
            elif cr.service == constants.TELNET.SERVICE_NAME:
                key = (target_machine.ip, cr.username, cr.port)
                if key in s.attacker_cached_telnet_connections:
                    c = s.attacker_cached_telnet_connections[key]
                    target_machine.telnet_connections.append(c)
                    target_machine.logged_in = True
                    target_machine.root = c.root
                    if cr.service not in target_machine.logged_in_services:
                        target_machine.logged_in_services.append(cr.service)
                    if cr.service not in target_machine.root_services:
                        target_machine.root_services.append(cr.service)
                else:
                    non_used_nor_cached_credentials.append(cr)
            elif cr.service == constants.FTP.SERVICE_NAME:
                key = (target_machine.ip, cr.username, cr.port)
                if key in s.attacker_cached_ftp_connections:
                    c = s.attacker_cached_ftp_connections[key]
                    target_machine.ftp_connections.append(c)
                    target_machine.logged_in = True
                    target_machine.root = c.root
                    if cr.service not in target_machine.logged_in_services:
                        target_machine.logged_in_services.append(cr.service)
                    if cr.service not in target_machine.root_services:
                        target_machine.root_services.append(cr.service)
                else:
                    non_used_nor_cached_credentials.append(cr)

        if target_machine is None or root or len(non_used_nor_cached_credentials) == 0:
            s_prime = s
            if target_machine is not None:
                new_machines_obs, total_new_ports, total_new_os, total_new_vuln, total_new_machines, \
                total_new_shell_access, total_new_flag_pts, total_new_root, total_new_osvdb_vuln_found, \
                total_new_logged_in, total_new_tools_installed, total_new_backdoors_installed = \
                    EnvDynamicsUtil.merge_new_obs_with_old(s.attacker_obs_state.machines, [target_machine],
                                                           env_config=env_config, action=a)
                s_prime.attacker_obs_state.machines = new_machines_obs

            return s_prime, total_new_ports, total_new_os, total_new_vuln, total_new_machines, \
                   total_new_shell_access, total_new_flag_pts, total_new_root, total_new_osvdb_vuln_found, \
                   total_new_logged_in, total_new_tools_installed, total_new_backdoors_installed, total_cost, False

        # If not logged in and there are credentials, setup a new connection
        connected = False
        users = []
        target_connections = []
        ports = []
        proxy_connections = [ConnectionObservationState(conn=env_config.emulation_config.agent_conn,
                                                        username=env_config.emulation_config.agent_username,
                                                        root=True, port=22, service=constants.SSH.SERVICE_NAME,
                                                        proxy=None, ip=env_config.emulation_config.agent_ip)]
        for m in s.attacker_obs_state.machines:
            ssh_connections_sorted_by_root = sorted(
                m.ssh_connections,
                key=lambda x: (constants.SSH_BACKDOOR.BACKDOOR_PREFIX in x.username, x.root, x.username),
                reverse=True)
            if len(ssh_connections_sorted_by_root) > 0:
                proxy_connections.append(ssh_connections_sorted_by_root[0])

        if service_name == constants.SSH.SERVICE_NAME:
            connected, users, target_connections, ports, cost, non_failed_credentials, proxies = ConnectionUtil._ssh_setup_connection(
                a=a, env_config=env_config, credentials=non_used_nor_cached_credentials,
                proxy_connections=proxy_connections, s=s)
        elif service_name == constants.TELNET.SERVICE_NAME:
            connected, users, target_connections, tunnel_threads, forward_ports, ports, cost, non_failed_credentials, \
            proxies = \
                ConnectionUtil._telnet_setup_connection(a=a, env_config=env_config,
                                                     credentials=non_used_nor_cached_credentials,
                                                     proxy_connections=proxy_connections, s=s)
        elif service_name == constants.FTP.SERVICE_NAME:
            connected, users, target_connections, tunnel_threads, forward_ports, ports, i_shells, \
            cost, non_failed_credentials, proxies = \
                ConnectionUtil._ftp_setup_connection(a=a, env_config=env_config,
                                                  credentials=non_used_nor_cached_credentials,
                                                  proxy_connections=proxy_connections,
                                                  s=s)

        s_prime = s
        if len(non_failed_credentials) > 0:
            total_cost += cost
            if connected:
                root = False
                target_machine.logged_in = True
                target_machine.shell_access_credentials = non_failed_credentials
                if service_name not in target_machine.logged_in_services:
                    target_machine.logged_in_services.append(service_name)
                if service_name not in target_machine.root_services:
                    target_machine.root_services.append(service_name)
                for i in range(len(target_connections)):
                    # Check if root
                    c_root = False
                    if service_name == constants.SSH.SERVICE_NAME:
                        c_root, cost = ConnectionUtil._ssh_finalize_connection(target_machine=target_machine, users=users,
                                                                            target_connections=target_connections, i=i,
                                                                            ports=ports, proxies=proxies,
                                                                            env_config=env_config)
                    elif service_name == constants.TELNET.SERVICE_NAME:
                        c_root, cost = ConnectionUtil._telnet_finalize_connection(target_machine=target_machine,
                                                                               users=users,
                                                                               target_connections=target_connections,
                                                                               i=i, tunnel_threads=tunnel_threads,
                                                                               forward_ports=forward_ports, ports=ports,
                                                                               proxies=proxies, env_config=env_config)
                    elif service_name == constants.FTP.SERVICE_NAME:
                        c_root, cost = ConnectionUtil._ftp_finalize_connection(target_machine=target_machine, users=users,
                                                                            target_connections=target_connections,
                                                                            i=i, tunnel_threads=tunnel_threads,
                                                                            forward_ports=forward_ports, ports=ports,
                                                                            interactive_shells=i_shells,
                                                                            proxies=proxies)
                    total_cost += cost
                    if c_root:
                        root = True
            target_machine.root = root
            new_machines_obs, total_new_ports_found, total_new_os_found, total_new_cve_vuln_found, total_new_machines, \
            total_new_shell_access, total_new_flag_pts, total_new_root, total_new_osvdb_vuln_found, \
            total_new_logged_in, total_new_tools_installed, total_new_backdoors_installed = \
                EnvDynamicsUtil.merge_new_obs_with_old(s.attacker_obs_state.machines, [target_machine], env_config=env_config,
                                                       action=a)
            s_prime.attacker_obs_state.machines = new_machines_obs
        else:
            target_machine.shell_access = False
            target_machine.shell_access_credentials = []

        return s_prime, total_new_ports, total_new_os, total_new_vuln, total_new_machines, \
               total_new_shell_access, total_new_flag_pts, total_new_root, total_new_osvdb_vuln_found, \
               total_new_logged_in, total_new_tools_installed, total_new_backdoors_installed, total_cost, True

    @staticmethod
    def _ssh_setup_connection(a: AttackerAction, env_config: EnvConfig,
                              credentials: List[Credential], proxy_connections: List[ConnectionObservationState],
                              s: EnvState) \
            -> Tuple[bool, List[str], List, List[int], float, List[Credential]]:
        """
        Helper function for setting up a SSH connection

        :param a: the action of the connection
        :param env_config: the environment config
        :param credentials: list of credentials to try
        :param proxy_connections: list of proxy connections to try
        :param s: env state
        :return: boolean whether connected or not, list of connected users, list of connection handles, list of ports,
                 cost, non_failed_credentials
        """
        connected = False
        users = []
        target_connections = []
        proxies = []
        ports = []
        start = time.time()
        non_failed_credentials = []
        for proxy_conn in proxy_connections:
            if proxy_conn.ip != env_config.hacker_ip:
                m = s.get_attacker_machine(proxy_conn.ip)
                if m is None or a.ip not in m.reachable or m.ip == a.ip:
                    continue
            else:
                if not a.ip in s.attacker_obs_state.agent_reachable:
                    continue
            for cr in credentials:
                if cr.service == constants.SSH.SERVICE_NAME:
                    try:
                        agent_addr = (proxy_conn.ip, cr.port)
                        target_addr = (a.ip, cr.port)
                        agent_transport = proxy_conn.conn.get_transport()
                        relay_channel = agent_transport.open_channel(constants.SSH.DIRECT_CHANNEL, target_addr,
                                                                     agent_addr,
                                                                     timeout=3)
                        target_conn = paramiko.SSHClient()
                        target_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        target_conn.connect(a.ip, username=cr.username, password=cr.pw, sock=relay_channel,
                                            timeout=3)
                        connected = True
                        users.append(cr.username)
                        target_connections.append(target_conn)
                        proxies.append(proxy_conn)
                        ports.append(cr.port)
                        non_failed_credentials.append(cr)
                    except Exception as e:
                        print("SSH exception :{}".format(str(e)))
                        print("user:{}, pw:{}".format(cr.username, cr.pw))
                        print("Target addr: {}, Source Addr: {}".format(target_addr, agent_addr))
                        print("Target ip in agent reachable: {}".format(a.ip in s.attacker_obs_state.agent_reachable))
                        print("Agent reachable:{}".format(s.attacker_obs_state.agent_reachable))
                        print("Action:{}, {}, {}".format(a.id, a.ip, a.descr))
                else:
                    non_failed_credentials.append(cr)
            if connected:
                break
        end = time.time()
        total_time = end - start
        return connected, users, target_connections, ports, total_time, non_failed_credentials, proxies

    @staticmethod
    def _ssh_finalize_connection(target_machine: AttackerMachineObservationState, users: List[str],
                                 target_connections: List, i: int, ports: List[int],
                                 proxies: List, env_config: EnvConfig) -> Tuple[bool, float]:
        """
        Helper function for finalizing a SSH connection and setting up the DTO

        :param target_machine: the target machine to connect to
        :param users: list of connected users
        :param target_connections: list of connection handles
        :param i: current index
        :param ports: list of ports of the connections
        :param proxies: proxy connections
        :param env_config: environment config
        :return: boolean whether the connection has root privileges or not, cost
        """
        start = time.time()
        for j in range(env_config.attacker_retry_check_root):
            outdata, errdata, total_time = EmulationUtil.execute_ssh_cmd(cmd="sudo -l",
                                                                         conn=target_connections[i])
            root = False
            if not "may not run sudo".format(users[i]) in errdata.decode("utf-8") \
                    and ("(ALL) NOPASSWD: ALL" in outdata.decode("utf-8") or
                         "(ALL : ALL) ALL" in outdata.decode("utf-8")):
                root = True
                target_machine.root = True
                break
            else:
                time.sleep(1)
        connection_dto = ConnectionObservationState(conn=target_connections[i], username=users[i],
                                                    root=root,
                                                    service=constants.SSH.SERVICE_NAME,
                                                    port=ports[i], proxy=proxies[i], ip=target_machine.ip)
        target_machine.ssh_connections.append(connection_dto)
        end = time.time()
        total_time = end - start
        return root, total_time

    @staticmethod
    def _telnet_setup_connection(a: AttackerAction, env_config: EnvConfig,
                                 credentials: List[Credential], proxy_connections: List,
                                 s: EnvState) \
            -> Tuple[bool, List[str], List, List[ForwardTunnelThread], List[int], List[int], float, List[Credential]]:
        """
        Helper function for setting up a Telnet connection to a target machine

        :param a: the action of the connection
        :param env_config: the environment config
        :param credentials: list of credentials to try
        :param proxies: proxy connections
        :param s: env state
        :return: connected (bool), connected users, connection handles, list of tunnel threads, list of forwarded ports,
                 list of ports, cost
        """
        connected = False
        users = []
        target_connections = []
        tunnel_threads = []
        forward_ports = []
        ports = []
        start = time.time()
        non_failed_credentials = []
        proxies = []
        for proxy_conn in proxy_connections:
            if proxy_conn.ip != env_config.hacker_ip:
                m = s.get_attacker_machine(proxy_conn.ip)
                if m is None or a.ip not in m.reachable or m.ip == a.ip:
                    continue
            else:
                if not a.ip in s.attacker_obs_state.agent_reachable:
                    continue
            for cr in credentials:
                if cr.service == constants.TELNET.SERVICE_NAME:
                    try:
                        forward_port = env_config.get_port_forward_port()
                        agent_addr = (proxy_conn.ip, cr.port)
                        target_addr = (a.ip, cr.port)
                        agent_transport = proxy_conn.conn.get_transport()
                        relay_channel = agent_transport.open_channel(constants.SSH.DIRECT_CHANNEL, target_addr,
                                                                     agent_addr,
                                                                     timeout=3)
                        tunnel_thread = ForwardTunnelThread(local_port=forward_port,
                                                            remote_host=a.ip, remote_port=cr.port,
                                                            transport=agent_transport)
                        tunnel_thread.start()
                        target_conn = telnetlib.Telnet(host=constants.TELNET.LOCALHOST, port=forward_port, timeout=3)
                        target_conn.read_until(constants.TELNET.LOGIN_PROMPT, timeout=3)
                        target_conn.write((cr.username + "\n").encode())
                        target_conn.read_until(constants.TELNET.PASSWORD_PROMPT, timeout=3)
                        target_conn.write((cr.pw + "\n").encode())
                        response = target_conn.read_until(constants.TELNET.PROMPT, timeout=3)
                        response = response.decode()
                        if not constants.TELNET.INCORRECT_LOGIN in response and response != "":
                            connected = True
                            users.append(cr.username)
                            target_connections.append(target_conn)
                            proxies.append(proxy_conn)
                            tunnel_threads.append(tunnel_thread)
                            forward_ports.append(forward_port)
                            ports.append(cr.port)
                        non_failed_credentials.append(cr)
                    except Exception as e:
                        print("telnet exception:{}".format(str(e)))
                        #print("Target:{} reachable from {}, {}".format(a.ip, m.ip, a.ip in m.reachable))
                        print("Target addr: {}, Source Addr: {}".format(target_addr, agent_addr))
                        print("Target ip in agent reachable: {}".format(a.ip in s.attacker_obs_state.agent_reachable))
                        print("Agent reachable:{}".format(s.attacker_obs_state.agent_reachable))
                else:
                    non_failed_credentials.append(cr)
            if connected:
                break
        end = time.time()
        total_time = end - start
        return connected, users, target_connections, tunnel_threads, forward_ports, ports, \
               total_time, non_failed_credentials, proxies

    @staticmethod
    def _telnet_finalize_connection(target_machine: AttackerMachineObservationState, users: List[str], target_connections: List,
                                    i: int,
                                    tunnel_threads: List, forward_ports: List[int], ports: List[int],
                                    proxies: List, env_config: EnvConfig) \
            -> Tuple[bool, float]:
        """
        Helper function for finalizing a Telnet connection to a target machine and creating the DTO

        :param target_machine: the target machine to connect to
        :param users: list of connected users
        :param target_connections: list of connection handles
        :param i: current index
        :param tunnel_threads: list of tunnel threads
        :param forward_ports: list of forwarded ports
        :param ports: list of ports of the connections
        :param proxies: proxies
        :param env_config: environment config
        :return: boolean whether the connection has root privileges or not, cost
        """
        start = time.time()
        for i in range(env_config.attacker_retry_check_root):
            target_connections[i].write("sudo -l\n".encode())
            response = target_connections[i].read_until(constants.TELNET.PROMPT, timeout=3)
            root = False
            if not "may not run sudo".format(users[i]) in response.decode("utf-8") \
                    and ("(ALL) NOPASSWD: ALL" in response.decode("utf-8") or
                         "(ALL : ALL) ALL" in response.decode("utf-8")):
                root = True
                break
            else:
                time.sleep(1)
        connection_dto = ConnectionObservationState(conn=target_connections[i], username=users[i], root=root,
                                                    service=constants.TELNET.SERVICE_NAME,
                                                    tunnel_thread=tunnel_threads[i],
                                                    tunnel_port=forward_ports[i],
                                                    port=ports[i], proxy=proxies[i], ip=target_machine.ip)
        target_machine.telnet_connections.append(connection_dto)
        end = time.time()
        total_time = end - start
        return root, total_time

    @staticmethod
    def _ftp_setup_connection(a: AttackerAction, env_config: EnvConfig,
                              credentials: List[Credential], proxy_connections: List,
                              s: EnvState) \
            -> Tuple[bool, List[str], List, List[ForwardTunnelThread], List[int], List[int], float, List[Credential]]:
        """
        Helper function for setting up a FTP connection

        :param a: the action of the connection
        :param env_config: the environment config
        :param credentials: list of credentials to try
        :param proxy_connections: proxy connections
        :param env_state: env state
        :return: connected (bool), connected users, connection handles, list of tunnel threads, list of forwarded ports,
                 list of ports, cost, non_failed_credentials
        """
        connected = False
        users = []
        target_connections = []
        tunnel_threads = []
        forward_ports = []
        ports = []
        interactive_shells = []
        start = time.time()
        non_failed_credentials = []
        proxies = []
        for proxy_conn in proxy_connections:
            if proxy_conn.ip != env_config.hacker_ip:
                m = s.get_attacker_machine(proxy_conn.ip)
                if m is None or a.ip not in m.reachable or m.ip == a.ip:
                    continue
            else:
                if not a.ip in s.attacker_obs_state.agent_reachable:
                    continue
            for cr in credentials:
                if cr.service == constants.FTP.SERVICE_NAME:
                    try:
                        forward_port = env_config.get_port_forward_port()
                        agent_addr = (proxy_conn.ip, cr.port)
                        target_addr = (a.ip, cr.port)
                        agent_transport = proxy_conn.conn.get_transport()
                        relay_channel = agent_transport.open_channel(constants.SSH.DIRECT_CHANNEL, target_addr,
                                                                     agent_addr,
                                                                     timeout=3)
                        tunnel_thread = ForwardTunnelThread(local_port=forward_port,
                                                            remote_host=a.ip, remote_port=cr.port,
                                                            transport=agent_transport)
                        tunnel_thread.start()
                        target_conn = FTP()
                        target_conn.connect(host=constants.FTP.LOCALHOST, port=forward_port, timeout=5)
                        login_result = target_conn.login(cr.username, cr.pw)
                        if constants.FTP.INCORRECT_LOGIN not in login_result:
                            connected = True
                            users.append(cr.username)
                            target_connections.append(target_conn)
                            proxies.append(proxy_conn)
                            tunnel_threads.append(tunnel_thread)
                            forward_ports.append(forward_port)
                            ports.append(cr.port)
                            # Create LFTP connection too to be able to search file system
                            shell = proxy_conn.conn.invoke_shell()
                            # clear output
                            if shell.recv_ready():
                                shell.recv(constants.COMMON.DEFAULT_RECV_SIZE)
                            shell.send(constants.FTP.LFTP_PREFIX + cr.username + ":" + cr.pw + "@" + a.ip + "\n")
                            time.sleep(0.5)
                            # clear output
                            if shell.recv_ready():
                                o = shell.recv(constants.COMMON.DEFAULT_RECV_SIZE)
                            interactive_shells.append(shell)
                            non_failed_credentials.append(cr)
                    except Exception as e:
                        print("FTP exception: {}".format(str(e)))
                        print("Target addr: {}, Source Addr: {}".format(target_addr, agent_addr))
                        print("Target ip in agent reachable: {}".format(a.ip in s.attacker_obs_state.agent_reachable))
                        print("Agent reachable:{}".format(s.attacker_obs_state.agent_reachable))
                else:
                    non_failed_credentials.append(cr)
            if connected:
                break
        end = time.time()
        total_time = end - start
        return connected, users, target_connections, tunnel_threads, forward_ports, ports, interactive_shells, total_time, \
               non_failed_credentials, proxies

    @staticmethod
    def _ftp_finalize_connection(target_machine: AttackerMachineObservationState, users: List[str], target_connections: List,
                                 i: int,
                                 tunnel_threads: List, forward_ports: List[int], ports: List[int],
                                 interactive_shells: List, proxies: List) -> Tuple[bool, float]:
        """
        Helper function for creating the connection DTO for FTP

        :param target_machine: the target machine to connect to
        :param users: list of users that are connected
        :param target_connections: list of connections to the target
        :param i: current index
        :param tunnel_threads: list of tunnel threads to the target
        :param forward_ports: list of forwarded ports to the target
        :param ports: list of ports of the connections
        :param interactive_shells: shells for LFTP
        :return: boolean, whether the connection has root privileges, cost
        """
        root = False
        connection_dto = ConnectionObservationState(conn=target_connections[i], username=users[i], root=root,
                                                    service=constants.FTP.SERVICE_NAME,
                                                    tunnel_thread=tunnel_threads[i],
                                                    tunnel_port=forward_ports[i],
                                                    port=ports[i],
                                                    interactive_shell=interactive_shells[i], ip=target_machine.ip,
                                                    proxy=proxies[i])
        target_machine.ftp_connections.append(connection_dto)
        return root, 0


    @staticmethod
    def find_jump_host_connection(ip, s: AttackerMachineObservationState, env_config: EnvConfig) -> ConnectionObservationState:
        """
        Utility function for finding a jump-host from the set of compromised machines to reach a target IP

        :param ip: the ip to reach
        :param s: the current state
        :param env_config: the environment configuration
        :return: a connection DTO
        """

        if ip in s.attacker_obs_state.agent_reachable:
            c = ConnectionObservationState(conn=env_config.emulation_config.agent_conn,
                                       username=env_config.emulation_config.agent_username,
                                       root=True, port=22,
                                       service=constants.SSH.SERVICE_NAME,
                                       proxy=None, ip=env_config.emulation_config.agent_ip)
            return c
        s.attacker_obs_state.sort_machines()

        for m in s.attacker_obs_state.machines:
            if m.logged_in and m.tools_installed and m.backdoor_installed and ip in m.reachable:

                # Start with ssh connections
                ssh_connections_sorted_by_root = sorted(
                    m.ssh_connections,
                    key=lambda x: (constants.SSH_BACKDOOR.BACKDOOR_PREFIX in x.username, x.root, x.username),
                    reverse=True)

                for c in ssh_connections_sorted_by_root:
                    alive = ConnectionUtil.test_connection(c)
                    if alive:
                        return c
        raise ValueError("No JumpHost found")


    @staticmethod
    def test_connection(c: ConnectionObservationState) -> bool:
        """
        Utility function for testing if a connection is alive or not

        :param c: the connection to thest
        :return: True if the connection is alive, otherwise false
        """
        cmd = "whoami"
        outdata, errdata, total_time = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=c.conn)
        if outdata is not None and outdata != "":
            return True
        else:
            return False