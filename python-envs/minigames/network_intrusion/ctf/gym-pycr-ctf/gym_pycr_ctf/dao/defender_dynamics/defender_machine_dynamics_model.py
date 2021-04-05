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

        self.init_open_connections = {}
        self.init_users = {}
        self.init_logged_in_users = {}
        self.init_processes = {}

        self.norm_num_new_open_connections = {}
        self.norm_num_new_failed_login_attempts = {}
        self.norm_num_new_users = {}
        self.norm_num_new_logged_in_users = {}
        self.norm_num_new_login_events = {}
        self.norm_num_new_processes = {}

        self.norm_init_open_connections = None
        self.norm_init_users = None
        self.norm_init_logged_in_users = None
        self.norm_init_processes = None

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

        # Normalize num_init_connections
        samples = []
        counts = []
        for init_connections_str, count in self.init_open_connections.items():
            samples.append(int(init_connections_str))
            counts.append(count)
        counts = np.array(counts)
        samples = np.array(samples)
        empirical_probabilities = counts / np.sum(counts)
        dist = stats.rv_discrete(name='init_connections_emp_dist',
                                 values=(samples, empirical_probabilities))
        self.norm_init_open_connections = dist

        # Normalize num_init_users
        samples = []
        counts = []
        for init_connections_str, count in self.init_users.items():
            samples.append(int(init_connections_str))
            counts.append(count)
        counts = np.array(counts)
        samples = np.array(samples)
        empirical_probabilities = counts / np.sum(counts)
        dist = stats.rv_discrete(name='init_users_emp_dist',
                                 values=(samples, empirical_probabilities))
        self.norm_init_users = dist

        # Normalize num_init_logged_in_users
        samples = []
        counts = []
        for init_connections_str, count in self.init_logged_in_users.items():
            samples.append(int(init_connections_str))
            counts.append(count)
        counts = np.array(counts)
        samples = np.array(samples)
        empirical_probabilities = counts / np.sum(counts)
        dist = stats.rv_discrete(name='init_logged_in_users_emp_dist',
                                 values=(samples, empirical_probabilities))
        self.norm_init_logged_in_users = dist

        # Normalize num_init_processe
        samples = []
        counts = []
        for init_connections_str, count in self.init_processes.items():
            samples.append(int(init_connections_str))
            counts.append(count)
        counts = np.array(counts)
        samples = np.array(samples)
        empirical_probabilities = counts / np.sum(counts)
        dist = stats.rv_discrete(name='init_processes_users_emp_dist',
                                 values=(samples, empirical_probabilities))
        self.norm_init_processes = dist

    def add_new_init_connections(self, init_open_connections: int) -> None:
        """
        Adds a new transition for initial open connections

        :param init_open_connections: the observed initial number of connections
        :return: None
        """
        if str(init_open_connections) in self.init_open_connections:
            self.init_open_connections[str(init_open_connections)] = \
                self.init_open_connections[str(init_open_connections)] + 1
        else:
            self.init_open_connections[str(init_open_connections)] = 1

    def add_new_init_users(self, init_users: int) -> None:
        """
        Adds a new transition for initial users

        :param init_users: the observed initial number of users
        :return: None
        """
        if str(init_users) in self.init_users:
            self.init_users[str(init_users)] = \
                self.init_users[str(init_users)] + 1
        else:
            self.init_users[str(init_users)] = 1

    def add_new_init_logged_in_users(self, init_logged_in_users: int) -> None:
        """
        Adds a new transition for logged in initial users

        :param init_logged_in_users: the observed initial number of logged in users
        :return: None
        """
        if str(init_logged_in_users) in self.init_logged_in_users:
            self.init_logged_in_users[str(init_logged_in_users)] = \
                self.init_logged_in_users[str(init_logged_in_users)] + 1
        else:
            self.init_logged_in_users[str(init_logged_in_users)] = 1

    def add_new_init_processes(self, init_processes: int) -> None:
        """
        Adds a new transition for initial number of processes

        :param init_processes: the observed initial number of processes
        :return: None
        """
        if str(init_processes) in self.init_logged_in_users:
            self.init_processes[str(init_processes)] = \
                self.init_processes[str(init_processes)] + 1
        else:
            self.init_processes[str(init_processes)] = 1

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
                                    num_new_failed_login_attempts: int) -> None:
        """
        Adds a new transition for failed login attempts

        :param attacker_action_id: the attacker action that triggered the transition
        :param logged_in_ips: the attacker state
        :param num_new_failed_login_attempts: the observed new number of faield login attempts
        :return: None
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

        self.init_open_connections = {}
        self.init_users = {}
        self.init_logged_in_users = {}
        self.init_processes = {}

        self.norm_init_open_connections = None
        self.norm_init_users = None
        self.norm_init_logged_in_users = None
        self.norm_init_processes = None

    def __str__(self):
        try:
            return "open_connections_dynamics:{},\n failed_login_attempts_dynamics:{},\n user_dynamics:{},\n " \
                   "logged_in_users_dynamics:{},\n login_events_dynamics:{},\n processes_dynamics:{}\n," \
                   "init_open_connections:{},\n init_users:{},\n init_logged_in_users:{},\n" \
                   "init_processes:{},\n norm_open_connections:{},\n norm_new_processes:{},\n" \
                   "norm_new_login_events:{},\n norm_new_users:{},\n norm_new_login_events:{}".format(
                self.num_new_open_connections, self.num_new_failed_login_attempts, self.num_new_users,
                self.num_new_logged_in_users, self.num_new_login_events, self.num_new_processes,
                self.init_open_connections, self.init_users, self.init_logged_in_users, self.init_processes,
                self.norm_num_new_open_connections.values(), self.norm_num_new_processes.values(),
                self.norm_num_new_login_events.values(),
                self.norm_num_new_users.values(), self.norm_num_new_login_events.values())
        except:
            return "open_connections_dynamics:{},\n failed_login_attempts_dynamics:{},\n user_dynamics:{},\n " \
                   "logged_in_users_dynamics:{},\n login_events_dynamics:{},\n processes_dynamics:{}\n," \
                   "init_open_connections:{},\n init_users:{},\n init_logged_in_users:{},\n" \
                   "init_processes:{},\n norm_open_connections:{},\n norm_new_processes:{},\n" \
                   "norm_new_login_events:{},\n norm_new_users:{},\n norm_new_login_events:{}".format(
                self.num_new_open_connections, self.num_new_failed_login_attempts, self.num_new_users,
                self.num_new_logged_in_users, self.num_new_login_events, self.num_new_processes,
                self.init_open_connections, self.init_users, self.init_logged_in_users, self.init_processes,
                self.norm_num_new_open_connections, self.norm_num_new_processes,
                self.norm_num_new_login_events,
                self.norm_num_new_users, self.norm_num_new_login_events)

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
        d["init_open_connections"] = self.init_open_connections
        d["init_users"] = self.init_users
        d["init_logged_in_users"] = self.init_logged_in_users
        d["init_processes"] = self.init_processes
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
        self.init_open_connections = d["init_open_connections"]
        self.init_users = d["init_users"]
        self.init_logged_in_users = d["init_logged_in_users"]
        self.init_processes = d["init_processes"]




