import json
import os
from scipy import stats
import numpy as np
from gym_pycr_ctf.util.experiments_util import util
from gym_pycr_ctf.dao.action.attacker.attacker_action import AttackerActionId
from gym_pycr_ctf.dao.defender_dynamics.defender_machine_dynamics_model import DefenderMachineDynamicsModel
import gym_pycr_ctf.constants.constants as constants


class DefenderDynamicsModel:
    """
    Represents a dynamics model of the defender for simulating stochastic (b, a) -> b' transitions based on
    maximum likelihood estimations
    """

    def __init__(self):
        self.num_new_alerts = {}
        self.num_new_priority = {}
        self.num_new_severe_alerts = {}
        self.num_new_warning_alerts = {}
        self.machines_dynamics_model = {}

        self.norm_num_new_alerts = {}
        self.norm_num_new_priority = {}
        self.norm_num_new_severe_alerts = {}
        self.norm_num_new_warning_alerts = {}
        self.norm_machines_dynamics_model = {}

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
                for num_warning_str, count in v2.items():
                    samples.append(int(num_warning_str))
                    counts.append(count)
                counts = np.array(counts)
                samples = np.array(samples)
                empirical_probabilities = counts / np.sum(counts)
                dist = stats.rv_discrete(name='num_new_warning_alerts_emp_dist',
                                         values=(samples, empirical_probabilities))
                self.norm_num_new_warning_alerts[(int(attack_id_str), logged_in_ips)] = dist

        for machine_ip, v in self.machines_dynamics_model.items():
            v.normalize()

    def add_new_alert_transition(self, attacker_action_id: AttackerActionId, logged_in_ips : str,
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

    def add_new_priority_transition(self, attacker_action_id: AttackerActionId, logged_in_ips : str,
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

    def add_new_severe_alert_transition(self, attacker_action_id: AttackerActionId, logged_in_ips : str,
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

    def add_new_warning_alert_transition(self, attacker_action_id: AttackerActionId, logged_in_ips : str,
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

    def update_model(self, s, s_prime, attacker_action_id: AttackerActionId, logged_in_ips: str) -> None:
        """
        Updates the dynamics model after observing a (s,a)->s' transition.

        :param s: the previous state
        :param s_prime: the new state
        :param attacker_action_id: the attacker action that triggered the transition
        :param logged_in_ips: the attacker state
        :return: None
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

            num_new_failed_login_attempts = s_prime.defender_obs_state.machines[i].num_failed_login_attempts_recent
            self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip].add_new_failed_login_attempt_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                num_new_failed_login_attempts=num_new_failed_login_attempts)

            num_new_users = s_prime.defender_obs_state.machines[i].num_users_recent
            self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip].add_new_user_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                num_new_users=num_new_users)

            num_new_logged_in_users = s_prime.defender_obs_state.machines[i].num_logged_in_users_recent
            self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip].add_new_logged_in_user_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                num_new_logged_in_users=num_new_logged_in_users)

            num_new_login_events = s_prime.defender_obs_state.machines[i].num_login_events_recent
            self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip].add_new_login_event_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                num_new_login_events=num_new_login_events)

            num_new_processes = s_prime.defender_obs_state.machines[i].num_processes_recent
            self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip].add_new_processes_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                num_new_processes=num_new_processes)

    def update_init_state_distribution(self, init_state) -> None:
        """
        Updates the dynamics model after observing a initial state

        :param init_state: the observed initial state
        :return: None
        """

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

    def reset(self) -> None:
        """
        Resets the model

        :return: None
        """
        self.num_new_alerts = {}
        self.num_new_priority = {}
        self.num_new_severe_alerts = {}
        self.num_new_warning_alerts = {}
        self.machines_dynamics_model = {}

        self.norm_num_new_alerts = {}
        self.norm_num_new_priority = {}
        self.norm_num_new_severe_alerts = {}
        self.norm_num_new_warning_alerts = {}
        self.norm_machines_dynamics_model = {}

    def __str__(self):
        try:
            return "alerts_dynamics:{},\n priority_dynamics:{},\n severe_alerts_dynamics:{},\n " \
                   "warning_alerts_dynamics:{},\n norm_alerts_dynamics:{},\n norm_priority_dynamics:{},\n" \
                   "norm_severe_alerts_dynamics:{},\n norm_warning_alerts_dynamics:{},\n" \
                   "machines_dynamics_model: {}\n".format(
                self.num_new_alerts, self.num_new_priority, self.num_new_severe_alerts, self.num_new_warning_alerts,
                self.norm_num_new_alerts.values(), self.norm_num_new_priority.values(),
                self.norm_num_new_severe_alerts.values(),
                self.norm_num_new_severe_alerts.values(),
                str(self.machines_dynamics_model)
            )
        except:
            return "alerts_dynamics:{},\n priority_dynamics:{},\n severe_alerts_dynamics:{},\n " \
                   "warning_alerts_dynamics:{},\n norm_alerts_dynamics:{},\n norm_priority_dynamics:{},\n" \
                   "norm_severe_alerts_dynamics:{},\n norm_warning_alerts_dynamics:{},\n" \
                   "machines_dynamics_model: {}\n".format(
                self.num_new_alerts, self.num_new_priority, self.num_new_severe_alerts, self.num_new_warning_alerts,
                self.norm_num_new_alerts, self.norm_num_new_priority,
                self.norm_num_new_severe_alerts,
                self.norm_num_new_severe_alerts,
                str(self.machines_dynamics_model)
            )

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
        self.num_new_alerts = d["num_new_alerts"]
        self.num_new_priority = d["num_new_priority"]
        self.num_new_severe_alerts = d["num_new_severe_alerts"]
        self.num_new_warning_alerts = d["num_new_warning_alerts"]
        m_dynamics_model_new = {}
        for k, v in d["machines_dynamics_model"].items():
            m = DefenderMachineDynamicsModel()
            m.from_dict(v)
            m_dynamics_model_new[k]= m
        self.machines_dynamics_model = m_dynamics_model_new

    def save_model(self, env_config) -> None:
        """
        Saves the model to disk as a json file

        :param env_config: the environment config
        :return: None
        """
        save_dir = None
        if env_config.emulation_config.save_dynamics_model_dir is not None:
            save_dir = env_config.emulation_config.save_dynamics_model_dir + "/" \
                       + constants.SYSTEM_IDENTIFICATION.DEFENDER_DYNAMICS_MODEL_FILE
        else:
            save_dir = util.get_script_path() + "/" + \
                       constants.SYSTEM_IDENTIFICATION.DEFENDER_DYNAMICS_MODEL_FILE
        d = self.to_dict()
        with open(save_dir, 'w') as fp:
            json.dump(d, fp)

    def read_model(self, env_config) -> None:
        """
        Loads json model from disk (according to env config) and populates the model

        :param env_config: the environment configuration
        :return: None
        """
        load_dir = None
        if env_config.emulation_config.save_dynamics_model_dir is not None:
            load_dir = env_config.emulation_config.save_dynamics_model_dir + "/" + \
                       constants.SYSTEM_IDENTIFICATION.DEFENDER_DYNAMICS_MODEL_FILE
        else:
            load_dir = util.get_script_path() + "/" + \
                       constants.SYSTEM_IDENTIFICATION.DEFENDER_DYNAMICS_MODEL_FILE
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

