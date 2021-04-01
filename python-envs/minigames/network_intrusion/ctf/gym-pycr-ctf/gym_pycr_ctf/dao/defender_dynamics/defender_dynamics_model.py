from gym_pycr_ctf.dao.action.attacker.attacker_action import AttackerActionId
from gym_pycr_ctf.dao.defender_dynamics.defender_machine_dynamics_model import DefenderMachineDynamicsModel

class DefenderDynamicsModel:

    def __init__(self):
        self.num_new_alerts = {}
        self.num_new_priority = {}
        self.num_new_severe_alerts = {}
        self.num_new_warning_alerts = {}
        self.machines_dynamics_model = {}

    def add_new_alert_transition(self, attacker_action_id: AttackerActionId, logged_in_ips : str,
                                 num_new_alerts: int):
        if attacker_action_id not in self.num_new_alerts:
            self.num_new_alerts[attacker_action_id.value] = {}
            self.num_new_alerts[attacker_action_id.value][logged_in_ips] = {}
            self.num_new_alerts[attacker_action_id.value][logged_in_ips][num_new_alerts] = 1
        else:
            if logged_in_ips in self.num_new_alerts[attacker_action_id.value]:
                if num_new_alerts in self.num_new_alerts[attacker_action_id.value][logged_in_ips]:
                    self.num_new_alerts[attacker_action_id.value][logged_in_ips][num_new_alerts] \
                        = self.num_new_alerts[attacker_action_id.value][logged_in_ips][num_new_alerts] + 1
            else:
                self.num_new_alerts[attacker_action_id.value][logged_in_ips] = {}
                self.num_new_alerts[attacker_action_id.value][logged_in_ips][num_new_alerts] = 1



    def add_new_priority_transition(self, attacker_action_id: AttackerActionId, logged_in_ips : str,
                                    num_new_priority: int):
        if attacker_action_id not in self.num_new_priority:
            self.num_new_priority[attacker_action_id.value] = {}
            self.num_new_priority[attacker_action_id.value][logged_in_ips] = {}
            self.num_new_priority[attacker_action_id.value][logged_in_ips][num_new_priority] = 1
        else:
            if logged_in_ips in self.num_new_priority[attacker_action_id.value]:
                if num_new_priority in self.num_new_priority[attacker_action_id.value][logged_in_ips]:
                    self.num_new_priority[attacker_action_id.value][logged_in_ips][num_new_priority] \
                        = self.num_new_priority[attacker_action_id.value][logged_in_ips][num_new_priority] + 1
            else:
                self.num_new_priority[attacker_action_id.value][logged_in_ips] = {}
                self.num_new_priority[attacker_action_id.value][logged_in_ips][num_new_priority] = 1


    def add_new_severe_alert_transition(self, attacker_action_id: AttackerActionId, logged_in_ips : str,
                                        num_new_severe_alerts: int):
        if attacker_action_id not in self.num_new_severe_alerts:
            self.num_new_severe_alerts[attacker_action_id.value] = {}
            self.num_new_severe_alerts[attacker_action_id.value][logged_in_ips] = {}
            self.num_new_severe_alerts[attacker_action_id.value][logged_in_ips][num_new_severe_alerts] = 1
        else:
            if logged_in_ips in self.num_new_severe_alerts[attacker_action_id.value]:
                if num_new_severe_alerts in self.num_new_severe_alerts[attacker_action_id.value][logged_in_ips]:
                    self.num_new_severe_alerts[attacker_action_id.value][logged_in_ips][num_new_severe_alerts] \
                        = self.num_new_severe_alerts[attacker_action_id.value][logged_in_ips][num_new_severe_alerts] + 1
            else:
                self.num_new_severe_alerts[attacker_action_id.value][logged_in_ips] = {}
                self.num_new_severe_alerts[attacker_action_id.value][logged_in_ips][num_new_severe_alerts] = 1



    def add_new_warning_alert_transition(self, attacker_action_id: AttackerActionId, logged_in_ips : str,
                                         num_new_warning_alerts: int):
        if attacker_action_id not in self.num_new_warning_alerts:
            self.num_new_warning_alerts[attacker_action_id.value] = {}
            self.num_new_warning_alerts[attacker_action_id.value][logged_in_ips] = {}
            self.num_new_warning_alerts[attacker_action_id.value][logged_in_ips][num_new_warning_alerts] = 1
        else:
            if logged_in_ips in self.num_new_warning_alerts[attacker_action_id.value]:
                if num_new_warning_alerts in self.num_new_warning_alerts[attacker_action_id.value][logged_in_ips]:
                    self.num_new_warning_alerts[attacker_action_id.value][logged_in_ips][num_new_warning_alerts] \
                        = self.num_new_warning_alerts[attacker_action_id.value][logged_in_ips][num_new_warning_alerts] + 1
            else:
                self.num_new_warning_alerts[attacker_action_id.value][logged_in_ips] = {}
                self.num_new_warning_alerts[attacker_action_id.value][logged_in_ips][num_new_warning_alerts] = 1



    def update_model(self, obs, obs_prime, attacker_action_id: AttackerActionId, logged_in_ips: str):
        num_new_alerts = obs_prime[1].num_alerts_total - obs[1].num_alerts_total
        self.add_new_alert_transition(attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                      num_new_alerts=num_new_alerts)
        num_new_priority = obs_prime[1].sum_priority_alerts_total - obs[1].sum_priority_alerts_total
        self.add_new_priority_transition(attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                         num_new_priority=num_new_priority)
        num_new_severe_alerts = obs_prime[1].num_severe_alerts_total - obs[1].num_severe_alerts_total
        self.add_new_severe_alert_transition(attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                             num_new_severe_alerts=num_new_severe_alerts)
        num_new_warning_alerts = obs_prime[1].num_warning_alerts_total - obs[1].num_warning_alerts_total
        self.add_new_warning_alert_transition(attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                                             num_new_warning_alerts=num_new_warning_alerts)

        for i in range(len(obs_prime[1].machines)):
            if obs_prime[1].machines[i].ip not in self.machines_dynamics_model:
                self.machines_dynamics_model[obs_prime[1].machines[i].ip] = DefenderMachineDynamicsModel()

            num_new_open_connections = obs_prime[1].machines[i].num_open_connections - \
                                       obs[1].machines[i].num_open_connections
            self.machines_dynamics_model[obs_prime[1].machines[i].ip].add_new_open_connection_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                num_new_open_connections=num_new_open_connections)

            num_new_failed_login_attempts = obs_prime[1].machines[i].num_failed_login_attempts - \
                                       obs[1].machines[i].num_failed_login_attempts
            self.machines_dynamics_model[obs_prime[1].machines[i].ip].add_new_failed_login_attempt_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                num_new_failed_login_attempts=num_new_failed_login_attempts)

            num_new_users = obs_prime[1].machines[i].num_users - \
                                       obs[1].machines[i].num_users
            self.machines_dynamics_model[obs_prime[1].machines[i].ip].add_new_user_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                num_new_users=num_new_users)

            num_new_logged_in_users = obs_prime[1].machines[i].num_logged_in_users - \
                            obs[1].machines[i].num_logged_in_users
            self.machines_dynamics_model[obs_prime[1].machines[i].ip].add_new_logged_in_user_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                num_new_logged_in_users=num_new_logged_in_users)

            num_new_login_events = obs_prime[1].machines[i].num_login_events - \
                                       obs[1].machines[i].num_login_events
            self.machines_dynamics_model[obs_prime[1].machines[i].ip].add_new_login_event_transition(
                attacker_action_id=attacker_action_id, logged_in_ips=logged_in_ips,
                num_new_login_events=num_new_login_events)

            num_new_processes = obs_prime[1].machines[i].num_processes - \
                                   obs[1].machines[i].num_processes
            self.machines_dynamics_model[obs_prime[1].machines[i].ip].add_new_login_event_transition(
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
