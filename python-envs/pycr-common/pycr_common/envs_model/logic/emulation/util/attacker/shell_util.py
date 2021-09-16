from typing import Tuple, List
import time
import random
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.action.attacker.attacker_action import AttackerAction
from gym_pycr_ctf.dao.network.env_state import EnvState
from gym_pycr_ctf.envs_model.logic.common.env_dynamics_util import EnvDynamicsUtil
from pycr_common.dao.observation.common.connection_observation_state import ConnectionObservationState
from gym_pycr_ctf.dao.observation.attacker.attacker_machine_observation_state import AttackerMachineObservationState
import pycr_common.constants.constants as constants
from pycr_common.dao.network.credential import Credential
from pycr_common.envs_model.logic.emulation.util.common.emulation_util import EmulationUtil
from pycr_common.envs_model.logic.emulation.util.common.connection_util import ConnectionUtil


class ShellUtil:
    """
    Class containing utility functions for the shell-related functionality to the emulation
    """

    @staticmethod
    def _find_flag_using_ssh(machine: AttackerMachineObservationState, env_config: EnvConfig, a: AttackerAction,
                             new_m_obs: AttackerMachineObservationState) -> Tuple[AttackerMachineObservationState, float,
                                                                                  bool, Tuple]:
        """
        Utility function for using existing SSH connections to a specific machine to search the file system for flags

        :param machine: the machine to search
        :param env_config: the env config
        :param a: the action of finding the flags
        :param new_m_obs: the updated machine observation with the found flags
        :return: the updated machine observation with the found flags, cost, root, alerts
        """
        total_cost = 0
        ssh_connections_sorted_by_root = sorted(
            machine.ssh_connections,
            key=lambda x: (constants.SSH_BACKDOOR.BACKDOOR_PREFIX in x.username, x.root, x.username),
            reverse=True)
        root_scan = False
        total_alerts = (0, 0)
        for c in ssh_connections_sorted_by_root:
            cache_file = \
                EmulationUtil.check_filesystem_action_cache(a=a, env_config=env_config, ip=machine.ip,
                                                            service=constants.SSH.SERVICE_NAME,
                                                            user=c.username, root=c.root)
            if cache_file is not None:
                flag_paths = EmulationUtil.parse_file_scan_file(file_name=cache_file,
                                                                env_config=env_config)
            else:
                if env_config.ids_router:
                    last_alert_ts = EmulationUtil.get_latest_alert_ts(env_config=env_config)
                cmd = a.cmd[0]
                if c.root:
                    cmd = constants.COMMANDS.SUDO + " " + cmd
                for i in range(env_config.attacker_ssh_retry_find_flag):
                    outdata, errdata, total_time = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=c.conn)
                    new_m_obs.filesystem_searched = True
                    if env_config.ids_router:
                        fast_logs = EmulationUtil.check_ids_fast_log(env_config=env_config)
                        if last_alert_ts is not None:
                            fast_logs = list(filter(lambda x: x[1] > last_alert_ts, fast_logs))
                        sum_priority_alerts = sum(list(map(lambda x: x[0], fast_logs)))
                        num_alerts = len(fast_logs)
                        EmulationUtil.write_alerts_response(sum_priorities=sum_priority_alerts, num_alerts=num_alerts,
                                                            action=a, env_config=env_config, ip=machine.ip,
                                                            user=c.username, service=constants.SSH.SERVICE_NAME)
                        env_config.attacker_action_alerts.user_ip_add_alert(action_id=a.id, ip=machine.ip, user=c.username,
                                                                            service=constants.SSH.SERVICE_NAME,
                                                                            alert=(sum_priority_alerts, num_alerts))

                    EmulationUtil.write_estimated_cost(total_time=total_time, action=a,
                                                       env_config=env_config, ip=machine.ip,
                                                       user=c.username,
                                                       service=constants.SSH.SERVICE_NAME)
                    env_config.attacker_action_costs.find_add_cost(action_id=a.id, ip=machine.ip, user=c.username,
                                                                   service=constants.SSH.SERVICE_NAME,
                                                                   cost=float(total_time))
                    outdata_str = outdata.decode()
                    flag_paths = outdata_str.split("\n")
                    flag_paths = list(filter(lambda x: x != '', flag_paths))
                    num_flags = 0
                    for fp in flag_paths:
                        fp = fp.replace(".txt", "")
                        if (machine.ip, fp) in env_config.flag_lookup:
                            num_flags += 1
                    if len(flag_paths) > 0 and num_flags > 0:
                        break
                    else:
                        time.sleep(1)

                # Persist cache
                EmulationUtil.write_file_system_scan_cache(action=a, env_config=env_config,
                                                           service=constants.SSH.SERVICE_NAME, user=c.username,
                                                           files=flag_paths, ip=machine.ip, root=c.root)

            # Check for flags
            for fp in flag_paths:
                fp = fp.replace(".txt", "")
                if (machine.ip, fp) in env_config.flag_lookup:
                    new_m_obs.flags_found.add(env_config.flag_lookup[(machine.ip, fp)])

            # Update cost
            if env_config.attacker_action_costs.find_exists(action_id=a.id, ip=machine.ip, user=c.username,
                                                            service=constants.SSH.SERVICE_NAME):
                cost = env_config.attacker_action_costs.find_get_cost(action_id=a.id, ip=machine.ip, user=c.username,
                                                                      service=constants.SSH.SERVICE_NAME)
                total_cost += cost

            # Update alerts
            if env_config.ids_router and env_config.attacker_action_alerts.user_ip_exists(action_id=a.id, ip=machine.ip,
                                                                                          user=c.username,
                                                                                          service=constants.SSH.SERVICE_NAME):
                alerts = env_config.attacker_action_alerts.user_ip_get_alert(action_id=a.id, ip=machine.ip, user=c.username,
                                                                             service=constants.SSH.SERVICE_NAME)
                total_alerts = alerts

            if c.root:
                root_scan = True
                break
        return new_m_obs, total_cost, root_scan, total_alerts

    @staticmethod
    def _find_flag_using_telnet(machine: AttackerMachineObservationState, env_config: EnvConfig, a: AttackerAction,
                                new_m_obs: AttackerMachineObservationState) \
            -> Tuple[AttackerMachineObservationState, float, bool, Tuple]:
        """
        Utility function for using existing Telnet connections to a specific machine to search the file system for flags

        :param machine: the machine to search
        :param env_config: the env config
        :param a: the action of finding the flags
        :param new_m_obs: the updated machine observation with the found flags
        :return: the updated machine observation with the found flags, cost, root, alerts
        """
        total_cost = 0
        total_alerts = (0, 0)
        telnet_connections_sorted_by_root = sorted(
            machine.telnet_connections,
            key=lambda x: (constants.SSH_BACKDOOR.BACKDOOR_PREFIX in x.username, x.root, x.username),
            reverse=True)
        root_scan = False
        for c in telnet_connections_sorted_by_root:
            cache_file = \
                EmulationUtil.check_filesystem_action_cache(a=a, env_config=env_config, ip=machine.ip,
                                                            service=constants.TELNET.SERVICE_NAME,
                                                            user=c.username, root=c.root)
            if cache_file is not None:
                flag_paths = EmulationUtil.parse_file_scan_file(file_name=cache_file,
                                                                env_config=env_config)
            else:
                cmd = a.cmd[0] + "\n"
                if c.root:
                    cmd = constants.COMMANDS.SUDO + " " + cmd
                if env_config.ids_router:
                    last_alert_ts = EmulationUtil.get_latest_alert_ts(env_config=env_config)
                start = time.time()
                c.conn.write(cmd.encode())
                response = c.conn.read_until(constants.TELNET.PROMPT, timeout=5)
                new_m_obs.filesystem_searched = True
                end = time.time()
                total_time = end - start
                if env_config.ids_router:
                    fast_logs = EmulationUtil.check_ids_fast_log(env_config=env_config)
                    if last_alert_ts is not None:
                        fast_logs = list(filter(lambda x: x[1] > last_alert_ts, fast_logs))
                    sum_priority_alerts = sum(list(map(lambda x: x[0], fast_logs)))
                    num_alerts = len(fast_logs)
                    EmulationUtil.write_alerts_response(sum_priorities=sum_priority_alerts, num_alerts=num_alerts,
                                                        action=a, env_config=env_config, ip=machine.ip,
                                                        user=c.username,
                                                        service=constants.TELNET.SERVICE_NAME)
                    env_config.attacker_action_alerts.user_ip_add_alert(action_id=a.id, ip=machine.ip, user=c.username,
                                                                        service=constants.TELNET.SERVICE_NAME,
                                                                        alert=(sum_priority_alerts, num_alerts))

                EmulationUtil.write_estimated_cost(total_time=total_time, action=a,
                                                   env_config=env_config, ip=machine.ip,
                                                   user=c.username,
                                                   service=constants.TELNET.SERVICE_NAME)
                env_config.attacker_action_costs.find_add_cost(action_id=a.id, ip=machine.ip, user=c.username,
                                                               service=constants.TELNET.SERVICE_NAME,
                                                               cost=float(total_time))
                flag_paths = response.decode().strip().split("\r\n")
                # Persist cache
                EmulationUtil.write_file_system_scan_cache(action=a, env_config=env_config,
                                                           service=constants.TELNET.SERVICE_NAME, user=c.username,
                                                           files=flag_paths, ip=machine.ip, root=c.root)
            # Check for flags
            for fp in flag_paths:
                fp = fp.replace(".txt", "")
                if (machine.ip, fp) in env_config.flag_lookup:
                    new_m_obs.flags_found.add(env_config.flag_lookup[(machine.ip, fp)])

            # Update cost
            if env_config.attacker_action_costs.find_exists(action_id=a.id, ip=machine.ip, user=c.username,
                                                            service=constants.TELNET.SERVICE_NAME):
                cost = env_config.attacker_action_costs.find_get_cost(action_id=a.id, ip=machine.ip, user=c.username,
                                                                      service=constants.TELNET.SERVICE_NAME)
                total_cost += cost

            # Update alerts
            if env_config.ids_router and env_config.attacker_action_alerts.user_ip_exists(action_id=a.id, ip=machine.ip,
                                                                                          user=c.username,
                                                                                          service=constants.TELNET.SERVICE_NAME):
                alerts = env_config.attacker_action_alerts.user_ip_get_alert(action_id=a.id, ip=machine.ip, user=c.username,
                                                                             service=constants.TELNET.SERVICE_NAME)
                total_alerts = alerts

            if c.root:
                root_scan = True
                break
        return new_m_obs, total_cost, root_scan, total_alerts

    @staticmethod
    def _find_flag_using_ftp(machine: AttackerMachineObservationState, env_config: EnvConfig, a: AttackerAction,
                             new_m_obs: AttackerMachineObservationState) \
            -> Tuple[AttackerMachineObservationState, float, bool, Tuple]:
        """
        Utility function for using existing FTP connections to a specific machine to search the file system for flags

        :param machine: the machine to search
        :param env_config: the env config
        :param a: the action of finding the flags
        :param new_m_obs: the updated machine observation with the found flags
        :return: the updated machine observation with the found flags, cost, root, alerts
        """
        total_cost = 0
        total_alerts = (0, 0)
        ftp_connections_sorted_by_root = sorted(
            machine.ftp_connections,
            key=lambda x: (constants.SSH_BACKDOOR.BACKDOOR_PREFIX in x.username, x.root, x.username),
            reverse=True)
        root_scan = False
        for c in ftp_connections_sorted_by_root:
            cache_file = \
                EmulationUtil.check_filesystem_action_cache(a=a, env_config=env_config, ip=machine.ip,
                                                            service=constants.FTP.SERVICE_NAME,
                                                            user=c.username, root=c.root)
            if cache_file is not None:
                flag_paths = EmulationUtil.parse_file_scan_file(file_name=cache_file,
                                                                env_config=env_config)
            else:
                for i in range(env_config.attacker_ftp_retry_find_flag):
                    cmd = a.alt_cmd[0] + "\n"
                    if c.root:
                        cmd = constants.COMMANDS.SUDO + " " + cmd
                    if env_config.ids_router:
                        last_alert_ts = EmulationUtil.get_latest_alert_ts(env_config=env_config)
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
                            if timeouts > env_config.shell_max_timeouts:
                                print("max timeouts FTP, env:{}".format(env_config.hacker_ip))
                                break
                            time.sleep(env_config.shell_read_wait)
                            timeouts += 1
                        if c.interactive_shell.recv_ready():
                            output += c.interactive_shell.recv(constants.COMMON.LARGE_RECV_SIZE)
                            timeouts = 0
                            if constants.FTP.LFTP_PROMPT in output.decode() \
                                    or constants.FTP.LFTP_PROMPT_2 in output.decode():
                                command_complete = True
                                end = time.time()
                                total_time = end - start
                                if env_config.ids_router:
                                    fast_logs = EmulationUtil.check_ids_fast_log(env_config=env_config)
                                    if last_alert_ts is not None:
                                        fast_logs = list(filter(lambda x: x[1] > last_alert_ts, fast_logs))
                                    sum_priority_alerts = sum(list(map(lambda x: x[0], fast_logs)))
                                    num_alerts = len(fast_logs)
                                    EmulationUtil.write_alerts_response(sum_priorities=sum_priority_alerts,
                                                                        num_alerts=num_alerts,
                                                                        action=a, env_config=env_config, ip=machine.ip,
                                                                        user=c.username,
                                                                        service=constants.FTP.SERVICE_NAME)
                                    env_config.attacker_action_alerts.user_ip_add_alert(action_id=a.id, ip=machine.ip,
                                                                                        user=c.username,
                                                                                        service=constants.FTP.SERVICE_NAME,
                                                                                        alert=(sum_priority_alerts, num_alerts))

                                EmulationUtil.write_estimated_cost(total_time=total_time, action=a,
                                                                   env_config=env_config, ip=machine.ip,
                                                                   user=c.username,
                                                                   service=constants.FTP.SERVICE_NAME)
                                env_config.attacker_action_costs.find_add_cost(action_id=a.id, ip=machine.ip, user=c.username,
                                                                               service=constants.FTP.SERVICE_NAME,
                                                                               cost=float(total_time))
                        else:
                            break

                    output_str = output.decode("utf-8")
                    output_str = env_config.shell_escape.sub("", output_str)
                    output_list = output_str.split('\r\n')
                    output_list = output_list[1:-1]  # remove command ([0]) and prompt ([-1])
                    flag_paths = list(filter(lambda x: not constants.FTP.ACCESS_FAILED in x and x != "", output_list))
                    ff = False
                    # Check for flags
                    for fp in flag_paths:
                        fp = fp.replace(".txt", "")
                        if (machine.ip, fp) in env_config.flag_lookup:
                            ff = True
                    if not ff:
                        continue
                    else:
                        break
                # Persist cache
                EmulationUtil.write_file_system_scan_cache(action=a, env_config=env_config,
                                                           service=constants.FTP.SERVICE_NAME, user=c.username,
                                                           files=flag_paths, ip=machine.ip, root=c.root)
            new_m_obs.filesystem_searched = True
            # Check for flags
            for fp in flag_paths:
                fp = fp.replace(".txt", "")
                if (machine.ip, fp) in env_config.flag_lookup:
                    new_m_obs.flags_found.add(env_config.flag_lookup[(machine.ip, fp)])

            # Update cost
            if env_config.attacker_action_costs.find_exists(action_id=a.id, ip=machine.ip, user=c.username,
                                                            service=constants.FTP.SERVICE_NAME):
                cost = env_config.attacker_action_costs.find_get_cost(action_id=a.id, ip=machine.ip, user=c.username,
                                                                      service=constants.FTP.SERVICE_NAME)
                total_cost += cost

            # Update alerts
            if env_config.ids_router and env_config.attacker_action_alerts.user_ip_exists(action_id=a.id, ip=machine.ip,
                                                                                          user=c.username,
                                                                                          service=constants.FTP.SERVICE_NAME):
                alerts = env_config.attacker_action_alerts.user_ip_get_alert(action_id=a.id, ip=machine.ip, user=c.username,
                                                                             service=constants.FTP.SERVICE_NAME)
                total_alerts = alerts

            if c.root:
                root_scan = True
                break
        return new_m_obs, total_cost, root_scan, total_alerts

    @staticmethod
    def parse_tools_installed_file(file_name: str, env_config: EnvConfig) -> List[str]:
        """
        Parses a file containing cached results of a install-tools action

        :param file_name: name of the file to parse
        :param env_config: environment config
        :return: a list of files
        """
        sftp_client = env_config.emulation_config.agent_conn.open_sftp()
        remote_file = sftp_client.open(env_config.nmap_cache_dir + file_name)
        installed = False
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
        return (
                "will be installed" in result or "already installed" in result or "already the newest version" in result)

    @staticmethod
    def install_tools_helper(s: EnvState, a: AttackerAction, env_config: EnvConfig) -> Tuple[EnvState, float, bool]:
        """
        Uses compromised machines with root access to install tools

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        new_machines_obs = []
        total_cost = 0
        total_alerts = (0, 0)
        for machine in s.attacker_obs_state.machines:
            new_m_obs = AttackerMachineObservationState(ip=machine.ip)
            installed = False
            if machine.logged_in and machine.root and not machine.tools_installed:
                # Start with ssh connections
                ssh_root_connections = filter(lambda x: x.root, machine.ssh_connections)
                ssh_root_connections = sorted(ssh_root_connections, key=lambda x: x.username)
                ssh_cost = 0
                for c in ssh_root_connections:
                    key = (machine.ip, c.username)
                    if env_config.attacker_use_user_command_cache and env_config.attacker_user_command_cache.get(key) is not None:
                        cache_m_obs, cost = env_config.attacker_user_command_cache.get(key)
                        new_m_obs.tools_installed = cache_m_obs.tools_installed
                        new_machines_obs.append(new_m_obs)
                        total_cost += cost
                        if new_m_obs.tools_installed:
                            break
                        else:
                            continue

                    cache_file = \
                        EmulationUtil.check_user_action_cache(a=a, env_config=env_config, ip=machine.ip,
                                                              user=c.username)
                    if cache_file is not None:
                        installed = ShellUtil.parse_tools_installed_file(file_name=cache_file,
                                                                           env_config=env_config)
                        new_m_obs.tools_installed = installed
                    else:
                        cmd = a.cmd[0]
                        if env_config.ids_router:
                            last_alert_ts = EmulationUtil.get_latest_alert_ts(env_config=env_config)
                        for i in range(env_config.attacker_retry_install_tools):
                            outdata, errdata, total_time = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=c.conn)
                            time.sleep(env_config.attacker_install_tools_sleep_seconds)
                            outdata = outdata.decode()
                            ssh_cost += float(total_time)
                            if ShellUtil._parse_tools_installed_check_result(result=outdata):
                                installed = True
                                new_m_obs.tools_installed = True
                            else:
                                print("tools installed failed result. out:{}, err:{}".format(outdata, errdata))
                            if installed:
                                break

                        # try to download seclists
                        seclists_installed = ShellUtil._check_if_seclists_is_installed(conn=c.conn, telnet=False)
                        if not seclists_installed:
                            cmd = a.cmd[1]
                            outdata, errdata, total_time = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=c.conn)
                            ssh_cost += float(total_time)

                        if env_config.ids_router:
                            fast_logs = EmulationUtil.check_ids_fast_log(env_config=env_config)
                            if last_alert_ts is not None:
                                fast_logs = list(filter(lambda x: x[1] > last_alert_ts, fast_logs))
                            sum_priority_alerts = sum(list(map(lambda x: x[0], fast_logs)))
                            num_alerts = len(fast_logs)
                            ssh_alerts = (sum_priority_alerts, num_alerts)
                            EmulationUtil.write_alerts_response(sum_priorities=sum_priority_alerts, num_alerts=num_alerts,
                                                                action=a, env_config=env_config, ip=machine.ip,
                                                                user=c.username)
                            env_config.attacker_action_alerts.user_ip_add_alert(action_id=a.id, ip=machine.ip, user=c.username,
                                                                                service=constants.SSH.SERVICE_NAME,
                                                                                alert=ssh_alerts)
                            total_alerts = (total_alerts[0] + ssh_alerts[0], total_alerts[1] + ssh_alerts[1])
                        EmulationUtil.write_estimated_cost(total_time=total_time, action=a,
                                                           env_config=env_config, ip=machine.ip,
                                                           user=c.username)
                        env_config.attacker_action_costs.install_add_cost(action_id=a.id, ip=machine.ip, user=c.username,
                                                                          cost=float(total_time))
                        # Persist cache
                        EmulationUtil.write_user_command_cache(action=a, env_config=env_config, user=c.username,
                                                               result=str(int(installed)), ip=machine.ip)

                    new_machines_obs.append(new_m_obs)
                    # Update cache
                    if env_config.attacker_use_user_command_cache:
                        env_config.attacker_user_command_cache.add(key, (new_m_obs, total_cost))

                    if installed:
                        break

                total_cost += ssh_cost

                # Telnet connections
                telnet_cost = 0
                if installed:
                    continue
                telnet_root_connections = filter(lambda x: x.root, machine.telnet_connections)
                telnet_root_connections = sorted(telnet_root_connections, key=lambda x: x.username)
                for c in telnet_root_connections:
                    key = (machine.ip, c.username)
                    if env_config.attacker_use_user_command_cache and env_config.attacker_user_command_cache.get(key) is not None:
                        cache_m_obs, cost = env_config.attacker_user_command_cache.get(key)
                        new_m_obs.tools_installed = cache_m_obs.tools_installed
                        new_machines_obs.append(new_m_obs)
                        total_cost += cost
                        if new_m_obs.tools_installed:
                            break
                        else:
                            continue

                    cache_file = \
                        EmulationUtil.check_user_action_cache(a=a, env_config=env_config, ip=machine.ip,
                                                              user=c.username)
                    if cache_file is not None:
                        installed = ShellUtil.parse_tools_installed_file(file_name=cache_file,
                                                                           env_config=env_config)
                        new_m_obs.tools_installed = installed
                    else:

                        # Install packages
                        cmd = a.cmd[0] + "\n"
                        start = time.time()
                        if env_config.ids_router:
                            last_alert_ts = EmulationUtil.get_latest_alert_ts(env_config=env_config)
                        for i in range(env_config.attacker_retry_install_tools):
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
                                print("tools installed failed result.{}".format(response))
                            if installed:
                                break

                        seclists_installed = ShellUtil._check_if_seclists_is_installed(conn=c.conn, telnet=True)
                        if not seclists_installed:
                            # Try to download SecLists
                            cmd = a.cmd[1] + "\n"
                            start = time.time()
                            c.conn.write(cmd.encode())
                            response = c.conn.read_until(constants.TELNET.PROMPT, timeout=2000)
                            response = response.decode()
                            end = time.time()
                            total_time = end - start
                            telnet_cost += float(total_time)

                        if env_config.ids_router:
                            fast_logs = EmulationUtil.check_ids_fast_log(env_config=env_config)
                            if last_alert_ts is not None:
                                fast_logs = list(filter(lambda x: x[1] > last_alert_ts, fast_logs))
                            sum_priority_alerts = sum(list(map(lambda x: x[0], fast_logs)))
                            num_alerts = len(fast_logs)
                            telnet_alerts = (sum_priority_alerts, num_alerts)
                            EmulationUtil.write_alerts_response(sum_priorities=sum_priority_alerts, num_alerts=num_alerts,
                                                                action=a, env_config=env_config, ip=machine.ip,
                                                                user=c.username, service=constants.TELNET.SERVICE_NAME)
                            env_config.attacker_action_alerts.user_ip_add_alert(action_id=a.id, ip=machine.ip, user=c.username,
                                                                                service=constants.TELNET.SERVICE_NAME,
                                                                                alert=telnet_alerts)
                            total_alerts = (total_alerts[0] + telnet_alerts[0], total_alerts[1] + telnet_alerts[1])

                        EmulationUtil.write_estimated_cost(total_time=total_time, action=a,
                                                           env_config=env_config, ip=machine.ip,
                                                           user=c.username)
                        env_config.attacker_action_costs.install_add_cost(action_id=a.id, ip=machine.ip, user=c.username,
                                                                          cost=float(total_time))
                        # Persist cache
                        EmulationUtil.write_user_command_cache(action=a, env_config=env_config, user=c.username,
                                                               result=str(int(installed)), ip=machine.ip)

                    new_machines_obs.append(new_m_obs)

                    # Update cache
                    if env_config.attacker_use_user_command_cache:
                        env_config.attacker_user_command_cache.add(key, (new_m_obs, total_cost))

                    if installed:
                        break

                new_m_obs.install_tools_tried = True

                total_cost += telnet_cost
        net_outcome = EnvDynamicsUtil.merge_new_obs_with_old(s.attacker_obs_state.machines, new_machines_obs,
                                                             env_config=env_config, action=a)
        s_prime = s
        s_prime.attacker_obs_state.machines = net_outcome.attacker_machine_observations

        reward = EnvDynamicsUtil.reward_function(net_outcome=net_outcome, env_config=env_config, action=a)

        # Emulate detection
        done, d_reward = EnvDynamicsUtil.emulate_detection(net_outcome=net_outcome, action=a, env_config=env_config)
        if done:
            reward = d_reward
        s_prime.attacker_obs_state.detected = done

        return s_prime, reward, done

    @staticmethod
    def _check_if_seclists_is_installed(conn, telnet: bool = False) -> bool:
        """
        Checks if seclists are downloaded

        :param conn: the connection to use for the command
        :param telnet: whether the connection is a telnet connection
        :return: True if downloaded, else false
        """
        cmd = constants.SHELL.CHECK_FOR_SECLISTS
        if not telnet:
            for i in range(8):
                outdata, errdata, total_time = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=conn)
                checklists_installed = "file exists" in outdata.decode() or "file exists" in errdata.decode()
                if checklists_installed:
                    break
                else:
                    print("checklists not installed:{}, {}".format(outdata.decode(), errdata.decode()))
            return checklists_installed
        else:
            cmd = cmd + "\n"
            conn.write(cmd.encode())
            response = conn.read_until(constants.TELNET.PROMPT, timeout=5)
            return "file exists" in response.decode()


    @staticmethod
    def execute_ssh_backdoor_helper(s: EnvState, a: AttackerAction, env_config: EnvConfig) \
            -> Tuple[EnvState, float, bool]:
        """
        Uses compromised machines with root access to setup SSH backdoor

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        username = constants.SSH_BACKDOOR.BACKDOOR_PREFIX + "_" + str(random.randint(0, 100000))
        pw = constants.SSH_BACKDOOR.DEFAULT_PW
        new_machines_obs = []
        total_cost = 0
        total_alerts = (0, 0)
        for machine in s.attacker_obs_state.machines:
            new_m_obs = AttackerMachineObservationState(ip=machine.ip)
            backdoor_created = False
            if machine.logged_in and machine.root and machine.tools_installed and not machine.backdoor_installed:
                new_m_obs.backdoor_tried = True
                # Check cached connections
                for cr in s.attacker_cached_backdoor_credentials.values():
                    if (machine.ip, cr.username, cr.port) in s.attacker_cached_ssh_connections:
                        conn_dto = s.attacker_cached_ssh_connections[(machine.ip, cr.username, cr.port)]
                        connection_dto = ConnectionObservationState(conn=conn_dto.conn, username=cr.username,
                                                                    root=machine.root,
                                                                    service=constants.SSH.SERVICE_NAME,
                                                                    port=cr.port, ip=machine.ip)
                        new_m_obs.shell_access_credentials.append(cr)
                        new_m_obs.backdoor_credentials.append(cr)
                        new_m_obs.ssh_connections.append(connection_dto)
                        new_m_obs.backdoor_installed = True
                        new_machines_obs.append(new_m_obs)
                        backdoor_created = True

                if backdoor_created:
                    continue

                # Try first to setup new ssh connections
                ssh_root_connections = list(filter(lambda x: x.root, machine.ssh_connections))
                ssh_root_connections = sorted(ssh_root_connections, key=lambda x: x.username)
                ssh_cost = 0
                for c in ssh_root_connections:
                    #try:
                    users = EmulationUtil._list_all_users(c, env_config=env_config)
                    users = sorted(users, key=lambda x: x)
                    user_exists = False
                    for user in users:
                        if constants.SSH_BACKDOOR.BACKDOOR_PREFIX in user:
                            user_exists = True
                            username = user

                    if not user_exists:
                        # Create user
                        create_user_cmd = a.cmd[1].format(username, pw, username)
                        outdata, errdata, total_time = EmulationUtil.execute_ssh_cmd(cmd=create_user_cmd, conn=c.conn)
                        ssh_cost += float(total_time)

                    credential = Credential(username=username, pw=pw, port=22, service="ssh")

                    # Start SSH Server
                    ssh_running = EmulationUtil._check_if_ssh_server_is_running(c.conn)
                    if not ssh_running:
                        start_ssh_cmd = a.cmd[0]
                        outdata, errdata, total_time = EmulationUtil.execute_ssh_cmd(cmd=start_ssh_cmd, conn=c.conn)
                        ssh_cost += float(total_time)

                    # Create SSH connection
                    new_m_obs.shell_access_credentials.append(credential)
                    new_m_obs.backdoor_credentials.append(credential)
                    a.ip = machine.ip
                    for i in range(5):
                        setup_connection_dto = ConnectionUtil._ssh_setup_connection(
                            a=a, env_config=env_config, credentials=[credential], proxy_connections=[c.proxy], s=s)
                        ssh_cost += setup_connection_dto.total_time
                        if len(setup_connection_dto.target_connections) > 0:
                            break
                        else:
                            time.sleep(5)

                    if len(setup_connection_dto.target_connections) == 0:
                        print("cannot install backdoor, machine:{}, credentials:{}".format(machine.ip, credential))

                    connection_dto = ConnectionObservationState(conn=setup_connection_dto.target_connections[0],
                                                                username=credential.username,
                                                                root=machine.root,
                                                                service=constants.SSH.SERVICE_NAME,
                                                                port=credential.port,
                                                                proxy=setup_connection_dto.proxies[0],
                                                                ip=machine.ip)
                    new_m_obs.ssh_connections.append(connection_dto)
                    new_m_obs.backdoor_installed = True
                    new_machines_obs.append(new_m_obs)
                    backdoor_created = True
                    # except Exception as e:
                    #     raise ValueError("Creating Backdoor Exception: {}, target:{}, proxy:{}".format(
                    #         str(e), a.ip, c.proxy.ip))

                    if backdoor_created:
                        break

                total_cost += ssh_cost

                # Telnet connections
                telnet_cost = 0
                if backdoor_created:
                    continue
                telnet_root_connections = filter(lambda x: x.root, machine.telnet_connections)
                telnet_root_connections = sorted(telnet_root_connections, key=lambda x: x.username)
                for c in telnet_root_connections:
                    try:
                        users = EmulationUtil._list_all_users(c, env_config=env_config, telnet=True)
                        user_exists = False
                        for user in users:
                            if constants.SSH_BACKDOOR.BACKDOOR_PREFIX in user:
                                user_exists = True
                                username = user

                        credential = Credential(username=username, pw=pw, port=22, service="ssh")

                        if not user_exists:
                            # Create user
                            create_user_cmd = a.cmd[1].format(username, pw, username) + "\n"
                            c.conn.write(create_user_cmd.encode())
                            response = c.conn.read_until(constants.TELNET.PROMPT, timeout=5)

                        ssh_running = EmulationUtil._check_if_ssh_server_is_running(c.conn, telnet=True)
                        if not ssh_running:
                            # Start SSH Server
                            start_ssh_cmd = a.cmd[0] + "\n"
                            c.conn.write(start_ssh_cmd.encode())
                            response = c.conn.read_until(constants.TELNET.PROMPT, timeout=5)

                        # Create SSH connection
                        new_m_obs.shell_access_credentials.append(credential)
                        new_m_obs.backdoor_credentials.append(credential)
                        a.ip = machine.ip
                        setup_connection_dto = ConnectionUtil._ssh_setup_connection(
                            a=a, env_config=env_config, credentials=[credential], proxy_connections=[c.proxy], s=s)
                        telnet_cost += setup_connection_dto.total_time
                        connection_dto = ConnectionObservationState(conn=setup_connection_dto.target_connections[0],
                                                                    username=credential.username,
                                                                    root=machine.root,
                                                                    service=constants.SSH.SERVICE_NAME,
                                                                    port=credential.port,
                                                                    proxy=setup_connection_dto.proxies[0],
                                                                    ip=machine.ip)
                        new_m_obs.ssh_connections.append(connection_dto)
                        new_m_obs.backdoor_installed = True
                        new_machines_obs.append(new_m_obs)
                        backdoor_created = True
                    except Exception as e:
                        pass
                        # raise ValueError("Creating Backdoor Exception: {}, target:{}, proxy:{}".format(str(e), a.ip,
                        #                                                                                c.proxy.ip))
                    if backdoor_created:
                        break

                total_cost += telnet_cost
        # if not backdoor_created:
        #     print("failed to create backdoor, target:{}".format(a.ip))
        net_outcome = EnvDynamicsUtil.merge_new_obs_with_old(s.attacker_obs_state.machines, new_machines_obs,
                                                             env_config=env_config, action=a)
        s_prime = s
        s_prime.attacker_obs_state.machines = net_outcome.attacker_machine_observations

        reward = EnvDynamicsUtil.reward_function(net_outcome=net_outcome, env_config=env_config, action=a)

        # Emulate detection
        done, d_reward = EnvDynamicsUtil.emulate_detection(net_outcome=net_outcome, action=a, env_config=env_config)
        if done:
            reward = d_reward
        s_prime.attacker_obs_state.detected = done

        return s_prime, reward, done

    @staticmethod
    def execute_service_login_helper(s: EnvState, a: AttackerAction, env_config: EnvConfig) \
            -> Tuple[EnvState, float, bool]:
        """
        Executes a service login on the emulation using previously found credentials

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime = s
        new_conn = False

        if env_config.ids_router:
            last_alert_ts = EmulationUtil.get_latest_alert_ts(env_config=env_config)

        for machine in s.attacker_obs_state.machines:
            a.ip = machine.ip
            s_1, net_out_1, new_conn_ssh = ConnectionUtil.login_service_helper(
                s=s_prime, a=a, alive_check=EnvDynamicsUtil.check_if_ssh_connection_is_alive,
                service_name=constants.SSH.SERVICE_NAME, env_config=env_config)
            s_2, net_out_2, new_conn_ftp = ConnectionUtil.login_service_helper(
                s=s_1, a=a, alive_check=EnvDynamicsUtil.check_if_ftp_connection_is_alive,
                service_name=constants.FTP.SERVICE_NAME, env_config=env_config)
            s_3, net_out_3, new_conn_telnet = ConnectionUtil.login_service_helper(
                s=s_2, a=a, alive_check=EnvDynamicsUtil.check_if_telnet_connection_is_alive,
                service_name=constants.TELNET.SERVICE_NAME, env_config=env_config)

            net_out_merged = net_out_1
            net_out_merged.update_counts(net_out_2)
            net_out_merged.update_counts(net_out_3)

            s_prime = s_3
            if new_conn_ssh or new_conn_ftp or new_conn_telnet:
                new_conn = True

            for m in s_prime.attacker_obs_state.machines:
                if m.ip == a.ip:
                    m.untried_credentials = False

        # Update cost cache
        total_cost = round(net_out_merged.cost, 1)
        if new_conn:
            env_config.attacker_action_costs.service_add_cost(action_id=a.id, ip=env_config.emulation_config.agent_ip,
                                                              cost=float(total_cost))

        # Update alerts cache
        if env_config.ids_router and new_conn:
            fast_logs = EmulationUtil.check_ids_fast_log(env_config=env_config)
            if last_alert_ts is not None:
                fast_logs = list(filter(lambda x: x[1] > last_alert_ts, fast_logs))
            sum_priority_alerts = sum(list(map(lambda x: x[0], fast_logs)))
            num_alerts = len(fast_logs)
            env_config.attacker_action_alerts.add_alert(action_id=a.id, ip=env_config.emulation_config.agent_ip,
                                                        alert=(sum_priority_alerts, num_alerts))

        a.ip = ""

        # Use measured cost
        if env_config.attacker_action_costs.service_exists(action_id=a.id, ip=env_config.emulation_config.agent_ip):
            a.cost = env_config.attacker_action_costs.service_get_cost(action_id=a.id, ip=env_config.emulation_config.agent_ip)

        # Use measured alerts
        if env_config.attacker_action_alerts.exists(action_id=a.id, ip=env_config.emulation_config.agent_ip):
            a.alerts = env_config.attacker_action_alerts.get_alert(action_id=a.id, ip=env_config.emulation_config.agent_ip)

        reward = EnvDynamicsUtil.reward_function(net_outcome=net_out_merged, env_config=env_config, action=a)

        # Emulate detection
        done, d_reward = EnvDynamicsUtil.emulate_detection(net_outcome=net_out_merged, action=a,
                                                           env_config=env_config)
        if done:
            reward = d_reward
        s_prime.attacker_obs_state.detected = done
        return s_prime, reward, done