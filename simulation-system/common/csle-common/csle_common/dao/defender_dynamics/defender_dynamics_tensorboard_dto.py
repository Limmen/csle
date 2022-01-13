
class DefenderDynamicsTensorboardDTO:
    """
    DTO for tensorboard logging of defender dynamics model
    """

    def __init__(self, t: int = 0, num_new_alerts: int = 0, num_new_priority: int = 0, num_new_severe_alerts: int = 0,
                 num_new_warning_alerts: int = 0, num_new_open_connections: int = 0,
                 num_new_failed_login_attempts: int = 0, num_new_login_events: int = 0, num_new_processes: int = 0,
                 index : int = 0, attacker_action_id: int = 0, attacker_action_idx : int = 0,
                 attacker_action_name : str = "", num_new_pids: float = 0.0, cpu_percent_change: float = 0.0,
                 new_mem_current_change: float = 0.0, new_mem_total_change: float = 0.0,
                 new_mem_percent_change: float = 0.0,
                 new_blk_read_change: float = 0.0, new_blk_write_change: float = 0.0,
                 new_net_rx_change: float = 0.0, new_net_tx_change: float = 0.0):
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
        :param num_new_pids: number of pids
        :param cpu_percent_change: CPU percent utilization
        :param new_mem_current_change: current memory usage
        :param new_mem_total_change: total available memory
        :param new_mem_percent_change: memory utilization percentage
        :param new_blk_read_change: number of read IO bytes
        :param new_blk_write_change: number of written IO bytes
        :param new_net_rx_change: received network bytes
        :param new_net_tx_change: sent network bytes
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
        self.num_pids = num_new_pids
        self.cpu_percent= cpu_percent_change
        self.mem_current = new_mem_current_change
        self.mem_total = new_mem_total_change
        self.mem_percent = new_mem_percent_change
        self.blk_read = new_blk_read_change
        self.blk_write = new_blk_write_change
        self.net_rx = new_net_rx_change
        self.net_tx = new_net_tx_change

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
        tensorboard_writer.add_scalar('system_id/'
                                      + "t=" + str(self.t) + "_id=" + str(self.attacker_action_id)
                                      + "_idx=" + str(self.attacker_action_idx) + "_" + self.attacker_action_name
                                      + "/num_pids",
                                      self.num_pids, self.index)
        tensorboard_writer.add_scalar('system_id/'
                                      + "t=" + str(self.t) + "_id=" + str(self.attacker_action_id)
                                      + "_idx=" + str(self.attacker_action_idx) + "_" + self.attacker_action_name
                                      + "/cpu_percent",
                                      self.cpu_percent, self.index)
        tensorboard_writer.add_scalar('system_id/'
                                      + "t=" + str(self.t) + "_id=" + str(self.attacker_action_id)
                                      + "_idx=" + str(self.attacker_action_idx) + "_" + self.attacker_action_name
                                      + "/mem_current",
                                      self.mem_current, self.index)
        tensorboard_writer.add_scalar('system_id/'
                                      + "t=" + str(self.t) + "_id=" + str(self.attacker_action_id)
                                      + "_idx=" + str(self.attacker_action_idx) + "_" + self.attacker_action_name
                                      + "/mem_total",
                                      self.mem_total, self.index)
        tensorboard_writer.add_scalar('system_id/'
                                      + "t=" + str(self.t) + "_id=" + str(self.attacker_action_id)
                                      + "_idx=" + str(self.attacker_action_idx) + "_" + self.attacker_action_name
                                      + "/mem_percent",
                                      self.mem_percent, self.index)
        tensorboard_writer.add_scalar('system_id/'
                                      + "t=" + str(self.t) + "_id=" + str(self.attacker_action_id)
                                      + "_idx=" + str(self.attacker_action_idx) + "_" + self.attacker_action_name
                                      + "/blk_read",
                                      self.blk_read, self.index)
        tensorboard_writer.add_scalar('system_id/'
                                      + "t=" + str(self.t) + "_id=" + str(self.attacker_action_id)
                                      + "_idx=" + str(self.attacker_action_idx) + "_" + self.attacker_action_name
                                      + "/blk_write",
                                      self.blk_write, self.index)
        tensorboard_writer.add_scalar('system_id/'
                                      + "t=" + str(self.t) + "_id=" + str(self.attacker_action_id)
                                      + "_idx=" + str(self.attacker_action_idx) + "_" + self.attacker_action_name
                                      + "/net_rx",
                                      self.net_rx, self.index)
        tensorboard_writer.add_scalar('system_id/'
                                      + "t=" + str(self.t) + "_id=" + str(self.attacker_action_id)
                                      + "_idx=" + str(self.attacker_action_idx) + "_" + self.attacker_action_name
                                      + "/net_tx",
                                      self.net_tx, self.index)

    def __str__(self):
        """
        :return: a string representation of the DTO
        """
        return f"t: {self.t}, num_new_alerts: {self.num_new_alerts}, num_new_priority: {self.num_new_priority}, " \
               f"num_new_severe_alerts: {self.num_new_severe_alerts}, " \
               f"num_new_warning_alerts: {self.num_new_warning_alerts}," \
               f" num_new_open_connections: {self.num_new_open_connections}, " \
               f"num_new_failed_login_attempts: {self.num_new_failed_login_attempts}, " \
               f"num_new_login_events: {self.num_new_login_events}, num_new_processes: {self.num_new_processes}, " \
               f"attacker_action_id: {self.attacker_action_id}, attacker_action_idx: {self.attacker_action_idx}," \
               f" attacker_action_name:{self.attacker_action_name}, num_pids:{self.num_pids}, " \
               f"cpu_percent: {self.cpu_percent}, mem_current:{self.mem_current}, mem_total: {self.mem_total}," \
               f"mem_percent: {self.mem_percent}, blk_read: {self.blk_read}, blk_write: {self.blk_write}," \
               f"net_rx: {self.net_rx}, net_tx: {self.net_tx}"