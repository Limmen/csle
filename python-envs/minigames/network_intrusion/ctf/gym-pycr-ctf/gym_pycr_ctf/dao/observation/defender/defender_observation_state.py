from typing import List
import numpy as np
import gym_pycr_ctf.constants.constants as constants
from gym_pycr_ctf.dao.observation.defender.defender_machine_observation_state import DefenderMachineObservationState
from gym_pycr_ctf.dao.action.defender.defender_action import DefenderAction


class DefenderObservationState:
    """
    Represents the defender's agent's current belief state of the environment
    """

    def __init__(self, num_machines : int, ids = False, maximum_number_of_stops : int = 1):
        """
        Initializes the DTO

        :param num_machines: the numer of machines
        :param ids: whether there is an IDS or not
        """
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
        self.num_login_attempts_total = 0

        self.num_alerts_total_all_stops = 0
        self.sum_priority_alerts_total_all_stops = 0
        self.num_severe_alerts_total_all_stops = 0
        self.num_warning_alerts_total_all_stops = 0
        self.num_login_attempts_total_all_stops = 0

        self.caught_attacker = False
        self.stopped = False
        self.adj_matrix = np.array(0)
        self.last_alert_ts = None
        self.step = 1
        self.maximum_number_of_stops = maximum_number_of_stops
        self.stops_remaining = maximum_number_of_stops
        self.first_stop_step = -1
        self.second_stop_step = -1
        self.third_stop_step = -1
        self.fourth_stop_step = -1

        self.snort_warning_baseline_reward = 0
        self.snort_severe_baseline_reward = 0
        self.snort_critical_baseline_reward = 0
        self.var_log_baseline_reward = 0
        self.step_baseline_reward = 0

        self.snort_warning_baseline_step = 1
        self.snort_severe_baseline_step = 1
        self.snort_critical_baseline_step = 1
        self.var_log_baseline_step = 1
        self.step_baseline_step = 1

        self.snort_severe_baseline_stopped = False
        self.snort_warning_baseline_stopped = False
        self.snort_critical_baseline_stopped = False
        self.var_log_baseline_stopped = False
        self.step_baseline_stopped = False

        self.snort_severe_baseline_caught_attacker = False
        self.snort_warning_baseline_caught_attacker = False
        self.snort_critical_baseline_caught_attacker = False
        self.var_log_baseline_caught_attacker = False
        self.step_baseline_caught_attacker = False

        self.snort_severe_baseline_early_stopping = False
        self.snort_warning_baseline_early_stopping = False
        self.snort_critical_baseline_early_stopping = False
        self.var_log_baseline_early_stopping = False
        self.step_baseline_early_stopping = False

        self.snort_severe_baseline_uncaught_intrusion_steps = 0
        self.snort_warning_baseline_uncaught_intrusion_steps = 0
        self.snort_critical_baseline_uncaught_intrusion_steps = 0
        self.var_log_baseline_uncaught_intrusion_steps = 0
        self.step_baseline_uncaught_intrusion_steps = 0

        self.snort_severe_baseline_first_stop_step = 0
        self.snort_warning_baseline_first_stop_step = 0
        self.snort_critical_baseline_first_stop_step = 0
        self.var_log_baseline_first_stop_step = 0
        self.step_baseline_first_stop_step = 0

        self.snort_severe_baseline_second_stop_step = 0
        self.snort_warning_baseline_second_stop_step = 0
        self.snort_critical_baseline_second_stop_step = 0
        self.var_log_baseline_second_stop_step = 0
        self.step_baseline_second_stop_step = 0

        self.snort_severe_baseline_third_stop_step = 0
        self.snort_warning_baseline_third_stop_step = 0
        self.snort_critical_baseline_third_stop_step = 0
        self.var_log_baseline_third_stop_step = 0
        self.step_baseline_third_stop_step = 0

        self.snort_severe_baseline_fourth_stop_step = 0
        self.snort_warning_baseline_fourth_stop_step = 0
        self.snort_critical_baseline_fourth_stop_step = 0
        self.var_log_baseline_fourth_stop_step = 0
        self.step_baseline_fourth_stop_step = 0

        self.snort_severe_baseline_stops_remaining = self.maximum_number_of_stops
        self.snort_warning_baseline_stops_remaining = self.maximum_number_of_stops
        self.snort_critical_baseline_stops_remaining = self.maximum_number_of_stops
        self.var_log_baseline_stops_remaining = self.maximum_number_of_stops
        self.step_baseline_stops_remaining = self.maximum_number_of_stops


    def sort_machines(self) -> None:
        """
        Sorts the machines in the observation

        :return: None
        """
        self.machines = sorted(self.machines, key=lambda x: int(x.ip.rsplit(".", 1)[-1]), reverse=False)

    def cleanup(self) -> None:
        """
        Cleans up the machines in the observation

        :return: None
        """
        for m in self.machines:
            m.cleanup()

    def get_action_ip(self, a : DefenderAction) -> str:
        """
        Gets the ip of the node that a defender action is targeted for

        :param a: the action
        :return: the ip of the target node
        """
        if a.index == -1:
            self.sort_machines()
            ips = list(map(lambda x: x.ip, self.machines))
            ips_str = "_".join(ips)
            return ips_str
        if a.index < len(self.machines) and a.index < self.num_machines:
            return self.machines[a.index].ip
        return a.ip

    def copy(self) -> "DefenderObservationState":
        """
        :return: a copy of the object
        """
        c = DefenderObservationState(num_machines = self.num_machines, ids=self.ids,
                                     maximum_number_of_stops=self.maximum_number_of_stops)
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
        c.snort_warning_baseline_reward = self.snort_warning_baseline_reward
        c.snort_severe_baseline_reward = self.snort_severe_baseline_reward
        c.snort_critical_baseline_reward = self.snort_critical_baseline_reward
        c.var_log_baseline_reward = self.var_log_baseline_reward
        c.step_baseline_reward = self.step_baseline_reward
        c.snort_warning_baseline_stopped = self.snort_warning_baseline_stopped
        c.snort_severe_baseline_stopped = self.snort_severe_baseline_stopped
        c.snort_critical_baseline_stopped = self.snort_critical_baseline_stopped
        c.var_log_baseline_stopped = self.var_log_baseline_stopped
        c.step_baseline_stopped = self.step_baseline_stopped
        c.snort_warning_baseline_step = self.snort_warning_baseline_step
        c.snort_severe_baseline_step = self.snort_severe_baseline_step
        c.snort_critical_baseline_step = self.snort_critical_baseline_step
        c.var_log_baseline_step = self.var_log_baseline_step
        c.step_baseline_step = self.step_baseline_step
        c.snort_warning_baseline_caught_attacker = self.snort_warning_baseline_caught_attacker
        c.snort_severe_baseline_caught_attacker = self.snort_severe_baseline_caught_attacker
        c.snort_critical_baseline_caught_attacker = self.snort_critical_baseline_caught_attacker
        c.var_log_baseline_caught_attacker = self.var_log_baseline_caught_attacker
        c.step_baseline_caught_attacker = self.step_baseline_caught_attacker
        c.snort_warning_baseline_early_stopping = self.snort_warning_baseline_early_stopping
        c.snort_severe_baseline_early_stopping = self.snort_severe_baseline_early_stopping
        c.snort_critical_baseline_early_stopping = self.snort_critical_baseline_early_stopping
        c.var_log_baseline_early_stopping = self.var_log_baseline_early_stopping
        c.step_baseline_caught_early_stopping = self.step_baseline_early_stopping
        c.snort_warning_baseline_uncaught_intrusion_steps = self.snort_warning_baseline_uncaught_intrusion_steps
        c.snort_severe_baseline_uncaught_intrusion_steps = self.snort_severe_baseline_uncaught_intrusion_steps
        c.snort_critical_baseline_uncaught_intrusion_steps = self.snort_critical_baseline_uncaught_intrusion_steps
        c.var_log_baseline_uncaught_intrusion_steps = self.var_log_baseline_uncaught_intrusion_steps
        c.step_baseline_caught_uncaught_intrusion_steps = self.step_baseline_uncaught_intrusion_steps
        c.last_alert_ts = self.last_alert_ts
        c.first_stop_step = self.first_stop_step
        c.second_stop_step = self.second_stop_step
        c.third_stop_step = self.third_stop_step
        c.fourth_stop_step = self.fourth_stop_step
        c.snort_severe_baseline_first_stop_step = self.snort_severe_baseline_first_stop_step
        c.snort_warning_baseline_first_stop_step = self.snort_warning_baseline_first_stop_step
        c.snort_critical_baseline_first_stop_step = self.snort_critical_baseline_first_stop_step
        c.var_log_baseline_first_stop_step = self.var_log_baseline_first_stop_step
        c.step_baseline_first_stop_step = self.step_baseline_first_stop_step
        c.snort_severe_baseline_second_stop_step = self.snort_severe_baseline_second_stop_step
        c.snort_warning_baseline_second_stop_step = self.snort_warning_baseline_second_stop_step
        c.snort_critical_baseline_second_stop_step = self.snort_critical_baseline_second_stop_step
        c.var_log_baseline_second_stop_step = self.var_log_baseline_second_stop_step
        c.step_baseline_second_stop_step = self.step_baseline_second_stop_step
        c.snort_severe_baseline_third_stop_step = self.snort_severe_baseline_third_stop_step
        c.snort_warning_baseline_third_stop_step = self.snort_warning_baseline_third_stop_step
        c.snort_critical_baseline_third_stop_step = self.snort_critical_baseline_third_stop_step
        c.var_log_baseline_third_stop_step = self.var_log_baseline_third_stop_step
        c.step_baseline_third_stop_step = self.step_baseline_third_stop_step
        c.snort_severe_baseline_fourth_stop_step = self.snort_severe_baseline_fourth_stop_step
        c.snort_warning_baseline_fourth_stop_step = self.snort_warning_baseline_fourth_stop_step
        c.snort_critical_baseline_fourth_stop_step = self.snort_critical_baseline_fourth_stop_step
        c.var_log_baseline_fourth_stop_step = self.var_log_baseline_fourth_stop_step
        c.step_baseline_fourth_stop_step = self.step_baseline_fourth_stop_step
        c.snort_severe_baseline_stops_remaining = self.snort_severe_baseline_stops_remaining
        c.snort_warning_baseline_stops_remaining = self.snort_warning_baseline_stops_remaining
        c.snort_critical_baseline_stops_remaining = self.snort_critical_baseline_stops_remaining
        c.var_log_baseline_stops_remaining = self.var_log_baseline_stops_remaining
        c.step_baseline_stops_remaining = self.step_baseline_stops_remaining
        c.num_warning_alerts_total_all_stops = self.num_warning_alerts_total_all_stops
        c.num_severe_alerts_total_all_stops = self.num_severe_alerts_total_all_stops
        c.num_alerts_total_all_stops = self.num_alerts_total_all_stops
        c.num_login_attempts_total = self.num_login_attempts_total
        c.num_login_attempts_total_all_stops = self.num_login_attempts_total_all_stops

        for m in self.machines:
            c.machines.append(m.copy())
        return c

    def update_info_dict(self, info: dict) -> dict:
        """
        Update the info dict with information from the defender's observation state

        :param info: the info dict
        :return: the updated dict
        """
        info[constants.INFO_DICT.CAUGHT_ATTACKER] = self.caught_attacker
        info[constants.INFO_DICT.EARLY_STOPPED] = self.stopped
        info[constants.INFO_DICT.SNORT_SEVERE_BASELINE_REWARD] = self.snort_severe_baseline_reward
        info[constants.INFO_DICT.SNORT_WARNING_BASELINE_REWARD] = self.snort_warning_baseline_reward
        info[constants.INFO_DICT.SNORT_CRITICAL_BASELINE_REWARD] = self.snort_critical_baseline_reward
        info[constants.INFO_DICT.VAR_LOG_BASELINE_REWARD] = self.var_log_baseline_reward
        info[constants.INFO_DICT.STEP_BASELINE_REWARD] = self.step_baseline_reward
        info[constants.INFO_DICT.SNORT_SEVERE_BASELINE_STEP] = self.snort_severe_baseline_step
        info[constants.INFO_DICT.SNORT_WARNING_BASELINE_STEP] = self.snort_warning_baseline_step
        info[constants.INFO_DICT.SNORT_CRITICAL_BASELINE_STEP] = self.snort_critical_baseline_step
        info[constants.INFO_DICT.VAR_LOG_BASELINE_STEP] = self.var_log_baseline_step
        info[constants.INFO_DICT.STEP_BASELINE_STEP] = self.step_baseline_step
        info[constants.INFO_DICT.SNORT_SEVERE_BASELINE_CAUGHT_ATTACKER] = self.snort_severe_baseline_caught_attacker
        info[constants.INFO_DICT.SNORT_WARNING_BASELINE_CAUGHT_ATTACKER] = self.snort_warning_baseline_caught_attacker
        info[constants.INFO_DICT.SNORT_CRITICAL_BASELINE_CAUGHT_ATTACKER] = self.snort_critical_baseline_caught_attacker
        info[constants.INFO_DICT.VAR_LOG_BASELINE_CAUGHT_ATTACKER] = self.var_log_baseline_caught_attacker
        info[constants.INFO_DICT.STEP_BASELINE_CAUGHT_ATTACKER] = self.step_baseline_caught_attacker
        info[constants.INFO_DICT.SNORT_SEVERE_BASELINE_EARLY_STOPPING] = self.snort_severe_baseline_early_stopping
        info[constants.INFO_DICT.SNORT_WARNING_BASELINE_EARLY_STOPPING] = self.snort_warning_baseline_early_stopping
        info[constants.INFO_DICT.SNORT_CRITICAL_BASELINE_EARLY_STOPPING] = self.snort_critical_baseline_early_stopping
        info[constants.INFO_DICT.VAR_LOG_BASELINE_EARLY_STOPPING] = self.var_log_baseline_early_stopping
        info[constants.INFO_DICT.STEP_BASELINE_EARLY_STOPPING] = self.step_baseline_early_stopping
        info[constants.INFO_DICT.SNORT_SEVERE_BASELINE_UNCAUGHT_INTRUSION_STEPS] = self.snort_severe_baseline_uncaught_intrusion_steps
        info[constants.INFO_DICT.SNORT_WARNING_BASELINE_UNCAUGHT_INTRUSION_STEPS] = self.snort_warning_baseline_uncaught_intrusion_steps
        info[constants.INFO_DICT.SNORT_CRITICAL_BASELINE_UNCAUGHT_INTRUSION_STEPS] = self.snort_critical_baseline_uncaught_intrusion_steps
        info[constants.INFO_DICT.VAR_LOG_BASELINE_UNCAUGHT_INTRUSION_STEPS] = self.var_log_baseline_uncaught_intrusion_steps
        info[constants.INFO_DICT.STEP_BASELINE_UNCAUGHT_INTRUSION_STEPS] = self.step_baseline_uncaught_intrusion_steps
        info[constants.INFO_DICT.DEFENDER_STOPS_REMAINING] = self.stops_remaining
        info[constants.INFO_DICT.DEFENDER_FIRST_STOP_STEP] = self.first_stop_step
        info[constants.INFO_DICT.DEFENDER_SECOND_STOP_STEP] = self.second_stop_step
        info[constants.INFO_DICT.DEFENDER_THIRD_STOP_STEP] = self.third_stop_step
        info[constants.INFO_DICT.DEFENDER_FOURTH_STOP_STEP] = self.fourth_stop_step
        info[constants.INFO_DICT.SNORT_SEVERE_BASELINE_FIRST_STOP_STEP] = self.snort_severe_baseline_first_stop_step
        info[constants.INFO_DICT.SNORT_WARNING_BASELINE_FIRST_STOP_STEP] = self.snort_warning_baseline_first_stop_step
        info[constants.INFO_DICT.SNORT_CRITICAL_BASELINE_FIRST_STOP_STEP] = self.snort_critical_baseline_first_stop_step
        info[constants.INFO_DICT.VAR_LOG_BASELINE_FIRST_STOP_STEP] = self.var_log_baseline_first_stop_step
        info[constants.INFO_DICT.STEP_BASELINE_FIRST_STOP_STEP] = self.step_baseline_first_stop_step
        info[constants.INFO_DICT.SNORT_SEVERE_BASELINE_SECOND_STOP_STEP] = self.snort_severe_baseline_second_stop_step
        info[constants.INFO_DICT.SNORT_WARNING_BASELINE_SECOND_STOP_STEP] = self.snort_warning_baseline_second_stop_step
        info[constants.INFO_DICT.SNORT_CRITICAL_BASELINE_SECOND_STOP_STEP] = self.snort_critical_baseline_second_stop_step
        info[constants.INFO_DICT.VAR_LOG_BASELINE_SECOND_STOP_STEP] = self.var_log_baseline_second_stop_step
        info[constants.INFO_DICT.STEP_BASELINE_SECOND_STOP_STEP] = self.step_baseline_second_stop_step
        info[constants.INFO_DICT.SNORT_SEVERE_BASELINE_THIRD_STOP_STEP] = self.snort_severe_baseline_third_stop_step
        info[constants.INFO_DICT.SNORT_WARNING_BASELINE_THIRD_STOP_STEP] = self.snort_warning_baseline_third_stop_step
        info[constants.INFO_DICT.SNORT_CRITICAL_BASELINE_THIRD_STOP_STEP] = self.snort_critical_baseline_third_stop_step
        info[constants.INFO_DICT.VAR_LOG_BASELINE_THIRD_STOP_STEP] = self.var_log_baseline_third_stop_step
        info[constants.INFO_DICT.STEP_BASELINE_THIRD_STOP_STEP] = self.step_baseline_third_stop_step
        info[constants.INFO_DICT.SNORT_SEVERE_BASELINE_FOURTH_STOP_STEP] = self.snort_severe_baseline_fourth_stop_step
        info[constants.INFO_DICT.SNORT_WARNING_BASELINE_FOURTH_STOP_STEP] = self.snort_warning_baseline_fourth_stop_step
        info[constants.INFO_DICT.SNORT_CRITICAL_BASELINE_FOURTH_STOP_STEP] = self.snort_critical_baseline_fourth_stop_step
        info[constants.INFO_DICT.VAR_LOG_BASELINE_FOURTH_STOP_STEP] = self.var_log_baseline_fourth_stop_step
        info[constants.INFO_DICT.STEP_BASELINE_FOURTH_STOP_STEP] = self.step_baseline_fourth_stop_step
        info[constants.INFO_DICT.SNORT_SEVERE_BASELINE_STOPS_REMAINING] = self.snort_severe_baseline_stops_remaining
        info[constants.INFO_DICT.SNORT_WARNING_BASELINE_STOPS_REMAINING] = self.snort_warning_baseline_stops_remaining
        info[constants.INFO_DICT.SNORT_CRITICAL_BASELINE_STOPS_REMAINING] = self.snort_critical_baseline_stops_remaining
        info[constants.INFO_DICT.VAR_LOG_BASELINE_STOPS_REMAINING] = self.var_log_baseline_stops_remaining
        info[constants.INFO_DICT.STEP_BASELINE_STOPS_REMAINING] = self.step_baseline_stops_remaining
        return info

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return  "# alerts recent:{}, # severe alerts recent: {}, # warning alerts recent: {}, " \
                "sum priority recent:{}, # alerts total:{} # severe alerts total: {}, " \
                "# warning alerts total: {}, sum priority total: {}, caught_attacker:{}," \
                "stopped:{}, step:{}, snort_severe_baseline_reward:{}, snort_warning_baseline_reward:{}," \
                "snort_severe_baseline_stopped:{}, snort_warning_baseline_stopped:{}," \
                "snort_critical_baseline_reward:{}, snort_critical_baseline_stopped:{}," \
                "var_log_baseline_reward:{}, var_log_baseline_stopped:{}, last_alert_ts:{}," \
                "snort_severe_baseline_step:{}, snort_warning_baseline_step:{}, snort_critical_baseline_step:{}," \
                "var_log_baseline_step:{}, step_baseline_reward:{}, step_baseline_step:{}, step_baseline_stopped:{}," \
                "number_of_stops_remaining:{}, first_stop_step:{}, second_stop_step:{}," \
                "third_stop_step:{}, fourth_stop_step:{}, maximum_number_of:stops:{}," \
                "snort_severe_baseline_first_stop_step:{}, snort_warning_baseline_first_stop_step:{}, " \
                "snort_critical_baseline_first_stop_step:{}, var_log_baseline_first_stop_step:{}, " \
                "step_baseline_first_stop_step:{}, snort_severe_baseline_second_stop_step:{}, " \
                "snort_warning_baseline_second_stop_step:{}, snort_critical_baseline_second_stop_step:{}," \
                "var_log_baseline_second_stop_step:{}, step_baseline_second_stop_step:{}, " \
                "snort_severe_baseline_third_stop_step:{}, snort_warning_baseline_third_stop_step:{}, " \
                "snort_critical_baseline_third_stop_step:{}, var_log_baseline_third_stop_step:{}, " \
                "step_baseline_third_stop_step:{}, " \
                "snort_severe_baseline_fourth_stop_step:{}, snort_warning_baseline_fourth_stop_step:{}, " \
                "snort_critical_baseline_fourth_stop_step:{}, var_log_baseline_fourth_stop_step:{}, " \
                "step_baseline_fourth_stop_step:{}, snort_severe_baseline_stops_remaining:{}, " \
                "snort_warning_baseline_stops_remaining:{}, snort_critical_baseline_stops_remaining:{}, " \
                "var_log_baseline_stops_remaining:{},step_baseline_stops_remaining:{}," \
                "num_severe_alerts_total_all_stops:{},num_warning_alerts_total_all_stops:{}, " \
                "num_login_attempts_total_all_stops:{},num_alerts_total_all_stops:{}," \
                "num_login_attempts_total:{}".format(
            self.num_alerts_recent, self.num_severe_alerts_recent, self.num_warning_alerts_recent,
            self.sum_priority_alerts_recent, self.num_alerts_total, self.num_severe_alerts_total,
            self.num_warning_alerts_total, self.sum_priority_alerts_total,
            self.caught_attacker, self.stopped, self.step, self.snort_severe_baseline_reward,
            self.snort_warning_baseline_reward, self.snort_severe_baseline_stopped,
            self.snort_warning_baseline_stopped, self.snort_critical_baseline_reward,
            self.snort_critical_baseline_stopped, self.var_log_baseline_reward, self.var_log_baseline_stopped,
            self.last_alert_ts, self.snort_severe_baseline_step, self.snort_warning_baseline_step,
            self.snort_critical_baseline_step, self.var_log_baseline_step, self.step_baseline_reward,
            self.step_baseline_step, self.step_baseline_stopped, self.stops_remaining, self.first_stop_step,
            self.second_stop_step, self.third_stop_step, self.fourth_stop_step, self.maximum_number_of_stops,
            self.snort_severe_baseline_first_stop_step, self.snort_warning_baseline_first_stop_step,
            self.snort_critical_baseline_first_stop_step, self.var_log_baseline_first_stop_step,
            self.step_baseline_first_stop_step,
            self.snort_severe_baseline_second_stop_step, self.snort_warning_baseline_second_stop_step,
            self.snort_critical_baseline_second_stop_step, self.var_log_baseline_second_stop_step,
            self.step_baseline_second_stop_step,
            self.snort_severe_baseline_third_stop_step, self.snort_warning_baseline_third_stop_step,
            self.snort_critical_baseline_third_stop_step, self.var_log_baseline_third_stop_step,
            self.step_baseline_third_stop_step,
            self.snort_severe_baseline_fourth_stop_step, self.snort_warning_baseline_fourth_stop_step,
            self.snort_critical_baseline_fourth_stop_step, self.var_log_baseline_fourth_stop_step,
            self.step_baseline_fourth_stop_step,
            self.snort_severe_baseline_stops_remaining, self.snort_warning_baseline_stops_remaining,
            self.snort_critical_baseline_fourth_stop_step, self.var_log_baseline_stops_remaining,
            self.step_baseline_stops_remaining,
            self.num_severe_alerts_total_all_stops, self.num_warning_alerts_total_all_stops,
            self.num_login_attempts_total_all_stops, self.num_alerts_total_all_stops, self.num_login_attempts_total
        ) + "\n" + "\n".join([str(i) + ":" + str(self.machines[i]) for i in range(len(self.machines))])
