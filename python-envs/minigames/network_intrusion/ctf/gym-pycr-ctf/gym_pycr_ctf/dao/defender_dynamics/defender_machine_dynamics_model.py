from scipy import stats
import numpy as np
from gym_pycr_ctf.dao.action.attacker.attacker_action import AttackerActionId

class DefenderMachineDynamicsModel:
    """
    Represents a dynamics model of specific machiens in the emulation of
    the defender for simulating stochastic (b, a) -> b' transitions based on
    maximum likelihood estimations
    """

    def __init__(self):
        self.num_new_open_connections = {}
        self.num_new_failed_login_attempts = {}
        self.num_new_users = {}
        self.num_new_logged_in_users = {}
        self.num_new_login_events = {}
        self.num_new_processes = {}

        self.norm_num_new_open_connections = {}
        self.norm_num_new_failed_login_attempts = {}
        self.norm_num_new_users = {}
        self.norm_num_new_logged_in_users = {}
        self.norm_num_new_login_events = {}
        self.norm_num_new_processes = {}

    def normalize(self) -> None:
        """
        Normalizes transition counts into distributions

        :return: None
        """

        # Normalize num_new_open_connections
        for attack_id_str, v1 in self.num_new_open_connections.items():
            for logged_in_ips, v2 in v1.items():
                samples = []
                counts = []
                for num_connections_str, count in v2.items():
                    samples.append(int(num_connections_str))
                    counts.append(count)
                counts = np.array(counts)
                samples = np.array(samples)
                empirical_probabilities = counts/np.sum(counts)
                dist = stats.rv_discrete(name='num_new_open_connections_emp_dist', values=(samples, empirical_probabilities))
                self.norm_num_new_open_connections[(int(attack_id_str), logged_in_ips)] = dist

        # Normalize num_new_failed_login_attempts
        for attack_id_str, v1 in self.num_new_failed_login_attempts.items():
            for logged_in_ips, v2 in v1.items():
                samples = []
                counts = []
                for num_failed_attempts_str, count in v2.items():
                    samples.append(int(num_failed_attempts_str))
                    counts.append(count)
                counts = np.array(counts)
                samples = np.array(samples)
                empirical_probabilities = counts / np.sum(counts)
                dist = stats.rv_discrete(name='num_new_failed_login_attempts_emp_dist',
                                         values=(samples, empirical_probabilities))
                self.norm_num_new_failed_login_attempts[(int(attack_id_str), logged_in_ips)] = dist

        # Normalize num_new_users
        for attack_id_str, v1 in self.num_new_users.items():
            for logged_in_ips, v2 in v1.items():
                samples = []
                counts = []
                for num_users_str, count in v2.items():
                    samples.append(int(num_users_str))
                    counts.append(count)
                counts = np.array(counts)
                samples = np.array(samples)
                empirical_probabilities = counts / np.sum(counts)
                dist = stats.rv_discrete(name='num_new_users_emp_dist',
                                         values=(samples, empirical_probabilities))
                self.norm_num_new_users[(int(attack_id_str), logged_in_ips)] = dist

        # Normalize num_new_logged_in_users
        for attack_id_str, v1 in self.num_new_logged_in_users.items():
            for logged_in_ips, v2 in v1.items():
                samples = []
                counts = []
                for num_logged_in_users_str, count in v2.items():
                    samples.append(int(num_logged_in_users_str))
                    counts.append(count)
                counts = np.array(counts)
                samples = np.array(samples)
                empirical_probabilities = counts / np.sum(counts)
                dist = stats.rv_discrete(name='num_new_logged_in_users_emp_dist',
                                         values=(samples, empirical_probabilities))
                self.norm_num_new_logged_in_users[(int(attack_id_str), logged_in_ips)] = dist

        # Normalize num_new_login_events
        for attack_id_str, v1 in self.num_new_login_events.items():
            for logged_in_ips, v2 in v1.items():
                samples = []
                counts = []
                for num_new_login_events_str, count in v2.items():
                    samples.append(int(num_new_login_events_str))
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
                for num_new_processes_str, count in v2.items():
                    samples.append(int(num_new_processes_str))
                    counts.append(count)
                counts = np.array(counts)
                samples = np.array(samples)
                empirical_probabilities = counts / np.sum(counts)
                dist = stats.rv_discrete(name='num_new_processes_emp_dist',
                                         values=(samples, empirical_probabilities))
                self.norm_num_new_processes[(int(attack_id_str), logged_in_ips)] = dist

    def add_new_open_connection_transition(self, attacker_action_id: AttackerActionId, logged_in_ips : str,
                                 num_new_open_connections: int) -> None:
        """
        Adds a new transition for open connections
        :param attacker_action_id: the attacker action that triggered the transition
        :param logged_in_ips: the attacker state
        :param num_new_open_connections: the observed new number of connections
        :return: None
        """
        if str(attacker_action_id.value) not in self.num_new_open_connections:
            self.num_new_open_connections[str(attacker_action_id.value)] = {}
            self.num_new_open_connections[str(attacker_action_id.value)][logged_in_ips] = {}
            self.num_new_open_connections[str(attacker_action_id.value)][logged_in_ips][
                str(num_new_open_connections)] = 1
        else:
            if logged_in_ips in self.num_new_open_connections[str(attacker_action_id.value)]:
                if str(num_new_open_connections) in self.num_new_open_connections[
                    str(attacker_action_id.value)][logged_in_ips]:
                    self.num_new_open_connections[str(attacker_action_id.value)][logged_in_ips][
                        str(num_new_open_connections)] \
                        = self.num_new_open_connections[str(attacker_action_id.value)][logged_in_ips][
                              str(num_new_open_connections)] + 1
                else:
                    self.num_new_open_connections[str(attacker_action_id.value)][logged_in_ips][
                        str(num_new_open_connections)] = 1
            else:
                self.num_new_open_connections[str(attacker_action_id.value)][logged_in_ips] = {}
                self.num_new_open_connections[str(attacker_action_id.value)][logged_in_ips][
                    str(num_new_open_connections)] = 1

    def add_new_failed_login_attempt_transition(self, attacker_action_id: AttackerActionId, logged_in_ips : str,
                                    num_new_failed_login_attempts: int):
        """
        Adds a new transition for failed login attempts

        :param attacker_action_id: the attacker action that triggered the transition
        :param logged_in_ips: the attacker state
        :param num_new_failed_login_attempts: the observed new number of faield login attempts
        :return: Noneg
        """
        if str(attacker_action_id.value) not in self.num_new_failed_login_attempts:
            self.num_new_failed_login_attempts[str(attacker_action_id.value)] = {}
            self.num_new_failed_login_attempts[str(attacker_action_id.value)][logged_in_ips] = {}
            self.num_new_failed_login_attempts[str(attacker_action_id.value)][logged_in_ips][
                str(num_new_failed_login_attempts)] = 1
        else:
            if logged_in_ips in self.num_new_failed_login_attempts[str(attacker_action_id.value)]:
                if str(num_new_failed_login_attempts) in self.num_new_failed_login_attempts[
                    str(attacker_action_id.value)][logged_in_ips]:
                    self.num_new_failed_login_attempts[str(attacker_action_id.value)][logged_in_ips][
                        str(num_new_failed_login_attempts)] \
                        = self.num_new_failed_login_attempts[str(attacker_action_id.value)][logged_in_ips][
                              str(num_new_failed_login_attempts)] + 1
                else:
                    self.num_new_failed_login_attempts[str(attacker_action_id.value)][logged_in_ips][
                        str(num_new_failed_login_attempts)] = 1
            else:
                self.num_new_failed_login_attempts[str(attacker_action_id.value)][logged_in_ips] = {}
                self.num_new_failed_login_attempts[str(attacker_action_id.value)][logged_in_ips][
                    str(num_new_failed_login_attempts)] = 1

    def add_new_user_transition(self, attacker_action_id: AttackerActionId, logged_in_ips : str,
                                        num_new_users: int) -> None:
        """
        Adds a new transition for user accounts

        :param attacker_action_id: the attacker action that triggered the transition
        :param logged_in_ips: the attacker state
        :param num_new_users: the observed number of new users
        :return: None
        """
        if str(attacker_action_id.value) not in self.num_new_users:
            self.num_new_users[str(attacker_action_id.value)] = {}
            self.num_new_users[str(attacker_action_id.value)][logged_in_ips] = {}
            self.num_new_users[str(attacker_action_id.value)][logged_in_ips][str(num_new_users)] = 1
        else:
            if logged_in_ips in self.num_new_users[str(attacker_action_id.value)]:
                if str(num_new_users) in self.num_new_users[str(attacker_action_id.value)][logged_in_ips]:
                    self.num_new_users[str(attacker_action_id.value)][logged_in_ips][str(num_new_users)] \
                        = self.num_new_users[str(attacker_action_id.value)][logged_in_ips][str(num_new_users)] + 1
                else:
                    self.num_new_users[str(attacker_action_id.value)][logged_in_ips][str(num_new_users)] = 1
            else:
                self.num_new_users[str(attacker_action_id.value)][logged_in_ips] = {}
                self.num_new_users[str(attacker_action_id.value)][logged_in_ips][str(num_new_users)] = 1

    def add_new_logged_in_user_transition(self, attacker_action_id: AttackerActionId, logged_in_ips : str,
                                          num_new_logged_in_users: int) -> None:
        """
        Adds a new transition for logged in users

        :param attacker_action_id: the attacker action that triggered the transition
        :param logged_in_ips: the attacker state
        :param num_new_logged_in_users: the observed number of new logged in users
        :return: None
        """
        if str(attacker_action_id.value) not in self.num_new_logged_in_users:
            self.num_new_logged_in_users[str(attacker_action_id.value)] = {}
            self.num_new_logged_in_users[str(attacker_action_id.value)][logged_in_ips] = {}
            self.num_new_logged_in_users[str(attacker_action_id.value)][logged_in_ips][
                str(num_new_logged_in_users)] = 1
        else:
            if logged_in_ips in self.num_new_logged_in_users[str(attacker_action_id.value)]:
                if str(num_new_logged_in_users) in self.num_new_logged_in_users[
                    str(attacker_action_id.value)][logged_in_ips]:
                    self.num_new_logged_in_users[str(attacker_action_id.value)][logged_in_ips][
                        str(num_new_logged_in_users)] \
                        = self.num_new_logged_in_users[str(attacker_action_id.value)][logged_in_ips][
                              str(num_new_logged_in_users)] + 1
                else:
                    self.num_new_logged_in_users[str(attacker_action_id.value)][logged_in_ips][
                        str(num_new_logged_in_users)] = 1
            else:
                self.num_new_logged_in_users[str(attacker_action_id.value)][logged_in_ips] = {}
                self.num_new_logged_in_users[str(attacker_action_id.value)][logged_in_ips][
                    str(num_new_logged_in_users)] = 1

    def add_new_login_event_transition(self, attacker_action_id: AttackerActionId, logged_in_ips : str,
                                         num_new_login_events: int) -> None:
        """
        Adds a new transition for login events

        :param attacker_action_id: the attacker action that triggered the transition
        :param logged_in_ips: the attacker state
        :param num_new_login_events: the observed new number of login events
        :return: None
        """
        if str(attacker_action_id.value) not in self.num_new_login_events:
            self.num_new_login_events[str(attacker_action_id.value)] = {}
            self.num_new_login_events[str(attacker_action_id.value)][logged_in_ips] = {}
            self.num_new_login_events[str(attacker_action_id.value)][logged_in_ips][str(num_new_login_events)] = 1
        else:
            if logged_in_ips in self.num_new_login_events[str(attacker_action_id.value)]:
                if str(num_new_login_events) in self.num_new_login_events[str(attacker_action_id.value)][
                    logged_in_ips]:
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

    def add_new_processes_transition(self, attacker_action_id: AttackerActionId, logged_in_ips : str,
                                          num_new_processes: int) -> None:
        """
        Adds a new transition for running processes

        :param attacker_action_id: the attacker action that triggered the transition
        :param logged_in_ips: the attacker state
        :param num_new_processes: the observed new number of processes
        :return: None
        """
        if str(attacker_action_id.value) not in self.num_new_processes:
            self.num_new_processes[str(attacker_action_id.value)] = {}
            self.num_new_processes[str(attacker_action_id.value)][logged_in_ips] = {}
            self.num_new_processes[str(attacker_action_id.value)][logged_in_ips][str(num_new_processes)] = 1
        else:
            if logged_in_ips in self.num_new_processes[str(attacker_action_id.value)]:
                if str(num_new_processes) in self.num_new_processes[str(attacker_action_id.value)][
                    logged_in_ips]:
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

    def reset(self) -> None:
        """
        Resets the model

        :return: None
        """
        self.num_new_open_connections = {}
        self.num_new_failed_login_attempts = {}
        self.num_new_users = {}
        self.num_new_logged_in_users = {}
        self.num_new_login_events = {}
        self.num_new_processes = {}

        self.norm_num_new_open_connections = {}
        self.norm_num_new_failed_login_attempts = {}
        self.norm_num_new_users = {}
        self.norm_num_new_logged_in_users = {}
        self.norm_num_new_login_events = {}
        self.norm_num_new_processes = {}

    def __str__(self):
        return "open_connections_dynamics:{},\n failed_login_attempts_dynamics:{},\n user_dynamics:{},\n " \
               "logged_in_users_dynamics:{},\n login_events_dynamics:{},\n processes_dynamics:{}\n".format(
            self.num_new_open_connections, self.num_new_failed_login_attempts, self.num_new_users,
            self.num_new_logged_in_users, self.num_new_login_events, self.num_new_processes
        )

    def to_dict(self) -> dict:
        """
        Converts the model to a dict representation

        :return: a dict representation of the model
        """
        d = {}
        d["num_new_open_connections"] = self.num_new_open_connections
        d["num_new_failed_login_attempts"] = self.num_new_failed_login_attempts
        d["num_new_users"] = self.num_new_users
        d["num_new_logged_in_users"] = self.num_new_logged_in_users
        d["num_new_login_events"] = self.num_new_login_events
        d["num_new_processes"] = self.num_new_processes
        return d


    def from_dict(self, d) -> None:
        """
        Populates the model with data from a dict

        :param d: the dict to use to populate the model
        :return: None
        """
        self.num_new_open_connections = d["num_new_open_connections"]
        self.num_new_failed_login_attempts = d["num_new_failed_login_attempts"]
        self.num_new_users = d["num_new_users"]
        self.num_new_logged_in_users = d["num_new_logged_in_users"]
        self.num_new_login_events = d["num_new_login_events"]
        self.num_new_processes = d["num_new_processes"]




