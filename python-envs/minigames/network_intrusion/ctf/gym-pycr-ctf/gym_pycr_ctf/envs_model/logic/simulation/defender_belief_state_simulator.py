from typing import Tuple
from gym_pycr_ctf.dao.network.env_state import EnvState
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.action.attacker.attacker_action import AttackerAction
from gym_pycr_ctf.dao.action.defender.defender_action import DefenderAction
from gym_pycr_ctf.envs_model.logic.common.env_dynamics_util import EnvDynamicsUtil


class DefenderBeliefStateSimulator:
    """
    Class that simulates belief state transitions of the defender
    """

    @staticmethod
    def update_state(s, attacker_action: AttackerAction, env_config: EnvConfig,
                     defender_action: DefenderAction)-> Tuple[EnvState, float, bool]:
        """
        Simulates a belief state transition of the defender

        :param s: the current state
        :param attacker_action: the attacker's previous action
        :param defender_action: the defender action
        :param env_config: the environment configuration
        :param defender_dynamics_model: dynamics model of the defender
        :return: s_prime, reward, done
        """
        s_prime = s
        logged_in_ips_str = EnvDynamicsUtil.logged_in_ips_str(env_config=env_config, a=attacker_action, s=s)

        num_new_alerts = 0
        num_new_priority = 0
        num_new_severe_alerts = 0
        num_new_warning_alerts = 0

        if env_config.use_attacker_action_stats_to_update_defender_state:
            num_new_alerts = attacker_action.alerts[0]
            num_new_priority = attacker_action.alerts[1]
            num_new_severe_alerts = num_new_alerts / 2
            num_new_warning_alerts = num_new_alerts / 2
        else:

            # Sample transitions
            # if (attacker_action.id.value, logged_in_ips_str) in \
            #         env_config.network_conf.defender_dynamics_model.norm_num_new_alerts:
            #     num_new_alerts = \
            #         env_config.network_conf.defender_dynamics_model.norm_num_new_alerts[
            #             (attacker_action.id.value, logged_in_ips_str)].rvs()

            # if (attacker_action.id.value, logged_in_ips_str) in \
            #         env_config.network_conf.defender_dynamics_model.norm_num_new_priority:
            #     num_new_priority = \
            #         env_config.network_conf.defender_dynamics_model.norm_num_new_priority[
            #             (attacker_action.id.value, logged_in_ips_str)].rvs()

            if (attacker_action.id.value, logged_in_ips_str) in \
                    env_config.network_conf.defender_dynamics_model.norm_num_new_severe_alerts:
                num_new_severe_alerts = \
                    env_config.network_conf.defender_dynamics_model.norm_num_new_severe_alerts[
                        (attacker_action.id.value, logged_in_ips_str)].rvs()
            else:
                print("miss 1: {}, action:{}".format((attacker_action.id.value, logged_in_ips_str), attacker_action))

            if (attacker_action.id.value, logged_in_ips_str) in \
                    env_config.network_conf.defender_dynamics_model.norm_num_new_warning_alerts:
                num_new_warning_alerts = \
                    env_config.network_conf.defender_dynamics_model.norm_num_new_warning_alerts[
                        (attacker_action.id.value, logged_in_ips_str)].rvs()
            else:
                print("miss 2: {}, action:{}".format((attacker_action.id.value, logged_in_ips_str), attacker_action))

            num_new_alerts = num_new_severe_alerts + num_new_warning_alerts
            num_new_priority = num_new_severe_alerts*3 + num_new_warning_alerts*1

        # Update network state
        s_prime.defender_obs_state.num_alerts_total = s_prime.defender_obs_state.num_alerts_total + num_new_alerts
        s_prime.defender_obs_state.num_alerts_recent = num_new_alerts
        s_prime.defender_obs_state.sum_priority_alerts_total = s_prime.defender_obs_state.sum_priority_alerts_total + \
                                                         num_new_priority
        s_prime.defender_obs_state.sum_priority_alerts_recent = num_new_priority
        s_prime.defender_obs_state.num_warning_alerts_total = s_prime.defender_obs_state.num_warning_alerts_total + \
                                                        num_new_warning_alerts
        s_prime.defender_obs_state.num_warning_alerts_recent = num_new_warning_alerts
        s_prime.defender_obs_state.num_severe_alerts_total = s_prime.defender_obs_state.num_severe_alerts_total + \
                                                       num_new_severe_alerts
        s_prime.defender_obs_state.num_severe_alerts_recent = num_new_severe_alerts

        # Update machines state
        for m in s_prime.defender_obs_state.machines:

            if m.ip in env_config.network_conf.defender_dynamics_model.machines_dynamics_model:
                m_dynamics = env_config.network_conf.defender_dynamics_model.machines_dynamics_model[m.ip]

                num_new_open_connections = 0
                num_new_failed_login_attempts = 0
                num_new_users = 0
                num_new_logged_in_users = 0
                num_new_login_events = 0
                num_new_processes = 0

                # Sample transitions
                if (attacker_action.id.value, logged_in_ips_str) in m_dynamics.norm_num_new_open_connections:
                    num_new_open_connections = \
                        m_dynamics.norm_num_new_open_connections[
                            (attacker_action.id.value, logged_in_ips_str)].rvs()

                if (attacker_action.id.value, logged_in_ips_str) in m_dynamics.norm_num_new_failed_login_attempts:
                    num_new_failed_login_attempts = m_dynamics.norm_num_new_failed_login_attempts[
                        (attacker_action.id.value, logged_in_ips_str)].rvs()

                if (attacker_action.id.value, logged_in_ips_str) in m_dynamics.norm_num_new_users:
                    num_new_users = m_dynamics.norm_num_new_users[
                        (attacker_action.id.value, logged_in_ips_str)].rvs()

                if (attacker_action.id.value, logged_in_ips_str) in m_dynamics.norm_num_new_logged_in_users:
                    num_new_logged_in_users = m_dynamics.norm_num_new_logged_in_users[
                        (attacker_action.id.value, logged_in_ips_str)].rvs()

                if (attacker_action.id.value, logged_in_ips_str) in m_dynamics.norm_num_new_login_events:
                    num_new_login_events = m_dynamics.norm_num_new_login_events[
                        (attacker_action.id.value, logged_in_ips_str)].rvs()

                if (attacker_action.id.value, logged_in_ips_str) in m_dynamics.norm_num_new_processes:
                    num_new_processes = m_dynamics.norm_num_new_processes[
                        (attacker_action.id.value, logged_in_ips_str)].rvs()

                # Update network state
                m.num_open_connections = m.num_open_connections + num_new_open_connections
                m.num_open_connections_recent = num_new_open_connections
                m.num_failed_login_attempts = m.num_failed_login_attempts + num_new_failed_login_attempts
                m.num_failed_login_attempts_recent = num_new_failed_login_attempts
                m.num_users = m.num_users + num_new_users
                m.num_users_recent = num_new_users
                m.num_logged_in_users = m.num_logged_in_users + num_new_logged_in_users
                m.num_logged_in_users_recent = num_new_logged_in_users
                m.num_login_events = m.num_login_events + num_new_login_events
                m.num_login_events_recent= num_new_login_events
                m.num_processes = m.num_processes + num_new_processes
                m.num_processes_recent = num_new_processes

        s_prime.defender_obs_state.step = s_prime.defender_obs_state.step + 1

        return s_prime, 0, True

    @staticmethod
    def init_state(s, attacker_action: AttackerAction, env_config: EnvConfig,
                     defender_action: DefenderAction) -> Tuple[EnvState, float, bool]:
        """
        Initializes the belief state of the defender

        :param s: the current state
        :param attacker_action: the attacker's previous action
        :param defender_action: the defender action
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        return DefenderBeliefStateSimulator.reset_state(s=s, attacker_action=attacker_action, env_config=env_config,
                                                        defender_action=defender_action)

    @staticmethod
    def reset_state(s: EnvState, attacker_action: AttackerAction, env_config: EnvConfig,
                   defender_action: DefenderAction) -> Tuple[EnvState, float, bool]:
        """
        Resets the belief state of the defender

        :param s: the current state
        :param attacker_action: the attacker's previous action
        :param defender_action: the defender action
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        s_prime = s

        # Reset stopped state
        s_prime.defender_obs_state.caught_attacker = False
        s_prime.defender_obs_state.stopped = False

        # Reset IDS states
        s_prime.defender_obs_state.num_alerts_recent = 0
        s_prime.defender_obs_state.num_severe_alerts_recent = 0
        s_prime.defender_obs_state.num_warning_alerts_recent = 0
        s_prime.defender_obs_state.sum_priority_alerts_recent = 0
        s_prime.defender_obs_state.num_alerts_total = 0
        s_prime.defender_obs_state.sum_priority_alerts_total = 0
        s_prime.defender_obs_state.num_severe_alerts_total = 0
        s_prime.defender_obs_state.num_warning_alerts_total = 0

        # Update logs timestamps and reset machine states
        for m in s_prime.defender_obs_state.machines:

            m.num_users = 0
            m.num_logged_in_users = 0
            m.num_processes = 0
            m.num_open_connections = 0

            if m.ip in env_config.network_conf.defender_dynamics_model.machines_dynamics_model:
                m_dynamics = env_config.network_conf.defender_dynamics_model.machines_dynamics_model[m.ip]

                # Sample initial states
                if m_dynamics.norm_num_new_open_connections is not None:
                    init_open_connections = m_dynamics.norm_init_open_connections.rvs()
                    m.num_open_connections = init_open_connections

                if m_dynamics.norm_init_users is not None:
                    init_users = m_dynamics.norm_init_users.rvs()
                    m.num_users = init_users

                if m_dynamics.norm_init_logged_in_users is not None:
                    init_logged_in_users = m_dynamics.norm_init_logged_in_users.rvs()
                    m.num_logged_in_users = init_logged_in_users

                if m_dynamics.norm_init_processes is not None:
                    init_processes = m_dynamics.norm_init_processes.rvs()
                    m.num_processes = init_processes

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
        s_prime.snort_severe_baseline_first_stop_step = 0
        s_prime.snort_warning_baseline_first_stop_step = 0
        s_prime.snort_critical_baseline_first_stop_step = 0
        s_prime.var_log_baseline_first_stop_step = 0
        s_prime.step_baseline_first_stop_step = 0
        s_prime.snort_severe_baseline_second_stop_step = 0
        s_prime.snort_warning_baseline_second_stop_step = 0
        s_prime.snort_critical_baseline_second_stop_step = 0
        s_prime.var_log_baseline_second_stop_step = 0
        s_prime.step_baseline_second_stop_step = 0
        s_prime.snort_severe_baseline_third_stop_step = 0
        s_prime.snort_warning_baseline_third_stop_step = 0
        s_prime.snort_critical_baseline_third_stop_step = 0
        s_prime.var_log_baseline_third_stop_step = 0
        s_prime.step_baseline_third_stop_step = 0
        s_prime.snort_severe_baseline_fourth_stop_step = 0
        s_prime.snort_warning_baseline_fourth_stop_step = 0
        s_prime.snort_critical_baseline_fourth_stop_step = 0
        s_prime.var_log_baseline_fourth_stop_step = 0
        s_prime.step_baseline_fourth_stop_step = 0
        s_prime.snort_severe_baseline_stops_remaining = 0
        s_prime.snort_warning_baseline_stops_remaining = 0
        s_prime.snort_critical_baseline_stops_remaining = 0
        s_prime.var_log_baseline_stops_remaining = 0
        s_prime.step_baseline_stops_remaining = 0

        return s_prime, 0, False
