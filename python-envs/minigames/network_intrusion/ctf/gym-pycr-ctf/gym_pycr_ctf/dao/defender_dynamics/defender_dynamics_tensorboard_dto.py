
class DefenderDynamicsTensorboardDTO:
    """
    DTO for tensorboard logging of defender dynamics model
    """

    def __init__(self, t: int = 0, num_new_alerts: int = 0, num_new_priority: int = 0, num_new_severe_alerts: int = 0,
                 num_new_warning_alerts: int = 0, num_new_open_connections: int = 0,
                 num_new_failed_login_attempts: int = 0, num_new_login_events: int = 0, num_new_processes: int = 0,
                 index : int = 0, attacker_action_id: int = 0, attacker_action_idx : int = 0,
                 attacker_action_name : str = ""):
        """
        Initializes the DTO

        :param t: the current time-step
        :param num_new_alerts: the number of new alerts
        :param num_new_priority: the number of new alert priorites
        :param num_new_severe_alerts: the number of new severe alerts
        :param num_new_warning_alerts: the number of new warning alerts
        :param num_new_open_connections: the number of new open connections
        :param num_new_failed_login_attempts: the number of new failed login attempts
        :param num_new_login_events: the number of new login events
        :param num_new_processes: the number of new processes
        :param index: the index for logging
        :param attacker_action_id: the attacker action id
        :param attacker_action_idx: the attacker action idx
        :param attacker_action_name: the attacker action name
        """
        self.t = t
        self.num_new_alerts = num_new_alerts
        self.num_new_priority = num_new_priority
        self.num_new_severe_alerts = num_new_severe_alerts
        self.num_new_warning_alerts = num_new_warning_alerts
        self.num_new_open_connections = num_new_open_connections
        self.num_new_failed_login_attempts = num_new_failed_login_attempts
        self.num_new_login_events = num_new_login_events
        self.num_new_processes = num_new_processes
        self.index = index
        self.attacker_action_id = attacker_action_id
        self.attacker_action_idx = attacker_action_idx
        self.attacker_action_name = attacker_action_name

    def log_tensorboard(self, tensorboard_writer) -> None:
        """
        Logs the dynamics to tensorboard

        :param tensorboard_writer: the tensorboard writer
        :return: None
        """
        tensorboard_writer.add_scalar('system_id/' + "t=" + str(self.t) + "_id=" + str(self.attacker_action_id)
                                      + "_idx=" + str(self.attacker_action_idx) + "_" + self.attacker_action_name
                                      + "/num_new_alerts",
                                           self.num_new_alerts, self.index)
        tensorboard_writer.add_scalar('system_id/'
                                      + "t=" + str(self.t) + "_id=" + str(self.attacker_action_id)
                                      + "_idx=" + str(self.attacker_action_idx) + "_" + self.attacker_action_name
                                      + "/num_new_priority",
                                      self.num_new_priority, self.index)
        tensorboard_writer.add_scalar('system_id/'
                                      + "t=" + str(self.t) + "_id=" + str(self.attacker_action_id)
                                      + "_idx=" + str(self.attacker_action_idx) + "_" + self.attacker_action_name
                                      + "/num_new_severe_alerts",
                                      self.num_new_severe_alerts, self.index)
        tensorboard_writer.add_scalar('system_id/'
                                      + "t=" + str(self.t) + "_id=" + str(self.attacker_action_id)
                                      + "_idx=" + str(self.attacker_action_idx) + "_" + self.attacker_action_name
                                      + "/num_new_warning_alerts",
                                      self.num_new_warning_alerts, self.index)
        tensorboard_writer.add_scalar('system_id/'
                                      + "t=" + str(self.t) + "_id=" + str(self.attacker_action_id)
                                      + "_idx=" + str(self.attacker_action_idx) + "_" + self.attacker_action_name
                                      + "/num_new_open_connections",
                                      self.num_new_open_connections, self.index)
        tensorboard_writer.add_scalar('system_id/'
                                      + "t=" + str(self.t) + "_id=" + str(self.attacker_action_id)
                                      + "_idx=" + str(self.attacker_action_idx) + "_" + self.attacker_action_name
                                      + "/num_new_failed_login_attempts",
                                      self.num_new_failed_login_attempts, self.index)
        tensorboard_writer.add_scalar('system_id/'
                                      + "t=" + str(self.t) + "_id=" + str(self.attacker_action_id)
                                      + "_idx=" + str(self.attacker_action_idx) + "_" + self.attacker_action_name
                                      + "/num_new_login_events",
                                      self.num_new_login_events, self.index)
        tensorboard_writer.add_scalar('system_id/'
                                      + "t=" + str(self.t) + "_id=" + str(self.attacker_action_id)
                                      + "_idx=" + str(self.attacker_action_idx) + "_" + self.attacker_action_name
                                      + "/num_new_processes",
                                      self.num_new_processes, self.index)

    def __str__(self):
        """
        :return: a string representation of the DTO
        """
        return "t: {}, num_new_alerts: {}, num_new_priority: {}, num_new_severe_alerts: {}, num_new_warning_alerts: {}," \
               " num_new_open_connections: {}, num_new_failed_login_attempts: {}, " \
               "num_new_login_events: {}, num_new_processes: {}, attacker_action_id: {}, attacker_action_idx: {}," \
               " attacker_action_name:{}".format(
            self.t, self.num_new_alerts, self.num_new_priority, self.num_new_severe_alerts, self.num_new_warning_alerts,
            self.num_new_open_connections, self.num_new_failed_login_attempts,
            self.num_new_login_events, self.num_new_processes, self.attacker_action_id, self.attacker_action_idx,
            self.attacker_action_name)