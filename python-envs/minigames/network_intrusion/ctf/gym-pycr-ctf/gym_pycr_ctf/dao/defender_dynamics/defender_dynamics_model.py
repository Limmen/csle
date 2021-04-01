import json
import os
from scipy import stats
import numpy as np
from gym_pycr_ctf.util.experiments_util import util
from gym_pycr_ctf.dao.action.attacker.attacker_action import AttackerActionId
from gym_pycr_ctf.dao.defender_dynamics.defender_machine_dynamics_model import DefenderMachineDynamicsModel

class DefenderDynamicsModel:

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

    def normalize(self):

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
                                 num_new_alerts: int):
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
                                    num_new_priority: int):
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
                                        num_new_severe_alerts: int):
        if str(attacker_action_id.value) not in self.num_new_severe_alerts:
            self.num_new_severe_alerts[str(attacker_action_id.value)] = {}
            self.num_new_severe_alerts[str(attacker_action_id.value)][logged_in_ips] = {}
            self.num_new_severe_alerts[str(attacker_action_id.value)][logged_in_ips][str(num_new_severe_alerts)] = 1
        else:
            if logged_in_ips in self.num_new_severe_alerts[str(attacker_action_id.value)]:
                if str(num_new_severe_alerts) in self.num_new_severe_alerts[str(attacker_action_id.value)][logged_in_ips]:
                    self.num_new_severe_alerts[str(attacker_action_id.value)][logged_in_ips][str(num_new_severe_alerts)] \
                        = self.num_new_severe_alerts[str(attacker_action_id.value)][logged_in_ips][str(num_new_severe_alerts)] + 1
                else:
                    self.num_new_severe_alerts[str(attacker_action_id.value)][logged_in_ips][str(num_new_severe_alerts)] = 1
            else:
                self.num_new_severe_alerts[str(attacker_action_id.value)][logged_in_ips] = {}
                self.num_new_severe_alerts[str(attacker_action_id.value)][logged_in_ips][str(num_new_severe_alerts)] = 1



    def add_new_warning_alert_transition(self, attacker_action_id: AttackerActionId, logged_in_ips : str,
                                         num_new_warning_alerts: int):
        if str(attacker_action_id.value) not in self.num_new_warning_alerts:
            self.num_new_warning_alerts[str(attacker_action_id.value)] = {}
            self.num_new_warning_alerts[str(attacker_action_id.value)][logged_in_ips] = {}
            self.num_new_warning_alerts[str(attacker_action_id.value)][logged_in_ips][str(num_new_warning_alerts)] = 1
        else:
            if logged_in_ips in self.num_new_warning_alerts[str(attacker_action_id.value)]:
                if str(num_new_warning_alerts) in self.num_new_warning_alerts[str(attacker_action_id.value)][logged_in_ips]:
                    self.num_new_warning_alerts[str(attacker_action_id.value)][logged_in_ips][str(num_new_warning_alerts)] \
                        = self.num_new_warning_alerts[str(attacker_action_id.value)][logged_in_ips][str(num_new_warning_alerts)] + 1
                else:
                    self.num_new_warning_alerts[str(attacker_action_id.value)][logged_in_ips][str(num_new_warning_alerts)] = 1
            else:
                self.num_new_warning_alerts[str(attacker_action_id.value)][logged_in_ips] = {}
                self.num_new_warning_alerts[str(attacker_action_id.value)][logged_in_ips][str(num_new_warning_alerts)] = 1



    def update_model(self, s, s_prime, attacker_action_id: AttackerActionId, logged_in_ips: str):
        num_new_alerts = s_prime.defender_obs_state.num_alerts_total
        self.add_new_alert_transition(attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                      num_new_alerts=num_new_alerts)
        num_new_priority = s_prime.defender_obs_state.sum_priority_alerts_total
        self.add_new_priority_transition(attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                         num_new_priority=num_new_priority)
        num_new_severe_alerts = s_prime.defender_obs_state.num_severe_alerts_total
        self.add_new_severe_alert_transition(attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                             num_new_severe_alerts=num_new_severe_alerts)
        num_new_warning_alerts = s_prime.defender_obs_state.num_warning_alerts_total
        self.add_new_warning_alert_transition(attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                             num_new_warning_alerts=num_new_warning_alerts)


        for i in range(len(s_prime.defender_obs_state.machines)):
            if s_prime.defender_obs_state.machines[i].ip not in self.machines_dynamics_model or \
                    self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip] is None:
                self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip] = DefenderMachineDynamicsModel()

            num_new_open_connections = s_prime.defender_obs_state.machines[i].num_open_connections \
                                       - s.defender_obs_state.machines[i].num_open_connections
            self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip].add_new_open_connection_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                num_new_open_connections=num_new_open_connections)

            num_new_failed_login_attempts = s_prime.defender_obs_state.machines[i].num_failed_login_attempts
            self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip].add_new_failed_login_attempt_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                num_new_failed_login_attempts=num_new_failed_login_attempts)

            num_new_users = s_prime.defender_obs_state.machines[i].num_users \
                            - s.defender_obs_state.machines[i].num_users
            self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip].add_new_user_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                num_new_users=num_new_users)

            num_new_logged_in_users = s_prime.defender_obs_state.machines[i].num_logged_in_users - \
                                      s.defender_obs_state.machines[i].num_logged_in_users
            self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip].add_new_logged_in_user_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                num_new_logged_in_users=num_new_logged_in_users)

            num_new_login_events = s_prime.defender_obs_state.machines[i].num_login_events
            self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip].add_new_login_event_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                num_new_login_events=num_new_login_events)

            num_new_processes = s_prime.defender_obs_state.machines[i].num_processes \
                                - s.defender_obs_state.machines[i].num_processes
            self.machines_dynamics_model[s_prime.defender_obs_state.machines[i].ip].add_new_processes_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                num_new_processes=num_new_processes)



    def reset(self):
        self.num_new_alerts = {}
        self.num_new_priority = {}
        self.num_new_severe_alerts = {}
        self.num_new_warning_alerts = {}
        self.machines_dynamics_model = {}



    def __str__(self):
        return "alerts_dynamics:{},\n priority_dynamics:{},\n severe_alerts_dynamics:{},\n " \
               "warning_alerts_dynamics:{},\n " \
               "machines_dynamics_model: {}\n".format(
            self.num_new_alerts, self.num_new_priority, self.num_new_severe_alerts, self.num_new_warning_alerts,
            self.machines_dynamics_model
        )

    def to_dict(self):
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

    def from_dict(self, d):
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


    def save_model(self, env_config):
        save_dir = None
        if env_config.emulation_config.save_dynamics_model_dir is not None:
            save_dir = env_config.emulation_config.save_dynamics_model_dir + "/defender_dynamics_model.json"
        else:
            save_dir = util.get_script_path() + "/defender_dynamics_model.json"
        d = self.to_dict()
        with open(save_dir, 'w') as fp:
            json.dump(d, fp)


    def read_model(self, env_config):
        load_dir = None
        if env_config.emulation_config.save_dynamics_model_dir is not None:
            load_dir = env_config.emulation_config.save_dynamics_model_dir + "/defender_dynamics_model.json"
        else:
            load_dir = util.get_script_path() + "/defender_dynamics_model.json"
        if os.path.exists(load_dir):
            with open(load_dir, 'r') as fp:
                d = json.load(fp)
                self.from_dict(d)

