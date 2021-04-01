from gym_pycr_ctf.dao.action.attacker.attacker_action import AttackerActionId

class DefenderMachineDynamicsModel:

    def __init__(self):
        self.num_new_open_connections = {}
        self.num_new_failed_login_attempts = {}
        self.num_new_users = {}
        self.num_new_logged_in_users = {}
        self.num_new_login_events = {}
        self.num_new_processes = {}


    def add_new_open_connection_transition(self, attacker_action_id: AttackerActionId, logged_in_ips : str,
                                 num_new_open_connections: int):
        if attacker_action_id not in self.num_new_open_connections:
            self.num_new_open_connections[attacker_action_id.value] = {}
            self.num_new_open_connections[attacker_action_id.value][logged_in_ips] = {}
            self.num_new_open_connections[attacker_action_id.value][logged_in_ips][num_new_open_connections] = 1
        else:
            if logged_in_ips in self.num_new_open_connections[attacker_action_id.value]:
                if num_new_open_connections in self.num_new_open_connections[attacker_action_id.value][logged_in_ips]:
                    self.num_new_open_connections[attacker_action_id.value][logged_in_ips][num_new_open_connections] \
                        = self.num_new_open_connections[attacker_action_id.value][logged_in_ips][num_new_open_connections] + 1
            else:
                self.num_new_open_connections[attacker_action_id.value][logged_in_ips] = {}
                self.num_new_open_connections[attacker_action_id.value][logged_in_ips][num_new_open_connections] = 1



    def add_new_failed_login_attempt_transition(self, attacker_action_id: AttackerActionId, logged_in_ips : str,
                                    num_new_failed_login_attempts: int):
        if attacker_action_id not in self.num_new_failed_login_attempts:
            self.num_new_failed_login_attempts[attacker_action_id.value] = {}
            self.num_new_failed_login_attempts[attacker_action_id.value][logged_in_ips] = {}
            self.num_new_failed_login_attempts[attacker_action_id.value][logged_in_ips][num_new_failed_login_attempts] = 1
        else:
            if logged_in_ips in self.num_new_failed_login_attempts[attacker_action_id.value]:
                if num_new_failed_login_attempts in self.num_new_failed_login_attempts[attacker_action_id.value][logged_in_ips]:
                    self.num_new_failed_login_attempts[attacker_action_id.value][logged_in_ips][num_new_failed_login_attempts] \
                        = self.num_new_failed_login_attempts[attacker_action_id.value][logged_in_ips][num_new_failed_login_attempts] + 1
            else:
                self.num_new_failed_login_attempts[attacker_action_id.value][logged_in_ips] = {}
                self.num_new_failed_login_attempts[attacker_action_id.value][logged_in_ips][num_new_failed_login_attempts] = 1

    def add_new_user_transition(self, attacker_action_id: AttackerActionId, logged_in_ips : str,
                                        num_new_users: int):
        if attacker_action_id not in self.num_new_users:
            self.num_new_users[attacker_action_id.value] = {}
            self.num_new_users[attacker_action_id.value][logged_in_ips] = {}
            self.num_new_users[attacker_action_id.value][logged_in_ips][num_new_users] = 1
        else:
            if logged_in_ips in self.num_new_users[attacker_action_id.value]:
                if num_new_users in self.num_new_users[attacker_action_id.value][logged_in_ips]:
                    self.num_new_users[attacker_action_id.value][logged_in_ips][num_new_users] \
                        = self.num_new_users[attacker_action_id.value][logged_in_ips][num_new_users] + 1
            else:
                self.num_new_users[attacker_action_id.value][logged_in_ips] = {}
                self.num_new_users[attacker_action_id.value][logged_in_ips][num_new_users] = 1

    def add_new_logged_in_user_transition(self, attacker_action_id: AttackerActionId, logged_in_ips : str,
                                          num_new_logged_in_users: int):
        if attacker_action_id not in self.num_new_logged_in_users:
            self.num_new_logged_in_users[attacker_action_id.value] = {}
            self.num_new_logged_in_users[attacker_action_id.value][logged_in_ips] = {}
            self.num_new_logged_in_users[attacker_action_id.value][logged_in_ips][num_new_logged_in_users] = 1
        else:
            if logged_in_ips in self.num_new_logged_in_users[attacker_action_id.value]:
                if num_new_logged_in_users in self.num_new_logged_in_users[attacker_action_id.value][logged_in_ips]:
                    self.num_new_logged_in_users[attacker_action_id.value][logged_in_ips][num_new_logged_in_users] \
                        = self.num_new_logged_in_users[attacker_action_id.value][logged_in_ips][num_new_logged_in_users] + 1
            else:
                self.num_new_logged_in_users[attacker_action_id.value][logged_in_ips] = {}
                self.num_new_logged_in_users[attacker_action_id.value][logged_in_ips][num_new_logged_in_users] = 1



    def add_new_login_event_transition(self, attacker_action_id: AttackerActionId, logged_in_ips : str,
                                         num_new_login_events: int):
        if attacker_action_id not in self.num_new_login_events:
            self.num_new_login_events[attacker_action_id.value] = {}
            self.num_new_login_events[attacker_action_id.value][logged_in_ips] = {}
            self.num_new_login_events[attacker_action_id.value][logged_in_ips][num_new_login_events] = 1
        else:
            if logged_in_ips in self.num_new_login_events[attacker_action_id.value]:
                if num_new_login_events in self.num_new_login_events[attacker_action_id.value][logged_in_ips]:
                    self.num_new_login_events[attacker_action_id.value][logged_in_ips][num_new_login_events] \
                        = self.num_new_login_events[attacker_action_id.value][logged_in_ips][num_new_login_events] + 1
            else:
                self.num_new_login_events[attacker_action_id.value][logged_in_ips] = {}
                self.num_new_login_events[attacker_action_id.value][logged_in_ips][num_new_login_events] = 1



    def add_new_processes_transition(self, attacker_action_id: AttackerActionId, logged_in_ips : str,
                                          num_new_processes: int):
        if attacker_action_id not in self.num_new_processes:
            self.num_new_processes[attacker_action_id.value] = {}
            self.num_new_processes[attacker_action_id.value][logged_in_ips] = {}
            self.num_new_processes[attacker_action_id.value][logged_in_ips][num_new_processes] = 1
        else:
            if logged_in_ips in self.num_new_processes[attacker_action_id.value]:
                if num_new_processes in self.num_new_processes[attacker_action_id.value][logged_in_ips]:
                    self.num_new_processes[attacker_action_id.value][logged_in_ips][num_new_processes] \
                        = self.num_new_processes[attacker_action_id.value][logged_in_ips][num_new_processes] + 1
            else:
                self.num_new_processes[attacker_action_id.value][logged_in_ips] = {}
                self.num_new_processes[attacker_action_id.value][logged_in_ips][num_new_processes] = 1



    def reset(self):
        self.num_new_open_connections = {}
        self.num_new_failed_login_attempts = {}
        self.num_new_users = {}
        self.num_new_logged_in_users = {}
        self.num_new_login_events = {}
        self.num_new_processes = {}


    def __str__(self):
        return "open_connections_dynamics:{},\n failed_login_attempts_dynamics:{},\n user_dynamics:{},\n " \
               "logged_in_users_dynamics:{},\n login_events_dynamics:{},\n processes_dynamics:{}\n".format(
            self.num_new_open_connections, self.num_new_failed_login_attempts, self.num_new_users,
            self.num_new_logged_in_users, self.num_new_login_events, self.num_new_processes
        )




