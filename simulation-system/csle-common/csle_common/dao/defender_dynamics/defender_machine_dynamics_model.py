from typing import Dict, Any
from scipy import stats
import numpy as np
from enum import Enum


class DefenderMachineDynamicsModel:
    """
    Represents a dynamics model of specific machines in the emulation of
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

        self.init_num_new_pids = {}
        self.init_cpu_percentage_change = {}
        self.init_new_mem_current = {}
        self.init_new_mem_total = {}
        self.init_new_mem_percent = {}
        self.init_new_blk_read = {}
        self.init_new_blk_write = {}
        self.init_new_net_rx = {}
        self.init_new_net_tx = {}

        self.num_new_pids = {}
        self.cpu_percentage_change = {}
        self.new_mem_current = {}
        self.new_mem_total = {}
        self.new_mem_percent = {}
        self.new_blk_read = {}
        self.new_blk_write = {}
        self.new_net_rx = {}
        self.new_net_tx = {}

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

                # Normalize num_new_pids
                for attack_id_str, v1 in self.num_new_pids.items():
                    for logged_in_ips, v2 in v1.items():
                        samples = []
                        counts = []
                        for num_login_attempts_str, count in v2.items():
                            samples.append(int(num_login_attempts_str))
                            counts.append(count)
                        counts = np.array(counts)
                        samples = np.array(samples)
                        empirical_probabilities = counts / np.sum(counts)
                        dist = stats.rv_discrete(name='num_new_pids_emp_dist',
                                                 values=(samples, empirical_probabilities))
                        self.norm_num_new_pids[(int(attack_id_str), logged_in_ips)] = dist

                # Normalize cpu_percentage_change
                for attack_id_str, v1 in self.cpu_percentage_change.items():
                    for logged_in_ips, v2 in v1.items():
                        samples = []
                        counts = []
                        for num_login_attempts_str, count in v2.items():
                            samples.append(int(num_login_attempts_str))
                            counts.append(count)
                        counts = np.array(counts)
                        samples = np.array(samples)
                        empirical_probabilities = counts / np.sum(counts)
                        dist = stats.rv_discrete(name='cpu_percentage_change_emp_dist',
                                                 values=(samples, empirical_probabilities))
                        self.norm_cpu_percentage_change[(int(attack_id_str), logged_in_ips)] = dist

                # Normalize new_mem_current
                for attack_id_str, v1 in self.new_mem_current.items():
                    for logged_in_ips, v2 in v1.items():
                        samples = []
                        counts = []
                        for num_login_attempts_str, count in v2.items():
                            samples.append(int(num_login_attempts_str))
                            counts.append(count)
                        counts = np.array(counts)
                        samples = np.array(samples)
                        empirical_probabilities = counts / np.sum(counts)
                        dist = stats.rv_discrete(name='new_mem_current_emp_dist',
                                                 values=(samples, empirical_probabilities))
                        self.norm_new_mem_current[(int(attack_id_str), logged_in_ips)] = dist

                # Normalize new_mem_total
                for attack_id_str, v1 in self.new_mem_total.items():
                    for logged_in_ips, v2 in v1.items():
                        samples = []
                        counts = []
                        for num_login_attempts_str, count in v2.items():
                            samples.append(int(num_login_attempts_str))
                            counts.append(count)
                        counts = np.array(counts)
                        samples = np.array(samples)
                        empirical_probabilities = counts / np.sum(counts)
                        dist = stats.rv_discrete(name='new_mem_total_emp_dist',
                                                 values=(samples, empirical_probabilities))
                        self.norm_new_mem_total[(int(attack_id_str), logged_in_ips)] = dist

                # Normalize new_mem_percent
                for attack_id_str, v1 in self.new_mem_percent.items():
                    for logged_in_ips, v2 in v1.items():
                        samples = []
                        counts = []
                        for num_login_attempts_str, count in v2.items():
                            samples.append(int(num_login_attempts_str))
                            counts.append(count)
                        counts = np.array(counts)
                        samples = np.array(samples)
                        empirical_probabilities = counts / np.sum(counts)
                        dist = stats.rv_discrete(name='new_mem_percent_emp_dist',
                                                 values=(samples, empirical_probabilities))
                        self.norm_new_mem_percent[(int(attack_id_str), logged_in_ips)] = dist

                # Normalize new_blk_read
                for attack_id_str, v1 in self.new_blk_read.items():
                    for logged_in_ips, v2 in v1.items():
                        samples = []
                        counts = []
                        for num_login_attempts_str, count in v2.items():
                            samples.append(int(num_login_attempts_str))
                            counts.append(count)
                        counts = np.array(counts)
                        samples = np.array(samples)
                        empirical_probabilities = counts / np.sum(counts)
                        dist = stats.rv_discrete(name='new_blk_read_emp_dist',
                                                 values=(samples, empirical_probabilities))
                        self.norm_new_blk_read[(int(attack_id_str), logged_in_ips)] = dist

                # Normalize new_blk_write
                for attack_id_str, v1 in self.new_blk_write.items():
                    for logged_in_ips, v2 in v1.items():
                        samples = []
                        counts = []
                        for num_login_attempts_str, count in v2.items():
                            samples.append(int(num_login_attempts_str))
                            counts.append(count)
                        counts = np.array(counts)
                        samples = np.array(samples)
                        empirical_probabilities = counts / np.sum(counts)
                        dist = stats.rv_discrete(name='new_blk_write_emp_dist',
                                                 values=(samples, empirical_probabilities))
                        self.norm_new_blk_write[(int(attack_id_str), logged_in_ips)] = dist

                # Normalize new_net_rx
                for attack_id_str, v1 in self.new_net_rx.items():
                    for logged_in_ips, v2 in v1.items():
                        samples = []
                        counts = []
                        for num_login_attempts_str, count in v2.items():
                            samples.append(int(num_login_attempts_str))
                            counts.append(count)
                        counts = np.array(counts)
                        samples = np.array(samples)
                        empirical_probabilities = counts / np.sum(counts)
                        dist = stats.rv_discrete(name='new_net_rx_emp_dist',
                                                 values=(samples, empirical_probabilities))
                        self.norm_new_net_rx[(int(attack_id_str), logged_in_ips)] = dist

                # Normalize new_net_tx
                for attack_id_str, v1 in self.new_net_tx.items():
                    for logged_in_ips, v2 in v1.items():
                        samples = []
                        counts = []
                        for num_login_attempts_str, count in v2.items():
                            samples.append(int(num_login_attempts_str))
                            counts.append(count)
                        counts = np.array(counts)
                        samples = np.array(samples)
                        empirical_probabilities = counts / np.sum(counts)
                        dist = stats.rv_discrete(name='new_net_tx_emp_dist',
                                                 values=(samples, empirical_probabilities))
                        self.norm_new_net_tx[(int(attack_id_str), logged_in_ips)] = dist

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

        # Normalize num_init_processes
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

        # Normalize init_num_new_pids
        samples = []
        counts = []
        for init_connections_str, count in self.init_num_new_pids.items():
            samples.append(int(init_connections_str))
            counts.append(count)
        counts = np.array(counts)
        samples = np.array(samples)
        empirical_probabilities = counts / np.sum(counts)
        dist = stats.rv_discrete(name='init_num_new_pids_users_emp_dist',
                                 values=(samples, empirical_probabilities))
        self.norm_init_num_new_pids = dist

        # Normalize init_cpu_percentage_change
        samples = []
        counts = []
        for init_connections_str, count in self.init_cpu_percentage_change.items():
            samples.append(int(init_connections_str))
            counts.append(count)
        counts = np.array(counts)
        samples = np.array(samples)
        empirical_probabilities = counts / np.sum(counts)
        dist = stats.rv_discrete(name='init_cpu_percentage_change_users_emp_dist',
                                 values=(samples, empirical_probabilities))
        self.norm_init_cpu_percentage_change = dist

        # Normalize init_new_mem_current
        samples = []
        counts = []
        for init_connections_str, count in self.init_new_mem_current.items():
            samples.append(int(init_connections_str))
            counts.append(count)
        counts = np.array(counts)
        samples = np.array(samples)
        empirical_probabilities = counts / np.sum(counts)
        dist = stats.rv_discrete(name='init_new_mem_current_users_emp_dist',
                                 values=(samples, empirical_probabilities))
        self.norm_init_new_mem_current = dist

        # Normalize init_new_mem_total
        samples = []
        counts = []
        for init_connections_str, count in self.init_new_mem_total.items():
            samples.append(int(init_connections_str))
            counts.append(count)
        counts = np.array(counts)
        samples = np.array(samples)
        empirical_probabilities = counts / np.sum(counts)
        dist = stats.rv_discrete(name='init_new_mem_total_users_emp_dist',
                                 values=(samples, empirical_probabilities))
        self.norm_init_new_mem_total = dist

        # Normalize init_new_mem_percent
        samples = []
        counts = []
        for init_connections_str, count in self.init_new_mem_percent.items():
            samples.append(int(init_connections_str))
            counts.append(count)
        counts = np.array(counts)
        samples = np.array(samples)
        empirical_probabilities = counts / np.sum(counts)
        dist = stats.rv_discrete(name='init_new_mem_percent_users_emp_dist',
                                 values=(samples, empirical_probabilities))
        self.norm_init_new_mem_percent = dist

        # Normalize init_new_blk_read
        samples = []
        counts = []
        for init_connections_str, count in self.init_new_blk_read.items():
            samples.append(int(init_connections_str))
            counts.append(count)
        counts = np.array(counts)
        samples = np.array(samples)
        empirical_probabilities = counts / np.sum(counts)
        dist = stats.rv_discrete(name='init_new_blk_read_users_emp_dist',
                                 values=(samples, empirical_probabilities))
        self.norm_init_new_blk_read = dist

        # Normalize init_new_blk_write
        samples = []
        counts = []
        for init_connections_str, count in self.init_new_blk_write.items():
            samples.append(int(init_connections_str))
            counts.append(count)
        counts = np.array(counts)
        samples = np.array(samples)
        empirical_probabilities = counts / np.sum(counts)
        dist = stats.rv_discrete(name='init_new_blk_write_users_emp_dist',
                                 values=(samples, empirical_probabilities))
        self.norm_init_new_blk_write = dist

        # Normalize init_new_net_rx
        samples = []
        counts = []
        for init_connections_str, count in self.init_new_net_rx.items():
            samples.append(int(init_connections_str))
            counts.append(count)
        counts = np.array(counts)
        samples = np.array(samples)
        empirical_probabilities = counts / np.sum(counts)
        dist = stats.rv_discrete(name='init_new_net_rx_users_emp_dist',
                                 values=(samples, empirical_probabilities))
        self.norm_init_new_net_rx = dist

        # Normalize init_new_net_tx
        samples = []
        counts = []
        for init_connections_str, count in self.init_new_net_tx.items():
            samples.append(int(init_connections_str))
            counts.append(count)
        counts = np.array(counts)
        samples = np.array(samples)
        empirical_probabilities = counts / np.sum(counts)
        dist = stats.rv_discrete(name='init_new_net_tx_users_emp_dist',
                                 values=(samples, empirical_probabilities))
        self.norm_init_new_net_tx = dist


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

    def add_new_open_connection_transition(self, attacker_action_id: Enum, logged_in_ips : str,
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

    def add_new_failed_login_attempt_transition(self, attacker_action_id: Enum, logged_in_ips : str,
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

    def add_new_user_transition(self, attacker_action_id: Enum, logged_in_ips : str,
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

    def add_new_logged_in_user_transition(self, attacker_action_id: Enum, logged_in_ips : str,
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

    def add_new_login_event_transition(self, attacker_action_id: Enum, logged_in_ips : str,
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

    def add_new_processes_transition(self, attacker_action_id: Enum, logged_in_ips : str,
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
                        = self.cpu_percentage_change[str(attacker_action_id.value)][logged_in_ips][
                              str(cpu_percent_change)] + 1
                else:
                    self.cpu_percentage_change[str(attacker_action_id.value)][logged_in_ips][
                        str(cpu_percent_change)] = 1
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

        self.num_new_pids = {}
        self.cpu_percentage_change = {}
        self.new_mem_current = {}
        self.new_mem_total = {}
        self.new_mem_percent = {}
        self.new_blk_read = {}
        self.new_blk_write = {}
        self.new_net_rx = {}
        self.new_net_tx = {}

        self.norm_num_new_pids = {}
        self.norm_cpu_percentage_change = {}
        self.norm_new_mem_current = {}
        self.norm_new_mem_total = {}
        self.norm_new_mem_percent = {}
        self.norm_new_blk_read = {}
        self.norm_new_blk_write = {}
        self.norm_new_net_rx = {}
        self.norm_new_net_tx = {}

        self.init_num_new_pids = {}
        self.init_cpu_percentage_change = {}
        self.init_new_mem_current = {}
        self.init_new_mem_total = {}
        self.init_new_mem_percent = {}
        self.init_new_blk_read = {}
        self.init_new_blk_write = {}
        self.init_new_net_rx = {}
        self.init_new_net_tx = {}

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
            return f"open_connections_dynamics:{self.num_new_open_connections}," \
                   f"\n failed_login_attempts_dynamics:{self.num_new_failed_login_attempts}," \
                   f"\n user_dynamics:{self.num_new_users},\n " \
                   f"logged_in_users_dynamics:{self.num_new_logged_in_users},\n " \
                   f"login_events_dynamics:{self.num_new_login_events}," \
                   f"\n processes_dynamics:{self.num_new_processes}\n," \
                   f"init_open_connections:{self.init_open_connections},\n init_users:{self.init_users}," \
                   f"\n init_logged_in_users:{self.init_logged_in_users},\n" \
                   f"init_processes:{self.init_processes},\n " \
                   f"norm_open_connections:{self.norm_num_new_open_connections.values()},\n " \
                   f"norm_new_processes:{self.norm_num_new_processes.values()},\n" \
                   f"norm_new_login_events:{self.norm_num_new_login_events.values()}," \
                   f"\n norm_new_users:{self.norm_num_new_users.values()}," \
                   f"\n norm_new_login_events:{self.norm_num_new_login_events.values()}" \
                   f"\n num_new_pids: {self.num_new_pids}, " \
                   f"\n cpu_percentage_change: {self.cpu_percentage_change}," \
                   f"\n new_mem_current: {self.new_mem_current}, " \
                   f"\n new_mem_total: {self.new_mem_total}, " \
                   f"\n new_mem_percent: {self.new_mem_percent}, " \
                   f"\n new_blk_read: {self.new_blk_read}, " \
                   f"\n new_blk_write: {self.new_blk_write}, " \
                   f"\n new_net_rx: {self.new_net_rx}, " \
                   f"\n new_net_tx: {self.new_net_tx}", \
                   f"\n norm_num_new_pids: {self.norm_num_new_pids.values()}, " \
                   f"\n norm_cpu_percentage_change: {self.norm_cpu_percentage_change.values()}," \
                   f"\n norm_new_mem_current: {self.norm_new_mem_current.values()}, " \
                   f"\n norm_new_mem_total: {self.norm_new_mem_total.values()}, " \
                   f"\n norm_new_mem_percent: {self.norm_new_mem_percent.values()}, " \
                   f"\n norm_new_blk_read: {self.norm_new_blk_read.values()}, " \
                   f"\n norm_new_blk_write: {self.norm_new_blk_write.values()}, " \
                   f"\n norm_new_net_rx: {self.norm_new_net_rx.values()}, " \
                   f"\n norm_new_net_tx: {self.norm_new_net_tx.values()}" \
                   f"\n init_num_new_pids: {self.init_num_new_pids}, \n" \
                   f" init_cpu_percentage_change: {self.init_cpu_percentage_change}, \n " \
                   f"init_new_mem_current: {self.init_new_mem_current}, \n, " \
                   f"init_new_mem_total: {self.init_new_mem_total}, \n " \
                   f"init_new_mem_percent: {self.init_new_mem_percent}, \n " \
                   f"init_new_blk_read: {self.init_new_blk_read},\n init_new_blk_write: {self.init_new_blk_write}, \n" \
                   f"init_new_net_rx: {self.init_new_net_rx}, \n init_new_net_tx: {self.init_new_net_tx},\n" \
                   f"norm_init_pid: {self.norm_init_num_new_pids.values()}, \n " \
                   f" norm_init_cpu_percentage_change: {self.norm_init_cpu_percentage_change.values()}, \n " \
                   f"norm_init_new_mem_current: {self.norm_init_new_mem_current.values()}, \n, " \
                   f"norm_init_new_mem_total: {self.norm_init_new_mem_total.values()}, \n " \
                   f"norm_init_new_mem_percent: {self.norm_init_new_mem_percent.values()}, \n " \
                   f"norm_init_new_blk_read: {self.norm_init_new_blk_read.values()}," \
                   f"\n norm_init_new_blk_write: {self.norm_init_new_blk_write.values()}, \n" \
                   f"norm_init_new_net_rx: {self.norm_init_new_net_rx.values()}, " \
                   f"\n norm_init_new_net_tx: {self.norm_init_new_net_tx.values()}"
        except:
            return f"open_connections_dynamics:{self.num_new_open_connections}," \
                   f"\n failed_login_attempts_dynamics:{self.num_new_failed_login_attempts}," \
                   f"\n user_dynamics:{self.num_new_users}, " \
                   f"\n logged_in_users_dynamics:{self.num_new_logged_in_users},\n " \
                   f"login_events_dynamics:{self.num_new_login_events},\n " \
                   f"processes_dynamics:{self.num_new_processes}\n," \
                   f"init_open_connections:{self.init_open_connections},\n " \
                   f"init_users:{self.init_users},\n init_logged_in_users:{self.init_logged_in_users},\n" \
                   f"init_processes:{self.init_processes}," \
                   f"\n norm_open_connections:{self.norm_num_new_open_connections}," \
                   f"\n norm_new_processes:{self.norm_num_new_processes},\n" \
                   f"norm_new_login_events:{self.norm_num_new_login_events}," \
                   f"\n norm_new_users:{self.norm_num_new_users}," \
                   f"\n norm_new_login_events:{self.norm_num_new_login_events}," \
                   f"\n num_new_pids: {self.num_new_pids}, \n cpu_percentage_change: {self.cpu_percentage_change}," \
                   f"\n new_mem_current: {self.new_mem_current}, \n new_mem_total: {self.new_mem_total}, " \
                   f"\n new_mem_percent: {self.new_mem_percent}, \n new_blk_read: {self.new_blk_read}, " \
                   f"\n new_blk_write: {self.new_blk_write}, \n new_net_rx: {self.new_net_rx}, " \
                   f"\n new_net_tx: {self.new_net_tx}, " \
                   f"\n norm_num_new_pids: {self.norm_num_new_pids}, " \
                   f"\n norm_cpu_percentage_change: {self.norm_cpu_percentage_change}," \
                   f"\n norm_new_mem_current: {self.norm_new_mem_current}, " \
                   f"\n norm_new_mem_total: {self.norm_new_mem_total}, " \
                   f"\n norm_new_mem_percent: {self.norm_new_mem_percent}, " \
                   f"\n norm_new_blk_read: {self.norm_new_blk_read}, " \
                   f"\n norm_new_blk_write: {self.norm_new_blk_write}, " \
                   f"\n norm_new_net_rx: {self.norm_new_net_rx}, " \
                   f"\n norm_new_net_tx: {self.norm_new_net_tx}" \
                   f"\n init_num_new_pids: {self.init_num_new_pids}, \n" \
                   f" init_cpu_percentage_change: {self.init_cpu_percentage_change}, \n " \
                   f"init_new_mem_current: {self.init_new_mem_current}, \n, " \
                   f"init_new_mem_total: {self.init_new_mem_total}, \n " \
                   f"init_new_mem_percent: {self.init_new_mem_percent}, \n " \
                   f"init_new_blk_read: {self.init_new_blk_read},\n init_new_blk_write: {self.init_new_blk_write}, \n" \
                   f"init_new_net_rx: {self.init_new_net_rx}, \n init_new_net_tx: {self.init_new_net_tx},\n" \
                   f" norm_init_pid: {self.norm_init_num_new_pids}, \n " \
                   f" norm_init_cpu_percentage_change: {self.norm_init_cpu_percentage_change}, \n " \
                   f"norm_init_new_mem_current: {self.norm_init_new_mem_current}, \n, " \
                   f"norm_init_new_mem_total: {self.norm_init_new_mem_total}, \n " \
                   f"norm_init_new_mem_percent: {self.norm_init_new_mem_percent}, \n " \
                   f"norm_init_new_blk_read: {self.norm_init_new_blk_read}," \
                   f"\n norm_init_new_blk_write: {self.norm_init_new_blk_write}, \n" \
                   f"norm_init_new_net_rx: {self.norm_init_new_net_rx}, " \
                   f"\n norm_init_new_net_tx: {self.norm_init_new_net_tx}"

    def to_dict(self) -> Dict[str, Any]:
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
        d["num_new_pids"] = self.num_new_pids
        d["new_mem_current"] = self.new_mem_current
        d["new_mem_total"] = self.new_mem_total
        d["new_mem_percent"] = self.new_mem_percent
        d["new_blk_read"] = self.new_blk_read
        d["new_blk_write"] = self.new_blk_write
        d["new_net_rx"] = self.new_net_rx
        d["new_net_tx"] = self.new_net_tx
        d["init_num_new_pids"] = self.init_num_new_pids
        d["init_new_mem_current"] = self.init_new_mem_current
        d["init_new_mem_total"] = self.init_new_mem_total
        d["init_new_mem_percent"] = self.init_new_mem_percent
        d["init_new_blk_read"] = self.init_new_blk_read
        d["init_new_blk_write"] = self.init_new_blk_write
        d["init_new_net_rx"] = self.init_new_net_rx
        d["init_new_net_tx"] = self.init_new_net_tx
        return d


    def from_dict(self, d: Dict[str, Any]) -> None:
        """
        Populates the model with data from a dict

        :param d: the dict to use to populate the model
        :return: None
        """
        self.num_new_open_connections = d["num_new_open_connections"].copy()
        self.num_new_failed_login_attempts = d["num_new_failed_login_attempts"].copy()
        self.num_new_users = d["num_new_users"].copy()
        self.num_new_logged_in_users = d["num_new_logged_in_users"].copy()
        self.num_new_login_events = d["num_new_login_events"].copy()
        self.num_new_processes = d["num_new_processes"].copy()
        self.init_open_connections = d["init_open_connections"].copy()
        self.init_users = d["init_users"].copy()
        self.init_logged_in_users = d["init_logged_in_users"].copy()
        self.init_processes = d["init_processes"].copy()
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

