"""
Experiment results
"""
from typing import List
import csv

class ExperimentResult:
    """
    DTO with experiment result from an experiment in the pycr-pwcrack-envs
    """

    def __init__(self, avg_episode_rewards: List[float] = None,
                 avg_episode_rewards_a: List[float] = None,
                 avg_episode_steps: List[int] = None, epsilon_values: List[float] = None,
                 cumulative_reward: List[int] = None, avg_episode_loss: List[float] = None,
                 lr_list : List[float] = None, avg_episode_flags : List[int] = None,
                 avg_episode_flags_percentage: List[float] = None,
                 eval_avg_episode_rewards : List[float] = None,
                 eval_avg_episode_steps: List[float] = None,
                 eval_avg_episode_flags: List[int] = None,
                 eval_avg_episode_flags_percentage: List[float] = None,
                 eval_2_avg_episode_rewards: List[float] = None,
                 eval_2_avg_episode_steps: List[float] = None,
                 eval_2_avg_episode_flags: List[int] = None,
                 eval_2_avg_episode_flags_percentage: List[float] = None,
                 train_env_specific_rewards: dict = None,
                 train_env_specific_steps: dict = None,
                 train_env_specific_flags: dict = None,
                 train_env_specific_flags_percentage: dict = None,
                 eval_env_specific_rewards: dict = None,
                 eval_env_specific_steps: dict = None,
                 eval_env_specific_flags: dict = None,
                 eval_env_specific_flags_percentage: dict = None,
                 eval_2_env_specific_rewards: dict = None,
                 eval_2_env_specific_steps: dict = None,
                 eval_2_env_specific_flags: dict = None,
                 eval_2_env_specific_flags_percentage: dict = None,
                 rollout_times : List = None, env_response_times : List = None,
                 action_pred_times : List = None, grad_comp_times : List = None,
                 weight_update_times : List = None,
                 avg_regret: List = None, avg_opt_frac : List = None
                 ):
        """
        Constructor, initializes the DTO

        :param avg_episode_rewards: list of episode rewards for attacker
        :param avg_episode_steps: list of episode steps
        :param epsilon_values: list of epsilon values
        :param cumulative_reward: list of attacker cumulative rewards
        :param avg_episode_loss: average loss for attacker
        :param lr_list: learning rates
        :param avg_episode_flags: avg number of flags catched per episode
        :param avg_episode_flags_percentage: avg % of flags catched per episode
        :param eval_avg_episode_rewards: list of episode rewards for eval deterministic
        :param eval_avg_episode_steps: list of episode steps for eval deterministic
        :param eval_avg_episode_flags: list of episode flags for eval deterministic
        :param eval_avg_episode_flags_percentage: list of episode flags for eval deterministic
        :param eval_2_avg_episode_rewards: list of episode rewards for second eval env deterministic
        :param eval_2_avg_episode_steps: list of episode steps for second eval enveval deterministic
        :param eval_2_avg_episode_flags: list of episode flags for second eval enveval deterministic
        :param eval_2_avg_episode_flags_percentage: list of episode flags for second eval env eval deterministic
        :param train_env_specific_rewards: rewards data for specific train env
        :param train_env_specific_flags: flags data for specific train env
        :param train_env_specific_steps: steps data for specific train env
        :param train_env_specific_flags_percentage: flags percentage for specific train env
        :param eval_env_specific_rewards: eval reward data for specific train env deterministic
        :param eval_env_specific_flags: eval flags data for specific train env deterministic
        :param eval_env_specific_flags_percentage: eval flags percentage data for specific train env deterministic
        :param eval_env_specific_steps: eval steps data for specific train env deterministic
        :param eval_2_env_specific_rewards: eval reward data for specific eval env deterministic
        :param eval_2_env_specific_flags: eval flags data for specific eval env deterministic
        :param eval_2_env_specific_flags_percentage: eval flags percentage dat2a for specific eval env deterministic
        :param eval_2_env_specific_steps: eval steps data for specific eval env env deterministic
        """
        self.avg_episode_rewards = avg_episode_rewards
        self.avg_episode_rewards_a = avg_episode_rewards_a
        self.avg_episode_steps = avg_episode_steps
        self.epsilon_values = epsilon_values
        self.cumulative_reward = cumulative_reward
        self.avg_episode_loss = avg_episode_loss
        self.lr_list = lr_list
        self.avg_episode_flags = avg_episode_flags
        self.avg_episode_flags_percentage = avg_episode_flags_percentage
        self.eval_avg_episode_rewards = eval_avg_episode_rewards
        self.eval_avg_episode_steps = eval_avg_episode_steps
        self.eval_avg_episode_flags = eval_avg_episode_flags
        self.eval_avg_episode_flags_percentage = eval_avg_episode_flags_percentage
        self.eval_2_avg_episode_rewards = eval_2_avg_episode_rewards
        self.eval_2_avg_episode_steps = eval_2_avg_episode_steps
        self.eval_2_avg_episode_flags = eval_2_avg_episode_flags
        self.eval_2_avg_episode_flags_percentage = eval_2_avg_episode_flags_percentage
        self.train_env_specific_rewards = train_env_specific_rewards
        self.train_env_specific_flags = train_env_specific_flags
        self.train_env_specific_steps = train_env_specific_steps
        self.train_env_specific_flags_percentage = train_env_specific_flags_percentage
        self.eval_env_specific_rewards = eval_env_specific_rewards
        self.eval_env_specific_flags = eval_env_specific_flags
        self.eval_env_specific_steps = eval_env_specific_steps
        self.eval_env_specific_flags_percentage = eval_env_specific_flags_percentage
        self.eval_2_env_specific_rewards = eval_2_env_specific_rewards
        self.eval_2_env_specific_flags = eval_2_env_specific_flags
        self.eval_2_env_specific_steps = eval_2_env_specific_steps
        self.eval_2_env_specific_flags_percentage = eval_2_env_specific_flags_percentage
        self.rollout_times = rollout_times
        self.env_response_times = env_response_times
        self.action_pred_times = action_pred_times
        self.grad_comp_times = grad_comp_times
        self.weight_update_times = weight_update_times
        self.avg_opt_frac = avg_opt_frac
        self.avg_regret = avg_regret
        if avg_episode_steps is None:
            self.avg_episode_steps = []
        if avg_episode_rewards is None:
            self.avg_episode_rewards = []
        if avg_episode_rewards_a is None:
            self.avg_episode_rewards_a = []
        if epsilon_values is None:
            self.epsilon_values = []
        if cumulative_reward is None:
            self.cumulative_reward = []
        if avg_episode_loss is None:
            self.avg_episode_loss = []
        if lr_list is None:
            self.lr_list = []
        if avg_episode_flags is None:
            self.avg_episode_flags = []
        if avg_episode_flags_percentage is None:
            self.avg_episode_flags_percentage = []
        if eval_avg_episode_rewards is None:
            self.eval_avg_episode_rewards = []
        if eval_avg_episode_steps is None:
            self.eval_avg_episode_steps = []
        if eval_avg_episode_flags is None:
            self.eval_avg_episode_flags = []
        if eval_avg_episode_flags_percentage is None:
            self.eval_avg_episode_flags_percentage = []
        if eval_2_avg_episode_rewards is None:
            self.eval_2_avg_episode_rewards = []
        if eval_2_avg_episode_steps is None:
            self.eval_2_avg_episode_steps = []
        if eval_2_avg_episode_flags is None:
            self.eval_2_avg_episode_flags = []
        if eval_2_avg_episode_flags_percentage is None:
            self.eval_2_avg_episode_flags_percentage = []
        if train_env_specific_rewards is None:
            self.train_env_specific_rewards = {}
        if train_env_specific_steps is None:
            self.train_env_specific_steps = {}
        if train_env_specific_flags is None:
            self.train_env_specific_flags = {}
        if train_env_specific_flags_percentage is None:
            self.train_env_specific_flags_percentage = {}
        if eval_env_specific_rewards is None:
            self.eval_env_specific_rewards = {}
        if eval_env_specific_steps is None:
            self.eval_env_specific_steps = {}
        if eval_env_specific_flags is None:
            self.eval_env_specific_flags = {}
        if eval_env_specific_flags_percentage is None:
            self.eval_env_specific_flags_percentage = {}
        if eval_2_env_specific_rewards is None:
            self.eval_2_env_specific_rewards = {}
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
        if avg_regret is None:
            self.avg_regret = []
        if avg_opt_frac is None:
            self.avg_opt_frac = []

    def to_csv(self, file_path : str) -> None:
        """
        Save result to csv

        :param file_path: path to save the csv file
        :return: None
        """
        metrics = [self.avg_episode_rewards, self.avg_episode_rewards_a, self.avg_episode_steps, self.epsilon_values,
                   self.cumulative_reward, self.avg_episode_loss, self.lr_list, self.avg_episode_flags,
                   self.avg_episode_flags_percentage, self.eval_avg_episode_rewards, self.eval_avg_episode_steps,
                   self.eval_avg_episode_flags, self.eval_avg_episode_flags_percentage,
                   self.eval_2_avg_episode_rewards, self.eval_2_avg_episode_steps,
                   self.eval_2_avg_episode_flags, self.eval_2_avg_episode_flags_percentage, self.rollout_times,
                   self.env_response_times, self.action_pred_times, self.grad_comp_times, self.weight_update_times,
                   self.avg_regret, self.avg_opt_frac
                   ]
        metric_labels = ["avg_episode_rewards", "avg_episode_rewards_a", "avg_episode_steps",
                         "epsilon_values", "cumulative_reward", "avg_episode_loss",
                         "lr_list", "avg_episode_flags", "avg_episode_flags_percentage", "eval_avg_episode_rewards",
                         "eval_avg_episode_steps", "eval_avg_episode_flags", "eval_avg_episode_flags_percentage",
                         "eval_2_avg_episode_rewards", "eval_2_avg_episode_steps", "eval_2_avg_episode_flags",
                         "eval_2_avg_episode_flags_percentage", "rollout_times", "env_response_times", "action_pred_times",
                         "grad_comp_times", "weight_update_times", "avg_regret", "avg_opt_frac"
                         ]
        filtered_metric_labels = []
        filtered_metrics = []
        for i in range(len(metrics)):
            if len(metrics[i]) > 0:
                filtered_metrics.append(metrics[i])
                filtered_metric_labels.append(metric_labels[i])
        for key in self.train_env_specific_rewards.keys():
            if len(self.train_env_specific_rewards[key]) > 0:
                filtered_metrics.append(self.train_env_specific_rewards[key])
                filtered_metric_labels.append(str(key) + "_" + "avg_episode_rewards")
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
        for key in self.eval_env_specific_rewards.keys():
            if len(self.eval_env_specific_rewards[key]) > 0:
                filtered_metrics.append(self.eval_env_specific_rewards[key])
                filtered_metric_labels.append(str(key) + "_" + "eval_avg_episode_rewards")
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
        for key in self.eval_2_env_specific_rewards.keys():
            if len(self.eval_2_env_specific_rewards[key]) > 0:
                filtered_metrics.append(self.eval_2_env_specific_rewards[key])
                filtered_metric_labels.append(str(key) + "_" + "eval_2_avg_episode_rewards")
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

        rows = zip(*filtered_metrics)
        with open(file_path, "w") as f:
            writer = csv.writer(f)
            writer.writerow(filtered_metric_labels)
            for row in rows:
                writer.writerow(row)