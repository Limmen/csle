
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
            log_str = "[Eval A] iter:{},Avg_Reg:{:.2f},Opt_frac:{:.2f},avg_R:{:.2f},rolling_avg_R:{:.2f}," \
                      "avg_t:{:.2f},rolling_avg_t:{:.2f},lr:{:.2E},avg_F:{:.2f},avg_F%:{:.2f}," \
                      "n_af:{},n_d:{}," \
                      "c:{:.2f},s:{:.2f},s_i:{:.2f},costs:{:.2f},costs_N:{:.2f},alerts:{:.2f}," \
                      "alerts_N:{:.2f}".format(
                self.iteration, self.avg_regret, self.avg_opt_frac, self.avg_episode_rewards, self.rolling_avg_rewards,
                self.avg_episode_steps, self.rolling_avg_steps, self.lr, self.avg_episode_flags,
                self.avg_episode_flags_percentage, self.n_af, self.n_d,
                self.episode_caught_frac, self.episode_early_stopped_frac, self.episode_successful_intrusion_frac,
                self.avg_episode_costs, self.avg_episode_costs_norm, self.avg_episode_alerts,
                self.avg_episode_alerts_norm
            )
        else:
            log_str = "[Train A] iter:{:.2f},avg_reg_T:{:.2f},opt_frac_T:{:.2f},avg_R_T:{:.2f},rolling_avg_R_T:{:.2f}," \
                      "avg_t_T:{:.2f},rolling_avg_t_T:{:.2f}," \
                      "loss:{:.6f},lr:{:.2E},episode:{},avg_F_T:{:.2f},avg_F_T%:{:.2f},eps:{:.2f}," \
                      "n_af:{},n_d:{},avg_R_E:{:.2f},avg_reg_E:{:.2f},avg_opt_frac_E:{:.2f}," \
                      "avg_t_E:{:.2f},avg_F_E:{:.2f},avg_F_E%:{:.2f}," \
                      "avg_R_E2:{:.2f},Avg_Reg_E2:{:.2f},Opt_frac_E2:{:.2f},avg_t_E2:{:.2f},avg_F_E2:{:.2f}," \
                      "avg_F_E2%:{:.2f},epsilon:{:.2f}," \
                      "c:{:.2f},s:{:.2f},s_i:{:.2f}," \
                      "c_E:{:.2f},s_E:{:.2f},s_i_E:{:.2f}," \
                      "c_E2:{:.2f},s_E2:{:.2f},s_i_E:{:.2f},costs:{:.2f},costs_N:{:.2f},alerts:{:.2f}," \
                      "alerts_N:{:.2f},E_costs:{:.2f},E_costs_N:{:.2f},E_alerts:{:.2f},E_alerts_N:{:.2f}," \
                      "E2_costs:{:.2f},E2_costs_N:{:.2f},E2_alerts:{:.2f},E2_alerts_N:{:.2f}," \
                      "tt_h:{:.2f},avg_F_T_E:{:.2f},avg_F_T_E%:{:.2f}".format(
                self.iteration, self.avg_regret, self.avg_opt_frac, self.avg_episode_rewards, self.rolling_avg_rewards,
                self.avg_episode_steps, self.rolling_avg_steps, self.avg_episode_loss,
                self.lr, self.total_num_episodes, self.avg_episode_flags,
                self.avg_episode_flags_percentage, self.eps,
                self.n_af, self.n_d,
                self.eval_avg_episode_rewards, self.avg_eval_regret, self.eval_avg_opt_frac, self.eval_avg_episode_steps,
                self.eval_avg_episode_flags,
                self.eval_avg_episode_flags_percentage, self.eval_2_avg_episode_rewards, self.avg_regret_2,
                self.avg_opt_frac_2,
                self.eval_2_avg_episode_steps,
                self.eval_2_avg_episode_flags, self.eval_2_avg_episode_flags_percentage,
                self.epsilon,
                self.episode_caught_frac, self.episode_early_stopped_frac, self.episode_successful_intrusion_frac,
                self.eval_episode_caught_frac, self.eval_episode_early_stopped_frac,
                self.eval_episode_successful_intrusion_frac,
                self.eval_2_episode_caught_frac, self.eval_2_episode_early_stopped_frac,
                self.eval_2_episode_successful_intrusion_frac,
                self.avg_episode_costs, self.avg_episode_costs_norm, self.avg_episode_alerts,
                self.avg_episode_alerts_norm,
                self.eval_avg_episode_costs, self.eval_avg_episode_costs_norm, self.eval_avg_episode_alerts,
                self.eval_avg_episode_alerts_norm, self.eval_2_avg_episode_costs, self.eval_2_avg_episode_costs_norm,
                self.eval_2_avg_episode_alerts, self.eval_2_avg_episode_alerts_norm, self.training_time_hours,
                self.eval_avg_episode_flags, self.eval_avg_episode_flags_percentage,
                self.eval_2_avg_episode_flags, self.eval_2_avg_episode_flags_percentage
            )
        return log_str

    def log_str_defender(self) -> str:
        """
        :return: a string representation of the DTO for the attacker
        """
        if self.eval:
            log_str = "[Eval D] iter:{},avg_R:{:.2f},rolling_avg_R:{:.2f},avg_uit:{:.2f},avg_opt_R_T:{:.2f}," \
                      "S_sev_avg_R:{:.2f},S_warn_avg_R:{:.2f}," \
                      "S_crit_avg_R:{:.2f},V_log_avg_R:{:.2f}, step_avg_R:{:.2f}," \
                      "S_sev_avg_t:{:.2f},S_warn_avg_t:{:.2f}," \
                      "S_crit_avg_t:{:.2f},V_log_avg_t:{:.2f}, step_avg_t:{:.2f}," \
                      "S_sev_avg_ca:{:.2f},S_warn_avg_ca:{:.2f}," \
                      "S_crit_avg_ca:{:.2f},V_log_avg_ca:{:.2f}, step_avg_ca:{:.2f}," \
                      "S_sev_avg_es:{:.2f},S_warn_avg_e:{:.2f}," \
                      "S_crit_avg_es:{:.2f},V_log_avg_es:{:.2f}, step_avg_es:{:.2f}," \
                      "S_sev_avg_uit:{:.2f},S_warn_avg_uit:{:.2f}," \
                      "S_crit_avg_uit:{:.2f},V_log_avg_uit:{:.2f}, step_avg_uit:{:.2f}," \
                      "avg_t:{:.2f},rolling_avg_t:{:.2f},lr:{:.2E}," \
                      "c:{:.2f},s:{:.2f},s_i:{:.2f},avg_I_t:{:.2f}, avg_stops_left_T:{:.2f}," \
                      "avg_first_stop_t_T:{:.2f},avg_second_stop_t_T:{:.2f},avg_third_stop_t_T:{:.2f}," \
                      "avg_fourth_stop_t_T:{:.2f}".format(
                self.iteration, self.avg_episode_rewards, self.rolling_avg_rewards, self.avg_uncaught_intrusion_steps,
                self.avg_optimal_defender_reward,
                self.avg_episode_snort_severe_baseline_rewards,
                self.avg_episode_snort_warning_baseline_rewards,
                self.avg_episode_snort_critical_baseline_rewards,
                self.avg_episode_var_log_baseline_rewards,
                self.avg_episode_step_baseline_rewards,
                self.avg_episode_snort_severe_baseline_steps,
                self.avg_episode_snort_warning_baseline_steps,
                self.avg_episode_snort_critical_baseline_steps,
                self.avg_episode_var_log_baseline_steps,
                self.avg_episode_step_baseline_steps,
                self.avg_episode_snort_severe_baseline_caught_attacker,
                self.avg_episode_snort_warning_baseline_caught_attacker,
                self.avg_episode_snort_critical_baseline_caught_attacker,
                self.avg_episode_var_log_baseline_caught_attacker,
                self.avg_episode_step_baseline_caught_attacker,
                self.avg_episode_snort_severe_baseline_early_stopping,
                self.avg_episode_snort_warning_baseline_early_stopping,
                self.avg_episode_snort_critical_baseline_early_stopping,
                self.avg_episode_var_log_baseline_early_stopping,
                self.avg_episode_step_baseline_early_stopping,
                self.avg_episode_snort_severe_baseline_uncaught_intrusion_steps,
                self.avg_episode_snort_warning_baseline_uncaught_intrusion_steps,
                self.avg_episode_snort_critical_baseline_uncaught_intrusion_steps,
                self.avg_episode_var_log_baseline_uncaught_intrusion_steps,
                self.avg_episode_step_baseline_uncaught_intrusion_steps,
                self.avg_episode_steps, self.rolling_avg_steps,
                self.lr, self.episode_caught_frac,
                self.episode_early_stopped_frac, self.episode_successful_intrusion_frac,
                self.avg_episode_intrusion_steps, self.avg_defender_stops_remaining, self.avg_defender_first_stop_step,
                self.avg_defender_second_stop_step, self.avg_defender_third_stop_step,
                self.avg_defender_fourth_stop_step)
        else:
            log_str = "[Train D] iter:{:.2f},avg_reg_T:{:.2f},opt_frac_T:{:.2f}," \
                      "avg_R_T:{:.2f},rolling_avg_R_T:{:.2f},avg_uit_T:{:.2f},avg_opt_R_T:{:.2f}," \
                      "S_sev_avg_R_T:{:.2f},S_warn_avg_R_T:{:.2f},S_crit_avg_R_T:{:.2f},V_log_avg_R_T:{:.2f}," \
                      "step_avg_R_T:{:.2f}, " \
                      "S_sev_avg_t_T:{:.2f},S_warn_avg_t_T:{:.2f}, " \
                      "S_crit_avg_t_T:{:.2f},V_log_avg_t_T:{:.2f}, step_avg_t_T:{:.2f}," \
                      "S_sev_avg_ca_T:{:.2f},S_warn_avg_ca_T:{:.2f}, " \
                      "S_crit_avg_ca_T:{:.2f},V_log_avg_ca_T:{:.2f}, step_avg_ca_T:{:.2f}," \
                      "S_sev_avg_es_T:{:.2f},S_warn_avg_es_T:{:.2f}, " \
                      "S_crit_avg_es_T:{:.2f},V_log_avg_es_T:{:.2f}, step_avg_es_T:{:.2f}," \
                      "S_sev_avg_uit_T:{:.2f},S_warn_avg_uit_T:{:.2f}, " \
                      "S_crit_avg_uit_T:{:.2f},V_log_avg_uit_T:{:.2f}, step_avg_uit_T:{:.2f}," \
                      "avg_t_T:{:.2f},rolling_avg_t_T:{:.2f}," \
                      "loss:{:.6f},lr:{:.2E},episode:{},avg_stops_left_T:{:.2f}," \
                      "avg_first_stop_t_T:{:.2f},avg_second_stop_t_T:{:.2f},avg_third_stop_t_T:{:.2f}," \
                      "avg_fourth_stop_t_T:{:.2f},eps:{:.2f}," \
                      "avg_R_E:{:.2f},avg_uit_E:{:.2f},opt_R_E:{:.2f},S_sev_avg_R_E:{:.2f},S_warn_avg_R_E:{:.2f}," \
                      "S_crit_avg_R_E:{:.2f},V_log_avg_R_E:{:.2f}, step_avg_R_E:{:.2f}," \
                      "S_sev_avg_t_E:{:.2f},S_warn_avg_t_E:{:.2f}, " \
                      "S_crit_avg_t_E:{:.2f},V_log_avg_t_E:{:.2f}, step_avg_t_E:{:.2f}," \
                      "S_sev_avg_ca_E:{:.2f},S_warn_avg_ca_E:{:.2f}, " \
                      "S_crit_avg_ca_E:{:.2f},V_log_avg_ca_E:{:.2f}, step_avg_ca_E:{:.2f}," \
                      "S_sev_avg_es_E:{:.2f},S_warn_avg_es_E:{:.2f}, " \
                      "S_crit_avg_es_E:{:.2f},V_log_avg_es_E:{:.2f}, step_avg_es_E:{:.2f}," \
                      "S_sev_avg_uit_E:{:.2f},S_warn_avg_uit_E:{:.2f}, " \
                      "S_crit_avg_uit_E:{:.2f},V_log_avg_uit_E:{:.2f}, step_avg_uit_E:{:.2f}," \
                      "avg_reg_E:{:.2f},avg_opt_frac_E:{:.2f}," \
                      "avg_t_E:{:.2f},avg_stops_left_E:{:.2f},avg_first_stop_t_E:{:.2f},avg_second_stop_t_E:{:.2f}," \
                      "avg_third_stop_t_E:{:.2f},avg_fourth_stop_t_E:{:.2f}," \
                      "avg_R_E2:{:.2f},avg_uit_E2:{:.2f},opt_R_E2:{:.2f},S_sev_avg_R_E2:{:.2f},S_warn_avg_R_E2:{:.2f}," \
                      "S_crit_avg_R_E2:{:.2f},V_log_avg_R_E2:{:.2f},step_avg_R_E2:{:.2f}," \
                      "S_sev_avg_t_E2:{:.2f},S_warn_avg_t_E2:{:.2f}," \
                      "S_crit_avg_t_E2:{:.2f},V_log_avg_t_E2:{:.2f},step_avg_t_E2:{:.2f}," \
                      "S_sev_avg_ca_E2:{:.2f},S_warn_avg_ca_E2:{:.2f}, " \
                      "S_crit_avg_ca_E2:{:.2f},V_log_avg_ca_E2:{:.2f}, step_avg_ca_E2:{:.2f}," \
                      "S_sev_avg_es_E2:{:.2f},S_warn_avg_es_E2:{:.2f}, " \
                      "S_crit_avg_es_E2:{:.2f},V_log_avg_es_E2:{:.2f}, step_avg_es_E2:{:.2f}," \
                      "S_sev_avg_uit_E2:{:.2f},S_warn_avg_uit_E2:{:.2f}, " \
                      "S_crit_avg_uit_E2:{:.2f},V_log_avg_uit_E2:{:.2f}, step_avg_uit_E2:{:.2f}," \
                      "avg_t_E2:{:.2f}," \
                      "epsilon:{:.2f}," \
                      "c:{:.2f},s:{:.2f},s_i:{:.2f},n_af:{:.2f}," \
                      "c_E:{:.2f},s_E:{:.2f},s_i_E:{:.2f}," \
                      "c_E2:{:.2f},s_E2:{:.2f},s_i_E2:{:.2f},avg_F_T:{:.2f},avg_F_T%:{:.2f}," \
                      "avg_F_E:{:.2f},avg_F_E%:{:.2f},avg_F_E2:{:.2f},avg_F_E2%:{:.2f}," \
                      "costs:{:.2f},costs_N:{:.2f},alerts:{:.2f}," \
                      "alerts_N:{:.2f},E_costs:{:.2f},E_costs_N:{:.2f},E_alerts:{:.2f},E_alerts_N:{:.2f}," \
                      "E2_costs:{:.2f},E2_costs_N:{:.2f},E2_alerts:{:.2f},E2_alerts_N:{:.2f}," \
                      "avg_I_t:{:.2f},E_avg_I_t:{:.2f},E2_avg_I_t:{:.2f}," \
                      "avg_F_T_E2:{:.2f},avg_F_T_E2%:{:.2f},avg_stops_left_E2:{:.2f}," \
                      "avg_first_stop_t_E2:{:.2f},avg_second_stop_t_E2:{:.2f}," \
                      "avg_third_stop_t_E2:{:.2f},avg_fourth_stop_t_E2:{:.2f}".format(
                self.iteration, self.avg_regret, self.avg_opt_frac, self.avg_episode_rewards,
                self.rolling_avg_rewards, self.avg_uncaught_intrusion_steps, self.avg_optimal_defender_reward,
                self.avg_episode_snort_severe_baseline_rewards, self.avg_episode_snort_warning_baseline_rewards,
                self.avg_episode_snort_critical_baseline_rewards, self.avg_episode_var_log_baseline_rewards,
                self.avg_episode_step_baseline_rewards,
                self.avg_episode_snort_severe_baseline_steps, self.avg_episode_snort_warning_baseline_steps,
                self.avg_episode_snort_critical_baseline_steps, self.avg_episode_var_log_baseline_steps,
                self.avg_episode_step_baseline_steps,
                self.avg_episode_snort_severe_baseline_caught_attacker, self.avg_episode_snort_warning_baseline_caught_attacker,
                self.avg_episode_snort_critical_baseline_caught_attacker, self.avg_episode_var_log_baseline_caught_attacker,
                self.avg_episode_step_baseline_caught_attacker,
                self.avg_episode_snort_severe_baseline_early_stopping, self.avg_episode_snort_warning_baseline_early_stopping,
                self.avg_episode_snort_critical_baseline_early_stopping, self.avg_episode_var_log_baseline_early_stopping,
                self.avg_episode_step_baseline_early_stopping,
                self.avg_episode_snort_severe_baseline_uncaught_intrusion_steps, self.avg_episode_snort_warning_baseline_uncaught_intrusion_steps,
                self.avg_episode_snort_critical_baseline_uncaught_intrusion_steps, self.avg_episode_var_log_baseline_uncaught_intrusion_steps,
                self.avg_episode_step_baseline_uncaught_intrusion_steps,
                self.avg_episode_steps, self.rolling_avg_steps, self.avg_episode_loss,
                self.lr, self.total_num_episodes, self.avg_defender_stops_remaining, self.avg_defender_first_stop_step,
                self.avg_defender_second_stop_step, self.avg_defender_third_stop_step,
                self.avg_defender_fourth_stop_step, self.eps,
                self.eval_avg_episode_rewards, self.eval_avg_uncaught_intrusion_steps,
                self.eval_avg_optimal_defender_reward,
                self.eval_avg_episode_snort_severe_baseline_rewards,
                self.eval_avg_episode_snort_warning_baseline_rewards,
                self.eval_avg_episode_snort_critical_baseline_rewards,
                self.eval_avg_episode_var_log_baseline_rewards, self.eval_avg_episode_step_baseline_rewards,
                self.eval_avg_episode_snort_severe_baseline_steps,
                self.eval_avg_episode_snort_warning_baseline_steps,
                self.eval_avg_episode_snort_critical_baseline_steps,
                self.eval_avg_episode_var_log_baseline_steps, self.eval_avg_episode_step_baseline_steps,
                self.eval_avg_episode_snort_severe_baseline_caught_attacker,
                self.eval_avg_episode_snort_warning_baseline_caught_attacker,
                self.eval_avg_episode_snort_critical_baseline_caught_attacker,
                self.eval_avg_episode_var_log_baseline_caught_attacker, self.eval_avg_episode_step_baseline_caught_attacker,
                self.eval_avg_episode_snort_severe_baseline_early_stopping,
                self.eval_avg_episode_snort_warning_baseline_early_stopping,
                self.eval_avg_episode_snort_critical_baseline_early_stopping,
                self.eval_avg_episode_var_log_baseline_early_stopping, self.eval_avg_episode_step_baseline_early_stopping,
                self.eval_avg_episode_snort_severe_baseline_uncaught_intrusion_steps,
                self.eval_avg_episode_snort_warning_baseline_uncaught_intrusion_steps,
                self.eval_avg_episode_snort_critical_baseline_uncaught_intrusion_steps,
                self.eval_avg_episode_var_log_baseline_uncaught_intrusion_steps, self.eval_avg_episode_step_baseline_uncaught_intrusion_steps,
                self.avg_eval_regret, self.eval_avg_opt_frac, self.eval_avg_episode_steps,
                self.eval_avg_defender_stops_remaining, self.eval_avg_defender_first_stop_step,
                self.eval_avg_defender_second_stop_step, self.eval_avg_defender_third_stop_step,
                self.eval_avg_defender_fourth_stop_step,
                self.eval_2_avg_episode_rewards, self.eval_2_avg_uncaught_intrusion_steps,
                self.eval_2_avg_optimal_defender_reward,
                self.eval_avg_2_episode_snort_severe_baseline_rewards,
                self.eval_avg_2_episode_snort_warning_baseline_rewards,
                self.eval_avg_2_episode_snort_critical_baseline_rewards,
                self.eval_avg_2_episode_var_log_baseline_rewards,
                self.eval_avg_2_episode_step_baseline_rewards,
                self.eval_avg_2_episode_snort_severe_baseline_steps,
                self.eval_avg_2_episode_snort_warning_baseline_steps,
                self.eval_avg_2_episode_snort_critical_baseline_steps,
                self.eval_avg_2_episode_var_log_baseline_steps,
                self.eval_avg_2_episode_step_baseline_steps,
                self.eval_avg_2_episode_snort_severe_baseline_caught_attacker,
                self.eval_avg_2_episode_snort_warning_baseline_caught_attacker,
                self.eval_avg_2_episode_snort_critical_baseline_caught_attacker,
                self.eval_avg_2_episode_var_log_baseline_caught_attacker,
                self.eval_avg_2_episode_step_baseline_caught_attacker,
                self.eval_avg_2_episode_snort_severe_baseline_early_stopping,
                self.eval_avg_2_episode_snort_warning_baseline_early_stopping,
                self.eval_avg_2_episode_snort_critical_baseline_early_stopping,
                self.eval_avg_2_episode_var_log_baseline_early_stopping,
                self.eval_avg_2_episode_step_baseline_early_stopping,
                self.eval_avg_2_episode_snort_severe_baseline_uncaught_intrusion_steps,
                self.eval_avg_2_episode_snort_warning_baseline_uncaught_intrusion_steps,
                self.eval_avg_2_episode_snort_critical_baseline_uncaught_intrusion_steps,
                self.eval_avg_2_episode_var_log_baseline_uncaught_intrusion_steps,
                self.eval_avg_2_episode_step_baseline_uncaught_intrusion_steps,
                self.eval_2_avg_episode_steps, self.epsilon,
                self.episode_caught_frac, self.episode_early_stopped_frac,
                self.episode_successful_intrusion_frac,
                self.n_af, self.eval_episode_caught_frac, self.eval_episode_early_stopped_frac,
                self.eval_episode_successful_intrusion_frac,
                self.eval_2_episode_caught_frac,
                self.eval_2_episode_early_stopped_frac, self.eval_2_episode_successful_intrusion_frac,
                self.avg_episode_flags, self.avg_episode_flags_percentage, self.eval_avg_episode_flags,
                self.eval_avg_episode_flags_percentage, self.eval_2_avg_episode_flags,
                self.eval_2_avg_episode_flags_percentage,
                self.avg_episode_costs, self.avg_episode_costs_norm, self.avg_episode_alerts,
                self.avg_episode_alerts_norm,
                self.eval_avg_episode_costs, self.eval_avg_episode_costs_norm, self.eval_avg_episode_alerts,
                self.eval_avg_episode_alerts_norm, self.eval_2_avg_episode_costs, self.eval_2_avg_episode_costs_norm,
                self.eval_2_avg_episode_alerts, self.eval_2_avg_episode_alerts_norm,
                self.avg_episode_intrusion_steps, self.eval_avg_episode_intrusion_steps,
                self.eval_2_avg_episode_intrusion_steps, self.eval_2_avg_defender_stops_remaining,
                self.eval_2_avg_defender_first_stop_step,
                self.eval_2_avg_defender_second_stop_step, self.eval_2_avg_defender_third_stop_step,
                self.eval_2_avg_defender_fourth_stop_step)
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
