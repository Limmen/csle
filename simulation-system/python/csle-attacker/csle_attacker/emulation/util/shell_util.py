from typing import Tuple
import time
import random
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.util.env_dynamics_util import EnvDynamicsUtil
from csle_common.dao.emulation_observation.common.emulation_connection_observation_state \
    import EmulationConnectionObservationState
from csle_common.dao.emulation_observation.attacker.emulation_attacker_machine_observation_state \
    import EmulationAttackerMachineObservationState
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.credential import Credential
from csle_common.util.emulation_util import EmulationUtil
from csle_common.util.connection_util import ConnectionUtil
from csle_common.logging.log import Logger


class ShellUtil:
    """
    Class containing utility functions for the shell-related functionality to the emulation
    """

    @staticmethod
    def _find_flag_using_ssh(machine: EmulationAttackerMachineObservationState,
                             emulation_env_config: EmulationEnvConfig,
                             a: EmulationAttackerAction, new_m_obs: EmulationAttackerMachineObservationState) \
            -> Tuple[EmulationAttackerMachineObservationState, float, bool]:
        """
        Utility function for using existing SSH connections to a specific machine to search the file system for flags

        :param machine: the machine to search
        :param emulation_env_config: the emulation env config
        :param a: the action of finding the flags
        :param new_m_obs: the updated machine observation with the found flags
        :return: the updated machine observation with the found flags, cost, root
        """
        total_cost = 0
        ssh_connections_sorted_by_root = sorted(
            machine.ssh_connections,
            key=lambda x: (constants.SSH_BACKDOOR.BACKDOOR_PREFIX in x.credential.username, x.root,
                           x.credential.username),
            reverse=True)
        root_scan = False
        flag_paths = []
        for c in ssh_connections_sorted_by_root:
            cmd = a.cmds[0]
            if c.root:
                cmd = constants.COMMANDS.SUDO + " " + cmd
            for i in range(constants.ENV_CONSTANTS.ATTACKER_SSH_RETRY_FIND_FLAG):
                outdata, errdata, total_time = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=c.conn)
                new_m_obs.filesystem_searched = True
                EmulationUtil.log_measured_action_time(total_time=total_time, action=a,
                                                       emulation_env_config=emulation_env_config)
                outdata_str = outdata.decode()
                flag_paths = outdata_str.split("\n")
                flag_paths = list(filter(lambda x: x != '', flag_paths))
                num_flags = 0
                for fp in flag_paths:
                    fp = fp.replace(".txt", "")
                    for node_flags_config in emulation_env_config.flags_config.node_flag_configs:
                        if node_flags_config.ip in machine.ips:
                            for flag in node_flags_config.flags:
                                if flag.name == fp:
                                    num_flags += 1
                    if fp in emulation_env_config.flags_config.node_flag_configs:
                        num_flags += 1
                if len(flag_paths) > 0 and num_flags > 0:
                    break
                else:
                    time.sleep(1)

            # Check for flags
            for fp in flag_paths:
                fp = fp.replace(".txt", "")
                for node_flags_config in emulation_env_config.flags_config.node_flag_configs:
                    if node_flags_config.ip in machine.ips:
                        for flag in node_flags_config.flags:
                            if flag.name == fp:
                                new_m_obs.flags_found.add(flag)

            if c.root:
                root_scan = True
                break
        return new_m_obs, total_cost, root_scan

    @staticmethod
    def _find_flag_using_telnet(machine: EmulationAttackerMachineObservationState,
                                emulation_env_config: EmulationEnvConfig, a: EmulationAttackerAction,
                                new_m_obs: EmulationAttackerMachineObservationState) \
            -> Tuple[EmulationAttackerMachineObservationState, float, bool]:
        """
        Utility function for using existing Telnet connections to a specific machine to search the file system for flags

        :param machine: the machine to search
        :param emulation_env_config: the emulation env config
        :param a: the action of finding the flags
        :param new_m_obs: the updated machine observation with the found flags
        :return: the updated machine observation with the found flags, cost, root
        """
        total_cost = 0
        telnet_connections_sorted_by_root = sorted(
            machine.telnet_connections,
            key=lambda x: (constants.SSH_BACKDOOR.BACKDOOR_PREFIX in x.credential.username, x.root,
                           x.credential.username),
            reverse=True)
        root_scan = False
        for c in telnet_connections_sorted_by_root:
            cmd = a.cmds[0] + "\n"
            if c.root:
                cmd = constants.COMMANDS.SUDO + " " + cmd
            start = time.time()
            c.conn.write(cmd.encode())
            response = c.conn.read_until(constants.TELNET.PROMPT, timeout=5)
            new_m_obs.filesystem_searched = True
            end = time.time()
            total_time = end - start

            EmulationUtil.log_measured_action_time(total_time=total_time, action=a,
                                                   emulation_env_config=emulation_env_config)
            flag_paths = response.decode().strip().split("\r\n")
            # Check for flags
            for fp in flag_paths:
                fp = fp.replace(".txt", "")
                for node_flags_config in emulation_env_config.flags_config.node_flag_configs:
                    if node_flags_config.ip in machine.ips:
                        for flag in node_flags_config.flags:
                            if flag.name == fp:
                                new_m_obs.flags_found.add(flag)

            if c.root:
                root_scan = True
                break
        return new_m_obs, total_cost, root_scan

    @staticmethod
    def _find_flag_using_ftp(machine: EmulationAttackerMachineObservationState,
                             emulation_env_config: EmulationEnvConfig, a: EmulationAttackerAction,
                             new_m_obs: EmulationAttackerMachineObservationState) \
            -> Tuple[EmulationAttackerMachineObservationState, float, bool]:
        """
        Utility function for using existing FTP connections to a specific machine to search the file system for flags

        :param machine: the machine to search
        :param emulation_env_config: the emulation env config
        :param a: the action of finding the flags
        :param new_m_obs: the updated machine observation with the found flags
        :return: the updated machine observation with the found flags, cost, root
        """
        total_cost = 0
        ftp_connections_sorted_by_root = sorted(
            machine.ftp_connections,
            key=lambda x: (constants.SSH_BACKDOOR.BACKDOOR_PREFIX in x.credential.username, x.root,
                           x.credential.username),
            reverse=True)
        root_scan = False
        flag_paths = []
        for c in ftp_connections_sorted_by_root:
            for i in range(constants.ENV_CONSTANTS.ATTACKER_FTP_RETRY_FIND_FLAG):
                cmd = a.alt_cmds[0] + "\n"
                if c.root:
                    cmd = constants.COMMANDS.SUDO + " " + cmd
                start = time.time()
                c.interactive_shell.send(cmd)
                output = b""

                # clear output
                if c.interactive_shell.recv_ready():
                    c.interactive_shell.recv(constants.COMMON.DEFAULT_RECV_SIZE)
                command_complete = False
                timeouts = 0
                while not command_complete:
                    while not c.interactive_shell.recv_ready():
                        if timeouts > constants.ENV_CONSTANTS.SHELL_MAX_TIMEOUTS:
                            Logger.__call__().get_logger().warning("max timeouts FTP, env:{}".format(
                                emulation_env_config.containers_config.agent_ip))
                            break
                        time.sleep(constants.ENV_CONSTANTS.SHELL_READ_WAIT)
                        timeouts += 1
                    if c.interactive_shell.recv_ready():
                        output += c.interactive_shell.recv(constants.COMMON.LARGE_RECV_SIZE)
                        timeouts = 0
                        if constants.FTP.LFTP_PROMPT in output.decode() \
                                or constants.FTP.LFTP_PROMPT_2 in output.decode():
                            command_complete = True
                            end = time.time()
                            total_time = end - start

                            EmulationUtil.log_measured_action_time(total_time=total_time, action=a,
                                                                   emulation_env_config=emulation_env_config)
                    else:
                        break

                    output_str = output.decode("utf-8")
                    output_str = constants.NMAP.SHELL_ESCAPE.sub("", output_str)
                    output_list = output_str.split('\r\n')
                    output_list = output_list[1:-1]  # remove command ([0]) and prompt ([-1])
                    flag_paths = list(filter(lambda x: constants.FTP.ACCESS_FAILED not in x and x != "", output_list))
                    ff = False
                    # Check for flags
                    for fp in flag_paths:
                        fp = fp.replace(".txt", "")
                        for node_flags_config in emulation_env_config.flags_config.node_flag_configs:
                            if node_flags_config.ip in machine.ips:
                                for flag in node_flags_config.flags:
                                    if flag.name == fp:
                                        ff = True
                    if not ff:
                        continue
                    else:
                        break
            new_m_obs.filesystem_searched = True

            # Check for flags
            for fp in flag_paths:
                fp = fp.replace(".txt", "")
                for node_flags_config in emulation_env_config.flags_config.node_flag_configs:
                    if node_flags_config.ip in machine.ips:
                        for flag in node_flags_config.flags:
                            if flag.name == fp:
                                new_m_obs.flags_found.add(flag)

            if c.root:
                root_scan = True
                break
        return new_m_obs, total_cost, root_scan

    @staticmethod
    def parse_tools_installed_file(file_name: str, emulation_env_config: EmulationEnvConfig) -> bool:
        """
        Parses a file containing cached results of a install-tools action

        :param file_name: name of the file to parse
        :param emulation_env_config: environment config
        :return: boolean: if installed or not
        """
        sftp_client = emulation_env_config.get_hacker_connection().open_sftp()
        remote_file = sftp_client.open(constants.NMAP.RESULTS_DIR + file_name)
        try:
            data = remote_file.read()
            data = data.decode()
            installed = bool(int(data))
        finally:
            remote_file.close()
        return installed

    @staticmethod
    def _parse_tools_installed_check_result(result: str) -> bool:
        """
        Checks the output result of a tools install action to see whether the action was successful or not.

        :param result: the result to check
        :return: True if sucessful otherwise False
        """
        return ("will be installed" in result or "already installed" in result
                or "already the newest version" in result)

    @staticmethod
    def install_tools_helper(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Uses compromised machines with root access to install tools

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        new_machines_obs = []
        total_cost = 0
        total_time = 0
        for machine in s.attacker_obs_state.machines:
            new_m_obs = EmulationAttackerMachineObservationState(ips=machine.ips)
            if machine.logged_in and machine.root:
                new_m_obs.install_tools_tried = True
            installed = False
            if machine.logged_in and machine.root and not machine.tools_installed:
                # Start with ssh connections
                ssh_root_connections = filter(lambda x: x.root, machine.ssh_connections)
                ssh_root_connections = sorted(ssh_root_connections, key=lambda x: x.credential.username)
                ssh_cost = 0
                for c in ssh_root_connections:
                    cmd = a.cmds[0]
                    for i in range(constants.ENV_CONSTANTS.ATTACKER_RETRY_INSTALL_TOOLS):
                        outdata, errdata, total_time = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=c.conn)
                        time.sleep(constants.ENV_CONSTANTS.ATTACKER_INSTALL_TOOLS_SLEEP_SECONDS)
                        outdata = outdata.decode()
                        ssh_cost += float(total_time)
                        if ShellUtil._parse_tools_installed_check_result(result=outdata):
                            installed = True
                            new_m_obs.tools_installed = True
                        else:
                            Logger.__call__().get_logger().warning(
                                "SSH tools installed failed result. out:{}, err:{}".format(outdata, errdata))
                        if installed:
                            break

                    # try to download seclists
                    seclists_installed = ShellUtil._check_if_seclists_is_installed(conn=c.conn, telnet=False)
                    if not seclists_installed:
                        cmd = a.cmds[1]
                        outdata, errdata, total_time = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=c.conn)
                        ssh_cost += float(total_time)

                    EmulationUtil.log_measured_action_time(total_time=total_time, action=a,
                                                           emulation_env_config=s.emulation_env_config)

                    new_machines_obs.append(new_m_obs)

                    if installed:
                        break

                total_cost += ssh_cost

                # Telnet connections
                telnet_cost = 0
                if installed:
                    continue
                telnet_root_connections = filter(lambda x: x.root, machine.telnet_connections)
                telnet_root_connections = sorted(telnet_root_connections, key=lambda x: x.credential.username)
                for c in telnet_root_connections:
                    # Install packages
                    cmd = a.cmds[0] + "\n"
                    start = time.time()
                    for i in range(constants.ENV_CONSTANTS.ATTACKER_RETRY_INSTALL_TOOLS):
                        try:
                            c.conn.write(cmd.encode())
                            response = c.conn.read_until(constants.TELNET.PROMPT, timeout=25)
                            response = response.decode()
                            end = time.time()
                            total_time = end - start
                            telnet_cost += float(total_time)
                            if ShellUtil._parse_tools_installed_check_result(result=response):
                                installed = True
                                new_m_obs.tools_installed = True
                            else:
                                Logger.__call__().get_logger().warning(
                                    "Telnet tools installed failed result.{}".format(response))
                            if installed:
                                break
                        except Exception as e:
                            Logger.__call__().get_logger().warning(
                                f"Telnet tools installed exception {str(e)}, {repr(e)}")
                            c = ConnectionUtil.reconnect_telnet(
                                c=c, forward_port=s.emulation_env_config.get_port_forward_port())

                    seclists_installed = ShellUtil._check_if_seclists_is_installed(conn=c.conn, telnet=True)
                    if not seclists_installed:
                        # Try to download SecLists
                        cmd = a.cmds[1] + "\n"
                        start = time.time()
                        c.conn.write(cmd.encode())
                        response = c.conn.read_until(constants.TELNET.PROMPT, timeout=2000)
                        response = response.decode()
                        end = time.time()
                        total_time = end - start
                        telnet_cost += float(total_time)

                    EmulationUtil.log_measured_action_time(total_time=total_time, action=a,
                                                           emulation_env_config=s.emulation_env_config)

                    new_machines_obs.append(new_m_obs)

                    if installed:
                        break

                total_cost += telnet_cost
        attacker_machine_observations = EnvDynamicsUtil.merge_new_obs_with_old(
            s.attacker_obs_state.machines, new_machines_obs, emulation_env_config=s.emulation_env_config, action=a)
        s_prime = s
        s_prime.attacker_obs_state.machines = attacker_machine_observations

        return s_prime

    @staticmethod
    def _check_if_seclists_is_installed(conn, telnet: bool = False) -> bool:
        """
        Checks if seclists are downloaded

        :param conn: the connection to use for the command
        :param telnet: whether the connection is a telnet connection
        :return: True if downloaded, else false
        """
        cmd = constants.SHELL.CHECK_FOR_SECLISTS
        checklists_installed = False
        if not telnet:
            for i in range(8):
                outdata, errdata, total_time = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=conn)
                checklists_installed = "file exists" in outdata.decode() or "file exists" in errdata.decode()
                if checklists_installed:
                    break
                else:
                    Logger.__call__().get_logger().warning(
                        "checklists not installed:{}, {}".format(outdata.decode(), errdata.decode()))
            return checklists_installed
        else:
            cmd = cmd + "\n"
            conn.write(cmd.encode())
            response = conn.read_until(constants.TELNET.PROMPT, timeout=5)
            return "file exists" in response.decode()

    @staticmethod
    def execute_ssh_backdoor_helper(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Uses compromised machines with root access to setup SSH backdoor

        :param s: the current state
        :param a: the action to take
        :return: s_prime
        """
        username = constants.SSH_BACKDOOR.BACKDOOR_PREFIX + "_" + str(random.randint(0, 100000))
        pw = constants.SSH_BACKDOOR.DEFAULT_PW
        new_machines_obs = []
        total_cost = 0
        for machine in s.attacker_obs_state.machines:
            new_m_obs = EmulationAttackerMachineObservationState(ips=machine.ips)
            backdoor_created = False
            if machine.logged_in and machine.root and machine.tools_installed and not machine.backdoor_installed:
                new_m_obs.backdoor_tried = True
                # Check cached connections
                for cr in s.attacker_cached_backdoor_credentials.values():
                    for ip in machine.ips:
                        if (ip, cr.username, cr.kafka_port) in s.attacker_cached_ssh_connections:
                            conn_dto = s.attacker_cached_ssh_connections[
                                (ip, cr.username, cr.kafka_port)]
                            connection_dto = EmulationConnectionObservationState(
                                conn=conn_dto.conn, credential=cr, root=machine.root,
                                service=constants.SSH.SERVICE_NAME, port=cr.kafka_port, ip=ip)
                            new_m_obs.shell_access_credentials.append(cr)
                            new_m_obs.backdoor_credentials.append(cr)
                            new_m_obs.ssh_connections.append(connection_dto)
                            new_m_obs.backdoor_installed = True
                            new_machines_obs.append(new_m_obs)
                            backdoor_created = True
                            break

                if backdoor_created:
                    continue

                # Try first to setup new ssh connections
                ssh_root_connections = list(filter(lambda x: x.root, machine.ssh_connections))
                ssh_root_connections = sorted(ssh_root_connections, key=lambda x: x.credential.username)
                ssh_cost = 0
                for c in ssh_root_connections:
                    users = EmulationUtil._list_all_users(c, emulation_env_config=s.emulation_env_config)
                    users = sorted(users, key=lambda x: x)
                    user_exists = False
                    for user in users:
                        if constants.SSH_BACKDOOR.BACKDOOR_PREFIX in user and not user == constants.SAMBA.BACKDOOR_USER:
                            user_exists = True
                            username = user

                    if not user_exists:
                        # Create user
                        create_user_cmd = a.cmds[1].format(username, pw, username)
                        outdata, errdata, total_time = EmulationUtil.execute_ssh_cmd(cmd=create_user_cmd, conn=c.conn)
                        ssh_cost += float(total_time)

                    credential = Credential(username=username, pw=pw, port=22, service="ssh")

                    # Start SSH Server
                    ssh_running = EmulationUtil._check_if_ssh_server_is_running(c.conn)
                    if not ssh_running:
                        start_ssh_cmd = a.cmds[0]
                        outdata, errdata, total_time = EmulationUtil.execute_ssh_cmd(cmd=start_ssh_cmd, conn=c.conn)
                        ssh_cost += float(total_time)

                    # Create SSH connection
                    new_m_obs.shell_access_credentials.append(credential)
                    new_m_obs.backdoor_credentials.append(credential)
                    a.ips = machine.ips
                    setup_connection_dto = None
                    for i in range(5):
                        setup_connection_dto = ConnectionUtil._ssh_setup_connection(
                            a=a, credentials=[credential], proxy_connections=[c.proxy], s=s)
                        ssh_cost += setup_connection_dto.total_time
                        if len(setup_connection_dto.target_connections) > 0:
                            break
                        else:
                            time.sleep(5)

                    if len(setup_connection_dto.target_connections) == 0:
                        Logger.__call__().get_logger().warning(
                            "cannot install backdoor, machine:{}, credentials:{}".format(machine.ips, credential))
                    connection_dto = EmulationConnectionObservationState(
                        conn=setup_connection_dto.target_connections[0], credential=credential, root=machine.root,
                        service=constants.SSH.SERVICE_NAME, port=credential.port, proxy=setup_connection_dto.proxies[0],
                        ip=setup_connection_dto.ip)
                    new_m_obs.ssh_connections.append(connection_dto)
                    new_m_obs.backdoor_installed = True
                    new_machines_obs.append(new_m_obs)
                    backdoor_created = True

                    if backdoor_created:
                        break

                total_cost += ssh_cost

                # Telnet connections
                telnet_cost = 0
                if backdoor_created:
                    continue
                telnet_root_connections = filter(lambda x: x.root, machine.telnet_connections)
                telnet_root_connections = sorted(telnet_root_connections, key=lambda x: x.credential.username)
                for c in telnet_root_connections:
                    try:
                        users = EmulationUtil._list_all_users(c,
                                                              emulation_env_config=s.emulation_env_config, telnet=True)
                        user_exists = False
                        for user in users:
                            if constants.SSH_BACKDOOR.BACKDOOR_PREFIX in user \
                                    and not user == constants.SAMBA.BACKDOOR_USER:
                                user_exists = True
                                username = user

                        credential = Credential(username=username, pw=pw, port=22, service="ssh")

                        if not user_exists:
                            # Create user
                            create_user_cmd = a.cmds[1].format(username, pw, username) + "\n"
                            c.conn.write(create_user_cmd.encode())
                            c.conn.read_until(constants.TELNET.PROMPT, timeout=5)

                        ssh_running = EmulationUtil._check_if_ssh_server_is_running(c.conn, telnet=True)
                        if not ssh_running:
                            # Start SSH Server
                            start_ssh_cmd = a.cmds[0] + "\n"
                            c.conn.write(start_ssh_cmd.encode())
                            c.conn.read_until(constants.TELNET.PROMPT, timeout=5)

                        # Create SSH connection
                        new_m_obs.shell_access_credentials.append(credential)
                        new_m_obs.backdoor_credentials.append(credential)
                        a.ips = machine.ips
                        setup_connection_dto = ConnectionUtil._ssh_setup_connection(
                            a=a, credentials=[credential], proxy_connections=[c.proxy], s=s)
                        telnet_cost += setup_connection_dto.total_time
                        connection_dto = EmulationConnectionObservationState(
                            conn=setup_connection_dto.target_connections[0], credential=credential, root=machine.root,
                            service=constants.SSH.SERVICE_NAME, port=credential.port,
                            proxy=setup_connection_dto.proxies[0], ip=setup_connection_dto.ip)
                        new_m_obs.ssh_connections.append(connection_dto)
                        new_m_obs.backdoor_installed = True
                        new_machines_obs.append(new_m_obs)
                        backdoor_created = True
                    except Exception as e:
                        Logger.__call__().get_logger().warning(
                            f"Exception occurred while setting up backdoors , {str(e)}, {repr(e)}")
                    if backdoor_created:
                        break

                total_cost += telnet_cost
        attacker_machine_observations = EnvDynamicsUtil.merge_new_obs_with_old(
            s.attacker_obs_state.machines, new_machines_obs, emulation_env_config=s.emulation_env_config, action=a)
        s_prime = s
        s_prime.attacker_obs_state.machines = attacker_machine_observations

        return s_prime

    @staticmethod
    def execute_service_login_helper(s: EmulationEnvState, a: EmulationAttackerAction) -> EmulationEnvState:
        """
        Executes a service login on the emulation using previously found credentials

        :param s: the current state
        :param a: the action to take
        :return: s_prime, reward, done
        """
        s_prime = s

        for machine in s.attacker_obs_state.machines:
            a.ips = machine.ips
            s_1, new_conn_ssh = ConnectionUtil.login_service_helper(
                s=s_prime, a=a, alive_check=EmulationEnvConfig.check_if_ssh_connection_is_alive,
                service_name=constants.SSH.SERVICE_NAME)
            s_2, new_conn_ftp = ConnectionUtil.login_service_helper(
                s=s_1, a=a, alive_check=EnvDynamicsUtil.check_if_ftp_connection_is_alive,
                service_name=constants.FTP.SERVICE_NAME)
            s_3, new_conn_telnet = ConnectionUtil.login_service_helper(
                s=s_2, a=a, alive_check=EnvDynamicsUtil.check_if_telnet_connection_is_alive,
                service_name=constants.TELNET.SERVICE_NAME)

            s_prime = s_3

            for m in s_prime.attacker_obs_state.machines:
                if m.ips == a.ips:
                    m.untried_credentials = False

        a.ips = ""

        return s_prime
