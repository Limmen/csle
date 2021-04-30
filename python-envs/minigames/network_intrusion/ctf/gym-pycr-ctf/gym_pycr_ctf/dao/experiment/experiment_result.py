"""
Experiment results
"""
from typing import List
import csv

class ExperimentResult:
    """
    DTO with experiment result from an experiment in the pycr-ctf-envs
    """

    def __init__(self, attacker_avg_episode_rewards: List[float] = None,
                 defender_avg_episode_rewards: List[float] = None,
                 avg_episode_steps: List[int] = None, epsilon_values: List[float] = None,
                 attacker_cumulative_reward: List[int] = None,
                 defender_cumulative_reward: List[int] = None,
                 attacker_avg_episode_loss: List[float] = None,
                 defender_avg_episode_loss: List[float] = None,
                 lr_list : List[float] = None,
                 avg_episode_flags : List[int] = None,
                 avg_episode_flags_percentage: List[float] = None,
                 attacker_eval_avg_episode_rewards : List[float] = None,
                 defender_eval_avg_episode_rewards: List[float] = None,
                 eval_avg_episode_steps: List[float] = None,
                 eval_avg_episode_flags: List[int] = None,
                 eval_avg_episode_flags_percentage: List[float] = None,
                 attacker_eval_2_avg_episode_rewards: List[float] = None,
                 defender_eval_2_avg_episode_rewards: List[float] = None,
                 eval_2_avg_episode_steps: List[float] = None,
                 eval_2_avg_episode_flags: List[int] = None,
                 eval_2_avg_episode_flags_percentage: List[float] = None,
                 attacker_train_env_specific_rewards: dict = None,
                 defender_train_env_specific_rewards: dict = None,
                 train_env_specific_steps: dict = None,
                 train_env_specific_flags: dict = None,
                 train_env_specific_flags_percentage: dict = None,
                 attacker_train_env_specific_regrets: dict = None,
                 defender_train_env_specific_regrets: dict = None,
                 attacker_train_env_specific_opt_fracs: dict = None,
                 defender_train_env_specific_opt_fracs: dict = None,
                 attacker_eval_env_specific_rewards: dict = None,
                 defender_eval_env_specific_rewards: dict = None,
                 eval_env_specific_steps: dict = None,
                 eval_env_specific_flags: dict = None,
                 eval_env_specific_flags_percentage: dict = None,
                 attacker_eval_env_specific_regrets: dict = None,
                 defender_eval_env_specific_regrets: dict = None,
                 attacker_eval_env_specific_opt_fracs: dict = None,
                 defender_eval_env_specific_opt_fracs: dict = None,
                 attacker_eval_2_env_specific_rewards: dict = None,
                 defender_eval_2_env_specific_rewards: dict = None,
                 eval_2_env_specific_steps: dict = None,
                 eval_2_env_specific_flags: dict = None,
                 eval_2_env_specific_flags_percentage: dict = None,
                 attacker_eval_2_env_specific_regrets: dict = None,
                 defender_eval_2_env_specific_regrets: dict = None,
                 attacker_eval_2_env_specific_opt_fracs: dict = None,
                 defender_eval_2_env_specific_opt_fracs: dict = None,
                 rollout_times : List = None, env_response_times : List = None,
                 action_pred_times : List = None, grad_comp_times : List = None,
                 weight_update_times : List = None,
                 attacker_avg_regret: List = None, defender_avg_regret: List = None,
                 attacker_avg_opt_frac : List = None, defender_avg_opt_frac : List = None,
                 attacker_eval_avg_regret: List = None, defender_eval_avg_regret: List = None,
                 attacker_eval_avg_opt_frac: List = None, defender_eval_avg_opt_frac: List = None,
                 attacker_eval_2_avg_regret: List = None, defender_eval_2_avg_regret: List = None,
                 attacker_eval_2_avg_opt_frac: List = None, defender_eval_2_avg_opt_frac: List = None,
                 caught_frac: List = None, early_stopping_frac: List = None,
                 intrusion_frac: List = None,
                 eval_caught_frac: List = None, eval_early_stopping_frac: List = None,
                 eval_intrusion_frac: List = None,
                 eval_2_caught_frac: List = None, eval_2_early_stopping_frac: List = None,
                 eval_2_intrusion_frac: List = None,
                 snort_severe_baseline_rewards : List = None, snort_warning_baseline_rewards : List = None,
                 eval_snort_severe_baseline_rewards: List = None, eval_snort_warning_baseline_rewards: List = None,
                 eval_2_snort_severe_baseline_rewards: List = None, eval_2_snort_warning_baseline_rewards: List = None,
                 snort_critical_baseline_rewards: List = None, var_log_baseline_rewards : List = None,
                 eval_snort_critical_baseline_rewards: List = None, eval_var_log_baseline_rewards: List = None,
                 eval_2_snort_critical_baseline_rewards: List = None, eval_2_var_log_baseline_rewards: List = None,
                 attacker_action_costs: List[float] = None,
                 attacker_action_costs_norm: List[float] = None,
                 attacker_action_alerts: List[float] = None,
                 attacker_action_alerts_norm: List[float] = None,
                 eval_attacker_action_costs: List[float] = None,
                 eval_attacker_action_costs_norm: List[float] = None,
                 eval_attacker_action_alerts: List[float] = None,
                 eval_attacker_action_alerts_norm: List[float] = None,
                 eval_2_attacker_action_costs: List[float] = None,
                 eval_2_attacker_action_costs_norm: List[float] = None,
                 eval_2_attacker_action_alerts: List[float] = None,
                 eval_2_attacker_action_alerts_norm: List[float] = None,
                 time_elapsed : List[float] = None
                 ):
        """
        Constructor, initializes the DTO

        :param attacker_avg_episode_rewards: list of episode rewards for attacker
        :param defender_avg_episode_rewards: list of episode rewards for defender
        :param avg_episode_steps: list of episode steps
        :param epsilon_values: list of epsilon values
        :param attacker_cumulative_reward: list of attacker cumulative rewards
        :param defender_cumulative_reward: list of defender cumulative rewards
        :param attacker_avg_episode_loss: average loss for attacker
        :param defender_avg_episode_loss: average loss for defnder
        :param lr_list: learning rates
        :param avg_episode_flags: avg number of flags catched per episode
        :param avg_episode_flags_percentage: avg % of flags catched per episode
        :param attacker_eval_avg_episode_rewards: list of episode rewards for eval deterministic attacker
        :param defender_eval_avg_episode_rewards: list of episode rewards for eval deterministic defender
        :param eval_avg_episode_steps: list of episode steps for eval deterministic
        :param eval_avg_episode_flags: list of episode flags for eval deterministic
        :param eval_avg_episode_flags_percentage: list of episode flags for eval deterministic
        :param attacker_eval_2_avg_episode_rewards: list of episode rewards for second eval env deterministic attacker
        :param defender_eval_2_avg_episode_rewards: list of episode rewards for second eval env deterministic defender
        :param eval_2_avg_episode_steps: list of episode steps for second eval enveval deterministic
        :param eval_2_avg_episode_flags: list of episode flags for second eval enveval deterministic
        :param eval_2_avg_episode_flags_percentage: list of episode flags for second eval env eval deterministic
        :param attacker_train_env_specific_rewards: rewards data for specific train env attacker
        :param defender_train_env_specific_rewards: rewards data for specific train env defender
        :param train_env_specific_flags: flags data for specific train env
        :param train_env_specific_steps: steps data for specific train env
        :param train_env_specific_flags_percentage: flags percentage for specific train env
        :param attacker_eval_env_specific_rewards: eval reward data for specific train env deterministic attacker
        :param defender_eval_env_specific_rewards: eval reward data for specific train env deterministic defender
        :param eval_env_specific_flags: eval flags data for specific train env deterministic
        :param eval_env_specific_flags_percentage: eval flags percentage data for specific train env deterministic
        :param eval_env_specific_steps: eval steps data for specific train env deterministic
        :param attacker_eval_2_env_specific_rewards: eval reward data for specific eval env deterministic attacker
        :param defender_eval_2_env_specific_rewards: eval reward data for specific eval env deterministic defender
        :param eval_2_env_specific_flags: eval flags data for specific eval env deterministic
        :param eval_2_env_specific_flags_percentage: eval flags percentage dat2a for specific eval env deterministic
        :param eval_2_env_specific_steps: eval steps data for specific eval env env deterministic
        :param caught_frac: percentage that the attacker was caught by the defender
        :param early_stopping_frac: percentage that the defender stopped too early
        :param intrusion_frac: percentage of successful intrusions by the attacker
        :param eval_caught_frac: eval percentage that the attacker was caught by the defender
        :param eval_early_stopping_frac: eval percentage that the defender stopped too early
        :param eval_intrusion_frac: eval percentage of successful intrusions by the attacker
        :param eval_2_caught_frac: eval2 percentage that the attacker was caught by the defender
        :param eval_2_early_stopping_frac: eval2 percentage that the defender stopped too early
        :param eval_2_intrusion_frac: eval2 percentage of successful intrusions by the attacker
        :param snort_severe_baseline_rewards: rewards of the snort severe baseline
        :param snort_warning_baseline_rewards: rewards of the snort warning baseline
        :param eval_snort_severe_baseline_rewards: eval rewards of the snort severe baseline
        :param eval_snort_warning_baseline_rewards: eval rewards of the snort warning baseline
        :param eval_2_snort_severe_baseline_rewards: eval 2 rewards of the snort severe baseline
        :param eval_2_snort_warning_baseline_rewards: eval 2 rewards of the snort warning baseline
        :param snort_critical_baseline_rewards: rewards of the snort critical baseline
        :param var_log_baseline_rewards: rewards of the var_log  baseline
        :param eval_snort_critical_baseline_rewards: eval rewards of the snort critical baseline
        :param eval_var_log_baseline_rewards: eval rewards of the var_log  baseline
        :param eval_2_snort_critical_baseline_rewards: eval 2 rewards of the snort critical baseline
        :param eval_2_var_log_baseline_rewards: eval 2 rewards of the var_log  baseline
        :param time_elapsed: the time elapsed from start of training
        """
        self.attacker_avg_episode_rewards = attacker_avg_episode_rewards
        self.defender_avg_episode_rewards = defender_avg_episode_rewards
        self.avg_episode_steps = avg_episode_steps
        self.epsilon_values = epsilon_values
        self.attacker_cumulative_reward = attacker_cumulative_reward
        self.defender_cumulative_reward = defender_cumulative_reward
        self.attacker_avg_episode_loss = attacker_avg_episode_loss
        self.defender_avg_episode_loss = defender_avg_episode_loss
        self.lr_list = lr_list
        self.avg_episode_flags = avg_episode_flags
        self.avg_episode_flags_percentage = avg_episode_flags_percentage
        self.attacker_eval_avg_episode_rewards = attacker_eval_avg_episode_rewards
        self.defender_eval_avg_episode_rewards = defender_eval_avg_episode_rewards
        self.eval_avg_episode_steps = eval_avg_episode_steps
        self.eval_avg_episode_flags = eval_avg_episode_flags
        self.eval_avg_episode_flags_percentage = eval_avg_episode_flags_percentage
        self.attacker_eval_2_avg_episode_rewards = attacker_eval_2_avg_episode_rewards
        self.defender_eval_2_avg_episode_rewards = defender_eval_2_avg_episode_rewards
        self.eval_2_avg_episode_steps = eval_2_avg_episode_steps
        self.eval_2_avg_episode_flags = eval_2_avg_episode_flags
        self.eval_2_avg_episode_flags_percentage = eval_2_avg_episode_flags_percentage
        self.attacker_train_env_specific_rewards = attacker_train_env_specific_rewards
        self.defender_train_env_specific_rewards = defender_train_env_specific_rewards
        self.train_env_specific_flags = train_env_specific_flags
        self.train_env_specific_steps = train_env_specific_steps
        self.train_env_specific_flags_percentage = train_env_specific_flags_percentage
        self.attacker_train_env_specific_regrets = attacker_train_env_specific_regrets
        self.defender_train_env_specific_regrets = defender_train_env_specific_regrets
        self.attacker_train_env_specific_opt_fracs = attacker_train_env_specific_opt_fracs
        self.defender_train_env_specific_opt_fracs = defender_train_env_specific_opt_fracs
        self.attacker_eval_env_specific_rewards = attacker_eval_env_specific_rewards
        self.defender_eval_env_specific_rewards = defender_eval_env_specific_rewards
        self.eval_env_specific_flags = eval_env_specific_flags
        self.eval_env_specific_steps = eval_env_specific_steps
        self.eval_env_specific_flags_percentage = eval_env_specific_flags_percentage
        self.attacker_eval_env_specific_regrets = attacker_eval_env_specific_regrets
        self.defender_eval_env_specific_regrets = defender_eval_env_specific_regrets
        self.attacker_eval_env_specific_opt_fracs = attacker_eval_env_specific_opt_fracs
        self.defender_eval_env_specific_opt_fracs = defender_eval_env_specific_opt_fracs
        self.attacker_eval_2_env_specific_rewards = attacker_eval_2_env_specific_rewards
        self.defender_eval_2_env_specific_rewards = defender_eval_2_env_specific_rewards
        self.eval_2_env_specific_flags = eval_2_env_specific_flags
        self.eval_2_env_specific_steps = eval_2_env_specific_steps
        self.eval_2_env_specific_flags_percentage = eval_2_env_specific_flags_percentage
        self.attacker_eval_2_env_specific_regrets = attacker_eval_2_env_specific_regrets
        self.defender_eval_2_env_specific_regrets = defender_eval_2_env_specific_regrets
        self.attacker_eval_2_env_specific_opt_fracs = attacker_eval_2_env_specific_opt_fracs
        self.defender_eval_2_env_specific_opt_fracs = defender_eval_2_env_specific_opt_fracs
        self.rollout_times = rollout_times
        self.env_response_times = env_response_times
        self.action_pred_times = action_pred_times
        self.grad_comp_times = grad_comp_times
        self.weight_update_times = weight_update_times
        self.attacker_avg_opt_frac = attacker_avg_opt_frac
        self.defender_avg_opt_frac = defender_avg_opt_frac
        self.attacker_avg_regret = attacker_avg_regret
        self.defender_avg_regret = defender_avg_regret
        self.attacker_eval_avg_regret = attacker_eval_avg_regret
        self.defender_eval_avg_regret = defender_eval_avg_regret
        self.attacker_eval_avg_opt_frac = attacker_eval_avg_opt_frac
        self.defender_eval_avg_opt_frac = defender_eval_avg_opt_frac
        self.attacker_eval_2_avg_regret = attacker_eval_2_avg_regret
        self.defender_eval_2_avg_regret = defender_eval_2_avg_regret
        self.attacker_eval_2_avg_opt_frac = attacker_eval_2_avg_opt_frac
        self.defender_eval_2_avg_opt_frac = defender_eval_2_avg_opt_frac
        self.caught_frac = caught_frac
        self.early_stopping_frac = early_stopping_frac
        self.intrusion_frac = intrusion_frac
        self.eval_caught_frac = eval_caught_frac
        self.eval_early_stopping_frac = eval_early_stopping_frac
        self.eval_intrusion_frac = eval_intrusion_frac
        self.eval_2_caught_frac = eval_2_caught_frac
        self.eval_2_early_stopping_frac = eval_2_early_stopping_frac
        self.eval_2_intrusion_frac = eval_2_intrusion_frac
        self.snort_severe_baseline_rewards = snort_severe_baseline_rewards
        self.snort_warning_baseline_rewards = snort_warning_baseline_rewards
        self.eval_snort_severe_baseline_rewards = eval_snort_severe_baseline_rewards
        self.eval_snort_warning_baseline_rewards = eval_snort_warning_baseline_rewards
        self.eval_2_snort_severe_baseline_rewards = eval_2_snort_severe_baseline_rewards
        self.eval_2_snort_warning_baseline_rewards = eval_2_snort_warning_baseline_rewards
        self.snort_critical_baseline_rewards = snort_critical_baseline_rewards
        self.var_log_baseline_rewards= var_log_baseline_rewards
        self.eval_snort_critical_baseline_rewards = eval_snort_critical_baseline_rewards
        self.eval_var_log_baseline_rewards = eval_var_log_baseline_rewards
        self.eval_2_snort_critical_baseline_rewards = eval_2_snort_critical_baseline_rewards
        self.eval_2_var_log_baseline_rewards = eval_2_var_log_baseline_rewards
        self.attacker_action_costs = attacker_action_costs
        self.attacker_action_costs_norm = attacker_action_costs_norm
        self.attacker_action_alerts = attacker_action_alerts
        self.attacker_action_alerts_norm = attacker_action_alerts_norm
        self.eval_attacker_action_costs = eval_attacker_action_costs
        self.eval_attacker_action_costs_norm = eval_attacker_action_costs_norm
        self.eval_attacker_action_alerts = eval_attacker_action_alerts
        self.eval_attacker_action_alerts_norm = eval_attacker_action_alerts_norm
        self.eval_2_attacker_action_costs = eval_2_attacker_action_costs
        self.eval_2_attacker_action_costs_norm = eval_2_attacker_action_costs_norm
        self.eval_2_attacker_action_alerts = eval_2_attacker_action_alerts
        self.eval_2_attacker_action_alerts_norm = eval_2_attacker_action_alerts_norm
        self.time_elapsed = time_elapsed

        if avg_episode_steps is None:
            self.avg_episode_steps = []
        if attacker_avg_episode_rewards is None:
            self.attacker_avg_episode_rewards = []
        if defender_avg_episode_rewards is None:
            self.defender_avg_episode_rewards = []
        if epsilon_values is None:
            self.epsilon_values = []
        if attacker_cumulative_reward is None:
            self.attacker_cumulative_reward = []
        if defender_cumulative_reward is None:
            self.defender_cumulative_reward = []
        if attacker_avg_episode_loss is None:
            self.attacker_avg_episode_loss = []
        if defender_avg_episode_loss is None:
            self.defender_avg_episode_loss = []
        if lr_list is None:
            self.lr_list = []
        if avg_episode_flags is None:
            self.avg_episode_flags = []
        if avg_episode_flags_percentage is None:
            self.avg_episode_flags_percentage = []
        if attacker_eval_avg_episode_rewards is None:
            self.attacker_eval_avg_episode_rewards = []
        if defender_eval_avg_episode_rewards is None:
            self.defender_eval_avg_episode_rewards = []
        if eval_avg_episode_steps is None:
            self.eval_avg_episode_steps = []
        if eval_avg_episode_flags is None:
            self.eval_avg_episode_flags = []
        if eval_avg_episode_flags_percentage is None:
            self.eval_avg_episode_flags_percentage = []
        if attacker_eval_2_avg_episode_rewards is None:
            self.attacker_eval_2_avg_episode_rewards = []
        if defender_eval_2_avg_episode_rewards is None:
            self.defender_eval_2_avg_episode_rewards = []
        if eval_2_avg_episode_steps is None:
            self.eval_2_avg_episode_steps = []
        if eval_2_avg_episode_flags is None:
            self.eval_2_avg_episode_flags = []
        if eval_2_avg_episode_flags_percentage is None:
            self.eval_2_avg_episode_flags_percentage = []
        if attacker_train_env_specific_rewards is None:
            self.attacker_train_env_specific_rewards = {}
        if defender_train_env_specific_rewards is None:
            self.defender_train_env_specific_rewards = {}
        if attacker_train_env_specific_regrets is None:
            self.attacker_train_env_specific_regrets = {}
        if defender_train_env_specific_regrets is None:
            self.defender_train_env_specific_regrets = {}
        if attacker_train_env_specific_opt_fracs is None:
            self.attacker_train_env_specific_opt_fracs = {}
        if defender_train_env_specific_opt_fracs is None:
            self.defender_train_env_specific_opt_fracs = {}
        if train_env_specific_steps is None:
            self.train_env_specific_steps = {}
        if train_env_specific_flags is None:
            self.train_env_specific_flags = {}
        if train_env_specific_flags_percentage is None:
            self.train_env_specific_flags_percentage = {}
        if attacker_eval_env_specific_rewards is None:
            self.attacker_eval_env_specific_rewards = {}
        if defender_eval_env_specific_rewards is None:
            self.defender_eval_env_specific_rewards = {}
        if attacker_eval_env_specific_regrets is None:
            self.attacker_eval_env_specific_regrets = {}
        if defender_eval_env_specific_regrets is None:
            self.defender_eval_env_specific_regrets = {}
        if attacker_eval_env_specific_opt_fracs is None:
            self.attacker_eval_env_specific_opt_fracs = {}
        if defender_eval_env_specific_opt_fracs is None:
            self.defender_eval_env_specific_opt_fracs = {}
        if eval_env_specific_steps is None:
            self.eval_env_specific_steps = {}
        if eval_env_specific_flags is None:
            self.eval_env_specific_flags = {}
        if eval_env_specific_flags_percentage is None:
            self.eval_env_specific_flags_percentage = {}
        if attacker_eval_2_env_specific_rewards is None:
            self.attacker_eval_2_env_specific_rewards = {}
        if defender_eval_2_env_specific_rewards is None:
            self.defender_eval_2_env_specific_rewards = {}
        if attacker_eval_2_env_specific_regrets is None:
            self.attacker_eval_2_env_specific_regrets = {}
        if defender_eval_2_env_specific_regrets is None:
            self.defender_eval_2_env_specific_regrets = {}
        if attacker_eval_2_env_specific_opt_fracs is None:
            self.attacker_eval_2_env_specific_opt_fracs = {}
        if defender_eval_2_env_specific_opt_fracs is None:
            self.defender_eval_2_env_specific_opt_fracs = {}
        if eval_2_env_specific_steps is None:
            self.eval_2_env_specific_steps = {}
        if eval_2_env_specific_flags is None:
            self.eval_2_env_specific_flags = {}
        if eval_2_env_specific_flags_percentage is None:
            self.eval_2_env_specific_flags_percentage = {}
        if rollout_times is None:
            self.rollout_times = []
        if env_response_times is None:
            self.env_response_times = []
        if action_pred_times is None:
            self.action_pred_times = []
        if grad_comp_times is None:
            self.grad_comp_times = []
        if weight_update_times is None:
            self.weight_update_times = []
        if attacker_avg_regret is None:
            self.attacker_avg_regret = []
        if defender_avg_regret is None:
            self.defender_avg_regret = []
        if attacker_avg_opt_frac is None:
            self.attacker_avg_opt_frac = []
        if defender_avg_opt_frac is None:
            self.defender_avg_opt_frac = []
        if attacker_eval_avg_regret is None:
            self.attacker_eval_avg_regret = []
        if defender_eval_avg_regret is None:
            self.defender_eval_avg_regret = []
        if attacker_eval_avg_opt_frac is None:
            self.attacker_eval_avg_opt_frac = []
        if defender_eval_avg_opt_frac is None:
            self.defender_eval_avg_opt_frac = []
        if attacker_eval_2_avg_regret is None:
            self.attacker_eval_2_avg_regret = []
        if defender_eval_2_avg_regret is None:
            self.defender_eval_2_avg_regret = []
        if attacker_eval_2_avg_opt_frac is None:
            self.attacker_eval_2_avg_opt_frac = []
        if defender_eval_2_avg_opt_frac is None:
            self.defender_eval_2_avg_opt_frac = []
        if caught_frac is None:
            self.caught_frac = []
        if early_stopping_frac is None:
            self.early_stopping_frac = []
        if intrusion_frac is None:
            self.intrusion_frac = []
        if eval_caught_frac is None:
            self.eval_caught_frac = []
        if eval_early_stopping_frac is None:
            self.eval_early_stopping_frac = []
        if eval_intrusion_frac is None:
            self.eval_intrusion_frac = []
        if eval_2_caught_frac is None:
            self.eval_2_caught_frac = []
        if eval_2_early_stopping_frac is None:
            self.eval_2_early_stopping_frac = []
        if eval_2_intrusion_frac is None:
            self.eval_2_intrusion_frac = []
        if snort_severe_baseline_rewards is None:
            self.snort_severe_baseline_rewards = []
        if snort_warning_baseline_rewards is None:
            self.snort_warning_baseline_rewards = []
        if eval_snort_severe_baseline_rewards is None:
            self.eval_snort_severe_baseline_rewards = []
        if eval_snort_warning_baseline_rewards is None:
            self.eval_snort_warning_baseline_rewards = []
        if eval_2_snort_severe_baseline_rewards is None:
            self.eval_2_snort_severe_baseline_rewards = []
        if eval_2_snort_warning_baseline_rewards is None:
            self.eval_2_snort_warning_baseline_rewards = []
        if snort_critical_baseline_rewards is None:
            self.snort_critical_baseline_rewards = []
        if var_log_baseline_rewards is None:
            self.var_log_baseline_rewards = []
        if eval_snort_critical_baseline_rewards is None:
            self.eval_snort_critical_baseline_rewards = []
        if eval_var_log_baseline_rewards is None:
            self.eval_var_log_baseline_rewards = []
        if eval_2_snort_critical_baseline_rewards is None:
            self.eval_2_snort_critical_baseline_rewards = []
        if eval_2_var_log_baseline_rewards is None:
            self.eval_2_var_log_baseline_rewards = []
        if attacker_action_costs is None:
            self.attacker_action_costs = []
        if attacker_action_costs_norm is None:
            self.attacker_action_costs_norm = []
        if attacker_action_alerts is None:
            self.attacker_action_alerts = []
        if attacker_action_alerts_norm is None:
            self.attacker_action_alerts_norm = []
        if eval_attacker_action_costs is None:
            self.eval_attacker_action_costs = []
        if eval_attacker_action_costs_norm is None:
            self.eval_attacker_action_costs_norm = []
        if eval_attacker_action_alerts is None:
            self.eval_attacker_action_alerts = []
        if eval_attacker_action_alerts_norm is None:
            self.eval_attacker_action_alerts_norm = []
        if eval_2_attacker_action_costs is None:
            self.eval_2_attacker_action_costs = []
        if eval_2_attacker_action_costs_norm is None:
            self.eval_2_attacker_action_costs_norm = []
        if eval_2_attacker_action_alerts is None:
            self.eval_2_attacker_action_alerts = []
        if eval_2_attacker_action_alerts_norm is None:
            self.eval_2_attacker_action_alerts_norm = []
        if time_elapsed is None:
            self.time_elapsed = []

    def to_csv(self, file_path : str) -> None:
        """
        Save result to csv

        :param file_path: path to save the csv file
        :return: None
        """
        metrics = [self.attacker_avg_episode_rewards, self.defender_avg_episode_rewards, self.avg_episode_steps,
                   self.epsilon_values,
                   self.attacker_cumulative_reward, self.defender_cumulative_reward,
                   self.attacker_avg_episode_loss, self.defender_avg_episode_loss,
                   self.lr_list, self.avg_episode_flags,
                   self.avg_episode_flags_percentage, self.attacker_eval_avg_episode_rewards,
                   self.defender_eval_avg_episode_rewards,
                   self.eval_avg_episode_steps,
                   self.eval_avg_episode_flags, self.eval_avg_episode_flags_percentage,
                   self.attacker_eval_2_avg_episode_rewards, self.defender_eval_2_avg_episode_rewards,
                   self.eval_2_avg_episode_steps,
                   self.eval_2_avg_episode_flags, self.eval_2_avg_episode_flags_percentage, self.rollout_times,
                   self.env_response_times, self.action_pred_times, self.grad_comp_times, self.weight_update_times,
                   self.attacker_avg_regret, self.defender_avg_regret,
                   self.attacker_avg_opt_frac, self.defender_avg_opt_frac,
                   self.attacker_eval_avg_regret, self.defender_eval_avg_regret,
                   self.attacker_eval_avg_opt_frac, self.defender_eval_avg_opt_frac,
                   self.attacker_eval_2_avg_regret, self.defender_eval_2_avg_regret,
                   self.attacker_eval_2_avg_opt_frac, self.defender_eval_2_avg_opt_frac,
                   self.caught_frac, self.early_stopping_frac, self.intrusion_frac,
                   self.eval_caught_frac, self.eval_early_stopping_frac, self.eval_intrusion_frac,
                   self.eval_2_caught_frac, self.eval_2_early_stopping_frac,
                   self.eval_2_intrusion_frac,
                   self.snort_severe_baseline_rewards, self.snort_warning_baseline_rewards,
                   self.eval_snort_severe_baseline_rewards, self.eval_snort_warning_baseline_rewards,
                   self.eval_2_snort_severe_baseline_rewards, self.eval_2_snort_warning_baseline_rewards,
                   self.snort_critical_baseline_rewards, self.var_log_baseline_rewards,
                   self.eval_snort_critical_baseline_rewards, self.eval_var_log_baseline_rewards,
                   self.eval_2_snort_critical_baseline_rewards, self.eval_2_var_log_baseline_rewards,
                   self.attacker_action_costs, self.attacker_action_costs_norm,
                   self.attacker_action_alerts, self.attacker_action_alerts_norm,
                   self.eval_attacker_action_costs, self.eval_attacker_action_costs_norm,
                   self.eval_attacker_action_alerts, self.eval_attacker_action_alerts_norm,
                   self.eval_2_attacker_action_costs, self.eval_2_attacker_action_costs_norm,
                   self.eval_2_attacker_action_alerts, self.eval_2_attacker_action_alerts_norm,
                   self.time_elapsed
                   ]
        metric_labels = ["attacker_avg_episode_rewards", "defender_avg_episode_rewards", "avg_episode_steps",
                         "epsilon_values", "attacker_cumulative_reward", "defender_cumulative_reward",
                         "attacker_avg_episode_loss",
                         "defender_avg_episode_loss",
                         "lr_list", "avg_episode_flags", "avg_episode_flags_percentage",
                         "attacker_eval_avg_episode_rewards", "defender_eval_avg_episode_rewards",
                         "eval_avg_episode_steps", "eval_avg_episode_flags", "eval_avg_episode_flags_percentage",
                         "attacker_eval_2_avg_episode_rewards", "defender_eval_2_avg_episode_rewards",
                         "eval_2_avg_episode_steps", "eval_2_avg_episode_flags",
                         "eval_2_avg_episode_flags_percentage", "rollout_times", "env_response_times",
                         "action_pred_times",
                         "grad_comp_times", "weight_update_times", "attacker_avg_regret", "defender_avg_regret",
                         "attacker_avg_opt_frac", "defender_avg_opt_frac",
                         "attacker_eval_avg_regret", "defender_eval_avg_regret",
                         "attacker_eval_avg_opt_frac", "defender_eval_avg_opt_frac",
                         "attacker_eval_2_avg_regret", "defender_eval_2_avg_regret",
                         "attacker_eval_2_avg_opt_frac", "defender_eval_2_avg_opt_frac",
                         "caught_frac","early_stopping_frac","intrusion_frac",
                         "eval_caught_frac", "eval_early_stopping_frac", "eval_intrusion_frac",
                         "eval_2_caught_frac", "eval_2_early_stopping_frac", "eval_2_intrusion_frac",
                         "snort_severe_baseline_rewards", "snort_warning_baseline_rewards",
                         "eval_snort_severe_baseline_rewards", "eval_snort_warning_baseline_rewards",
                         "eval_2_snort_severe_baseline_rewards", "eval_2_snort_warning_baseline_rewards",
                         "snort_critical_baseline_rewards", "var_log_baseline_rewards",
                         "eval_snort_critical_baseline_rewards", "eval_var_log_baseline_rewards",
                         "eval_2_snort_critical_baseline_rewards", "eval_2_var_log_baseline_rewards",
                         "attacker_action_costs", "attacker_action_costs_norm",
                         "attacker_action_alerts", "attacker_action_alerts_norm",
                         "eval_attacker_action_costs", "eval_attacker_action_costs_norm",
                         "eval_attacker_action_alerts", "eval_attacker_action_alerts_norm",
                         "eval_2_attacker_action_costs", "eval_2_attacker_action_costs_norm",
                         "eval_2_attacker_action_alerts", "eval_2_attacker_action_alerts_norm",
                         "time_elapsed"
                         ]
        filtered_metric_labels = []
        filtered_metrics = []
        for i in range(len(metrics)):
            if len(metrics[i]) > 0:
                filtered_metrics.append(metrics[i])
                filtered_metric_labels.append(metric_labels[i])

        for key in self.attacker_train_env_specific_rewards.keys():
            if len(self.attacker_train_env_specific_rewards[key]) > 0:
                filtered_metrics.append(self.attacker_train_env_specific_rewards[key])
                filtered_metric_labels.append(str(key) + "_" + "attacker_avg_episode_rewards")
        for key in self.defender_train_env_specific_rewards.keys():
            if len(self.defender_train_env_specific_rewards[key]) > 0:
                filtered_metrics.append(self.defender_train_env_specific_rewards[key])
                filtered_metric_labels.append(str(key) + "_" + "defender_avg_episode_rewards")
        for key in self.attacker_train_env_specific_regrets.keys():
            if len(self.attacker_train_env_specific_regrets[key]) > 0:
                filtered_metrics.append(self.attacker_train_env_specific_regrets[key])
                filtered_metric_labels.append(str(key) + "_" + "attacker_avg_episode_regrets")
        for key in self.defender_train_env_specific_regrets.keys():
            if len(self.defender_train_env_specific_regrets[key]) > 0:
                filtered_metrics.append(self.defender_train_env_specific_regrets[key])
                filtered_metric_labels.append(str(key) + "_" + "defender_avg_episode_regrets")
        for key in self.attacker_train_env_specific_opt_fracs.keys():
            if len(self.attacker_train_env_specific_opt_fracs[key]) > 0:
                filtered_metrics.append(self.attacker_train_env_specific_opt_fracs[key])
                filtered_metric_labels.append(str(key) + "_" + "attacker_avg_episode_opt_fracs")
        for key in self.defender_train_env_specific_opt_fracs.keys():
            if len(self.defender_train_env_specific_opt_fracs[key]) > 0:
                filtered_metrics.append(self.defender_train_env_specific_opt_fracs[key])
                filtered_metric_labels.append(str(key) + "_" + "defender_avg_episode_opt_fracs")
        for key in self.train_env_specific_steps.keys():
            if len(self.train_env_specific_steps[key]) > 0:
                filtered_metrics.append(self.train_env_specific_steps[key])
                filtered_metric_labels.append(str(key) + "_" + "avg_episode_steps")
        for key in self.train_env_specific_flags.keys():
            if len(self.train_env_specific_flags[key]) > 0:
                filtered_metrics.append(self.train_env_specific_flags[key])
                filtered_metric_labels.append(str(key) + "_" + "avg_episode_flags")
        for key in self.train_env_specific_flags_percentage.keys():
            if len(self.train_env_specific_flags_percentage[key]) > 0:
                filtered_metrics.append(self.train_env_specific_flags_percentage[key])
                filtered_metric_labels.append(str(key) + "_" + "avg_episode_flags_percentage")
        for key in self.attacker_eval_env_specific_rewards.keys():
            if len(self.attacker_eval_env_specific_rewards[key]) > 0:
                filtered_metrics.append(self.attacker_eval_env_specific_rewards[key])
                filtered_metric_labels.append(str(key) + "_" + "attacker_eval_avg_episode_rewards")
        for key in self.defender_eval_env_specific_rewards.keys():
            if len(self.defender_eval_env_specific_rewards[key]) > 0:
                filtered_metrics.append(self.defender_eval_env_specific_rewards[key])
                filtered_metric_labels.append(str(key) + "_" + "defender_eval_avg_episode_rewards")
        for key in self.attacker_eval_env_specific_regrets.keys():
            if len(self.attacker_eval_env_specific_regrets[key]) > 0:
                filtered_metrics.append(self.attacker_eval_env_specific_regrets[key])
                filtered_metric_labels.append(str(key) + "_" + "attacker_eval_avg_episode_regrets")
        for key in self.defender_eval_env_specific_regrets.keys():
            if len(self.defender_eval_env_specific_regrets[key]) > 0:
                filtered_metrics.append(self.defender_eval_env_specific_regrets[key])
                filtered_metric_labels.append(str(key) + "_" + "defender_eval_avg_episode_regrets")
        for key in self.attacker_eval_env_specific_opt_fracs.keys():
            if len(self.attacker_eval_env_specific_opt_fracs[key]) > 0:
                filtered_metrics.append(self.attacker_eval_env_specific_opt_fracs[key])
                filtered_metric_labels.append(str(key) + "_" + "attacker_eval_avg_episode_opt_fracs")
        for key in self.defender_eval_env_specific_opt_fracs.keys():
            if len(self.defender_eval_env_specific_opt_fracs[key]) > 0:
                filtered_metrics.append(self.defender_eval_env_specific_opt_fracs[key])
                filtered_metric_labels.append(str(key) + "_" + "defender_eval_avg_episode_opt_fracs")
        for key in self.eval_env_specific_steps.keys():
            if len(self.eval_env_specific_steps[key]) > 0:
                filtered_metrics.append(self.eval_env_specific_steps[key])
                filtered_metric_labels.append(str(key) + "_" + "eval_avg_episode_steps")
        for key in self.eval_env_specific_flags.keys():
            if len(self.eval_env_specific_flags[key]) > 0:
                filtered_metrics.append(self.eval_env_specific_flags[key])
                filtered_metric_labels.append(str(key) + "_" + "eval_avg_episode_flags")
        for key in self.eval_env_specific_flags_percentage.keys():
            if len(self.eval_env_specific_flags_percentage[key]) > 0:
                filtered_metrics.append(self.eval_env_specific_flags_percentage[key])
                filtered_metric_labels.append(str(key) + "_" + "eval_avg_episode_flags_percentage")
        for key in self.attacker_eval_2_env_specific_rewards.keys():
            if len(self.attacker_eval_2_env_specific_rewards[key]) > 0:
                filtered_metrics.append(self.attacker_eval_2_env_specific_rewards[key])
                filtered_metric_labels.append(str(key) + "_" + "attacker_eval_2_avg_episode_rewards")
        for key in self.defender_eval_2_env_specific_rewards.keys():
            if len(self.defender_eval_2_env_specific_rewards[key]) > 0:
                filtered_metrics.append(self.defender_eval_2_env_specific_rewards[key])
                filtered_metric_labels.append(str(key) + "_" + "defender_eval_2_avg_episode_rewards")
        for key in self.attacker_eval_2_env_specific_regrets.keys():
            if len(self.attacker_eval_2_env_specific_regrets[key]) > 0:
                filtered_metrics.append(self.attacker_eval_2_env_specific_regrets[key])
                filtered_metric_labels.append(str(key) + "_" + "attacker_eval_2_avg_episode_regrets")
        for key in self.defender_eval_2_env_specific_regrets.keys():
            if len(self.defender_eval_2_env_specific_regrets[key]) > 0:
                filtered_metrics.append(self.defender_eval_2_env_specific_regrets[key])
                filtered_metric_labels.append(str(key) + "_" + "defender_eval_2_avg_episode_regrets")
        for key in self.attacker_eval_2_env_specific_opt_fracs.keys():
            if len(self.attacker_eval_2_env_specific_opt_fracs[key]) > 0:
                filtered_metrics.append(self.attacker_eval_2_env_specific_opt_fracs[key])
                filtered_metric_labels.append(str(key) + "_" + "attacker_eval_2_avg_episode_opt_fracs")
        for key in self.defender_eval_2_env_specific_opt_fracs.keys():
            if len(self.defender_eval_2_env_specific_opt_fracs[key]) > 0:
                filtered_metrics.append(self.defender_eval_2_env_specific_opt_fracs[key])
                filtered_metric_labels.append(str(key) + "_" + "defender_eval_2_avg_episode_opt_fracs")
        for key in self.eval_2_env_specific_steps.keys():
            if len(self.eval_2_env_specific_steps[key]) > 0:
                filtered_metrics.append(self.eval_2_env_specific_steps[key])
                filtered_metric_labels.append(str(key) + "_" + "eval_2_avg_episode_steps")
        for key in self.eval_2_env_specific_flags.keys():
            if len(self.eval_2_env_specific_flags[key]) > 0:
                filtered_metrics.append(self.eval_2_env_specific_flags[key])
                filtered_metric_labels.append(str(key) + "_" + "eval_2_avg_episode_flags")
        for key in self.eval_2_env_specific_flags_percentage.keys():
            if len(self.eval_2_env_specific_flags_percentage[key]) > 0:
                filtered_metrics.append(self.eval_2_env_specific_flags_percentage[key])
                filtered_metric_labels.append(str(key) + "_" + "eval_2_avg_episode_flags_percentage")

        # for i in range(len(filtered_metrics)):
        #     print("filtered metric: {}, len:{}".format(filtered_metric_labels[i], len(filtered_metrics[i])))

        rows = zip(*filtered_metrics)
        with open(file_path, "w") as f:
            writer = csv.writer(f)
            writer.writerow(filtered_metric_labels)
            for row in rows:
                writer.writerow(row)