from typing import List
from gym_pycr_ctf.dao.experiment.experiment_result import ExperimentResult

class TrainAgentLogDTO:
    """
    DTO with information for logging during training
    """
    def __init__(self, iteration: int = 0, train_result : ExperimentResult = None, eval_result: ExperimentResult = None,
                 attacker_episode_rewards: List[float] = None,
                 attacker_episode_avg_loss: List[float] = None,
                 attacker_lr: float = 0.0,
                 defender_episode_rewards: List[float] = None,
                 defender_episode_avg_loss: List[float] = None,
                 defender_lr: float = 0.0,
                 total_num_episodes : int = 1,
                 episode_steps : List[int] = None, episode_flags : List[int] = None,
                 eval: bool = False, episode_flags_percentage: List[float] = None, progress_left : float = 0.0,
                 n_af : int = 0, n_d : int = 0,
                 attacker_eval_episode_rewards: List[int] = None,
                 defender_eval_episode_rewards: List[int] = None,
                 eval_episode_steps : List[int] = None, eval_episode_flags : List[int] = None,
                 eval_episode_flags_percentage : List[float]= None,
                 attacker_eval_2_episode_rewards : List[int] = None,
                 defender_eval_2_episode_rewards: List[int] = None,
                 eval_2_episode_steps: List[int] = None, eval_2_episode_flags: List[int] = None,
                 eval_2_episode_flags_percentage: List[float] = None,
                 attacker_train_episode_env_specific_rewards: dict = None,
                 defender_train_episode_env_specific_rewards: dict = None,
                 train_env_specific_steps: dict = None,
                 train_env_specific_flags: dict = None,
                 train_env_specific_flags_percentage: dict = None,
                 attacker_eval_env_specific_rewards: dict = None,
                 defender_eval_env_specific_rewards: dict = None,
                 eval_env_specific_steps: dict = None,
                 eval_env_specific_flags: dict = None,
                 eval_env_specific_flags_percentage: dict = None,
                 attacker_eval_2_env_specific_rewards: dict = None,
                 defender_eval_2_env_specific_rewards: dict = None,
                 eval_2_env_specific_steps: dict = None,
                 eval_2_env_specific_flags: dict = None,
                 eval_2_env_specific_flags_percentage: dict = None,
                 rollout_times : List[float] = None, env_response_times: List[float]= None,
                 action_pred_times : List[float] = None, grad_comp_times : List[float] = None,
                 weight_update_times : List[float]= None,
                 episode_caught : List[int] = None, episode_early_stopped : List[int] = None,
                 episode_successful_intrusion : List[int] = None,
                 eval_episode_caught : List[int] = None,
                 eval_episode_early_stopped : List[int] = None,
                 eval_episode_successful_intrusion : List[int] = None,
                 eval_2_episode_caught: List[int] = None,
                 eval_2_episode_early_stopped: List[int] = None,
                 eval_2_episode_successful_intrusion: List[int] = None,
                 episode_snort_severe_baseline_rewards : List[int] = None,
                 episode_snort_warning_baseline_rewards: List[int] = None,
                 eval_episode_snort_severe_baseline_rewards: List[int] = None,
                 eval_episode_snort_warning_baseline_rewards: List[int] = None,
                 eval_2_episode_snort_severe_baseline_rewards: List[int] = None,
                 eval_2_episode_snort_warning_baseline_rewards: List[int] = None,
                 episode_snort_critical_baseline_rewards: List[int] = None,
                 episode_var_log_baseline_rewards: List[int] = None,
                 eval_episode_snort_critical_baseline_rewards: List[int] = None,
                 eval_episode_var_log_baseline_rewards: List[int] = None,
                 eval_2_episode_snort_critical_baseline_rewards: List[int] = None,
                 eval_2_episode_var_log_baseline_rewards: List[int] = None,
                 episode_snort_severe_baseline_steps: List[int] = None,
                 episode_snort_warning_baseline_steps: List[int] = None,
                 eval_episode_snort_severe_baseline_steps: List[int] = None,
                 eval_episode_snort_warning_baseline_steps: List[int] = None,
                 eval_2_episode_snort_severe_baseline_steps: List[int] = None,
                 eval_2_episode_snort_warning_baseline_steps: List[int] = None,
                 episode_snort_critical_baseline_steps: List[int] = None,
                 episode_var_log_baseline_steps: List[int] = None,
                 eval_episode_snort_critical_baseline_steps: List[int] = None,
                 eval_episode_var_log_baseline_steps: List[int] = None,
                 eval_2_episode_snort_critical_baseline_steps: List[int] = None,
                 eval_2_episode_var_log_baseline_steps: List[int] = None,
                 episode_step_baseline_rewards : List[int] = None,
                 episode_step_baseline_steps: List[int] = None,
                 eval_episode_step_baseline_rewards: List[int] = None,
                 eval_episode_step_baseline_steps: List[int] = None,
                 eval_2_episode_step_baseline_rewards: List[int] = None,
                 eval_2_episode_step_baseline_steps: List[int] = None,
                 attacker_action_costs :List[float] = None,
                 attacker_action_costs_norm :List[float] = None,
                 attacker_action_alerts :List[float] = None,
                 attacker_action_alerts_norm :List[float] = None,
                 eval_attacker_action_costs: List[float] = None,
                 eval_attacker_action_costs_norm: List[float] = None,
                 eval_attacker_action_alerts: List[float] = None,
                 eval_attacker_action_alerts_norm: List[float] = None,
                 eval_2_attacker_action_costs: List[float] = None,
                 eval_2_attacker_action_costs_norm: List[float] = None,
                 eval_2_attacker_action_alerts: List[float] = None,
                 eval_2_attacker_action_alerts_norm: List[float] = None,
                 start_time: float = 0.0,
                 episode_intrusion_steps: List[int] = None,
                 eval_episode_intrusion_steps: List[int] = None,
                 eval_2_episode_intrusion_steps: List[int] = None,
                 episode_snort_severe_baseline_caught_attacker: List[int] = None,
                 episode_snort_warning_baseline_caught_attacker: List[int] = None,
                 eval_episode_snort_severe_baseline_caught_attacker: List[int] = None,
                 eval_episode_snort_warning_baseline_caught_attacker: List[int] = None,
                 eval_2_episode_snort_severe_baseline_caught_attacker: List[int] = None,
                 eval_2_episode_snort_warning_baseline_caught_attacker: List[int] = None,
                 episode_snort_critical_baseline_caught_attacker: List[int] = None,
                 episode_var_log_baseline_caught_attacker: List[int] = None,
                 eval_episode_snort_critical_baseline_caught_attacker: List[int] = None,
                 eval_episode_var_log_baseline_caught_attacker: List[int] = None,
                 eval_2_episode_snort_critical_baseline_caught_attacker: List[int] = None,
                 eval_2_episode_var_log_baseline_caught_attacker: List[int] = None,
                 episode_step_baseline_caught_attacker: List[int] = None,
                 eval_episode_step_baseline_caught_attacker: List[int] = None,
                 eval_2_episode_step_baseline_caught_attacker: List[int] = None,
                 episode_snort_severe_baseline_early_stopping: List[int] = None,
                 episode_snort_warning_baseline_early_stopping: List[int] = None,
                 eval_episode_snort_severe_baseline_early_stopping: List[int] = None,
                 eval_episode_snort_warning_baseline_early_stopping: List[int] = None,
                 eval_2_episode_snort_severe_baseline_early_stopping: List[int] = None,
                 eval_2_episode_snort_warning_baseline_early_stopping: List[int] = None,
                 episode_snort_critical_baseline_early_stopping: List[int] = None,
                 episode_var_log_baseline_early_stopping: List[int] = None,
                 eval_episode_snort_critical_baseline_early_stopping: List[int] = None,
                 eval_episode_var_log_baseline_early_stopping: List[int] = None,
                 eval_2_episode_snort_critical_baseline_early_stopping: List[int] = None,
                 eval_2_episode_var_log_baseline_early_stopping: List[int] = None,
                 episode_step_baseline_early_stopping: List[int] = None,
                 eval_episode_step_baseline_early_stopping: List[int] = None,
                 eval_2_episode_step_baseline_early_stopping: List[int] = None,
                 episode_snort_severe_baseline_uncaught_intrusion_steps: List[int] = None,
                 episode_snort_warning_baseline_uncaught_intrusion_steps: List[int] = None,
                 eval_episode_snort_severe_baseline_uncaught_intrusion_steps: List[int] = None,
                 eval_episode_snort_warning_baseline_uncaught_intrusion_steps: List[int] = None,
                 eval_2_episode_snort_severe_baseline_uncaught_intrusion_steps: List[int] = None,
                 eval_2_episode_snort_warning_baseline_uncaught_intrusion_steps: List[int] = None,
                 episode_snort_critical_baseline_uncaught_intrusion_steps: List[int] = None,
                 episode_var_log_baseline_uncaught_intrusion_steps: List[int] = None,
                 eval_episode_snort_critical_baseline_uncaught_intrusion_steps: List[int] = None,
                 eval_episode_var_log_baseline_uncaught_intrusion_steps: List[int] = None,
                 eval_2_episode_snort_critical_baseline_uncaught_intrusion_steps: List[int] = None,
                 eval_2_episode_var_log_baseline_uncaught_intrusion_steps: List[int] = None,
                 episode_step_baseline_uncaught_intrusion_steps: List[int] = None,
                 eval_episode_step_baseline_uncaught_intrusion_steps: List[int] = None,
                 eval_2_episode_step_baseline_uncaught_intrusion_steps: List[int] = None,
                 uncaught_intrusion_steps : List[int] = None,
                 eval_uncaught_intrusion_steps: List[int] = None,
                 eval_2_uncaught_intrusion_steps: List[int] = None
                 ):
        self.iteration = iteration
        self.train_result = train_result
        self.eval_result = eval_result
        self.attacker_episode_rewards = attacker_episode_rewards
        self.attacker_episode_avg_loss = attacker_episode_avg_loss
        self.attacker_lr = attacker_lr
        self.defender_episode_rewards = defender_episode_rewards
        self.defender_episode_avg_loss = defender_episode_avg_loss
        self.defender_lr = defender_lr
        self.total_num_episodes = total_num_episodes
        self.episode_steps = episode_steps
        self.episode_flags = episode_flags
        self.eval = eval
        self.episode_flags_percentage = episode_flags_percentage
        self.progress_left = progress_left
        self.n_af = n_af
        self.n_d = n_d
        self.attacker_eval_episode_rewards = attacker_eval_episode_rewards
        self.defender_eval_episode_rewards = defender_eval_episode_rewards
        self.eval_episode_steps = eval_episode_steps
        self.eval_episode_flags = eval_episode_flags
        self.eval_episode_flags_percentage = eval_episode_flags_percentage
        self.attacker_eval_2_episode_rewards = attacker_eval_2_episode_rewards
        self.defender_eval_2_episode_rewards = defender_eval_2_episode_rewards
        self.eval_2_episode_steps = eval_2_episode_steps
        self.eval_2_episode_flags = eval_2_episode_flags
        self.eval_2_episode_flags_percentage = eval_2_episode_flags_percentage
        self.attacker_train_episode_env_specific_rewards = attacker_train_episode_env_specific_rewards
        self.defender_train_episode_env_specific_rewards = defender_train_episode_env_specific_rewards
        self.train_env_specific_steps = train_env_specific_steps
        self.train_env_specific_flags = train_env_specific_flags
        self.train_env_specific_flags_percentage = train_env_specific_flags_percentage
        self.attacker_eval_env_specific_rewards = attacker_eval_env_specific_rewards
        self.defender_eval_env_specific_rewards = defender_eval_env_specific_rewards
        self.eval_env_specific_steps = eval_env_specific_steps
        self.eval_env_specific_flags = eval_env_specific_flags
        self.eval_env_specific_flags_percentage = eval_env_specific_flags_percentage
        self.attacker_eval_2_env_specific_rewards = attacker_eval_2_env_specific_rewards
        self.defender_eval_2_env_specific_rewards = defender_eval_2_env_specific_rewards
        self.eval_2_env_specific_steps = eval_2_env_specific_steps
        self.eval_2_env_specific_flags = eval_2_env_specific_flags
        self.eval_2_env_specific_flags_percentage = eval_2_env_specific_flags_percentage
        self.rollout_times = rollout_times
        self.env_response_times = env_response_times
        self.action_pred_times = action_pred_times
        self.grad_comp_times = grad_comp_times
        self.weight_update_times = weight_update_times
        self.episode_caught = episode_caught
        self.episode_early_stopped = episode_early_stopped
        self.episode_successful_intrusion = episode_successful_intrusion
        self.eval_episode_caught = eval_episode_caught
        self.eval_episode_early_stopped = eval_episode_early_stopped
        self.eval_episode_successful_intrusion = eval_episode_successful_intrusion
        self.eval_2_episode_caught = eval_2_episode_caught
        self.eval_2_episode_early_stopped = eval_2_episode_early_stopped
        self.eval_2_episode_successful_intrusion = eval_2_episode_successful_intrusion
        self.episode_snort_severe_baseline_rewards = episode_snort_severe_baseline_rewards
        self.episode_snort_warning_baseline_rewards = episode_snort_warning_baseline_rewards
        self.eval_episode_snort_severe_baseline_rewards = eval_episode_snort_severe_baseline_rewards
        self.eval_episode_snort_warning_baseline_rewards = eval_episode_snort_warning_baseline_rewards
        self.eval_2_episode_snort_severe_baseline_rewards = eval_2_episode_snort_severe_baseline_rewards
        self.eval_2_episode_snort_warning_baseline_rewards = eval_2_episode_snort_warning_baseline_rewards
        self.episode_snort_critical_baseline_rewards = episode_snort_critical_baseline_rewards
        self.episode_var_log_baseline_rewards = episode_var_log_baseline_rewards
        self.eval_episode_snort_critical_baseline_rewards = eval_episode_snort_critical_baseline_rewards
        self.eval_episode_var_log_baseline_rewards = eval_episode_var_log_baseline_rewards
        self.eval_2_episode_var_log_baseline_rewards = eval_2_episode_var_log_baseline_rewards
        self.eval_2_episode_snort_critical_baseline_rewards = eval_2_episode_snort_critical_baseline_rewards
        self.episode_snort_severe_baseline_steps = episode_snort_severe_baseline_steps
        self.episode_snort_warning_baseline_steps = episode_snort_warning_baseline_steps
        self.eval_episode_snort_severe_baseline_steps = eval_episode_snort_severe_baseline_steps
        self.eval_episode_snort_warning_baseline_steps = eval_episode_snort_warning_baseline_steps
        self.eval_2_episode_snort_severe_baseline_steps = eval_2_episode_snort_severe_baseline_steps
        self.eval_2_episode_snort_warning_baseline_steps = eval_2_episode_snort_warning_baseline_steps
        self.episode_snort_critical_baseline_steps = episode_snort_critical_baseline_steps
        self.episode_var_log_baseline_steps = episode_var_log_baseline_steps
        self.eval_episode_snort_critical_baseline_steps = eval_episode_snort_critical_baseline_steps
        self.eval_episode_var_log_baseline_steps = eval_episode_var_log_baseline_steps
        self.eval_2_episode_var_log_baseline_steps = eval_2_episode_var_log_baseline_steps
        self.eval_2_episode_snort_critical_baseline_steps = eval_2_episode_snort_critical_baseline_steps
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
        self.start_time = start_time
        self.episode_step_baseline_rewards = episode_step_baseline_rewards
        self.episode_step_baseline_steps = episode_step_baseline_steps
        self.eval_episode_step_baseline_rewards = eval_episode_step_baseline_rewards
        self.eval_episode_step_baseline_steps = eval_episode_step_baseline_steps
        self.eval_2_episode_step_baseline_rewards = eval_2_episode_step_baseline_rewards
        self.eval_2_episode_step_baseline_steps = eval_2_episode_step_baseline_steps
        self.episode_intrusion_steps = episode_intrusion_steps
        self.eval_episode_intrusion_steps = eval_episode_intrusion_steps
        self.eval_2_episode_intrusion_steps = eval_2_episode_intrusion_steps
        self.episode_snort_severe_baseline_caught_attacker = episode_snort_severe_baseline_caught_attacker
        self.episode_snort_warning_baseline_caught_attacker = episode_snort_warning_baseline_caught_attacker
        self.eval_episode_snort_severe_baseline_caught_attacker = eval_episode_snort_severe_baseline_caught_attacker
        self.eval_episode_snort_warning_baseline_caught_attacker = eval_episode_snort_warning_baseline_caught_attacker
        self.eval_2_episode_snort_severe_baseline_caught_attacker = eval_2_episode_snort_severe_baseline_caught_attacker
        self.eval_2_episode_snort_warning_baseline_caught_attacker = eval_2_episode_snort_warning_baseline_caught_attacker
        self.episode_snort_critical_baseline_caught_attacker = episode_snort_critical_baseline_caught_attacker
        self.episode_var_log_baseline_caught_attacker = episode_var_log_baseline_caught_attacker
        self.eval_episode_snort_critical_baseline_caught_attacker = eval_episode_snort_critical_baseline_caught_attacker
        self.eval_episode_var_log_baseline_caught_attacker = eval_episode_var_log_baseline_caught_attacker
        self.eval_2_episode_var_log_baseline_caught_attacker = eval_2_episode_var_log_baseline_caught_attacker
        self.eval_2_episode_snort_critical_baseline_caught_attacker = eval_2_episode_snort_critical_baseline_caught_attacker
        self.episode_step_baseline_caught_attacker = episode_step_baseline_caught_attacker
        self.eval_episode_step_baseline_caught_attacker = eval_episode_step_baseline_caught_attacker
        self.eval_2_episode_step_baseline_caught_attacker = eval_2_episode_step_baseline_caught_attacker
        self.episode_snort_severe_baseline_early_stopping = episode_snort_severe_baseline_early_stopping
        self.episode_snort_warning_baseline_early_stopping = episode_snort_warning_baseline_early_stopping
        self.eval_episode_snort_severe_baseline_early_stopping = eval_episode_snort_severe_baseline_early_stopping
        self.eval_episode_snort_warning_baseline_early_stopping = eval_episode_snort_warning_baseline_early_stopping
        self.eval_2_episode_snort_severe_baseline_early_stopping = eval_2_episode_snort_severe_baseline_early_stopping
        self.eval_2_episode_snort_warning_baseline_early_stopping = eval_2_episode_snort_warning_baseline_early_stopping
        self.episode_snort_critical_baseline_early_stopping = episode_snort_critical_baseline_early_stopping
        self.episode_var_log_baseline_early_stopping = episode_var_log_baseline_early_stopping
        self.eval_episode_snort_critical_baseline_early_stopping = eval_episode_snort_critical_baseline_early_stopping
        self.eval_episode_var_log_baseline_early_stopping = eval_episode_var_log_baseline_early_stopping
        self.eval_2_episode_var_log_baseline_early_stopping = eval_2_episode_var_log_baseline_early_stopping
        self.eval_2_episode_snort_critical_baseline_early_stopping = eval_2_episode_snort_critical_baseline_early_stopping
        self.episode_step_baseline_early_stopping = episode_step_baseline_early_stopping
        self.eval_episode_step_baseline_early_stopping = eval_episode_step_baseline_early_stopping
        self.eval_2_episode_step_baseline_early_stopping = eval_2_episode_step_baseline_early_stopping
        self.episode_snort_severe_baseline_uncaught_intrusion_steps = episode_snort_severe_baseline_uncaught_intrusion_steps
        self.episode_snort_warning_baseline_uncaught_intrusion_steps = episode_snort_warning_baseline_uncaught_intrusion_steps
        self.eval_episode_snort_severe_baseline_uncaught_intrusion_steps = eval_episode_snort_severe_baseline_uncaught_intrusion_steps
        self.eval_episode_snort_warning_baseline_uncaught_intrusion_steps = eval_episode_snort_warning_baseline_uncaught_intrusion_steps
        self.eval_2_episode_snort_severe_baseline_uncaught_intrusion_steps = eval_2_episode_snort_severe_baseline_uncaught_intrusion_steps
        self.eval_2_episode_snort_warning_baseline_uncaught_intrusion_steps = eval_2_episode_snort_warning_baseline_uncaught_intrusion_steps
        self.episode_snort_critical_baseline_uncaught_intrusion_steps = episode_snort_critical_baseline_uncaught_intrusion_steps
        self.episode_var_log_baseline_uncaught_intrusion_steps = episode_var_log_baseline_uncaught_intrusion_steps
        self.eval_episode_snort_critical_baseline_uncaught_intrusion_steps = eval_episode_snort_critical_baseline_uncaught_intrusion_steps
        self.eval_episode_var_log_baseline_uncaught_intrusion_steps = eval_episode_var_log_baseline_uncaught_intrusion_steps
        self.eval_2_episode_var_log_baseline_uncaught_intrusion_steps = eval_2_episode_var_log_baseline_uncaught_intrusion_steps
        self.eval_2_episode_snort_critical_baseline_uncaught_intrusion_steps = eval_2_episode_snort_critical_baseline_uncaught_intrusion_steps
        self.episode_step_baseline_uncaught_intrusion_steps = episode_step_baseline_uncaught_intrusion_steps
        self.eval_episode_step_baseline_uncaught_intrusion_steps = eval_episode_step_baseline_uncaught_intrusion_steps
        self.eval_2_episode_step_baseline_uncaught_intrusion_steps = eval_2_episode_step_baseline_uncaught_intrusion_steps
        self.uncaught_intrusion_steps = uncaught_intrusion_steps
        self.eval_uncaught_intrusion_steps = eval_uncaught_intrusion_steps
        self.eval_2_uncaught_intrusion_steps = eval_2_uncaught_intrusion_steps


    def initialize(self):
        self.start_time = 0.0
        self.iteration = 0
        self.train_result = ExperimentResult()
        self.eval_result = ExperimentResult()
        self.attacker_episode_rewards = []
        self.attacker_episode_avg_loss = []
        self.attacker_lr = 0.0
        self.defender_episode_rewards = []
        self.defender_episode_avg_loss = []
        self.defender_lr = 0.0
        self.total_num_episodes = 1
        self.episode_steps = []
        self.episode_flags = []
        self.eval = False
        self.episode_flags_percentage = []
        self.progress_left = 0.0
        self.n_af = 0
        self.n_d = 0
        self.attacker_eval_episode_rewards = []
        self.defender_eval_episode_rewards = []
        self.eval_episode_steps = []
        self.eval_episode_flags = []
        self.eval_episode_flags_percentage = []
        self.attacker_eval_2_episode_rewards = []
        self.defender_eval_2_episode_rewards = []
        self.eval_2_episode_steps = []
        self.eval_2_episode_flags = []
        self.eval_2_episode_flags_percentage = []
        self.attacker_train_episode_env_specific_rewards = {}
        self.defender_train_episode_env_specific_rewards = {}
        self.train_env_specific_steps = {}
        self.train_env_specific_flags = {}
        self.train_env_specific_flags_percentage = {}
        self.attacker_eval_env_specific_rewards = {}
        self.defender_eval_env_specific_rewards = {}
        self.eval_env_specific_steps = {}
        self.eval_env_specific_flags = {}
        self.eval_env_specific_flags_percentage = {}
        self.attacker_eval_2_env_specific_rewards = {}
        self.defender_eval_2_env_specific_rewards = {}
        self.eval_2_env_specific_steps = {}
        self.eval_2_env_specific_flags = {}
        self.eval_2_env_specific_flags_percentage = {}
        self.rollout_times = []
        self.env_response_times = []
        self.action_pred_times = []
        self.grad_comp_times = []
        self.weight_update_times = []
        self.episode_caught = []
        self.episode_early_stopped = []
        self.episode_successful_intrusion = []
        self.eval_episode_caught = []
        self.eval_episode_early_stopped = []
        self.eval_episode_successful_intrusion = []
        self.eval_2_episode_caught = []
        self.eval_2_episode_early_stopped = []
        self.eval_2_episode_successful_intrusion = []
        self.snort_severe_baseline_rewards = []
        self.snort_warning_baseline_rewards = []
        self.eval_snort_severe_baseline_rewards = []
        self.eval_snort_warning_baseline_rewards = []
        self.eval_2_episode_snort_severe_baseline_rewards = []
        self.eval_2_episode_snort_warning_baseline_rewards = []
        self.episode_snort_critical_baseline_rewards = []
        self.episode_var_log_baseline_rewards = []
        self.eval_episode_snort_critical_baseline_rewards = []
        self.eval_episode_var_log_baseline_rewards = []
        self.eval_2_episode_snort_critical_baseline_rewards = []
        self.eval_2_episode_var_log_baseline_rewards = []
        self.episode_snort_warning_baseline_rewards = []
        self.episode_snort_severe_baseline_rewards = []
        self.eval_episode_snort_severe_baseline_rewards = []
        self.eval_episode_snort_warning_baseline_rewards = []
        self.snort_severe_baseline_steps = []
        self.snort_warning_baseline_steps = []
        self.eval_snort_severe_baseline_steps = []
        self.eval_snort_warning_baseline_steps = []
        self.eval_2_episode_snort_severe_baseline_steps = []
        self.eval_2_episode_snort_warning_baseline_steps = []
        self.episode_snort_critical_baseline_steps = []
        self.episode_var_log_baseline_steps = []
        self.eval_episode_snort_critical_baseline_steps = []
        self.eval_episode_var_log_baseline_steps = []
        self.eval_2_episode_snort_critical_baseline_steps = []
        self.eval_2_episode_var_log_baseline_steps = []
        self.episode_snort_warning_baseline_steps = []
        self.episode_snort_severe_baseline_steps = []
        self.eval_episode_snort_severe_baseline_steps = []
        self.eval_episode_snort_warning_baseline_steps = []
        self.attacker_action_costs = []
        self.attacker_action_costs_norm = []
        self.attacker_action_alerts = []
        self.attacker_action_alerts_norm = []
        self.eval_attacker_action_costs = []
        self.eval_attacker_action_costs_norm = []
        self.eval_attacker_action_alerts = []
        self.eval_attacker_action_alerts_norm = []
        self.eval_2_attacker_action_costs = []
        self.eval_2_attacker_action_costs_norm = []
        self.eval_2_attacker_action_alerts = []
        self.eval_2_attacker_action_alerts_norm = []
        self.episode_step_baseline_rewards = []
        self.episode_step_baseline_steps = []
        self.eval_episode_step_baseline_rewards = []
        self.eval_episode_step_baseline_steps = []
        self.eval_2_episode_step_baseline_rewards = []
        self.eval_2_episode_step_baseline_steps = []
        self.episode_intrusion_steps = []
        self.eval_episode_intrusion_steps = []
        self.eval_2_episode_intrusion_steps = []
        self.snort_severe_baseline_caught_attacker = []
        self.snort_warning_baseline_caught_attacker = []
        self.eval_snort_severe_baseline_caught_attacker = []
        self.eval_snort_warning_baseline_caught_attacker = []
        self.eval_2_episode_snort_severe_baseline_caught_attacker = []
        self.eval_2_episode_snort_warning_baseline_caught_attacker = []
        self.episode_snort_critical_baseline_caught_attacker = []
        self.episode_var_log_baseline_caught_attacker = []
        self.eval_episode_snort_critical_baseline_caught_attacker = []
        self.eval_episode_var_log_baseline_caught_attacker = []
        self.eval_2_episode_snort_critical_baseline_caught_attacker = []
        self.eval_2_episode_var_log_baseline_caught_attacker = []
        self.episode_snort_warning_baseline_caught_attacker = []
        self.episode_snort_severe_baseline_caught_attacker = []
        self.eval_episode_snort_severe_baseline_caught_attacker = []
        self.eval_episode_snort_warning_baseline_caught_attacker = []
        self.episode_step_baseline_caught_attacker = []
        self.eval_episode_step_baseline_caught_attacker = []
        self.eval_2_episode_step_baseline_caught_attacker = []
        self.snort_severe_baseline_early_stopping = []
        self.snort_warning_baseline_early_stopping = []
        self.eval_snort_severe_baseline_early_stopping = []
        self.eval_snort_warning_baseline_early_stopping = []
        self.eval_2_episode_snort_severe_baseline_early_stopping = []
        self.eval_2_episode_snort_warning_baseline_early_stopping = []
        self.episode_snort_critical_baseline_early_stopping = []
        self.episode_var_log_baseline_early_stopping = []
        self.eval_episode_snort_critical_baseline_early_stopping = []
        self.eval_episode_var_log_baseline_early_stopping = []
        self.eval_2_episode_snort_critical_baseline_early_stopping = []
        self.eval_2_episode_var_log_baseline_early_stopping = []
        self.episode_snort_warning_baseline_early_stopping = []
        self.episode_snort_severe_baseline_early_stopping = []
        self.eval_episode_snort_severe_baseline_early_stopping = []
        self.eval_episode_snort_warning_baseline_early_stopping = []
        self.episode_step_baseline_early_stopping = []
        self.eval_episode_step_baseline_early_stopping = []
        self.eval_2_episode_step_baseline_early_stopping = []
        self.snort_severe_baseline_uncaught_intrusion_steps = []
        self.snort_warning_baseline_uncaught_intrusion_steps = []
        self.eval_snort_severe_baseline_uncaught_intrusion_steps = []
        self.eval_snort_warning_baseline_uncaught_intrusion_steps = []
        self.eval_2_episode_snort_severe_baseline_uncaught_intrusion_steps = []
        self.eval_2_episode_snort_warning_baseline_uncaught_intrusion_steps = []
        self.episode_snort_critical_baseline_uncaught_intrusion_steps = []
        self.episode_var_log_baseline_uncaught_intrusion_steps = []
        self.eval_episode_snort_critical_baseline_uncaught_intrusion_steps = []
        self.eval_episode_var_log_baseline_uncaught_intrusion_steps = []
        self.eval_2_episode_snort_critical_baseline_uncaught_intrusion_steps = []
        self.eval_2_episode_var_log_baseline_uncaught_intrusion_steps = []
        self.episode_snort_warning_baseline_uncaught_intrusion_steps = []
        self.episode_snort_severe_baseline_uncaught_intrusion_steps = []
        self.eval_episode_snort_severe_baseline_uncaught_intrusion_steps = []
        self.eval_episode_snort_warning_baseline_uncaught_intrusion_steps = []
        self.episode_step_baseline_uncaught_intrusion_steps = []
        self.eval_episode_step_baseline_uncaught_intrusion_steps = []
        self.eval_2_episode_step_baseline_uncaught_intrusion_steps = []
        self.uncaught_intrusion_steps = []
        self.eval_uncaught_intrusion_steps = []
        self.eval_2_uncaught_intrusion_steps = []

    def copy(self):
        c = TrainAgentLogDTO()
        c.iteration = self.iteration
        c.train_result = self.train_result
        c.eval_result = self.eval_result
        c.attacker_episode_rewards = self.attacker_episode_rewards
        c.attacker_episode_avg_loss = self.attacker_episode_avg_loss
        c.attacker_lr = self.attacker_lr
        c.defender_episode_rewards = self.defender_episode_rewards
        c.defender_episode_avg_loss = self.defender_episode_avg_loss
        c.defender_lr = self.defender_lr
        c.total_num_episodes = self.total_num_episodes
        c.episode_steps = self.episode_steps
        c.episode_flags = self.episode_flags
        c.eval = self.eval
        c.episode_flags_percentage = self.episode_flags_percentage
        c.progress_left = self.progress_left
        c.n_af = self.n_af
        c.n_d = self.n_d
        c.attacker_eval_episode_rewards = self.attacker_eval_episode_rewards
        c.defender_eval_episode_rewards = self.defender_eval_episode_rewards
        c.eval_episode_steps = self.eval_episode_steps
        c.eval_episode_flags = self.eval_episode_flags
        c.eval_episode_flags_percentage = self.eval_episode_flags_percentage
        c.attacker_eval_2_episode_rewards = self.attacker_eval_2_episode_rewards
        c.defender_eval_2_episode_rewards = self.defender_eval_2_episode_rewards
        c.eval_2_episode_steps = self.eval_2_episode_steps
        c.eval_2_episode_flags = self.eval_2_episode_flags
        c.eval_2_episode_flags_percentage = self.eval_2_episode_flags_percentage
        c.attacker_train_episode_env_specific_rewards = self.attacker_train_episode_env_specific_rewards
        c.defender_train_episode_env_specific_rewards = self.defender_train_episode_env_specific_rewards
        c.train_env_specific_steps = self.train_env_specific_steps
        c.train_env_specific_flags = self.train_env_specific_flags
        c.train_env_specific_flags_percentage = self.train_env_specific_flags_percentage
        c.attacker_eval_env_specific_rewards = self.attacker_eval_env_specific_rewards
        c.defender_eval_env_specific_rewards = self.defender_eval_env_specific_rewards
        c.eval_env_specific_steps = self.eval_env_specific_steps
        c.eval_env_specific_flags = self.eval_env_specific_flags
        c.eval_env_specific_flags_percentage = self.eval_env_specific_flags_percentage
        c.attacker_eval_2_env_specific_rewards = self.attacker_eval_2_env_specific_rewards
        c.defender_eval_2_env_specific_rewards = self.defender_eval_2_env_specific_rewards
        c.eval_2_env_specific_steps = self.eval_2_env_specific_steps
        c.eval_2_env_specific_flags = self.eval_2_env_specific_flags
        c.eval_2_env_specific_flags_percentage = self.eval_2_env_specific_flags_percentage
        c.rollout_times = self.rollout_times
        c.env_response_times = self.env_response_times
        c.action_pred_times = self.action_pred_times
        c.grad_comp_times = self.grad_comp_times
        c.weight_update_times = self.weight_update_times
        c.episode_caught = self.episode_caught
        c.episode_early_stopped = self.episode_early_stopped
        c.episode_successful_intrusion = self.episode_successful_intrusion
        c.eval_episode_caught = self.eval_episode_caught
        c.eval_episode_early_stopped = self.eval_episode_early_stopped
        c.eval_episode_successful_intrusion = self.eval_episode_successful_intrusion
        c.eval_2_episode_caught = self.eval_2_episode_caught
        c.eval_2_episode_early_stopped = self.eval_2_episode_early_stopped
        c.eval_2_episode_successful_intrusion = self.eval_2_episode_successful_intrusion
        c.episode_snort_severe_baseline_rewards = self.episode_snort_severe_baseline_rewards
        c.episode_snort_warning_baseline_rewards = self.episode_snort_warning_baseline_rewards
        c.eval_episode_snort_severe_baseline_rewards = self.eval_episode_snort_severe_baseline_rewards
        c.eval_episode_snort_warning_baseline_rewards = self.eval_episode_snort_warning_baseline_rewards
        c.eval_2_episode_snort_severe_baseline_rewards = self.eval_2_episode_snort_severe_baseline_rewards
        c.eval_2_episode_snort_warning_baseline_rewards = self.eval_2_episode_snort_warning_baseline_rewards
        c.episode_snort_critical_baseline_rewards = self.episode_snort_critical_baseline_rewards
        c.episode_var_log_baseline_rewards = self.episode_var_log_baseline_rewards
        c.eval_episode_snort_critical_baseline_rewards = self.eval_episode_snort_critical_baseline_rewards
        c.eval_episode_var_log_baseline_rewards = self.eval_episode_var_log_baseline_rewards
        c.eval_2_episode_var_log_baseline_rewards = self.eval_2_episode_var_log_baseline_rewards
        c.eval_2_episode_snort_critical_baseline_rewards = self.eval_2_episode_snort_critical_baseline_rewards
        c.episode_snort_severe_baseline_steps = self.episode_snort_severe_baseline_steps
        c.episode_snort_warning_baseline_steps = self.episode_snort_warning_baseline_steps
        c.eval_episode_snort_severe_baseline_steps = self.eval_episode_snort_severe_baseline_steps
        c.eval_episode_snort_warning_baseline_steps = self.eval_episode_snort_warning_baseline_steps
        c.eval_2_episode_snort_severe_baseline_steps = self.eval_2_episode_snort_severe_baseline_steps
        c.eval_2_episode_snort_warning_baseline_steps = self.eval_2_episode_snort_warning_baseline_steps
        c.episode_snort_critical_baseline_steps = self.episode_snort_critical_baseline_steps
        c.episode_var_log_baseline_steps = self.episode_var_log_baseline_steps
        c.eval_episode_snort_critical_baseline_steps = self.eval_episode_snort_critical_baseline_steps
        c.eval_episode_var_log_baseline_steps = self.eval_episode_var_log_baseline_steps
        c.eval_2_episode_var_log_baseline_steps = self.eval_2_episode_var_log_baseline_steps
        c.eval_2_episode_snort_critical_baseline_steps = self.eval_2_episode_snort_critical_baseline_steps
        c.attacker_action_costs = self.attacker_action_costs
        c.attacker_action_costs_norm = self.attacker_action_costs_norm
        c.attacker_action_alerts = self.attacker_action_alerts
        c.attacker_action_alerts_norm = self.attacker_action_alerts_norm
        c.eval_attacker_action_costs = self.eval_attacker_action_costs
        c.eval_attacker_action_costs_norm = self.eval_attacker_action_costs_norm
        c.eval_attacker_action_alerts = self.eval_attacker_action_alerts
        c.eval_attacker_action_alerts_norm = self.eval_attacker_action_alerts_norm
        c.eval_2_attacker_action_costs = self.eval_2_attacker_action_costs
        c.eval_2_attacker_action_costs_norm = self.eval_2_attacker_action_costs_norm
        c.eval_2_attacker_action_alerts = self.eval_2_attacker_action_alerts
        c.eval_2_attacker_action_alerts_norm = self.eval_2_attacker_action_alerts_norm
        c.start_time = self.start_time
        c.episode_step_baseline_rewards = self.episode_step_baseline_rewards
        c.episode_step_baseline_steps = self.episode_step_baseline_steps
        c.eval_episode_step_baseline_rewards = self.eval_episode_step_baseline_rewards
        c.eval_episode_step_baseline_steps = self.eval_episode_step_baseline_steps
        c.eval_2_episode_step_baseline_rewards = self.eval_2_episode_step_baseline_rewards
        c.eval_2_episode_step_baseline_steps = self.eval_2_episode_step_baseline_steps
        c.episode_intrusion_steps = self.episode_intrusion_steps
        c.eval_episode_intrusion_steps = self.eval_episode_intrusion_steps
        c.eval_2_episode_intrusion_steps = self.eval_2_episode_intrusion_steps
        c.episode_snort_severe_baseline_caught_attacker = self.episode_snort_severe_baseline_caught_attacker
        c.episode_snort_warning_baseline_caught_attacker = self.episode_snort_warning_baseline_caught_attacker
        c.eval_episode_snort_severe_baseline_caught_attacker = self.eval_episode_snort_severe_baseline_caught_attacker
        c.eval_episode_snort_warning_baseline_caught_attacker = self.eval_episode_snort_warning_baseline_caught_attacker
        c.eval_2_episode_snort_severe_baseline_caught_attacker = self.eval_2_episode_snort_severe_baseline_caught_attacker
        c.eval_2_episode_snort_warning_baseline_caught_attacker = self.eval_2_episode_snort_warning_baseline_caught_attacker
        c.episode_snort_critical_baseline_caught_attacker = self.episode_snort_critical_baseline_caught_attacker
        c.episode_var_log_baseline_caught_attacker = self.episode_var_log_baseline_caught_attacker
        c.eval_episode_snort_critical_baseline_caught_attacker = self.eval_episode_snort_critical_baseline_caught_attacker
        c.eval_episode_var_log_baseline_caught_attacker = self.eval_episode_var_log_baseline_caught_attacker
        c.eval_2_episode_var_log_baseline_caught_attacker = self.eval_2_episode_var_log_baseline_caught_attacker
        c.eval_2_episode_snort_critical_baseline_caught_attacker = self.eval_2_episode_snort_critical_baseline_caught_attacker
        c.episode_step_baseline_caught_attacker = self.episode_step_baseline_caught_attacker
        c.eval_episode_step_baseline_caught_attacker = self.eval_episode_step_baseline_caught_attacker
        c.eval_2_episode_step_baseline_caught_attacker = self.eval_2_episode_step_baseline_caught_attacker
        c.episode_snort_severe_baseline_early_stopping = self.episode_snort_severe_baseline_early_stopping
        c.episode_snort_warning_baseline_early_stopping = self.episode_snort_warning_baseline_early_stopping
        c.eval_episode_snort_severe_baseline_early_stopping = self.eval_episode_snort_severe_baseline_early_stopping
        c.eval_episode_snort_warning_baseline_early_stopping = self.eval_episode_snort_warning_baseline_early_stopping
        c.eval_2_episode_snort_severe_baseline_early_stopping = self.eval_2_episode_snort_severe_baseline_early_stopping
        c.eval_2_episode_snort_warning_baseline_early_stopping = self.eval_2_episode_snort_warning_baseline_early_stopping
        c.episode_snort_critical_baseline_early_stopping = self.episode_snort_critical_baseline_early_stopping
        c.episode_var_log_baseline_early_stopping = self.episode_var_log_baseline_early_stopping
        c.eval_episode_snort_critical_baseline_early_stopping = self.eval_episode_snort_critical_baseline_early_stopping
        c.eval_episode_var_log_baseline_early_stopping = self.eval_episode_var_log_baseline_early_stopping
        c.eval_2_episode_var_log_baseline_early_stopping = self.eval_2_episode_var_log_baseline_early_stopping
        c.eval_2_episode_snort_critical_baseline_early_stopping = self.eval_2_episode_snort_critical_baseline_early_stopping
        c.episode_step_baseline_early_stopping = self.episode_step_baseline_early_stopping
        c.eval_episode_step_baseline_early_stopping = self.eval_episode_step_baseline_early_stopping
        c.eval_2_episode_step_baseline_early_stopping = self.eval_2_episode_step_baseline_early_stopping
        c.episode_snort_severe_baseline_uncaught_intrusion_steps = self.episode_snort_severe_baseline_uncaught_intrusion_steps
        c.episode_snort_warning_baseline_uncaught_intrusion_steps = self.episode_snort_warning_baseline_uncaught_intrusion_steps
        c.eval_episode_snort_severe_baseline_uncaught_intrusion_steps = self.eval_episode_snort_severe_baseline_uncaught_intrusion_steps
        c.eval_episode_snort_warning_baseline_uncaught_intrusion_steps = self.eval_episode_snort_warning_baseline_uncaught_intrusion_steps
        c.eval_2_episode_snort_severe_baseline_uncaught_intrusion_steps = self.eval_2_episode_snort_severe_baseline_uncaught_intrusion_steps
        c.eval_2_episode_snort_warning_baseline_uncaught_intrusion_steps = self.eval_2_episode_snort_warning_baseline_uncaught_intrusion_steps
        c.episode_snort_critical_baseline_uncaught_intrusion_steps = self.episode_snort_critical_baseline_uncaught_intrusion_steps
        c.episode_var_log_baseline_uncaught_intrusion_steps = self.episode_var_log_baseline_uncaught_intrusion_steps
        c.eval_episode_snort_critical_baseline_uncaught_intrusion_steps = self.eval_episode_snort_critical_baseline_uncaught_intrusion_steps
        c.eval_episode_var_log_baseline_uncaught_intrusion_steps = self.eval_episode_var_log_baseline_uncaught_intrusion_steps
        c.eval_2_episode_var_log_baseline_uncaught_intrusion_steps = self.eval_2_episode_var_log_baseline_uncaught_intrusion_steps
        c.eval_2_episode_snort_critical_baseline_uncaught_intrusion_steps = self.eval_2_episode_snort_critical_baseline_uncaught_intrusion_steps
        c.episode_step_baseline_uncaught_intrusion_steps = self.episode_step_baseline_uncaught_intrusion_steps
        c.eval_episode_step_baseline_uncaught_intrusion_steps = self.eval_episode_step_baseline_uncaught_intrusion_steps
        c.eval_2_episode_step_baseline_uncaught_intrusion_steps = self.eval_2_episode_step_baseline_uncaught_intrusion_steps
        c.uncaught_intrusion_steps = self.uncaught_intrusion_steps
        c.eval_uncaught_intrusion_steps = self.eval_uncaught_intrusion_steps
        c.eval_2_uncaught_intrusion_steps = self.eval_2_uncaught_intrusion_steps

    def copy_saved_env_2(self, saved_log_dto):
        self.attacker_eval_2_episode_rewards = saved_log_dto.attacker_eval_2_episode_rewards
        self.defender_eval_2_episode_rewards = saved_log_dto.defender_eval_2_episode_rewards
        self.eval_2_episode_steps = saved_log_dto.eval_2_episode_steps
        self.eval_2_episode_flags_percentage = saved_log_dto.eval_2_episode_flags_percentage
        self.eval_2_episode_flags = saved_log_dto.eval_2_episode_flags
        self.eval_2_episode_caught = saved_log_dto.eval_2_episode_caught
        self.eval_2_episode_early_stopped = saved_log_dto.eval_2_episode_early_stopped
        self.eval_2_episode_successful_intrusion = saved_log_dto.eval_2_episode_successful_intrusion
        self.eval_2_episode_snort_severe_baseline_rewards = saved_log_dto.eval_2_episode_snort_severe_baseline_rewards
        self.eval_2_episode_snort_warning_baseline_rewards = saved_log_dto.eval_2_episode_snort_warning_baseline_rewards
        self.eval_2_episode_snort_critical_baseline_rewards = saved_log_dto.eval_2_episode_snort_critical_baseline_rewards
        self.eval_2_episode_var_log_baseline_rewards = saved_log_dto.eval_2_episode_var_log_baseline_rewards
        self.eval_2_episode_step_baseline_rewards = saved_log_dto.eval_2_episode_step_baseline_rewards
        self.attacker_eval_2_env_specific_rewards = saved_log_dto.attacker_eval_2_env_specific_rewards
        self.defender_eval_2_env_specific_rewards = saved_log_dto.defender_eval_2_env_specific_rewards
        self.eval_2_episode_snort_severe_baseline_steps = saved_log_dto.eval_2_episode_snort_severe_baseline_steps
        self.eval_2_episode_snort_warning_baseline_steps = saved_log_dto.eval_2_episode_snort_warning_baseline_steps
        self.eval_2_episode_snort_critical_baseline_steps = saved_log_dto.eval_2_episode_snort_critical_baseline_steps
        self.eval_2_episode_var_log_baseline_steps = saved_log_dto.eval_2_episode_var_log_baseline_steps
        self.eval_2_episode_step_baseline_steps = saved_log_dto.eval_2_episode_step_baseline_steps
        self.eval_2_env_specific_steps = saved_log_dto.eval_2_env_specific_steps
        self.eval_2_env_specific_flags = saved_log_dto.eval_2_env_specific_flags
        self.eval_2_env_specific_flags_percentage = saved_log_dto.eval_2_env_specific_flags_percentage
        self.eval_2_attacker_action_costs = saved_log_dto.eval_2_attacker_action_costs
        self.eval_2_attacker_action_costs_norm = saved_log_dto.eval_2_attacker_action_costs_norm
        self.eval_2_attacker_action_alerts = saved_log_dto.eval_2_attacker_action_alerts
        self.eval_2_attacker_action_alerts_norm = saved_log_dto.eval_2_attacker_action_alerts_norm
        self.eval_2_episode_intrusion_steps = saved_log_dto.eval_2_episode_intrusion_steps
        self.eval_2_episode_snort_severe_baseline_caught_attacker = saved_log_dto.eval_2_episode_snort_severe_baseline_caught_attacker
        self.eval_2_episode_snort_warning_baseline_caught_attacker = saved_log_dto.eval_2_episode_snort_warning_baseline_caught_attacker
        self.eval_2_episode_snort_critical_baseline_caught_attacker = saved_log_dto.eval_2_episode_snort_critical_baseline_caught_attacker
        self.eval_2_episode_var_log_baseline_caught_attacker = saved_log_dto.eval_2_episode_var_log_baseline_caught_attacker
        self.eval_2_episode_step_baseline_caught_attacker = saved_log_dto.eval_2_episode_step_baseline_caught_attacker
        self.eval_2_episode_snort_severe_baseline_early_stopping = saved_log_dto.eval_2_episode_snort_severe_baseline_early_stopping
        self.eval_2_episode_snort_warning_baseline_early_stopping = saved_log_dto.eval_2_episode_snort_warning_baseline_early_stopping
        self.eval_2_episode_snort_critical_baseline_early_stopping = saved_log_dto.eval_2_episode_snort_critical_baseline_early_stopping
        self.eval_2_episode_var_log_baseline_early_stopping = saved_log_dto.eval_2_episode_var_log_baseline_early_stopping
        self.eval_2_episode_step_baseline_early_stopping = saved_log_dto.eval_2_episode_step_baseline_early_stopping
        self.eval_2_episode_snort_severe_baseline_uncaught_intrusion_steps = saved_log_dto.eval_2_episode_snort_severe_baseline_uncaught_intrusion_steps
        self.eval_2_episode_snort_warning_baseline_uncaught_intrusion_steps = saved_log_dto.eval_2_episode_snort_warning_baseline_uncaught_intrusion_steps
        self.eval_2_episode_snort_critical_baseline_uncaught_intrusion_steps = saved_log_dto.eval_2_episode_snort_critical_baseline_uncaught_intrusion_steps
        self.eval_2_episode_var_log_baseline_uncaught_intrusion_steps = saved_log_dto.eval_2_episode_var_log_baseline_uncaught_intrusion_steps
        self.eval_2_episode_step_baseline_uncaught_intrusion_steps = saved_log_dto.eval_2_episode_step_baseline_uncaught_intrusion_steps
        self.eval_2_uncaught_intrusion_steps = saved_log_dto.eval_2_uncaught_intrusion_steps

    def eval_update_env_specific_metrics(self, env_config, infos, i):
        if env_config.emulation_config is not None:
            agent_ip = env_config.emulation_config.agent_ip
        else:
            agent_ip = env_config.idx
        num_flags = env_config.num_flags

        if agent_ip not in self.attacker_eval_env_specific_rewards:
            self.attacker_eval_env_specific_rewards[agent_ip] = [self.attacker_episode_rewards]
        else:
            self.attacker_eval_env_specific_rewards[agent_ip].append(self.attacker_episode_rewards)

        if agent_ip not in self.defender_eval_env_specific_rewards:
            self.defender_eval_env_specific_rewards[agent_ip] = [self.defender_episode_rewards]
        else:
            self.defender_eval_env_specific_rewards[agent_ip].append(self.defender_episode_rewards)

        if agent_ip not in self.eval_env_specific_steps:
            self.eval_env_specific_steps[agent_ip] = [self.episode_steps]
        else:
            self.eval_env_specific_steps[agent_ip].append(self.episode_steps)

        if agent_ip not in self.eval_env_specific_flags:
            self.eval_env_specific_flags[agent_ip] = [infos["flags"]]
        else:
            self.eval_env_specific_flags[agent_ip].append(infos["flags"])

        if agent_ip not in self.eval_env_specific_flags_percentage:
            self.eval_env_specific_flags_percentage[agent_ip] = [infos["flags"] / num_flags]
        else:
            self.eval_env_specific_flags_percentage[agent_ip].append(infos["flags"] / num_flags)

    def eval_2_update_env_specific_metrics(self, env_config, infos, i):

        if env_config.emulation_config is not None:
            agent_ip = env_config.emulation_config.agent_ip
        else:
            agent_ip = env_config.idx
        num_flags = env_config.num_flags

        if agent_ip not in self.attacker_eval_2_env_specific_rewards:
            self.attacker_eval_2_env_specific_rewards[agent_ip] = [self.attacker_episode_rewards]
        else:
            self.attacker_eval_2_env_specific_rewards[agent_ip].append(self.attacker_episode_rewards)

        if agent_ip not in self.defender_eval_2_env_specific_rewards:
            self.defender_eval_2_env_specific_rewards[agent_ip] = [self.defender_episode_rewards]
        else:
            self.defender_eval_2_env_specific_rewards[agent_ip].append(self.defender_episode_rewards)

        if agent_ip not in self.eval_2_env_specific_steps:
            self.eval_2_env_specific_steps[agent_ip] = [self.episode_steps]
        else:
            self.eval_2_env_specific_steps[agent_ip].append(self.episode_steps)

        if agent_ip not in self.eval_2_env_specific_flags:
            self.eval_2_env_specific_flags[agent_ip] = [infos["flags"]]
        else:
            self.eval_2_env_specific_flags[agent_ip].append(infos["flags"])

        if agent_ip not in self.eval_2_env_specific_flags_percentage:
            self.eval_2_env_specific_flags_percentage[agent_ip] = [infos["flags"] / num_flags]
        else:
            self.eval_2_env_specific_flags_percentage[agent_ip].append(infos["flags"] / num_flags)







