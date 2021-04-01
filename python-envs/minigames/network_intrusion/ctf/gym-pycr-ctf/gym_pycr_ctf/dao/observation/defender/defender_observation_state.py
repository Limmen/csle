from typing import List
import numpy as np
from gym_pycr_ctf.dao.observation.defender.defender_machine_observation_state import DefenderMachineObservationState
from gym_pycr_ctf.dao.observation.common.connection_observation_state import ConnectionObservationState
from gym_pycr_ctf.dao.action.defender.defender_action import DefenderAction
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.envs_model.logic.emulation.util.defender.read_logs_util import ReadLogsUtil
from gym_pycr_ctf.envs_model.logic.emulation.util.defender.shell_util import ShellUtil
from gym_pycr_ctf.envs_model.logic.emulation.util.common.emulation_util import EmulationUtil
from gym_pycr_ctf.dao.state_representation.state_type import StateType
import gym_pycr_ctf.constants.constants as constants
import time


class DefenderObservationState:
    """
    Represents the defender's agent's current belief state of the environment
    """

    def __init__(self, num_machines : int, ids = False):
        self.num_machines = num_machines
        self.ids = ids
        self.machines : List[DefenderMachineObservationState] = []
        self.defense_actions_tried = set()
        self.num_alerts_recent = 0
        self.num_severe_alerts_recent = 0
        self.num_warning_alerts_recent = 0
        self.sum_priority_alerts_recent = 0
        self.num_alerts_total = 0
        self.sum_priority_alerts_total = 0
        self.num_severe_alerts_total = 0
        self.num_warning_alerts_total = 0
        self.caught_attacker = False
        self.stopped = False
        self.adj_matrix = np.array(0)
        self.ids_last_alert_ts = None

    def reset(self, env_config: EnvConfig, state_type: StateType) -> None:
        """
        Resets the defender's state

        :param env_config: the environment configuration
        :param state_type: the type of the belief state
        :return: None
        """
        self.num_alerts_recent = 0
        self.num_severe_alerts_recent = 0
        self.num_warning_alerts_recent = 0
        self.sum_priority_alerts_recent = 0
        self.num_alerts_total = 0
        self.sum_priority_alerts_total = 0
        self.num_severe_alerts_total = 0
        self.num_warning_alerts_total = 0

        # Update IDS timestamp
        if env_config.ids_router:
            self.last_alert_ts = EmulationUtil.get_latest_alert_ts(env_config=env_config)

        # Update logs timestamps
        for m in self.machines:
            m.failed_auth_last_ts = ReadLogsUtil.read_latest_ts_auth(emulation_config=m.emulation_config)
            m.login_last_ts = ReadLogsUtil.read_latest_ts_login(emulation_config=m.emulation_config)

        self.update_belief_state(env_config=env_config, state_type=state_type)

    def update_belief_state(self, env_config: EnvConfig, state_type: StateType) -> None:
        """
        Updates the defender's belief state

        :param env_config: the environment config
        :param state_type: the type of the state
        :return: None
        """

        print("-- Updating The Defender's Belief State -- ")

        tstart = time.time()

        # Measure IDS
        if env_config.ids_router:
            self.last_alert_ts = EmulationUtil.get_latest_alert_ts(env_config=env_config)
            # num_alerts, num_severe_alerts, num_warning_alerts, sum_priority_alerts, num_recent_alerts, \
            # num_recent_severe_alerts, num_recent_warning_alerts, sum_recent_priority_alerts = \
            #     ReadLogsUtil.read_ids_data(env_config=env_config, episode_last_alert_ts=self.last_alert_ts)

            num_alerts, num_severe_alerts, num_warning_alerts, sum_priority_alerts = \
                ReadLogsUtil.read_ids_data(env_config=env_config, episode_last_alert_ts=self.last_alert_ts)

            self.num_alerts_total = num_alerts
            self.num_severe_alerts_total = num_severe_alerts
            self.num_warning_alerts_total = num_warning_alerts
            self.sum_priority_alerts_total = sum_priority_alerts
            # self.num_alerts_recent = num_recent_alerts
            # self.num_severe_alerts_recent = num_recent_severe_alerts
            # self.num_warning_alerts_recent = num_recent_warning_alerts
            # self.sum_priority_alerts_recent = sum_recent_priority_alerts


        if state_type == StateType.BASE or state_type == StateType.ESSENTIAL or state_type == StateType.COMPACT:
            # Measure Node specific features
            for m in self.machines:

                # Measure metrics of the node
                m.num_logged_in_users = ShellUtil.read_logged_in_users(emulation_config=m.emulation_config)
                m.num_failed_login_attempts = ReadLogsUtil.read_failed_login_attempts(
                    emulation_config=m.emulation_config, failed_auth_last_ts=m.failed_auth_last_ts)
                m.num_open_connections = ShellUtil.read_open_connections(emulation_config=m.emulation_config)
                if state_type != StateType.COMPACT:
                    m.num_login_events = ReadLogsUtil.read_successful_login_events(
                        emulation_config=m.emulation_config, login_last_ts=m.login_last_ts)
                if state_type == StateType.BASE:
                    m.num_processes = ShellUtil.read_processes(emulation_config=m.emulation_config)

        tend = time.time()
        total_time = tend - tstart

        print("-- The Defender's Belief State Updated Successfully in {} seconds -- ".format(total_time))


    def initialize_state(self, service_lookup: dict,
                         cached_connections: dict, env_config: EnvConfig) -> None:
        """
        Initializes the defender's state by measuring various metrics using root-logins on the servers of
        the emulation

        :param service_lookup: a dict with numeric ids of services
        :param cached_connections: cached connections, if connections exist we can reuse them
        :param env_config: the environment configuraiton
        :return: None
        """
        print("-- Initializing The Defender's Belief State -- ")

        self.adj_matrix = env_config.network_conf.adj_matrix

        # Measure IDS
        if env_config.ids_router:
            self.last_alert_ts = EmulationUtil.get_latest_alert_ts(env_config=env_config)
            # num_alerts, num_severe_alerts, num_warning_alerts, sum_priority_alerts, num_recent_alerts, \
            # num_recent_severe_alerts, num_recent_warning_alerts, sum_recent_priority_alerts = \
            #     ReadLogsUtil.read_ids_data(env_config=env_config, episode_last_alert_ts=self.last_alert_ts)

            num_alerts, num_severe_alerts, num_warning_alerts, sum_priority_alerts = \
                ReadLogsUtil.read_ids_data(env_config=env_config, episode_last_alert_ts=self.last_alert_ts)

            self.num_alerts_total = num_alerts
            self.num_severe_alerts_total = num_severe_alerts
            self.num_warning_alerts_total = num_warning_alerts
            self.sum_priority_alerts_total = sum_priority_alerts
            # self.num_alerts_recent = num_recent_alerts
            # self.num_severe_alerts_recent = num_recent_severe_alerts
            # self.num_warning_alerts_recent = num_recent_warning_alerts
            # self.sum_priority_alerts_recent = sum_recent_priority_alerts

        # Measure Node specific features
        for node in env_config.network_conf.nodes:
            if node.ip == env_config.emulation_config.agent_ip:
                continue
            d_obs = node.to_defender_machine_obs(service_lookup)

            # Setup connection
            if node.ip in cached_connections:
                (node_connections, ec) = cached_connections[node.ip]
                node_conn = node_connections[0]
            else:
                ec = env_config.emulation_config.copy(ip=node.ip, username=constants.PYCR_ADMIN.user,
                                           pw=constants.PYCR_ADMIN.pw)
                ec.connect_agent()
                node_conn = ConnectionObservationState(
                    conn=ec.agent_conn, username=ec.agent_username, root=True, port=22,
                    service=constants.SSH.SERVICE_NAME, proxy=None, ip=node.ip)
            d_obs.ssh_connections.append(node_conn)
            d_obs.emulation_config = ec

            # Measure metrics of the node
            d_obs.num_logged_in_users = ShellUtil.read_logged_in_users(emulation_config=d_obs.emulation_config)
            d_obs.num_open_connections = ShellUtil.read_open_connections(emulation_config=d_obs.emulation_config)
            d_obs.num_users = ShellUtil.read_users(emulation_config=d_obs.emulation_config)
            d_obs.failed_auth_last_ts = ReadLogsUtil.read_latest_ts_auth(emulation_config=d_obs.emulation_config)
            d_obs.num_failed_login_attempts = ReadLogsUtil.read_failed_login_attempts(
                emulation_config=d_obs.emulation_config, failed_auth_last_ts=d_obs.failed_auth_last_ts)
            d_obs.login_last_ts = ReadLogsUtil.read_latest_ts_login(emulation_config=d_obs.emulation_config)
            d_obs.num_login_events = ReadLogsUtil.read_successful_login_events(
                emulation_config=d_obs.emulation_config, login_last_ts=d_obs.login_last_ts)
            d_obs.num_processes = ShellUtil.read_processes(emulation_config=d_obs.emulation_config)
            self.machines.append(d_obs)

        print("-- The Defender's Belief State Initialized Sucessfully -- ")


    def sort_machines(self):
        self.machines = sorted(self.machines, key=lambda x: int(x.ip.rsplit(".", 1)[-1]), reverse=False)

    def cleanup(self):
        for m in self.machines:
            m.cleanup()

    def get_action_ip(self, a : DefenderAction):
        if a.index == -1:
            self.sort_machines()
            ips = list(map(lambda x: x.ip, self.machines))
            ips_str = "_".join(ips)
            return ips_str
        if a.index < len(self.machines) and a.index < self.num_machines:
            return self.machines[a.index].ip
        return a.ip

    def copy(self):
        c = DefenderObservationState(num_machines = self.num_machines, ids=self.ids)
        c.caught_attacker = self.caught_attacker
        c.stopped = self.stopped
        c.defense_actions_tried = self.defense_actions_tried.copy()
        c.num_alerts_recent = self.num_alerts_recent
        c.num_severe_alerts_recent = self.num_severe_alerts_recent
        c.num_warning_alerts_recent = self.num_warning_alerts_recent
        c.sum_priority_alerts_recent = self.sum_priority_alerts_recent
        c.num_alerts_total = self.num_alerts_total
        c.num_severe_alerts_total = self.num_severe_alerts_total
        c.num_warning_alerts_total = self.num_warning_alerts_total
        c.sum_priority_alerts_total = self.sum_priority_alerts_total
        c.adj_matrix = self.adj_matrix
        for m in self.machines:
            c.machines.append(m.copy())
        return c

    def __str__(self):
        return  "# alerts recent:{}, # severe alerts recent: {}, # warning alerts recent: {}, " \
                "sum priority recent:{}, # alerts total:{} # severe alerts total: {}, " \
                "# warning alerts total: {}, sum priority total: {}, caught_attacker:{}," \
                " stopped:{}".format(
            self.num_alerts_recent, self.num_severe_alerts_recent, self.num_warning_alerts_recent,
            self.sum_priority_alerts_recent, self.num_alerts_total, self.num_severe_alerts_total,
            self.num_warning_alerts_total, self.sum_priority_alerts_total,
            self.caught_attacker, self.stopped) + "\n" + \
                "\n".join([str(i) + ":" + str(self.machines[i]) for i in range(len(self.machines))])
