from typing import Tuple
from gym_pycr_ctf.dao.network.env_state import EnvState
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.action.defender.defender_action import DefenderAction
from gym_pycr_ctf.envs_model.logic.emulation.util.defender.read_logs_util import ReadLogsUtil
from gym_pycr_ctf.envs_model.logic.emulation.util.defender.shell_util import ShellUtil
from gym_pycr_ctf.envs_model.logic.emulation.util.common.emulation_util import EmulationUtil
from gym_pycr_ctf.dao.state_representation.state_type import StateType
from gym_pycr_ctf.dao.observation.common.connection_observation_state import ConnectionObservationState
import gym_pycr_ctf.constants.constants as constants

class DefenderUpdateStateMiddleware:
    """
    Class that implements update state actions for the defender.
    """

    @staticmethod
    def update_belief_state(s: EnvState, a: DefenderAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Updates the defender's state by measuring the emulation

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime = s

        # Measure IDS
        if env_config.ids_router:
            num_alerts, num_severe_alerts, num_warning_alerts, sum_priority_alerts = \
                ReadLogsUtil.read_ids_data(env_config=env_config,
                                           episode_last_alert_ts=s_prime.defender_obs_state.last_alert_ts)

            s_prime.defender_obs_state.num_alerts_recent = num_alerts
            s_prime.defender_obs_state.num_severe_alerts_recent = num_severe_alerts
            s_prime.defender_obs_state.num_warning_alerts_recent = num_warning_alerts
            s_prime.defender_obs_state.sum_priority_alerts_recent = sum_priority_alerts

            s_prime.defender_obs_state.num_alerts_total = num_alerts + \
                                                          s_prime.defender_obs_state.num_alerts_recent
            s_prime.defender_obs_state.num_severe_alerts_total = num_severe_alerts + \
                                                                 s_prime.defender_obs_state.num_severe_alerts_recent
            s_prime.defender_obs_state.num_warning_alerts_total = num_warning_alerts + \
                                                                  s_prime.defender_obs_state.num_warning_alerts_recent
            s_prime.defender_obs_state.sum_priority_alerts_total = sum_priority_alerts + \
                                                                   s_prime.defender_obs_state.sum_priority_alerts_recent
            s_prime.defender_obs_state.last_alert_ts = EmulationUtil.get_latest_alert_ts(env_config=env_config)

        if s_prime.state_type == StateType.BASE or s_prime.state_type == s_prime.StateType.ESSENTIAL \
                or s_prime.state_type == StateType.COMPACT:

            # Measure Node specific features
            for m in s_prime.defender_obs_state.machines:
                # Measure metrics of the node
                num_logged_in_users = ShellUtil.read_logged_in_users(emulation_config=m.emulation_config)
                m.num_logged_in_users_recent = num_logged_in_users - m.num_logged_in_users
                m.num_logged_in_users = num_logged_in_users

                num_failed_login_attempts = ReadLogsUtil.read_failed_login_attempts(
                    emulation_config=m.emulation_config, failed_auth_last_ts=m.failed_auth_last_ts)
                m.num_failed_login_attempts_recent = num_failed_login_attempts
                m.num_failed_login_attempts = num_failed_login_attempts + m.num_failed_login_attempts_recent

                num_open_connections = ShellUtil.read_open_connections(emulation_config=m.emulation_config)
                if num_open_connections == -1:
                    m.num_open_connections_recent = 0
                else:
                    m.num_open_connections_recent = num_open_connections - m.num_open_connections
                    m.num_open_connections = num_open_connections

                if s_prime.state_type != StateType.COMPACT:
                    num_login_events = ReadLogsUtil.read_successful_login_events(
                        emulation_config=m.emulation_config, login_last_ts=m.login_last_ts)
                    m.num_login_events_recent = num_login_events
                    m.num_login_events = num_login_events + m.num_login_events_recent

                if s_prime.state_type == StateType.BASE:

                    num_processes = ShellUtil.read_processes(emulation_config=m.emulation_config)
                    if num_processes == -1:
                        m.num_processes_recent = 0
                    else:
                        m.num_processes_recent = num_processes - m.num_processes
                        m.num_processes = num_processes

                    num_users = ShellUtil.read_users(emulation_config=m.emulation_config)
                    m.num_users_recent = num_users - m.num_users
                    m.num_users = num_users

                m.failed_auth_last_ts = ReadLogsUtil.read_latest_ts_auth(emulation_config=m.emulation_config)
                m.login_last_ts = ReadLogsUtil.read_latest_ts_login(emulation_config=m.emulation_config)

        s_prime.defender_obs_state.step = s_prime.defender_obs_state.step + 1

        return s_prime, 0, False

    @staticmethod
    def initialize_state(s: EnvState, a: DefenderAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Initializes the defender's state by measuring the emulation

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime = s

        s_prime.defender_obs_state.adj_matrix = env_config.network_conf.adj_matrix

        # Measure IDS
        if env_config.ids_router:
            s_prime.defender_obs_state.last_alert_ts = EmulationUtil.get_latest_alert_ts(env_config=env_config)

            s_prime.defender_obs_state.num_alerts_recent = 0
            s_prime.defender_obs_state.num_severe_alerts_recent = 0
            s_prime.defender_obs_state.num_warning_alerts_recent = 0
            s_prime.defender_obs_state.sum_priority_alerts_recent = 0

            s_prime.defender_obs_state.num_alerts_total = 0
            s_prime.defender_obs_state.sum_priority_alerts_total = 0
            s_prime.defender_obs_state.num_severe_alerts_total = 0
            s_prime.defender_obs_state.num_warning_alerts_total = 0

        # Measure Node specific features
        for node in env_config.network_conf.nodes:
            if node.ip == env_config.emulation_config.agent_ip:
                continue
            d_obs = node.to_defender_machine_obs(s.service_lookup)

            # Setup connection
            if node.ip in s_prime.defender_cached_ssh_connections:
                (node_connections, ec) = s_prime.defender_cached_ssh_connections[node.ip]
                node_conn = node_connections[0]
            else:
                ec = env_config.emulation_config.copy(ip=node.ip, username=constants.PYCR_ADMIN.user,
                                                      pw=constants.PYCR_ADMIN.pw)
                ec.connect_agent()
                node_conn = ConnectionObservationState(
                    conn=ec.agent_conn, username=ec.agent_username, root=True, port=22,
                    service=constants.SSH.SERVICE_NAME, proxy=None, ip=node.ip)
            d_obs.ssh_connections.append(node_conn)
            d_obs.emulation_config = ec

            # Measure metrics of the node
            d_obs.failed_auth_last_ts = ReadLogsUtil.read_latest_ts_auth(emulation_config=d_obs.emulation_config)
            d_obs.login_last_ts = ReadLogsUtil.read_latest_ts_login(emulation_config=d_obs.emulation_config)

            num_logged_in_users = ShellUtil.read_logged_in_users(emulation_config=d_obs.emulation_config)
            d_obs.num_logged_in_users = num_logged_in_users

            num_open_connections = ShellUtil.read_open_connections(emulation_config=d_obs.emulation_config)
            d_obs.num_open_connections = num_open_connections

            num_processes = ShellUtil.read_processes(emulation_config=d_obs.emulation_config)
            d_obs.num_processes = num_processes

            num_users = ShellUtil.read_users(emulation_config=d_obs.emulation_config)
            d_obs.num_users = num_users

            d_obs.num_failed_login_attempts = 0
            d_obs.num_login_events = 0
            d_obs.num_open_connections_recent = 0
            d_obs.num_failed_login_attempts_recent = 0
            d_obs.num_users_recent = 0
            d_obs.num_logged_in_users_recent = 0
            d_obs.num_login_events_recent = 0
            d_obs.num_processes_recent = 0

            s_prime.defender_obs_state.machines.append(d_obs)

        s_prime.defender_obs_state.step = 0

        return s_prime, 0, False

    @staticmethod
    def reset_state(s: EnvState, a: DefenderAction, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Resets the defender's state

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime = s

        # Reset stopped state
        s_prime.defender_obs_state.caught_attacker = False
        s_prime.defender_obs_state.stopped = False

        # Reset ids states
        s_prime.defender_obs_state.num_alerts_recent = 0
        s_prime.defender_obs_state.num_severe_alerts_recent = 0
        s_prime.defender_obs_state.num_warning_alerts_recent = 0
        s_prime.defender_obs_state.sum_priority_alerts_recent = 0

        s_prime.defender_obs_state.num_alerts_total = 0
        s_prime.defender_obs_state.sum_priority_alerts_total = 0
        s_prime.defender_obs_state.num_severe_alerts_total = 0
        s_prime.defender_obs_state.num_warning_alerts_total = 0

        # Update IDS timestamp
        if env_config.ids_router:
            s_prime.defender_obs_state.last_alert_ts = EmulationUtil.get_latest_alert_ts(env_config=env_config)

        # Update logs timestamps and reset machine states
        for m in s_prime.defender_obs_state.machines:
            m.failed_auth_last_ts = ReadLogsUtil.read_latest_ts_auth(emulation_config=m.emulation_config)
            m.login_last_ts = ReadLogsUtil.read_latest_ts_login(emulation_config=m.emulation_config)

            num_logged_in_users = ShellUtil.read_logged_in_users(emulation_config=m.emulation_config)
            m.num_logged_in_users = num_logged_in_users

            num_open_connections = ShellUtil.read_open_connections(emulation_config=m.emulation_config)
            m.num_open_connections = num_open_connections

            if s_prime.state_type == StateType.BASE:
                num_processes = ShellUtil.read_processes(emulation_config=m.emulation_config)
                m.num_processes = num_processes

                num_users = ShellUtil.read_users(emulation_config=m.emulation_config)
                m.num_users = num_users

            m.num_failed_login_attempts = 0
            m.num_login_events = 0
            m.num_open_connections_recent = 0
            m.num_failed_login_attempts_recent = 0
            m.num_users_recent = 0
            m.num_logged_in_users_recent = 0
            m.num_login_events_recent = 0
            m.num_processes_recent = 0

        s_prime.defender_obs_state.step = 0

        return s_prime, 0, False