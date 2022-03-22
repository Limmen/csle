from typing import Tuple, Union
import csle_common.constants.constants as constants
from csle_common.envs_model.logic.emulation.util.defender.read_logs_util import ReadLogsUtil
from csle_common.envs_model.logic.emulation.util.defender.shell_util import ShellUtil
from csle_common.envs_model.logic.emulation.util.common.emulation_util import EmulationUtil
from csle_common.dao.state_representation.state_type import StateType
from csle_common.dao.observation.common.connection_observation_state import ConnectionObservationState
from gym_csle_ctf.dao.network.env_state import EnvState
from gym_csle_ctf.dao.network.env_config import CSLEEnvConfig
from gym_csle_ctf.dao.action.defender.defender_action import DefenderAction
from gym_csle_ctf.dao.action.attacker.attacker_action import AttackerAction
from gym_csle_ctf.dao.observation.defender.defender_observation_state import DefenderObservationState
from gym_csle_ctf.dao.observation.defender.defender_machine_observation_state import DefenderMachineObservationState


class DefenderUpdateStateMiddleware:
    """
    Class that implements update state actions for the defender.
    """

    @staticmethod
    def update_belief_state(s: EnvState, defender_action: DefenderAction, attacker_action: AttackerAction,
                            env_config: CSLEEnvConfig) -> Tuple[EnvState, float, bool]:
        """
        Updates the defender's state by measuring the emulation

        :param s: the current state
        :param defender_action: the action to take
        :param attacker_action: the attacker's previous action
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime = s

        aggregated_stats, avg_stats_dict = s_prime.docker_stats_thread.compute_averages()
        DefenderUpdateStateMiddleware.__update_docker_stats(s_prime.defender_obs_state, aggregated_stats)

        # Measure IDS
        if env_config.ids_router:

            if env_config.use_attacker_action_stats_to_update_defender_state:
                num_new_alerts = attacker_action.alerts[0]
                num_new_priority = attacker_action.alerts[1]
                num_new_severe_alerts = num_new_alerts / 2
                num_new_warning_alerts = num_new_alerts / 2
            else:
                num_new_alerts, num_new_severe_alerts, num_new_warning_alerts, num_new_priority = \
                    ReadLogsUtil.read_ids_data(env_config=env_config,
                                               episode_last_alert_ts=s_prime.defender_obs_state.last_alert_ts)

            s_prime.defender_obs_state.num_alerts_total = s_prime.defender_obs_state.num_alerts_total + \
                                                          num_new_alerts
            s_prime.defender_obs_state.num_severe_alerts_total = s_prime.defender_obs_state.num_severe_alerts_total + \
                                                                 num_new_severe_alerts
            s_prime.defender_obs_state.num_warning_alerts_total = s_prime.defender_obs_state.num_warning_alerts_total + \
                                                                  num_new_warning_alerts
            s_prime.defender_obs_state.sum_priority_alerts_total = s_prime.defender_obs_state.sum_priority_alerts_total + \
                                                                   num_new_priority
            s_prime.defender_obs_state.num_login_attempts_total = sum(list(map(lambda x: x.num_failed_login_attempts,
                                                                               s_prime.defender_obs_state.machines)))
            s_prime.defender_obs_state.num_warning_alerts_total_all_stops = \
                s_prime.defender_obs_state.num_warning_alerts_total_all_stops + \
                                                                  num_new_warning_alerts
            s_prime.defender_obs_state.sum_priority_alerts_total_all_stops = \
                s_prime.defender_obs_state.sum_priority_alerts_total_all_stops + \
                                                                   num_new_priority
            s_prime.defender_obs_state.num_login_attempts_total_all_stops = sum(
                list(map(lambda x: x.num_failed_login_attempts, s_prime.defender_obs_state.machines)))

            s_prime.defender_obs_state.num_alerts_recent = num_new_alerts
            s_prime.defender_obs_state.num_severe_alerts_recent = num_new_severe_alerts
            s_prime.defender_obs_state.num_warning_alerts_recent = num_new_warning_alerts
            s_prime.defender_obs_state.sum_priority_alerts_recent = num_new_priority


        if s_prime.state_type == StateType.BASE or s_prime.state_type == StateType.ESSENTIAL \
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
                m.num_failed_login_attempts = m.num_failed_login_attempts + m.num_failed_login_attempts_recent

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
                    m.num_login_events = m.num_login_events + m.num_login_events_recent

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

                if m.ip in avg_stats_dict:
                    DefenderUpdateStateMiddleware.__update_docker_stats(m, avg_stats_dict[m.ip])

                    m.failed_auth_last_ts = ReadLogsUtil.read_latest_ts_auth(emulation_config=m.emulation_config)
                    m.login_last_ts = ReadLogsUtil.read_latest_ts_login(emulation_config=m.emulation_config)

        s_prime.defender_obs_state.step = s_prime.defender_obs_state.step + 1

        if env_config.ids_router:
            s_prime.defender_obs_state.last_alert_ts = EmulationUtil.get_latest_alert_ts(env_config=env_config)

        return s_prime, 0, False

    @staticmethod
    def initialize_state(s: EnvState, defender_action: DefenderAction, attacker_action: AttackerAction,
                         env_config: CSLEEnvConfig) -> Tuple[EnvState, float, bool]:
        """
        Initializes the defender's state by measuring the emulation

        :param s: the current state
        :param defender_action: the action to take
        :param attacker_action: the attacker's previous action
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime = s

        aggregated_stats, avg_stats_dict = s_prime.docker_stats_thread.compute_averages()
        DefenderUpdateStateMiddleware.__update_docker_stats(s_prime.defender_obs_state, aggregated_stats)

        s_prime.defender_obs_state.adj_matrix = env_config.network_conf.adj_matrix

        # Measure Node specific features
        for node in env_config.network_conf.nodes:
            if node.ip == env_config.emulation_config.agent_ip:
                continue
            d_obs = DefenderMachineObservationState.from_node(node,s.service_lookup)

            # Setup connection
            if node.ip in s_prime.defender_cached_ssh_connections:
                (node_connections, ec) = s_prime.defender_cached_ssh_connections[node.ip]
                node_conn = node_connections[0]
            else:
                ec = env_config.emulation_config.copy(ip=node.ip, username=constants.CSLE_ADMIN.USER,
                                                      pw=constants.CSLE_ADMIN.PW)
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

            if d_obs.ip in avg_stats_dict:
                DefenderUpdateStateMiddleware.__update_docker_stats(d_obs, avg_stats_dict[d_obs.ip])

            s_prime.defender_obs_state.machines.append(d_obs)


        # Measure IDS (This has to be after the setup of machine-connections to make sure the time-stamp is correct.
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
            s_prime.defender_obs_state.num_login_attempts_total = 0

            s_prime.defender_obs_state.num_alerts_total_all_stops = 0
            s_prime.defender_obs_state.sum_priority_alerts_total_all_stops = 0
            s_prime.defender_obs_state.num_severe_alerts_total_all_stops = 0
            s_prime.defender_obs_state.num_warning_alerts_total_all_stops = 0
            s_prime.defender_obs_state.num_login_attempts_total_all_stops = 0

        s_prime.defender_obs_state.step = 1
        s_prime.defender_obs_state.snort_warning_baseline_reward = 0
        s_prime.defender_obs_state.snort_severe_baseline_reward = 0
        s_prime.defender_obs_state.snort_critical_baseline_reward = 0
        s_prime.defender_obs_state.var_log_baseline_reward = 0
        s_prime.defender_obs_state.step_baseline_reward = 0
        s_prime.defender_obs_state.snort_warning_baseline_step = 1
        s_prime.defender_obs_state.snort_severe_baseline_step = 1
        s_prime.defender_obs_state.snort_critical_baseline_step = 1
        s_prime.defender_obs_state.var_log_baseline_step = 1
        s_prime.defender_obs_state.step_baseline_step = 1
        s_prime.defender_obs_state.snort_warning_baseline_stopped = False
        s_prime.defender_obs_state.snort_severe_baseline_stopped = False
        s_prime.defender_obs_state.snort_critical_baseline_stopped = False
        s_prime.defender_obs_state.var_log_baseline_stopped = False
        s_prime.defender_obs_state.step_baseline_stopped = False
        s_prime.defender_obs_state.snort_severe_baseline_caught_attacker = False
        s_prime.defender_obs_state.snort_warning_baseline_caught_attacker = False
        s_prime.defender_obs_state.snort_critical_baseline_caught_attacker = False
        s_prime.defender_obs_state.var_log_baseline_caught_attacker = False
        s_prime.defender_obs_state.step_baseline_caught_attacker = False
        s_prime.defender_obs_state.snort_severe_baseline_early_stopping = False
        s_prime.defender_obs_state.snort_warning_baseline_early_stopping = False
        s_prime.defender_obs_state.snort_critical_baseline_early_stopping = False
        s_prime.defender_obs_state.var_log_baseline_early_stopping = False
        s_prime.defender_obs_state.step_baseline_early_stopping = False
        s_prime.defender_obs_state.snort_severe_baseline_uncaught_intrusion_steps = 0
        s_prime.defender_obs_state.snort_warning_baseline_uncaught_intrusion_steps = 0
        s_prime.defender_obs_state.snort_critical_baseline_uncaught_intrusion_steps = 0
        s_prime.defender_obs_state.var_log_baseline_uncaught_intrusion_steps = 0
        s_prime.defender_obs_state.step_baseline_uncaught_intrusion_steps = 0
        s_prime.defender_obs_state.stops_remaining = s_prime.defender_obs_state.maximum_number_of_stops
        s_prime.defender_obs_state.first_stop_step = -1
        s_prime.defender_obs_state.second_stop_step = -1
        s_prime.defender_obs_state.third_stop_step = -1
        s_prime.defender_obs_state.fourth_stop_step = -1
        s_prime.defender_obs_state.first_stop_step = -1
        s_prime.defender_obs_state.second_stop_step = -1
        s_prime.defender_obs_state.third_stop_step = -1
        s_prime.defender_obs_state.fourth_stop_step = -1
        s_prime.defender_obs_state.snort_severe_baseline_first_stop_step = 0
        s_prime.defender_obs_state.snort_warning_baseline_first_stop_step = 0
        s_prime.defender_obs_state.snort_critical_baseline_first_stop_step = 0
        s_prime.defender_obs_state.var_log_baseline_first_stop_step = 0
        s_prime.defender_obs_state.step_baseline_first_stop_step = 0
        s_prime.defender_obs_state.snort_severe_baseline_second_stop_step = 0
        s_prime.defender_obs_state.snort_warning_baseline_second_stop_step = 0
        s_prime.defender_obs_state.snort_critical_baseline_second_stop_step = 0
        s_prime.defender_obs_state.var_log_baseline_second_stop_step = 0
        s_prime.defender_obs_state.step_baseline_second_stop_step = 0
        s_prime.defender_obs_state.snort_severe_baseline_third_stop_step = 0
        s_prime.defender_obs_state.snort_warning_baseline_third_stop_step = 0
        s_prime.defender_obs_state.snort_critical_baseline_third_stop_step = 0
        s_prime.defender_obs_state.var_log_baseline_third_stop_step = 0
        s_prime.defender_obs_state.step_baseline_third_stop_step = 0
        s_prime.defender_obs_state.snort_severe_baseline_fourth_stop_step = 0
        s_prime.defender_obs_state.snort_warning_baseline_fourth_stop_step = 0
        s_prime.defender_obs_state.snort_critical_baseline_fourth_stop_step = 0
        s_prime.defender_obs_state.var_log_baseline_fourth_stop_step = 0
        s_prime.defender_obs_state.step_baseline_fourth_stop_step = 0
        s_prime.defender_obs_state.snort_severe_baseline_stops_remaining = s_prime.defender_obs_state.maximum_number_of_stops
        s_prime.defender_obs_state.snort_warning_baseline_stops_remaining = s_prime.defender_obs_state.maximum_number_of_stops
        s_prime.defender_obs_state.snort_critical_baseline_stops_remaining = s_prime.defender_obs_state.maximum_number_of_stops
        s_prime.defender_obs_state.var_log_baseline_stops_remaining = s_prime.defender_obs_state.maximum_number_of_stops
        s_prime.defender_obs_state.step_baseline_stops_remaining = s_prime.defender_obs_state.maximum_number_of_stops

        return s_prime, 0, False

    @staticmethod
    def reset_state(s: EnvState, defender_action: DefenderAction, env_config: CSLEEnvConfig,
                    attacker_action: AttackerAction) -> Tuple[EnvState, float, bool]:
        """
        Resets the defender's state

        :param s: the current state
        :param defender_action: the action to take
        :param attacker_action: the attacker's previous action
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

        s_prime.defender_obs_state.step = 1
        s_prime.defender_obs_state.snort_warning_baseline_reward = 0
        s_prime.defender_obs_state.snort_severe_baseline_reward = 0
        s_prime.defender_obs_state.snort_critical_baseline_reward = 0
        s_prime.defender_obs_state.var_log_baseline_reward = 0
        s_prime.defender_obs_state.step_baseline_reward = 0
        s_prime.defender_obs_state.snort_warning_baseline_step = 1
        s_prime.defender_obs_state.snort_severe_baseline_step = 1
        s_prime.defender_obs_state.snort_critical_baseline_step = 1
        s_prime.defender_obs_state.var_log_baseline_step = 1
        s_prime.defender_obs_state.step_baseline_step = 1
        s_prime.defender_obs_state.snort_warning_baseline_stopped = False
        s_prime.defender_obs_state.snort_severe_baseline_stopped = False
        s_prime.defender_obs_state.snort_critical_baseline_stopped = False
        s_prime.defender_obs_state.var_log_baseline_stopped = False
        s_prime.defender_obs_state.step_baseline_stopped = False
        s_prime.defender_obs_state.snort_severe_baseline_caught_attacker = False
        s_prime.defender_obs_state.snort_warning_baseline_caught_attacker = False
        s_prime.defender_obs_state.snort_critical_baseline_caught_attacker = False
        s_prime.defender_obs_state.var_log_baseline_caught_attacker = False
        s_prime.defender_obs_state.step_baseline_caught_attacker = False
        s_prime.defender_obs_state.snort_severe_baseline_early_stopping = False
        s_prime.defender_obs_state.snort_warning_baseline_early_stopping = False
        s_prime.defender_obs_state.snort_critical_baseline_early_stopping = False
        s_prime.defender_obs_state.var_log_baseline_early_stopping = False
        s_prime.defender_obs_state.step_baseline_early_stopping = False
        s_prime.defender_obs_state.snort_severe_baseline_uncaught_intrusion_steps = 0
        s_prime.defender_obs_state.snort_warning_baseline_uncaught_intrusion_steps = 0
        s_prime.defender_obs_state.snort_critical_baseline_uncaught_intrusion_steps = 0
        s_prime.defender_obs_state.var_log_baseline_uncaught_intrusion_steps = 0
        s_prime.defender_obs_state.step_baseline_uncaught_intrusion_steps = 0
        s_prime.defender_obs_state.stops_remaining = s_prime.defender_obs_state.maximum_number_of_stops
        s_prime.defender_obs_state.first_stop_step = -1
        s_prime.defender_obs_state.second_stop_step = -1
        s_prime.defender_obs_state.third_stop_step = -1
        s_prime.defender_obs_state.fourth_stop_step = -1
        s_prime.defender_obs_state.first_stop_step = -1
        s_prime.defender_obs_state.second_stop_step = -1
        s_prime.defender_obs_state.third_stop_step = -1
        s_prime.defender_obs_state.fourth_stop_step = -1
        s_prime.defender_obs_state.snort_severe_baseline_first_stop_step = 0
        s_prime.defender_obs_state.snort_warning_baseline_first_stop_step = 0
        s_prime.defender_obs_state.snort_critical_baseline_first_stop_step = 0
        s_prime.defender_obs_state.var_log_baseline_first_stop_step = 0
        s_prime.defender_obs_state.step_baseline_first_stop_step = 0
        s_prime.defender_obs_state.snort_severe_baseline_second_stop_step = 0
        s_prime.defender_obs_state.snort_warning_baseline_second_stop_step = 0
        s_prime.defender_obs_state.snort_critical_baseline_second_stop_step = 0
        s_prime.defender_obs_state.var_log_baseline_second_stop_step = 0
        s_prime.defender_obs_state.step_baseline_second_stop_step = 0
        s_prime.defender_obs_state.snort_severe_baseline_third_stop_step = 0
        s_prime.defender_obs_state.snort_warning_baseline_third_stop_step = 0
        s_prime.defender_obs_state.snort_critical_baseline_third_stop_step = 0
        s_prime.defender_obs_state.var_log_baseline_third_stop_step = 0
        s_prime.defender_obs_state.step_baseline_third_stop_step = 0
        s_prime.defender_obs_state.snort_severe_baseline_fourth_stop_step = 0
        s_prime.defender_obs_state.snort_warning_baseline_fourth_stop_step = 0
        s_prime.defender_obs_state.snort_critical_baseline_fourth_stop_step = 0
        s_prime.defender_obs_state.var_log_baseline_fourth_stop_step = 0
        s_prime.defender_obs_state.step_baseline_fourth_stop_step = 0
        s_prime.defender_obs_state.snort_severe_baseline_stops_remaining = s_prime.defender_obs_state.maximum_number_of_stops
        s_prime.defender_obs_state.snort_warning_baseline_stops_remaining = s_prime.defender_obs_state.maximum_number_of_stops
        s_prime.defender_obs_state.snort_critical_baseline_stops_remaining = s_prime.defender_obs_state.maximum_number_of_stops
        s_prime.defender_obs_state.var_log_baseline_stops_remaining = s_prime.defender_obs_state.maximum_number_of_stops
        s_prime.defender_obs_state.step_baseline_stops_remaining = s_prime.defender_obs_state.maximum_number_of_stops

        return s_prime, 0, False

    @staticmethod
    def __update_docker_stats(state_obj: Union[DefenderObservationState, DefenderMachineObservationState], stats_obj) \
            -> None:
        """
        Helper method for updating docker stats states

        :param state_obj: the state object to update
        :param stats_obj: the stats object to use for the update
        :return: None
        """
        state_obj.num_pids_recent = float("{:.1f}".format(stats_obj.pids - state_obj.num_pids))
        state_obj.num_pids = stats_obj.pids
        state_obj.cpu_percent_recent = float("{:.1f}".format(stats_obj.cpu_percent - \
                                                        state_obj.cpu_percent))
        state_obj.cpu_percent = stats_obj.cpu_percent
        state_obj.mem_current_recent = float("{:.1f}".format(stats_obj.mem_current \
                                                        - state_obj.mem_current))
        state_obj.mem_current = stats_obj.mem_current
        state_obj.mem_total_recent = float("{:.1f}".format(stats_obj.mem_total - state_obj.mem_total))
        state_obj.mem_total = stats_obj.mem_total
        state_obj.mem_percent_recent = float("{:.1f}".format(stats_obj.mem_percent \
                                                        - state_obj.mem_percent))
        state_obj.mem_percent = stats_obj.mem_percent
        state_obj.blk_read_recent = float("{:.1f}".format(stats_obj.blk_read \
                                                     - state_obj.blk_read_recent))
        state_obj.blk_read = stats_obj.blk_read
        state_obj.blk_write_recent = float("{:.1f}".format(stats_obj.blk_write - state_obj.blk_write))
        state_obj.blk_write = stats_obj.blk_write
        state_obj.net_rx_recent = float("{:.1f}".format(stats_obj.net_rx - state_obj.net_rx))
        state_obj.net_rx = stats_obj.net_rx
        state_obj.net_tx_recent = float("{:.1f}".format(stats_obj.net_tx - state_obj.net_tx))
        state_obj.net_tx = stats_obj.net_tx