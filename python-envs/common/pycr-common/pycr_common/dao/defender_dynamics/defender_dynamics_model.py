import json
import os
from scipy import stats
import numpy as np
from pycr_common.util.experiments_util import util
from enum import Enum
from pycr_common.dao.defender_dynamics.defender_machine_dynamics_model import DefenderMachineDynamicsModel
from pycr_common.dao.defender_dynamics.defender_dynamics_tensorboard_dto import DefenderDynamicsTensorboardDTO
import pycr_common.constants.constants as constants


class DefenderDynamicsModel:
    """
    Represents a dynamics model of the defender for simulating stochastic (b, a) -> b' transitions based on
    maximum likelihood estimations
    """

    def __init__(self):
        """
        Initializes the model
        """
        self.num_new_alerts = {}
        self.num_new_priority = {}
        self.num_new_severe_alerts = {}
        self.num_new_warning_alerts = {}
        self.num_new_failed_login_attempts = {}
        self.num_new_open_connections = {}
        self.num_new_login_events = {}
        self.num_new_processes = {}
        self.num_new_pids = {}
        self.cpu_percentage_change = {}
        self.new_mem_current = {}
        self.new_mem_total = {}
        self.new_mem_percent = {}
        self.new_blk_read = {}
        self.new_blk_write = {}
        self.new_net_rx = {}
        self.new_net_tx = {}
        self.init_num_new_pids = {}
        self.init_cpu_percentage_change = {}
        self.init_new_mem_current = {}
        self.init_new_mem_total = {}
        self.init_new_mem_percent = {}
        self.init_new_blk_read = {}
        self.init_new_blk_write = {}
        self.init_new_net_rx = {}
        self.init_new_net_tx = {}

        self.machines_dynamics_model = {}

        self.norm_num_new_alerts = {}
        self.norm_num_new_priority = {}
        self.norm_num_new_severe_alerts = {}
        self.norm_num_new_warning_alerts = {}
        self.norm_num_new_failed_login_attempts = {}
        self.norm_num_new_open_connections = {}
        self.norm_num_new_login_events = {}
        self.norm_num_new_processes = {}
        self.norm_machines_dynamics_model = {}
        self.norm_num_new_pids = {}
        self.norm_cpu_percentage_change = {}
        self.norm_new_mem_current = {}
        self.norm_new_mem_total = {}
        self.norm_new_mem_percent = {}
        self.norm_new_blk_read = {}
        self.norm_new_blk_write = {}
        self.norm_new_net_rx = {}
        self.norm_new_net_tx = {}
        self.norm_init_num_new_pids = {}
        self.norm_init_cpu_percentage_change = {}
        self.norm_init_new_mem_current = {}
        self.norm_init_new_mem_total = {}
        self.norm_init_new_mem_percent = {}
        self.norm_init_new_blk_read = {}
        self.norm_init_new_blk_write = {}
        self.norm_init_new_net_rx = {}
        self.norm_init_new_net_tx = {}

    def normalize(self) -> None:
        """
        Normalizes transition counts into probability distributions

        :return: None
        """

        # Normalize num_new_alerts
        for attack_id_str, v1 in self.num_new_alerts.items():
            for logged_in_ips, v2 in v1.items():
                samples = []
                counts = []
                for num_alerts_str, count in v2.items():
                    samples.append(int(num_alerts_str))
                    counts.append(count)
                counts = np.array(counts)
                samples = np.array(samples)
                empirical_probabilities = counts/np.sum(counts)
                dist = stats.rv_discrete(name='num_new_alerts_emp_dist', values=(samples, empirical_probabilities))
                self.norm_num_new_alerts[(int(attack_id_str), logged_in_ips)] = dist

        # Normalize num_new_priority
        for attack_id_str, v1 in self.num_new_priority.items():
            for logged_in_ips, v2 in v1.items():
                samples = []
                counts = []
                for num_priority_str, count in v2.items():
                    samples.append(int(num_priority_str))
                    counts.append(count)
                counts = np.array(counts)
                samples = np.array(samples)
                empirical_probabilities = counts / np.sum(counts)
                dist = stats.rv_discrete(name='num_new_priority_emp_dist', values=(samples, empirical_probabilities))
                self.norm_num_new_priority[(int(attack_id_str), logged_in_ips)] = dist

        # Normalize num_new_severe_alerts
        for attack_id_str, v1 in self.num_new_severe_alerts.items():
            for logged_in_ips, v2 in v1.items():
                samples = []
                counts = []
                for num_severe_str, count in v2.items():
                    samples.append(int(num_severe_str))
                    counts.append(count)
                counts = np.array(counts)
                samples = np.array(samples)
                empirical_probabilities = counts / np.sum(counts)
                dist = stats.rv_discrete(name='num_new_severe_alerts_emp_dist',
                                         values=(samples, empirical_probabilities))
                self.norm_num_new_severe_alerts[(int(attack_id_str), logged_in_ips)] = dist

        # Normalize num_new_warning_alerts
        for attack_id_str, v1 in self.num_new_warning_alerts.items():
            for logged_in_ips, v2 in v1.items():
                samples = []
                counts = []
                for num_login_attempts_str, count in v2.items():
                    samples.append(int(num_login_attempts_str))
                    counts.append(count)
                counts = np.array(counts)
                samples = np.array(samples)
                empirical_probabilities = counts / np.sum(counts)
                dist = stats.rv_discrete(name='num_new_warning_alerts_emp_dist',
                                         values=(samples, empirical_probabilities))
                self.norm_num_new_warning_alerts[(int(attack_id_str), logged_in_ips)] = dist

        # Normalize num_new_failed_login_attempts
        for attack_id_str, v1 in self.num_new_failed_login_attempts.items():
            for logged_in_ips, v2 in v1.items():
                samples = []
                counts = []
                for num_login_attempts_str, count in v2.items():
                    samples.append(int(num_login_attempts_str))
                    counts.append(count)
                counts = np.array(counts)
                samples = np.array(samples)
                empirical_probabilities = counts / np.sum(counts)
                dist = stats.rv_discrete(name='num_new_login_attempts_emp_dist',
                                         values=(samples, empirical_probabilities))
                self.norm_num_new_failed_login_attempts[(int(attack_id_str), logged_in_ips)] = dist

        # Normalize num_new_open_connections
        for attack_id_str, v1 in self.num_new_open_connections.items():
            for logged_in_ips, v2 in v1.items():
                samples = []
                counts = []
                for num_login_attempts_str, count in v2.items():
                    samples.append(int(num_login_attempts_str))
                    counts.append(count)
                counts = np.array(counts)
                samples = np.array(samples)
                empirical_probabilities = counts / np.sum(counts)
                dist = stats.rv_discrete(name='num_new_open_connections_emp_dist',
                                         values=(samples, empirical_probabilities))
                self.norm_num_new_open_connections[(int(attack_id_str), logged_in_ips)] = dist

        # Normalize num_new_login_events
        for attack_id_str, v1 in self.num_new_login_events.items():
            for logged_in_ips, v2 in v1.items():
                samples = []
                counts = []
                for num_login_attempts_str, count in v2.items():
                    samples.append(int(num_login_attempts_str))
                    counts.append(count)
                counts = np.array(counts)
                samples = np.array(samples)
                empirical_probabilities = counts / np.sum(counts)
                dist = stats.rv_discrete(name='num_new_login_events_emp_dist',
                                         values=(samples, empirical_probabilities))
                self.norm_num_new_login_events[(int(attack_id_str), logged_in_ips)] = dist

        # Normalize num_new_processes
        for attack_id_str, v1 in self.num_new_processes.items():
            for logged_in_ips, v2 in v1.items():
                samples = []
                counts = []
                for num_login_attempts_str, count in v2.items():
                    samples.append(int(num_login_attempts_str))
                    counts.append(count)
                counts = np.array(counts)
                samples = np.array(samples)
                empirical_probabilities = counts / np.sum(counts)
                dist = stats.rv_discrete(name='num_new_processes_emp_dist',
                                         values=(samples, empirical_probabilities))
                self.norm_num_new_processes[(int(attack_id_str), logged_in_ips)] = dist

        # Normalize machine specific distributions
        for machine_ip, v in self.machines_dynamics_model.items():
            v.normalize()

    def add_new_alert_transition(self, attacker_action_id: Enum, logged_in_ips : str,
                                 num_new_alerts: int) -> None:
        """
        Adds a new transition for alerts

        :param attacker_action_id: the attacker action that triggered the transition
        :param logged_in_ips: the attacker state
        :param num_new_alerts: the number observed number of new alerts
        :return: None
        """
        if str(attacker_action_id.value) not in self.num_new_alerts:
            self.num_new_alerts[str(attacker_action_id.value)] = {}
            self.num_new_alerts[str(attacker_action_id.value)][logged_in_ips] = {}
            self.num_new_alerts[str(attacker_action_id.value)][logged_in_ips][str(num_new_alerts)] = 1
        else:
            if logged_in_ips in self.num_new_alerts[str(attacker_action_id.value)]:
                if str(num_new_alerts) in self.num_new_alerts[str(attacker_action_id.value)][logged_in_ips]:
                    self.num_new_alerts[str(attacker_action_id.value)][logged_in_ips][str(num_new_alerts)] \
                        = self.num_new_alerts[str(attacker_action_id.value)][logged_in_ips][str(num_new_alerts)] + 1
                else:
                    self.num_new_alerts[str(attacker_action_id.value)][logged_in_ips][str(num_new_alerts)] = 1
            else:
                self.num_new_alerts[str(attacker_action_id.value)][logged_in_ips] = {}
                self.num_new_alerts[str(attacker_action_id.value)][logged_in_ips][str(num_new_alerts)] = 1

    def add_new_priority_transition(self, attacker_action_id: Enum, logged_in_ips : str,
                                    num_new_priority: int) -> None:
        """
        Adds a new transition for intrusion prevention priorities

        :param attacker_action_id: the attacker action that triggered the transition
        :param logged_in_ips: the attacker state
        :param num_new_priority: the observed new priorities
        :return: None
        """
        if str(attacker_action_id.value) not in self.num_new_priority:
            self.num_new_priority[str(attacker_action_id.value)] = {}
            self.num_new_priority[str(attacker_action_id.value)][logged_in_ips] = {}
            self.num_new_priority[str(attacker_action_id.value)][logged_in_ips][str(num_new_priority)] = 1
        else:
            if logged_in_ips in self.num_new_priority[str(attacker_action_id.value)]:
                if str(num_new_priority) in self.num_new_priority[str(attacker_action_id.value)][logged_in_ips]:
                    self.num_new_priority[str(attacker_action_id.value)][logged_in_ips][str(num_new_priority)] \
                        = self.num_new_priority[str(attacker_action_id.value)][logged_in_ips][str(num_new_priority)] + 1
                else:
                    self.num_new_priority[str(attacker_action_id.value)][logged_in_ips][str(num_new_priority)] = 1
            else:
                self.num_new_priority[str(attacker_action_id.value)][logged_in_ips] = {}
                self.num_new_priority[str(attacker_action_id.value)][logged_in_ips][str(num_new_priority)] = 1

    def add_new_severe_alert_transition(self, attacker_action_id: Enum, logged_in_ips : str,
                                        num_new_severe_alerts: int) -> None:
        """
        Adds a new transition for intrusion prevention severe alerts

        :param attacker_action_id: the attacker action that triggered the transition
        :param logged_in_ips: the attacker state
        :param num_new_severe_alerts: the observed new number of severe alerts
        :return: None
        """
        if str(attacker_action_id.value) not in self.num_new_severe_alerts:
            self.num_new_severe_alerts[str(attacker_action_id.value)] = {}
            self.num_new_severe_alerts[str(attacker_action_id.value)][logged_in_ips] = {}
            self.num_new_severe_alerts[str(attacker_action_id.value)][logged_in_ips][str(num_new_severe_alerts)] = 1
        else:
            if logged_in_ips in self.num_new_severe_alerts[str(attacker_action_id.value)]:
                if str(num_new_severe_alerts) in self.num_new_severe_alerts[str(attacker_action_id.value)][
                    logged_in_ips]:
                    self.num_new_severe_alerts[str(attacker_action_id.value)][logged_in_ips][
                        str(num_new_severe_alerts)] \
                        = self.num_new_severe_alerts[str(attacker_action_id.value)][logged_in_ips][
                              str(num_new_severe_alerts)] + 1
                else:
                    self.num_new_severe_alerts[str(attacker_action_id.value)][logged_in_ips][
                        str(num_new_severe_alerts)] = 1
            else:
                self.num_new_severe_alerts[str(attacker_action_id.value)][logged_in_ips] = {}
                self.num_new_severe_alerts[str(attacker_action_id.value)][logged_in_ips][
                    str(num_new_severe_alerts)] = 1

    def add_new_warning_alert_transition(self, attacker_action_id: Enum, logged_in_ips : str,
                                         num_new_warning_alerts: int) -> None:
        """
        Adds a new transition for intrusion prevention warning alerts

        :param attacker_action_id: the attacker action that triggered the transition
        :param logged_in_ips: the attacker state
        :param num_new_warning_alerts: observed new warning alerts
        :return: None
        """
        if str(attacker_action_id.value) not in self.num_new_warning_alerts:
            self.num_new_warning_alerts[str(attacker_action_id.value)] = {}
            self.num_new_warning_alerts[str(attacker_action_id.value)][logged_in_ips] = {}
            self.num_new_warning_alerts[str(attacker_action_id.value)][logged_in_ips][
                str(num_new_warning_alerts)] = 1
        else:
            if logged_in_ips in self.num_new_warning_alerts[str(attacker_action_id.value)]:
                if str(num_new_warning_alerts) in self.num_new_warning_alerts[
                    str(attacker_action_id.value)][logged_in_ips]:
                    self.num_new_warning_alerts[str(attacker_action_id.value)][logged_in_ips][
                        str(num_new_warning_alerts)] \
                        = self.num_new_warning_alerts[str(attacker_action_id.value)][logged_in_ips][
                              str(num_new_warning_alerts)] + 1
                else:
                    self.num_new_warning_alerts[str(attacker_action_id.value)][logged_in_ips][
                        str(num_new_warning_alerts)] = 1
            else:
                self.num_new_warning_alerts[str(attacker_action_id.value)][logged_in_ips] = {}
                self.num_new_warning_alerts[str(attacker_action_id.value)][logged_in_ips][
                    str(num_new_warning_alerts)] = 1

    def add_new_failed_login_attempt_transition(self, attacker_action_id: Enum, logged_in_ips: str,
                                                num_new_login_attempts: int) -> None:
        """
        Adds a new transition for intrusion prevention login attempts

        :param attacker_action_id: the attacker action that triggered the transition
        :param logged_in_ips: the attacker state
        :param num_new_login_attempts: observed new login attempts
        :return: None
        """
        if str(attacker_action_id.value) not in self.num_new_failed_login_attempts:
            self.num_new_failed_login_attempts[str(attacker_action_id.value)] = {}
            self.num_new_failed_login_attempts[str(attacker_action_id.value)][logged_in_ips] = {}
            self.num_new_failed_login_attempts[str(attacker_action_id.value)][logged_in_ips][
                str(num_new_login_attempts)] = 1
        else:
            if logged_in_ips in self.num_new_failed_login_attempts[str(attacker_action_id.value)]:
                if str(num_new_login_attempts) in self.num_new_failed_login_attempts[
                    str(attacker_action_id.value)][logged_in_ips]:
                    self.num_new_failed_login_attempts[str(attacker_action_id.value)][logged_in_ips][
                        str(num_new_login_attempts)] \
                        = self.num_new_failed_login_attempts[str(attacker_action_id.value)][logged_in_ips][
                              str(num_new_login_attempts)] + 1
                else:
                    self.num_new_failed_login_attempts[str(attacker_action_id.value)][logged_in_ips][
                        str(num_new_login_attempts)] = 1
            else:
                self.num_new_failed_login_attempts[str(attacker_action_id.value)][logged_in_ips] = {}
                self.num_new_failed_login_attempts[str(attacker_action_id.value)][logged_in_ips][
                    str(num_new_login_attempts)] = 1

    def add_new_connections_transition(self, attacker_action_id: Enum, logged_in_ips: str,
                                       num_new_connections: int) -> None:
        """
        Adds a new transition for intrusion prevention new connections

        :param attacker_action_id: the attacker action that triggered the transition
        :param logged_in_ips: the attacker state
        :param num_new_connections: observed new connections
        :return: None
        """
        if str(attacker_action_id.value) not in self.num_new_open_connections:
            self.num_new_open_connections[str(attacker_action_id.value)] = {}
            self.num_new_open_connections[str(attacker_action_id.value)][logged_in_ips] = {}
            self.num_new_open_connections[str(attacker_action_id.value)][logged_in_ips][
                str(num_new_connections)] = 1
        else:
            if logged_in_ips in self.num_new_open_connections[str(attacker_action_id.value)]:
                if str(num_new_connections) in self.num_new_open_connections[
                    str(attacker_action_id.value)][logged_in_ips]:
                    self.num_new_open_connections[str(attacker_action_id.value)][logged_in_ips][
                        str(num_new_connections)] \
                        = self.num_new_open_connections[str(attacker_action_id.value)][logged_in_ips][
                              str(num_new_connections)] + 1
                else:
                    self.num_new_open_connections[str(attacker_action_id.value)][logged_in_ips][
                        str(num_new_connections)] = 1
            else:
                self.num_new_open_connections[str(attacker_action_id.value)][logged_in_ips] = {}
                self.num_new_open_connections[str(attacker_action_id.value)][logged_in_ips][
                    str(num_new_connections)] = 1

    def add_new_login_events_transition(self, attacker_action_id: Enum, logged_in_ips: str,
                                        num_new_login_events: int) -> None:
        """
        Adds a new transition for intrusion prevention new login events

        :param attacker_action_id: the attacker action that triggered the transition
        :param logged_in_ips: the attacker state
        :param num_new_login_events: observed new login events
        :return: None
        """
        if str(attacker_action_id.value) not in self.num_new_login_events:
            self.num_new_login_events[str(attacker_action_id.value)] = {}
            self.num_new_login_events[str(attacker_action_id.value)][logged_in_ips] = {}
            self.num_new_login_events[str(attacker_action_id.value)][logged_in_ips][
                str(num_new_login_events)] = 1
        else:
            if logged_in_ips in self.num_new_login_events[str(attacker_action_id.value)]:
                if str(num_new_login_events) in self.num_new_login_events[
                    str(attacker_action_id.value)][logged_in_ips]:
                    self.num_new_login_events[str(attacker_action_id.value)][logged_in_ips][
                        str(num_new_login_events)] \
                        = self.num_new_login_events[str(attacker_action_id.value)][logged_in_ips][
                              str(num_new_login_events)] + 1
                else:
                    self.num_new_login_events[str(attacker_action_id.value)][logged_in_ips][
                        str(num_new_login_events)] = 1
            else:
                self.num_new_login_events[str(attacker_action_id.value)][logged_in_ips] = {}
                self.num_new_login_events[str(attacker_action_id.value)][logged_in_ips][
                    str(num_new_login_events)] = 1

    def add_new_processes_transition(self, attacker_action_id: Enum, logged_in_ips: str,
                                     num_new_processes: int) -> None:
        """
        Adds a new transition for intrusion prevention new processes

        :param attacker_action_id: the attacker action that triggered the transition
        :param logged_in_ips: the attacker state
        :param num_new_processes: observed new processes
        :return: None
        """
        if str(attacker_action_id.value) not in self.num_new_processes:
            self.num_new_processes[str(attacker_action_id.value)] = {}
            self.num_new_processes[str(attacker_action_id.value)][logged_in_ips] = {}
            self.num_new_processes[str(attacker_action_id.value)][logged_in_ips][
                str(num_new_processes)] = 1
        else:
            if logged_in_ips in self.num_new_processes[str(attacker_action_id.value)]:
                if str(num_new_processes) in self.num_new_processes[
                    str(attacker_action_id.value)][logged_in_ips]:
                    self.num_new_processes[str(attacker_action_id.value)][logged_in_ips][
                        str(num_new_processes)] \
                        = self.num_new_processes[str(attacker_action_id.value)][logged_in_ips][
                              str(num_new_processes)] + 1
                else:
                    self.num_new_processes[str(attacker_action_id.value)][logged_in_ips][
                        str(num_new_processes)] = 1
            else:
                self.num_new_processes[str(attacker_action_id.value)][logged_in_ips] = {}
                self.num_new_processes[str(attacker_action_id.value)][logged_in_ips][
                    str(num_new_processes)] = 1

    def add_new_pids_transition(self, attacker_action_id: Enum, logged_in_ips: str,
                                 num_new_pids: int) -> None:
        """
        Adds a new transition for pids

        :param attacker_action_id: the attacker action that triggered the transition
        :param logged_in_ips: the attacker state
        :param num_new_pids: the number of observed new pids
        :return: None
        """
        if str(attacker_action_id.value) not in self.num_new_pids:
            self.num_new_pids[str(attacker_action_id.value)] = {}
            self.num_new_pids[str(attacker_action_id.value)][logged_in_ips] = {}
            self.num_new_pids[str(attacker_action_id.value)][logged_in_ips][str(num_new_pids)] = 1
        else:
            if logged_in_ips in self.num_new_pids[str(attacker_action_id.value)]:
                if str(num_new_pids) in self.num_new_pids[str(attacker_action_id.value)][logged_in_ips]:
                    self.num_new_pids[str(attacker_action_id.value)][logged_in_ips][str(num_new_pids)] \
                        = self.num_new_pids[str(attacker_action_id.value)][logged_in_ips][str(num_new_pids)] + 1
                else:
                    self.num_new_pids[str(attacker_action_id.value)][logged_in_ips][str(num_new_pids)] = 1
            else:
                self.num_new_pids[str(attacker_action_id.value)][logged_in_ips] = {}
                self.num_new_pids[str(attacker_action_id.value)][logged_in_ips][str(num_new_pids)] = 1

    def add_new_cpu_percent_transition(self, attacker_action_id: Enum, logged_in_ips: str,
                                       cpu_percent_change: float) -> None:
        """
        Adds a new transition for CPU percent

        :param attacker_action_id: the attacker action that triggered the transition
        :param logged_in_ips: the attacker state
        :param cpu_percent_change: the observed change in CPU percent
        :return: None
        """
        if str(attacker_action_id.value) not in self.cpu_percentage_change:
            self.cpu_percentage_change[str(attacker_action_id.value)] = {}
            self.cpu_percentage_change[str(attacker_action_id.value)][logged_in_ips] = {}
            self.cpu_percentage_change[str(attacker_action_id.value)][logged_in_ips][str(cpu_percent_change)] = 1
        else:
            if logged_in_ips in self.cpu_percentage_change[str(attacker_action_id.value)]:
                if str(cpu_percent_change) in self.cpu_percentage_change[str(attacker_action_id.value)][logged_in_ips]:
                    self.cpu_percentage_change[str(attacker_action_id.value)][logged_in_ips][str(cpu_percent_change)] \
                        = self.cpu_percentage_change[str(attacker_action_id.value)][logged_in_ips][str(cpu_percent_change)] + 1
                else:
                    self.cpu_percentage_change[str(attacker_action_id.value)][logged_in_ips][str(cpu_percent_change)] = 1
            else:
                self.cpu_percentage_change[str(attacker_action_id.value)][logged_in_ips] = {}
                self.cpu_percentage_change[str(attacker_action_id.value)][logged_in_ips][str(cpu_percent_change)] = 1

    def add_new_mem_current_transition(self, attacker_action_id: Enum, logged_in_ips: str,
                                       new_mem_current: int) -> None:
        """
        Adds a new transition for current used memory

        :param attacker_action_id: the attacker action that triggered the transition
        :param logged_in_ips: the attacker state
        :param new_mem_current: the observed change in mem current
        :return: None
        """
        if str(attacker_action_id.value) not in self.new_mem_current:
            self.new_mem_current[str(attacker_action_id.value)] = {}
            self.new_mem_current[str(attacker_action_id.value)][logged_in_ips] = {}
            self.new_mem_current[str(attacker_action_id.value)][logged_in_ips][str(new_mem_current)] = 1
        else:
            if logged_in_ips in self.new_mem_current[str(attacker_action_id.value)]:
                if str(new_mem_current) in self.new_mem_current[str(attacker_action_id.value)][logged_in_ips]:
                    self.new_mem_current[str(attacker_action_id.value)][logged_in_ips][str(new_mem_current)] \
                        = self.new_mem_current[str(attacker_action_id.value)][logged_in_ips][str(new_mem_current)] + 1
                else:
                    self.new_mem_current[str(attacker_action_id.value)][logged_in_ips][str(new_mem_current)] = 1
            else:
                self.new_mem_current[str(attacker_action_id.value)][logged_in_ips] = {}
                self.new_mem_current[str(attacker_action_id.value)][logged_in_ips][str(new_mem_current)] = 1

    def add_new_mem_total_transition(self, attacker_action_id: Enum, logged_in_ips: str,
                                     new_mem_total_change: int) -> None:
        """
        Adds a new transition for total memory available

        :param attacker_action_id: the attacker action that triggered the transition
        :param logged_in_ips: the attacker state
        :param new_mem_total_change: the observed change in mem total
        :return: None
        """
        if str(attacker_action_id.value) not in self.new_mem_total:
            self.new_mem_total[str(attacker_action_id.value)] = {}
            self.new_mem_total[str(attacker_action_id.value)][logged_in_ips] = {}
            self.new_mem_total[str(attacker_action_id.value)][logged_in_ips][str(new_mem_total_change)] = 1
        else:
            if logged_in_ips in self.new_mem_total[str(attacker_action_id.value)]:
                if str(new_mem_total_change) in self.new_mem_total[str(attacker_action_id.value)][logged_in_ips]:
                    self.new_mem_total[str(attacker_action_id.value)][logged_in_ips][str(new_mem_total_change)] \
                        = self.new_mem_total[str(attacker_action_id.value)][logged_in_ips][
                              str(new_mem_total_change)] + 1
                else:
                    self.new_mem_total[str(attacker_action_id.value)][logged_in_ips][str(new_mem_total_change)] = 1
            else:
                self.new_mem_total[str(attacker_action_id.value)][logged_in_ips] = {}
                self.new_mem_total[str(attacker_action_id.value)][logged_in_ips][str(new_mem_total_change)] = 1

    def add_new_mem_percent_transition(self, attacker_action_id: Enum, logged_in_ips: str,
                                     new_mem_percent_change: int) -> None:
        """
        Adds a new transition for memory utilization percentage

        :param attacker_action_id: the attacker action that triggered the transition
        :param logged_in_ips: the attacker state
        :param new_mem_percent_change: the observed change in mem percent
        :return: None
        """
        if str(attacker_action_id.value) not in self.new_mem_percent:
            self.new_mem_percent[str(attacker_action_id.value)] = {}
            self.new_mem_percent[str(attacker_action_id.value)][logged_in_ips] = {}
            self.new_mem_percent[str(attacker_action_id.value)][logged_in_ips][str(new_mem_percent_change)] = 1
        else:
            if logged_in_ips in self.new_mem_percent[str(attacker_action_id.value)]:
                if str(new_mem_percent_change) in self.new_mem_percent[str(attacker_action_id.value)][logged_in_ips]:
                    self.new_mem_percent[str(attacker_action_id.value)][logged_in_ips][str(new_mem_percent_change)] \
                        = self.new_mem_percent[str(attacker_action_id.value)][logged_in_ips][
                              str(new_mem_percent_change)] + 1
                else:
                    self.new_mem_percent[str(attacker_action_id.value)][logged_in_ips][str(new_mem_percent_change)] = 1
            else:
                self.new_mem_percent[str(attacker_action_id.value)][logged_in_ips] = {}
                self.new_mem_percent[str(attacker_action_id.value)][logged_in_ips][str(new_mem_percent_change)] = 1

    def add_new_blk_read_transition(self, attacker_action_id: Enum, logged_in_ips: str,
                                       new_blk_read_change: int) -> None:
        """
        Adds a new transition for blk read

        :param attacker_action_id: the attacker action that triggered the transition
        :param logged_in_ips: the attacker state
        :param new_blk_read_change: the observed change in blk read
        :return: None
        """
        if str(attacker_action_id.value) not in self.new_blk_read:
            self.new_blk_read[str(attacker_action_id.value)] = {}
            self.new_blk_read[str(attacker_action_id.value)][logged_in_ips] = {}
            self.new_blk_read[str(attacker_action_id.value)][logged_in_ips][str(new_blk_read_change)] = 1
        else:
            if logged_in_ips in self.new_blk_read[str(attacker_action_id.value)]:
                if str(new_blk_read_change) in self.new_blk_read[str(attacker_action_id.value)][logged_in_ips]:
                    self.new_blk_read[str(attacker_action_id.value)][logged_in_ips][str(new_blk_read_change)] \
                        = self.new_blk_read[str(attacker_action_id.value)][logged_in_ips][
                              str(new_blk_read_change)] + 1
                else:
                    self.new_blk_read[str(attacker_action_id.value)][logged_in_ips][str(new_blk_read_change)] = 1
            else:
                self.new_blk_read[str(attacker_action_id.value)][logged_in_ips] = {}
                self.new_blk_read[str(attacker_action_id.value)][logged_in_ips][str(new_blk_read_change)] = 1

    def add_new_blk_write_transition(self, attacker_action_id: Enum, logged_in_ips: str,
                                    new_blk_write_change: int) -> None:
        """
        Adds a new transition for blk write

        :param attacker_action_id: the attacker action that triggered the transition
        :param logged_in_ips: the attacker state
        :param new_blk_write_change: the observed change in blk write
        :return: None
        """
        if str(attacker_action_id.value) not in self.new_blk_write:
            self.new_blk_write[str(attacker_action_id.value)] = {}
            self.new_blk_write[str(attacker_action_id.value)][logged_in_ips] = {}
            self.new_blk_write[str(attacker_action_id.value)][logged_in_ips][str(new_blk_write_change)] = 1
        else:
            if logged_in_ips in self.new_blk_write[str(attacker_action_id.value)]:
                if str(new_blk_write_change) in self.new_blk_write[str(attacker_action_id.value)][logged_in_ips]:
                    self.new_blk_write[str(attacker_action_id.value)][logged_in_ips][str(new_blk_write_change)] \
                        = self.new_blk_write[str(attacker_action_id.value)][logged_in_ips][
                              str(new_blk_write_change)] + 1
                else:
                    self.new_blk_write[str(attacker_action_id.value)][logged_in_ips][str(new_blk_write_change)] = 1
            else:
                self.new_blk_write[str(attacker_action_id.value)][logged_in_ips] = {}
                self.new_blk_write[str(attacker_action_id.value)][logged_in_ips][str(new_blk_write_change)] = 1

    def add_new_net_tx_transition(self, attacker_action_id: Enum, logged_in_ips: str,
                                     new_net_tx_change: int) -> None:
        """
        Adds a new transition for net tx

        :param attacker_action_id: the attacker action that triggered the transition
        :param logged_in_ips: the attacker state
        :param new_net_tx_change: the observed change in net tx
        :return: None
        """
        if str(attacker_action_id.value) not in self.new_net_tx:
            self.new_net_tx[str(attacker_action_id.value)] = {}
            self.new_net_tx[str(attacker_action_id.value)][logged_in_ips] = {}
            self.new_net_tx[str(attacker_action_id.value)][logged_in_ips][str(new_net_tx_change)] = 1
        else:
            if logged_in_ips in self.new_net_tx[str(attacker_action_id.value)]:
                if str(new_net_tx_change) in self.new_net_tx[str(attacker_action_id.value)][logged_in_ips]:
                    self.new_net_tx[str(attacker_action_id.value)][logged_in_ips][str(new_net_tx_change)] \
                        = self.new_net_tx[str(attacker_action_id.value)][logged_in_ips][
                              str(new_net_tx_change)] + 1
                else:
                    self.new_net_tx[str(attacker_action_id.value)][logged_in_ips][str(new_net_tx_change)] = 1
            else:
                self.new_net_tx[str(attacker_action_id.value)][logged_in_ips] = {}
                self.new_net_tx[str(attacker_action_id.value)][logged_in_ips][str(new_net_tx_change)] = 1

    def add_new_net_rx_transition(self, attacker_action_id: Enum, logged_in_ips: str,
                                  new_net_rx_change: int) -> None:
        """
        Adds a new transition for net tx

        :param attacker_action_id: the attacker action that triggered the transition
        :param logged_in_ips: the attacker state
        :param new_net_rx_change: the observed change in net tx
        :return: None
        """
        if str(attacker_action_id.value) not in self.new_net_rx:
            self.new_net_rx[str(attacker_action_id.value)] = {}
            self.new_net_rx[str(attacker_action_id.value)][logged_in_ips] = {}
            self.new_net_rx[str(attacker_action_id.value)][logged_in_ips][str(new_net_rx_change)] = 1
        else:
            if logged_in_ips in self.new_net_rx[str(attacker_action_id.value)]:
                if str(new_net_rx_change) in self.new_net_rx[str(attacker_action_id.value)][logged_in_ips]:
                    self.new_net_rx[str(attacker_action_id.value)][logged_in_ips][str(new_net_rx_change)] \
                        = self.new_net_rx[str(attacker_action_id.value)][logged_in_ips][
                              str(new_net_rx_change)] + 1
                else:
                    self.new_net_rx[str(attacker_action_id.value)][logged_in_ips][str(new_net_rx_change)] = 1
            else:
                self.new_net_rx[str(attacker_action_id.value)][logged_in_ips] = {}
                self.new_net_rx[str(attacker_action_id.value)][logged_in_ips][str(new_net_rx_change)] = 1

    def add_new_init_pids(self, init_pids: int) -> None:
        """
        Adds a new transition for initial pids

        :param init_pids: the observed initial number of pids
        :return: None
        """
        if str(init_pids) in self.init_num_new_pids:
            self.init_num_new_pids[str(init_pids)] = \
                self.init_num_new_pids[str(init_pids)] + 1
        else:
            self.init_num_new_pids[str(init_pids)] = 1

    def add_new_init_cpu_percentage(self, init_cpu_percentage: int) -> None:
        """
        Adds a new transition for initial cpu_percentage

        :param init_cpu_percentage: the observed initial cpu_percentage
        :return: None
        """
        if str(init_cpu_percentage) in self.init_cpu_percentage_change:
            self.init_cpu_percentage_change[str(init_cpu_percentage)] = \
                self.init_cpu_percentage_change[str(init_cpu_percentage)] + 1
        else:
            self.init_cpu_percentage_change[str(init_cpu_percentage)] = 1

    def add_new_init_mem_current(self, init_mem_current: int) -> None:
        """
        Adds a new transition for initial mem_current

        :param init_mem_current: the observed initial mem_current
        :return: None
        """
        if str(init_mem_current) in self.init_new_mem_current:
            self.init_new_mem_current[str(init_mem_current)] = \
                self.init_new_mem_current[str(init_mem_current)] + 1
        else:
            self.init_new_mem_current[str(init_mem_current)] = 1

    def add_new_init_mem_total(self, init_mem_total: int) -> None:
        """
        Adds a new transition for initial mem_total

        :param init_mem_total: the observed initial mem_total
        :return: None
        """
        if str(init_mem_total) in self.init_new_mem_total:
            self.init_new_mem_total[str(init_mem_total)] = \
                self.init_new_mem_total[str(init_mem_total)] + 1
        else:
            self.init_new_mem_total[str(init_mem_total)] = 1

    def add_new_init_mem_percent(self, init_mem_percent: int) -> None:
        """
        Adds a new transition for initial mem_percent

        :param init_mem_percent: the observed initial mem_percent
        :return: None
        """
        if str(init_mem_percent) in self.init_new_mem_percent:
            self.init_new_mem_percent[str(init_mem_percent)] = \
                self.init_new_mem_percent[str(init_mem_percent)] + 1
        else:
            self.init_new_mem_percent[str(init_mem_percent)] = 1

    def add_new_init_blk_read(self, init_blk_read: int) -> None:
        """
        Adds a new transition for initial blk_read

        :param init_blk_read: the observed initial blk_read
        :return: None
        """
        if str(init_blk_read) in self.init_new_blk_read:
            self.init_new_blk_read[str(init_blk_read)] = \
                self.init_new_blk_read[str(init_blk_read)] + 1
        else:
            self.init_new_blk_read[str(init_blk_read)] = 1

    def add_new_init_blk_write(self, init_blk_write: int) -> None:
        """
        Adds a new transition for initial blk_write

        :param init_blk_write: the observed initial blk_write
        :return: None
        """
        if str(init_blk_write) in self.init_new_blk_write:
            self.init_new_blk_write[str(init_blk_write)] = \
                self.init_new_blk_write[str(init_blk_write)] + 1
        else:
            self.init_new_blk_write[str(init_blk_write)] = 1

    def add_new_init_net_rx(self, init_net_rx: int) -> None:
        """
        Adds a new transition for initial net_rx

        :param init_net_rx: the observed initial net_rx
        :return: None
        """
        if str(init_net_rx) in self.init_new_net_rx:
            self.init_new_net_rx[str(init_net_rx)] = \
                self.init_new_net_rx[str(init_net_rx)] + 1
        else:
            self.init_new_net_rx[str(init_net_rx)] = 1

    def add_new_init_net_tx(self, init_net_tx: int) -> None:
        """
        Adds a new transition for initial net_tx

        :param init_net_tx: the observed initial net_tx
        :return: None
        """
        if str(init_net_tx) in self.init_new_net_tx:
            self.init_new_net_tx[str(init_net_tx)] = \
                self.init_new_net_tx[str(init_net_tx)] + 1
        else:
            self.init_new_net_tx[str(init_net_tx)] = 1


    def update_model(self, s, s_prime, attacker_action_id: Enum, logged_in_ips: str, t: int=0,
                     idx: int = 0, attacker_action_name = "", attacker_action_idx : int = 0) \
            -> DefenderDynamicsTensorboardDTO:
        """
        Updates the dynamics model after observing a (s,a)->s' transition.

        :param s: the previous state
        :param s_prime: the new state
        :param attacker_action_id: the attacker action that triggered the transition
        :param logged_in_ips: the attacker state
        :param t: the current time step
        :param idx: trajectory index
        :return: A Tensorboard DTO of the update
        """

        # Update IDS Dynamics
        num_new_alerts = s_prime.defender_obs_state.num_alerts_recent
        self.add_new_alert_transition(attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                      num_new_alerts=num_new_alerts)
        num_new_priority = s_prime.defender_obs_state.sum_priority_alerts_recent
        self.add_new_priority_transition(attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                         num_new_priority=num_new_priority)
        num_new_severe_alerts = s_prime.defender_obs_state.num_severe_alerts_recent
        self.add_new_severe_alert_transition(attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                             num_new_severe_alerts=num_new_severe_alerts)
        num_new_warning_alerts = s_prime.defender_obs_state.num_warning_alerts_recent
        self.add_new_warning_alert_transition(attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                             num_new_warning_alerts=num_new_warning_alerts)

        # Update Docker stats Dynamics
        num_new_pids = s_prime.defender_obs_state.num_pids_recent
        self.add_new_pids_transition(attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                              num_new_pids=num_new_pids)

        cpu_percent_change = s_prime.defender_obs_state.cpu_percent_recent
        self.add_new_cpu_percent_transition(attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                     cpu_percent_change=cpu_percent_change)

        new_mem_current_change = s_prime.defender_obs_state.mem_current_recent
        self.add_new_mem_current_transition(attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                            new_mem_current=new_mem_current_change)

        new_mem_total_change = s_prime.defender_obs_state.mem_total_recent
        self.add_new_mem_total_transition(attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                            new_mem_total_change=new_mem_total_change)

        new_mem_percent_change = s_prime.defender_obs_state.mem_percent_recent
        self.add_new_mem_percent_transition(attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                          new_mem_percent_change=new_mem_percent_change)

        new_blk_read_change = s_prime.defender_obs_state.blk_read_recent
        self.add_new_blk_read_transition(attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                            new_blk_read_change=new_blk_read_change)

        new_blk_write_change = s_prime.defender_obs_state.blk_write_recent
        self.add_new_blk_write_transition(attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                         new_blk_write_change=new_blk_write_change)

        new_net_rx_change = s_prime.defender_obs_state.net_rx_recent
        self.add_new_net_rx_transition(attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                          new_net_rx_change=new_net_rx_change)

        new_net_tx_change = s_prime.defender_obs_state.net_rx_recent
        self.add_new_net_tx_transition(attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                       new_net_tx_change=new_net_tx_change)


        num_new_open_connections_total = 0
        num_new_failed_login_attempts_total = 0
        num_new_users_total = 0
        num_new_logged_in_users_total = 0
        num_new_login_events_total = 0
        num_new_processes_total = 0

        # Update dynamics of all nodes
        for i in range(len(s_prime.defender_obs_state.machines)):
            if s_prime.defender_obs_state.machines[i].ip not in self.machines_dynamics_model or \
                    self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip] is None:
                self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip] = DefenderMachineDynamicsModel()

            num_new_open_connections = s_prime.defender_obs_state.machines[i].num_open_connections \
                                       - s.defender_obs_state.machines[i].num_open_connections
            self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip].add_new_open_connection_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                num_new_open_connections=num_new_open_connections)
            num_new_open_connections_total += num_new_open_connections

            num_new_failed_login_attempts = s_prime.defender_obs_state.machines[i].num_failed_login_attempts_recent
            self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip].add_new_failed_login_attempt_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                num_new_failed_login_attempts=num_new_failed_login_attempts)
            num_new_failed_login_attempts_total += num_new_failed_login_attempts

            num_new_users = s_prime.defender_obs_state.machines[i].num_users_recent
            self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip].add_new_user_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                num_new_users=num_new_users)
            num_new_users_total += num_new_users

            num_new_logged_in_users = s_prime.defender_obs_state.machines[i].num_logged_in_users_recent
            self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip].add_new_logged_in_user_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                num_new_logged_in_users=num_new_logged_in_users)
            num_new_logged_in_users_total += num_new_logged_in_users

            num_new_login_events = s_prime.defender_obs_state.machines[i].num_login_events_recent
            self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip].add_new_login_event_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                num_new_login_events=num_new_login_events)
            num_new_login_events_total += num_new_login_events

            num_new_processes = s_prime.defender_obs_state.machines[i].num_processes_recent
            self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip].add_new_processes_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                num_new_processes=num_new_processes)
            num_new_processes_total += num_new_processes

            # Update Docker stats Dynamics
            num_new_pids_machine = s_prime.defender_obs_state.machines[i].num_pids_recent
            self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip].add_new_pids_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                         num_new_pids=num_new_pids_machine)

            cpu_percent_change_machine = s_prime.defender_obs_state.machines[i].cpu_percent_recent
            self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip].add_new_cpu_percent_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                                cpu_percent_change=cpu_percent_change_machine)

            new_mem_current_change_machine = s_prime.defender_obs_state.machines[i].mem_current_recent
            self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip].add_new_mem_current_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                                new_mem_current=new_mem_current_change_machine)

            new_mem_total_change_machine = s_prime.defender_obs_state.machines[i].mem_total_recent
            self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip].add_new_mem_total_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                              new_mem_total_change=new_mem_total_change_machine)

            new_mem_percent_change_machine = s_prime.defender_obs_state.machines[i].mem_percent_recent
            self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip].add_new_mem_percent_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                                new_mem_percent_change=new_mem_percent_change_machine)

            new_blk_read_change_machine = s_prime.defender_obs_state.machines[i].blk_read_recent
            self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip].add_new_blk_read_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                             new_blk_read_change=new_blk_read_change_machine)

            new_blk_write_change_machine = s_prime.defender_obs_state.machines[i].blk_write_recent
            self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip].add_new_blk_write_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                              new_blk_write_change=new_blk_write_change_machine)

            new_net_rx_change_machine = s_prime.defender_obs_state.machines[i].net_rx_recent
            self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip].add_new_net_rx_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                           new_net_rx_change=new_net_rx_change_machine)

            new_net_tx_change_machine = s_prime.defender_obs_state.machines[i].net_rx_recent
            self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip].add_new_net_tx_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                new_net_tx_change=new_net_tx_change_machine)


        self.add_new_failed_login_attempt_transition(attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                                     num_new_login_attempts=num_new_failed_login_attempts_total)
        self.add_new_connections_transition(attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                                     num_new_connections=num_new_open_connections_total)
        self.add_new_login_events_transition(attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                            num_new_login_events=num_new_login_events_total)
        self.add_new_processes_transition(attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                             num_new_processes=num_new_processes_total)

        tb_dto = DefenderDynamicsTensorboardDTO(
            t=t, num_new_alerts = num_new_alerts, num_new_priority=num_new_priority, 
            num_new_severe_alerts=num_new_severe_alerts, num_new_warning_alerts=num_new_warning_alerts,
            num_new_open_connections=num_new_open_connections_total,
            num_new_failed_login_attempts=num_new_failed_login_attempts_total,
            num_new_login_events=num_new_login_events_total,
            num_new_processes=num_new_processes_total, index=idx, attacker_action_id=attacker_action_id.value,
            attacker_action_idx=attacker_action_idx, attacker_action_name=attacker_action_name,
            num_new_pids=num_new_pids, cpu_percent_change=cpu_percent_change,
            new_mem_current_change=new_mem_current_change,
            new_mem_total_change=new_mem_total_change, new_mem_percent_change=new_mem_percent_change,
            new_blk_read_change=new_blk_read_change,
            new_blk_write_change=new_blk_write_change, new_net_rx_change=new_net_rx_change,
            new_net_tx_change=new_net_tx_change
        )
        return tb_dto

    def update_init_state_distribution(self, init_state) -> None:
        """
        Updates the dynamics model after observing a initial state

        :param init_state: the observed initial state
        :return: None
        """
        # Update global initial state dynamics
        init_pids = init_state.defender_obs_state.num_pids
        self.add_new_init_pids(init_pids=init_pids)
        init_cpu_percentage = init_state.defender_obs_state.cpu_percent
        self.add_new_init_cpu_percentage(init_cpu_percentage=init_cpu_percentage)
        init_mem_current = init_state.defender_obs_state.mem_current
        self.add_new_init_mem_current(init_mem_current=init_mem_current)
        init_mem_total = init_state.defender_obs_state.mem_total
        self.add_new_init_mem_total(init_mem_total=init_mem_total)
        init_mem_percent = init_state.defender_obs_state.mem_percent
        self.add_new_init_mem_percent(init_mem_percent=init_mem_percent)
        init_blk_read = init_state.defender_obs_state.blk_read
        self.add_new_init_blk_read(init_blk_read=init_blk_read)
        init_blk_write = init_state.defender_obs_state.blk_write
        self.add_new_init_blk_write(init_blk_write=init_blk_write)
        init_net_rx = init_state.defender_obs_state.net_rx
        self.add_new_init_net_rx(init_net_rx=init_net_rx)
        init_net_tx = init_state.defender_obs_state.net_tx
        self.add_new_init_net_tx(init_net_tx=init_net_tx)


        # Update initial state dynamics of all nodes
        for i in range(len(init_state.defender_obs_state.machines)):
            if init_state.defender_obs_state.machines[i].ip not in self.machines_dynamics_model or \
                    self.machines_dynamics_model[init_state.defender_obs_state.machines[i].ip] is None:
                self.machines_dynamics_model[init_state.defender_obs_state.machines[i].ip] = DefenderMachineDynamicsModel()

            init_connections = init_state.defender_obs_state.machines[i].num_open_connections
            self.machines_dynamics_model[init_state.defender_obs_state.machines[i].ip].add_new_init_connections(
                init_open_connections=init_connections)

            init_users = init_state.defender_obs_state.machines[i].num_users
            self.machines_dynamics_model[init_state.defender_obs_state.machines[i].ip].add_new_init_users(
                init_users=init_users)

            init_logged_in_users = init_state.defender_obs_state.machines[i].num_logged_in_users
            self.machines_dynamics_model[init_state.defender_obs_state.machines[i].ip].add_new_init_logged_in_users(
                init_logged_in_users=init_logged_in_users)

            init_processes = init_state.defender_obs_state.machines[i].num_processes
            self.machines_dynamics_model[init_state.defender_obs_state.machines[i].ip].add_new_init_processes(
                init_processes=init_processes)

            init_pids = init_state.defender_obs_state.machines[i].num_pids
            self.machines_dynamics_model[init_state.defender_obs_state.machines[i].ip].add_new_init_pids(init_pids=init_pids)
            init_cpu_percentage = init_state.defender_obs_state.machines[i].cpu_percent
            self.machines_dynamics_model[init_state.defender_obs_state.machines[i].ip].add_new_init_cpu_percentage(init_cpu_percentage=init_cpu_percentage)
            init_mem_current = init_state.defender_obs_state.machines[i].mem_current
            self.machines_dynamics_model[init_state.defender_obs_state.machines[i].ip].add_new_init_mem_current(init_mem_current=init_mem_current)
            init_mem_total = init_state.defender_obs_state.machines[i].mem_total
            self.machines_dynamics_model[init_state.defender_obs_state.machines[i].ip].add_new_init_mem_total(init_mem_total=init_mem_total)
            init_mem_percent = init_state.defender_obs_state.machines[i].mem_percent
            self.machines_dynamics_model[init_state.defender_obs_state.machines[i].ip].add_new_init_mem_percent(init_mem_percent=init_mem_percent)
            init_blk_read = init_state.defender_obs_state.machines[i].blk_read
            self.machines_dynamics_model[init_state.defender_obs_state.machines[i].ip].add_new_init_blk_read(init_blk_read=init_blk_read)
            init_blk_write = init_state.defender_obs_state.machines[i].blk_write
            self.machines_dynamics_model[init_state.defender_obs_state.machines[i].ip].add_new_init_blk_write(init_blk_write=init_blk_write)
            init_net_rx = init_state.defender_obs_state.machines[i].net_rx
            self.machines_dynamics_model[init_state.defender_obs_state.machines[i].ip].add_new_init_net_rx(init_net_rx=init_net_rx)
            init_net_tx = init_state.defender_obs_state.machines[i].net_tx
            self.machines_dynamics_model[init_state.defender_obs_state.machines[i].ip].add_new_init_net_tx(init_net_tx=init_net_tx)



    def reset(self) -> None:
        """
        Resets the model

        :return: None
        """
        self.num_new_alerts = {}
        self.num_new_priority = {}
        self.num_new_severe_alerts = {}
        self.num_new_warning_alerts = {}
        self.num_new_pids = {}
        self.cpu_percentage_change = {}
        self.new_mem_current = {}
        self.new_mem_total = {}
        self.new_mem_percent = {}
        self.new_blk_read = {}
        self.new_blk_write = {}
        self.new_net_rx = {}
        self.new_net_tx = {}
        self.init_num_new_pids = {}
        self.init_cpu_percentage_change = {}
        self.init_new_mem_current = {}
        self.init_new_mem_total = {}
        self.init_new_mem_percent = {}
        self.init_new_blk_read = {}
        self.init_new_blk_write = {}
        self.init_new_net_rx = {}
        self.init_new_net_tx = {}
        self.machines_dynamics_model = {}


        self.norm_num_new_alerts = {}
        self.norm_num_new_priority = {}
        self.norm_num_new_severe_alerts = {}
        self.norm_num_new_warning_alerts = {}
        self.norm_machines_dynamics_model = {}
        self.norm_num_new_pids = {}
        self.norm_cpu_percentage_change = {}
        self.norm_new_mem_current = {}
        self.norm_new_mem_total = {}
        self.norm_new_mem_percent = {}
        self.norm_new_blk_read = {}
        self.norm_new_blk_write = {}
        self.norm_new_net_rx = {}
        self.norm_new_net_tx = {}
        self.norm_init_num_new_pids = {}
        self.norm_init_cpu_percentage_change = {}
        self.norm_init_new_mem_current = {}
        self.norm_init_new_mem_total = {}
        self.norm_init_new_mem_percent = {}
        self.norm_init_new_blk_read = {}
        self.norm_init_new_blk_write = {}
        self.norm_init_new_net_rx = {}
        self.norm_init_new_net_tx = {}

    def __str__(self):
        try:
            return f"alerts_dynamics:{self.num_new_alerts},\n priority_dynamics:{self.num_new_priority}," \
                   f"\n severe_alerts_dynamics:{self.num_new_severe_alerts},\n " \
                   f"warning_alerts_dynamics:{self.num_new_warning_alerts},\n " \
                   f"failed_login_attempts_dynamics:{self.num_new_failed_login_attempts}\n," \
                   f"connections_dynamics:{self.num_new_open_connections},\n " \
                   f"login_events_dynamics:{self.num_new_login_events},\n " \
                   f"processes_dynamics:{self.num_new_processes},\n" \
                   f"norm_alerts_dynamics:{self.norm_num_new_alerts.values()},\n " \
                   f"norm_priority_dynamics:{self.norm_num_new_priority.values()},\n" \
                   f"norm_severe_alerts_dynamics:{self.norm_num_new_severe_alerts.values()}," \
                   f"\n norm_warning_alerts_dynamics:{self.norm_num_new_warning_alerts.values()},\n" \
                   f"norm_failed_login_attempts_dynamics:{self.norm_num_new_failed_login_attempts.values()},\n " \
                   f"norm_connections_dynamics:{self.norm_num_new_open_connections.values()},\n " \
                   f"norm_login_events_dynamics:{self.norm_num_new_login_events.values()},\n " \
                   f"norm_processes_dynamics:{self.norm_num_new_processes.values()},\n " \
                   f"norm_machines_dynamics_model: {str(self.machines_dynamics_model)}\n" \
                   f"num_new_pids: {self.num_new_pids}\n, cpu_percentage_change: {self.cpu_percentage_change}, \n" \
                   f"new_mem_current: {self.new_mem_current}, \n new_mem_total: {self.new_mem_total}, \n," \
                   f"new_mem_percent: {self.new_mem_percent}, \n new_blk_read: {self.new_blk_read}, " \
                   f"new_blk_write: {self.new_blk_write}, new_net_rx: {self.new_net_rx}, new_net_tx: {self.new_net_tx}" \
                   f"norm_num_new_pids: {self.norm_num_new_pids.values()}\n, " \
                   f"norm_cpu_percentage_change: {self.norm_cpu_percentage_change.values()}, \n" \
                   f"norm_new_mem_current: {self.norm_new_mem_current.values()}, \n " \
                   f"norm_new_mem_total: {self.norm_new_mem_total.values()}, \n," \
                   f"norm_new_mem_percent: {self.norm_new_mem_percent.values()}, \n " \
                   f"norm_new_blk_read: {self.norm_new_blk_read.values()}, " \
                   f"norm_new_blk_write: {self.norm_new_blk_write.values()}, " \
                   f"norm_new_net_rx: {self.norm_new_net_rx.values()}, " \
                   f"norm_new_net_tx: {self.norm_new_net_tx.values()}" \
                   f"init_num_new_pids: {self.init_num_new_pids}\n, " \
                   f"init_cpu_percentage_change: {self.init_cpu_percentage_change}, \n" \
                   f"init_new_mem_current: {self.init_new_mem_current}, \n " \
                   f"init_new_mem_total: {self.init_new_mem_total}, \n," \
                   f"init_new_mem_percent: {self.init_new_mem_percent}, \n " \
                   f"init_new_blk_read: {self.init_new_blk_read}, " \
                   f"init_new_blk_write: {self.init_new_blk_write}, init_new_net_rx: {self.init_new_net_rx}, " \
                   f"init_new_net_tx: {self.init_new_net_tx}" \
                   f"norm_init_num_new_pids: {self.norm_init_num_new_pids.values()}\n, " \
                   f"norm_init_cpu_percentage_change: {self.norm_init_cpu_percentage_change.values()}, \n" \
                   f"norm_init_new_mem_current: {self.norm_init_new_mem_current.values()}, \n " \
                   f"norm_init_new_mem_total: {self.norm_init_new_mem_total.values()}, \n," \
                   f"norm_init_new_mem_percent: {self.norm_init_new_mem_percent.values()}, \n " \
                   f"norm_init_new_blk_read: {self.norm_init_new_blk_read.values()}, " \
                   f"norm_init_new_blk_write: {self.norm_init_new_blk_write.values()}, " \
                   f"norm_init_new_net_rx: {self.norm_init_new_net_rx.values()}, " \
                   f"norm_init_new_net_tx: {self.norm_init_new_net_tx.values()}"
        except:
            return f"alerts_dynamics:{self.num_new_alerts},\n priority_dynamics:{self.num_new_priority}," \
                   f"\n severe_alerts_dynamics:{self.num_new_severe_alerts},\n " \
                   f"warning_alerts_dynamics:{self.num_new_warning_alerts},\n " \
                   f"norm_alerts_dynamics:{self.norm_num_new_alerts},\n " \
                   f"norm_priority_dynamics:{self.norm_num_new_priority},\n" \
                   f"norm_severe_alerts_dynamics:{self.norm_num_new_severe_alerts},\n " \
                   f"norm_warning_alerts_dynamics:{self.norm_num_new_warning_alerts},\n" \
                   f"machines_dynamics_model: {str(self.machines_dynamics_model)}\n, " \
                   f"num_new_pids: {self.num_new_pids}\n, cpu_percentage_change: {self.cpu_percentage_change}, \n" \
                   f"new_mem_current: {self.new_mem_current}, \n new_mem_total: {self.new_mem_total}, \n," \
                   f"new_mem_percent: {self.new_mem_percent}, \n new_blk_read: {self.new_blk_read}, " \
                   f"new_blk_write: {self.new_blk_write}, new_net_rx: {self.new_net_rx}, new_net_tx: {self.new_net_tx}" \
                   f"init_num_new_pids: {self.init_num_new_pids}\n, " \
                   f"init_cpu_percentage_change: {self.init_cpu_percentage_change}, \n" \
                   f"init_new_mem_current: {self.init_new_mem_current}, \n " \
                   f"init_new_mem_total: {self.init_new_mem_total}, \n," \
                   f"init_new_mem_percent: {self.init_new_mem_percent}, \n " \
                   f"init_new_blk_read: {self.init_new_blk_read}, " \
                   f"init_new_blk_write: {self.init_new_blk_write}, init_new_net_rx: {self.init_new_net_rx}, " \
                   f"init_new_net_tx: {self.init_new_net_tx}" \
                   f"norm_init_num_new_pids: {self.norm_init_num_new_pids}\n, " \
                   f"norm_init_cpu_percentage_change: {self.norm_init_cpu_percentage_change}, \n" \
                   f"norm_init_new_mem_current: {self.norm_init_new_mem_current}, \n " \
                   f"norm_init_new_mem_total: {self.norm_init_new_mem_total}, \n," \
                   f"norm_init_new_mem_percent: {self.norm_init_new_mem_percent}, \n " \
                   f"norm_init_new_blk_read: {self.norm_init_new_blk_read}, " \
                   f"norm_init_new_blk_write: {self.norm_init_new_blk_write}, " \
                   f"norm_init_new_net_rx: {self.norm_init_new_net_rx}, " \
                   f"norm_init_new_net_tx: {self.norm_init_new_net_tx}"

    def to_dict(self) -> dict:
        """
        Converts the model to a dict representation

        :return: dict representation of the model
        """
        d={}
        d["num_new_alerts"] = self.num_new_alerts
        d["num_new_priority"] = self.num_new_priority
        d["num_new_severe_alerts"] = self.num_new_severe_alerts
        d["num_new_warning_alerts"] = self.num_new_warning_alerts
        d["num_new_failed_login_attempts"] = self.num_new_failed_login_attempts
        d["num_new_open_connections"] = self.num_new_open_connections
        d["num_new_login_events"] = self.num_new_login_events
        d["num_new_processes"] = self.num_new_processes
        d["num_new_pids"] = self.num_new_pids
        d["cpu_percentage_change"] = self.cpu_percentage_change
        d["new_mem_current"] = self.new_mem_current
        d["new_mem_total"] = self.new_mem_total
        d["new_mem_percent"] = self.new_mem_percent
        d["new_blk_read"] = self.new_blk_read
        d["new_blk_write"] = self.new_blk_write
        d["new_net_rx"] = self.new_net_rx
        d["new_net_tx"] = self.new_net_tx
        d["init_num_new_pids"] = self.init_num_new_pids
        d["init_cpu_percentage_change"] = self.init_cpu_percentage_change
        d["init_new_mem_current"] = self.init_new_mem_current
        d["init_new_mem_total"] = self.init_new_mem_total
        d["init_new_mem_percent"] = self.init_new_mem_percent
        d["init_new_blk_read"] = self.init_new_blk_read
        d["init_new_blk_write"] = self.init_new_blk_write
        d["init_new_net_rx"] = self.init_new_net_rx
        d["init_new_net_tx"] = self.init_new_net_tx

        m_dynamics_model_new = {}
        for k,v in self.machines_dynamics_model.items():
            m_dynamics_model_new[k]=v.to_dict()
        d["machines_dynamics_model"] = m_dynamics_model_new
        return d

    def from_dict(self, d) -> None:
        """
        Bootstraps the model with data from a dict

        :param d: the input dict
        :return: None
        """
        self.num_new_alerts = d["num_new_alerts"].copy()
        self.num_new_priority = d["num_new_priority"].copy()
        self.num_new_severe_alerts = d["num_new_severe_alerts"].copy()
        self.num_new_warning_alerts = d["num_new_warning_alerts"].copy()
        if "num_new_failed_login_attempts" in d:
            self.num_new_failed_login_attempts = d["num_new_failed_login_attempts"].copy()
        if "num_new_open_connections" in d:
            self.num_new_open_connections = d["num_new_open_connections"].copy()
        if "num_new_login_events" in d:
            self.num_new_login_events = d["num_new_login_events"].copy()
        if "num_new_processes" in d:
            self.num_new_processes = d["num_new_processes"].copy()
        if "num_new_pids" in d:
            self.num_new_pids = d["num_new_pids"].copy()
        if "cpu_percentage_change" in d:
            self.cpu_percentage_change = d["cpu_percentage_change"].copy()
        if "new_mem_current" in d:
            self.new_mem_current = d["new_mem_current"].copy()
        if "new_mem_total" in d:
            self.new_mem_total = d["new_mem_total"].copy()
        if "new_mem_percent" in d:
            self.new_mem_percent = d["new_mem_percent"].copy()
        if "new_blk_read" in d:
            self.new_blk_read = d["new_blk_read"].copy()
        if "new_blk_write" in d:
            self.new_blk_write = d["new_blk_write"].copy()
        if "new_net_rx" in d:
            self.new_net_rx = d["new_net_rx"].copy()
        if "new_net_tx" in d:
            self.new_net_tx = d["new_net_tx"].copy()

        if "init_num_new_pids" in d:
            self.init_num_new_pids = d["init_num_new_pids"].copy()
        if "init_cpu_percentage_change" in d:
            self.init_cpu_percentage_change = d["init_cpu_percentage_change"].copy()
        if "init_new_mem_current" in d:
            self.init_new_mem_current = d["init_new_mem_current"].copy()
        if "init_new_mem_total" in d:
            self.init_new_mem_total = d["init_new_mem_total"].copy()
        if "init_new_mem_percent" in d:
            self.init_new_mem_percent = d["init_new_mem_percent"].copy()
        if "init_new_blk_read" in d:
            self.init_new_blk_read = d["init_new_blk_read"].copy()
        if "init_new_blk_write" in d:
            self.init_new_blk_write = d["init_new_blk_write"].copy()
        if "init_new_net_rx" in d:
            self.init_new_net_rx = d["init_new_net_rx"].copy()
        if "init_new_net_tx" in d:
            self.init_new_net_tx = d["init_new_net_tx"].copy()

        m_dynamics_model_new = {}
        for k, v in d["machines_dynamics_model"].items():
            m = DefenderMachineDynamicsModel()
            m.from_dict(v)
            m_dynamics_model_new[k]= m
        self.machines_dynamics_model = m_dynamics_model_new

    def save_model(self, dir_path : str, model_name: str) -> None:
        """
        Saves the model to disk as a json file

        :param dir_path: the path to the dir where to save the model
        :param model_name: the name of the model file
        :return: None
        """
        if model_name is None:
            model_name = constants.SYSTEM_IDENTIFICATION.DEFENDER_DYNAMICS_MODEL_FILE
        save_dir = None
        if dir_path is not None:
            save_dir = dir_path + "/" \
                       + model_name
        else:
            save_dir = util.get_script_path() + "/" + \
                       model_name
        d = self.to_dict()
        with open(save_dir, 'w') as fp:
            json.dump(d, fp)

    def read_model(self, dir_path:str, model_name : str = None) -> None:
        """
        Loads json model from disk (according to env config) and populates the model

        :param dir_path: the path to the dir where the model is stored
        :param model_name: (optional) a custom model name
        :return: None
        """
        if model_name is None:
            model_name = constants.SYSTEM_IDENTIFICATION.DEFENDER_DYNAMICS_MODEL_FILE
        load_dir = None
        if dir_path is not None:
            load_dir = dir_path + "/" + model_name
        else:
            load_dir = util.get_script_path() + "/" + model_name
        if os.path.exists(load_dir):
            with open(load_dir, 'r') as fp:
                d = json.load(fp)
                self.from_dict(d)
        else:
            print("Warning: Could not read dynamics model, path does not exist:{}".format(load_dir))

    def read_model_path(self, path: str) -> None:
        """
        Reads a json model from a specific path and populates the model

        :param path: the path to read the model from
        :return: None
        """
        load_dir = path
        if os.path.exists(load_dir):
            with open(load_dir, 'r') as fp:
                d = json.load(fp)
                self.from_dict(d)

