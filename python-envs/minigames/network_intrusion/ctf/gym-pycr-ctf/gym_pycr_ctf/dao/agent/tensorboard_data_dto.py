
class TensorboardDataDTO:
    """
    DTO with information for logging in tensorboard
    """
    def __init__(self, iteration : int = 0, avg_episode_rewards : float = 0.0,
                 avg_episode_steps : float = 0.0,
                 avg_episode_loss: float = 0.0, eps : float = 0.0,
                 lr: float = 0.0, eval: bool = False,
                 avg_flags_catched: float = 0.0, avg_episode_flags_percentage: float = 0.0,
                 eval_avg_episode_rewards: float = 0.0, eval_avg_episode_steps: float = 0.0,
                 eval_avg_episode_flags: float = 0.0, eval_avg_episode_flags_percentage: float = 0.0,
                 eval_2_avg_episode_rewards: float = 0.0, eval_2_avg_episode_steps: float = 0.0,
                 eval_2_avg_episode_flags: float = 0.0, eval_2_avg_episode_flags_percentage: float = 0.0,
                 rolling_avg_episode_rewards: float = 0.0, rolling_avg_episode_steps: float = 0.0,
                 tensorboard_writer = None, episode_caught_frac: float = 0.0,
                 episode_early_stopped_frac: float = 0.0, episode_successful_intrusion_frac: float = 0.0,
                 eval_episode_caught_frac: float = 0.0, eval_episode_early_stopped_frac: float = 0.0,
                 eval_episode_successful_intrusion_frac: float = 0.0, eval_2_episode_caught_frac: float = 0.0,
                 eval_2_episode_early_stopped_frac: float = 0.0, eval_2_episode_successful_intrusion_frac: float = 0.0,
                 avg_regret: float = 0.0, avg_opt_frac: float = 0.0, rolling_avg_rewards: float = 0.0,
                 rolling_avg_steps: float = 0.0, avg_episode_flags: float = 0.0, n_af: int = 0,
                 n_d : int = 0,
                 avg_episode_costs: float = 0.0, avg_episode_costs_norm: float = 0.0,
                 avg_episode_alerts: float = 0.0, avg_episode_alerts_norm: float = 0.0,
                 eval_avg_episode_costs: float = 0.0, eval_avg_episode_costs_norm: float = 0.0,
                 eval_avg_episode_alerts: float = 0.0, eval_avg_episode_alerts_norm: float = 0.0,
                 eval_2_avg_episode_costs: float = 0.0, eval_2_avg_episode_costs_norm: float = 0.0,
                 eval_2_avg_episode_alerts: float = 0.0, eval_2_avg_episode_alerts_norm: float = 0.0,
                 total_num_episodes: int = 0, avg_eval_regret: float = 0.0,
                 eval_avg_opt_frac: float = 0.0, avg_regret_2: float = 0.0,
                 avg_opt_frac_2: float = 0.0, epsilon: float = 0.0, training_time_hours: float = 0.0,
                 avg_episode_snort_severe_baseline_rewards : float = 0.0,
                 avg_episode_snort_warning_baseline_rewards: float = 0.0,
                 eval_avg_episode_snort_severe_baseline_rewards: float = 0.0,
                 eval_avg_episode_snort_warning_baseline_rewards: float = 0.0,
                 eval_avg_2_episode_snort_severe_baseline_rewards: float = 0.0,
                 eval_avg_2_episode_snort_warning_baseline_rewards: float = 0.0,
                 avg_episode_snort_critical_baseline_rewards: float = 0.0,
                 avg_episode_var_log_baseline_rewards: float = 0.0,
                 avg_episode_step_baseline_rewards: float = 0.0,
                 eval_avg_episode_snort_critical_baseline_rewards: float = 0.0,
                 eval_avg_episode_var_log_baseline_rewards: float = 0.0,
                 eval_avg_episode_step_baseline_rewards: float = 0.0,
                 eval_avg_2_episode_snort_critical_baseline_rewards: float = 0.0,
                 eval_avg_2_episode_var_log_baseline_rewards: float = 0.0,
                 eval_avg_2_episode_step_baseline_rewards: float = 0.0,
                 avg_episode_snort_severe_baseline_steps: float = 0.0,
                 avg_episode_snort_warning_baseline_steps: float = 0.0,
                 eval_avg_episode_snort_severe_baseline_steps: float = 0.0,
                 eval_avg_episode_snort_warning_baseline_steps: float = 0.0,
                 eval_avg_2_episode_snort_severe_baseline_steps: float = 0.0,
                 eval_avg_2_episode_snort_warning_baseline_steps: float = 0.0,
                 avg_episode_snort_critical_baseline_steps: float = 0.0,
                 avg_episode_var_log_baseline_steps: float = 0.0,
                 avg_episode_step_baseline_steps: float = 0.0,
                 eval_avg_episode_snort_critical_baseline_steps: float = 0.0,
                 eval_avg_episode_var_log_baseline_steps: float = 0.0,
                 eval_avg_episode_step_baseline_steps: float = 0.0,
                 eval_avg_2_episode_snort_critical_baseline_steps: float = 0.0,
                 eval_avg_2_episode_var_log_baseline_steps: float = 0.0,
                 eval_avg_2_episode_step_baseline_steps: float = 0.0,
                 avg_episode_snort_severe_baseline_caught_attacker: float = 0.0,
                 avg_episode_snort_warning_baseline_caught_attacker: float = 0.0,
                 eval_avg_episode_snort_severe_baseline_caught_attacker: float = 0.0,
                 eval_avg_episode_snort_warning_baseline_caught_attacker: float = 0.0,
                 eval_avg_2_episode_snort_severe_baseline_caught_attacker: float = 0.0,
                 eval_avg_2_episode_snort_warning_baseline_caught_attacker: float = 0.0,
                 avg_episode_snort_critical_baseline_caught_attacker: float = 0.0,
                 avg_episode_var_log_baseline_caught_attacker: float = 0.0,
                 avg_episode_step_baseline_caught_attacker: float = 0.0,
                 eval_avg_episode_snort_critical_baseline_caught_attacker: float = 0.0,
                 eval_avg_episode_var_log_baseline_caught_attacker: float = 0.0,
                 eval_avg_episode_step_baseline_caught_attacker: float = 0.0,
                 eval_avg_2_episode_snort_critical_baseline_caught_attacker: float = 0.0,
                 eval_avg_2_episode_var_log_baseline_caught_attacker: float = 0.0,
                 eval_avg_2_episode_step_baseline_caught_attacker: float = 0.0,
                 avg_episode_snort_severe_baseline_early_stopping: float = 0.0,
                 avg_episode_snort_warning_baseline_early_stopping: float = 0.0,
                 eval_avg_episode_snort_severe_baseline_early_stopping: float = 0.0,
                 eval_avg_episode_snort_warning_baseline_early_stopping: float = 0.0,
                 eval_avg_2_episode_snort_severe_baseline_early_stopping: float = 0.0,
                 eval_avg_2_episode_snort_warning_baseline_early_stopping: float = 0.0,
                 avg_episode_snort_critical_baseline_early_stopping: float = 0.0,
                 avg_episode_var_log_baseline_early_stopping: float = 0.0,
                 avg_episode_step_baseline_early_stopping: float = 0.0,
                 eval_avg_episode_snort_critical_baseline_early_stopping: float = 0.0,
                 eval_avg_episode_var_log_baseline_early_stopping: float = 0.0,
                 eval_avg_episode_step_baseline_early_stopping: float = 0.0,
                 eval_avg_2_episode_snort_critical_baseline_early_stopping: float = 0.0,
                 eval_avg_2_episode_var_log_baseline_early_stopping: float = 0.0,
                 eval_avg_2_episode_step_baseline_early_stopping: float = 0.0,
                 avg_episode_snort_severe_baseline_uncaught_intrusion_steps: float = 0.0,
                 avg_episode_snort_warning_baseline_uncaught_intrusion_steps: float = 0.0,
                 eval_avg_episode_snort_severe_baseline_uncaught_intrusion_steps: float = 0.0,
                 eval_avg_episode_snort_warning_baseline_uncaught_intrusion_steps: float = 0.0,
                 eval_avg_2_episode_snort_severe_baseline_uncaught_intrusion_steps: float = 0.0,
                 eval_avg_2_episode_snort_warning_baseline_uncaught_intrusion_steps: float = 0.0,
                 avg_episode_snort_critical_baseline_uncaught_intrusion_steps: float = 0.0,
                 avg_episode_var_log_baseline_uncaught_intrusion_steps: float = 0.0,
                 avg_episode_step_baseline_uncaught_intrusion_steps: float = 0.0,
                 eval_avg_episode_snort_critical_baseline_uncaught_intrusion_steps: float = 0.0,
                 eval_avg_episode_var_log_baseline_uncaught_intrusion_steps: float = 0.0,
                 eval_avg_episode_step_baseline_uncaught_intrusion_steps: float = 0.0,
                 eval_avg_2_episode_snort_critical_baseline_uncaught_intrusion_steps: float = 0.0,
                 eval_avg_2_episode_var_log_baseline_uncaught_intrusion_steps: float = 0.0,
                 eval_avg_2_episode_step_baseline_uncaught_intrusion_steps: float = 0.0,
                 avg_episode_intrusion_steps : float = 0.0,
                 eval_avg_episode_intrusion_steps: float = 0.0,
                 eval_2_avg_episode_intrusion_steps: float = 0.0,
                 avg_uncaught_intrusion_steps : float = 0.0,
                 eval_avg_uncaught_intrusion_steps: float = 0.0,
                 eval_2_avg_uncaught_intrusion_steps: float = 0.0,
                 avg_optimal_defender_reward: float = 0.0,
                 eval_avg_optimal_defender_reward: float = 0.0,
                 eval_2_avg_optimal_defender_reward: float = 0.0,
                 avg_defender_stops_remaining : float = 0.0,
                 eval_avg_defender_stops_remaining: float = 0.0,
                 eval_2_avg_defender_stops_remaining: float = 0.0,
                 avg_defender_first_stop_step: float = 0.0,
                 eval_avg_defender_first_stop_step: float = 0.0,
                 eval_2_avg_defender_first_stop_step: float = 0.0,
                 avg_defender_second_stop_step: float = 0.0,
                 eval_avg_defender_second_stop_step: float = 0.0,
                 eval_2_avg_defender_second_stop_step: float = 0.0,
                 avg_defender_third_stop_step: float = 0.0,
                 eval_avg_defender_third_stop_step: float = 0.0,
                 eval_2_avg_defender_third_stop_step: float = 0.0,
                 avg_defender_fourth_stop_step: float = 0.0,
                 eval_avg_defender_fourth_stop_step: float = 0.0,
                 eval_2_avg_defender_fourth_stop_step: float = 0.0
                 ):
        self.iteration = iteration
        self.avg_episode_rewards = avg_episode_rewards
        self.avg_episode_steps = avg_episode_steps
        self.avg_episode_loss = avg_episode_loss
        self.eps = eps
        self.lr = lr
        self.eval = eval
        self.avg_flags_catched = avg_flags_catched
        self.avg_episode_flags_percentage = avg_episode_flags_percentage
        self.eval_avg_episode_rewards = eval_avg_episode_rewards
        self.eval_avg_episode_steps = eval_avg_episode_steps
        self.eval_avg_episode_flags = eval_avg_episode_flags
        self.eval_avg_episode_flags_percentage = eval_avg_episode_flags_percentage
        self.eval_2_avg_episode_rewards = eval_2_avg_episode_rewards
        self.eval_2_avg_episode_steps = eval_2_avg_episode_steps
        self.eval_2_avg_episode_flags = eval_2_avg_episode_flags
        self.eval_2_avg_episode_flags_percentage = eval_2_avg_episode_flags_percentage
        self.rolling_avg_episode_rewards = rolling_avg_episode_rewards
        self.rolling_avg_episode_steps = rolling_avg_episode_steps
        self.tensorboard_writer = tensorboard_writer
        self.episode_caught_frac = episode_caught_frac
        self.episode_early_stopped_frac = episode_early_stopped_frac
        self.episode_successful_intrusion_frac = episode_successful_intrusion_frac
        self.eval_episode_caught_frac = eval_episode_caught_frac
        self.eval_episode_early_stopped_frac = eval_episode_early_stopped_frac
        self.eval_episode_successful_intrusion_frac = eval_episode_successful_intrusion_frac
        self.eval_2_episode_caught_frac = eval_2_episode_caught_frac
        self.eval_2_episode_early_stopped_frac = eval_2_episode_early_stopped_frac
        self.eval_2_episode_successful_intrusion_frac = eval_2_episode_successful_intrusion_frac
        self.avg_regret = avg_regret
        self.avg_opt_frac = avg_opt_frac
        self.rolling_avg_rewards = rolling_avg_rewards
        self.rolling_avg_steps = rolling_avg_steps
        self.avg_episode_flags = avg_episode_flags
        self.n_af = n_af
        self.n_d = n_d
        self.avg_episode_costs = avg_episode_costs
        self.avg_episode_costs_norm = avg_episode_costs_norm
        self.avg_episode_alerts = avg_episode_alerts
        self.avg_episode_alerts_norm = avg_episode_alerts_norm
        self.eval_avg_episode_costs = eval_avg_episode_costs
        self.eval_avg_episode_costs_norm = eval_avg_episode_costs_norm
        self.eval_avg_episode_alerts = eval_avg_episode_alerts
        self.eval_avg_episode_alerts_norm = eval_avg_episode_alerts_norm
        self.eval_2_avg_episode_costs = eval_2_avg_episode_costs
        self.eval_2_avg_episode_costs_norm = eval_2_avg_episode_costs_norm
        self.eval_2_avg_episode_alerts = eval_2_avg_episode_alerts
        self.eval_2_avg_episode_alerts_norm = eval_2_avg_episode_alerts_norm
        self.total_num_episodes = total_num_episodes
        self.avg_eval_regret = avg_eval_regret
        self.eval_avg_opt_frac = eval_avg_opt_frac
        self.avg_regret_2 = avg_regret_2
        self.avg_opt_frac_2 = avg_opt_frac_2
        self.epsilon = epsilon
        self.training_time_hours = training_time_hours
        self.avg_episode_snort_severe_baseline_rewards = avg_episode_snort_severe_baseline_rewards
        self.avg_episode_snort_warning_baseline_rewards = avg_episode_snort_warning_baseline_rewards
        self.eval_avg_episode_snort_severe_baseline_rewards = eval_avg_episode_snort_severe_baseline_rewards
        self.eval_avg_episode_snort_warning_baseline_rewards = eval_avg_episode_snort_warning_baseline_rewards
        self.eval_avg_2_episode_snort_severe_baseline_rewards = eval_avg_2_episode_snort_severe_baseline_rewards
        self.eval_avg_2_episode_snort_warning_baseline_rewards = eval_avg_2_episode_snort_warning_baseline_rewards
        self.avg_episode_snort_critical_baseline_rewards = avg_episode_snort_critical_baseline_rewards
        self.avg_episode_var_log_baseline_rewards = avg_episode_var_log_baseline_rewards
        self.avg_episode_step_baseline_rewards = avg_episode_step_baseline_rewards
        self.eval_avg_episode_snort_critical_baseline_rewards = eval_avg_episode_snort_critical_baseline_rewards
        self.eval_avg_episode_var_log_baseline_rewards = eval_avg_episode_var_log_baseline_rewards
        self.eval_avg_episode_step_baseline_rewards = eval_avg_episode_step_baseline_rewards
        self.eval_avg_2_episode_snort_critical_baseline_rewards = eval_avg_2_episode_snort_critical_baseline_rewards
        self.eval_avg_2_episode_var_log_baseline_rewards = eval_avg_2_episode_var_log_baseline_rewards
        self.eval_avg_2_episode_step_baseline_rewards = eval_avg_2_episode_step_baseline_rewards
        self.avg_episode_snort_severe_baseline_steps = avg_episode_snort_severe_baseline_steps
        self.avg_episode_snort_warning_baseline_steps = avg_episode_snort_warning_baseline_steps
        self.eval_avg_episode_snort_severe_baseline_steps = eval_avg_episode_snort_severe_baseline_steps
        self.eval_avg_episode_snort_warning_baseline_steps = eval_avg_episode_snort_warning_baseline_steps
        self.eval_avg_2_episode_snort_severe_baseline_steps = eval_avg_2_episode_snort_severe_baseline_steps
        self.eval_avg_2_episode_snort_warning_baseline_steps = eval_avg_2_episode_snort_warning_baseline_steps
        self.avg_episode_snort_critical_baseline_steps = avg_episode_snort_critical_baseline_steps
        self.avg_episode_var_log_baseline_steps = avg_episode_var_log_baseline_steps
        self.avg_episode_step_baseline_steps = avg_episode_step_baseline_steps
        self.eval_avg_episode_snort_critical_baseline_steps = eval_avg_episode_snort_critical_baseline_steps
        self.eval_avg_episode_var_log_baseline_steps = eval_avg_episode_var_log_baseline_steps
        self.eval_avg_episode_step_baseline_steps = eval_avg_episode_step_baseline_steps
        self.eval_avg_2_episode_snort_critical_baseline_steps = eval_avg_2_episode_snort_critical_baseline_steps
        self.eval_avg_2_episode_var_log_baseline_steps = eval_avg_2_episode_var_log_baseline_steps
        self.eval_avg_2_episode_step_baseline_steps = eval_avg_2_episode_step_baseline_steps
        self.avg_episode_snort_severe_baseline_caught_attacker = avg_episode_snort_severe_baseline_caught_attacker
        self.avg_episode_snort_warning_baseline_caught_attacker = avg_episode_snort_warning_baseline_caught_attacker
        self.eval_avg_episode_snort_severe_baseline_caught_attacker = eval_avg_episode_snort_severe_baseline_caught_attacker
        self.eval_avg_episode_snort_warning_baseline_caught_attacker = eval_avg_episode_snort_warning_baseline_caught_attacker
        self.eval_avg_2_episode_snort_severe_baseline_caught_attacker = eval_avg_2_episode_snort_severe_baseline_caught_attacker
        self.eval_avg_2_episode_snort_warning_baseline_caught_attacker = eval_avg_2_episode_snort_warning_baseline_caught_attacker
        self.avg_episode_snort_critical_baseline_caught_attacker = avg_episode_snort_critical_baseline_caught_attacker
        self.avg_episode_var_log_baseline_caught_attacker = avg_episode_var_log_baseline_caught_attacker
        self.avg_episode_step_baseline_caught_attacker = avg_episode_step_baseline_caught_attacker
        self.eval_avg_episode_snort_critical_baseline_caught_attacker = eval_avg_episode_snort_critical_baseline_caught_attacker
        self.eval_avg_episode_var_log_baseline_caught_attacker = eval_avg_episode_var_log_baseline_caught_attacker
        self.eval_avg_episode_step_baseline_caught_attacker = eval_avg_episode_step_baseline_caught_attacker
        self.eval_avg_2_episode_snort_critical_baseline_caught_attacker = eval_avg_2_episode_snort_critical_baseline_caught_attacker
        self.eval_avg_2_episode_var_log_baseline_caught_attacker = eval_avg_2_episode_var_log_baseline_caught_attacker
        self.eval_avg_2_episode_step_baseline_caught_attacker = eval_avg_2_episode_step_baseline_caught_attacker
        self.avg_episode_snort_severe_baseline_early_stopping = avg_episode_snort_severe_baseline_early_stopping
        self.avg_episode_snort_warning_baseline_early_stopping = avg_episode_snort_warning_baseline_early_stopping
        self.eval_avg_episode_snort_severe_baseline_early_stopping = eval_avg_episode_snort_severe_baseline_early_stopping
        self.eval_avg_episode_snort_warning_baseline_early_stopping = eval_avg_episode_snort_warning_baseline_early_stopping
        self.eval_avg_2_episode_snort_severe_baseline_early_stopping = eval_avg_2_episode_snort_severe_baseline_early_stopping
        self.eval_avg_2_episode_snort_warning_baseline_early_stopping = eval_avg_2_episode_snort_warning_baseline_early_stopping
        self.avg_episode_snort_critical_baseline_early_stopping = avg_episode_snort_critical_baseline_early_stopping
        self.avg_episode_var_log_baseline_early_stopping = avg_episode_var_log_baseline_early_stopping
        self.avg_episode_step_baseline_early_stopping = avg_episode_step_baseline_early_stopping
        self.eval_avg_episode_snort_critical_baseline_early_stopping = eval_avg_episode_snort_critical_baseline_early_stopping
        self.eval_avg_episode_var_log_baseline_early_stopping = eval_avg_episode_var_log_baseline_early_stopping
        self.eval_avg_episode_step_baseline_early_stopping = eval_avg_episode_step_baseline_early_stopping
        self.eval_avg_2_episode_snort_critical_baseline_early_stopping = eval_avg_2_episode_snort_critical_baseline_early_stopping
        self.eval_avg_2_episode_var_log_baseline_early_stopping = eval_avg_2_episode_var_log_baseline_early_stopping
        self.eval_avg_2_episode_step_baseline_early_stopping = eval_avg_2_episode_step_baseline_early_stopping
        self.avg_episode_snort_severe_baseline_uncaught_intrusion_steps = avg_episode_snort_severe_baseline_uncaught_intrusion_steps
        self.avg_episode_snort_warning_baseline_uncaught_intrusion_steps = avg_episode_snort_warning_baseline_uncaught_intrusion_steps
        self.eval_avg_episode_snort_severe_baseline_uncaught_intrusion_steps = eval_avg_episode_snort_severe_baseline_uncaught_intrusion_steps
        self.eval_avg_episode_snort_warning_baseline_uncaught_intrusion_steps = eval_avg_episode_snort_warning_baseline_uncaught_intrusion_steps
        self.eval_avg_2_episode_snort_severe_baseline_uncaught_intrusion_steps = eval_avg_2_episode_snort_severe_baseline_uncaught_intrusion_steps
        self.eval_avg_2_episode_snort_warning_baseline_uncaught_intrusion_steps = eval_avg_2_episode_snort_warning_baseline_uncaught_intrusion_steps
        self.avg_episode_snort_critical_baseline_uncaught_intrusion_steps = avg_episode_snort_critical_baseline_uncaught_intrusion_steps
        self.avg_episode_var_log_baseline_uncaught_intrusion_steps = avg_episode_var_log_baseline_uncaught_intrusion_steps
        self.avg_episode_step_baseline_uncaught_intrusion_steps = avg_episode_step_baseline_uncaught_intrusion_steps
        self.eval_avg_episode_snort_critical_baseline_uncaught_intrusion_steps = eval_avg_episode_snort_critical_baseline_uncaught_intrusion_steps
        self.eval_avg_episode_var_log_baseline_uncaught_intrusion_steps = eval_avg_episode_var_log_baseline_uncaught_intrusion_steps
        self.eval_avg_episode_step_baseline_uncaught_intrusion_steps = eval_avg_episode_step_baseline_uncaught_intrusion_steps
        self.eval_avg_2_episode_snort_critical_baseline_uncaught_intrusion_steps = eval_avg_2_episode_snort_critical_baseline_uncaught_intrusion_steps
        self.eval_avg_2_episode_var_log_baseline_uncaught_intrusion_steps = eval_avg_2_episode_var_log_baseline_uncaught_intrusion_steps
        self.eval_avg_2_episode_step_baseline_uncaught_intrusion_steps = eval_avg_2_episode_step_baseline_uncaught_intrusion_steps
        self.avg_episode_intrusion_steps = avg_episode_intrusion_steps
        self.eval_avg_episode_intrusion_steps = eval_avg_episode_intrusion_steps
        self.eval_2_avg_episode_intrusion_steps = eval_2_avg_episode_intrusion_steps
        self.avg_uncaught_intrusion_steps = avg_uncaught_intrusion_steps
        self.eval_avg_uncaught_intrusion_steps = eval_avg_uncaught_intrusion_steps
        self.eval_2_avg_uncaught_intrusion_steps = eval_2_avg_uncaught_intrusion_steps
        self.avg_optimal_defender_reward = avg_optimal_defender_reward
        self.eval_avg_optimal_defender_reward = eval_avg_optimal_defender_reward
        self.eval_2_avg_optimal_defender_reward = eval_2_avg_optimal_defender_reward
        self.avg_defender_stops_remaining = avg_defender_stops_remaining
        self.eval_avg_defender_stops_remaining = eval_avg_defender_stops_remaining
        self.eval_2_avg_defender_stops_remaining = eval_2_avg_defender_stops_remaining
        self.avg_defender_first_stop_step = avg_defender_first_stop_step
        self.eval_avg_defender_first_stop_step = eval_avg_defender_first_stop_step
        self.eval_2_avg_defender_first_stop_step = eval_2_avg_defender_first_stop_step
        self.avg_defender_second_stop_step = avg_defender_second_stop_step
        self.eval_avg_defender_second_stop_step = eval_avg_defender_second_stop_step
        self.eval_2_avg_defender_second_stop_step = eval_2_avg_defender_second_stop_step
        self.avg_defender_third_stop_step = avg_defender_third_stop_step
        self.eval_avg_defender_third_stop_step = eval_avg_defender_third_stop_step
        self.eval_2_avg_defender_third_stop_step = eval_2_avg_defender_third_stop_step
        self.avg_defender_fourth_stop_step = avg_defender_third_stop_step
        self.eval_avg_defender_fourth_stop_step = eval_avg_defender_fourth_stop_step
        self.eval_2_avg_defender_fourth_stop_step = eval_2_avg_defender_fourth_stop_step

    def log_tensorboard_defender(self) -> None:
        """
        Log metrics to tensorboard for defender

        :return: None
        """
        train_or_eval = "eval" if self.eval else "train"
        self.tensorboard_writer.add_scalar('defender/avg_episode_rewards/' + train_or_eval,
                                      self.avg_episode_rewards, self.iteration)
        self.tensorboard_writer.add_scalar('defender/rolling_avg_episode_rewards/' + train_or_eval,
                                      self.rolling_avg_episode_rewards, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_steps/' + train_or_eval, self.avg_episode_steps,
                                           self.iteration)
        self.tensorboard_writer.add_scalar('defender/rolling_avg_episode_steps/' + train_or_eval,
                                      self.rolling_avg_episode_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/episode_avg_loss/' + train_or_eval, self.avg_episode_loss,
                                           self.iteration)
        self.tensorboard_writer.add_scalar('defender/epsilon/' + train_or_eval, self.epsilon, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_rewards/' + train_or_eval,
                                      self.eval_avg_episode_rewards, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_steps/' + train_or_eval,
                                           self.eval_avg_episode_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_2_avg_episode_rewards/' + train_or_eval,
                                      self.eval_2_avg_episode_rewards, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_2_avg_episode_steps/' + train_or_eval,
                                      self.eval_2_avg_episode_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/episode_caught_frac/' + train_or_eval,
                                      self.episode_caught_frac, self.iteration)
        self.tensorboard_writer.add_scalar('defender/episode_early_stopped_frac/' + train_or_eval,
                                      self.episode_early_stopped_frac, self.iteration)
        self.tensorboard_writer.add_scalar('defender/episode_successful_intrusion_frac/' + train_or_eval,
                                      self.episode_successful_intrusion_frac, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_episode_caught_frac/' + train_or_eval,
                                      self.eval_episode_caught_frac, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_episode_early_stopped_frac/' + train_or_eval,
                                      self.eval_episode_early_stopped_frac, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_episode_successful_intrusion_frac/' + train_or_eval,
                                      self.eval_episode_successful_intrusion_frac, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_2_episode_caught_frac/' + train_or_eval,
                                      self.eval_2_episode_caught_frac, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_2_episode_early_stopped_frac/' + train_or_eval,
                                      self.eval_2_episode_early_stopped_frac, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_2_episode_successful_intrusion_frac/' + train_or_eval,
                                      self.eval_2_episode_successful_intrusion_frac, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_snort_severe_baseline_rewards/' + train_or_eval,
                                      self.avg_episode_snort_severe_baseline_rewards, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_snort_warning_baseline_rewards/' + train_or_eval,
                                      self.avg_episode_snort_warning_baseline_rewards, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_snort_severe_baseline_rewards/' + train_or_eval,
                                      self.eval_avg_episode_snort_severe_baseline_rewards, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_snort_warning_baseline_rewards/' + train_or_eval,
                                      self.eval_avg_episode_snort_warning_baseline_rewards, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_2_episode_snort_severe_baseline_rewards/' + train_or_eval,
                                      self.eval_avg_2_episode_snort_severe_baseline_rewards, self.iteration)
        self.tensorboard_writer.add_scalar(
            'defender/eval_avg_2_episode_snort_warning_baseline_rewards/' + train_or_eval,
            self.eval_avg_2_episode_snort_warning_baseline_rewards, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_snort_critical_baseline_rewards/' + train_or_eval,
                                      self.avg_episode_snort_critical_baseline_rewards, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_var_log_baseline_rewards/' + train_or_eval,
                                      self.avg_episode_var_log_baseline_rewards, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_step_baseline_rewards/' + train_or_eval,
                                           self.avg_episode_step_baseline_rewards, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_snort_critical_baseline_rewards/' + train_or_eval,
                                      self.eval_avg_episode_snort_critical_baseline_rewards, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_var_log_baseline_rewards/' + train_or_eval,
                                      self.eval_avg_episode_var_log_baseline_rewards, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_step_baseline_rewards/' + train_or_eval,
                                           self.eval_avg_episode_step_baseline_rewards, self.iteration)
        self.tensorboard_writer.add_scalar(
            'defender/eval_avg_2_episode_snort_critical_baseline_rewards/' + train_or_eval,
            self.eval_avg_2_episode_snort_critical_baseline_rewards, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_2_episode_var_log_baseline_rewards/' + train_or_eval,
                                      self.eval_avg_2_episode_var_log_baseline_rewards, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_2_episode_step_baseline_rewards/' + train_or_eval,
                                           self.eval_avg_2_episode_step_baseline_rewards, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_snort_severe_baseline_steps/' + train_or_eval,
                                           self.avg_episode_snort_severe_baseline_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_snort_warning_baseline_steps/' + train_or_eval,
                                           self.avg_episode_snort_warning_baseline_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_snort_severe_baseline_steps/' + train_or_eval,
                                           self.eval_avg_episode_snort_severe_baseline_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_snort_warning_baseline_steps/' + train_or_eval,
                                           self.eval_avg_episode_snort_warning_baseline_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_2_episode_snort_severe_baseline_steps/' + train_or_eval,
                                           self.eval_avg_2_episode_snort_severe_baseline_steps, self.iteration)
        self.tensorboard_writer.add_scalar(
            'defender/eval_avg_2_episode_snort_warning_baseline_steps/' + train_or_eval,
            self.eval_avg_2_episode_snort_warning_baseline_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_snort_critical_baseline_steps/' + train_or_eval,
                                           self.avg_episode_snort_critical_baseline_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_var_log_baseline_steps/' + train_or_eval,
                                           self.avg_episode_var_log_baseline_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_step_baseline_steps/' + train_or_eval,
                                           self.avg_episode_step_baseline_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_snort_critical_baseline_steps/' + train_or_eval,
                                           self.eval_avg_episode_snort_critical_baseline_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_var_log_baseline_steps/' + train_or_eval,
                                           self.eval_avg_episode_var_log_baseline_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_step_baseline_steps/' + train_or_eval,
                                           self.eval_avg_episode_step_baseline_steps, self.iteration)
        self.tensorboard_writer.add_scalar(
            'defender/eval_avg_2_episode_snort_critical_baseline_steps/' + train_or_eval,
            self.eval_avg_2_episode_snort_critical_baseline_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_2_episode_var_log_baseline_steps/' + train_or_eval,
                                           self.eval_avg_2_episode_var_log_baseline_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_2_episode_step_baseline_steps/' + train_or_eval,
                                           self.eval_avg_2_episode_step_baseline_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_snort_severe_baseline_caught_attacker/' + train_or_eval,
                                           self.avg_episode_snort_severe_baseline_caught_attacker, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_snort_warning_baseline_caught_attacker/' + train_or_eval,
                                           self.avg_episode_snort_warning_baseline_caught_attacker, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_snort_severe_baseline_caught_attacker/' + train_or_eval,
                                           self.eval_avg_episode_snort_severe_baseline_caught_attacker, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_snort_warning_baseline_caught_attacker/' + train_or_eval,
                                           self.eval_avg_episode_snort_warning_baseline_caught_attacker, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_2_episode_snort_severe_baseline_caught_attacker/' + train_or_eval,
                                           self.eval_avg_2_episode_snort_severe_baseline_caught_attacker, self.iteration)
        self.tensorboard_writer.add_scalar(
            'defender/eval_avg_2_episode_snort_warning_baseline_caught_attacker/' + train_or_eval,
            self.eval_avg_2_episode_snort_warning_baseline_caught_attacker, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_snort_critical_baseline_caught_attacker/' + train_or_eval,
                                           self.avg_episode_snort_critical_baseline_caught_attacker, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_var_log_baseline_caught_attacker/' + train_or_eval,
                                           self.avg_episode_var_log_baseline_caught_attacker, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_step_baseline_caught_attacker/' + train_or_eval,
                                           self.avg_episode_step_baseline_caught_attacker, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_snort_critical_baseline_caught_attacker/' + train_or_eval,
                                           self.eval_avg_episode_snort_critical_baseline_caught_attacker, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_var_log_baseline_caught_attacker/' + train_or_eval,
                                           self.eval_avg_episode_var_log_baseline_caught_attacker, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_step_baseline_caught_attacker/' + train_or_eval,
                                           self.eval_avg_episode_step_baseline_caught_attacker, self.iteration)
        self.tensorboard_writer.add_scalar(
            'defender/eval_avg_2_episode_snort_critical_baseline_caught_attacker/' + train_or_eval,
            self.eval_avg_2_episode_snort_critical_baseline_caught_attacker, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_2_episode_var_log_baseline_caught_attacker/' + train_or_eval,
                                           self.eval_avg_2_episode_var_log_baseline_caught_attacker, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_2_episode_step_baseline_caught_attacker/' + train_or_eval,
                                           self.eval_avg_2_episode_step_baseline_caught_attacker, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_snort_severe_baseline_early_stopping/' + train_or_eval,
                                           self.avg_episode_snort_severe_baseline_early_stopping, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_snort_warning_baseline_early_stopping/' + train_or_eval,
                                           self.avg_episode_snort_warning_baseline_early_stopping, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_snort_severe_baseline_early_stopping/' + train_or_eval,
                                           self.eval_avg_episode_snort_severe_baseline_early_stopping, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_snort_warning_baseline_early_stopping/' + train_or_eval,
                                           self.eval_avg_episode_snort_warning_baseline_early_stopping, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_2_episode_snort_severe_baseline_early_stopping/' + train_or_eval,
                                           self.eval_avg_2_episode_snort_severe_baseline_early_stopping, self.iteration)
        self.tensorboard_writer.add_scalar(
            'defender/eval_avg_2_episode_snort_warning_baseline_early_stopping/' + train_or_eval,
            self.eval_avg_2_episode_snort_warning_baseline_early_stopping, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_snort_critical_baseline_early_stopping/' + train_or_eval,
                                           self.avg_episode_snort_critical_baseline_early_stopping, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_var_log_baseline_early_stopping/' + train_or_eval,
                                           self.avg_episode_var_log_baseline_early_stopping, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_step_baseline_early_stopping/' + train_or_eval,
                                           self.avg_episode_step_baseline_early_stopping, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_snort_critical_baseline_early_stopping/' + train_or_eval,
                                           self.eval_avg_episode_snort_critical_baseline_early_stopping, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_var_log_baseline_early_stopping/' + train_or_eval,
                                           self.eval_avg_episode_var_log_baseline_early_stopping, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_step_baseline_early_stopping/' + train_or_eval,
                                           self.eval_avg_episode_step_baseline_early_stopping, self.iteration)
        self.tensorboard_writer.add_scalar(
            'defender/eval_avg_2_episode_snort_critical_baseline_early_stopping/' + train_or_eval,
            self.eval_avg_2_episode_snort_critical_baseline_early_stopping, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_2_episode_var_log_baseline_early_stopping/' + train_or_eval,
                                           self.eval_avg_2_episode_var_log_baseline_early_stopping, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_2_episode_step_baseline_early_stopping/' + train_or_eval,
                                           self.eval_avg_2_episode_step_baseline_early_stopping, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_snort_severe_baseline_uncaught_intrusion_steps/' + train_or_eval,
                                           self.avg_episode_snort_severe_baseline_uncaught_intrusion_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_snort_warning_baseline_uncaught_intrusion_steps/' + train_or_eval,
                                           self.avg_episode_snort_warning_baseline_uncaught_intrusion_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_snort_severe_baseline_uncaught_intrusion_steps/' + train_or_eval,
                                           self.eval_avg_episode_snort_severe_baseline_uncaught_intrusion_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_snort_warning_baseline_uncaught_intrusion_steps/' + train_or_eval,
                                           self.eval_avg_episode_snort_warning_baseline_uncaught_intrusion_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_2_episode_snort_severe_baseline_uncaught_intrusion_steps/' + train_or_eval,
                                           self.eval_avg_2_episode_snort_severe_baseline_uncaught_intrusion_steps, self.iteration)
        self.tensorboard_writer.add_scalar(
            'defender/eval_avg_2_episode_snort_warning_baseline_uncaught_intrusion_steps/' + train_or_eval,
            self.eval_avg_2_episode_snort_warning_baseline_uncaught_intrusion_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_snort_critical_baseline_uncaught_intrusion_steps/' + train_or_eval,
                                           self.avg_episode_snort_critical_baseline_uncaught_intrusion_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_var_log_baseline_uncaught_intrusion_steps/' + train_or_eval,
                                           self.avg_episode_var_log_baseline_uncaught_intrusion_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_step_baseline_uncaught_intrusion_steps/' + train_or_eval,
                                           self.avg_episode_step_baseline_uncaught_intrusion_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_snort_critical_baseline_uncaught_intrusion_steps/' + train_or_eval,
                                           self.eval_avg_episode_snort_critical_baseline_uncaught_intrusion_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_var_log_baseline_uncaught_intrusion_steps/' + train_or_eval,
                                           self.eval_avg_episode_var_log_baseline_uncaught_intrusion_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_step_baseline_uncaught_intrusion_steps/' + train_or_eval,
                                           self.eval_avg_episode_step_baseline_uncaught_intrusion_steps, self.iteration)
        self.tensorboard_writer.add_scalar(
            'defender/eval_avg_2_episode_snort_critical_baseline_uncaught_intrusion_steps/' + train_or_eval,
            self.eval_avg_2_episode_snort_critical_baseline_uncaught_intrusion_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_2_episode_var_log_baseline_uncaught_intrusion_steps/' + train_or_eval,
                                           self.eval_avg_2_episode_var_log_baseline_uncaught_intrusion_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_2_episode_step_baseline_uncaught_intrusion_steps/' + train_or_eval,
                                           self.eval_avg_2_episode_step_baseline_uncaught_intrusion_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_episode_intrusion_steps/' + train_or_eval,
                                           self.avg_episode_intrusion_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_episode_intrusion_steps/' + train_or_eval,
                                           self.eval_avg_episode_intrusion_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_2_avg_episode_intrusion_steps/' + train_or_eval,
                                           self.eval_2_avg_episode_intrusion_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_uncaught_intrusion_steps/' + train_or_eval,
                                           self.avg_uncaught_intrusion_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_uncaught_intrusion_steps/' + train_or_eval,
                                           self.eval_avg_uncaught_intrusion_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_2_avg_uncaught_intrusion_steps/' + train_or_eval,
                                           self.eval_2_avg_uncaught_intrusion_steps, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_optimal_defender_reward/' + train_or_eval,
                                           self.avg_optimal_defender_reward, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_optimal_defender_reward/' + train_or_eval,
                                           self.eval_avg_optimal_defender_reward, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_2_avg_optimal_defender_reward/' + train_or_eval,
                                           self.eval_2_avg_optimal_defender_reward, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_defender_stops_remaining/' + train_or_eval,
                                           self.avg_defender_stops_remaining, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_defender_stops_remaining/' + train_or_eval,
                                           self.eval_avg_defender_stops_remaining, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_2_avg_defender_stops_remaining/' + train_or_eval,
                                           self.eval_2_avg_defender_stops_remaining, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_defender_first_stop_step/' + train_or_eval,
                                           self.avg_defender_first_stop_step, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_defender_first_stop_step/' + train_or_eval,
                                           self.eval_avg_defender_first_stop_step, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_2_avg_defender_first_stop_step/' + train_or_eval,
                                           self.eval_2_avg_defender_first_stop_step, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_defender_second_stop_step/' + train_or_eval,
                                           self.avg_defender_second_stop_step, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_defender_second_stop_step/' + train_or_eval,
                                           self.eval_avg_defender_second_stop_step, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_2_avg_defender_second_stop_step/' + train_or_eval,
                                           self.eval_2_avg_defender_second_stop_step, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_defender_third_stop_step/' + train_or_eval,
                                           self.avg_defender_third_stop_step, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_defender_third_stop_step/' + train_or_eval,
                                           self.eval_avg_defender_third_stop_step, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_2_avg_defender_third_stop_step/' + train_or_eval,
                                           self.eval_2_avg_defender_third_stop_step, self.iteration)
        self.tensorboard_writer.add_scalar('defender/avg_defender_fourth_stop_step/' + train_or_eval,
                                           self.avg_defender_fourth_stop_step, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_avg_defender_fourth_stop_step/' + train_or_eval,
                                           self.eval_avg_defender_fourth_stop_step, self.iteration)
        self.tensorboard_writer.add_scalar('defender/eval_2_avg_defender_fourth_stop_step/' + train_or_eval,
                                           self.eval_2_avg_defender_fourth_stop_step, self.iteration)
        if not eval:
            self.tensorboard_writer.add_scalar('defender/lr', self.lr, self.iteration)


    def log_str_attacker(self) -> str:
        """
        :return: a string representation of the DTO for the attacker
        """
        if self.eval:
            log_str = f"[Eval A] iter:{self.iteration},Avg_Reg:{self.avg_regret:.2f},Opt_frac:{self.avg_opt_frac:.2f}," \
                      f"avg_R:{self.avg_episode_rewards:.2f},rolling_avg_R:{self.rolling_avg_rewards:.2f}," \
                      f"avg_t:{self.avg_episode_steps:.2f},rolling_avg_t:{self.rolling_avg_steps:.2f}," \
                      f"lr:{self.lr:.2E},avg_F:{self.avg_episode_flags:.2f}," \
                      f"avg_F%:{self.avg_episode_flags_percentage:.2f}," \
                      f"n_af:{self.n_af},n_d:{self.n_d}," \
                      f"c:{self.episode_caught_frac:.2f},s:{self.episode_early_stopped_frac:.2f}," \
                      f"s_i:{self.episode_successful_intrusion_frac:.2f}," \
                      f"costs:{self.avg_episode_costs:.2f},costs_N:{self.avg_episode_costs_norm:.2f}," \
                      f"alerts:{self.avg_episode_alerts:.2f}," \
                      f"alerts_N:{self.avg_episode_alerts_norm:.2f}"
        else:
            log_str = f"[Train A] iter:{self.iteration:.2f},avg_reg_T:{self.avg_regret:.2f}," \
                      f"opt_frac_T:{self.avg_opt_frac:.2f},avg_R_T:{self.avg_episode_rewards:.2f}," \
                      f"rolling_avg_R_T:{self.rolling_avg_rewards:.2f}," \
                      f"avg_t_T:{self.avg_episode_steps:.2f},rolling_avg_t_T:{self.rolling_avg_steps:.2f}," \
                      f"loss:{self.avg_episode_loss:.6f},lr:{self.lr:.2E},episode:{self.total_num_episodes}," \
                      f"avg_F_T:{self.avg_episode_flags:.2f},avg_F_T%:{self.avg_episode_flags_percentage:.2f}," \
                      f"eps:{self.eps:.2f}," \
                      f"n_af:{self.n_af},n_d:{self.n_d},avg_R_E:{self.eval_avg_episode_rewards:.2f}," \
                      f"avg_reg_E:{self.avg_eval_regret:.2f},avg_opt_frac_E:{self.eval_avg_opt_frac:.2f}," \
                      f"avg_t_E:{self.eval_avg_episode_steps:.2f},avg_F_E:{self.eval_avg_episode_flags:.2f}," \
                      f"avg_F_E%:{self.eval_avg_episode_flags_percentage:.2f}," \
                      f"avg_R_E2:{self.eval_2_avg_episode_rewards:.2f},Avg_Reg_E2:{self.avg_regret_2:.2f}," \
                      f"Opt_frac_E2:{self.avg_opt_frac_2:.2f},avg_t_E2:{self.eval_2_avg_episode_steps:.2f}," \
                      f"avg_F_E2:{self.eval_2_avg_episode_flags:.2f}," \
                      f"avg_F_E2%:{self.eval_2_avg_episode_flags_percentage:.2f},epsilon:{self.epsilon:.2f}," \
                      f"c:{self.episode_caught_frac:.2f},s:{self.episode_early_stopped_frac:.2f}," \
                      f"s_i:{self.episode_successful_intrusion_frac:.2f}," \
                      f"c_E:{self.eval_episode_caught_frac:.2f},es_E:{self.eval_episode_early_stopped_frac:.2f}," \
                      f"s_i_E:{self.eval_episode_successful_intrusion_frac:.2f}," \
                      f"c_E2:{self.eval_2_episode_caught_frac:.2f},es_E2:{self.eval_2_episode_early_stopped_frac:.2f}," \
                      f"s_i_E:{self.eval_2_episode_successful_intrusion_frac:.2f},costs:{self.avg_episode_costs:.2f}," \
                      f"costs_N:{self.avg_episode_costs_norm:.2f},alerts:{self.avg_episode_alerts:.2f}," \
                      f"alerts_N:{self.avg_episode_alerts_norm:.2f},E_costs:{self.eval_avg_episode_costs:.2f}," \
                      f"E_costs_N:{self.eval_avg_episode_costs_norm:.2f},E_alerts:{self.eval_avg_episode_alerts:.2f}," \
                      f"E_alerts_N:{self.eval_avg_episode_alerts_norm:.2f}," \
                      f"E2_costs:{self.eval_2_avg_episode_costs:.2f},E2_costs_N:{self.eval_2_avg_episode_costs_norm:.2f}," \
                      f"E2_alerts:{self.eval_2_avg_episode_alerts:.2f}," \
                      f"E2_alerts_N:{self.eval_2_avg_episode_alerts_norm:.2f}," \
                      f"tt_h:{self.training_time_hours:.2f},avg_F_T_E:{self.eval_2_avg_episode_flags:.2f}," \
                      f"avg_F_T_E%:{self.eval_2_avg_episode_flags_percentage:.2f}"
        return log_str

    def log_str_defender(self) -> str:
        """
        :return: a string representation of the DTO for the attacker
        """
        if self.eval:
            log_str = f"[Eval D] iter:{self.iteration},avg_R:{self.avg_episode_rewards:.2f}," \
                      f"rolling_avg_R:{self.rolling_avg_rewards:.2f}," \
                      f"avg_uit:{self.avg_uncaught_intrusion_steps:.2f}," \
                      f"avg_opt_R_T:{self.avg_optimal_defender_reward:.2f}," \
                      f"S_sev_avg_R:{self.avg_episode_snort_severe_baseline_rewards:.2f}," \
                      f"S_warn_avg_R:{self.avg_episode_snort_warning_baseline_rewards:.2f}," \
                      f"S_crit_avg_R:{self.avg_episode_snort_critical_baseline_rewards:.2f}," \
                      f"V_log_avg_R:{self.avg_episode_snort_critical_baseline_rewards:.2f}, " \
                      f"step_avg_R:{self.avg_episode_step_baseline_rewards:.2f}," \
                      f"S_sev_avg_t:{self.avg_episode_snort_severe_baseline_steps:.2f}," \
                      f"S_warn_avg_t:{self.avg_episode_snort_warning_baseline_steps:.2f}," \
                      f"S_crit_avg_t:{self.avg_episode_snort_critical_baseline_steps:.2f}," \
                      f"V_log_avg_t:{self.avg_episode_var_log_baseline_steps:.2f}, " \
                      f"step_avg_t:{self.avg_episode_step_baseline_steps:.2f}," \
                      f"S_sev_avg_ca:{self.avg_episode_snort_severe_baseline_caught_attacker:.2f}," \
                      f"S_warn_avg_ca:{self.avg_episode_snort_warning_baseline_caught_attacker:.2f}," \
                      f"S_crit_avg_ca:{self.avg_episode_snort_critical_baseline_caught_attacker:.2f}," \
                      f"V_log_avg_ca:{self.avg_episode_var_log_baseline_caught_attacker:.2f}, " \
                      f"step_avg_ca:{self.avg_episode_step_baseline_caught_attacker:.2f}," \
                      f"S_sev_avg_es:{self.avg_episode_snort_severe_baseline_early_stopping:.2f}," \
                      f"S_warn_avg_e:{self.avg_episode_snort_warning_baseline_early_stopping:.2f}," \
                      f"S_crit_avg_es:{self.avg_episode_snort_critical_baseline_early_stopping:.2f}," \
                      f"V_log_avg_es:{self.avg_episode_var_log_baseline_early_stopping:.2f}, " \
                      f"step_avg_es:{self.avg_episode_step_baseline_early_stopping:.2f}," \
                      f"S_sev_avg_uit:{self.avg_episode_snort_severe_baseline_uncaught_intrusion_steps:.2f}," \
                      f"S_warn_avg_uit:{self.avg_episode_snort_warning_baseline_uncaught_intrusion_steps:.2f}," \
                      f"S_crit_avg_uit:{self.avg_episode_snort_critical_baseline_uncaught_intrusion_steps:.2f}," \
                      f"V_log_avg_uit:{self.avg_episode_var_log_baseline_uncaught_intrusion_steps:.2f}, " \
                      f"step_avg_uit:{self.avg_episode_step_baseline_uncaught_intrusion_steps:.2f}," \
                      f"avg_t:{self.avg_episode_steps:.2f},rolling_avg_t:{self.rolling_avg_steps:.2f}," \
                      f"lr:{self.lr:.2E}," \
                      f"c:{self.episode_caught_frac:.2f},es:{self.episode_early_stopped_frac:.2f}," \
                      f"s_i:{self.episode_successful_intrusion_frac:.2f},avg_I_t:{self.avg_episode_intrusion_steps:.2f}, " \
                      f"avg_stops_left_T:{self.avg_defender_stops_remaining:.2f}," \
                      f"avg_first_stop_t_T:{self.avg_defender_first_stop_step:.2f}," \
                      f"avg_second_stop_t_T:{self.avg_defender_second_stop_step:.2f}," \
                      f"avg_third_stop_t_T:{self.avg_defender_third_stop_step:.2f}," \
                      f"avg_fourth_stop_t_T:{self.avg_defender_fourth_stop_step:.2f}"
        else:
            log_str = f"[Train D] iter:{self.iteration},avg_reg_T:{self.avg_regret:.2f},opt_frac_T:{self.avg_opt_frac:.2f}," \
                      f"avg_R_T:{self.avg_episode_rewards:.2f},rolling_avg_R_T:{self.rolling_avg_rewards:.2f}," \
                      f"avg_uit_T:{self.avg_uncaught_intrusion_steps:.2f}," \
                      f"avg_opt_R_T:{self.avg_optimal_defender_reward:.2f}," \
                      f"S_sev_avg_R_T:{self.avg_episode_snort_severe_baseline_rewards:.2f}," \
                      f"S_warn_avg_R_T:{self.avg_episode_snort_warning_baseline_rewards:.2f}," \
                      f"S_crit_avg_R_T:{self.avg_episode_snort_critical_baseline_rewards:.2f}," \
                      f"V_log_avg_R_T:{self.avg_episode_var_log_baseline_rewards:.2f}," \
                      f"step_avg_R_T:{self.avg_episode_step_baseline_rewards:.2f}, " \
                      f"S_sev_avg_t_T:{self.avg_episode_snort_severe_baseline_steps:.2f}," \
                      f"S_warn_avg_t_T:{self.avg_episode_snort_warning_baseline_steps:.2f}, " \
                      f"S_crit_avg_t_T:{self.avg_episode_snort_critical_baseline_steps:.2f}," \
                      f"V_log_avg_t_T:{self.avg_episode_var_log_baseline_steps:.2f}, " \
                      f"step_avg_t_T:{self.avg_episode_step_baseline_steps:.2f}," \
                      f"S_sev_avg_ca_T:{self.avg_episode_snort_severe_baseline_caught_attacker:.2f}," \
                      f"S_warn_avg_ca_T:{ self.avg_episode_snort_warning_baseline_caught_attacker:.2f}, " \
                      f"S_crit_avg_ca_T:{self.avg_episode_snort_critical_baseline_caught_attacker:.2f}," \
                      f"V_log_avg_ca_T:{self.avg_episode_var_log_baseline_caught_attacker:.2f}, " \
                      f"step_avg_ca_T:{self.avg_episode_step_baseline_caught_attacker:.2f}," \
                      f"S_sev_avg_es_T:{self.avg_episode_snort_severe_baseline_early_stopping:.2f}," \
                      f"S_warn_avg_es_T:{self.avg_episode_snort_warning_baseline_early_stopping:.2f}, " \
                      f"S_crit_avg_es_T:{self.avg_episode_snort_critical_baseline_early_stopping:.2f}," \
                      f"V_log_avg_es_T:{self.avg_episode_var_log_baseline_early_stopping:.2f}, " \
                      f"step_avg_es_T:{self.avg_episode_step_baseline_early_stopping:.2f}," \
                      f"S_sev_avg_uit_T:{self.avg_episode_snort_severe_baseline_uncaught_intrusion_steps:.2f}," \
                      f"S_warn_avg_uit_T:{self.avg_episode_snort_warning_baseline_uncaught_intrusion_steps:.2f}, " \
                      f"S_crit_avg_uit_T:{self.avg_episode_snort_critical_baseline_uncaught_intrusion_steps:.2f}," \
                      f"V_log_avg_uit_T:{self.avg_episode_var_log_baseline_uncaught_intrusion_steps:.2f}," \
                      f"step_avg_uit_T:{self.avg_episode_step_baseline_uncaught_intrusion_steps:.2f}," \
                      f"avg_t_T:{self.avg_episode_steps:.2f}," \
                      f"rolling_avg_t_T:{self.rolling_avg_steps:.2f}," \
                      f"loss:{self.avg_episode_loss:.6f}," \
                      f"lr:{self.lr:.2E}," \
                      f"episode:{self.total_num_episodes}," \
                      f"avg_stops_left_T:{self.avg_defender_stops_remaining:.2f}," \
                      f"avg_first_stop_t_T:{self.avg_defender_first_stop_step:.2f}," \
                      f"avg_second_stop_t_T:{self.avg_defender_second_stop_step:.2f}," \
                      f"avg_third_stop_t_T:{self.avg_defender_third_stop_step:.2f}," \
                      f"avg_fourth_stop_t_T:{self.avg_defender_fourth_stop_step:.2f},eps:{self.eps:.2f}," \
                      f"avg_R_E:{self.eval_avg_episode_rewards:.2f}," \
                      f"avg_uit_E:{self.eval_avg_uncaught_intrusion_steps:.2f}," \
                      f"opt_R_E:{self.eval_avg_optimal_defender_reward:.2f}," \
                      f"S_sev_avg_R_E:{self.eval_avg_episode_snort_severe_baseline_rewards:.2f}," \
                      f"S_warn_avg_R_E:{self.eval_avg_episode_snort_warning_baseline_rewards:.2f}," \
                      f"S_crit_avg_R_E:{self.eval_avg_episode_snort_critical_baseline_rewards:.2f}," \
                      f"V_log_avg_R_E:{self.eval_avg_episode_var_log_baseline_rewards:.2f}, " \
                      f"step_avg_R_E:{self.eval_avg_episode_step_baseline_rewards:.2f}," \
                      f"S_sev_avg_t_E:{self.eval_avg_episode_snort_severe_baseline_steps:.2f}," \
                      f"S_warn_avg_t_E:{self.eval_avg_episode_snort_warning_baseline_steps:.2f}, " \
                      f"S_crit_avg_t_E:{self.eval_avg_episode_snort_critical_baseline_steps:.2f}," \
                      f"V_log_avg_t_E:{self.eval_avg_episode_var_log_baseline_steps:.2f}, " \
                      f"step_avg_t_E:{self.eval_avg_episode_step_baseline_steps:.2f}," \
                      f"S_sev_avg_ca_E:{self.eval_avg_episode_snort_severe_baseline_caught_attacker:.2f}," \
                      f"S_warn_avg_ca_E:{self.eval_avg_episode_snort_warning_baseline_caught_attacker:.2f}, " \
                      f"S_crit_avg_ca_E:{self.eval_avg_episode_snort_critical_baseline_caught_attacker:.2f}," \
                      f"V_log_avg_ca_E:{self.eval_avg_episode_var_log_baseline_caught_attacker:.2f}, " \
                      f"step_avg_ca_E:{self.eval_avg_episode_step_baseline_caught_attacker:.2f}," \
                      f"S_sev_avg_es_E:{self.eval_avg_episode_snort_severe_baseline_early_stopping:.2f}," \
                      f"S_warn_avg_es_E:{self.eval_avg_episode_snort_warning_baseline_early_stopping:.2f}, " \
                      f"S_crit_avg_es_E:{self.eval_avg_episode_snort_critical_baseline_early_stopping:.2f}," \
                      f"V_log_avg_es_E:{self.eval_avg_episode_var_log_baseline_early_stopping:.2f}, " \
                      f"step_avg_es_E:{self.eval_avg_episode_step_baseline_early_stopping:.2f}," \
                      f"S_sev_avg_uit_E:{self.eval_avg_episode_snort_severe_baseline_uncaught_intrusion_steps:.2f}," \
                      f"S_warn_avg_uit_E:{self.eval_avg_episode_snort_warning_baseline_uncaught_intrusion_steps:.2f}, " \
                      f"S_crit_avg_uit_E:{self.eval_avg_episode_snort_critical_baseline_uncaught_intrusion_steps:.2f}," \
                      f"V_log_avg_uit_E:{self.eval_avg_episode_var_log_baseline_uncaught_intrusion_steps:.2f}, " \
                      f"step_avg_uit_E:{self.eval_avg_episode_step_baseline_uncaught_intrusion_steps:.2f}," \
                      f"avg_reg_E:{self.avg_eval_regret:.2f},avg_opt_frac_E:{self.eval_avg_opt_frac:.2f}," \
                      f"avg_t_E:{self.eval_avg_episode_steps:.2f}," \
                      f"avg_stops_left_E:{self.eval_avg_defender_stops_remaining:.2f}," \
                      f"avg_first_stop_t_E:{self.eval_avg_defender_first_stop_step:.2f}," \
                      f"avg_second_stop_t_E:{self.eval_avg_defender_second_stop_step:.2f}," \
                      f"avg_third_stop_t_E:{self.eval_avg_defender_third_stop_step:.2f}," \
                      f"avg_fourth_stop_t_E:{self.eval_avg_defender_fourth_stop_step:.2f}," \
                      f"avg_R_E2:{self.eval_2_avg_episode_rewards:.2f}," \
                      f"avg_uit_E2:{self.eval_2_avg_uncaught_intrusion_steps:.2f}," \
                      f"opt_R_E2:{self.eval_2_avg_optimal_defender_reward:.2f}," \
                      f"S_sev_avg_R_E2:{self.eval_avg_2_episode_snort_severe_baseline_rewards:.2f}," \
                      f"S_warn_avg_R_E2:{self.eval_avg_2_episode_snort_warning_baseline_rewards:.2f}," \
                      f"S_crit_avg_R_E2:{self.eval_avg_2_episode_snort_critical_baseline_rewards:.2f}," \
                      f"V_log_avg_R_E2:{self.eval_avg_2_episode_var_log_baseline_rewards:.2f}," \
                      f"step_avg_R_E2:{self.eval_avg_2_episode_step_baseline_rewards:.2f}," \
                      f"S_sev_avg_t_E2:{self.eval_avg_2_episode_snort_severe_baseline_steps:.2f}," \
                      f"S_warn_avg_t_E2:{self.eval_avg_2_episode_snort_warning_baseline_steps:.2f}," \
                      f"S_crit_avg_t_E2:{self.eval_avg_2_episode_snort_critical_baseline_steps:.2f}," \
                      f"V_log_avg_t_E2:{self.eval_avg_2_episode_var_log_baseline_steps:.2f}," \
                      f"step_avg_t_E2:{self.eval_avg_2_episode_step_baseline_steps:.2f}," \
                      f"S_sev_avg_ca_E2:{self.eval_avg_2_episode_snort_severe_baseline_caught_attacker:.2f}," \
                      f"S_warn_avg_ca_E2:{self.eval_avg_2_episode_snort_warning_baseline_caught_attacker:.2f}, " \
                      f"S_crit_avg_ca_E2:{self.eval_avg_2_episode_snort_critical_baseline_caught_attacker:.2f}," \
                      f"V_log_avg_ca_E2:{self.eval_avg_2_episode_var_log_baseline_caught_attacker:.2f}, " \
                      f"step_avg_ca_E2:{self.eval_avg_2_episode_step_baseline_caught_attacker:.2f}," \
                      f"S_sev_avg_es_E2:{self.eval_avg_2_episode_snort_severe_baseline_early_stopping:.2f}," \
                      f"S_warn_avg_es_E2:{self.eval_avg_2_episode_snort_warning_baseline_early_stopping:.2f}, " \
                      f"S_crit_avg_es_E2:{self.eval_avg_2_episode_snort_critical_baseline_early_stopping:.2f}," \
                      f"V_log_avg_es_E2:{self.eval_avg_2_episode_var_log_baseline_early_stopping:.2f}, " \
                      f"step_avg_es_E2:{self.eval_avg_2_episode_step_baseline_early_stopping:.2f}," \
                      f"S_sev_avg_uit_E2:{self.eval_avg_2_episode_snort_severe_baseline_uncaught_intrusion_steps:.2f}," \
                      f"S_warn_avg_uit_E2:{self.eval_avg_2_episode_snort_warning_baseline_uncaught_intrusion_steps:.2f}, " \
                      f"S_crit_avg_uit_E2:{self.eval_avg_2_episode_snort_critical_baseline_uncaught_intrusion_steps:.2f}," \
                      f"V_log_avg_uit_E2:{self.eval_avg_2_episode_var_log_baseline_uncaught_intrusion_steps:.2f}, " \
                      f"step_avg_uit_E2:{self.eval_avg_2_episode_step_baseline_uncaught_intrusion_steps:.2f}," \
                      f"avg_t_E2:{self.eval_2_avg_episode_steps:.2f}," \
                      f"epsilon:{self.epsilon:.2f}," \
                      f"c:{self.episode_caught_frac:.2f},es:{self.episode_early_stopped_frac:.2f}," \
                      f"s_i:{self.episode_successful_intrusion_frac:.2f}," \
                      f"n_af:{self.n_af:.2f}," \
                      f"c_E:{self.eval_episode_caught_frac:.2f},es_E:{self.eval_episode_early_stopped_frac:.2f}," \
                      f"s_i_E:{self.eval_episode_successful_intrusion_frac:.2f}," \
                      f"c_E2:{self.eval_2_episode_caught_frac:.2f},ess_E2:{self.eval_2_episode_early_stopped_frac:.2f}," \
                      f"s_i_E2:{self.eval_2_episode_successful_intrusion_frac:.2f},avg_F_T:{self.avg_episode_flags:.2f}," \
                      f"avg_F_T%:{self.avg_episode_flags_percentage:.2f}," \
                      f"avg_F_E:{self.eval_avg_episode_flags:.2f},avg_F_E%:{self.eval_avg_episode_flags_percentage:.2f}," \
                      f"avg_F_E2:{self.eval_2_avg_episode_flags:.2f}," \
                      f"avg_F_E2%:{self.eval_2_avg_episode_flags_percentage:.2f}," \
                      f"costs:{self.avg_episode_costs:.2f},costs_N:{self.avg_episode_costs_norm:.2f}," \
                      f"alerts:{self.avg_episode_alerts:.2f}," \
                      f"alerts_N:{self.avg_episode_alerts_norm:.2f},E_costs:{self.eval_avg_episode_costs:.2f}," \
                      f"E_costs_N:{self.eval_avg_episode_costs_norm:.2f},E_alerts:{self.eval_avg_episode_alerts:.2f}," \
                      f"E_alerts_N:{self.eval_avg_episode_alerts_norm:.2f}," \
                      f"E2_costs:{self.eval_2_avg_episode_costs:.2f},E2_costs_N:{self.eval_2_avg_episode_costs_norm:.2f}," \
                      f"E2_alerts:{self.eval_2_avg_episode_alerts:.2f}," \
                      f"E2_alerts_N:{self.eval_2_avg_episode_alerts_norm:.2f}," \
                      f"avg_I_t:{self.avg_episode_intrusion_steps:.2f}," \
                      f"E_avg_I_t:{self.eval_avg_episode_intrusion_steps:.2f}," \
                      f"E2_avg_I_t:{self.eval_2_avg_defender_stops_remaining:.2f}," \
                      f"avg_F_T_E2:{self.eval_2_avg_episode_flags:.2f}," \
                      f"avg_F_T_E2%:{self.eval_2_avg_episode_flags_percentage:.2f}," \
                      f"avg_stops_left_E2:{self.eval_2_avg_defender_stops_remaining:.2f}," \
                      f"avg_first_stop_t_E2:{self.eval_2_avg_defender_first_stop_step:.2f}," \
                      f"avg_second_stop_t_E2:{self.eval_2_avg_defender_second_stop_step:.2f}," \
                      f"avg_third_stop_t_E2:{self.eval_2_avg_defender_third_stop_step:.2f}," \
                      f"avg_fourth_stop_t_E2:{self.eval_2_avg_defender_fourth_stop_step:.2f}"
        return log_str
    

    def log_tensorboard_attacker(self) -> None:
        """
        Log metrics to tensorboard for attacker
        
        :return: None
        """
        train_or_eval = "eval" if self.eval else "train"
        self.tensorboard_writer.add_scalar('attacker/avg_episode_rewards/' + train_or_eval,
                                                           self.avg_episode_rewards,
                                                           self.iteration)
        self.tensorboard_writer.add_scalar('attacker/rolling_avg_episode_rewards/' + train_or_eval,
                                                           self.rolling_avg_episode_rewards,
                                                           self.iteration)
        self.tensorboard_writer.add_scalar('attacker/avg_episode_steps/' + train_or_eval,
                                                           self.avg_episode_steps,
                                                           self.iteration)
        self.tensorboard_writer.add_scalar('attacker/rolling_avg_episode_steps/' + train_or_eval,
                                                           self.rolling_avg_episode_steps,
                                                           self.iteration)
        self.tensorboard_writer.add_scalar('attacker/episode_avg_loss/' + train_or_eval,
                                                           self.avg_episode_loss,
                                                           self.iteration)
        self.tensorboard_writer.add_scalar('attacker/epsilon/' + train_or_eval,
                                                           self.epsilon,
                                                           self.iteration)
        self.tensorboard_writer.add_scalar('attacker/avg_episode_flags/' + train_or_eval,
                                                           self.avg_flags_catched,
                                                           self.iteration)
        self.tensorboard_writer.add_scalar('attacker/avg_episode_flags_percentage/' + train_or_eval,
                                                           self.avg_episode_flags_percentage,
                                                           self.iteration)
        self.tensorboard_writer.add_scalar('attacker/eval_avg_episode_rewards/' + train_or_eval,
                                                           self.eval_avg_episode_rewards,
                                                           self.iteration)
        self.tensorboard_writer.add_scalar('attacker/eval_avg_episode_steps/' + train_or_eval,
                                                           self.eval_avg_episode_steps,
                                                           self.iteration)
        self.tensorboard_writer.add_scalar('attacker/eval_avg_episode_flags/' + train_or_eval,
                                                           self.eval_avg_episode_flags,
                                                           self.iteration)
        self.tensorboard_writer.add_scalar('attacker/eval_avg_episode_flags_percentage/'
                                                           + train_or_eval,
                                                           self.eval_avg_episode_flags_percentage,
                                                           self.iteration)

        self.tensorboard_writer.add_scalar('attacker/eval_2_avg_episode_rewards/' + train_or_eval,
                                                           self.eval_2_avg_episode_rewards,
                                                           self.iteration)
        self.tensorboard_writer.add_scalar('attacker/eval_2_avg_episode_steps/' + train_or_eval,
                                                           self.eval_2_avg_episode_steps,
                                                           self.iteration)
        self.tensorboard_writer.add_scalar('attacker/eval_2_avg_episode_flags/' + train_or_eval,
                                                           self.eval_2_avg_episode_flags,
                                                           self.iteration)
        self.tensorboard_writer.add_scalar('attacker/eval_2_avg_episode_flags_percentage/'
                                                           + train_or_eval,
                                                           self.eval_2_avg_episode_flags_percentage,
                                                           self.iteration)

        self.tensorboard_writer.add_scalar('attacker/episode_caught_frac/' + train_or_eval,
                                                           self.episode_caught_frac,
                                                           self.iteration)
        self.tensorboard_writer.add_scalar('attacker/episode_early_stopped_frac/' + train_or_eval,
                                                           self.episode_early_stopped_frac,
                                                           self.iteration)
        self.tensorboard_writer.add_scalar('attacker/episode_successful_intrusion_frac/'
                                                           + train_or_eval,
                                                           self.episode_successful_intrusion_frac,
                                                           self.iteration)
        self.tensorboard_writer.add_scalar('attacker/eval_episode_caught_frac/' + train_or_eval,
                                                           self.eval_episode_caught_frac,
                                                           self.iteration)
        self.tensorboard_writer.add_scalar('attacker/eval_episode_early_stopped_frac/' + train_or_eval,
                                                           self.eval_episode_early_stopped_frac,
                                                           self.iteration)
        self.tensorboard_writer.add_scalar('attacker/eval_episode_successful_intrusion_frac/'
                                                           + train_or_eval,
                                                           self.eval_episode_successful_intrusion_frac,
                                                           self.iteration)
        self.tensorboard_writer.add_scalar('attacker/eval_2_episode_caught_frac/' + train_or_eval,
                                                           self.eval_2_episode_caught_frac,
                                                           self.iteration)
        self.tensorboard_writer.add_scalar('attacker/eval_2_episode_early_stopped_frac/'
                                                           + train_or_eval,
                                                           self.eval_2_episode_early_stopped_frac,
                                                           self.iteration)
        self.tensorboard_writer.add_scalar('attacker/eval_2_episode_successful_intrusion_frac/'
                                                           + train_or_eval,
                                                           self.eval_2_episode_successful_intrusion_frac,
                                                           self.iteration)

        if not self.eval:
            self.tensorboard_writer.add_scalar('attacker/lr', self.lr, self.iteration)
